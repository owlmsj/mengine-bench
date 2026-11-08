"""LEADERBOARD.md from `results/*/result.json`: one table (#23).

Scores are self-reported: the maintainer reviews each result pull request,
judges the bundle, and the table trusts what was merged. A run is ranked when
it ran the current bench major.minor (a patch changes no task or prompt; when it
changes how runs are judged, the ranked ones are judged again from their bundles),
holds every catalog task exactly once, and was judged by the official judge. Everything
else is listed under "Not ranked" with the reason.
"""

from __future__ import annotations

import gzip
import json
import os
import statistics
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

from mengine_bench import __version__, catalog
from mengine_bench.analyze import tie_note
from mengine_bench.bundle import RESULT_NAME, SUMMARY_NAME
from mengine_bench.judge import OFFICIAL_JUDGE_EFFORT, OFFICIAL_JUDGE_MODEL, RUBRIC_VERSION
from mengine_bench.prices import price_text
from mengine_bench.report import count_text, hardware_short_text, time_text, tokens_text
from mengine_bench.runner.stats import stream_stats
from mengine_bench.scoring import (CORRECT_SHARE, JUDGE_SHARE, SPEED_FULL_S, SPEED_SHARE, SPEED_ZERO_S, combined_score,
                                   speed_points)

# #223: downloadable final workspaces of tasks whose deliverable is visual.
VISUAL_WORKSPACES = ("web-mondrian-landing", "web-word-universe", "file-media-edit", "3d-print-homage",
                     "web-archery-game")
CONFIG_CELL_CHARS = 60
# #99: an older run never had these tasks, so it stays complete and its ranking stays in the history.
# Older runs stay in the history: they match the catalog apart from the tasks that came and went since (#99, #103).
TASKS_CHANGED_SINCE_1_5 = frozenset({"web-word-universe", "ue-packaged-bug", "rs-lock-bug", "gd-astar-doors", "gd-ecs-collision-bug"})
# #124: bench 2.0 dropped three saturated evals, rewrote the 3D one and added eight.
TASKS_CHANGED_IN_2_0 = frozenset({"lc-changelog", "vis-chart", "ir-studio-wiki", "3d-voxel-landscape", "3d-print-homage",
                                  "cfg-source-drift", "git-merge-conflict", "ts-plugin-bug", "sec-leak-fix", "infra-gpu-fit",
                                  "hw-stutter-tuning", "doc-lab-pdf", "web-plan-ranking"})
# #151: bench 2.2 added three tasks ported from Terminal-Bench 2.1.
TASKS_ADDED_IN_2_2 = frozenset({"txt-regex-log", "ds-sqlite-recover", "py-async-cancel"})
# #153: bench 2.3 adds computer use and basic media. More 2.3 ids go here only; the note below follows.
TASKS_ADDED_IN_2_3 = frozenset({"cu-social-cycle", "media-voice", "cu-webmail", "web-fact-search", "file-media-edit"})
# #218: bench 2.8 adds the archery game, judged by play (#213, #214).
TASKS_ADDED_IN_2_8 = frozenset({"web-archery-game"})
TASKS_THAT_CAME_AND_WENT = (TASKS_CHANGED_SINCE_1_5 | TASKS_CHANGED_IN_2_0 | TASKS_ADDED_IN_2_2 | TASKS_ADDED_IN_2_3
                            | TASKS_ADDED_IN_2_8)
# #139: the owner kept the 2.0 runs ranked in 2.1, which only shortened the time limits (#137); they cost real runs.
# #151: and kept the 2.0 and 2.1 runs ranked in 2.2, which added three tasks; #153: and all three in 2.3;
# #161: and all four in 2.4, which adds a scored cleanup check to the two site tasks.
# #164: and all five in 2.5, which hardens checks the older runs were graded without; their Score uses the 2.5
# weights from their own published values.
RANKED_WITH_CURRENT: dict[str, frozenset[str]] = {"2.1": frozenset({"2.0"}), "2.2": frozenset({"2.0", "2.1"}),
                                                  "2.3": frozenset({"2.0", "2.1", "2.2"}),
                                                  "2.4": frozenset({"2.0", "2.1", "2.2", "2.3"}),
                                                  "2.5": frozenset({"2.0", "2.1", "2.2", "2.3", "2.4"}),
                                                  # #185: 2.6 changes no task, prompt or limit. #187 (owner, 2026-11-04): the
                                                  # 20- and 23-task rows (2.0 to 2.2) move to history; one catalog per ranking.
                                                  "2.6": frozenset({"2.3", "2.4", "2.5"}),
                                                  # #210 (owner, 2026-11-06): 2.7 changes only the Score formula.
                                                  "2.7": frozenset({"2.3", "2.4", "2.5", "2.6"}),
                                                  # #218 (owner, 2026-11-07): 2.8 adds web-archery-game; the
                                                  # 28-task rows stay ranked, marked, without a vote on it.
                                                  "2.8": frozenset({"2.3", "2.4", "2.5", "2.6", "2.7"})}
# #185: a rubric bump used to unrank every run until it was judged again (about 380 Opus xhigh votes for 2.6). The
# older rubric's votes stay ranked until the owner re-judges, marked on the row as "(rubric 2.5)".
RANKED_RUBRICS: dict[str, frozenset[str]] = {"2.6": frozenset({"2.5"})}
RANKED_WITH_NOTE = ("Bench 2.3 to 2.7 runs stay in this ranking (#153, #161, #164, #185, #187, #210, #218): they ran the "
                    f"{23 + len(TASKS_ADDED_IN_2_3)}-task catalog, without web-archery-game (added in 2.8, #218), each row "
                    "marked with its version, and every Score and "
                    "Speed here use the 2.7 formula (#210), recomputed from the row's published Correct %, Judge and Time; "
                    "no run was run or judged again.\nA row marked 2.4 or older was graded without the 2.5 checks (fetched "
                    "sources, workspace writes and more, #164); a row marked 2.3 also lacks the 2.4 check that cu-social-cycle "
                    "and cu-webmail\nclose the tabs and apps they opened; a row marked \"rubric 2.5\" keeps its 2.5 judge votes "
                    "until it is judged again (#185).\nThe bench 2.0 to 2.2 runs (20 and 23 tasks) moved to history on "
                    "2026-11-04 (#187), with the Scores of their own version.\n")
# #146: runs the owner keeps on the board without ranking them, by bundle name, with why.
OBSERVED_RUNS: dict[str, str] = {
    # Owner (2026-11-04): replaced by a rerun of the same setup on bench 2.5.2.
    "2026-11-03_claude_claude-opus-5-5_low_0756f921": (
        "Opus 5.5 low on bench 2.4.0, replaced in the ranking by the same setup rerun on 2.5.2 "
        "(2026-11-03_claude_claude-opus-5-5_low_eb72035c), graded with the 2.5 checks."),
    # #164: the validation run of the 2.5 checks, kept on the board with its reason.
    "2026-11-03_claude_claude-opus-5-5_low_01327b0c": (
        "Opus 5.5 low on a 2.5.0 pre-release commit (529a84d), before the final fetch-evidence rules and four "
        "parser fixes of #164; it validated the new checks (every failure checked by hand was real), so it is "
        "shown, not ranked."),
    # #187: the clean Codex Astra run of 2026-11-02 (#146: three tasks never answered) is bench 2.1 history now.
}
# #193: the ranking fits a laptop screen; the #162 run stats (thinking, tool calls, seconds per call) fold below it.
# #210: Date after Setup, so a rerun of one preset reads apart from the others.
COLUMNS = ("#", "Score", "Setup", "Date", "Correct %", "Solved", "Judge", "Speed", "Time", "Cost", "Run")
DETAIL_COLUMNS = ("#", "Model", "Timeouts", "Tokens", "Generated", "Thinking", "Turns", "Tools", "Tool s", "Hardware",
                  "Config", "Submitter", "Date")
DETAILS_SUMMARY = "Run details: tokens, turns, tools, hardware, config"
# #210 (owner, 2026-11-06): a preset keeps its latest runs ranked; older reruns fold below so one setup run many times
# does not crowd the ranking.
RUNS_RANKED_PER_PRESET = 3
OLDER_RUNS_SUMMARY = f"Older runs of ranked setups (beyond the {RUNS_RANKED_PER_PRESET} most recent of each)"
CONSISTENCY_SUMMARY = "Consistency of setups with several ranked runs"
COST_LEGEND = ("Cost: `$x` as the harness reported it, `~$x` estimated from the run's tokens at API list prices, "
               "`$0.00 (local)` a local model, `>=` a lower bound (a step went unmeasured), `n/a` neither. "
               "Tool s: median seconds per tool call, `-` where the harness does not time each call.\n")

LEADERBOARD_HEADER = """# Leaderboard

Generated by `mengine-bench leaderboard` from `results/*/result.json`; do not
edit by hand. Score = {CORRECT_SHARE} x Correct % + {JUDGE_SHARE} x Judge + {SPEED_SHARE} x Speed x Correct % / 100, Speed 100 at
{SPEED_FULL_S:g} min of Time or less, 0 at {SPEED_ZERO_S:g} min or more (docs/SCORING.md); Cost
(exact or estimated, legend below the table) never counts; the run statistics fold under each table. Runs are self-reported by each submitter and judged
by the maintainer on review; the transcripts are in each bundle. Only complete,
judged runs of the current bench version are ranked. A setup (harness, model and effort) keeps its
{RUNS} most recent runs ranked; its older runs fold below the table (#210). Older rankings stay below as history:
their Scores and Speeds use that version's formula and do not compare with the table above.
""".format(CORRECT_SHARE=CORRECT_SHARE, JUDGE_SHARE=JUDGE_SHARE, SPEED_SHARE=SPEED_SHARE, SPEED_FULL_S=SPEED_FULL_S / 60,
           SPEED_ZERO_S=SPEED_ZERO_S / 60, RUNS=RUNS_RANKED_PER_PRESET)


@dataclass(frozen=True)
class RankedBundle:
    result: dict[str, object]
    summary_link: str
    # #162: median seconds per tool call, from the result or else the bundle's transcripts.
    tool_s: float | None = None
    # #164: the Score shown and ranked; the current table recomputes it with today's weights.
    score: float | None = None
    # #210: the Speed shown; the current table recomputes it from Time on today's line, history keeps its own.
    speed: float | None = None


@dataclass(frozen=True)
class Leaderboard:
    markdown: str
    ranked: int
    history: int = 0
    # (bundle, why it is not ranked)
    unranked: list[tuple[str, str]] = field(default_factory=list)


def _fmt(value: object) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.1f}"
    return str(value)


def _link(path: Path, base: Path) -> str:
    return Path(os.path.relpath(path.resolve(), base.resolve())).as_posix()


def major_minor(version: object) -> str:
    """Runs compare within a bench major.minor; a patch changes no task, prompt or score."""
    return ".".join(str(version).split(".")[:2])


def ranked_versions() -> frozenset[str]:
    """The bench major.minor versions ranked together: the current one and any the owner kept with it (#139)."""
    current = major_minor(__version__)
    return frozenset({current}) | RANKED_WITH_CURRENT.get(current, frozenset())


def is_complete_run(result: dict[str, object]) -> bool:
    """True when the run holds every catalog task of its own bench version exactly once."""
    tasks = result["tasks"]
    assert isinstance(tasks, list)
    ids = [str(task["id"]) for task in tasks]
    expected = {task.id for task in catalog.all_tasks()}
    # #151: a ranked older version (a 2.1 run under 2.2) is complete on its own catalog, not the current one.
    if major_minor(result.get("bench_version")) != major_minor(__version__):
        return len(ids) == len(set(ids)) and set(ids) - TASKS_THAT_CAME_AND_WENT == expected - TASKS_THAT_CAME_AND_WENT
    return len(ids) == len(set(ids)) and set(ids) == expected


def _infra_reason(result: dict[str, object]) -> str | None:
    from mengine_bench.runner.infra_faults import infra_fault

    for task in result.get("tasks", []):
        if task.get("status") == "infra":
            signature = infra_fault(task.get("flags", [])) or "host refusal"
            return f"infra fault on {task['id']}: {signature}; rerun that task"
    return None


def unranked_reason(result: dict[str, object]) -> str | None:
    """Why a run is not ranked, or None when it is."""
    if reason := _infra_reason(result):
        return reason
    if major_minor(result.get("bench_version")) not in ranked_versions():
        ranked = " and ".join(f"{version}.x" for version in sorted(ranked_versions(), key=_version_key))
        return f"older bench {result.get('bench_version')}; only bench {ranked} runs are ranked"
    if not is_complete_run(result):
        return "incomplete: not exactly every catalog task once (a --tasks run, or a crash before the bundle)"
    judge = result.get("judge")
    if not isinstance(judge, dict):
        return "waiting for the judge (`mengine-bench judge`)"
    used = f"{judge.get('agent')} {judge.get('model')}@{judge.get('effort')} rubric {judge.get('rubric')}"
    rubrics = ", ".join(sorted(ranked_rubrics(), key=_version_key))
    official = f"claude {OFFICIAL_JUDGE_MODEL}@{OFFICIAL_JUDGE_EFFORT} rubric {rubrics}"
    accepted = {f"claude {OFFICIAL_JUDGE_MODEL}@{OFFICIAL_JUDGE_EFFORT} rubric {rubric}" for rubric in ranked_rubrics()}
    if used not in accepted:
        return f"judged by {used}; only {official} judges are ranked"
    return None


def ranked_rubrics() -> frozenset[str]:
    """The judge rubrics ranked together: the current one and any older one kept until a re-judge (#185)."""
    return frozenset({RUBRIC_VERSION}) | RANKED_RUBRICS.get(RUBRIC_VERSION, frozenset())


def _history_version(result: dict[str, object]) -> str | None:
    """The older bench major.minor of a complete run the official judge model voted on, else None."""
    version = major_minor(result.get("bench_version"))
    judge = result.get("judge")
    if version in ranked_versions() or not is_complete_run(result) or not isinstance(judge, dict):
        return None
    official = (judge.get("agent"), judge.get("model"), judge.get("effort")) == ("claude", OFFICIAL_JUDGE_MODEL,
                                                                                 OFFICIAL_JUDGE_EFFORT)
    return version if official else None


def _version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def _by_score(entry: RankedBundle) -> float:
    return -float(entry.score or 0.0)


def current_speed(totals: dict[str, object]) -> float | None:
    """#210: Speed on today's line from the run's published Time; 2.7 moved it from 5/30 min to 10/40 min."""
    time_s = totals.get("time_s")
    return speed_points(float(time_s)) if isinstance(time_s, (int, float)) else None


def current_score(totals: dict[str, object]) -> float | None:
    """#164 #210: Score with today's formula from the run's published Correct %, Judge and Time.

    Weights changed in 2.5, and weights and the Speed line in 2.7; every ranked run is recomputed from its own
    published values, so no number is edited by hand and no run is judged again. History keeps its version's Score.
    """
    correct, judge, speed = totals.get("correct"), totals.get("judge"), current_speed(totals)
    if not isinstance(correct, (int, float)) or speed is None:
        return None
    return combined_score(float(correct), float(judge) if isinstance(judge, (int, float)) else None, speed)


def _config_cell(config: object) -> str:
    if not isinstance(config, dict):
        return "-"
    parts = []
    for key, value in config.items():
        if key == "personal_instructions":
            parts += [f"instructions={item}" for item in value] if isinstance(value, list) else []
            continue
        parts.append(f"{key}={value}")
    text = ", ".join(parts) or "-"
    return text if len(text) <= CONFIG_CELL_CHARS else text[:CONFIG_CELL_CHARS - 3] + "..."


def run_cost_text(result: dict[str, object]) -> str:
    """#162: the harness's exact cost, else the list-price estimate (`~$x`, `$0.00 (local)`), else n/a."""
    totals = result.get("totals")
    totals = totals if isinstance(totals, dict) else {}
    usd, estimate = totals.get("cost_usd"), price_text(result)
    if estimate == "$0.00 (local)":
        return estimate
    bound = ">= " if totals.get("cost_lower_bound") else ""
    # #202: opencode reports 0 for a model it has no price for; a declared --price is then the cost.
    harness_unpriced = usd == 0 and bool(result.get("price_per_mtok")) and estimate.startswith("~")
    if totals.get("cost_basis") == "harness" and isinstance(usd, (int, float)) and not harness_unpriced:
        return f"{bound}${usd:.2f}"
    return bound + estimate if estimate.startswith("~") else estimate


def bundle_tool_s(bundle: Path, result: dict[str, object]) -> float | None:
    """Median seconds per tool call: the run's own `tool_s_median`, else re-read from its transcripts."""
    totals = result.get("totals")
    stats = totals.get("stats") if isinstance(totals, dict) else None
    if isinstance(stats, dict) and "tool_s_median" in stats:
        value = stats["tool_s_median"]
        return float(value) if isinstance(value, (int, float)) else None
    calls: list[float] = []
    for transcript in sorted((bundle / "transcripts").glob("*.jsonl.gz")):
        for line in gzip.decompress(transcript.read_bytes()).decode("utf-8", errors="replace").splitlines():
            record = json.loads(line) if line.strip() else {}
            if record.get("stream") == "stdout":
                calls.extend(stream_stats(str(record.get("text") or "")).tool_call_s)
    return round(statistics.median(calls), 2) if calls else None


def _cells_line(cells: list[str]) -> str:
    return "| " + " | ".join(cell.replace("|", "/") for cell in cells) + " |"


def _row(rank: int, entry: RankedBundle) -> str:
    row = entry.result
    agent, totals = row["agent"], row["totals"]
    assert isinstance(agent, dict) and isinstance(totals, dict)
    harness = f"{agent['name']} {agent.get('version') or ''}".strip()
    setup = f"{agent['model']} {_fmt(agent.get('effort'))}<br>{harness}"
    return _cells_line([str(rank), f"**{_fmt(entry.score)}**", setup, str(row.get("date") or "-"),
                        _fmt(totals.get("correct")),
                        f"{totals.get('solved')}/{totals.get('total')}", _fmt(totals.get("judge")),
                        _fmt(entry.speed), time_text(totals.get("time_s")), run_cost_text(row),
                        _run_cell(entry)])


def _detail_row(rank: int, entry: RankedBundle) -> str:
    row = entry.result
    agent, totals = row["agent"], row["totals"]
    assert isinstance(agent, dict) and isinstance(totals, dict)
    stats = totals.get("stats") if isinstance(totals.get("stats"), dict) else {}
    assert isinstance(stats, dict)
    return _cells_line([str(rank), str(agent["model"]), _fmt(totals.get("timeouts")), tokens_text(totals.get("tokens")),
                        count_text(stats.get("generated_tokens")), count_text(stats.get("reasoning_tokens")),
                        _fmt(stats.get("model_turns")), _fmt(stats.get("tool_calls")),
                        "-" if entry.tool_s is None else f"{entry.tool_s:.1f}",
                        hardware_short_text(row.get("environment")), _config_cell(row.get("config")),
                        _fmt(row.get("submitter")), str(row.get("date"))])


def _run_cell(entry: RankedBundle) -> str:
    version = major_minor(entry.result.get("bench_version"))
    link = f"[run]({entry.summary_link})"
    marks = [] if version == major_minor(__version__) else [f"bench {version}"]
    judge = entry.result.get("judge")
    rubric = judge.get("rubric") if isinstance(judge, dict) else None
    if rubric is not None and str(rubric) != RUBRIC_VERSION:
        marks.append(f"rubric {rubric}")
    return link if not marks else f"{link} ({', '.join(marks)})"


def _header(columns: tuple[str, ...]) -> list[str]:
    return ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]


def _table(rows: Iterable[RankedBundle]) -> str:
    entries = list(rows)
    ranking = _header(COLUMNS) + [_row(rank, entry) for rank, entry in enumerate(entries, start=1)]
    details = _header(DETAIL_COLUMNS) + [_detail_row(rank, entry) for rank, entry in enumerate(entries, start=1)]
    # GitHub renders a table inside <details> only with a blank line after <summary>.
    return ("\n".join(ranking) + f"\n\n<details><summary>{DETAILS_SUMMARY}</summary>\n\n" + "\n".join(details)
            + "\n\n</details>\n")


def preset_key(result: dict[str, object]) -> tuple[str, str, str]:
    """#210: harness name, model and effort; the harness patch version and the run id are the same preset."""
    agent = result.get("agent")
    agent = agent if isinstance(agent, dict) else {}
    return str(agent.get("name")), str(agent.get("model")), str(agent.get("effort"))


def _recency(entry: RankedBundle) -> tuple[str, str]:
    return str(entry.result.get("date") or ""), str(entry.result.get("started_at") or "")


def split_older_runs(entries: list[RankedBundle]) -> tuple[list[RankedBundle], list[RankedBundle]]:
    """#210: (kept, older): each preset's RUNS_RANKED_PER_PRESET most recent runs, by date then started_at."""
    presets: dict[tuple[str, str, str], list[RankedBundle]] = {}
    for entry in entries:
        presets.setdefault(preset_key(entry.result), []).append(entry)
    older_ids = {id(entry) for runs in presets.values()
                 for entry in sorted(runs, key=_recency, reverse=True)[RUNS_RANKED_PER_PRESET:]}
    return ([entry for entry in entries if id(entry) not in older_ids],
            [entry for entry in entries if id(entry) in older_ids])


def _consistency(entries: list[RankedBundle]) -> str:
    """#210: Score min-max and mean of each preset with 2+ ranked runs, folded under the ranking; '' when none."""
    presets: dict[tuple[str, str, str], list[float]] = {}
    for entry in entries:
        if entry.score is not None:
            presets.setdefault(preset_key(entry.result), []).append(float(entry.score))
    lines = [_cells_line([f"{model} {effort}<br>{name}", str(len(scores)), f"{min(scores):.1f}-{max(scores):.1f}",
                          f"{statistics.mean(scores):.1f}"])
             for (name, model, effort), scores in presets.items() if len(scores) > 1]
    if not lines:
        return ""
    table = _header(("Setup", "Ranked runs", "Score min-max", "Score mean")) + sorted(lines)
    return f"<details><summary>{CONSISTENCY_SUMMARY}</summary>\n\n" + "\n".join(table) + "\n\n</details>\n"


def judged_runs(results_dir: Path, version: str) -> list[dict[str, object]]:
    """Complete runs of one bench major.minor that the official judge model voted on."""
    runs = []
    for result_file in sorted(results_dir.glob(f"*/{RESULT_NAME}")):
        result = json.loads(result_file.read_text(encoding="utf-8"))
        judge = result.get("judge")
        official = isinstance(judge, dict) and (judge.get("model"), judge.get("effort")) == (OFFICIAL_JUDGE_MODEL,
                                                                                             OFFICIAL_JUDGE_EFFORT)
        if major_minor(result.get("bench_version")) == version and is_complete_run(result) and official:
            runs.append(result)
    return runs


def build_leaderboard(results_dir: Path, link_base: Path) -> Leaderboard:
    ranked: list[RankedBundle] = []
    unranked: list[tuple[str, str]] = []
    history: dict[str, list[RankedBundle]] = {}
    observed: list[RankedBundle] = []
    observation_notes: dict[str, str] = dict(OBSERVED_RUNS)
    visual_runs: list[str] = []
    for result_file in sorted(results_dir.glob(f"*/{RESULT_NAME}")):
        bundle = result_file.parent
        links = [f"[{task}]({_link(bundle / 'workspace' / (task + '.tar.gz'), link_base)})"
                 for task in VISUAL_WORKSPACES if (bundle / 'workspace' / (task + '.tar.gz')).is_file()]
        if links:
            visual_runs.append(f"- [{bundle.name}]({_link(bundle / SUMMARY_NAME, link_base)}): " + ", ".join(links))
        result = json.loads(result_file.read_text(encoding="utf-8"))
        reason = unranked_reason(result)
        older = _history_version(result)
        totals = result.get("totals") if isinstance(result.get("totals"), dict) else {}
        score = totals.get("score") if older is not None else current_score(totals)
        speed = totals.get("speed") if older is not None else current_speed(totals)
        entry = RankedBundle(result=result, summary_link=_link(bundle / SUMMARY_NAME, link_base),
                             tool_s=bundle_tool_s(bundle, result), score=score, speed=speed)
        if infra_reason := _infra_reason(result):
            observation_notes[bundle.name] = infra_reason
        if bundle.name in observation_notes:
            observed.append(entry)
        elif older is not None:
            history.setdefault(older, []).append(entry)
        elif reason is not None:
            unranked.append((_link(bundle, link_base), reason))
        else:
            ranked.append(entry)
    ranked.sort(key=_by_score)
    ranked, older_runs = split_older_runs(ranked)
    note = [RANKED_WITH_NOTE] if RANKED_WITH_CURRENT.get(major_minor(__version__)) else []
    sections = [LEADERBOARD_HEADER, *note, _table(ranked) if ranked else "No results yet.\n", COST_LEGEND,
                *tie_note([entry.result for entry in ranked])]
    if consistency := _consistency(ranked):
        sections.append(consistency)
    if older_runs:
        sections.append(f"<details><summary>{OLDER_RUNS_SUMMARY}</summary>\n\n" + _table(older_runs) + "\n</details>\n")
    if observed:
        notes = "\n".join(f"- {Path(entry.summary_link).parent.name}: {observation_notes[Path(entry.summary_link).parent.name]}"
                          for entry in observed)
        sections.append("## Observations (not ranked)\n\n" + _table(sorted(observed, key=_by_score)) + "\n" + notes + "\n")
    for version in sorted(history, key=_version_key, reverse=True):
        sections.append(f"## Bench {version} (history)\n\n" + _table(sorted(history[version], key=_by_score)))
    if unranked:
        sections.append("## Not ranked\n\n" + "\n".join(f"- `{name}`: {reason}" for name, reason in unranked) + "\n")
    if visual_runs:
        sections.append("<details><summary>Download visual task workspaces</summary>\n\n"
                        "Each archive contains the final task workspace, including its inputs. "
                        "Older runs without a saved workspace have no download.\n\n"
                        + "\n".join(visual_runs) + "\n\n</details>\n")
    return Leaderboard(markdown="\n".join(sections), ranked=len(ranked), history=sum(map(len, history.values())),
                       unranked=unranked)
