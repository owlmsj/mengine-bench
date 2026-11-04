"""Re-run current graders on archived final workspaces, never the agent (#185)."""

from __future__ import annotations

import gzip
import json
import tarfile
import tempfile
from pathlib import Path

from mengine_bench import __version__, catalog
from mengine_bench.bundle import REPO_ROOT, RESULT_NAME, SUMMARY_NAME, public_json, public_text
from mengine_bench.redact import PathScope, local_names
from mengine_bench.report import render_summary
from mengine_bench.run_command import _correctness, _detail
from mengine_bench.runner.leftovers import LeftProcess
from mengine_bench.runner.task_run import StepRecord, TaskRunRecord, _grade, add_cleanup_check
from mengine_bench.scoring import TaskOutcome, score_run


def _extract(archive_path: Path, workspace: Path) -> None:
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        for member in members:
            destination = workspace / member.name
            if not member.isfile() or not destination.resolve().is_relative_to(workspace.resolve()):
                raise ValueError(f"received archive member {member.name!r}; expected a regular file inside workspace")
        archive.extractall(workspace, members=members, filter="data")


def _streams(bundle: Path, row: dict[str, object]) -> list[str]:
    relative = row.get("transcript")
    if not relative:
        return []
    path = bundle / str(relative)
    if not path.resolve().is_relative_to(bundle.resolve()):
        raise ValueError(f"received transcript {relative!r}; expected a path inside bundle")
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        entries = [json.loads(line) for line in stream if line.strip()]
    return [entry["text"] for entry in sorted(entries, key=lambda entry: int(entry["step"]))
            if entry["stream"] == "stdout"]


def _regrade_task(bundle: Path, row: dict[str, object], version: str) -> None:
    task_id = str(row["id"])
    archive = bundle / "workspace" / f"{task_id}.tar.gz"
    if not archive.resolve().is_relative_to((bundle / "workspace").resolve()):
        raise ValueError(f"received task id {task_id!r}; expected a workspace archive inside bundle")
    if not archive.is_file():
        row.setdefault("flags", []).append("regrade skipped: workspace not kept")
        return
    task = catalog.task_by_id(task_id)
    if task is None:
        row.setdefault("flags", []).append("regrade skipped: task absent from current catalog")
        return
    scratch = REPO_ROOT / "tmp"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="mengine-bench-regrade-", dir=scratch) as temporary:
        workspace = Path(temporary) / "workspace"
        workspace.mkdir()
        _extract(archive, workspace)
        record = TaskRunRecord(task_id=task_id, status=str(row["status"]), workspace=workspace,
                               steps=[StepRecord(index=step["index"], wall_s=step["wall_s"],
                                                 exit_code=step["exit_code"], status=step["status"])
                                      for step in row.get("steps", [])],
                               answers=list(row["answers"]), streams=_streams(bundle, row),
                               outside_writes=list(row.get("outside_writes", [])),
                               outside_unmeasured=row.get("outside_unmeasured"),
                               left_open_tabs=row.get("left_open_tabs"),
                               left_running=[LeftProcess(**left) for left in row.get("left_running", [])])
        _grade(task, record)
        if record.error:
            raise ValueError(f"received failed grading for {task_id!r}: {record.error}; expected completed checks")
        record.status = str(row["status"])
        add_cleanup_check(task, record)
        detail = _detail(task, record)
        scope = PathScope(workspaces=(workspace,), names=local_names())
        checks = public_json(detail["checks"], scope)
        row.setdefault("graded_with", []).append({"bench_version": row.get("grading_version", version),
                                                  "correct": row["c"], "checks": row["checks"]})
        row.update(c=_correctness(record), checks=checks, grading_version=__version__,
                   solved=record.status == "ok" and record.check is not None and record.check.passed)
        packet_path = bundle / "judge" / f"{task_id}.json"
        if packet_path.is_file():
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            packet.setdefault("checks_graded_with", []).append({"checks": packet["checks"],
                                                                "status": packet.get("status", "ok")})
            packet.update(checks=[[check["name"], check["ok"]] for check in checks], status=row["status"])
            packet_path.write_text(json.dumps(packet, indent=1, ensure_ascii=False) + "\n",
                                   encoding="utf-8", newline="\n")


def regrade_bundle(bundle: Path) -> dict[str, object]:
    """Keep run metadata and judge votes; replace correctness, check rows and derived totals."""
    result = json.loads((bundle / RESULT_NAME).read_text(encoding="utf-8"))
    for row in result["tasks"]:
        _regrade_task(bundle, row, result["bench_version"])
    outcomes = [TaskOutcome(task_id=row["id"], status=row["status"], correctness=row["c"],
                            solved=row["solved"], agent_s=row["agent_s"],
                            judge=row.get("judge") if result.get("judge") else None)
                for row in result["tasks"]]
    scored = score_run(outcomes)
    result["totals"].update(correct=scored.correct, solved=scored.solved, total=scored.total,
                            speed=scored.speed, score=scored.score)
    scope = PathScope(names=local_names().allowing(result.get("submitter")))
    (bundle / RESULT_NAME).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                                      encoding="utf-8", newline="\n")
    (bundle / SUMMARY_NAME).write_text(public_text(render_summary(result), scope), encoding="utf-8", newline="\n")
    return result
