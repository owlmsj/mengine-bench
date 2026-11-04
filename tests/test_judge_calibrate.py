"""Calibration reads audit exports and votes stored packets without modifying bundles."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fakes import FakeCalibrationJudge
from mengine_bench import bundle_judge, cli, visual
from mengine_bench.judge import JudgeContext, RUBRIC_VERSION

VOTES = Path(__file__).parent / "fixtures" / "judge_calibration" / "votes.txt"


def test_parse_exported_votes_with_free_labels_and_ab_aliases() -> None:
    from mengine_bench import judge_calibrate
    votes = judge_calibrate.parse_votes(VOTES.read_text(encoding="utf-8"))
    assert [(vote.task_id, vote.pick, vote.a, vote.b) for vote in votes] == [
        ("ds-ab-playtest", "Run Alpha", 80, 70), ("web-mondrian-landing", "empate", 60, 90)]
    for pick in ("Run Alpha", "Run Beta", "empate", "-"):
        [vote] = judge_calibrate.parse_votes(
            f"ds-ab-playtest: {pick} Run Alpha=0 Run Beta=100 (auditor: empate; judge 78/72)")
        assert (vote.pick, vote.a, vote.b) == (pick, 0, 100)
    [vote] = judge_calibrate.parse_votes(
        "ds-ab-playtest: A custom A custom=80 B custom=70 (auditor: empate; judge 78/72)")
    assert vote.pick == "A custom"


@pytest.mark.parametrize("text", ["", "task: A A=101 B=2 (auditor: A; judge 1/2)",
                                  "task: A A=1 (auditor: A; judge 1/2)", "bad line",
                                  "task: A A=1 B=2 (auditor: A; judge 1/2)\n" * 2])
def test_parser_rejects_missing_invalid_and_duplicate_votes(text: str) -> None:
    from mengine_bench import judge_calibrate
    with pytest.raises(ValueError, match="received.*expected"):
        judge_calibrate.parse_votes(text)


def _bundles(root: Path) -> tuple[Path, Path]:
    bundles = root / "bundle-a", root / "bundle-b"
    for bundle in bundles:
        (bundle / "judge").mkdir(parents=True)
        (bundle / "result.json").write_text('{"unchanged": true}', encoding="utf-8")
        for task in ("ds-ab-playtest", "web-mondrian-landing"):
            context = JudgeContext(task_id=task, prompts=(), answers=("stored answer",), diff="", transcript_tail="",
                                   checks=())
            (bundle / "judge" / f"{task}.json").write_text(json.dumps(context.record()), encoding="utf-8")
        page = bundle / "judge" / "web-mondrian-landing" / "landing" / "index.html"
        page.parent.mkdir(parents=True)
        page.write_text("<html>fixture</html>", encoding="utf-8")
    return bundles


def _snapshot(bundles: tuple[Path, Path]) -> dict[Path, bytes]:
    return {path: path.read_bytes() for bundle in bundles for path in bundle.rglob("*") if path.is_file()}


def test_command_reuses_packet_rendering_writes_only_on_request_and_enforces_limit(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    bundles = _bundles(tmp_path)
    before = _snapshot(bundles)
    monkeypatch.chdir(tmp_path)
    agent_args: list[tuple[object, ...]] = []
    monkeypatch.setattr(cli, "make_agent", lambda *args: agent_args.append(args))
    fake = FakeCalibrationJudge([88, 79, 60, 90] * 3)
    monkeypatch.setattr(cli, "RubricJudge", lambda agent: fake)
    budgets: list[int] = []

    def render(html: Path, png: Path, budget_ms: int) -> str:
        assert html.read_text(encoding="utf-8") == "<html>fixture</html>"
        budgets.append(budget_ms)
        png.parent.mkdir(parents=True, exist_ok=True)
        png.write_bytes(b"fixture frame")
        return visual.RENDERED

    monkeypatch.setattr(bundle_judge, "render_headless", render)
    argv = ["judge-calibrate", "--votes", str(VOTES.resolve()), *(str(bundle) for bundle in bundles)]
    assert cli.main(argv) == 0
    report = capsys.readouterr().out
    assert "| ds-ab-playtest | Run Alpha | A | 80 | 88 | 8 |" in report
    assert "| ds-ab-playtest | Run Alpha | B | 70 | 79 | 9 |" in report
    assert "Mean |diff|: 4.2" in report and "Beyond 8: 1" in report
    assert f"Rubric: {RUBRIC_VERSION}" in report
    assert not (tmp_path / "docs").exists()
    assert cli.main([*argv, "--write", "--max-beyond", "0"]) == 1
    saved = list((tmp_path / "docs" / "judge-calibration").glob(f"*-{RUBRIC_VERSION}.md"))
    assert len(saved) == 1 and saved[0].read_text(encoding="utf-8") == capsys.readouterr().out
    assert cli.main([*argv, "--max-beyond", "1"]) == 0
    assert agent_args == [("claude", "claude-opus-5-5", "xhigh", None)] * 3
    assert budgets == [1000, 4000, 8000] * 6
    assert fake.seen[2][1] == ("frame-1s.png", "frame-4s.png", "screenshot.png", "reference.png")
    assert fake.seen[0][0].answers == ("stored answer",)
    assert _snapshot(bundles) == before


def test_missing_vote_writes_no_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                      capsys: pytest.CaptureFixture[str]) -> None:
    bundles = _bundles(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "make_agent", lambda *args: None)
    monkeypatch.setattr(cli, "RubricJudge", lambda agent: FakeCalibrationJudge([None]))
    assert cli.main(["judge-calibrate", "--votes", str(VOTES.resolve()), *map(str, bundles), "--write"]) == 1
    assert "expected a judge vote" in capsys.readouterr().out
    assert not (tmp_path / "docs").exists()


def test_calibration_uses_real_rubric_prompt_without_launching_a_judge(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    from mengine_bench import judge

    bundles = _bundles(tmp_path)
    votes = tmp_path / "votes.txt"
    votes.write_text(VOTES.read_text(encoding="utf-8").splitlines()[0], encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "make_agent", lambda *args: None)
    prompts: list[str] = []

    def reply(agent: object, prompt: str, audit: Path, timeout_s: float,
              files: object = None) -> str:
        prompts.append(prompt)
        return '{"approach": 30, "deliverable": 25, "verification": 25, "score": 80, "rationale": "fixture"}'

    monkeypatch.setattr(judge, "_ask", reply)
    assert cli.main(["judge-calibrate", "--votes", str(votes), *map(str, bundles)]) == 0
    assert len(prompts) == 2 and all("stored answer" in prompt for prompt in prompts)
    assert "Beyond 8: 1" in capsys.readouterr().out
