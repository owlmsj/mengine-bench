"""Runs without a judge store the judge's evidence; `mengine-bench judge` finishes and rescores them."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from conftest import FakeAgent
from mengine_bench import cli, visual
from test_bundle_leaderboard import REFERENCE_AGENT

# Answers both judge prompts: the rubric (a score) and the vision checklist (all items visible).
JUDGE = r"""
import json, re, sys
from pathlib import Path
prompt = Path(sys.argv[2]).read_text(encoding="utf-8")
if "screenshot.png" in prompt:
    items = re.findall(r"^(\d+)\. ", prompt, re.MULTILINE)
    print(json.dumps({item: True for item in items}))
else:
    print(json.dumps({"score": 80, "rationale": "solid"}))
"""

VISUAL_AGENT = """
import sys
from pathlib import Path
from mengine_bench import catalog
task = next(t for t in catalog.all_tasks() if t.id == "web-mondrian-landing")
sys.stdout.write(task.reference(Path(sys.argv[1]))[-1] or "done")
"""


def _template(fake_agent: FakeAgent, name: str, body: str) -> str:
    argv = json.loads(fake_agent(name, body))
    # -I would hide the installed package from the fake agent; drop it.
    argv.remove("-I")
    return json.dumps(argv)


def _run(fake_agent: FakeAgent, out: Path, task: str, body: str) -> Path:
    assert cli.main(["run", "--suite", "fast", "--agent", "cmd", "--cmd", _template(fake_agent, "agent", body),
                     "--model", "fake/ref", "--tasks", task, "--out", str(out)]) == 0
    [bundle] = out.glob("fast/*")
    return bundle


def _judge(fake_agent: FakeAgent, bundle: Path) -> int:
    return cli.main(["judge", str(bundle), "--judge", "cmd", "--judge-cmd", _template(fake_agent, "judge", JUDGE),
                     "--judge-model", "judge-x", "--judge-effort", "high", "--judge-votes", "3"])


def test_judging_later_sets_subjective_and_composite(fake_agent: FakeAgent, tmp_path: Path) -> None:
    bundle = _run(fake_agent, tmp_path / "results", "ds-ab-playtest", REFERENCE_AGENT)
    before = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    assert before["totals"]["subjective"] is None and before["judge_pending"] is True
    assert "pending" in (bundle / "summary.md").read_text(encoding="utf-8")
    assert _judge(fake_agent, bundle) == 0
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    [task] = result["tasks"]
    assert task["judge_votes"] == [80, 80, 80] and task["judge_rationales"] == ["solid"] * 3
    assert task["subjective"] == 80.0 and result["totals"]["subjective"] == 80.0
    assert result["totals"]["composite"] is not None
    assert result["totals"]["objective"] == before["totals"]["objective"], "a non-visual objective is unchanged"
    assert result["judge"] == {"label": "judge-x@high", "model": "judge-x", "effort": "high", "votes": 3,
                               "deferred": True}
    assert result["judge_pending"] is False
    assert "judged after the run" in (bundle / "summary.md").read_text(encoding="utf-8")
    assert _judge(fake_agent, bundle) == 1, "a judged bundle is not judged twice"


def test_visual_task_is_finished_by_the_vision_judge_from_the_stored_screenshot(
        fake_agent: FakeAgent, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_render(html: Path, png: Path) -> str:
        png.parent.mkdir(parents=True, exist_ok=True)
        png.write_bytes(b"P" * 50_000)
        return visual.RENDERED

    monkeypatch.setattr(visual, "RENDER", fake_render)
    bundle = _run(fake_agent, tmp_path / "results", "web-mondrian-landing", VISUAL_AGENT)
    before = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    [task] = before["tasks"]
    assert task["passed"] is False and "unrendered" in task["flags"], "no judge yet: capped like before"
    assert (bundle / "judge" / "web-mondrian-landing.png").stat().st_size == 50_000
    packet = json.loads((bundle / "judge" / "web-mondrian-landing.json").read_text(encoding="utf-8"))
    assert packet["vision"]["checklist"] and packet["vision"]["screenshot_ok"] is True
    assert _judge(fake_agent, bundle) == 0
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    [task] = result["tasks"]
    assert task["passed"] is True and task["c"] == 1.0
    assert not {"unrendered", "no judge"} & set(task["flags"])
    assert any(re.match(r"vision: ", check["name"]) for check in task["checks"])
    assert len(task["vision"]["ballots"]) == 3
    assert result["grading"] == {"visual": "rendered"}
    assert result["totals"]["objective"] > before["totals"]["objective"]


def test_judge_refuses_a_bundle_without_packets(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    bundle = tmp_path / "old"
    bundle.mkdir()
    (bundle / "result.json").write_text(json.dumps({"judge": None, "tasks": []}), encoding="utf-8")
    assert cli.main(["judge", str(bundle), "--judge", "cmd", "--judge-cmd", "x {prompt_file}"]) == 1
    assert "without judge packets" in capsys.readouterr().out
