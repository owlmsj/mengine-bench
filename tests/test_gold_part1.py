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
    "ue-packaged-bug",
    "ds-ab-playtest",
    "bo-pnl-runway",
    "bo-reconcile",
    "ds-sql-funnel",
    "lc-changelog",
    "vis-chart",
    "cmp-handoff",
}


def _edit_result(ws: Path, **fields: object) -> None:
    """Change what the reference delivered: every eval hands over its facts in result.json (#98)."""
    path = ws / "result.json"
    path.write_text(json.dumps({**json.loads(path.read_text(encoding="utf-8")), **fields}), encoding="utf-8")


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



@pytest.mark.parametrize("invoice_id", ["INV-1021", "INV-1036"])
@pytest.mark.parametrize("wrong_paid", [0, "not a number", None])
def test_reconcile_rejects_wrong_paid(
    tmp_path: Path, invoice_id: str, wrong_paid: object,
) -> None:
    from mengine_bench.tasks import business

    business._recon_setup(tmp_path)
    business._recon_reference(tmp_path)
    output = tmp_path / "result.json"
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
    output = tmp_path / "result.json"
    reconciliation = json.loads(output.read_text(encoding="utf-8"))
    for mismatch in reconciliation["mismatched"]:
        mismatch["paid"] += delta
    output.write_text(json.dumps(reconciliation), encoding="utf-8")
    assert business._recon_check(tmp_path, [""]).passed is expected


@pytest.mark.parametrize("case,expected", [
    ("strings", True), ("objects", True), ("mixed", True), ("duplicate_mismatch", False),
    ("non_object_mismatch", False), ("wrong_id", False), ("missing_id", False),
    ("repeated_id", False), ("non_list", False),
])
def test_reconcile_id_forms_and_exclusive_categories(tmp_path: Path, case: str, expected: bool) -> None:
    from mengine_bench.tasks import business

    business._recon_reference(tmp_path)
    output = tmp_path / "result.json"
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
    _edit_result(tmp_path, **{key: wrong})
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
    _edit_result(tmp_path, **{key: valid})
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
    assert json.loads((tmp_path / "result.json").read_text(encoding="utf-8")) == {
        "funnel": {"pc": {"install": 2, "tutorial_complete": 2, "first_match": 1, "purchase": 1},
                   "steamdeck": {"install": 1, "tutorial_complete": 1, "first_match": 1, "purchase": 1}},
        "biggest_drop": {"pc": "first_match", "steamdeck": "tutorial_complete"},
    }


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
    # #98: a yes in any common writing is the same decision; a no or a bare 1 is not.
    ("ship_b", "true", True), ("ship_b", "yes", True), ("ship_b", 1, False),
    ("ship_b", False, False), ("ship_b", "no", False),
])
def test_ab_counts_stay_exact_and_the_decision_must_be_yes(
    tmp_path: Path, key: str, value: object, expected: bool,
) -> None:
    from mengine_bench.tasks import business

    business._ab_reference(tmp_path)
    _edit_result(tmp_path, **{key: value})
    assert business._ab_check(tmp_path, [""]).passed is expected


@pytest.mark.parametrize("line", ["revenue", "gross_margin_pct", "ebitda"])
@pytest.mark.parametrize("case,expected", [
    # #98: the csv became a month-to-value map, so the order of the months is no longer part of the answer.
    ("reference", True), ("reordered", True), ("duplicate", False), ("missing", False),
])
def test_pnl_checks_every_month_of_every_line(tmp_path: Path, line: str, case: str, expected: bool) -> None:
    from mengine_bench.tasks import business

    business._pnl_reference(tmp_path)
    series = json.loads((tmp_path / "result.json").read_text(encoding="utf-8"))[line]
    months = list(series)
    if case == "reordered":
        series = dict(reversed(series.items()))
    if case == "duplicate":
        series[months[1]] = series[months[0]]
    if case == "missing":
        del series[months[-1]]
    _edit_result(tmp_path, **{line: series})
    result = business._pnl_check(tmp_path, [""])
    assert dict(result.checks)[f"{line} per month"] is expected
    assert result.passed is expected


@pytest.mark.parametrize("count,expected", [
    ("{count}", True), ("{count}.0", True), ("{count}.1", False), ("0", False), ("nan", False),
])
def test_funnel_accepts_only_exact_numeric_users(tmp_path: Path, count: str, expected: bool) -> None:
    from mengine_bench.tasks import funnel

    funnel._funnel_reference(tmp_path)
    counts = json.loads((tmp_path / "result.json").read_text(encoding="utf-8"))["funnel"]
    counts["pc"]["install"] = count.format(count=counts["pc"]["install"])
    _edit_result(tmp_path, funnel=counts)
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

    answers = context._changelog_reference(tmp_path)
    build = json.loads((tmp_path / "result.json").read_text(encoding="utf-8"))[key]
    _edit_result(tmp_path, **{key: form.format(build)})
    assert context._changelog_check(tmp_path, answers).passed is expected


@pytest.mark.parametrize("key,value,expected", [
    ("top_gpu", " h200 ", True), ("bottom_gpu", " 40 90 ", True),
    ("top_gpu", "NVIDIA H200", True), ("bottom_gpu", "Nvidia 4090 GPU", True),
    ("top_gpu", "NOT-H200: H100", False), ("bottom_gpu", "NOT-4090: H100", False),
    ("top_gpu", "H2000", False), ("bottom_gpu", "H100", False),
    ("ratio", 6.0, True), ("ratio", "5.8", True), ("ratio", 7.3, False),
    ("ratio", 4.7, False), ("ratio", "nan", False),
])
def test_chart_normalizes_names_and_reads_the_ratio_with_a_margin(
    tmp_path: Path, key: str, value: object, expected: bool,
) -> None:
    from mengine_bench.tasks import context

    answers = context._chart_reference(tmp_path)
    _edit_result(tmp_path, **{key: value})
    assert context._chart_check(tmp_path, answers).passed is expected


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
    _edit_result(tmp_path, **{key: value})
    result = compaction._handoff_check(tmp_path, answers)
    assert dict(result.checks)[f"answer {key}"] is expected
    assert result.passed is expected


@pytest.mark.parametrize("answer,expected", [
    ("", 0.0), ("{}", 0.0), ('{"final_vram_mib": ""}', 0.0),
    ('{"final_vram_mib": 7697}', 2 / 11), ('{"final_vram_mib": 7881}', 0.0),
])
def test_handoff_spill_credit_requires_a_number(tmp_path: Path, answer: str, expected: float) -> None:
    from mengine_bench.tasks import compaction

    (tmp_path / "result.json").write_text(answer, encoding="utf-8")
    assert compaction._handoff_check(tmp_path, ["any reply"]).score == expected


def test_runway_uses_the_june_balance_not_the_older_line(tmp_path: Path) -> None:
    # #41: the balance file also holds May, and the close is at the end of June.
    from mengine_bench.tasks import business
    business._pnl_setup(tmp_path)
    answers = business._pnl_reference(tmp_path)
    assert business._pnl_check(tmp_path, answers).passed
    assert "31/05/2026" in (tmp_path / "finance" / "cash_balance.txt").read_text(encoding="utf-8")
    burn = json.loads((tmp_path / "result.json").read_text(encoding="utf-8"))["burn"]
    _edit_result(tmp_path, runway_months=round(business.CASH_MAY / burn, 1))
    assert not business._pnl_check(tmp_path, answers).passed
