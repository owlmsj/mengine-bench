"""`mengine-bench judge`: judge a bundle whose run had no judge, then rescore it.

A run without a judge stores the judge's evidence in the bundle:
judge/<task>.json (prompts, answers, workspace diff, transcript tail, checks,
all redacted). The maintainer runs this while reviewing the result pull
request, so competitors need no judge of their own and every run on the
leaderboard is judged the same way. The judge sets SUBJECTIVE and COMPOSITE;
it never changes the checks.
"""

from __future__ import annotations

import json
import tempfile
from collections.abc import MutableMapping
from pathlib import Path

from mengine_bench.bundle import JUDGE_DIR, RESULT_NAME, SUMMARY_NAME, public_text
from mengine_bench.judge import JudgeContext, SubjectiveJudge
from mengine_bench.redact import PathScope, local_names
from mengine_bench.report import render_summary, totals_block
from mengine_bench.runner.agents import Agent
from mengine_bench.scoring import TaskOutcome, score_suite

Task = MutableMapping[str, object]


def _outcome(task: Task) -> TaskOutcome:
    votes = task["judge_votes"]
    assert isinstance(votes, list)
    return TaskOutcome(task_id=str(task["id"]), category=str(task["category"]),
                       check_score=float(task["check_score"]),  # type: ignore[arg-type]
                       mandatory_ok=bool(task["mandatory_ok"]), passed=bool(task["passed"]),
                       agent_s=None if task["agent_s"] is None else float(task["agent_s"]),  # type: ignore[arg-type]
                       status=str(task["status"]), judge_votes=tuple(int(vote) for vote in votes))


def judge_bundle(bundle: Path, judge_agent: Agent, votes: int) -> dict[str, object]:
    """Judge every task with a packet, rescore, and rewrite result.json and summary.md."""
    result = json.loads((bundle / RESULT_NAME).read_text(encoding="utf-8"))
    judge = result.get("judge")
    if isinstance(judge, dict):
        raise ValueError(f"received {bundle.name} already judged by {judge.get('label')}; expected a run "
                         f"made without a judge")
    if not result.get("judge_pending"):
        raise ValueError(f"received {bundle.name} without judge packets ({JUDGE_DIR}/); expected a run made "
                         f"without a judge by bench 0.2.0 or later")
    subjective = SubjectiveJudge(judge_agent, votes=votes)
    tasks = result["tasks"]
    with tempfile.TemporaryDirectory(prefix="mengine-bench-judge-") as tmp:
        for task in tasks:
            packet_file = bundle / JUDGE_DIR / f"{task['id']}.json"
            if not packet_file.is_file():
                continue
            print(f"[{task['id']}] judging", flush=True)
            packet = json.loads(packet_file.read_text(encoding="utf-8"))
            verdict = subjective.grade(JudgeContext.from_record(packet), Path(tmp) / str(task["id"]))
            task["judge_votes"] = list(verdict.votes)
            task["judge_rationales"], task["judge_errors"] = list(verdict.rationales), list(verdict.errors)
    if not any(task["judge_votes"] for task in tasks):
        raise ValueError(f"received no judge votes for {bundle.name} (see judge_errors); expected a working judge")
    suite = score_suite([_outcome(task) for task in tasks], judge=subjective.label)
    for task, score in zip(tasks, suite.tasks):
        task.update(c=score.correctness, o=round(score.objective, 2), subjective=score.subjective)
    result["totals"] = totals_block(suite)
    result["judge"] = {"label": subjective.label, "model": judge_agent.model, "effort": judge_agent.effort,
                       "votes": votes, "deferred": True}
    result["environment"]["judge"] = {"model": judge_agent.model, "effort": judge_agent.effort, "votes": votes}
    result["judge_pending"] = False
    (bundle / RESULT_NAME).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
                                      newline="\n")
    scope = PathScope(names=local_names().allowing(result.get("submitter")))
    (bundle / SUMMARY_NAME).write_text(public_text(render_summary(result), scope), encoding="utf-8", newline="\n")
    return result
