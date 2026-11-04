"""Result bundles: one directory per run, written by `mengine-bench run`.

Layout:
    results/<date>_<agent>_<model>_<effort>_<run id>/
        result.json                  scores, per-task data, environment
        summary.md                   human summary
        transcripts/<task>.jsonl.gz  raw agent output per step
        judge/<task>.json            judge evidence for `mengine-bench judge`
        judge/<task>/<file>          each declared deliverable, verbatim after redaction
        evidence/<task>/<file>       human-only media, verbatim bytes, privacy scanned

Everything in a bundle is public once merged. Text passes secret and local-path
redaction; opaque media stays verbatim and still passes the privacy scan (#165).
"""

from __future__ import annotations

import gzip
import io
import json
import re
import shutil
import stat
import subprocess
from collections.abc import Mapping, MutableMapping
from pathlib import Path

from mengine_bench.redact import (
    LocalNames, PathScope, find_leaks, local_names, redact_paths, redact_text, redact_value,
)
from mengine_bench.report import render_summary

RESULT_NAME = "result.json"
SUMMARY_NAME = "summary.md"
JUDGE_DIR = "judge"
EVIDENCE_FILE_BYTES = 5 * 1024 * 1024
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
        # results/ holds this clone's own bundles (left untracked by `submit`); they change no bench code.
        status = subprocess.run([git, "status", "--porcelain", "--", ".", ":(exclude)results"], cwd=root,
                                capture_output=True, text=True, timeout=60, check=False)
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


def public_json(value: object, scope: PathScope) -> object:
    return redact_value(json.loads(redact_paths(json.dumps(value), scope)))


def write_bundle(results: MutableMapping[str, object], out_root: Path, transcripts: Mapping[str, Path],
                 scope: PathScope, packets: Mapping[str, Mapping[str, object]] | None = None,
                 deliverables: Mapping[str, Mapping[str, Path]] | None = None,
                 evidence: Mapping[str, Mapping[str, Path]] | None = None) -> Path:
    """Write the bundle for `results`; `transcripts` maps a task id to its raw transcript dir,
    `packets` holds the judge evidence; `deliverables` and human-only `evidence` map task ids to {relative path: file}."""
    agent = results["agent"]
    tasks = results["tasks"]
    assert isinstance(agent, dict) and isinstance(tasks, list)
    name = bundle_dir_name(str(results["date"]), str(agent["name"]), str(agent["model"]),
                           agent.get("effort"), str(results["run_id"]))
    bundle_dir = out_root / name
    (bundle_dir / "transcripts").mkdir(parents=True, exist_ok=False)
    for task in tasks:
        source = transcripts.get(task["id"])
        task["transcript"] = None
        if source is None:
            continue
        transcript = f"transcripts/{task['id']}.jsonl.gz"
        (bundle_dir / transcript).write_bytes(_gzip(transcript_jsonl(source, scope)))
        task["transcript"] = transcript
    for task_id, packet in (packets or {}).items():
        (bundle_dir / JUDGE_DIR).mkdir(exist_ok=True)
        (bundle_dir / JUDGE_DIR / f"{task_id}.json").write_text(
            json.dumps(public_json(packet, scope), indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
            newline="\n")
    for task_id, files in (deliverables or {}).items():
        _write_deliverables(bundle_dir / JUDGE_DIR / task_id, files, scope)
    for task in tasks:
        notes = _write_evidence(bundle_dir / "evidence" / task["id"], (evidence or {}).get(task["id"], {}), scope)
        if notes:
            task.setdefault("flags", []).extend(notes)
    public = public_json(results, scope)
    assert isinstance(public, dict)
    (bundle_dir / RESULT_NAME).write_text(json.dumps(public, indent=2, ensure_ascii=False) + "\n",
                                          encoding="utf-8", newline="\n")
    (bundle_dir / SUMMARY_NAME).write_text(public_text(render_summary(public), scope), encoding="utf-8",
                                           newline="\n")
    return bundle_dir


def _evidence_file_problem(source: Path, workspace: Path) -> str | None:
    relative = source.relative_to(workspace)
    ancestors = [source, *(source.parents[index] for index in range(len(relative.parts)))]
    if any(path.is_symlink() or getattr(path.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
           for path in ancestors):
        return "symlink or junction"
    if not source.resolve().is_relative_to(workspace.resolve()):
        return "file outside the workspace"
    if not source.is_file():
        return "missing or nonregular file"
    if source.stat().st_size > EVIDENCE_FILE_BYTES:
        return f"file of {source.stat().st_size} bytes"
    return None


def _write_evidence(target: Path, files: Mapping[str, Path], scope: PathScope) -> list[str]:
    """#165: preserve human media bytes; unsafe or oversized files leave public skip notes."""
    notes: list[str] = []
    for relative, source in files.items():
        try:
            workspace = next((root for root in scope.workspaces if source.is_relative_to(root)), None)
            problem = "file outside the workspace" if workspace is None else _evidence_file_problem(source, workspace)
            dest = target / relative
            if not dest.resolve().is_relative_to(target.resolve()):
                problem = "path outside the evidence directory"
            if problem:
                raise ValueError(problem)
            # Bound the read too, since the agent could have left a writer running (#165).
            with source.open("rb") as stream:
                raw = stream.read(EVIDENCE_FILE_BYTES + 1)
            if len(raw) > EVIDENCE_FILE_BYTES:
                raise ValueError(f"file of more than {EVIDENCE_FILE_BYTES} bytes")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
        except (OSError, ValueError) as error:
            received = str(error) if isinstance(error, ValueError) else type(error).__name__
            notes.append(f"evidence {relative!r} skipped: received {received}; expected a regular workspace file "
                         f"without symlinks, at most {EVIDENCE_FILE_BYTES} bytes")
    return notes


def _write_deliverables(target: Path, files: Mapping[str, Path], scope: PathScope) -> None:
    """Store each deliverable under its workspace-relative path, redacted like every other text."""
    for relative, source in files.items():
        if not source.is_file():
            continue
        dest = target / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        if is_image_deliverable(relative):
            # #153: an image the judge must see; bundle_leaks still scans its text chunks.
            dest.write_bytes(source.read_bytes())
            continue
        text = source.read_text(encoding="utf-8", errors="replace")
        dest.write_text(public_text(text, scope), encoding="utf-8", newline="")


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
IMAGE_DELIVERABLE_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp")


def is_image_deliverable(relative: str) -> bool:
    return relative.lower().endswith(IMAGE_DELIVERABLE_SUFFIXES)


def _without_png_pixels(raw: bytes) -> bytes:
    """Compressed pixels fit text patterns by chance (#42); the PNG's text chunks still get scanned."""
    if not raw.startswith(PNG_SIGNATURE):
        return raw
    kept, offset = [], len(PNG_SIGNATURE)
    while offset < len(raw):
        end = offset + 12 + int.from_bytes(raw[offset:offset + 4], "big")
        if raw[offset + 4:offset + 8] != b"IDAT":
            kept.append(raw[offset:end])
        offset = end
    return b"".join(kept)


def bundle_leaks(bundle_dir: Path, names: LocalNames) -> dict[str, dict[str, int]]:
    """Per file, what redaction missed (counts only: the output is pasted into PRs)."""
    found: dict[str, dict[str, int]] = {}
    for path in sorted(bundle_dir.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(bundle_dir)
        raw = path.read_bytes()
        # #165: evidence is opaque bytes even with a .gz name; scan its text chunks like image deliverables.
        if path.suffix == ".gz" and relative.parts[0] != "evidence":
            raw = gzip.decompress(raw)
        leaks = find_leaks(_without_png_pixels(raw).decode("utf-8", errors="replace"), names)
        if leaks:
            found[relative.as_posix()] = leaks
    return found
