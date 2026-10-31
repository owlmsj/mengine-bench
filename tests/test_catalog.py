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


def test_every_task_has_room_to_finish() -> None:
    """#39: GLM 5.3 lost a task at 300 s and took 306 s on another; DeepSeek stopped at 900 s with all checks passing."""
    limits = {task.id: task.timeout_s for task in catalog.all_tasks()}
    assert min(limits.values()) >= 600, limits
    assert {task for task, limit in limits.items() if limit == 1800} == {
        "gd-integration-repo", "web-mondrian-landing", "3d-voxel-landscape"}
