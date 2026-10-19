"""Result bundles: one directory per run, written by `mengine-bench run`.

Layout:
    results/<suite>/<date>_<agent>_<model>_<effort>_<run id>/
        result.json                  scores, per-task data, environment
        summary.md                   human summary
        transcripts/<task>.jsonl.gz  raw agent output per step

Everything in a bundle is public once merged, so every text passes the secret
and local-path redaction first.
"""

from __future__ import annotations

import gzip
import io
import json
import re
import shutil
import subprocess
from collections.abc import Mapping, MutableMapping
from pathlib import Path

from mengine_bench.redact import LocalNames, PathScope, local_names, redact_paths, redact_text, redact_value
from mengine_bench.report import render_summary

RESULT_NAME = "result.json"
SUMMARY_NAME = "summary.md"
_STEP_FILE = re.compile(r"^step-(?P<label>.+)\.(?P<stream>stdout|stderr)\.txt$")
REPO_ROOT = Path(__file__).resolve().parents[1]


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


def write_bundle(results: MutableMapping[str, object], out_root: Path, transcripts: Mapping[str, Path],
                 scope: PathScope) -> Path:
    """Write the bundle for `results`; `transcripts` maps a task id to its raw transcript dir."""
    agent = results["agent"]
    tasks = results["tasks"]
    assert isinstance(agent, dict) and isinstance(tasks, list)
    name = bundle_dir_name(str(results["date"]), str(agent["name"]), str(agent["model"]),
                           agent.get("effort"), str(results["run_id"]))
    bundle_dir = out_root / str(results["suite"]) / name
    (bundle_dir / "transcripts").mkdir(parents=True, exist_ok=False)
    for task in tasks:
        source = transcripts.get(task["id"])
        task["transcript"] = None
        if source is None:
            continue
        transcript = f"transcripts/{task['id']}.jsonl.gz"
        (bundle_dir / transcript).write_bytes(_gzip(transcript_jsonl(source, scope)))
        task["transcript"] = transcript
    public = redact_value(json.loads(redact_paths(json.dumps(results), scope)))
    assert isinstance(public, dict)
    (bundle_dir / RESULT_NAME).write_text(json.dumps(public, indent=2, ensure_ascii=False) + "\n",
                                          encoding="utf-8", newline="\n")
    (bundle_dir / SUMMARY_NAME).write_text(public_text(render_summary(public), scope), encoding="utf-8",
                                           newline="\n")
    return bundle_dir
