"""`mengine-bench analyze` and the tie note: what separates runs, read from published results (#82)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench import __version__, analyze, catalog, cli, leaderboard
from test_bundle_leaderboard import _write_result

IDS = [task.id for task in catalog.all_tasks()]


def _run(model: str, seconds: float = 30.0, judge: int = 80, correct: dict[str, float] | None = None) -> dict[str, object]:
    tasks = [{"id": task_id, "c": (correct or {}).get(task_id, 1.0), "solved": True, "judge": judge,
              "agent_s": seconds, "status": "ok"} for task_id in IDS]
    mean_c = sum(task["c"] for task in tasks) / len(tasks)
    return {"agent": {"model": model, "effort": "low"}, "tasks": tasks,
            "totals": {"correct": 100 * mean_c, "judge": float(judge), "speed": 50.0, "score": 100 * mean_c,
                       "time_s": seconds * len(IDS)}}


def test_identical_runs_are_a_coin_flip_and_a_better_run_always_wins() -> None:
    same = analyze.task_points(_run("a"))
    assert analyze.win_share(same, same) == 0.5
    better, worse = analyze.task_points(_run("a", judge=90)), analyze.task_points(_run("b", judge=60))
    assert analyze.win_share(better, worse) == 1.0


def test_win_share_is_the_same_on_every_call() -> None:
    uneven = analyze.task_points(_run("a", correct={"ds-sql-funnel": 0.0}))
    even = analyze.task_points(_run("b", seconds=45.0))
    assert analyze.win_share(uneven, even) == analyze.win_share(uneven, even)


def test_a_lead_that_rests_on_one_task_is_a_tie() -> None:
    one_task = _run("a", judge=80)
    one_task["tasks"][0]["judge"] = 100
    share = analyze.win_share(analyze.task_points(one_task), analyze.task_points(_run("b", judge=81)))
    assert 0.5 < share < analyze.TIE_BELOW


def test_the_report_names_the_tasks_that_separate_runs_and_the_points_of_each_part() -> None:
    report = analyze.render_analysis([_run("fast", seconds=30.0, judge=90),
                                      _run("slow", seconds=60.0, judge=70, correct={"ds-sql-funnel": 0.33})], "1.4")
    assert "2 judged runs" in report
    assert "| ds-sql-funnel | 0.33 | 0.67 | yes |" in report
    assert "| gd-astar-doors | 1.00 | 1.00 | no |" in report
    assert "| fast/low | slow/low |" in report


def test_a_timeout_shows_on_its_task() -> None:
    timed = _run("a")
    next(task for task in timed["tasks"] if task["id"] == "3d-voxel-landscape")["status"] = "timeout"
    row = next(line for line in analyze.render_analysis([timed], "1.4").splitlines() if "3d-voxel-landscape" in line)
    assert row.endswith("| 1 |")


def _with_tasks(results: Path, name: str, score: float, run: dict[str, object]) -> None:
    bundle = _write_result(results, name, score)
    stored = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    stored["tasks"] = run["tasks"]
    (bundle / "result.json").write_text(json.dumps(stored), encoding="utf-8")


def test_the_board_calls_a_tie_from_the_resamples_not_from_a_fixed_gap(tmp_path: Path) -> None:
    results = tmp_path / "results"
    _with_tasks(results, "a", 95.7, _run("a", judge=95))
    _with_tasks(results, "b", 95.6, _run("b", judge=95))
    _with_tasks(results, "c", 60.0, _run("c", judge=40))
    board = leaderboard.build_leaderboard(results, tmp_path).markdown
    assert "#1 and #2 (50%)" in board and "#2 and #3" not in board
    assert "within 1 point" not in board


def test_runs_without_task_data_get_no_tie_note(tmp_path: Path) -> None:
    results = tmp_path / "results"
    _write_result(results, "a", 95.7)
    _write_result(results, "b", 95.1)
    assert "tie" not in leaderboard.build_leaderboard(results, tmp_path).markdown


def test_the_command_reads_one_version_and_says_when_it_has_no_runs(tmp_path: Path,
                                                                    capsys: pytest.CaptureFixture[str]) -> None:
    results = tmp_path / "results"
    _with_tasks(results, "a", 90.0, _run("a"))
    assert cli.main(["analyze", "--results", str(results)]) == 0
    assert "1 judged runs" in capsys.readouterr().out
    assert cli.main(["analyze", "--results", str(results), "--version", "0.1"]) == 1
    out = capsys.readouterr().out
    assert "received no judged runs of bench 0.1" in out and leaderboard.major_minor(__version__) in out
