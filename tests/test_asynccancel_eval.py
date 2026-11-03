"""#151: py-async-cancel passes a run_tasks that cleans up on Ctrl+C and fails the ones that leak, serialize or overrun."""

from __future__ import annotations

from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.core import EvalTask, write
from mengine_bench.tasks.asynccancel import AC_MODULE, AC_SCENARIOS, _ac_check, _ac_setup

PARALLEL, LIMIT, BELOW, AT, QUEUED = (label for label, *_ in AC_SCENARIOS)

# Another valid route: a fixed pool of workers pulling from a queue, cancelled together on the way out.
WORKER_POOL = '''import asyncio


async def run_tasks(tasks, max_concurrent):
    queue = asyncio.Queue()
    for job in tasks:
        queue.put_nowait(job)

    async def worker():
        while True:
            try:
                job = queue.get_nowait()
            except asyncio.QueueEmpty:
                return
            await job()

    workers = [asyncio.ensure_future(worker()) for _ in range(min(max_concurrent, len(tasks)))]
    try:
        await asyncio.gather(*workers)
    finally:
        for task in workers:
            task.cancel()
        await asyncio.gather(*workers, return_exceptions=True)
'''

# asyncio.gather over a semaphore: the queued job cancels at once, gather ends, and asyncio.run then cancels the
# running jobs' cleanup (upstream's "above max concurrent" gotcha).
GATHER = '''import asyncio


async def run_tasks(tasks, max_concurrent):
    slots = asyncio.Semaphore(max_concurrent)

    async def one(job):
        async with slots:
            await job()

    await asyncio.gather(*(one(job) for job in tasks))
'''

SERIAL = '''async def run_tasks(tasks, max_concurrent):
    for job in tasks:
        await job()
'''

UNBOUNDED = '''import asyncio


async def run_tasks(tasks, max_concurrent):
    async with asyncio.TaskGroup() as group:
        for job in tasks:
            group.create_task(job())
'''

# Swallows the cancel and carries on, so the queued job starts after Ctrl+C.
KEEPS_GOING = '''import asyncio


async def run_tasks(tasks, max_concurrent):
    for start in range(0, len(tasks), max_concurrent):
        try:
            await asyncio.gather(*(job() for job in tasks[start:start + max_concurrent]), return_exceptions=True)
        except asyncio.CancelledError:
            pass
'''


def _task() -> EvalTask:
    return next(task for task in catalog.all_tasks() if task.id == "py-async-cancel")


def _with(tmp_path: Path, source: str) -> list[str]:
    _ac_setup(tmp_path)
    write(tmp_path, AC_MODULE, source)
    return _ac_check(tmp_path, [""]).failed()


def test_the_reference_passes_and_the_untouched_folder_fails(tmp_path: Path) -> None:
    task = _task()
    (tmp_path / "bare").mkdir()
    (tmp_path / "solved").mkdir()
    task.setup(tmp_path / "bare")
    bare = task.check(tmp_path / "bare", [""])
    assert not bare.passed and set(bare.failed()) == {PARALLEL, LIMIT, BELOW, AT, QUEUED}
    task.setup(tmp_path / "solved")
    result = task.check(tmp_path / "solved", task.reference(tmp_path / "solved"))
    assert result.passed, (result.failed(), result.details)


def test_a_worker_pool_also_passes(tmp_path: Path) -> None:
    assert _with(tmp_path, WORKER_POOL) == []


@pytest.mark.parametrize(("source", "lost"), [
    (GATHER, [QUEUED]),
    (SERIAL, [PARALLEL, BELOW, AT, QUEUED]),
    (UNBOUNDED, [LIMIT, QUEUED]),
    (KEEPS_GOING, [QUEUED]),
])
def test_a_runner_that_leaks_or_ignores_the_limit_fails_that_check(tmp_path: Path, source: str, lost: list[str]) -> None:
    assert _with(tmp_path, source) == lost


def test_the_brief_does_not_hand_over_the_method() -> None:
    prompt = _task().steps[0].prompt.lower()
    for word in ("semaphore", "taskgroup", "gather", "cancellederror", "finally", "shield"):
        assert word not in prompt, word
