"""Console entry point: run, list, leaderboard, selftest, tasks-doc."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import uuid
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path

from mengine_bench import __version__, catalog, visual
from mengine_bench.core import FULL, SUITES, EvalTask, scratch_root
from mengine_bench.judge import DEFAULT_VOTES, JudgeContext, SubjectiveJudge, VisionChecklistJudge, workspace_diff
from mengine_bench.bundle import bench_commit, run_scope, write_bundle
from mengine_bench.leaderboard import build_leaderboard
from mengine_bench.report import (
    SUMMARIES_BEGIN, SUMMARIES_END, RunMeta, TaskDetail, build_results, collect_environment, render_task_summaries,
    render_tasks_table, replace_tasks_table,
)
from mengine_bench.runner.agents import AGENT_NAMES, Agent, make_agent
from mengine_bench.runner.task_run import TaskRunRecord, run_task, snapshot
from mengine_bench.scoring import TaskOutcome, score_suite

JUDGE_CHOICES = ("none", *AGENT_NAMES)
# docs/SCORING.md recommends this judge; reports always state the one used.
DEFAULT_JUDGE_MODEL = "claude-opus-5-5"
DEFAULT_JUDGE_EFFORT = "xhigh"
TRANSCRIPT_TAIL_CHARS = 4_000


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mengine-bench")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="run a suite against an agent and write results")
    run.add_argument("--suite", choices=SUITES, required=True)
    run.add_argument("--agent", choices=AGENT_NAMES, required=True)
    run.add_argument("--model", required=True)
    run.add_argument("--effort")
    run.add_argument("--cmd", help='argv template for --agent cmd: JSON list or quoted string with {prompt_file}')
    run.add_argument("--tasks", default="", help="comma-separated task ids (default: whole suite)")
    run.add_argument("--judge", choices=JUDGE_CHOICES, default="none")
    run.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL)
    run.add_argument("--judge-effort", default=DEFAULT_JUDGE_EFFORT)
    run.add_argument("--judge-votes", type=int, default=DEFAULT_VOTES)
    run.add_argument("--judge-cmd", help="argv template for --judge cmd")
    run.add_argument("--out", type=Path, default=Path("results"), help="bundles go to <out>/<suite>/<run>/")
    run.add_argument("--submitter", help="free-text credit stored in result.json (optional, public)")
    run.add_argument("--work", type=Path, help="workspace root (default: outside the repo, in the temp dir)")
    run.add_argument("--dry-run", action="store_true")
    listing = sub.add_parser("list", help="list the tasks of a suite")
    listing.add_argument("--suite", choices=SUITES, default=FULL)
    board = sub.add_parser("leaderboard", help="rank results/**/result.json into LEADERBOARD.md")
    board.add_argument("--results", type=Path, default=Path("results"))
    board.add_argument("--output", type=Path, default=Path("LEADERBOARD.md"))
    selftest = sub.add_parser("selftest", help="run every task's gold self-test without an agent")
    selftest.add_argument("--tasks", default="")
    doc = sub.add_parser("tasks-doc", help="print (or --write) the docs/TASKS.md table; --readme rewrites the "
                                           "README task summaries")
    doc.add_argument("--write", type=Path, nargs="?", const=Path("docs/TASKS.md"))
    doc.add_argument("--readme", type=Path, nargs="?", const=Path("README.md"))
    return parser


def _select(pool: Sequence[EvalTask], ids: str) -> list[EvalTask]:
    if not ids:
        return list(pool)
    wanted = [item.strip() for item in ids.split(",") if item.strip()]
    known = {task.id for task in pool}
    unknown = [item for item in wanted if item not in known]
    if unknown:
        raise SystemExit(f"error: received --tasks {unknown}; expected ids from: {', '.join(sorted(known))}")
    return [task for task in pool if task.id in wanted]


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "list":
        for task in catalog.tasks(args.suite):
            print(f"{task.id}\t{task.category}\tw={task.weight}\tpar={task.par_s:g}s")
        return 0
    if args.command == "leaderboard":
        return _leaderboard(args)
    if args.command == "selftest":
        return _selftest(_select(catalog.all_tasks(), args.tasks))
    if args.command == "tasks-doc":
        return _tasks_doc(args.write, args.readme)
    return _run(args)


def _run(args: argparse.Namespace) -> int:
    tasks = _select(catalog.tasks(args.suite), args.tasks)
    if args.agent == "cmd" and not args.cmd:
        raise SystemExit("error: received --agent cmd without --cmd; expected an argv template with {prompt_file}")
    if args.judge == "cmd" and not args.judge_cmd:
        raise SystemExit("error: received --judge cmd without --judge-cmd; expected an argv template")
    if args.dry_run:
        plan = {"suite": args.suite, "agent": args.agent, "model": args.model, "effort": args.effort,
                "judge": args.judge, "tasks": [task.id for task in tasks], "dry_run": True, "launches": 0}
        print(json.dumps(plan))
        return 0
    agent = make_agent(args.agent, args.model, args.effort, args.cmd)
    judge_agent = None
    if args.judge != "none":
        judge_agent = make_agent(args.judge, args.judge_model, args.judge_effort, args.judge_cmd)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    # Outside the repo by default: an agent working under the bench checkout
    # could read the gold checks in mengine_bench/tasks.
    work = (args.work or scratch_root() / "runs" / stamp).resolve()
    previous_judge = visual.JUDGE
    if judge_agent is not None:
        visual.JUDGE = VisionChecklistJudge(judge_agent, votes=args.judge_votes)
    try:
        results = _run_tasks(tasks, agent, judge_agent, args, work)
    finally:
        visual.JUDGE = previous_judge
    transcripts = {task.id: work / task.id / "transcripts" for task in tasks}
    bundle = write_bundle(results, args.out, transcripts, run_scope(work))
    totals = results["totals"]
    print(f"objective {totals['objective']} solved {totals['solved']}/{totals['total']}")  # type: ignore[index]
    print(f"wrote bundle {bundle}; raw workspaces in {work}")
    return 0


def _leaderboard(args: argparse.Namespace) -> int:
    board = build_leaderboard(args.results, args.output.parent)
    args.output.write_text(board.markdown, encoding="utf-8", newline="\n")
    for name in board.partial:
        print(f"partial (not ranked): {name}")
    print(f"wrote {args.output}: {board.ranked} ranked run(s), {len(board.partial)} partial")
    return 0


def _run_tasks(tasks: Sequence[EvalTask], agent: Agent, judge_agent: Agent | None, args: argparse.Namespace,
               work: Path) -> dict[str, object]:
    started_at = _utc_now()
    subjective = SubjectiveJudge(judge_agent, votes=args.judge_votes) if judge_agent is not None else None
    outcomes: list[TaskOutcome] = []
    details: dict[str, TaskDetail] = {}
    votes: dict[str, tuple[int, ...]] = {}
    vision = visual.JUDGE if isinstance(visual.JUDGE, VisionChecklistJudge) else None
    for task in tasks:
        print(f"[{task.id}] running", flush=True)
        if vision is not None:
            vision.history.clear()
        record: TaskRunRecord | None = None
        try:
            record = run_task(task, agent, work / task.id)
            detail = _post_process(task, record, vision, subjective, work / task.id, votes)
        except Exception as error:  # noqa: BLE001 - one task must not abort the suite
            record, detail = _crashed_task(task, record, error)
            votes.pop(task.id, None)
        details[task.id] = detail
        outcomes.append(_outcome(task, record, votes.get(task.id, ())))
        print(f"[{task.id}] {record.status} c={detail['check_score']:.2f} t={record.agent_s:.1f}s", flush=True)
    label = subjective.label if subjective is not None else None
    suite = score_suite(args.suite, outcomes, judge=label if any(votes.values()) else None)
    meta = RunMeta(date=datetime.now().strftime("%Y-%m-%d"), suite=args.suite, agent=agent.name, model=args.model,
                   effort=args.effort, agent_version=agent.version(), judge_label=label,
                   judge_votes=args.judge_votes if label else 0, run_id=uuid.uuid4().hex[:8],
                   started_at=started_at, finished_at=_utc_now(), submitter=args.submitter,
                   judge_model=args.judge_model if label else None, judge_effort=args.judge_effort if label else None)
    return build_results(meta, suite, details, votes, collect_environment(), bench_commit())


def _post_process(task: EvalTask, record: TaskRunRecord, vision: VisionChecklistJudge | None,
                  subjective: SubjectiveJudge | None, root: Path, votes: dict[str, tuple[int, ...]]) -> TaskDetail:
    detail = _detail(task, record)
    detail["vision"] = _vision_record(vision)
    if subjective is not None:
        verdict = subjective.grade(_judge_context(task, record, root), root / "judge")
        votes[task.id] = verdict.votes
        detail["judge_rationales"] = list(verdict.rationales)
        detail["judge_errors"] = list(verdict.errors)
    return detail


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


def _vision_record(vision: VisionChecklistJudge | None) -> dict[str, object] | None:
    # A call with no valid ballot falls back to "no judge" and grades nothing.
    if vision is None or not vision.history or not vision.history[-1]["ballots"]:
        return None
    return vision.history[-1]


def _detail(task: EvalTask, record: TaskRunRecord) -> TaskDetail:
    check = record.check
    checks: list[dict[str, object]] = []
    if check is not None:
        checks = [{"name": name, "ok": ok, "mandatory": True} for name, ok in check.mandatory]
        checks += [{"name": name, "ok": ok, "mandatory": False} for name, ok in check.checks]
    return TaskDetail(
        par_s=task.par_s,
        steps=[{"index": s.index, "wall_s": round(s.wall_s, 2), "exit_code": s.exit_code, "status": s.status}
               for s in record.steps],
        grading_s=record.grading_s, checks=checks,
        check_score=check.score if check is not None else 0.0,
        mandatory_ok=check.mandatory_ok if check is not None else False,
        passed=check.passed if check is not None else False,
        flags=_flags(record), error=_public_error(record.error, record),
        judge_rationales=[], judge_errors=[], answers=list(record.answers),
        pass_ratio=check.pass_ratio if check is not None else 1.0, vision=None,
    )


def _flags(record: TaskRunRecord) -> list[str]:
    flags = list(getattr(record.check, "flags", []))
    if record.status != "ok":
        flags.append(record.status)
    return flags


def _public_error(error: str | None, record: TaskRunRecord) -> str | None:
    # Error texts may embed workspace paths; results are published, so cut them.
    if error is None or record.workspace is None:
        return error
    root = str(record.workspace.parent.resolve())
    return error.replace(root, "<workspace>").replace(str(record.workspace.parent), "<workspace>")


def _outcome(task: EvalTask, record: TaskRunRecord, votes: tuple[int, ...]) -> TaskOutcome:
    check = record.check
    return TaskOutcome(
        task_id=task.id, category=task.category, weight=task.weight, par_s=task.par_s,
        check_score=check.score if check is not None else 0.0,
        mandatory_ok=check.mandatory_ok if check is not None else False,
        passed=check.passed if check is not None else False,
        # Score the exact time result.json records, so the totals follow
        # from the published task times.
        agent_s=round(record.agent_s, 2) if record.steps else None, status=record.status, judge_votes=votes,
    )


def _judge_context(task: EvalTask, record: TaskRunRecord, root: Path) -> JudgeContext:
    after = snapshot(record.workspace) if record.workspace is not None else {}
    transcripts = sorted((root / "transcripts").glob("*.stdout.txt"))
    tail = transcripts[-1].read_text(encoding="utf-8")[-TRANSCRIPT_TAIL_CHARS:] if transcripts else ""
    checks = () if record.check is None else (*record.check.mandatory, *record.check.checks)
    return JudgeContext(task_id=task.id, prompts=tuple(step.prompt for step in task.steps),
                        answers=tuple(record.answers), diff=workspace_diff(record.initial_files, after),
                        transcript_tail=tail, checks=tuple(checks))


def _selftest(tasks: Sequence[EvalTask]) -> int:
    failures = 0
    previous = visual.RENDER
    # Gold must not depend on a browser or judge: grade visual tasks on gates only.
    visual.RENDER = lambda html, png: visual.NO_BROWSER
    try:
        with tempfile.TemporaryDirectory(prefix="selftest-", dir=scratch_root()) as tmp:
            for task in tasks:
                problem = _gold_problem(task, Path(tmp) / task.id)
                failures += problem is not None
                print(f"FAIL {task.id}: {problem}" if problem else f"PASS {task.id}", flush=True)
    finally:
        visual.RENDER = previous
    print(f"{len(tasks) - failures}/{len(tasks)} gold self-tests passed")
    return 1 if failures else 0


def _gold_problem(task: EvalTask, root: Path) -> str | None:
    empty, solved = root / "empty", root / "solved"
    empty.mkdir(parents=True)
    task.setup(empty)
    if task.check(empty, [""] * len(task.steps)).passed:
        return "gold passes an untouched workspace"
    solved.mkdir()
    task.setup(solved)
    result = task.check(solved, task.reference(solved))
    return None if result.passed else f"reference fails {result.failed()}"


def _tasks_doc(target: Path | None, readme: Path | None) -> int:
    table = render_tasks_table(catalog.all_tasks())
    if target is None and readme is None:
        sys.stdout.write(table)
        return 0
    if target is not None:
        target.write_text(replace_tasks_table(target.read_text(encoding="utf-8"), table), encoding="utf-8",
                          newline="\n")
        print(f"updated {target}")
    if readme is not None:
        summaries = render_task_summaries(catalog.all_tasks())
        updated = replace_tasks_table(readme.read_text(encoding="utf-8"), summaries, SUMMARIES_BEGIN, SUMMARIES_END)
        readme.write_text(updated, encoding="utf-8", newline="\n")
        print(f"updated {readme}")
    return 0
