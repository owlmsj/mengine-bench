"""#165: the bench-audit skill builds its page from two bundles and auditor rows."""

import importlib.util
import json
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "bench-audit"


def _build_module():
    spec = importlib.util.spec_from_file_location("bench_audit_build", SKILL / "build.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _bundle(root: Path, name: str, judge: int) -> Path:
    bundle = root / name
    (bundle / "judge" / "landing").mkdir(parents=True)
    (bundle / "judge" / "landing" / "index.html").write_text("<!doctype html><title>x</title>", encoding="utf-8")
    (bundle / "judge" / "landing.png").write_bytes(b"\x89PNG fixture")
    (bundle / "evidence" / "voice").mkdir(parents=True)
    (bundle / "evidence" / "voice" / "announcement.wav").write_bytes(b"RIFF fixture")
    result = {"totals": {"score": 80.0, "solved": 2, "time_s": 125.0, "cost_usd": 1.5, "cost_basis": "harness", "judge": 70.0},
              "tasks": [{"id": "landing", "agent_s": 30.0, "cost_usd": 0.5, "judge": judge, "judge_rationale": "why",
                         "judge_parts": {"approach": 30}, "answers": ["done"]},
                        {"id": "voice", "agent_s": 20.0, "cost_usd": 0.4, "judge": judge, "answers": ["spoken"]}]}
    (bundle / "result.json").write_text(json.dumps(result), encoding="utf-8")
    return bundle


def _side(correct: str = "yes") -> dict:
    return {"grader_c": 1.0, "really_correct": correct, "evidence": "e", "solution": "s", "judge": 80, "my_judge": 78,
            "judge_verdict": "fair", "why": "w"}


def test_the_page_holds_every_row_the_media_and_a_publish_map(tmp_path: Path) -> None:
    a, b = _bundle(tmp_path, "run-a", 80), _bundle(tmp_path, "run-b", 60)
    rows = [{"task": "voice", "brief": "speak", "a": _side(), "b": _side("partial"), "grader_issue": None, "better": "a"},
            {"task": "landing", "brief": "page", "a": _side(), "b": _side(), "grader_issue": "passes blank page", "better": "tie"}]
    (tmp_path / "g1.json").write_text(json.dumps(rows), encoding="utf-8")
    config = {"id": "t", "title": "Audit <A>", "verdict": ["one"], "rows": ["g1.json"],
              "runs": [{"key": "a", "label": "Run A", "bundle": str(a)}, {"key": "b", "label": "Run B", "bundle": str(b)}]}
    (tmp_path / "audit.json").write_text(json.dumps(config), encoding="utf-8")
    files = _build_module().build(tmp_path / "audit.json", tmp_path / "site")
    html = (tmp_path / "site" / "index.html").read_text(encoding="utf-8")
    data = json.loads(html.split("const DATA = ", 1)[1].split(";\nconst $", 1)[0])
    assert [row["task"] for row in data["rows"]] == ["landing", "voice"], "rows follow the bundle's task order"
    assert data["runs"][0]["totals"]["real"] == 2 and data["runs"][1]["totals"]["real"] == 1
    assert data["rows"][0]["a"]["rationale"] == "why" and data["rows"][0]["a"]["answer"] == "done"
    assert data["gaps"] == [{"task": "landing", "text": "passes blank page"}]
    kinds = {item["kind"] for group in data["media"] for items in group["items"].values() for item in items}
    assert kinds == {"page", "audio"}
    assert "assets/a/voice/files/announcement.wav" in files and Path(files["assets/a/landing/page.html"]).is_file()
    assert json.loads((tmp_path / "site" / "files.json").read_text(encoding="utf-8")) == files
    assert "<title>Audit &lt;A></title>" in html


def test_a_row_missing_a_side_is_refused_with_the_task_named(tmp_path: Path) -> None:
    a, b = _bundle(tmp_path, "run-a", 80), _bundle(tmp_path, "run-b", 60)
    (tmp_path / "g1.json").write_text(json.dumps([{"task": "voice", "a": _side()}]), encoding="utf-8")
    config = {"rows": ["g1.json"], "runs": [{"key": "a", "label": "A", "bundle": str(a)}, {"key": "b", "label": "B", "bundle": str(b)}]}
    (tmp_path / "audit.json").write_text(json.dumps(config), encoding="utf-8")
    with pytest.raises(SystemExit, match="'voice' missing \\['b'\\]"):
        _build_module().build(tmp_path / "audit.json", tmp_path / "site")
