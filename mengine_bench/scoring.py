"""Objective and subjective scores; the formulas are docs/SCORING.md verbatim.

Bump SCORING_VERSION on any formula change: reports carry it and the
leaderboard never mixes versions.
"""

from __future__ import annotations

import statistics
from collections.abc import Sequence
from dataclasses import dataclass, field

SCORING_VERSION = "1.0"

STATUSES = ("ok", "timeout", "crash", "unsupported")
COMPOSITE_OBJECTIVE_SHARE = 0.6


@dataclass(frozen=True)
class TaskOutcome:
    """What a run produced for one task, before scoring."""

    task_id: str
    category: str
    check_score: float  # share of checks passed, 0..1
    mandatory_ok: bool
    passed: bool  # the task's own pass rule (CheckResult.passed)
    agent_s: float | None  # agent wall time, grading and judging excluded
    status: str = "ok"
    judge_votes: tuple[int, ...] = ()


@dataclass(frozen=True)
class TaskScore:
    task_id: str
    category: str
    status: str
    correctness: float
    solved: bool
    objective: float
    agent_s: float | None
    subjective: float | None


@dataclass(frozen=True)
class CategoryScore:
    objective: float
    accuracy: float
    solved: int
    total: int


@dataclass(frozen=True)
class SuiteScore:
    scoring_version: str
    objective: float
    accuracy: float
    solved: int
    total: int
    total_agent_s: float
    subjective: float | None
    composite: float | None
    judge: str | None
    unsupported: tuple[str, ...]
    tasks: tuple[TaskScore, ...]
    by_category: dict[str, CategoryScore] = field(default_factory=dict)


def score_task(outcome: TaskOutcome) -> TaskScore:
    if outcome.status not in STATUSES:
        raise ValueError(f"task {outcome.task_id!r} received status {outcome.status!r}; expected one of {STATUSES}")
    if not 0.0 <= outcome.check_score <= 1.0:
        raise ValueError(f"task {outcome.task_id!r} received check_score {outcome.check_score}; expected 0..1")
    correctness, solved = _correctness(outcome)
    objective = 100.0 * correctness
    return TaskScore(
        task_id=outcome.task_id, category=outcome.category,
        status=outcome.status, correctness=correctness, solved=solved,
        objective=objective, agent_s=outcome.agent_s, subjective=_median_vote(outcome),
    )


def _correctness(outcome: TaskOutcome) -> tuple[float, bool]:
    if outcome.status != "ok":
        return 0.0, False
    if not outcome.mandatory_ok:
        return 0.0, False
    return outcome.check_score, outcome.passed


def _median_vote(outcome: TaskOutcome) -> float | None:
    if not outcome.judge_votes:
        return None
    bad = [vote for vote in outcome.judge_votes if not 0 <= vote <= 100]
    if bad:
        raise ValueError(f"task {outcome.task_id!r} received judge votes {bad}; expected ints 0..100")
    return float(statistics.median(outcome.judge_votes))


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def _category_scores(scored: Sequence[TaskScore]) -> dict[str, CategoryScore]:
    result: dict[str, CategoryScore] = {}
    for category in sorted({task.category for task in scored}):
        group = [task for task in scored if task.category == category]
        result[category] = CategoryScore(
            objective=round(_mean([t.objective for t in group]), 1),
            accuracy=round(_mean([100.0 * t.correctness for t in group]), 1),
            solved=sum(t.solved for t in group),
            total=len(group),
        )
    return result


def score_suite(outcomes: Sequence[TaskOutcome], judge: str | None = None) -> SuiteScore:
    """Aggregate one run. `judge` names model and effort; required with votes
    because scores from different judges are not comparable."""
    if not outcomes:
        raise ValueError("received no task outcomes; expected at least one")
    scored = tuple(score_task(outcome) for outcome in outcomes)
    judged = any(task.subjective is not None for task in scored)
    if judged and not judge:
        raise ValueError(f"received judge votes but judge={judge!r}; expected 'model@effort'")
    objective = round(_mean([t.objective for t in scored]), 1)
    subjective = None
    if judged:
        # A task the judge could not grade (no votes) counts as 0, so skipping
        # hard tasks never inflates the subjective score.
        subjective = round(_mean([t.subjective or 0.0 for t in scored]), 1)
    composite = None
    if subjective is not None:
        share = COMPOSITE_OBJECTIVE_SHARE
        composite = round(share * objective + (1 - share) * subjective, 1)
    return SuiteScore(
        scoring_version=SCORING_VERSION, objective=objective,
        accuracy=round(_mean([100.0 * t.correctness for t in scored]), 1),
        solved=sum(t.solved for t in scored), total=len(scored),
        total_agent_s=round(sum(t.agent_s or 0.0 for t in scored), 1),
        subjective=subjective, composite=composite, judge=judge if judged else None,
        unsupported=tuple(t.task_id for t in scored if t.status == "unsupported"),
        tasks=scored, by_category=_category_scores(scored),
    )
