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
    assert files == [f"judge/{TASK}.json", "result.json", "summary.md", f"transcripts/{TASK}.jsonl.gz"]
    packet_text = (bundle / f"judge/{TASK}.json").read_text(encoding="utf-8")
    packet = json.loads(packet_text)
    assert set(packet) == {"task_id", "prompts", "answers", "diff", "transcript_tail", "checks", "deliverables",
                           "render"}
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
                  task_ids: list[str] | None = None, bench_version: str = __version__) -> Path:
    ids = task_ids if task_ids is not None else [task.id for task in catalog.all_tasks()]
    result = {
        "date": "2026-10-19", "bench_version": bench_version, "submitter": "dquill",
        "agent": {"name": "codex", "model": model, "effort": "high", "version": "codex-cli 0.162.1"},
        "judge": {"agent": "claude", "model": "claude-opus-5-5", "effort": "xhigh", "rubric": "2.0"} if judged else None,
        "config": {"personal_instructions": [], "provider": "openai", "mcp": "none"},
        "environment": {"os": "Linux 6", "cpu": "AMD Ryzen 9 7950X", "cpu_count": 32, "ram_gb": 62.6,
                        "gpu": "NVIDIA GeForce RTX 4090 (24 GB)"},
        "totals": {"score": score, "correct": 80.0, "solved": 10, "total": len(ids), "judge": 70.0 if judged else None,
                   "time_s": 1830.0, "cost_usd": 2.5, "cost_basis": "price", "cost_lower_bound": True,
                   "tokens": {"input": 1_500_000, "cached_input": 0, "output": 250_000, "reasoning": 0}},
        "tasks": [{"id": task_id} for task_id in ids],
    }
    bundle = results / name
    bundle.mkdir(parents=True)
    (bundle / "result.json").write_text(json.dumps(result), encoding="utf-8")
    return bundle


def test_leaderboard_is_one_table_sorted_by_score_with_the_spec_columns(tmp_path: Path) -> None:
    results = tmp_path / "results"
    _write_result(results, "low", 50.0, model="low-model")
    _write_result(results, "high", 90.0, model="high-model")
    board = leaderboard.build_leaderboard(results, tmp_path)
    assert board.ranked == 2 and board.unranked == []
    table = board.markdown[board.markdown.index("| # |"):]
    header = table.splitlines()[0]
    assert header == ("| # | Score | Correct % | Solved | Judge | Time | Cost | Tokens | Agent | Model | Effort | "
                      "Hardware | Config | Submitter | Date | Run |")
    assert table.index("high-model") < table.index("low-model")
    row = table.splitlines()[2]
    for cell in ("| 1 | **90.0** | 80.0 | 10/", "| 70.0 | 30 min 30 s | >= $2.50 (price) | 1.75M |",
                 "| codex codex-cli 0.162.1 | high-model | high |", "AMD Ryzen 9 7950X, NVIDIA GeForce RTX 4090 (24 GB)",
                 "provider=openai, mcp=none", "| dquill | 2026-10-19 | [run](results/high/summary.md) |"):
        assert cell in row, (cell, row)
    assert board.markdown.count("| # |") == 1, "one table"


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
    assert board.ranked == 2
    assert board.unranked == [("results/old", f"older bench 0.2.0; only bench {major}.{minor}.x runs are ranked")]


def test_bench_is_version_1_0_0() -> None:
    import tomllib
    pyproject = tomllib.loads((Path(__file__).resolve().parents[1] / "pyproject.toml").read_text(encoding="utf-8"))
    assert __version__ == pyproject["project"]["version"] == "1.0.0"


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
                               "judged by claude claude-haiku-5-5@xhigh rubric 2.0; only claude claude-opus-5-5@xhigh rubric 2.0 judges are ranked")]


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
