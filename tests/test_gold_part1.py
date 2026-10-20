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

from mengine_bench.core import FAST, FULL, EvalTask

PART1_MODULES = ("gamedev", "business", "hard", "context", "compaction")

# Source catalog membership (private v1 suite); ids and suites must not drift.
EXPECTED_SUITES: dict[str, frozenset[str]] = {
    "gd-astar-doors": frozenset({FAST, FULL}),
    "gd-ecs-collision-bug": frozenset({FAST, FULL}),
    "ds-ab-playtest": frozenset({FAST, FULL}),
    "bo-pnl-runway": frozenset({FAST, FULL}),
    "bo-reconcile": frozenset({FULL}),
    "ds-sql-funnel": frozenset({FAST, FULL}),
    "lc-changelog": frozenset({FAST, FULL}),
    "vis-chart": frozenset({FAST, FULL}),
    "cmp-handoff": frozenset({FAST, FULL}),
}
HARD_IDS = {"ds-sql-funnel"}

def _modules() -> list[ModuleType]:
    return [importlib.import_module(f"mengine_bench.tasks.{name}") for name in PART1_MODULES]


def _part1_tasks() -> list[EvalTask]:
    return [task for module in _modules() for task in module.TASKS]


def test_part1_ids_suites_and_weights() -> None:
    found = {task.id: task for task in _part1_tasks()}
    assert {tid: t.suites for tid, t in found.items()} == EXPECTED_SUITES
    assert {tid for tid, t in found.items() if t.weight == 2} == HARD_IDS
    assert all(t.par_s >= 1 and float(t.par_s).is_integer() for t in found.values())


@pytest.mark.parametrize("task_id", sorted(EXPECTED_SUITES))
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

