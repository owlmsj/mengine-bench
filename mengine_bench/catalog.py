"""Task registry: auto-discovers `mengine_bench/tasks/*.py` modules.

A contributor adds a task by dropping a module that exposes
`TASKS: list[EvalTask]`; no central list to edit, so merges rarely conflict.
"""

from __future__ import annotations

import importlib
import importlib.util
import pkgutil
from collections.abc import Iterable
from pathlib import Path
from types import ModuleType

from mengine_bench import candidates as candidates_package
from mengine_bench import tasks as tasks_package
from mengine_bench.core import EvalTask


def discover_task_modules(package: ModuleType = tasks_package) -> list[ModuleType]:
    names = sorted(info.name for info in pkgutil.iter_modules(package.__path__))
    return [importlib.import_module(f"{package.__name__}.{name}") for name in names if not name.startswith("_")]


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


def tasks_from_dir(folder: Path) -> list[EvalTask]:
    """#228: an external pool (mengine#952) of task modules; loaded by path, never joins the catalog."""
    modules: list[ModuleType] = []
    for path in sorted(folder.glob("*.py")):
        if path.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(f"mengine_bench_external_{path.stem}", path)
        if spec is None or spec.loader is None:
            raise ValueError(f"received {path}; expected an importable Python module")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules.append(module)
    tasks = collect(modules)
    if not tasks:
        raise ValueError(f"received {folder} with no TASKS; expected *.py modules exposing TASKS: list[EvalTask]")
    return tasks


def all_tasks() -> list[EvalTask]:
    return collect(discover_task_modules())


def candidate_tasks() -> list[EvalTask]:
    """Tasks outside the catalog (docs/CANDIDATES.md), runnable by id with `run --tasks` for a probe, never ranked."""
    return collect(discover_task_modules(candidates_package))


def task_by_id(task_id: str) -> EvalTask | None:
    return next((task for task in [*all_tasks(), *candidate_tasks()] if task.id == task_id), None)
