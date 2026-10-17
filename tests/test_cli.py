"""CLI: dry run, listing, selftest and the generated docs/TASKS.md."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench import catalog, cli
from mengine_bench.report import TASKS_BEGIN, TASKS_END, render_tasks_table
from mengine_bench.runner import process

ROOT = Path(__file__).resolve().parents[1]


def test_dry_run_lists_tasks_and_launches_nothing(monkeypatch: pytest.MonkeyPatch,
                                                  capsys: pytest.CaptureFixture[str]) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("dry run launched a process")

    monkeypatch.setattr(process, "run_process", forbidden)
    assert cli.main(["run", "--suite", "fast", "--agent", "claude", "--model", "m", "--dry-run"]) == 0
    plan = json.loads(capsys.readouterr().out)
    assert plan["tasks"] == [task.id for task in catalog.tasks("fast")]
    assert len(plan["tasks"]) == 14
    assert plan["launches"] == 0 and plan["dry_run"] is True


def test_unknown_task_id_is_rejected() -> None:
    with pytest.raises(SystemExit, match="nope"):
        cli.main(["run", "--suite", "fast", "--agent", "claude", "--model", "m", "--tasks", "nope", "--dry-run"])


def test_cmd_agent_requires_template() -> None:
    with pytest.raises(SystemExit, match="--cmd"):
        cli.main(["run", "--suite", "fast", "--agent", "cmd", "--model", "m", "--dry-run"])


def test_list_full_suite(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["list", "--suite", "full"]) == 0
    assert len(capsys.readouterr().out.strip().splitlines()) == 20


def test_selftest_runs_gold_without_agent(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["selftest", "--tasks", "gd-astar-doors,vis-chart"]) == 0
    out = capsys.readouterr().out
    assert "PASS gd-astar-doors" in out and "PASS vis-chart" in out


def test_tasks_doc_matches_catalog() -> None:
    doc = (ROOT / "docs" / "TASKS.md").read_text(encoding="utf-8")
    start, end = doc.index(TASKS_BEGIN) + len(TASKS_BEGIN), doc.index(TASKS_END)
    expected = render_tasks_table(catalog.all_tasks())
    assert doc[start:end].strip() == expected.strip(), "regenerate with: uv run mengine-bench tasks-doc --write"
    assert expected.count("\n| ") == 20 + 1
