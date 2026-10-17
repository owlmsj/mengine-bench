"""Task registry: auto-discovers `mengine_bench/tasks/*.py` modules.

A contributor adds a task by dropping a module that exposes
`TASKS: list[EvalTask]`; no central list to edit, so merges rarely conflict.
"""

from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Iterable
from types import ModuleType

from mengine_bench import tasks as tasks_package
from mengine_bench.core import SUITES, EvalTask


def discover_task_modules() -> list[ModuleType]:
    names = sorted(info.name for info in pkgutil.iter_modules(tasks_package.__path__))
    return [importlib.import_module(f"{tasks_package.__name__}.{name}") for name in names if not name.startswith("_")]


def collect(modules: Iterable[ModuleType]) -> list[EvalTask]:
    found: list[EvalTask] = []
    owner: dict[str, str] = {}
    for module in modules:
        declared = getattr(module, "TASKS", None)
        if not isinstance(declared, (list, tuple)) or not all(isinstance(t, EvalTask) for t in declared):
            raise ValueError(f"module {module.__name__!r} has TASKS={declared!r:.80}; expected list[EvalTask]")
        for task in declared:
            if task.id in owner:
                raise ValueError(f"duplicate task id {task.id!r} in {module.__name__!r}; "
                                 f"already defined in {owner[task.id]!r}")
            owner[task.id] = module.__name__
            found.append(task)
    return found


def select(found: Iterable[EvalTask], suite: str) -> list[EvalTask]:
    if suite not in SUITES:
        raise ValueError(f"received suite={suite!r}; expected one of {SUITES}")
    return [task for task in found if suite in task.suites]


def all_tasks() -> list[EvalTask]:
    return collect(discover_task_modules())


def tasks(suite: str) -> list[EvalTask]:
    if suite not in SUITES:
        raise ValueError(f"received suite={suite!r}; expected one of {SUITES}")
    return select(all_tasks(), suite)
