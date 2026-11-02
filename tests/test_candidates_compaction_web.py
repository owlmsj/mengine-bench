"""Hermetic gold tests for the compaction and web candidates (#127)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.candidates.compaction_web import TASKS
from mengine_bench.core import EvalTask


@pytest.mark.parametrize("task", TASKS, ids=lambda task: task.id)
def test_reference_passes_and_untouched_fails(task: EvalTask, tmp_path: Path) -> None:
    task.setup(tmp_path)
    assert not task.check(tmp_path, [""] * len(task.steps)).passed
    assert task.check(tmp_path, task.reference(tmp_path)).passed


def test_candidates_stay_outside_catalog() -> None:
    assert not {task.id for task in TASKS} & {task.id for task in catalog.all_tasks()}


@pytest.mark.parametrize("task", [task for task in TASKS if len(task.steps) == 2], ids=lambda task: task.id)
def test_fresh_session_retains_only_handoff(task: EvalTask, tmp_path: Path) -> None:
    first, second = tmp_path / "first", tmp_path / "second"
    task.setup(first)
    task.reference(first)
    step = task.steps[1]
    assert step.fresh_session and step.carry and step.hide
    second.mkdir()
    for filename in step.carry:
        (second / filename).write_bytes((first / filename).read_bytes())
    assert not any((second / filename).exists() for filename in step.hide)
    assert not (second / "result.json").exists()
    # The harness retains the carried summary for final grading (#127).
    (second / "result.json").write_bytes((first / "result.json").read_bytes())
    assert task.check(second, []).passed


def _replace_result(ws: Path, key: str, value: object) -> None:
    path = ws / "result.json"
    result = json.loads(path.read_text(encoding="utf-8"))
    result[key] = value
    path.write_text(json.dumps(result), encoding="utf-8")


@pytest.mark.parametrize("key,wrong", [
    ("new_price_brl", 59), ("starts_on", "2026-07-01"),
    ("approved_role", "backend developer"), ("role_owner", "Caio"),
    ("cloud_cap_brl", 6000), ("billing_due", "2026-08-31"),
    ("designer_gate", {"quarter": "Q4", "revenue_above_brl": 30000}),
    ("designer_gate", {"quarter": "Q3", "revenue_above_brl": 300000}),
])
def test_meeting_rejects_plausible_wrong_answer(tmp_path: Path, key: str, wrong: object) -> None:
    task = next(task for task in TASKS if task.id == "cmp-meeting-decisions")
    task.setup(tmp_path)
    task.reference(tmp_path)
    _replace_result(tmp_path, key, wrong)
    assert f"answer {key}" in task.check(tmp_path, []).failed()


@pytest.mark.parametrize("summary", ["", "x" * 2001])
def test_meeting_rejects_unusable_note(tmp_path: Path, summary: str) -> None:
    task = TASKS[0]
    task.reference(tmp_path)
    (tmp_path / "DECISIONS.md").write_text(summary, encoding="utf-8")
    assert not task.check(tmp_path, []).passed


def test_meeting_accepts_common_formats(tmp_path: Path) -> None:
    task = TASKS[0]
    task.reference(tmp_path)
    for key, value in {"new_price_brl": "R$ 55,00", "cloud_cap_brl": "R$ 60.000,00",
                       "starts_on": "01/08/2026", "billing_due": "July 31, 2026",
                       "approved_role": "sre", "role_owner": "LIVIA"}.items():
        _replace_result(tmp_path, key, value)
    assert task.check(tmp_path, []).passed


@pytest.mark.parametrize("key,wrong", [
    ("last_edited_file", "tests/net_test.cpp"),
    ("failing_test", "ReplicationTest.Serialization"),
    ("last_p99_ms", 12.9), ("last_p99_ms", "11.8 or 12.9"),
    ("abandoned_approach", "scalar serializer"),
    ("abandonment_reason", "too slow on x86"),
])
def test_trajectory_rejects_plausible_wrong_answer(tmp_path: Path, key: str, wrong: object) -> None:
    task = next(task for task in TASKS if task.id == "cmp-agent-trajectory")
    task.reference(tmp_path)
    _replace_result(tmp_path, key, wrong)
    assert f"answer {key}" in task.check(tmp_path, []).failed()


@pytest.mark.parametrize("summary", ["", "x" * 1801])
def test_trajectory_rejects_unusable_note(tmp_path: Path, summary: str) -> None:
    task = next(task for task in TASKS if task.id == "cmp-agent-trajectory")
    task.reference(tmp_path)
    (tmp_path / "STATE.md").write_text(summary, encoding="utf-8")
    assert not task.check(tmp_path, []).passed


def test_trajectory_accepts_common_formats(tmp_path: Path) -> None:
    task = next(task for task in TASKS if task.id == "cmp-agent-trajectory")
    task.reference(tmp_path)
    for key, value in {"last_p99_ms": "11,80 ms", "last_edited_file": "server\\net\\replication.cpp",
                       "abandoned_approach": "AVX2 serializer", "abandonment_reason": "ARM64 build crashes"}.items():
        _replace_result(tmp_path, key, value)
    assert task.check(tmp_path, []).passed
