"""Bundle naming and judged runs."""

from __future__ import annotations

import json
from pathlib import Path

from conftest import FakeAgent
from mengine_bench import cli
from mengine_bench.bundle import bundle_dir_name

REFERENCE_AGENT = """
import sys
from pathlib import Path
from mengine_bench import catalog
task = next(t for t in catalog.all_tasks() if t.id == "ds-ab-playtest")
sys.stdout.write(task.reference(Path(sys.argv[1]))[-1])
"""

JUDGE = """
import json
print(json.dumps({"score": 80, "rationale": "solid"}))
"""


def test_bundle_dir_name_slugs_every_part() -> None:
    name = bundle_dir_name("2026-10-17", "opencode", "deepseek/v4.1:flash", None, "a1b2c3d4")
    assert name == "2026-10-17_opencode_deepseek-v4.1-flash_none_a1b2c3d4"
    assert bundle_dir_name("2026-10-17", "claude", "claude-opus-5-5", "x high", "ff").endswith("_x-high_ff")


def test_judged_run_records_votes_and_rationales(fake_agent: FakeAgent, tmp_path: Path) -> None:
    agent = json.loads(fake_agent("reference", REFERENCE_AGENT))
    agent.remove("-I")
    judge = json.loads(fake_agent("judge", JUDGE))
    out = tmp_path / "results"
    assert cli.main(["run", "--agent", "cmd", "--cmd", json.dumps(agent), "--model", "fake/ref",
                     "--tasks", "ds-ab-playtest", "--out", str(out), "--work", str(tmp_path / "work"),
                     "--judge", "cmd", "--judge-cmd", json.dumps(judge), "--judge-model", "judge-x",
                     "--judge-effort", "high", "--judge-votes", "3"]) == 0
    [bundle] = out.glob("*")
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    [task] = result["tasks"]
    assert task["judge_votes"] == [80, 80, 80] and task["judge_rationales"] == ["solid"] * 3
    assert result["totals"]["subjective"] == 80.0
    assert result["environment"]["judge"] == {"model": "judge-x", "effort": "high", "votes": 3}
