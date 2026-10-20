"""Run totals; the formulas are docs/SCORING.md verbatim (#23).

- Correct % = 100 * mean(c_i) over the tasks, c_i = share of scored checks
  passed (0 on a failed gate, a crash or a timeout).
- Judge = mean of the one rubric vote per task, 0-100 (set by `mengine-bench judge`).
- Score = 0.7 * Correct + 0.3 * Judge, from the published one-decimal values.
- Time = total agent wall seconds; Cost = USD with its basis. Neither is folded
  into Score. Comparability is the bench major.minor version, so there is no
  separate scoring version, no weights and no par times.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

from mengine_bench.runner.agents import Usage

STATUSES = ("ok", "timeout", "crash")
CORRECT_SHARE = 0.7
JUDGE_SHARE = 0.3
COST_BASES = ("harness", "price", "n/a")
PRICE_KEYS = ("input", "cached", "output")
PRICE_FORMAT = "input=X,cached=Y,output=Z in USD per million tokens, or 0 for free/local inference"
MTOK = 1_000_000


@dataclass(frozen=True)
class Price:
    """Declared USD per million tokens; reasoning tokens are already inside output."""

    input: float
    cached: float
    output: float

    def cost_usd(self, usage: Usage) -> float | None:
        if usage.input_tokens is None or usage.output_tokens is None:
            return None
        cached = usage.cached_input_tokens or 0
        return ((usage.input_tokens - cached) * self.input + cached * self.cached
                + usage.output_tokens * self.output) / MTOK


def parse_price(text: str) -> Price:
    """`--price input=X,cached=Y,output=Z` (USD per Mtok) or `--price 0`."""
    if text.strip() == "0":
        return Price(0.0, 0.0, 0.0)
    values: dict[str, float] = {}
    for part in text.split(","):
        key, _, raw = part.partition("=")
        try:
            number = float(raw)
        except ValueError:
            number = math.nan
        if key.strip() not in PRICE_KEYS or not math.isfinite(number) or number < 0:
            raise ValueError(f"received --price {text!r}; expected {PRICE_FORMAT}")
        values[key.strip()] = number
    if set(values) != set(PRICE_KEYS):
        raise ValueError(f"received --price {text!r}; expected {PRICE_FORMAT}")
    return Price(**values)


@dataclass(frozen=True)
class TaskOutcome:
    """What a run produced for one task, before scoring."""

    task_id: str
    status: str
    correctness: float  # CheckResult.score: share of scored checks passed, 0 on a failed gate
    solved: bool
    agent_s: float | None  # agent wall time, grading and judging excluded; timeouts count in full
    step_usages: tuple[Usage | None, ...] = ()  # one per started step; None = unmeasured
    judge: int | None = None


@dataclass(frozen=True)
class TokenTotals:
    """Sums of the token counts that were measured."""

    input: int = 0
    cached_input: int = 0
    output: int = 0
    reasoning: int = 0


@dataclass(frozen=True)
class Cost:
    usd: float | None
    basis: str  # one of COST_BASES
    # True when a step has no usage (crash, timeout) or a partial one: the true cost is higher.
    lower_bound: bool


@dataclass(frozen=True)
class TaskScore:
    task_id: str
    status: str
    correctness: float
    solved: bool
    agent_s: float | None
    judge: int | None
    cost_usd: float | None
    tokens: TokenTotals


@dataclass(frozen=True)
class RunScore:
    correct: float
    solved: int
    total: int
    judge: float | None
    score: float | None
    time_s: float
    cost: Cost
    tokens: TokenTotals
    tasks: tuple[TaskScore, ...]


def combined_score(correct: float, judge: float | None) -> float | None:
    """Score from the published Correct % and Judge, so anyone recomputes it from the table."""
    if judge is None:
        return None
    return round(CORRECT_SHARE * correct + JUDGE_SHARE * judge, 1)


def judge_mean(votes: Sequence[int | None]) -> float | None:
    """Mean vote, None before judging; a partly judged run is an error, not a smaller mean."""
    judged = [vote for vote in votes if vote is not None]
    if not judged:
        return None
    if len(judged) != len(votes):
        raise ValueError(f"received judge votes for {len(judged)} of {len(votes)} tasks; expected all or none")
    return round(sum(judged) / len(judged), 1)


def _validate(outcome: TaskOutcome) -> None:
    if outcome.status not in STATUSES:
        raise ValueError(f"task {outcome.task_id!r} received status {outcome.status!r}; expected one of {STATUSES}")
    if not 0.0 <= outcome.correctness <= 1.0:
        raise ValueError(f"task {outcome.task_id!r} received correctness {outcome.correctness!r}; expected 0..1")
    vote = outcome.judge
    if vote is not None and (type(vote) is not int or not 0 <= vote <= 100):
        raise ValueError(f"task {outcome.task_id!r} received judge {vote!r}; expected an int 0..100 or None")


def _measured(outcomes: Sequence[TaskOutcome]) -> list[Usage]:
    return [usage for outcome in outcomes for usage in outcome.step_usages if usage is not None]


def _basis(outcomes: Sequence[TaskOutcome], price: Price | None) -> str:
    measured = _measured(outcomes)
    if not measured:
        return "n/a"
    if all(usage.cost_usd is not None for usage in measured):
        return "harness"
    if price is not None and all(price.cost_usd(usage) is not None for usage in measured):
        return "price"
    return "n/a"


def _usd(usages: Sequence[Usage], basis: str, price: Price | None) -> float | None:
    if basis == "harness":
        return sum(usage.cost_usd or 0.0 for usage in usages)
    if basis == "price" and price is not None:
        return sum(price.cost_usd(usage) or 0.0 for usage in usages)
    return None


def _tokens(usages: Sequence[Usage]) -> TokenTotals:
    return TokenTotals(input=sum(u.input_tokens or 0 for u in usages),
                       cached_input=sum(u.cached_input_tokens or 0 for u in usages),
                       output=sum(u.output_tokens or 0 for u in usages),
                       reasoning=sum(u.reasoning_tokens or 0 for u in usages))


def _round_usd(value: float | None) -> float | None:
    return None if value is None else round(value, 4)


def _task_score(outcome: TaskOutcome, basis: str, price: Price | None) -> TaskScore:
    ok = outcome.status == "ok"
    usages = _measured([outcome])
    return TaskScore(task_id=outcome.task_id, status=outcome.status, correctness=outcome.correctness if ok else 0.0,
                     solved=ok and outcome.solved, agent_s=outcome.agent_s, judge=outcome.judge,
                     cost_usd=_round_usd(_usd(usages, basis, price)) if usages else 0.0 if basis != "n/a" else None,
                     tokens=_tokens(usages))


def score_run(outcomes: Sequence[TaskOutcome], price: Price | None = None) -> RunScore:
    if not outcomes:
        raise ValueError("received no task outcomes; expected at least one")
    for outcome in outcomes:
        _validate(outcome)
    basis = _basis(outcomes, price)
    tasks = tuple(_task_score(outcome, basis, price) for outcome in outcomes)
    measured = _measured(outcomes)
    unmeasured = any(usage is None for outcome in outcomes for usage in outcome.step_usages)
    partial = any(usage.cost_source == "partial" for usage in measured)
    correct = round(100.0 * sum(task.correctness for task in tasks) / len(tasks), 1)
    judge = judge_mean([task.judge for task in tasks])
    return RunScore(
        correct=correct, solved=sum(task.solved for task in tasks), total=len(tasks), judge=judge,
        score=combined_score(correct, judge), time_s=round(sum(task.agent_s or 0.0 for task in tasks), 1),
        cost=Cost(usd=_round_usd(_usd(measured, basis, price)), basis=basis, lower_bound=unmeasured or partial),
        tokens=_tokens(measured), tasks=tasks,
    )
