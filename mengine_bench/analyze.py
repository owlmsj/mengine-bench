"""`mengine-bench analyze`: what separates runs, read from published results (#82). No agent runs.

Task resampling tests how much the order rests on this task set. Same-setup reruns separately measure
run-to-run noise; without a repeated setup that floor is not measured.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from statistics import mean, median, stdev

from mengine_bench.report import time_text
from mengine_bench.scoring import CORRECT_SHARE, JUDGE_SHARE, SPEED_SHARE, combined_score, speed_points

RESAMPLES = 2000
RESAMPLE_SEED = 82
# Under this share the lead is not read as a lead. On the 9 runs of bench 1.3, 2.2 points that hold in 66% of the
# draws are a tie and 0.8 points that hold in 86% are a lead: the fixed 1 point gap had both backwards. At 90%, 7 of
# the 8 neighbours were ties and the table said nothing.
TIE_BELOW = 0.8
# Ignore increases up to 25% so small time/token fluctuations do not warn (#94).
TIME_INCREASE_LIMIT = 0.25
INPUT_TOKEN_INCREASE_LIMIT = 0.25
# Six points was the largest measured difference between two judge votes on the same message (#94).
JUDGE_DROP_LIMIT = 6

Run = Mapping[str, object]


def setup_key(result: Run) -> str:
    """Published setup identity, computed on read; patch and executable versions are not setup changes (#185)."""
    agent = result["agent"]
    assert isinstance(agent, dict)
    config = json.dumps(result.get("config") or {}, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    digest = hashlib.sha256(config.encode("utf-8")).hexdigest()[:12]
    minor = ".".join(str(result.get("bench_version")).split(".")[:2])
    return f"{agent.get('name')}/{agent.get('model')}/{agent.get('effort')}/{digest}/{minor}"


def _setup_groups(runs: Sequence[Run]) -> dict[str, list[Run]]:
    groups: dict[str, list[Run]] = {}
    for run in runs:
        groups.setdefault(setup_key(run), []).append(run)
    return {key: group for key, group in groups.items() if len(group) > 1}


def _metric_values(runs: Sequence[Run], metric: str) -> list[float]:
    values = [run["totals"].get(metric) for run in runs]  # type: ignore[union-attr]
    return [float(value) for value in values if isinstance(value, (int, float))]


def score_noise_floor(runs: Sequence[Run]) -> float | None:
    """The largest measured Score range among same-setup reruns, or no measurement."""
    scores = [_metric_values(group, "score") for group in _setup_groups(runs).values()]
    spreads = [max(values) - min(values) for values in scores if len(values) > 1]
    return max(spreads) if spreads else None


def _noise_section(runs: Sequence[Run]) -> list[str]:
    lines = ["## Same setup, several runs", ""]
    groups = _setup_groups(runs)
    for key, group in sorted(groups.items()):
        lines.extend([f"Setup `{key}` ({len(group)} runs)", "", "| metric | max-min | sample stdev |",
                      "| --- | --- | --- |"])
        for label, metric in (("Score", "score"), ("Correct %", "correct"), ("Judge", "judge"), ("Time (s)", "time_s")):
            values = _metric_values(group, metric)
            spread = f"{max(values) - min(values):.1f} | {stdev(values):.1f}" if len(values) > 1 else "not measured | not measured"
            lines.append(f"| {label} | {spread} |")
        lines.append("")
    floor = score_noise_floor(runs)
    lines.append(f"noise floor: {floor:.1f} Score points" if floor is not None else
                 "noise floor: not measured (no setup has two runs)")
    return lines


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

    speed = [SPEED_SHARE * float(run["totals"]["speed"]) * float(run["totals"]["correct"]) / 100 for run in runs]  # type: ignore[index]
    parts = (("Correct", points("correct", CORRECT_SHARE)), ("Judge", points("judge", JUDGE_SHARE)), ("Speed", speed))
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


def _regression_warnings(previous: Run, latest: Run, time_key: str, noise_floor: float | None = None) -> list[str]:
    if noise_floor is None:
        return []
    old_score, new_score = previous.get("score"), latest.get("score")
    if isinstance(old_score, (int, float)) and isinstance(new_score, (int, float)):
        if old_score - new_score <= noise_floor:
            return []
    passed = {check["name"] for check in previous.get("checks", []) if check.get("ok") is True}
    warnings = [f"check failed: {check['name']}" for check in latest.get("checks", [])
                if check.get("ok") is False and check["name"] in passed]
    if isinstance(old_score, (int, float)) and isinstance(new_score, (int, float)):
        warnings.append(f"Score: {old_score:g} -> {new_score:g}")
    old_tokens, new_tokens = previous.get("tokens") or {}, latest.get("tokens") or {}
    metrics = (("Time", previous.get(time_key), latest.get(time_key), TIME_INCREASE_LIMIT),
               ("Judge", previous.get("judge"), latest.get("judge"), None),
               ("Input tokens", old_tokens.get("input"), new_tokens.get("input"), INPUT_TOKEN_INCREASE_LIMIT))
    for label, before, after, increase in metrics:
        if not isinstance(before, (int, float)) or not isinstance(after, (int, float)):
            continue
        worse = before - after > JUDGE_DROP_LIMIT if increase is None else after > before * (1 + increase)
        if worse:
            warnings.append(f"{label}: {before:g} -> {after:g}")
    return warnings


def _changed_tasks(previous: Run, latest: Run, noise_floor: float) -> list[str]:
    old_tasks = {task["id"]: task for task in previous["tasks"]}
    lines = []
    for task in latest["tasks"]:
        before = old_tasks.get(task["id"])
        if before is None:
            continue
        warnings = _regression_warnings(before, task, "agent_s", noise_floor)
        if warnings:
            lines.append(f"  - {task['id']}: {'; '.join(warnings)}")
    return lines


def _run_date(run: Run) -> str:
    return str(run.get("started_at") or run.get("date") or "")


def _changes_section(runs: Sequence[Run], noise_floor: float | None = None) -> list[str]:
    groups: dict[str, list[Run]] = {}
    for run in runs:
        if not _run_date(run):
            continue
        groups.setdefault(setup_key(run), []).append(run)
    lines = ["## Changes since the last run", ""]
    repeated = [key for key, group in groups.items() if len(group) > 1]
    for key in repeated:
        previous, latest = sorted(groups[key], key=_run_date)[-2:]
        if len(_metric_values([previous, latest], "score")) < 2:
            continue
        warnings = _regression_warnings(previous["totals"], latest["totals"], "time_s", noise_floor)
        if not warnings:
            continue
        agent = latest["agent"]
        lines.append(f"- {agent.get('name')} {agent.get('model')}/{agent.get('effort')}, setup {key} "
                     f"({_run_date(previous)} -> {_run_date(latest)})")
        lines.append(f"  - Run: {'; '.join(warnings)}")
        assert noise_floor is not None
        lines.extend(_changed_tasks(previous, latest, noise_floor))
    if len(lines) == 2:
        lines.append("No repeated combinations to compare." if not repeated else
                     "noise floor: not measured" if noise_floor is None else "No warnings.")
    return lines


def render_analysis(runs: Sequence[Run], version: str) -> str:
    sections = [[f"# Bench {version}: {len(runs)} judged runs"], _parts_table(runs), _tasks_table(runs), _pairs_table(runs),
                _noise_section(runs), _changes_section(runs, score_noise_floor(runs))]
    return "\n\n".join("\n".join(section) for section in sections) + "\n"
