"""Bundle naming, the shipped JSON schema, and judged bundles on the leaderboard."""

from __future__ import annotations

import json
from pathlib import Path

from conftest import FakeAgent
from mengine_bench import cli
from mengine_bench.bundle import bundle_dir_name
from mengine_bench.verify import load_schema, verify_bundle
from test_bundle_verify import board_as_complete

ROOT = Path(__file__).resolve().parents[1]

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


def test_schema_ships_in_package_and_docs() -> None:
    docs = json.loads((ROOT / "docs" / "result.schema.json").read_text(encoding="utf-8"))
    assert docs == load_schema(), "docs/result.schema.json must be a copy of the packaged schema"


def test_judged_bundle_verifies_and_groups_by_judge(fake_agent: FakeAgent, tmp_path: Path) -> None:
    agent = json.loads(fake_agent("reference", REFERENCE_AGENT))
    agent.remove("-I")
    judge = json.loads(fake_agent("judge", JUDGE))
    out = tmp_path / "results"
    assert cli.main(["run", "--suite", "fast", "--agent", "cmd", "--cmd", json.dumps(agent), "--model", "fake/ref",
                     "--tasks", "ds-ab-playtest", "--out", str(out), "--work", str(tmp_path / "work"),
                     "--judge", "cmd", "--judge-cmd", json.dumps(judge), "--judge-model", "judge-x",
                     "--judge-effort", "high", "--judge-votes", "3"]) == 0
    [bundle] = out.glob("fast/*")
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    [task] = result["tasks"]
    assert task["judge_votes"] == [80, 80, 80] and task["judge_rationales"] == ["solid"] * 3
    assert result["totals"]["subjective"] == 80.0
    assert result["environment"]["judge"] == {"model": "judge-x", "effort": "high", "votes": 3}
    report = verify_bundle(bundle)
    assert report.ok, [(i.name, i.detail) for i in report.items if i.status == "FAIL"]
    assert any(item.status == "SELF-REPORTED" and item.name == "judge" for item in report.items)
    board = board_as_complete(out, tmp_path)
    assert "## FAST, judge judge-x@high" in board and "| 80.0 |" in board
