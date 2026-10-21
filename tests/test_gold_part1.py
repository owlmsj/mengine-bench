"""Gold self-tests for the ported part-1 tasks.

reference solution -> PASS; untouched workspace + empty answers -> FAIL.
A gold that passes an empty workspace measures nothing; one that fails its
own reference would fail every agent.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from types import ModuleType

import pytest

from mengine_bench.core import EvalTask

PART1_MODULES = ("gamedev", "business", "funnel", "context", "compaction")

# Source catalog membership (private v1 suite); ids must not drift.
EXPECTED_IDS = {
    "gd-astar-doors",
    "gd-ecs-collision-bug",
    "ds-ab-playtest",
    "bo-pnl-runway",
    "bo-reconcile",
    "ds-sql-funnel",
    "lc-changelog",
    "vis-chart",
    "cmp-handoff",
}

def _modules() -> list[ModuleType]:
    return [importlib.import_module(f"mengine_bench.tasks.{name}") for name in PART1_MODULES]


def _part1_tasks() -> list[EvalTask]:
    return [task for module in _modules() for task in module.TASKS]


def test_part1_ids() -> None:
    assert {task.id for task in _part1_tasks()} == EXPECTED_IDS


@pytest.mark.parametrize("task_id", sorted(EXPECTED_IDS))
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



def test_ecs_untouched_tests_grant_no_correctness(tmp_path: Path) -> None:
    task = next(t for t in _part1_tasks() if t.id == "gd-ecs-collision-bug")
    task.setup(tmp_path)
    result = task.check(tmp_path, [""])
    assert not result.passed
    assert result.score == 0
    assert result.mandatory == [("visible tests left untouched", True)]


@pytest.mark.parametrize("fixed_file,expected_check", [
    ("arena_ecs/systems/movement.py", "hidden movement"),
    ("arena_ecs/systems/collision.py", "hidden collision"),
])
def test_ecs_scores_movement_and_collision_separately(
    tmp_path: Path, fixed_file: str, expected_check: str,
) -> None:
    from mengine_bench.tasks import gamedev

    gamedev._ecs_setup(tmp_path)
    gamedev._ecs_reference(tmp_path)
    for rel in ("arena_ecs/systems/movement.py", "arena_ecs/systems/collision.py"):
        if rel != fixed_file:
            (tmp_path / rel).write_text(gamedev.ECS_FILES[rel], encoding="utf-8")
    result = gamedev._ecs_check(tmp_path, [""])
    assert result.score == 0.5
    assert [name for name, ok in result.checks if ok] == [expected_check]
    assert not result.passed


def test_ecs_modified_visible_tests_fail_integrity(tmp_path: Path) -> None:
    from mengine_bench.tasks import gamedev

    gamedev._ecs_setup(tmp_path)
    gamedev._ecs_reference(tmp_path)
    (tmp_path / "tests/test_systems.py").write_text("", encoding="utf-8")
    result = gamedev._ecs_check(tmp_path, [""])
    assert result.mandatory == [("visible tests left untouched", False)]
    assert all(ok for _, ok in result.checks)
    assert not result.passed


@pytest.mark.parametrize("invoice_id", ["INV-1021", "INV-1036"])
@pytest.mark.parametrize("wrong_paid", [0, "not a number", None])
def test_reconcile_rejects_wrong_paid(
    tmp_path: Path, invoice_id: str, wrong_paid: object,
) -> None:
    from mengine_bench.tasks import business

    business._recon_setup(tmp_path)
    business._recon_reference(tmp_path)
    output = tmp_path / "reconciliation.json"
    reconciliation = json.loads(output.read_text(encoding="utf-8"))
    for mismatch in reconciliation["mismatched"]:
        if mismatch["id"] == invoice_id:
            mismatch["paid"] = wrong_paid
    output.write_text(json.dumps(reconciliation), encoding="utf-8")
    result = business._recon_check(tmp_path, [""])
    assert not result.passed
    assert "invoiced vs paid on mismatches" in result.failed()


@pytest.mark.parametrize("delta,expected", [(0.005, True), (0.02, False)])
def test_reconcile_paid_cent_tolerance(tmp_path: Path, delta: float, expected: bool) -> None:
    from mengine_bench.tasks import business

    business._recon_setup(tmp_path)
    business._recon_reference(tmp_path)
    output = tmp_path / "reconciliation.json"
    reconciliation = json.loads(output.read_text(encoding="utf-8"))
    for mismatch in reconciliation["mismatched"]:
        mismatch["paid"] += delta
    output.write_text(json.dumps(reconciliation), encoding="utf-8")
    assert business._recon_check(tmp_path, [""]).passed is expected


@pytest.mark.parametrize("case,expected", [
    ("strings", True), ("objects", True), ("mixed", True), ("duplicate_mismatch", True),
    ("non_object_mismatch", False), ("wrong_id", False), ("missing_id", False),
    ("repeated_id", False), ("non_list", False),
])
def test_reconcile_id_forms_and_exclusive_categories(tmp_path: Path, case: str, expected: bool) -> None:
    from mengine_bench.tasks import business

    business._recon_reference(tmp_path)
    output = tmp_path / "reconciliation.json"
    reconciliation = json.loads(output.read_text(encoding="utf-8"))
    if case in ("objects", "mixed"):
        for key in ("unpaid", "duplicated"):
            reconciliation[key] = [
                {"id": inv} if case == "objects" or i == 0 else inv
                for i, inv in enumerate(reconciliation[key])
            ]
    if case == "duplicate_mismatch":
        reconciliation["mismatched"].append({"id": "INV-1015", "invoiced": 10, "paid": 20})
    if case == "non_object_mismatch":
        reconciliation["mismatched"].append("WRONG")
    if case == "wrong_id":
        reconciliation["unpaid"][0] = "WRONG"
    if case == "missing_id":
        reconciliation["unpaid"][0] = {}
    if case == "repeated_id":
        reconciliation["unpaid"].append(reconciliation["unpaid"][0])
    if case == "non_list":
        reconciliation["mismatched"] = {"id": "INV-1021"}
    output.write_text(json.dumps(reconciliation), encoding="utf-8")
    assert business._recon_check(tmp_path, [""]).passed is expected


@pytest.mark.parametrize("key,wrong", [
    ("final_decode", "138.0"),
    ("final_decode", "38.01"),
    ("final_decode", "-38.0"),
    ("final_vram_mib", "17697"),
    ("discarded_quant", "Q60"),
    ("discarded_quant", "notQ6_K"),
    ("pending", "NOTREADME"),
    ("pending", "check_visionary"),
    ("file_line", "scripts/start_server.ps1:1650"),
    ("measure_command", "fake_measure_decode.ps1"),
])
def test_handoff_rejects_embedded_answer_tokens(tmp_path: Path, key: str, wrong: str) -> None:
    from mengine_bench.tasks import compaction

    compaction._handoff_setup(tmp_path)
    answers = compaction._handoff_reference(tmp_path)
    payload = json.loads(answers[-1])
    payload[key] = wrong
    answers[-1] = json.dumps(payload)
    result = compaction._handoff_check(tmp_path, answers)
    assert not result.passed
    assert f"answer {key}" in result.failed()


@pytest.mark.parametrize("key,valid", [
    ("final_decode", "decode: 38,0 t/s"),
    ("final_decode", "38.00"),
    ("final_decode", "38"),
    ("discarded_quant", "Q6_K does not fit"),
    ("pending", "Update README.md"),
    ("pending", "Remove check_vision.ps1"),
])
def test_handoff_accepts_answer_tokens_in_prose(tmp_path: Path, key: str, valid: str) -> None:
    from mengine_bench.tasks import compaction

    compaction._handoff_setup(tmp_path)
    answers = compaction._handoff_reference(tmp_path)
    payload = json.loads(answers[-1])
    payload[key] = valid
    answers[-1] = json.dumps(payload)
    assert compaction._handoff_check(tmp_path, answers).passed


def test_funnel_counts_ordered_steps_without_expiry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    from mengine_bench.tasks import funnel

    users = [("p", "pc", 0), ("q", "pc", 0), ("s", "steamdeck", 0), ("test", "pc", 1)]
    events = [
        ("p", "install", "2026-01-01 00:00:00"),
        ("p", "install", "2026-01-02 00:00:00"),
        ("p", "tutorial_complete", "2026-01-20 00:00:00"),
        ("p", "first_match", "2026-01-30 00:00:00"),
        ("p", "purchase", "2026-02-20 00:00:00"),
        ("q", "purchase", "2026-01-01 00:00:00"),
        ("q", "install", "2026-01-02 00:00:00"),
        ("q", "first_match", "2026-01-03 00:00:00"),
        ("q", "tutorial_complete", "2026-01-04 00:00:00"),
    ]
    events += [(uid, step, "2026-01-01 00:00:00")
               for uid in ("s", "test", "ghost") for step in funnel.FUNNEL]
    events += [("s", "purchase", "2026-01-01 00:00:00")]
    monkeypatch.setattr(funnel, "_funnel_rows", lambda: (users, list(reversed(events))))
    expected = [
        ("pc", "install", 2, 1.0), ("pc", "tutorial_complete", 2, 1.0),
        ("pc", "first_match", 1, 0.5), ("pc", "purchase", 1, 1.0),
        ("steamdeck", "install", 1, 1.0), ("steamdeck", "tutorial_complete", 1, 1.0),
        ("steamdeck", "first_match", 1, 1.0), ("steamdeck", "purchase", 1, 1.0),
    ]
    assert funnel._funnel_expected() == expected
    funnel._funnel_setup(tmp_path)
    assert not funnel._funnel_check(tmp_path, [""]).passed
    assert funnel._funnel_check(tmp_path, funnel._funnel_reference(tmp_path)).passed
    csv_text = "platform,step,users,conv_from_prev\n" + "".join(
        f"{platform},{step},{count},{conversion:.4f}\n" for platform, step, count, conversion in expected
    )
    assert (tmp_path / "funnel.csv").read_text(encoding="utf-8") == csv_text


@pytest.mark.parametrize("task", _part1_tasks(), ids=lambda task: task.id)
def test_part1_summaries_are_short_sentences(task: EvalTask) -> None:
    assert 0 < len(task.summary) <= 120
    assert task.summary.endswith(".") and task.summary.count(".") == 1
    assert "\n" not in task.summary
    assert task.provenance
