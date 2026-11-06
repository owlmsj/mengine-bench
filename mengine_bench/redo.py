"""`mengine-bench redo <bundle>`: rerun some tasks of a bundle with the bundle's own agent (#205).

A task that crashed for the runner's sake (a pid that vanished, #205) is run again instead of the
whole run. Each task takes the `run` path (run_one_task: the #144 silent retry, judge packet,
deliverables, evidence, workspace), its bundle files and row are replaced, and the run totals are
scored again. run_id, date, agent and config stay; `redo` in result.json records what was redone,
why, and what the first attempt was. Votes of the redone tasks are cleared, so the run waits for
the judge again, and every workspace archive is repacked without the dirs `run` now leaves out.
"""

from __future__ import annotations

import json
import shutil
import tempfile
from dataclasses import dataclass, fields
from pathlib import Path

from mengine_bench import __version__, catalog
from mengine_bench.bundle import (
    JUDGE_DIR, REPO_ROOT, RESULT_NAME, SUMMARY_NAME, bench_commit, public_json, public_text, repack_workspace,
    run_scope, write_bundle,
)
from mengine_bench.core import EvalTask
from mengine_bench.leaderboard import major_minor
from mengine_bench.redact import LocalNames, PathScope, local_names
from mengine_bench.report import RunMeta, TaskDetail, build_results, render_summary, totals_block
from mengine_bench.run_command import JudgeEvidence, _utc_now, run_one_task
from mengine_bench.runner.agents import Agent, Usage
from mengine_bench.runner.stats import RunStats, merge_stats, stats_record
from mengine_bench.scoring import Price, TaskOutcome, score_run

REDO_FLAG = "redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json"
# Medians, not counts: result.json keeps no per-task rates, so they cannot be merged again.
STATS_LISTS = frozenset({"turn_rates", "tool_call_s"})


@dataclass(frozen=True)
class RedoPlan:
    """What `redo` reruns: the bundle's result as read, its tasks to rerun, and why."""

    bundle: Path
    result: dict[str, object]
    tasks: list[EvalTask]
    reason: str
    price: Price | None


def plan_redo(bundle: Path, ids: str) -> RedoPlan:
    """Read the bundle and pick its tasks: `ids` (comma-separated) or, when empty, every crashed one."""
    result = json.loads((bundle / RESULT_NAME).read_text(encoding="utf-8"))
    version = str(result.get("bench_version"))
    # A patch changes no task, prompt or limit (CONTRIBUTING), so the bundle's catalog is still the installed one.
    if major_minor(version) != major_minor(__version__):
        raise ValueError(f"received bundle of bench {version}; expected bench {major_minor(__version__)} "
                         f"(installed {__version__})")
    present = [str(row["id"]) for row in result["tasks"]]
    wanted = [item.strip() for item in ids.split(",") if item.strip()]
    unknown = [item for item in wanted if item not in present]
    if unknown:
        raise ValueError(f"received --tasks {unknown}; expected ids from the bundle: {', '.join(present)}")
    reason = "named with --tasks" if wanted else "status crash"
    if not wanted:
        wanted = [str(row["id"]) for row in result["tasks"] if row.get("status") == "crash"]
    if not wanted:
        raise ValueError(f"received no task with status crash in {bundle.name}; expected one, or --tasks ids")
    found = {task_id: catalog.task_by_id(task_id) for task_id in present if task_id in wanted}
    missing = [task_id for task_id, task in found.items() if task is None]
    if missing:
        raise ValueError(f"received task ids {missing} absent from the installed catalog; expected catalog ids")
    price = result.get("price_per_mtok")
    return RedoPlan(bundle=bundle, result=result, tasks=[task for task in found.values() if task is not None],
                    reason=reason,
                    price=None if not isinstance(price, dict) else Price(float(price["input"]),
                                                                         float(price["cached"]),
                                                                         float(price["output"])))


def redo_bundle(plan: RedoPlan, agent: Agent, work: Path) -> LocalNames:
    """Rerun the plan's tasks under `work` and rewrite the bundle; return the names the privacy check uses."""
    result = plan.result
    started_at = _utc_now()
    evidence = JudgeEvidence()
    outcomes: list[TaskOutcome] = []
    details: dict[str, TaskDetail] = {}
    for task in plan.tasks:
        outcome, details[task.id] = run_one_task(task, agent, work, evidence)
        outcomes.append(outcome)
    scope = run_scope(work, local_names().allowing(result.get("submitter")))
    new_rows = _write_task_files(plan, agent, outcomes, details, evidence, work, scope)
    previous: dict[str, object] = {}
    for index, row in enumerate(result["tasks"]):
        new_row = new_rows.get(str(row["id"]))
        if new_row is None:
            continue
        previous[row["id"]] = {"status": row.get("status"), "error": row.get("error"), "c": row.get("c"),
                               "flags": row.get("flags", [])}
        new_row["flags"].append(REDO_FLAG)
        result["tasks"][index] = new_row
    _repack_workspaces(plan.bundle, result["tasks"])
    entry: dict[str, object] = {"tasks": list(new_rows), "reason": plan.reason, "previous": previous,
                                "bench_version": __version__, "bench_commit": bench_commit(),
                                "agent_version": agent.version(), "started_at": started_at,
                                "finished_at": _utc_now()}
    if result.get("judge") is not None:
        # A vote must exist for every task or none (scoring.judge_mean): the run waits for `judge` again.
        entry["judge_cleared"], result["judge"] = result["judge"], None
    result.setdefault("redo", []).append(entry)
    _rescore(result, plan.price)
    public = public_json(result, scope)
    assert isinstance(public, dict)
    (plan.bundle / RESULT_NAME).write_text(json.dumps(public, indent=2, ensure_ascii=False) + "\n",
                                           encoding="utf-8", newline="\n")
    (plan.bundle / SUMMARY_NAME).write_text(public_text(render_summary(public), scope), encoding="utf-8",
                                            newline="\n")
    return scope.names


def _write_task_files(plan: RedoPlan, agent: Agent, outcomes: list[TaskOutcome], details: dict[str, TaskDetail],
                      evidence: JudgeEvidence, work: Path, scope: PathScope) -> dict[str, dict[str, object]]:
    """write_bundle into a staging dir, then move each redone task's files over the old ones; return the new rows."""
    result = plan.result
    row_agent = result["agent"]
    meta = RunMeta(date=str(result["date"]), agent=str(row_agent["name"]), model=str(row_agent["model"]),
                   effort=row_agent.get("effort"), agent_version=agent.version(), run_id=str(result["run_id"]),
                   started_at=str(result.get("started_at")), finished_at=str(result.get("finished_at")),
                   submitter=result.get("submitter"), price=plan.price, config=result.get("config", {}))
    partial = build_results(meta, score_run(outcomes, plan.price), details, {}, {})
    transcripts = {task.id: work / task.id / "transcripts" for task in plan.tasks}
    scratch = REPO_ROOT / "tmp"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="mengine-bench-redo-", dir=scratch) as temporary:
        staged = write_bundle(partial, Path(temporary), transcripts, scope, evidence.packets, evidence.deliverables,
                              evidence.evidence, evidence.workspaces)
        for task in plan.tasks:
            _drop_task_files(plan.bundle, task.id)
            for relative in _task_paths(task.id):
                if (staged / relative).exists():
                    (plan.bundle / relative).parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(staged / relative), str(plan.bundle / relative))
        rows = json.loads((staged / RESULT_NAME).read_text(encoding="utf-8"))["tasks"]
    return {str(row["id"]): row for row in rows}


def _task_paths(task_id: str) -> tuple[str, ...]:
    return (f"transcripts/{task_id}.jsonl.gz", f"{JUDGE_DIR}/{task_id}.json", f"{JUDGE_DIR}/{task_id}",
            f"evidence/{task_id}", f"workspace/{task_id}.tar.gz")


def _drop_task_files(bundle: Path, task_id: str) -> None:
    """The first attempt's files, and the frames of its vote (bundle_judge.judge_frames names them)."""
    judge_dir = bundle / JUDGE_DIR
    frames = [path for path in judge_dir.glob(f"{task_id}*.png")
              if path.name in (f"{task_id}.png", f"{task_id}-1s.png", f"{task_id}-4s.png")
              or path.name.startswith(f"{task_id}-state-")] if judge_dir.is_dir() else []
    for path in [*(bundle / relative for relative in _task_paths(task_id)), *frames]:
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        elif path.exists() or path.is_symlink():
            path.unlink()


def _repack_workspaces(bundle: Path, rows: list[dict[str, object]]) -> None:
    for row in rows:
        archive = bundle / "workspace" / f"{row['id']}.tar.gz"
        if not archive.is_file():
            continue
        dropped = repack_workspace(archive)
        if dropped:
            row.setdefault("flags", []).append(f"workspace archive repacked without {', '.join(dropped)} (#205)")


def _usage(record: object) -> Usage | None:
    if not isinstance(record, dict):
        return None
    return Usage(**{field.name: record.get(field.name) for field in fields(Usage)})


def _rescore(result: dict[str, object], price: Price | None) -> None:
    """Totals from every row, as `run` scores them; the judge total waits for a full set of votes."""
    rows = result["tasks"]
    judged = result.get("judge") is not None
    outcomes = [TaskOutcome(task_id=str(row["id"]), status=str(row["status"]), correctness=float(row["c"]),
                            solved=bool(row["solved"]), agent_s=row.get("agent_s"),
                            step_usages=tuple(_usage(step.get("usage")) for step in row.get("steps", [])),
                            judge=row.get("judge") if judged else None)
                for row in rows]
    run = score_run(outcomes, price)
    totals = result["totals"]
    names = {field.name for field in fields(RunStats)} - STATS_LISTS
    merged = stats_record(merge_stats(RunStats(**{name: value for name, value in row.get("stats", {}).items()
                                                  if name in names}) for row in rows))
    old_stats = totals.get("stats") if isinstance(totals.get("stats"), dict) else {}
    # result.json keeps per-task medians only, so the run's medians stay as the first run measured them (#205).
    merged.update(turn_tps_median=old_stats.get("turn_tps_median"), tool_s_median=old_stats.get("tool_s_median"))
    totals.update(totals_block(run), timeouts=sum(row["status"] == "timeout" for row in rows), stats=merged)
