"""Result bundles from a fake run, and LEADERBOARD.md from result.json files."""

from __future__ import annotations

import gzip
import json
import uuid
from pathlib import Path

import pytest

from conftest import FakeAgent
from fakes import MARKER, fake_secret
from mengine_bench import __version__, catalog, cli, leaderboard
from mengine_bench.core import scratch_root
from mengine_bench.judge import RUBRIC_VERSION
from mengine_bench.redact import LocalNames

TASK = "ds-ab-playtest"

# Applies the reference solution like a perfect agent, and leaks a planted
# secret on stderr so the transcript must be redacted before publishing.
REFERENCE_AGENT = """
import sys
from pathlib import Path
from mengine_bench import catalog
task = next(t for t in catalog.all_tasks() if t.id == "ds-ab-playtest")
answers = task.reference(Path(sys.argv[1]))
sys.stderr.write("debug: " + " ".join(sys.argv[3:]) + "\\n")
sys.stdout.buffer.write(answers[-1].encode("utf-8"))
"""


def test_bundle_holds_result_summary_and_redacted_transcripts(fake_agent: FakeAgent, tmp_path: Path,
                                                              monkeypatch: pytest.MonkeyPatch,
                                                              capsys: pytest.CaptureFixture[str]) -> None:
    # A key no pattern knows, only its env var name: the exact-value rule must catch it.
    env_secret = "envkey-" + uuid.uuid4().hex
    monkeypatch.setenv("FAKE_PROVIDER_API_KEY", env_secret)
    template = json.loads(fake_agent("reference", REFERENCE_AGENT))
    # -I would hide the installed package from the fake agent; drop it.
    template.remove("-I")
    template += [fake_secret("openai"), env_secret]
    out = tmp_path / "results"
    assert cli.main(["run", "--agent", "cmd", "--cmd", json.dumps(template), "--model", "fake/ref",
                     "--tasks", TASK, "--out", str(out), "--submitter", "Alice Example"]) == 0
    printed = capsys.readouterr().out
    assert "privacy check: clean" in printed and "removed raw run dir" in printed
    assert list((scratch_root() / "runs").iterdir()) == [], "the raw run dir holds unredacted transcripts"
    [bundle] = out.glob("*")
    assert bundle.name.split("_")[1:4] == ["cmd", "fake-ref", "none"]
    files = sorted(p.relative_to(bundle).as_posix() for p in bundle.rglob("*") if p.is_file())
    # #185: since 2.6 the bundle also keeps the task's final workspace for `regrade`.
    assert files == [f"judge/{TASK}.json", "result.json", "summary.md", f"transcripts/{TASK}.jsonl.gz",
                     f"workspace/{TASK}.tar.gz"]
    packet_text = (bundle / f"judge/{TASK}.json").read_text(encoding="utf-8")
    packet = json.loads(packet_text)
    assert set(packet) == {"task_id", "prompts", "answers", "diff", "transcript_tail", "checks", "deliverables",
                           "render", "status", "stats"}
    assert packet["status"] == "ok" and "turn_tps_median" not in packet["stats"]
    assert packet["diff"] and env_secret not in packet_text and str(tmp_path) not in packet_text
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    assert result["submitter"] == "Alice Example"
    assert result["started_at"].endswith("Z") and result["finished_at"] >= result["started_at"]
    assert set(result["bench_commit"]) == {"sha", "dirty"}
    [task] = result["tasks"]
    assert task["solved"] and task["transcript"] == f"transcripts/{TASK}.jsonl.gz"
    transcript = gzip.decompress((bundle / task["transcript"]).read_bytes()).decode("utf-8")
    assert MARKER not in transcript and "[REDACTED:" in transcript
    assert env_secret not in transcript and "[REDACTED:env]" in transcript
    assert str(tmp_path) not in transcript and str(tmp_path) not in json.dumps(result)
    assert result["config"] == {"personal_instructions": []} and result["judge"] is None


def test_earlier_runs_block_and_personal_instructions_are_recorded(fake_agent: FakeAgent, tmp_path: Path,
                                                                    monkeypatch: pytest.MonkeyPatch) -> None:
    template = json.loads(fake_agent("reference", REFERENCE_AGENT))
    template.remove("-I")
    argv = ["run", "--agent", "cmd", "--cmd", json.dumps(template), "--model", "fake/ref",
            "--tasks", TASK, "--out", str(tmp_path / "results")]
    monkeypatch.setattr(cli, "blocking_problems", lambda *args, **kwargs: ["earlier run left on disk: x"])
    with pytest.raises(SystemExit, match="1 earlier run"):
        cli.main(argv)
    assert not (tmp_path / "results").exists(), "a refused run launches nothing"
    with pytest.raises(SystemExit):
        cli.main([*argv, "--allow-unclean"])
    monkeypatch.setattr(cli, "blocking_problems", lambda *args, **kwargs: [])
    monkeypatch.setattr(cli, "personal_instructions", lambda *args, **kwargs: ["~/.claude/CLAUDE.md"])
    assert cli.main(argv) == 0
    [result_file] = (tmp_path / "results").glob("*/result.json")
    result = json.loads(result_file.read_text(encoding="utf-8"))
    assert result["config"]["personal_instructions"] == ["~/.claude/CLAUDE.md"]
    assert "preflight" not in result
    assert "personal_instructions=~/.claude/CLAUDE.md" in (result_file.parent / "summary.md").read_text(
        encoding="utf-8")


def test_privacy_check_fails_on_a_leak_and_names_only_file_and_kind(tmp_path: Path,
                                                                    capsys: pytest.CaptureFixture[str]) -> None:
    bundle = tmp_path / "bundle"
    (bundle / "transcripts").mkdir(parents=True)
    home = "C:" + "\\Users\\" + "dana"
    (bundle / "transcripts" / "t.jsonl.gz").write_bytes(gzip.compress(f"cwd {home}\\work".encode()))
    (bundle / "summary.md").write_text("clean\n", encoding="utf-8")
    assert cli._privacy_check(bundle, LocalNames()) == 1
    printed = capsys.readouterr().out
    assert "privacy check: transcripts/t.jsonl.gz: home path x1" in printed and home not in printed


def test_scoring_uses_the_recorded_rounded_agent_time() -> None:
    # Scoring on the unrounded time made the published total_agent_s differ
    # from the sum of the published task times at a 0.05 boundary.
    from mengine_bench.runner.task_run import StepRecord, TaskRunRecord
    task = next(t for t in catalog.all_tasks() if t.id == TASK)
    record = TaskRunRecord(task_id=TASK, steps=[StepRecord(0, 0.2549, 0, "ok")])
    from mengine_bench import run_command
    assert run_command._outcome(task, record).agent_s == 0.25


def _write_result(results: Path, name: str, score: float | None, *, model: str = "m", judged: bool = True,
                  task_ids: list[str] | None = None, bench_version: str = __version__, date: str = "2026-10-19",
                  harness_version: str = "codex-cli 0.162.1") -> Path:
    ids = task_ids if task_ids is not None else [task.id for task in catalog.all_tasks()]
    # #164 #210: the current table recomputes Score from Correct, Judge and Time; at 10 min (Speed 100) the formula
    # gives back `score` when Correct and Judge equal it, so a test sets one number and the ranking follows it.
    correct, judge, speed = (score, score, 100.0) if score is not None and judged else (80.0, 70.0 if judged else None, 0.0)
    result = {
        "date": date, "started_at": f"{date}T12:00:00Z", "bench_version": bench_version, "submitter": "dquill",
        "agent": {"name": "codex", "model": model, "effort": "high", "version": harness_version},
        "judge": {"agent": "claude", "model": "claude-opus-5-5", "effort": "xhigh", "rubric": leaderboard.RUBRIC_VERSION} if judged else None,
        "config": {"personal_instructions": [], "provider": "openai", "mcp": "none"},
        "environment": {"os": "Linux 6", "cpu": "AMD Ryzen 9 7950X", "cpu_count": 32, "ram_gb": 62.6,
                        "gpu": "NVIDIA GeForce RTX 4090 (24 GB)"},
        "totals": {"score": score, "correct": correct, "solved": 10, "total": len(ids), "judge": judge,
                   "speed": speed, "time_s": 600.0 if speed else 1830.0, "cost_usd": 2.5, "cost_basis": "price", "cost_lower_bound": True,
                   "tokens": {"input": 1_500_000, "cached_input": 0, "output": 250_000, "reasoning": 0},
                   "timeouts": 1, "stats": {"generated_tokens": 3400, "model_turns": 12}},
        "tasks": [{"id": task_id} for task_id in ids],
    }
    bundle = results / name
    bundle.mkdir(parents=True)
    (bundle / "result.json").write_text(json.dumps(result), encoding="utf-8")
    return bundle


def test_leaderboard_ranks_in_a_narrow_table_and_keeps_the_stats_in_details(tmp_path: Path) -> None:
    # #193: the 23-column table broke even on a 2k laptop screen; the ranking fits, the run stats fold below it.
    results = tmp_path / "results"
    _write_result(results, "low", 50.0, model="low-model")
    _write_result(results, "high", 90.0, model="high-model")
    board = leaderboard.build_leaderboard(results, tmp_path)
    assert board.ranked == 2 and board.unranked == []
    table = board.markdown[board.markdown.index("| # |"):]
    assert table.splitlines()[0] == ("| # | Score | Setup | Date | Correct % | Solved | Judge | Speed | Time | Cost | "
                                      "Run |")
    assert table.index("high-model") < table.index("low-model")
    row = table.splitlines()[2]
    for cell in ("| 1 | **90.0** | high-model high<br>codex codex-cli 0.162.1 | 2026-10-19 | 90.0 | 10/",
                 "| 90.0 | 100.0 | 10 min 00 s | n/a | [run](results/high/summary.md) |"):
        assert cell in row, (cell, row)
    details = board.markdown[board.markdown.index("<details>"):board.markdown.index("</details>")]
    assert details.count("| # |") == 1
    assert ("| # | Model | Timeouts | Tokens | Generated | Thinking | Turns | Tools | Tool s | Hardware | Config | "
            "Submitter | Date |") in details
    detail_row = next(line for line in details.splitlines() if line.startswith("| 1 |"))
    for cell in ("| 1 | high-model | 1 | 1.75M | 3.4k | - | 12 | - | - |",
                 "AMD Ryzen 9 7950X, NVIDIA GeForce RTX 4090 (24 GB)", "| provider=openai, mcp=none | dquill | 2026-10-19 |"):
        assert cell in detail_row, (cell, detail_row)
    assert board.markdown.count("| # | Score |") == 1, "one ranking table"


@pytest.mark.parametrize("task_ids", [[TASK], [TASK, TASK]], ids=["subset", "duplicate"])
def test_leaderboard_lists_incomplete_runs_apart(tmp_path: Path, task_ids: list[str]) -> None:
    results = tmp_path / "results"
    _write_result(results, "part", 99.0, task_ids=task_ids)
    target = tmp_path / "LEADERBOARD.md"
    assert cli.main(["leaderboard", "--results", str(results), "--output", str(target)]) == 0
    text = target.read_text(encoding="utf-8")
    assert "| 1 | " not in text and "No results yet." in text
    assert "- `results/part`: incomplete" in text[text.index("## Not ranked"):]


def test_leaderboard_lists_runs_waiting_for_the_judge_apart(tmp_path: Path) -> None:
    results = tmp_path / "results"
    _write_result(results, "pending", None, judged=False)
    board = leaderboard.build_leaderboard(results, tmp_path)
    assert board.ranked == 0
    assert board.unranked == [("results/pending", "waiting for the judge (`mengine-bench judge`)")]


def test_leaderboard_ranks_the_current_major_minor_only(tmp_path: Path) -> None:
    # A patch release changes no task, prompt or score, so 1.0.x runs compare; 0.2 runs do not.
    results = tmp_path / "results"
    _write_result(results, "old", 99.0, bench_version="0.2.0")
    major, minor, _ = __version__.split(".")
    _write_result(results, "patch", 60.0, bench_version=f"{major}.{minor}.99")
    _write_result(results, "current", 50.0)
    board = leaderboard.build_leaderboard(results, tmp_path)
    assert board.ranked == 2 and board.history == 1 and board.unranked == []


def test_2_3_to_2_7_runs_stay_ranked_in_2_8_and_2_0_to_2_2_are_history_187_210_218(tmp_path: Path) -> None:
    # #139, #151, #153, #161, #164: the owner kept every 2.x run ranked and marked. #187 (owner, 2026-11-04): one
    # catalog per ranking; the 20- and 23-task rows (2.0 to 2.2) are history, the 28-task rows (2.3 on) stay, marked.
    # #210: 2.7 changes only the Score formula, so the 2.6 rows stay ranked too. #218 (owner, 2026-11-07): 2.8 adds
    # web-archery-game and the ranking stays alive: the 28-task 2.7 rows stay ranked, marked, without that task.
    # The archery module sorts first in the catalog: the 2.0 to 2.2 fixtures never had it, as the real runs.
    added = leaderboard.TASKS_ADDED_IN_2_2 | leaderboard.TASKS_ADDED_IN_2_3 | leaderboard.TASKS_ADDED_IN_2_8
    old_ids = [task.id for task in catalog.all_tasks() if task.id not in added]
    v22_ids = [task.id for task in catalog.all_tasks()
               if task.id not in leaderboard.TASKS_ADDED_IN_2_3 | leaderboard.TASKS_ADDED_IN_2_8]
    results = tmp_path / "results"
    _write_result(results, "v20", 90.0, model="v20-model", bench_version="2.0.0", task_ids=old_ids)
    _write_result(results, "v21", 85.0, model="v21-model", bench_version="2.1.1", task_ids=old_ids)
    _write_result(results, "v22", 80.0, model="v22-model", bench_version="2.2.0", task_ids=v22_ids)
    _write_result(results, "v23", 75.0, model="v23-model", bench_version="2.3.1")
    _write_result(results, "v24", 70.0, model="v24-model", bench_version="2.4.0")
    _write_result(results, "v25", 65.0, model="v25-model", bench_version="2.5.2")
    _write_result(results, "v26", 60.0, model="v26-model", bench_version="2.6.1")
    v27_ids = [task.id for task in catalog.all_tasks() if task.id not in leaderboard.TASKS_ADDED_IN_2_8]
    _write_result(results, "v27", 55.0, model="v27-model", bench_version="2.7.0", task_ids=v27_ids)
    _write_result(results, "v28", 50.0, model="v28-model")
    _write_result(results, "v21-short", 99.0, model="short-model", bench_version="2.1.1", task_ids=old_ids[1:])
    _write_result(results, "v17", 99.0, model="v17-model", bench_version="1.7.3", task_ids=[TASK])
    board = leaderboard.build_leaderboard(results, tmp_path)
    assert board.ranked == 6 and board.history == 3
    text = board.markdown
    assert "Bench 2.3 to 2.7 runs stay in this ranking (#153, #161, #164, #185, #187, #210, #218)" in text
    assert "The bench 2.0 to 2.2 runs (20 and 23 tasks) moved to history" in " ".join(text.split())
    order = [text.index(mark) for mark in ("v23-model", "v24-model", "v25-model", "v26-model", "v27-model", "v28-model",
                                           "## Bench 2.2 (history)",
                                           "v22-model", "## Bench 2.1 (history)", "v21-model", "## Bench 2.0 (history)",
                                           "v20-model", "## Not ranked")]
    assert order == sorted(order)
    assert "[run](results/v23/summary.md) (bench 2.3) |" in text
    assert "[run](results/v24/summary.md) (bench 2.4) |" in text
    assert "[run](results/v25/summary.md) (bench 2.5) |" in text
    assert "[run](results/v26/summary.md) (bench 2.6) |" in text
    assert "[run](results/v27/summary.md) (bench 2.7) |" in text
    assert "[run](results/v28/summary.md) |" in text
    assert text.index("[run](results/v20/summary.md) (bench 2.0) |") > text.index("## Bench 2.0 (history)")
    assert [name for name, _ in board.unranked] == ["results/v17", "results/v21-short"]


def test_an_observed_run_is_shown_with_its_reason_and_never_ranked_146(tmp_path: Path,
                                                                     monkeypatch: pytest.MonkeyPatch) -> None:
    # #146: a run the owner keeps on the board, outside the ranking, with why.
    monkeypatch.setattr(leaderboard, "OBSERVED_RUNS", {"stalled": "the model never replied on 3 tasks"})
    results = tmp_path / "results"
    _write_result(results, "stalled", 99.0, model="stalled-model")
    _write_result(results, "current", 50.0, model="current-model")
    board = leaderboard.build_leaderboard(results, tmp_path)
    assert board.ranked == 1 and board.unranked == []
    text = board.markdown
    observed = text[text.index("## Observations (not ranked)"):]
    assert "stalled-model" in observed and "- stalled: the model never replied on 3 tasks" in observed
    assert text.index("current-model") < text.index("## Observations (not ranked)")


def test_an_older_ranking_stays_on_the_board_as_history(tmp_path: Path) -> None:
    # #41: the owner keeps the previous version's ranking; its Scores use that version's formula.
    results = tmp_path / "results"
    _write_result(results, "old-low", 40.0, model="old-low-model", bench_version="0.2.0")
    _write_result(results, "old-high", 99.0, model="old-high-model", bench_version="0.2.1")
    _write_result(results, "older", 70.0, model="older-model", bench_version="0.1.0")
    _write_result(results, "old-pending", None, judged=False, bench_version="0.2.0")
    _write_result(results, "current", 50.0, model="current-model")
    board = leaderboard.build_leaderboard(results, tmp_path)
    assert (board.ranked, board.history) == (1, 3)
    text = board.markdown
    order = [text.index(mark) for mark in ("current-model", "## Bench 0.2 (history)", "old-high-model", "old-low-model",
                                           "## Bench 0.1 (history)", "older-model", "## Not ranked")]
    assert order == sorted(order)
    assert [name for name, _ in board.unranked] == ["results/old-pending"]


def test_the_current_table_recomputes_score_with_todays_weights_and_history_keeps_its_own_164(tmp_path: Path) -> None:
    # #164: 2.5 moved 0.1 from Correct to Judge; a stored Score from older weights must not rank a current run.
    results = tmp_path / "results"
    current = _write_result(results, "current", 60.0, model="current-model")
    stale = json.loads((current / "result.json").read_text(encoding="utf-8"))
    stale["totals"]["score"] = 99.0
    (current / "result.json").write_text(json.dumps(stale), encoding="utf-8")
    _write_result(results, "rival", 70.0, model="rival-model")
    _write_result(results, "old", 41.0, model="old-model", bench_version="0.2.0")
    board = leaderboard.build_leaderboard(results, tmp_path)
    text = board.markdown
    assert "| 1 | **70.0** |" in text and "| 2 | **60.0** |" in text, text
    assert "**99.0**" not in text
    assert "**41.0**" in text[text.index("## Bench 0.2 (history)"):]
    assert leaderboard.current_score({"correct": 53.3, "judge": 56.7, "speed": 32.0, "time_s": 1320.0}) == 51.3
    assert leaderboard.current_score({"correct": 80.0, "judge": None, "speed": 0.0, "time_s": 600.0}) is None


def test_ranked_rows_are_rescored_with_the_2_7_formula_from_published_time_and_history_keeps_its_own_210(
        tmp_path: Path) -> None:
    # #210: weights 0.5/0.35/0.15 and Speed 100 at 10 min, 0 at 40 min. Stored 2.6 Speed and Score came from the
    # 5/30 min line and 0.25 weights; the ranking recomputes both from Correct, Judge and Time, edits no bundle.
    results = tmp_path / "results"
    published = {"v26": ("2.6.1", 97.3, 78.0, 780.0, 74.0, 86.2), "v27": ("2.7.0", 99.2, 83.4, 1140.0, 44.0, 82.5),
                 "v22": ("2.2.0", 90.0, 70.0, 900.0, 60.0, 41.0)}
    added = leaderboard.TASKS_ADDED_IN_2_3
    for name, (version, correct, judge, time_s, speed, score) in published.items():
        ids = [task.id for task in catalog.all_tasks() if version != "2.2.0" or task.id not in added]
        bundle = _write_result(results, name, score, model=f"{name}-model", bench_version=version, task_ids=ids)
        result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
        result["totals"].update(correct=correct, judge=judge, time_s=time_s, speed=speed, score=score)
        (bundle / "result.json").write_text(json.dumps(result), encoding="utf-8")
    text = leaderboard.build_leaderboard(results, tmp_path).markdown
    rows = [line for line in text.splitlines() if line.startswith("| 1 |") or line.startswith("| 2 |")]
    assert rows[0].startswith("| 1 | **89.2** | v27-model") and "| 99.2 | " in rows[0] and "| 83.4 | 70.0 | 19 min 00 s |" in rows[0]
    assert rows[1].startswith("| 2 | **89.1** | v26-model") and "| 78.0 | 90.0 | 13 min 00 s |" in rows[1]
    assert "(bench 2.6)" in rows[1]
    history = text[text.index("## Bench 2.2 (history)"):]
    assert "| 1 | **41.0** | v22-model" in history and "| 70.0 | 60.0 | 15 min 00 s |" in history
    flat = " ".join(text.split())
    assert "0.5 x Correct % + 0.35 x Judge + 0.15 x Speed x Correct % / 100" in flat
    assert "Speed 100 at 10 min of Time or less, 0 at 40 min or more" in flat
    assert "every Score and Speed here use the 2.7 formula (#210), recomputed from the row's published Correct %, Judge and Time" in flat
    stored = json.loads((results / "v26" / "result.json").read_text(encoding="utf-8"))["totals"]
    assert (stored["speed"], stored["score"]) == (74.0, 86.2), "the leaderboard never edits a bundle"


def test_bench_is_version_2_8_0() -> None:
    import tomllib
    pyproject = tomllib.loads((Path(__file__).resolve().parents[1] / "pyproject.toml").read_text(encoding="utf-8"))
    assert __version__ == pyproject["project"]["version"] == "2.8.0"


def test_leaderboard_ranks_only_the_official_judge(tmp_path: Path) -> None:
    # Judge scores from different judges do not compare (#23): a run judged by
    # anything but claude-opus-5-5 at xhigh is listed apart.
    results = tmp_path / "results"
    bundle = _write_result(results, "cheap-judge", 88.0)
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    result["judge"]["model"] = "claude-haiku-5-5"
    (bundle / "result.json").write_text(json.dumps(result), encoding="utf-8")
    board = leaderboard.build_leaderboard(results, tmp_path)
    assert board.ranked == 0
    assert board.unranked == [("results/cheap-judge",
                               f"judged by claude claude-haiku-5-5@xhigh rubric {leaderboard.RUBRIC_VERSION}; only claude "
                               f"claude-opus-5-5@xhigh rubric {', '.join(sorted(leaderboard.ranked_rubrics()))} judges are ranked")]


@pytest.mark.parametrize("field,value", [("agent", "cmd"), ("rubric", "1.0")])
def test_leaderboard_ranks_only_the_claude_adapter_and_current_rubric(tmp_path: Path, field: str,
                                                                      value: str) -> None:
    # `judge --judge cmd` keeps the default model and effort labels (#23 review):
    # the adapter and rubric must match too.
    results = tmp_path / "results"
    bundle = _write_result(results, "custom", 88.0)
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    result["judge"][field] = value
    (bundle / "result.json").write_text(json.dumps(result), encoding="utf-8")
    board = leaderboard.build_leaderboard(results, tmp_path)
    assert board.ranked == 0 and "only claude claude-opus-5-5@xhigh" in board.unranked[0][1]


def test_a_complete_1_7_run_stays_complete_in_2_0() -> None:
    # #124: the 1.7 catalog had lc-changelog, vis-chart, ir-studio-wiki and 3d-voxel-landscape and none of the new eight;
    # without this, every older ranking vanished from the history when 2.0 shipped.
    from mengine_bench.leaderboard import is_complete_run

    ids_1_7 = ["ds-ab-playtest", "bo-pnl-runway", "bo-reconcile", "cmp-handoff", "lc-changelog", "vis-chart", "ds-sql-funnel",
               "ue-packaged-bug", "ir-studio-wiki", "ir-server-logs", "gd-integration-repo", "rs-lock-bug",
               "web-mondrian-landing", "3d-voxel-landscape", "web-word-universe"]
    assert is_complete_run({"bench_version": "1.7.3", "tasks": [{"id": task_id} for task_id in ids_1_7]})
    assert not is_complete_run({"bench_version": "1.7.3", "tasks": [{"id": task_id} for task_id in ids_1_7[1:]]})


@pytest.mark.parametrize(("totals", "price", "model", "expected"), [
    ({"cost_usd": 3.19, "cost_basis": "harness"}, None, "m", "$3.19"),
    ({"cost_usd": 3.19, "cost_basis": "harness", "cost_lower_bound": True}, None, "m", ">= $3.19"),
    ({"cost_usd": None, "cost_basis": None}, None, "claude-sonnet-5-5", "~$5.40"),
    ({"cost_usd": None, "cost_basis": None, "cost_lower_bound": True}, None, "claude-sonnet-5-5", ">= ~$5.40"),
    ({"cost_usd": 0.0, "cost_basis": "price"}, {"input": 0, "cached": 0, "output": 0}, "local-27b", "$0.00 (local)"),
    ({"cost_usd": None, "cost_basis": None}, None, "unpriced-model", "n/a"),
    # #202: opencode reports 0 for a model it has no price for; the declared --price is the cost then.
    ({"cost_usd": 0.0, "cost_basis": "harness", "cost_lower_bound": True}, {"input": 0.091, "cached": 0.0091, "output": 0.4551},
     "maritaca/S5", ">= ~$0.15"),
], ids=["exact", "exact-bound", "estimate", "estimate-bound", "local", "neither", "harness-zero-declared-price"])
def test_one_cost_cell_is_exact_estimated_local_or_na_162(totals: dict[str, object], price: object, model: str,
                                                        expected: str) -> None:
    result = {"agent": {"model": model}, "price_per_mtok": price, "config": {},
              "totals": {**totals, "tokens": {"input": 1_000_000, "cached_input": 0, "output": 140_000}}}
    assert leaderboard.run_cost_text(result) == expected


def _claude_tool_stream() -> str:
    events = [
        {"type": "assistant", "timestamp": "2026-11-03T13:43:00.000Z",
         "message": {"id": "a", "content": [{"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "ls"}}]}},
        {"type": "user", "timestamp": "2026-11-03T13:43:01.500Z",
         "message": {"content": [{"type": "tool_result", "tool_use_id": "t1"}]}},
        {"type": "assistant", "timestamp": "2026-11-03T13:43:02.000Z",
         "message": {"id": "b", "content": [{"type": "tool_use", "id": "t2", "name": "Read", "input": {"path": "x"}}]}},
        {"type": "user", "timestamp": "2026-11-03T13:43:06.000Z",
         "message": {"content": [{"type": "tool_result", "tool_use_id": "t2"}]}},
        {"type": "assistant", "timestamp": "2026-11-03T13:43:07.000Z",
         "message": {"id": "c", "content": [{"type": "tool_use", "id": "t3", "name": "Read", "input": {"path": "y"}}]}},
        {"type": "user", "timestamp": "2026-11-03T13:43:09.500Z",
         "message": {"content": [{"type": "tool_result", "tool_use_id": "t3"}]}},
    ]
    return "\n".join(json.dumps(event) for event in events) + "\n"


def test_tool_seconds_come_from_the_bundle_transcripts_or_stay_a_dash_162(tmp_path: Path) -> None:
    import gzip

    results = tmp_path / "results"
    timed = _write_result(results, "timed", 90.0, model="timed-model")
    (timed / "transcripts").mkdir()
    lines = [json.dumps({"step": "0", "stream": "stdout", "text": _claude_tool_stream()}),
             json.dumps({"step": "0", "stream": "stderr", "text": ""})]
    (timed / "transcripts" / "t.jsonl.gz").write_bytes(gzip.compress(("\n".join(lines) + "\n").encode("utf-8")))
    untimed = _write_result(results, "untimed", 80.0, model="untimed-model")
    (untimed / "transcripts").mkdir()
    no_stamps = _claude_tool_stream().replace('"timestamp"', '"stamp"')
    (untimed / "transcripts" / "t.jsonl.gz").write_bytes(gzip.compress(
        (json.dumps({"step": "0", "stream": "stdout", "text": no_stamps}) + "\n").encode("utf-8")))
    markdown = leaderboard.build_leaderboard(results, tmp_path).markdown
    details = markdown[markdown.index("<details>"):]
    rows = {line.split(" | ")[1]: line for line in details.splitlines()
            if line.startswith("| 1 |") or line.startswith("| 2 |")}
    # Median of 1.5, 4.0 and 2.5 s; a stream without stamps has no per-call time, never an estimate.
    assert set(rows) == {"timed-model", "untimed-model"}
    assert " | 12 | - | 2.5 | " in rows["timed-model"] and " | 12 | - | - | " in rows["untimed-model"]


def test_the_summary_has_thinking_tools_and_tool_seconds_per_task_162() -> None:
    from mengine_bench.report import render_summary
    stats = {"model_turns": 4, "tool_calls": 9, "tool_s_median": 1.25, "generated_tokens": 3000, "reasoning_tokens": 1200}
    summary = render_summary({"bench_version": "2.4.0", "date": "d", "agent": {"name": "a", "model": "m"},
                              "totals": {"score": 1.0, "correct": 1.0, "solved": 1, "total": 2, "judge": 1.0, "time_s": 1.0},
                              "tasks": [{"id": "timed", "status": "ok", "flags": [], "c": 1.0, "agent_s": 1.0, "checks": [],
                                         "stats": stats},
                                        {"id": "untimed", "status": "ok", "flags": [], "c": 1.0, "agent_s": 1.0,
                                         "checks": [], "stats": {**stats, "tool_s_median": None}}]})
    assert "| turns | tools | tool s | generated | thinking | first write |" in summary
    assert "| 4 | 9 | 1.2 | 3.0k | 1.2k | - |" in summary and "| 4 | 9 | - | 3.0k | 1.2k | - |" in summary


def test_infra_run_is_an_observation(tmp_path: Path) -> None:
    results = tmp_path / "results"
    bundle = _write_result(results, "infra", 99.0)
    path = bundle / "result.json"
    result = json.loads(path.read_text())
    signature = "only files this session is allowed to read can be uploaded"
    result["tasks"][0].update(status="infra", flags=[f"infra fault: {signature}; rerun that task"])
    path.write_text(json.dumps(result))
    reason = f"infra fault on {result['tasks'][0]['id']}: {signature}; rerun that task"
    assert leaderboard.unranked_reason(result) == reason
    board = leaderboard.build_leaderboard(results, tmp_path)
    assert board.ranked == 0 and "## Observations (not ranked)" in board.markdown
    assert reason in board.markdown


def test_a_run_judged_with_the_kept_older_rubric_is_ranked_and_marked(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # #185: a rubric bump no longer empties the ranking; the older rubric's votes stay ranked, marked on the row.
    results = tmp_path / "results"
    older = leaderboard.RUBRIC_VERSION
    _write_result(results, "kept", 88.0)  # judged with the rubric current at write time
    monkeypatch.setattr(leaderboard, "RUBRIC_VERSION", "9.9")
    monkeypatch.setattr(leaderboard, "RANKED_RUBRICS", {"9.9": frozenset({older})})
    board = leaderboard.build_leaderboard(results, tmp_path)
    assert board.ranked == 1 and board.unranked == []
    assert f"(rubric {older})" in board.markdown
    monkeypatch.setattr(leaderboard, "RANKED_RUBRICS", {})
    board = leaderboard.build_leaderboard(results, tmp_path)
    assert board.ranked == 0
    assert board.unranked[0][1].endswith("; only claude claude-opus-5-5@xhigh rubric 9.9 judges are ranked")


def test_a_preset_keeps_its_3_latest_runs_ranked_and_older_ones_fold_below_210(tmp_path: Path) -> None:
    # #210 (owner, 2026-11-06): one setup rerun many times crowded the ranking. A preset (harness name, model, effort;
    # not the harness patch or run id) keeps its 3 most recent runs ranked; older ones stay visible, folded below.
    results = tmp_path / "results"
    for name, score, date, harness in (("a", 90.0, "2026-10-01", "codex-cli 0.160.0"), ("b", 80.0, "2026-10-02", "codex-cli 0.161.0"),
                                       ("c", 70.0, "2026-10-03", "codex-cli 0.162.1"), ("d", 60.0, "2026-10-04", "codex-cli 0.162.1")):
        _write_result(results, name, score, model="same-model", date=date, harness_version=harness)
    _write_result(results, "other", 75.0, model="other-model", date="2026-10-05")
    board = leaderboard.build_leaderboard(results, tmp_path)
    text = board.markdown
    ranking = text[text.index("| # | Score |"):text.index("<details>")]
    assert board.ranked == 4 and "**90.0**" not in ranking, ranking
    assert [line.split(" | ")[1] for line in ranking.splitlines()[2:6]] == ["**80.0**", "**75.0**", "**70.0**", "**60.0**"]
    assert "| 1 | **80.0** | same-model high<br>codex codex-cli 0.161.0 | 2026-10-02 | 80.0 |" in ranking
    older = text[text.index("Older runs of ranked setups"):]
    assert text.index("Older runs of ranked setups") > text.index("| 4 | **60.0** |")
    assert "| 1 | **90.0** | same-model high<br>codex codex-cli 0.160.0 | 2026-10-01 | 90.0 |" in older
    consistency = text[text.index("| Setup | Ranked runs | Score min-max | Score mean |"):]
    assert "| same-model high<br>codex | 3 | 60.0-80.0 | 70.0 |" in consistency
    assert "other-model" not in consistency.split("</details>")[0], "one run shows no consistency"


def test_leaderboard_links_available_visual_workspaces_for_all_runs(tmp_path: Path) -> None:
    results = tmp_path / "results"
    ranked = _write_result(results, "ranked", 90.0)
    partial = _write_result(results, "partial", 80.0, task_ids=["web-archery-game"])
    for bundle, names in [(ranked, ["web-mondrian-landing", "3d-print-homage", "file-media-edit"]),
                          (partial, ["web-archery-game"])]:
        folder = bundle / "workspace"
        folder.mkdir()
        for name in names:
            (folder / f"{name}.tar.gz").write_bytes(b"fixture")
    board = leaderboard.build_leaderboard(results, tmp_path).markdown
    for name in ("web-mondrian-landing", "3d-print-homage", "file-media-edit"):
        assert f"[{name}](results/ranked/workspace/{name}.tar.gz)" in board
    assert "[web-archery-game](results/partial/workspace/web-archery-game.tar.gz)" in board
    assert "results/ranked/workspace/web-archery-game.tar.gz" not in board
    assert "results/partial/workspace/web-mondrian-landing.tar.gz" not in board
