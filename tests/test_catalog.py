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


def test_limits_fit_the_measured_times_and_cap_the_worst_case_at_56_minutes() -> None:
    # #98: from 7 to 10 runs. The slowest short eval took 50 s, Mondrian 194 s and 3D 288 s. The 56 min apply only when an
    # agent hits every limit; the prompt also asks it to stop polishing once the work is right.
    limits = {task.id: task.timeout_s for task in catalog.all_tasks()}
    assert sum(limits.values()) == 3360, limits
    assert {task: limit for task, limit in limits.items() if limit != 180} == {
        "gd-integration-repo": 300, "web-mondrian-landing": 300, "3d-voxel-landscape": 420, "web-word-universe": 360}
