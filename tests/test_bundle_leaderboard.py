"""Result bundles from a fake run, and LEADERBOARD.md from result.json files."""

from __future__ import annotations

import gzip
import json
import uuid
from pathlib import Path

import pytest

from conftest import FakeAgent
from fakes import MARKER, fake_secret
from mengine_bench import catalog, cli, leaderboard
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
    assert cli.main(["run", "--suite", "fast", "--agent", "cmd", "--cmd", json.dumps(template), "--model", "fake/ref",
                     "--tasks", TASK, "--out", str(out), "--submitter", "Alice Example"]) == 0
    printed = capsys.readouterr().out
    assert "privacy check: clean" in printed and "removed raw run dir" in printed
    assert list((scratch_root() / "runs").iterdir()) == [], "the raw run dir holds unredacted transcripts"
    [bundle] = out.glob("fast/*")
    assert bundle.name.split("_")[1:4] == ["cmd", "fake-ref", "none"]
    files = sorted(p.relative_to(bundle).as_posix() for p in bundle.rglob("*") if p.is_file())
    assert files == ["result.json", "summary.md", f"transcripts/{TASK}.jsonl.gz"]
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    assert result["submitter"] == "Alice Example"
    assert result["started_at"].endswith("Z") and result["finished_at"] >= result["started_at"]
    assert set(result["bench_commit"]) == {"sha", "dirty"}
    [task] = result["tasks"]
    assert task["passed"] and task["transcript"] == f"transcripts/{TASK}.jsonl.gz"
    transcript = gzip.decompress((bundle / task["transcript"]).read_bytes()).decode("utf-8")
    assert MARKER not in transcript and "[REDACTED:" in transcript
    assert env_secret not in transcript and "[REDACTED:env]" in transcript
    assert str(tmp_path) not in transcript and str(tmp_path) not in json.dumps(result)
    assert result["preflight"] == []
    assert "- Preflight: clean" in (bundle / "summary.md").read_text(encoding="utf-8")


def test_run_refuses_unclean_preflight_unless_allowed(fake_agent: FakeAgent, tmp_path: Path,
                                                      monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cli, "contamination", lambda *args, **kwargs: ["claude global instructions: x"])
    template = json.loads(fake_agent("reference", REFERENCE_AGENT))
    template.remove("-I")
    argv = ["run", "--suite", "fast", "--agent", "cmd", "--cmd", json.dumps(template), "--model", "fake/ref",
            "--tasks", TASK, "--out", str(tmp_path / "results")]
    with pytest.raises(SystemExit, match="1 preflight finding"):
        cli.main(argv)
    assert not (tmp_path / "results").exists(), "a refused run launches nothing"
    assert cli.main([*argv, "--allow-unclean"]) == 0
    [result_file] = (tmp_path / "results").glob("fast/*/result.json")
    assert json.loads(result_file.read_text(encoding="utf-8"))["preflight"] == ["claude global instructions: x"]
    assert "NOT CLEAN, not ranked" in (result_file.parent / "summary.md").read_text(encoding="utf-8")


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
    assert cli._outcome(task, record, ()).agent_s == 0.25


def _write_result(results: Path, name: str, objective: float, *, model: str = "m", judge: str | None = None,
                  visual: str = "rendered", task_ids: list[str] | None = None) -> Path:
    ids = task_ids if task_ids is not None else [task.id for task in catalog.tasks("fast")]
    result = {
        "suite": "fast", "scoring_version": "1.0", "date": "2026-10-19", "bench_version": "0.1.0",
        "agent": {"name": "cmd", "model": model, "effort": None, "version": None},
        "judge": None if judge is None else {"label": judge},
        "grading": {"visual": visual},
        "totals": {"objective": objective, "accuracy": objective, "solved": 1, "total": len(ids),
                   "total_agent_s": 10.0, "subjective": None, "composite": None},
        "tasks": [{"id": task_id} for task_id in ids],
    }
    bundle = results / "fast" / name
    bundle.mkdir(parents=True)
    (bundle / "result.json").write_text(json.dumps(result), encoding="utf-8")
    return bundle


def test_leaderboard_ranks_by_objective_and_groups_by_judge_and_visual_profile(tmp_path: Path) -> None:
    results = tmp_path / "results"
    _write_result(results, "low", 50.0, model="low-model")
    _write_result(results, "high", 90.0, model="high-model")
    _write_result(results, "judged", 70.0, model="judged-model", judge="judge-x@high")
    _write_result(results, "blind", 80.0, model="blind-model", visual="unrendered")
    board = leaderboard.build_leaderboard(results, tmp_path)
    assert board.ranked == 4 and board.unranked == []
    plain = board.markdown[board.markdown.index("## FAST, no judge, visual rendered"):]
    assert plain.index("| 1 | cmd  | high-model |") < plain.index("| 2 | cmd  | low-model |")
    assert "[summary](results/fast/high/summary.md)" in plain
    assert "## FAST, judge judge-x@high, visual rendered" in board.markdown
    assert "## FAST, no judge, visual unrendered" in board.markdown


@pytest.mark.parametrize("task_ids", [[TASK], [TASK, TASK]], ids=["subset", "duplicate"])
def test_leaderboard_lists_partial_runs_apart(tmp_path: Path, task_ids: list[str]) -> None:
    results = tmp_path / "results"
    _write_result(results, "part", 99.0, task_ids=task_ids)
    target = tmp_path / "LEADERBOARD.md"
    assert cli.main(["leaderboard", "--results", str(results), "--output", str(target)]) == 0
    text = target.read_text(encoding="utf-8")
    assert "| 1 | " not in text and "No results yet." in text
    assert "- `results/fast/part`: not exactly its suite's task set" in text[text.index("## Not ranked"):]


def test_leaderboard_lists_unclean_runs_apart(tmp_path: Path) -> None:
    results = tmp_path / "results"
    bundle = _write_result(results, "unclean", 99.0)
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    result["preflight"] = ["codex global instructions: <HOME>/.codex/AGENTS.md"]
    (bundle / "result.json").write_text(json.dumps(result), encoding="utf-8")
    _write_result(results, "clean", 50.0)
    board = leaderboard.build_leaderboard(results, tmp_path)
    assert board.ranked == 1
    assert board.unranked == [("results/fast/unclean", "started with preflight findings")]
