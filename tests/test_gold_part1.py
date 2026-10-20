"""Gold self-tests for the ported part-1 tasks.

reference solution -> PASS; untouched workspace + empty answers -> FAIL.
A gold that passes an empty workspace measures nothing; one that fails its
own reference would fail every agent.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from types import ModuleType

import pytest

from mengine_bench.core import EvalTask

PART1_MODULES = ("gamedev", "business", "hard", "context", "compaction")

# Source catalog membership (private v1 suite); ids must not drift.
EXPECTED_IDS = {
    "gd-astar-doors",
    "gd-ecs-collision-bug",
    "ds-ab-playtest",
    "bo-pnl-runway",
    "bo-reconcile",
    "gd-lockstep-desync",
    "ds-sql-funnel",
    "bo-safe-conversion",
    "lc-changelog",
    "lc-contract",
    "vis-chart",
    "cmp-handoff",
    "cmp-meeting-decisions",
    "cmp-agent-trajectory",
}

def _modules() -> list[ModuleType]:
    return [importlib.import_module(f"mengine_bench.tasks.{name}") for name in PART1_MODULES]


def _part1_tasks() -> list[EvalTask]:
    return [task for module in _modules() for task in module.TASKS]


def test_part1_ids() -> None:
    assert {task.id for task in _part1_tasks()} == EXPECTED_IDS


@pytest.mark.parametrize("task_id", sorted(EXPECTED_IDS))
def test_reference_passes_and_untouched_workspace_fails(task_id: str, tmp_path: Path) -> None:
    task = next(t for t in _part1_tasks() if t.id == task_id)
    empty = tmp_path / "empty"
    empty.mkdir()
    task.setup(empty)
    baseline = task.check(empty, [""] * len(task.steps))
    assert not baseline.passed, f"{task.id}: gold passes an untouched workspace"

    solved = tmp_path / "solved"
    solved.mkdir()
    task.setup(solved)
    answers = task.reference(solved)
    result = task.check(solved, answers)
    assert result.passed, f"{task.id}: reference fails {result.failed()}"

