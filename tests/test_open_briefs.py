"""#98: the evals state a problem and an outcome. Any valid route and format passes, a wrong answer does not."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.checkpoints import reached_checkpoints
from mengine_bench.core import Checkpoint, is_no, is_yes, near, near_share, number
from mengine_bench.judge import JUDGE_SYSTEM_PROMPT
from mengine_bench.report import _checkpoint_lines
from mengine_bench.runner.task_run import TIME_LIMIT_NOTE
from mengine_bench.tasks import business, context, funnel, ir


@pytest.mark.parametrize(("text", "expected"), [
    (9.4, 9.4), ("9.4", 9.4), ("9,4", 9.4), ("9.4 months", 9.4), ("R$ 1.234,56", 1234.56), ("1,234.56", 1234.56),
    ("-197.288,23", -197288.23), ("1.234.567", 1234567.0), ("1,234", 1234.0), ("38%", 38.0),
])
def test_number_reads_common_writings(text: object, expected: float) -> None:
    assert number(text) == expected


@pytest.mark.parametrize("text", ["10 or 12", "ten", "", None, True, float("nan")])
def test_number_refuses_what_is_not_one_answer(text: object) -> None:
    assert number(text) is None


@pytest.mark.parametrize("value", [0.38, 38, "38%", "38.0 %", "0.38"])
def test_a_share_may_come_in_any_unit(value: object) -> None:
    assert near_share(value, 0.38, 2e-3)


@pytest.mark.parametrize("value", [0.45, 45, "45%", "0.38%", None])
def test_a_wrong_share_fails_in_any_unit(value: object) -> None:
    assert not near_share(value, 0.38, 2e-3)


def test_yes_and_no_are_not_each_other() -> None:
    assert is_yes(True) and is_yes("yes") and not is_yes(False) and not is_yes("no") and not is_yes(None)
    assert is_no(False) and is_no("No") and not is_no(True) and not is_no(None)


def _deliver(ws: Path, payload: object) -> None:
    (ws / "result.json").write_text(json.dumps(payload), encoding="utf-8")


def _ab_answer() -> dict[str, object]:
    exp = business._ab_expected()
    return {"ship_b": True, "sessions_a": exp["sessions_a"], "sessions_b": exp["sessions_b"], "completion_rate_a": exp["rate_a"],
            "completion_rate_b": exp["rate_b"], "p_value": exp["p_value"]}


def test_the_ab_decision_accepts_any_valid_test_and_units(tmp_path: Path) -> None:
    exp = business._ab_expected()
    _deliver(tmp_path, {**_ab_answer(), "completion_rate_a": f"{100 * float(exp['rate_a']):.2f}%", "completion_rate_b": 100 * float(exp["rate_b"]),
                        "p_value": 0.0003, "ship_b": "yes"})
    assert business._ab_check(tmp_path, ["any reply"]).passed


@pytest.mark.parametrize(("key", "bad"), [("sessions_a", 930), ("p_value", 0.2), ("ship_b", False), ("completion_rate_b", 0.41)])
def test_the_ab_decision_still_fails_a_wrong_answer(tmp_path: Path, key: str, bad: object) -> None:
    _deliver(tmp_path, {**_ab_answer(), key: bad})
    assert not business._ab_check(tmp_path, [""]).passed


def test_a_correct_answer_in_the_chat_alone_earns_nothing(tmp_path: Path) -> None:
    assert not business._ab_check(tmp_path, [json.dumps(_ab_answer())]).passed


def test_the_funnel_takes_either_shape_and_rejects_a_wrong_count(tmp_path: Path) -> None:
    rows = funnel._funnel_expected()
    drops = funnel._biggest_drops()
    as_lists = {platform: [{"step": row[1], "users": row[2]} for row in rows if row[0] == platform] for platform in drops}
    _deliver(tmp_path, {"funnel": as_lists, "biggest_drop": drops})
    assert funnel._funnel_check(tmp_path, [""]).passed
    as_lists["pc"][1]["users"] += 1
    _deliver(tmp_path, {"funnel": as_lists, "biggest_drop": drops})
    assert not funnel._funnel_check(tmp_path, [""]).passed


# What the briefs must not hand over: the method (#98).
HANDED_OVER = r"z-test|pooled|erfc|\bCTE\b|Dijkstra|A\*|unittest|Reply ONLY|summarize in|separator ;|1\.234,56|Do not ask|is_test"


@pytest.mark.parametrize("task", catalog.all_tasks(), ids=lambda task: task.id)
def test_no_brief_dictates_the_method(task: catalog.EvalTask) -> None:
    prompts = " ".join(step.prompt for step in task.steps)
    assert not re.search(HANDED_OVER, prompts), prompts


@pytest.mark.parametrize("task", catalog.all_tasks(), ids=lambda task: task.id)
def test_every_eval_declares_checkpoints(task: catalog.EvalTask) -> None:
    assert task.checkpoints, task.id
    for mark in task.checkpoints:
        re.compile(mark.pattern)


def test_checkpoints_find_tool_calls_only_and_in_order() -> None:
    marks = (Checkpoint("read the data", r"playtest_ab"), Checkpoint("recorded", r"result\.json"), Checkpoint("never", r"nothing_like_this"))
    stream = "\n".join([
        json.dumps({"type": "item.started", "item": {"type": "command_execution", "command": "cat result.json"}}),
        json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "I will read playtest_ab"}}),
        json.dumps({"type": "item.completed", "item": {"type": "command_execution", "command": "cat playtest_ab.csv"}}),
        json.dumps({"type": "item.completed", "item": {"type": "file_change", "changes": [{"path": "result.json"}]}}),
    ])
    assert reached_checkpoints(marks, [stream]) == [{"name": "read the data", "call": 1}, {"name": "recorded", "call": 2},
                                                    {"name": "never", "call": None}]


def test_checkpoints_stay_out_of_the_judge_and_show_in_the_summary() -> None:
    assert "checkpoint" not in JUDGE_SYSTEM_PROMPT.lower()
    task = {"id": "t", "status": "ok", "flags": [], "c": 1.0, "judge": None, "agent_s": 1.0, "checks": [], "tokens": None,
            "checkpoints": [{"name": "read the data", "call": 2}, {"name": "tested it", "call": None}]}
    summary = "\n".join(_checkpoint_lines([task]))
    assert "read the data (call 2)" in summary and "not seen: tested it" in summary


def test_format_is_never_a_defect_and_any_route_can_earn_full_marks() -> None:
    assert "rubric 2.5" in JUDGE_SYSTEM_PROMPT
    assert "any valid route can earn full marks" in JUDGE_SYSTEM_PROMPT
    assert "are never defects" in JUDGE_SYSTEM_PROMPT
    assert "a code fence around" not in JUDGE_SYSTEM_PROMPT


@pytest.mark.parametrize(("text", "expected"), [
    ("1.98e-4", 1.98e-4), ("2.0E-4", 2e-4), ("(197288.23)", -197288.23), ("\u2212197288.23", -197288.23), ("R$ (1.234,56)", -1234.56),
])
def test_number_reads_scientific_and_negative_writings(text: str, expected: float) -> None:
    assert number(text) == pytest.approx(expected)


def test_brazilian_thousands_count_only_when_the_value_fits() -> None:
    assert near("182.000", 182000, 1) and near("182.000", 182, 1) and not near("182.000", 500, 1)


@pytest.mark.parametrize("key", ["players", "users", "count"])
def test_the_funnel_reads_the_count_under_any_plain_name(tmp_path: Path, key: str) -> None:
    rows = funnel._funnel_expected()
    flat = [{"platform": row[0], "step": row[1], key: row[2]} for row in rows]
    _deliver(tmp_path, {"funnel": flat, "biggest_drop": funnel._biggest_drops()})
    assert funnel._funnel_check(tmp_path, [""]).passed


@pytest.mark.parametrize(("value", "ok"), [(99.92, True), ("99.92%", True), (0.99917, True), (99.917, True), (99.9, False), (99.5, False)])
def test_availability_takes_rounding_and_units_not_a_wrong_value(tmp_path: Path, value: object, ok: bool) -> None:
    good = {**ir._logs_expected(), "root_cause": "/data disk full"}
    _deliver(tmp_path, {**good, "availability_june_pct": value})
    assert ir._logs_check(tmp_path, [""]).passed is ok


@pytest.mark.parametrize(("value", "ok"), [("35 min 49 s", True), ("00:35:49", True), (36, True), (35.82, True), (34, False), ("1 h", False)])
def test_the_outage_length_takes_common_writings(tmp_path: Path, value: object, ok: bool) -> None:
    good = {**ir._logs_expected(), "root_cause": "/data disk full"}
    _deliver(tmp_path, {**good, "minutes_down": value})
    assert ir._logs_check(tmp_path, [""]).passed is ok


def test_the_changelog_takes_a_full_timestamp_and_a_titled_approver(tmp_path: Path) -> None:
    gold = context._changelog()[1]
    context_ws = tmp_path
    _deliver(context_ws, {**gold, "builds_between": 162, "revert_date": f"{gold['revert_date']}T00:00:00", "revert_approver": f"{gold['revert_approver']} (producer)"})
    assert context._changelog_check(context_ws, [""]).passed


def test_every_prompt_caps_the_revisions_and_says_time_counts() -> None:
    assert "at most 2 rounds of revision" in TIME_LIMIT_NOTE and "Time counts" in TIME_LIMIT_NOTE
