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
    ("pending", "Remove check_vision.ps1 from README"),
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


@pytest.mark.parametrize("key,value,expected", [
    ("sessions_a", "900", True), ("sessions_b", "900.0", True),
    ("sessions_a", 900, True), ("sessions_a", "900.1", False),
    ("sessions_b", 970, False), ("sessions_a", "nan", False),
    ("ship_b", "true", False), ("ship_b", 1, False),
])
def test_ab_numeric_counts_keep_exact_method(
    tmp_path: Path, key: str, value: object, expected: bool,
) -> None:
    from mengine_bench.tasks import business

    payload = business._ab_expected()
    payload[key] = value
    (tmp_path / "ab_result.json").write_text(json.dumps(payload), encoding="utf-8")
    assert business._ab_check(tmp_path, [""]).passed is expected


@pytest.mark.parametrize("case,expected", [
    ("reference", True), ("duplicate", False), ("reordered", False), ("missing", False),
])
def test_pnl_checks_every_line_in_order(tmp_path: Path, case: str, expected: bool) -> None:
    from mengine_bench.tasks import business

    business._pnl_reference(tmp_path)
    output = tmp_path / "pnl.csv"
    lines = output.read_text(encoding="utf-8").splitlines()
    if case == "duplicate":
        lines.insert(2, lines[1])
    if case == "reordered":
        lines[1], lines[2] = lines[2], lines[1]
    if case == "missing":
        lines.pop()
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    result = business._pnl_check(tmp_path, [""])
    assert dict(result.checks)["pnl.csv lines in order"] is expected
    assert result.passed is expected


@pytest.mark.parametrize("count,expected", [
    ("{count}", True), ("{count}.0", True), ("{count}.1", False), ("0", False), ("nan", False),
])
def test_funnel_accepts_only_exact_numeric_users(tmp_path: Path, count: str, expected: bool) -> None:
    from mengine_bench.tasks import funnel

    funnel._funnel_reference(tmp_path)
    output = tmp_path / "funnel.csv"
    lines = output.read_text(encoding="utf-8").splitlines()
    fields = lines[1].split(",")
    fields[2] = count.format(count=fields[2])
    lines[1] = ",".join(fields)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert funnel._funnel_check(tmp_path, [""]).passed is expected


@pytest.mark.parametrize("key", ["build_change", "build_revert"])
@pytest.mark.parametrize("form,expected", [
    ("{}", True), ("Build {}", True), ("v{}", True), ("  build {}  ", True),
    ("{}0", False), ("NotBuild {}", False), ("0.9.180", False),
])
def test_changelog_normalizes_only_build_prefixes(
    tmp_path: Path, key: str, form: str, expected: bool,
) -> None:
    from mengine_bench.tasks import context

    payload = json.loads(context._changelog_reference(tmp_path)[0])
    payload[key] = form.format(payload[key])
    assert context._changelog_check(tmp_path, [json.dumps(payload)]).passed is expected


@pytest.mark.parametrize("key,value,expected", [
    ("top_gpu", " b200 ", True), ("bottom_gpu", " a 100 ", True),
    ("top_gpu", "NVIDIA B200", True), ("bottom_gpu", "Nvidia A100 GPU", True),
    ("top_gpu", "NOT-B200: H100", False), ("bottom_gpu", "NOT-A100: H100", False),
    ("top_gpu", "B2000", False), ("bottom_gpu", "H100", False),
    ("ratio", 2.96, True), ("ratio", "2.964", True), ("ratio", 2.966, False),
    ("ratio", 2.95, False), ("ratio", "nan", False),
])
def test_chart_normalizes_names_and_uses_rounded_ratio(
    tmp_path: Path, key: str, value: object, expected: bool,
) -> None:
    from mengine_bench.tasks import context

    payload = {"top_gpu": "B200", "top_tps": 210, "bottom_gpu": "A100", "ratio": 2.96}
    payload[key] = value
    assert context._chart_check(tmp_path, [json.dumps(payload)]).passed is expected


@pytest.mark.parametrize("key,value,expected", [
    ("final_vram_mib", "7697 MiB (7881 was the spilled reading)", True),
    ("final_vram_mib", "7881 MiB, corrected to 7697", False),
    ("final_vram_mib", "7697.1", False), ("final_vram_mib", "", False),
    ("file_line", "start_server.ps1, line 165", True),
    ("file_line", "start_server.ps1:1650", False),
    ("measure_command", "measure_decode.ps1 131072 1024", True),
    ("measure_command", "measure_decode.ps1", False),
    ("measure_command", "measure_decode.ps1 131072", False),
    ("measure_command", "measure_decode.ps1 1024", False),
    ("measure_command", "measure_decode.ps1 1310720 10240", False),
    ("pending", "Update README.md", True), ("pending", "Fix the README", True),
    ("pending", "Remove check_vision.ps1 from README", True),
    ("pending", "Edit README", True), ("pending", "Replace the README reference", True),
    ("pending", "evals README still cites check_vision.ps1", True),
    ("pending", "README is up to date; nothing remains", False),
    ("pending", "Remove check_vision.ps1", False),
])
def test_handoff_retains_final_measurement_command_and_pending_action(
    tmp_path: Path, key: str, value: object, expected: bool,
) -> None:
    from mengine_bench.tasks import compaction

    answers = compaction._handoff_reference(tmp_path)
    payload = json.loads(answers[-1])
    payload[key] = value
    answers[-1] = json.dumps(payload)
    result = compaction._handoff_check(tmp_path, answers)
    assert dict(result.checks)[f"answer {key}"] is expected
    assert result.passed is expected


@pytest.mark.parametrize("answer,expected", [
    ("", 0.0), ("{}", 0.0), ('{"final_vram_mib": ""}', 0.0),
    ('{"final_vram_mib": 7697}', 0.2), ('{"final_vram_mib": 7881}', 0.0),
])
def test_handoff_spill_credit_requires_a_number(tmp_path: Path, answer: str, expected: float) -> None:
    from mengine_bench.tasks import compaction

    assert compaction._handoff_check(tmp_path, [answer]).score == expected


@pytest.mark.parametrize("original,replacement,expected", [
    ('"D": 3', '"D": 3', True),
    ('"D": 3', '"D": 1', False),
    ("def find_path(grid):", 'def find_path(grid):\n    if grid == ["S..G"]:\n        return None', False),
])
def test_astar_hidden_tests_reject_wrong_door_cost_and_visible_regression(
    tmp_path: Path, original: str, replacement: str, expected: bool,
) -> None:
    from mengine_bench.tasks import gamedev

    gamedev._astar_setup(tmp_path)
    assert original in gamedev.ASTAR_REFERENCE
    (tmp_path / "pathfind.py").write_text(
        gamedev.ASTAR_REFERENCE.replace(original, replacement), encoding="utf-8",
    )
    assert gamedev._astar_check(tmp_path, [""]).passed is expected


@pytest.mark.parametrize("original,replacement,expected", [
    ("pb.x + bb.w", "pb.x + bb.w", True),
    ("pb.x + bb.w", "pb.x + ba.w", False),
    ("pb.y + bb.h", "pb.y + ba.h", False),
    ("pa.x < pb.x", "pa.x <= pb.x", False),
    ("pa.y < pb.y", "pa.y <= pb.y", False),
])
def test_ecs_hidden_collision_rejects_wrong_sizes_and_negative_edge_contacts(
    tmp_path: Path, original: str, replacement: str, expected: bool,
) -> None:
    from mengine_bench.tasks import gamedev

    gamedev._ecs_setup(tmp_path)
    gamedev._ecs_reference(tmp_path)
    collision = tmp_path / "arena_ecs/systems/collision.py"
    source = collision.read_text(encoding="utf-8")
    assert original in source
    collision.write_text(source.replace(original, replacement), encoding="utf-8")
    result = gamedev._ecs_check(tmp_path, [""])
    assert result.mandatory_ok
    assert dict(result.checks)["hidden movement"]
    assert dict(result.checks)["hidden collision"] is expected


@pytest.mark.parametrize("task_id", ["gd-astar-doors", "gd-ecs-collision-bug"])
@pytest.mark.parametrize("solved", [True, False])
def test_gamedev_stdlib_prompts_keep_accept_reject_contract(
    tmp_path: Path, task_id: str, solved: bool,
) -> None:
    from mengine_bench.tasks import gamedev

    task = next(task for task in gamedev.TASKS if task.id == task_id)
    assert all("Python standard library only" in step.prompt for step in task.steps)
    task.setup(tmp_path)
    answers = task.reference(tmp_path) if solved else [""]
    assert task.check(tmp_path, answers).passed is solved


def test_runway_uses_the_june_balance_not_the_older_line(tmp_path: Path) -> None:
    # #41: the balance file also holds May, and the close is at the end of June.
    from mengine_bench.tasks import business
    business._pnl_setup(tmp_path)
    answers = business._pnl_reference(tmp_path)
    assert business._pnl_check(tmp_path, answers).passed
    assert "31/05/2026" in (tmp_path / "finance" / "cash_balance.txt").read_text(encoding="utf-8")
    runway = json.loads((tmp_path / "runway.json").read_text(encoding="utf-8"))
    runway["runway_months"] = round(business.CASH_MAY / runway["burn_avg_3m"], 1)
    (tmp_path / "runway.json").write_text(json.dumps(runway), encoding="utf-8")
    assert not business._pnl_check(tmp_path, answers).passed
