"""Registry discovery."""

import types

import pytest

from mengine_bench import catalog
from mengine_bench.core import CheckResult, EvalTask, Step


def task(task_id: str) -> EvalTask:
    return EvalTask(
        id=task_id, category="coding", provenance="test", summary="t",
        setup=lambda ws: None, steps=(Step("x"),), check=lambda ws, a: CheckResult(),
        reference=lambda ws: [],
    )


def test_discovery_runs_on_empty_package() -> None:
    assert isinstance(catalog.all_tasks(), list)


def test_collect_keeps_module_order() -> None:
    mod = types.ModuleType("fake")
    mod.TASKS = [task("a"), task("b")]  # type: ignore[attr-defined]
    assert [t.id for t in catalog.collect([mod])] == ["a", "b"]


def test_catalog_has_no_suites() -> None:
    assert not hasattr(catalog, "select") and not hasattr(catalog, "tasks")


def test_module_without_task_list_is_rejected() -> None:
    mod = types.ModuleType("broken")
    mod.TASKS = "nope"  # type: ignore[attr-defined]
    with pytest.raises(ValueError, match="broken"):
        catalog.collect([mod])


def test_duplicate_ids_are_rejected() -> None:
    one, two = types.ModuleType("one"), types.ModuleType("two")
    one.TASKS = [task("dup")]  # type: ignore[attr-defined]
    two.TASKS = [task("dup")]  # type: ignore[attr-defined]
    with pytest.raises(ValueError, match="'dup'"):
        catalog.collect([one, two])
