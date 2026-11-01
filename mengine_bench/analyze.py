"""`mengine-bench analyze`: what separates runs, read from published results (#82). No agent runs.

Runs are not repeated, so the order is tested another way: draw the 14 tasks again with replacement, many
times, and count how often one run keeps its lead. That shows how much the order rests on this set of tasks.
It says nothing about the noise between two runs of the same agent.
"""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from statistics import mean, median

from mengine_bench.report import time_text
from mengine_bench.scoring import combined_score, speed_points

RESAMPLES = 2000
RESAMPLE_SEED = 82
# Under this share the lead is not read as a lead. On the 9 runs of bench 1.3, 2.2 points that hold in 66% of the
# draws are a tie and 0.8 points that hold in 86% are a lead: the fixed 1 point gap had both backwards. At 90%, 7 of
# the 8 neighbours were ties and the table said nothing.
TIE_BELOW = 0.8

Run = Mapping[str, object]


@dataclass(frozen=True)
class TaskPoint:
    correct: float
    judge: float
    seconds: float


def task_points(result: Run) -> dict[str, TaskPoint]:
    """One point per task, or nothing for a result that holds no per-task grades."""
    tasks = result["tasks"]
    assert isinstance(tasks, list)
    if not tasks or any(task.get("c") is None or task.get("judge") is None for task in tasks):
        return {}
    return {str(task["id"]): TaskPoint(float(task["c"]), float(task["judge"]), float(task.get("agent_s") or 0.0))
            for task in tasks}


def _score(points: Sequence[TaskPoint]) -> float:
    correct = 100 * mean(point.correct for point in points)
    time_s = sum(point.seconds for point in points)
    return combined_score(correct, mean(point.judge for point in points), speed_points(time_s)) or 0.0


def win_share(first: Mapping[str, TaskPoint], second: Mapping[str, TaskPoint]) -> float:
    """How often `first` beats `second` when the tasks are drawn again; a tied draw counts half."""
    ids = sorted(set(first) & set(second))
    rng = random.Random(RESAMPLE_SEED)
    wins = 0.0
    for _ in range(RESAMPLES):
        draw = rng.choices(ids, k=len(ids))
        a, b = _score([first[i] for i in draw]), _score([second[i] for i in draw])
        wins += 1.0 if a > b else 0.5 if a == b else 0.0
    return wins / RESAMPLES


def tie_note(ranked: Sequence[Run]) -> list[str]:
    """The leaderboard's line on neighbours whose lead does not hold when the tasks are drawn again."""
    pairs = []
    for rank, (higher, lower) in enumerate(zip(ranked, ranked[1:], strict=False), start=1):
        first, second = task_points(higher), task_points(lower)
        if first and second and (share := win_share(first, second)) < TIE_BELOW:
            pairs.append(f"#{rank} and #{rank + 1} ({share:.0%})")
    if not pairs:
        return []
    return [f"Read as ties, because the higher run keeps its lead in under {TIE_BELOW:.0%} of {RESAMPLES} draws of the "
            f"tasks: {', '.join(pairs)}. `mengine-bench analyze` shows the rest.\n"]


def _label(result: Run) -> str:
    agent = result["agent"]
    assert isinstance(agent, dict)
    return f"{agent.get('model')}/{agent.get('effort')}"


def _parts_table(runs: Sequence[Run]) -> list[str]:
    def points(key: str, share: float) -> list[float]:
        return [share * float(run["totals"][key]) for run in runs]  # type: ignore[index]

    speed = [0.15 * float(run["totals"]["speed"]) * float(run["totals"]["correct"]) / 100 for run in runs]  # type: ignore[index]
    parts = (("Correct", points("correct", 0.6)), ("Judge", points("judge", 0.25)), ("Speed", speed))
    return ["## Score points between the best and the worst run", "", "| part | points |", "| --- | --- |",
            *(f"| {name} | {max(values) - min(values):.1f} |" for name, values in parts)]


def _tasks_table(runs: Sequence[Run]) -> list[str]:
    rows: dict[str, list[Mapping[str, object]]] = {}
    for run in runs:
        tasks = run["tasks"]
        assert isinstance(tasks, list)
        for task in tasks:
            rows.setdefault(str(task["id"]), []).append(task)
    lines = ["## Tasks", "", "| task | lowest c | mean c | separates runs | judge range | median time | longest | timeouts |",
             "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for task_id, tasks in rows.items():
        scores = [float(task["c"]) for task in tasks]  # type: ignore[arg-type]
        votes = [int(task["judge"]) for task in tasks]  # type: ignore[call-overload]
        times = [float(task.get("agent_s") or 0.0) for task in tasks]  # type: ignore[arg-type]
        lines.append(f"| {task_id} | {min(scores):.2f} | {mean(scores):.2f} | {'yes' if max(scores) > min(scores) else 'no'} | "
                     f"{min(votes)}-{max(votes)} | {time_text(median(times))} | {time_text(max(times))} | "
                     f"{sum(task.get('status') == 'timeout' for task in tasks)} |")
    return lines


def _pairs_table(runs: Sequence[Run]) -> list[str]:
    ordered = sorted(runs, key=lambda run: -float(run["totals"]["score"] or 0.0))  # type: ignore[index]
    lines = ["## Neighbours on the ranking", "", f"Share of {RESAMPLES} draws of the tasks where the higher run stays "
             "ahead. This depends on the task set, not on the noise between two runs of one agent.", "",
             "| higher | lower | gap | stays ahead | read |", "| --- | --- | --- | --- | --- |"]
    for higher, lower in zip(ordered, ordered[1:], strict=False):
        share = win_share(task_points(higher), task_points(lower))
        gap = float(higher["totals"]["score"] or 0.0) - float(lower["totals"]["score"] or 0.0)  # type: ignore[index]
        lines.append(f"| {_label(higher)} | {_label(lower)} | {gap:.1f} | {share:.0%} | "
                     f"{'tie' if share < TIE_BELOW else 'lead'} |")
    return lines


def render_analysis(runs: Sequence[Run], version: str) -> str:
    sections = [[f"# Bench {version}: {len(runs)} judged runs"], _parts_table(runs), _tasks_table(runs), _pairs_table(runs)]
    return "\n\n".join("\n".join(section) for section in sections) + "\n"
