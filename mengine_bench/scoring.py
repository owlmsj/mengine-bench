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
MANDATORY_CAP = 0.5
SPEED_SHARE = 0.2
COMPOSITE_OBJECTIVE_SHARE = 0.6


@dataclass(frozen=True)
class TaskOutcome:
    """What a run produced for one task, before scoring."""

    task_id: str
    category: str
    weight: int
    par_s: float
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
    weight: int
    status: str
    correctness: float
    solved: bool
    speed: float
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
    suite: str
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
    speed = _speed(outcome) if solved else 0.0
    objective = 100.0 * correctness * ((1.0 - SPEED_SHARE) + SPEED_SHARE * speed)
    return TaskScore(
        task_id=outcome.task_id, category=outcome.category, weight=outcome.weight,
        status=outcome.status, correctness=correctness, solved=solved, speed=speed,
        objective=objective, agent_s=outcome.agent_s, subjective=_median_vote(outcome),
    )


def _correctness(outcome: TaskOutcome) -> tuple[float, bool]:
    if outcome.status != "ok":
        return 0.0, False
    if not outcome.mandatory_ok:
        return min(outcome.check_score, MANDATORY_CAP), False
    return outcome.check_score, outcome.passed


def _speed(outcome: TaskOutcome) -> float:
    if outcome.agent_s is None or outcome.agent_s <= 0:
        # No timing means no speed credit; never reward a missing measurement.
        return 0.0 if outcome.agent_s is None else 1.0
    return min(1.0, outcome.par_s / outcome.agent_s)


def _median_vote(outcome: TaskOutcome) -> float | None:
    if not outcome.judge_votes:
        return None
    bad = [vote for vote in outcome.judge_votes if not 0 <= vote <= 100]
    if bad:
        raise ValueError(f"task {outcome.task_id!r} received judge votes {bad}; expected ints 0..100")
    return float(statistics.median(outcome.judge_votes))


def _weighted_mean(pairs: Sequence[tuple[int, float]]) -> float:
    total_weight = sum(weight for weight, _ in pairs)
    return sum(weight * value for weight, value in pairs) / total_weight


def _category_scores(scored: Sequence[TaskScore]) -> dict[str, CategoryScore]:
    result: dict[str, CategoryScore] = {}
    for category in sorted({task.category for task in scored}):
        group = [task for task in scored if task.category == category]
        result[category] = CategoryScore(
            objective=round(_weighted_mean([(t.weight, t.objective) for t in group]), 1),
            accuracy=round(_weighted_mean([(t.weight, 100.0 * t.correctness) for t in group]), 1),
            solved=sum(t.solved for t in group),
            total=len(group),
        )
    return result


def score_suite(suite: str, outcomes: Sequence[TaskOutcome], judge: str | None = None) -> SuiteScore:
    """Aggregate one run. `judge` names model and effort; required with votes
    because scores from different judges are not comparable."""
    if not outcomes:
        raise ValueError(f"suite {suite!r} received no task outcomes; expected at least one")
    scored = tuple(score_task(outcome) for outcome in outcomes)
    judged = any(task.subjective is not None for task in scored)
    if judged and not judge:
        raise ValueError(f"suite {suite!r} has judge votes but judge={judge!r}; expected 'model@effort'")
    objective = round(_weighted_mean([(t.weight, t.objective) for t in scored]), 1)
    subjective = None
    if judged:
        # A task the judge could not grade (no votes) counts as 0, so skipping
        # hard tasks never inflates the subjective score.
        subjective = round(_weighted_mean([(t.weight, t.subjective or 0.0) for t in scored]), 1)
    composite = None
    if subjective is not None:
        share = COMPOSITE_OBJECTIVE_SHARE
        composite = round(share * objective + (1 - share) * subjective, 1)
    return SuiteScore(
        suite=suite, scoring_version=SCORING_VERSION, objective=objective,
        accuracy=round(_weighted_mean([(t.weight, 100.0 * t.correctness) for t in scored]), 1),
        solved=sum(t.solved for t in scored), total=len(scored),
        total_agent_s=round(sum(t.agent_s or 0.0 for t in scored), 1),
        subjective=subjective, composite=composite, judge=judge if judged else None,
        unsupported=tuple(t.task_id for t in scored if t.status == "unsupported"),
        tasks=scored, by_category=_category_scores(scored),
    )
