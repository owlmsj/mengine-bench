"""CLI: dry run, listing, selftest and the generated docs/TASKS.md and README task summaries."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench import catalog, cli
from mengine_bench.report import (
    SUMMARIES_BEGIN, SUMMARIES_END, TASKS_BEGIN, TASKS_END, render_task_summaries, render_tasks_table,
)
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
    assert len(plan["tasks"]) == 12
    assert plan["launches"] == 0 and plan["dry_run"] is True


def test_unknown_task_id_is_rejected() -> None:
    with pytest.raises(SystemExit, match="nope"):
        cli.main(["run", "--suite", "fast", "--agent", "claude", "--model", "m", "--tasks", "nope", "--dry-run"])


def test_cmd_agent_requires_template() -> None:
    with pytest.raises(SystemExit, match="--cmd"):
        cli.main(["run", "--suite", "fast", "--agent", "cmd", "--model", "m", "--dry-run"])


def test_list_full_suite(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["list", "--suite", "full"]) == 0
    assert len(capsys.readouterr().out.strip().splitlines()) == 14


def test_selftest_runs_gold_without_agent(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["selftest", "--tasks", "gd-astar-doors,vis-chart"]) == 0
    out = capsys.readouterr().out
    assert "PASS gd-astar-doors" in out and "PASS vis-chart" in out


def test_tasks_doc_matches_catalog() -> None:
    doc = (ROOT / "docs" / "TASKS.md").read_text(encoding="utf-8")
    start, end = doc.index(TASKS_BEGIN) + len(TASKS_BEGIN), doc.index(TASKS_END)
    expected = render_tasks_table(catalog.all_tasks())
    assert doc[start:end].strip() == expected.strip(), "regenerate with: uv run mengine-bench tasks-doc --write"
    assert expected.count("\n| ") == 14 + 1


def test_readme_task_summaries_match_catalog() -> None:
    doc = (ROOT / "README.md").read_text(encoding="utf-8")
    start, end = doc.index(SUMMARIES_BEGIN) + len(SUMMARIES_BEGIN), doc.index(SUMMARIES_END)
    expected = render_task_summaries(catalog.all_tasks())
    assert doc[start:end].strip() == expected.strip(), "regenerate with: uv run mengine-bench tasks-doc --readme"
    assert all(f"`{task.id}`" in expected for task in catalog.all_tasks())


def test_tasks_doc_readme_rewrites_only_the_marked_block(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text(f"intro\n{SUMMARIES_BEGIN}\nstale\n{SUMMARIES_END}\noutro\n", encoding="utf-8")
    assert cli.main(["tasks-doc", "--readme", str(readme)]) == 0
    text = readme.read_text(encoding="utf-8")
    assert "stale" not in text and text.startswith("intro\n") and text.endswith("outro\n")
    assert render_task_summaries(catalog.all_tasks()).strip() in text
