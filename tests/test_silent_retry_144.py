"""#144: a step that got no reply from the model before its limit runs once more; a slow agent never does."""

from __future__ import annotations

from pathlib import Path

import pytest

from mengine_bench import run_command
from mengine_bench.catalog import all_tasks
from mengine_bench.run_command import SILENT_RETRY_NOTE, JudgeEvidence, RunSettings, run_tasks
from mengine_bench.runner.stats import RunStats
from mengine_bench.runner.task_run import StepRecord, TaskRunRecord, silent_timeout


def _timeout(task_id: str, stats: RunStats, answers: list[str] | None = None) -> TaskRunRecord:
    return TaskRunRecord(task_id=task_id, status="timeout", answers=answers or [],
                         steps=[StepRecord(0, 90.0, None, "timeout", "step 0 exceeded", stats=stats)])


def test_silent_means_nothing_at_all_from_the_model_144() -> None:
    assert silent_timeout(_timeout("t", RunStats()))
    assert not silent_timeout(_timeout("t", RunStats(tool_calls=1)))
    assert not silent_timeout(_timeout("t", RunStats(generated_tokens=40)))
    assert not silent_timeout(_timeout("t", RunStats(), answers=["partial reply"]))
    assert not silent_timeout(TaskRunRecord(task_id="t", status="ok", steps=[StepRecord(0, 5.0, 0, "ok")]))


class FakeAgent:
    name = "fake"

    def version(self) -> str:
        return "0"


def test_a_silent_task_is_retried_once_and_flagged_a_slow_one_is_not_144(monkeypatch: pytest.MonkeyPatch,
                                                                        tmp_path: Path) -> None:
    silent, slow = all_tasks()[:2]
    calls: list[str] = []

    def fake_run_task(task, agent, root):
        root.mkdir(parents=True)
        calls.append(task.id)
        if task.id == silent.id and calls.count(task.id) == 1:
            return _timeout(task.id, RunStats())
        if task.id == slow.id:
            return _timeout(task.id, RunStats(tool_calls=3, generated_tokens=500))
        return TaskRunRecord(task_id=task.id, steps=[StepRecord(0, 20.0, 0, "ok")])

    monkeypatch.setattr(run_command, "run_task", fake_run_task)
    monkeypatch.setattr(run_command, "collect_environment", lambda: {})
    monkeypatch.setattr(run_command, "bench_commit", lambda: {"sha": "test"})
    results = run_tasks([silent, slow], FakeAgent(), RunSettings(model="m", effort=None), tmp_path, JudgeEvidence())
    assert calls == [silent.id, silent.id, slow.id]
    tasks = {task["id"]: task for task in results["tasks"]}
    assert tasks[silent.id]["status"] == "ok" and SILENT_RETRY_NOTE in tasks[silent.id]["flags"]
    assert tasks[slow.id]["status"] == "timeout" and SILENT_RETRY_NOTE not in tasks[slow.id]["flags"]
    assert (tmp_path / f"{silent.id}.silent").is_dir()
