"""Console entry point: list, selftest, run, submit, judge, leaderboard, tasks-doc."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path

from mengine_bench import __version__, catalog
from mengine_bench.bundle import bundle_leaks, run_scope, write_bundle
from mengine_bench.bundle_judge import judge_bundle
from mengine_bench.core import EvalTask, scratch_root
from mengine_bench.leaderboard import build_leaderboard
from mengine_bench.preflight import contamination
from mengine_bench.redact import LocalNames, local_names
from mengine_bench.report import (
    SUMMARIES_BEGIN, SUMMARIES_END, cost_text, render_task_summaries, render_tasks_table, replace_tasks_table,
    time_text,
)
from mengine_bench.environment import parse_config
from mengine_bench.run_command import JudgeEvidence, RunSettings, run_tasks
from mengine_bench.runner.agents import AGENT_NAMES, make_agent
from mengine_bench.scoring import parse_price
from mengine_bench.submit import SubmitError, gh_login, submit

# The one judge for every ranked run (docs/SCORING.md); the flags exist for tests.
DEFAULT_JUDGE_MODEL = "claude-opus-5-5"
DEFAULT_JUDGE_EFFORT = "xhigh"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mengine-bench")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="run every task against an agent and write a bundle (--submit opens the PR)")
    run.add_argument("--agent", choices=AGENT_NAMES, required=True)
    run.add_argument("--model", required=True)
    run.add_argument("--effort")
    run.add_argument("--cmd", help="argv template for --agent cmd: JSON list or quoted string with {prompt_file}")
    run.add_argument("--tasks", default="",
                     help="comma-separated task ids, for debugging; such a run is never ranked (default: every task)")
    run.add_argument("--price", help="USD per million tokens when the harness reports no USD: "
                                     "input=X,cached=Y,output=Z, or 0 for free/local inference")
    run.add_argument("--config", action="append", default=[], metavar="KEY=VALUE",
                     help="declared setup, repeatable, recorded in result.json and never applied "
                          "(e.g. provider=local, quant=Q4_K_M, ctx=256k, mcp=none)")
    run.add_argument("--out", type=Path, default=Path("results"), help="bundles go to <out>/<run>/")
    run.add_argument("--submitter", help="public credit in result.json (default with --submit: your GitHub login)")
    run.add_argument("--submit", action="store_true",
                     help="after a clean run, open the pull request with the bundle (needs gh, logged in)")
    run.add_argument("--work", type=Path, help="workspace root, kept after the run (default: a temp dir, removed "
                                               "once the bundle is written)")
    run.add_argument("--allow-unclean", action="store_true",
                     help="run despite preflight findings; they are recorded and the run is not ranked")
    run.add_argument("--dry-run", action="store_true", help="print the plan and the preflight findings; run nothing")
    sub.add_parser("list", help="list the tasks")
    board = sub.add_parser("leaderboard", help="rank results/*/result.json into LEADERBOARD.md")
    board.add_argument("--results", type=Path, default=Path("results"))
    board.add_argument("--output", type=Path, default=Path("LEADERBOARD.md"))
    send = sub.add_parser("submit", help="open the pull request for a clean bundle (needs gh, logged in)")
    send.add_argument("bundle", type=Path)
    judge = sub.add_parser("judge", help="judge a bundle (maintainer): one rubric vote per task, then rescore")
    judge.add_argument("bundle", type=Path)
    judge.add_argument("--judge", choices=AGENT_NAMES, default="claude")
    judge.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL)
    judge.add_argument("--judge-effort", default=DEFAULT_JUDGE_EFFORT)
    judge.add_argument("--judge-cmd", help="argv template for --judge cmd")
    selftest = sub.add_parser("selftest", help="run every task's gold self-test without an agent")
    selftest.add_argument("--tasks", default="")
    doc = sub.add_parser("tasks-doc", help="print (or --write) the docs/TASKS.md table; --readme rewrites the "
                                           "README task table")
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
        for task in catalog.all_tasks():
            print(f"{task.id}\t{task.category}\t{task.summary}")
        return 0
    if args.command == "leaderboard":
        return _leaderboard(args)
    if args.command == "selftest":
        return _selftest(_select(catalog.all_tasks(), args.tasks))
    if args.command == "tasks-doc":
        return _tasks_doc(args.write, args.readme)
    if args.command == "submit":
        return _submit(args.bundle)
    if args.command == "judge":
        return _judge(args)
    return _run(args)


def _judge(args: argparse.Namespace) -> int:
    if args.judge == "cmd" and not args.judge_cmd:
        raise SystemExit("error: received --judge cmd without --judge-cmd; expected an argv template")
    judge_agent = make_agent(args.judge, args.judge_model, args.judge_effort, args.judge_cmd)
    try:
        result = judge_bundle(args.bundle, judge_agent)
    except ValueError as error:
        print(f"judge: FAILED: {error}")
        return 1
    totals = result["totals"]
    assert isinstance(totals, dict)
    print(f"judged {args.bundle.name}: Score {totals['score']} = 0.7 x correct {totals['correct']} "
          f"+ 0.3 x judge {totals['judge']}")
    print("updated result.json and summary.md; commit them with LEADERBOARD.md")
    return 0


def _submit(bundle: Path) -> int:
    try:
        url = submit(bundle)
    except SubmitError as error:
        print(f"submit: FAILED: {error}")
        return 1
    print(f"submitted: {url}")
    return 0


def _run(args: argparse.Namespace) -> int:
    tasks = _select(catalog.all_tasks(), args.tasks)
    if args.agent == "cmd" and not args.cmd:
        raise SystemExit("error: received --agent cmd without --cmd; expected an argv template with {prompt_file}")
    try:
        price = None if args.price is None else parse_price(args.price)
        config: dict[str, object] = dict(parse_config(args.config))
    except ValueError as error:
        raise SystemExit(f"error: {error}") from error
    if args.submit and args.allow_unclean:
        raise SystemExit("error: received --submit with --allow-unclean; expected a clean run to publish")
    if args.submit and not args.dry_run:
        # Fail before the run, not 30 minutes later.
        try:
            login = gh_login()
        except SubmitError as error:
            raise SystemExit(f"error: --submit needs gh logged in: {error}") from error
        args.submitter = args.submitter or login
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    # Outside the repo by default: an agent working under the bench checkout
    # could read the gold checks in mengine_bench/tasks.
    scratch = scratch_root()
    work = (args.work or scratch / "runs" / stamp).resolve()
    problems = contamination(args.agent, work, scratch, env=os.environ)
    for problem in problems:
        print(f"preflight: {problem}")
    if args.dry_run:
        plan = {"agent": args.agent, "model": args.model, "effort": args.effort,
                "judge": "on review (maintainer: mengine-bench judge)", "tasks": [task.id for task in tasks],
                "dry_run": True, "launches": 0,
                "preflight": "clean" if not problems else f"{len(problems)} finding(s)"}
        print(json.dumps(plan))
        return 0
    if problems and not args.allow_unclean:
        raise SystemExit(f"error: received {len(problems)} preflight finding(s) above; expected a clean run "
                         f"(README, 'Run hygiene'), or --allow-unclean to record them and stay unranked")
    agent = make_agent(args.agent, args.model, args.effort, args.cmd)
    evidence = JudgeEvidence()
    settings = RunSettings(model=args.model, effort=args.effort, submitter=args.submitter, price=price,
                           config=config)
    results = run_tasks(tasks, agent, settings, work, evidence)
    results["preflight"] = problems
    transcripts = {task.id: work / task.id / "transcripts" for task in tasks}
    scope = run_scope(work, local_names().allowing(args.submitter))
    bundle = write_bundle(results, args.out, transcripts, scope, evidence.packets, evidence.deliverables)
    totals = results["totals"]
    assert isinstance(totals, dict)
    print(f"correct {totals['correct']}% solved {totals['solved']}/{totals['total']} time "
          f"{time_text(totals['time_s'])} cost {cost_text(totals)}; Score waits for the judge")
    print(f"wrote bundle {bundle}")
    if args.work is None:
        # Raw transcripts are unredacted, and a later run's agent could read these solutions.
        shutil.rmtree(work, ignore_errors=True)
        print(f"removed raw run dir {work}" if not work.exists() else f"could not fully remove {work}; delete it")
    else:
        print(f"raw workspaces kept in {work}")
    privacy = _privacy_check(bundle, scope.names)
    if privacy or not args.submit:
        return privacy
    return _submit(bundle)


def _privacy_check(bundle: Path, names: LocalNames) -> int:
    leaks = bundle_leaks(bundle, names)
    for name, kinds in leaks.items():
        print(f"privacy check: {name}: " + ", ".join(f"{kind} x{count}" for kind, count in sorted(kinds.items())))
    if leaks:
        print("privacy check: FAILED; do not publish this bundle")
        return 1
    print("privacy check: clean")
    return 0


def _leaderboard(args: argparse.Namespace) -> int:
    board = build_leaderboard(args.results, args.output.parent)
    args.output.write_text(board.markdown, encoding="utf-8", newline="\n")
    for name, reason in board.unranked:
        print(f"not ranked: {name}: {reason}")
    print(f"wrote {args.output}: {board.ranked} ranked run(s), {len(board.unranked)} not ranked")
    return 0


def _selftest(tasks: Sequence[EvalTask]) -> int:
    failures = 0
    with tempfile.TemporaryDirectory(prefix="selftest-", dir=scratch_root()) as tmp:
        for task in tasks:
            problem = _gold_problem(task, Path(tmp) / task.id)
            failures += problem is not None
            print(f"FAIL {task.id}: {problem}" if problem else f"PASS {task.id}", flush=True)
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
