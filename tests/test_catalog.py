"""Registry discovery."""

import types

import pytest

from mengine_bench import catalog
from mengine_bench.core import FAST, FULL, CheckResult, EvalTask, Step


def task(task_id: str, suites: frozenset[str]) -> EvalTask:
    return EvalTask(
        id=task_id, category="coding", suites=suites, provenance="test", summary="t",
        setup=lambda ws: None, steps=(Step("x"),), check=lambda ws, a: CheckResult(),
        reference=lambda ws: [], par_s=10.0,
    )


def test_discovery_runs_on_empty_package() -> None:
    assert isinstance(catalog.all_tasks(), list)


def test_collect_filters_by_suite() -> None:
    mod = types.ModuleType("fake")
    mod.TASKS = [task("a", frozenset({FAST, FULL})), task("b", frozenset({FULL}))]  # type: ignore[attr-defined]
    found = catalog.collect([mod])
    assert [t.id for t in catalog.select(found, FAST)] == ["a"]
    assert [t.id for t in catalog.select(found, FULL)] == ["a", "b"]


def test_module_without_task_list_is_rejected() -> None:
    mod = types.ModuleType("broken")
    mod.TASKS = "nope"  # type: ignore[attr-defined]
    with pytest.raises(ValueError, match="broken"):
        catalog.collect([mod])


def test_duplicate_ids_are_rejected() -> None:
    one, two = types.ModuleType("one"), types.ModuleType("two")
    one.TASKS = [task("dup", frozenset({FULL}))]  # type: ignore[attr-defined]
    two.TASKS = [task("dup", frozenset({FULL}))]  # type: ignore[attr-defined]
    with pytest.raises(ValueError, match="'dup'"):
        catalog.collect([one, two])


def test_unknown_suite_is_rejected() -> None:
    with pytest.raises(ValueError, match="'nightly'"):
        catalog.tasks("nightly")
