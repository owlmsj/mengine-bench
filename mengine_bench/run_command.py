"""`mengine-bench run`: run every task, grade it, and collect the judge's evidence for the bundle.

Runs never judge (#23): each task leaves a judge packet and its declared
deliverables, and the maintainer judges the bundle with `mengine-bench judge`.
One task failing never aborts the run: it is recorded as a crash.
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from mengine_bench.bundle import bench_commit
from mengine_bench.core import EvalTask
from mengine_bench.judge import JudgeContext, workspace_diff
from mengine_bench.environment import collect_environment
from mengine_bench.report import RunMeta, TaskDetail, build_results, stats_summary, usage_record
from mengine_bench.runner.agents import Agent, split_jsonl
from mengine_bench.runner.stats import stats_record
from mengine_bench.runner.task_run import TaskRunRecord, run_task, snapshot
from mengine_bench.scoring import Price, TaskOutcome, score_run

TRANSCRIPT_TAIL_CHARS = 4_000
# The judge grades self-verification from these; the stream tail rarely shows them (#23 review).
COMMANDS_SHOWN = 40


@dataclass(frozen=True)
class RunSettings:
    """What the submitter declared for the run; recorded, never applied to the harness except model/effort."""

    model: str
    effort: str | None
    submitter: str | None = None
    price: Price | None = None
    config: dict[str, object] = field(default_factory=dict)


@dataclass
class JudgeEvidence:
    """What `write_bundle` stores for the maintainer's judge, per task id."""

    packets: dict[str, dict[str, object]] = field(default_factory=dict)
    # Workspace-relative deliverable path -> its file in the run's workspace.
    deliverables: dict[str, dict[str, Path]] = field(default_factory=dict)


def run_tasks(tasks: Sequence[EvalTask], agent: Agent, settings: RunSettings, work: Path,
              evidence: JudgeEvidence) -> dict[str, object]:
    """Run and grade every task; `evidence` collects the judge packets and deliverables."""
    started_at = _utc_now()
    outcomes: list[TaskOutcome] = []
    details: dict[str, TaskDetail] = {}
    for task in tasks:
        print(f"[{task.id}] running", flush=True)
        record: TaskRunRecord | None = None
        try:
            record = run_task(task, agent, work / task.id)
            detail = _detail(task, record)
            evidence.packets[task.id] = _judge_packet(task, record, work / task.id)
            evidence.deliverables[task.id] = _deliverables(task, record)
        except Exception as error:  # noqa: BLE001 - one task must not abort the run
            record, detail = _crashed_task(task, record, error)
            evidence.packets[task.id] = _crash_packet(task, record)
        details[task.id] = detail
        outcomes.append(_outcome(task, record))
        correct = 0.0 if record.status == "crash" else _correctness(record)
        print(f"[{task.id}] {record.status} c={correct:.2f} t={record.agent_s:.1f}s", flush=True)
    run = score_run(outcomes, settings.price)
    meta = RunMeta(date=datetime.now().strftime("%Y-%m-%d"), agent=agent.name, model=settings.model,
                   effort=settings.effort, agent_version=agent.version(), run_id=uuid.uuid4().hex[:8],
                   started_at=started_at, finished_at=_utc_now(), submitter=settings.submitter,
                   price=settings.price, config=settings.config)
    return build_results(meta, run, details, collect_environment(), bench_commit())


def agent_commands(stdout: str) -> list[str]:
    """Shell commands in any harness's JSON stream: every "command" string (Claude Bash input, Codex
    command_execution, opencode bash state), consecutive repeats (started/completed) dropped."""
    found: list[str] = []
    pending: list[object] = list(split_jsonl(stdout))
    while pending:
        value = pending.pop(0)
        if isinstance(value, list):
            pending[:0] = value
            continue
        if not isinstance(value, dict):
            continue
        command = value.get("command")
        if isinstance(command, str) and command and (not found or found[-1] != command):
            found.append(command)
        pending[:0] = [item for key, item in value.items() if key != "command"]
    return found


def _judge_context(task: EvalTask, record: TaskRunRecord, root: Path) -> JudgeContext:
    after = snapshot(record.workspace) if record.workspace is not None else {}
    transcripts = sorted((root / "transcripts").glob("*.stdout.txt"))
    tail = transcripts[-1].read_text(encoding="utf-8")[-TRANSCRIPT_TAIL_CHARS:] if transcripts else ""
    commands = [command for path in transcripts for command in agent_commands(path.read_text(encoding="utf-8"))]
    if commands:
        listed = "\n".join(f"$ {command[:300]}" for command in commands[-COMMANDS_SHOWN:])
        tail = f"Shell commands the agent ran (last {COMMANDS_SHOWN}):\n{listed}\n\nStream tail:\n{tail}"
    checks = () if record.check is None else (*record.check.mandatory, *record.check.checks)
    return JudgeContext(task_id=task.id, prompts=tuple(step.prompt for step in task.steps),
                        answers=tuple(record.answers), diff=workspace_diff(record.initial_files, after),
                        transcript_tail=tail, checks=tuple(checks), status=record.status,
                        stats=stats_summary(stats_record(record.stats)))


def _judge_packet(task: EvalTask, record: TaskRunRecord, root: Path) -> dict[str, object]:
    """The evidence `mengine-bench judge` needs later (judge/<task>.json)."""
    packet = _judge_context(task, record, root).record()
    packet.update(deliverables=list(task.deliverables), render=task.render_target)
    return packet


def _crash_packet(task: EvalTask, record: TaskRunRecord) -> dict[str, object]:
    """A crashed task still gets a vote, from the prompts and whatever answers exist."""
    checks = () if record.check is None else (*record.check.mandatory, *record.check.checks)
    context = JudgeContext(task_id=task.id, prompts=tuple(step.prompt for step in task.steps),
                           answers=tuple(record.answers), diff="", transcript_tail=record.error or "",
                           checks=tuple(checks))
    packet = context.record()
    packet.update(deliverables=[], render=None)
    return packet


def _deliverables(task: EvalTask, record: TaskRunRecord) -> dict[str, Path]:
    if record.workspace is None:
        return {}
    return {rel: record.workspace / rel for rel in task.deliverables if (record.workspace / rel).is_file()}


def _crashed_task(task: EvalTask, record: TaskRunRecord | None, error: Exception) -> tuple[TaskRunRecord, TaskDetail]:
    """Record a task whose run or post-processing raised as `crash`, keeping what was graded.

    Scoring gives a crash c = 0.
    """
    message = f"post-processing failed: {type(error).__name__}: {error}"
    if record is None:
        record = TaskRunRecord(task_id=task.id)
    record.status = "crash"
    record.error = f"{record.error} {message}" if record.error else message
    try:
        return record, _detail(task, record)
    except Exception:  # noqa: BLE001 - fall back to an ungraded crash with no evidence
        record.check, record.workspace = None, None
        return record, _detail(task, record)


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _detail(task: EvalTask, record: TaskRunRecord) -> TaskDetail:
    check = record.check
    checks: list[dict[str, object]] = []
    if check is not None:
        checks = [{"name": name, "ok": ok, "mandatory": True} for name, ok in check.mandatory]
        checks += [{"name": name, "ok": ok, "mandatory": False} for name, ok in check.checks]
    return TaskDetail(
        steps=[{"index": s.index, "wall_s": round(s.wall_s, 2), "exit_code": s.exit_code, "status": s.status,
                "usage": usage_record(s.usage)} for s in record.steps],
        grading_s=record.grading_s, checks=checks,
        flags=[] if record.status == "ok" else [record.status], error=_public_error(record.error, record),
        answers=list(record.answers), usage=usage_record(record.usage), stats=record.stats,
    )


def _public_error(error: str | None, record: TaskRunRecord) -> str | None:
    # Error texts may embed workspace paths; results are published, so cut them.
    if error is None or record.workspace is None:
        return error
    root = str(record.workspace.parent.resolve())
    return error.replace(root, "<workspace>").replace(str(record.workspace.parent), "<workspace>")


def _correctness(record: TaskRunRecord) -> float:
    if record.check is None:
        return 0.0
    return record.check.partial_score if record.status == "timeout" else record.check.score


def _outcome(task: EvalTask, record: TaskRunRecord) -> TaskOutcome:
    check = record.check
    return TaskOutcome(
        task_id=task.id, status=record.status,
        correctness=_correctness(record),
        solved=check.passed if check is not None else False,
        # Score the exact time result.json records, so the totals follow
        # from the published task times.
        agent_s=round(record.agent_s, 2) if record.steps else None,
        step_usages=tuple(step.usage for step in record.steps),
    )
