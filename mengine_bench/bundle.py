"""Result bundles: one self-contained, auditable directory per run.

Layout (docs/SUBMITTING.md):
    results/<suite>/<date>_<agent>_<model>_<effort>_<run id>/
        result.json                  scores, raw per-task data, environment
        summary.md                   human summary
        transcripts/<task>.jsonl.gz  raw agent output per step, redacted
        workspaces/<task>.tar.gz     final workspace, so verify can re-grade
        MANIFEST.sha256              sha256 of every other file

Archives are byte-deterministic (sorted members, zeroed mtimes and owners) so
the same run always hashes the same.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import re
import shutil
import subprocess
import tarfile
from collections.abc import Mapping, MutableMapping
from dataclasses import dataclass
from pathlib import Path

from mengine_bench.redact import (
    LocalNames, PathScope, find_secrets, local_names, redact_paths, redact_text, redact_value,
)
from mengine_bench.report import render_summary

MANIFEST_NAME = "MANIFEST.sha256"
# Left in the raw run dir (never published) for `mengine-bench rebundle`.
RAW_RUN_NAME = "run.json"
# Per-task fields verify re-grades byte-exact; name tokens must not rewrite them.
GRADED_KEYS = ("answers", "checks")
RESULT_NAME = "result.json"
SUMMARY_NAME = "summary.md"
# Per-file cap inside a workspace archive; bigger files are listed as excluded.
WORKSPACE_FILE_CAP = 1 * 2**20
# Whole bundle cap, enforced by verify and the results workflow.
BUNDLE_SIZE_CAP = 25 * 2**20
# Browser user-data dirs an agent (or an older bench) left in the workspace;
# their cache files can stay locked by a live browser.
BROWSER_PROFILE_DIRS = frozenset({"_browser-profile", ".browser-profile", "browser-profile", ".verify-profile",
                                  "verify-profile", ".chrome-profile", "chrome-profile", ".edge-profile",
                                  "edge-profile", "user-data-dir", ".user-data-dir"})
# Caches, dependency trees and grading scratch: never part of the solution.
EXCLUDED_DIRS = frozenset({".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache",
                           ".mypy_cache", ".ruff_cache", ".cache", "vision-judge"}) | BROWSER_PROFILE_DIRS
_STEP_FILE = re.compile(r"^step-(?P<label>.+)\.(?P<stream>stdout|stderr)\.txt$")
REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class TaskArtifacts:
    """Where a task run left its raw transcripts and final workspace."""

    transcripts: Path
    workspace: Path | None


def _slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9.]+", "-", text).strip("-") or "unknown"


def bundle_dir_name(date: str, agent: str, model: str, effort: str | None, run_id: str) -> str:
    return "_".join([date, _slug(agent), _slug(model), _slug(effort or "none"), _slug(run_id)])


def bench_commit(root: Path = REPO_ROOT) -> dict[str, object]:
    """HEAD of the bench checkout and whether its tree was dirty (None outside git)."""
    git = shutil.which("git")
    unknown: dict[str, object] = {"sha": None, "dirty": None}
    if git is None or not (root / ".git").exists():
        return unknown
    try:
        head = subprocess.run([git, "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, timeout=30,
                              check=False)
        status = subprocess.run([git, "status", "--porcelain"], cwd=root, capture_output=True, text=True,
                                timeout=60, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return unknown
    if head.returncode or status.returncode:
        return unknown
    return {"sha": head.stdout.strip(), "dirty": bool(status.stdout.strip())}


def run_scope(work: Path, names: LocalNames | None = None) -> PathScope:
    """Everything local a run under `work` must scrub: its step workspaces, the run dir, this machine's names."""
    workspaces = tuple(sorted(path for path in work.glob("*/step-*") if path.is_dir()))
    return PathScope(workspaces=workspaces, workdirs=(work,), names=local_names() if names is None else names)


def public_text(text: str, scope: PathScope) -> str:
    return redact_text(redact_paths(text, scope))


def without_graded(result: Mapping[str, object]) -> dict[str, object]:
    """`result` minus the graded fields that verify re-derives byte-exact."""
    tasks = result.get("tasks")
    trimmed = [{k: v for k, v in task.items() if k not in GRADED_KEYS} for task in tasks] \
        if isinstance(tasks, list) else tasks
    return {**result, "tasks": trimmed}


def _public_result(results: Mapping[str, object], scope: PathScope) -> dict[str, object]:
    # Answers and check names are re-graded by verify, so a user name that is
    # also a task word (fixtures use first names) must not rewrite them; paths
    # and secrets still go.
    paths_only = PathScope(workspaces=scope.workspaces, workdirs=scope.workdirs)
    public = redact_value(json.loads(redact_paths(json.dumps(results), paths_only)))
    assert isinstance(public, dict)
    graded = [{k: task[k] for k in GRADED_KEYS if k in task} for task in public["tasks"]]
    public = json.loads(redact_paths(json.dumps(without_graded(public)), scope))
    for task, kept in zip(public["tasks"], graded):
        task.update(kept)
    return public


def _gzip(raw: bytes) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", mtime=0) as stream:
        stream.write(raw)
    return buffer.getvalue()


def transcript_jsonl(transcripts: Path, scope: PathScope) -> bytes:
    """One JSON line per step and stream; raw output stays inside `text`."""
    lines: list[str] = []
    files = sorted(transcripts.glob("step-*.txt")) if transcripts.is_dir() else []
    for path in files:
        match = _STEP_FILE.match(path.name)
        if match is None:
            continue
        text = public_text(path.read_text(encoding="utf-8", errors="replace"), scope)
        lines.append(json.dumps({"step": match["label"], "stream": match["stream"], "text": text},
                                ensure_ascii=False))
    return ("\n".join(lines) + "\n" if lines else "").encode("utf-8")


def _workspace_members(workspace: Path) -> tuple[list[tuple[str, bytes]], list[dict[str, str]]]:
    kept: list[tuple[str, bytes]] = []
    excluded: list[dict[str, str]] = []
    for path in sorted(workspace.rglob("*")):
        rel = path.relative_to(workspace)
        if any(part in EXCLUDED_DIRS for part in rel.parts) or path.is_dir():
            continue
        name = rel.as_posix()
        if path.is_symlink() or not path.is_file():
            excluded.append({"path": name, "reason": "not a regular file"})
            continue
        # One locked file must not fail the whole run's bundle.
        try:
            oversized = path.stat().st_size > WORKSPACE_FILE_CAP
            body = b"" if oversized else path.read_bytes()
        except OSError as error:
            excluded.append({"path": name, "reason": f"unreadable: {type(error).__name__}"})
            continue
        if oversized:
            excluded.append({"path": name, "reason": f"over {WORKSPACE_FILE_CAP} bytes"})
            continue
        # Workspaces stay byte-exact for re-grading, so a file with a secret
        # is dropped rather than rewritten.
        if find_secrets(body.decode("utf-8", errors="replace")):
            excluded.append({"path": name, "reason": "secret-like content"})
            continue
        kept.append((name, body))
    return kept, excluded


def workspace_archive(workspace: Path) -> tuple[bytes, dict[str, object]]:
    kept, excluded = _workspace_members(workspace)
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for name, body in kept:
            info = tarfile.TarInfo(name)
            info.size, info.mode, info.mtime = len(body), 0o644, 0
            archive.addfile(info, io.BytesIO(body))
    summary: dict[str, object] = {"files": len(kept), "bytes": sum(len(body) for _, body in kept),
                                  "excluded": excluded}
    return _gzip(raw.getvalue()), summary


def manifest_lines(bundle_dir: Path) -> list[str]:
    lines = []
    for path in sorted(bundle_dir.rglob("*")):
        rel = path.relative_to(bundle_dir).as_posix()
        if path.is_file() and rel != MANIFEST_NAME:
            lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {rel}")
    return lines


def write_manifest(bundle_dir: Path) -> Path:
    path = bundle_dir / MANIFEST_NAME
    path.write_text("\n".join(manifest_lines(bundle_dir)) + "\n", encoding="utf-8", newline="\n")
    return path


def write_bundle(results: MutableMapping[str, object], out_root: Path,
                 artifacts: Mapping[str, TaskArtifacts], scope: PathScope) -> Path:
    """Write the bundle for `results`; every text in it passes `public_text` with `scope`."""
    agent = results["agent"]
    tasks = results["tasks"]
    assert isinstance(agent, dict) and isinstance(tasks, list)
    name = bundle_dir_name(str(results["date"]), str(agent["name"]), str(agent["model"]),
                           agent.get("effort"), str(results["run_id"]))
    bundle_dir = out_root / str(results["suite"]) / name
    bundle_dir.mkdir(parents=True, exist_ok=False)
    (bundle_dir / "transcripts").mkdir()
    (bundle_dir / "workspaces").mkdir()
    for task in tasks:
        source = artifacts.get(task["id"])
        task["transcript"] = None
        task["workspace"] = None
        if source is None:
            continue
        transcript = f"transcripts/{task['id']}.jsonl.gz"
        (bundle_dir / transcript).write_bytes(_gzip(transcript_jsonl(source.transcripts, scope)))
        task["transcript"] = transcript
        if source.workspace is not None and source.workspace.is_dir():
            archive, summary = workspace_archive(source.workspace)
            task["workspace"] = {"archive": f"workspaces/{task['id']}.tar.gz", **summary}
            (bundle_dir / str(task["workspace"]["archive"])).write_bytes(archive)
    public = _public_result(results, scope)
    (bundle_dir / RESULT_NAME).write_text(json.dumps(public, indent=2, ensure_ascii=False) + "\n",
                                          encoding="utf-8", newline="\n")
    (bundle_dir / SUMMARY_NAME).write_text(public_text(render_summary(public), scope), encoding="utf-8",
                                           newline="\n")
    write_manifest(bundle_dir)
    return bundle_dir


def save_raw_run(work: Path, results: Mapping[str, object], artifacts: Mapping[str, TaskArtifacts]) -> Path:
    """Keep the recorded run next to its transcripts so `rebundle` never reruns agents or judges."""
    stored = {task_id: {"transcripts": art.transcripts.relative_to(work).as_posix(),
                        "workspace": None if art.workspace is None else art.workspace.relative_to(work).as_posix()}
              for task_id, art in artifacts.items()}
    path = work / RAW_RUN_NAME
    path.write_text(json.dumps({"results": results, "artifacts": stored}, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8", newline="\n")
    return path


def _last_step_dir(task_dir: Path) -> Path | None:
    steps = [path for path in task_dir.glob("step-*") if path.is_dir() and path.name[5:].isdigit()]
    return max(steps, key=lambda path: int(path.name[5:]), default=None)


def load_raw_run(raw: Path, result_file: Path | None = None) -> tuple[dict[str, object], dict[str, TaskArtifacts]]:
    """Recorded results and artifacts of a raw run dir.

    Runs older than run.json kept transcripts and workspaces but not the
    recorded data; `result_file` (the old bundle's result.json) supplies it,
    and the final workspace is the highest `step-<n>` dir.
    """
    stored_file = raw / RAW_RUN_NAME
    if stored_file.is_file():
        stored = json.loads(stored_file.read_text(encoding="utf-8"))
        artifacts = {task_id: TaskArtifacts(transcripts=raw / entry["transcripts"],
                                            workspace=None if entry["workspace"] is None else raw / entry["workspace"])
                     for task_id, entry in stored["artifacts"].items()}
        return stored["results"], artifacts
    if result_file is None:
        raise FileNotFoundError(f"received raw run dir without {RAW_RUN_NAME} (the recorded scores, checks, timings "
                                f"and judge votes; runs before bench 'rebundle' did not store it); expected it, or "
                                f"--result <old bundle>/result.json to take that data from")
    results = json.loads(result_file.read_text(encoding="utf-8"))
    artifacts = {str(task["id"]): TaskArtifacts(transcripts=raw / str(task["id"]) / "transcripts",
                                                workspace=_last_step_dir(raw / str(task["id"])))
                 for task in results["tasks"] if (raw / str(task["id"])).is_dir()}
    return results, artifacts
