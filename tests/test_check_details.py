"""A failed check says what it expected and what it received, so a person can read why (#82)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench import anchors, catalog, cli
from mengine_bench.core import CheckResult, run_hidden_tests, saw, write
from mengine_bench.judge import TaskVerdict
from mengine_bench.report import render_summary
from mengine_bench.run_command import _detail
from mengine_bench.runner.task_run import TaskRunRecord
from mengine_bench.tasks import business, gamedev


def _by_id(task_id: str):
    return next(task for task in catalog.all_tasks() if task.id == task_id)


def _solved(task_id: str, ws: Path) -> list[str]:
    task = _by_id(task_id)
    task.setup(ws)
    return task.reference(ws)


def test_a_detail_is_kept_only_for_a_failed_check() -> None:
    result = CheckResult()
    result.add("right", True, "not shown")
    result.add("wrong", False, saw(3, 2))
    assert result.details == {"wrong": "expected 2, received 3"}


def test_a_long_received_value_is_cut() -> None:
    assert len(saw("x" * 5000, 1)) <= 300


@pytest.mark.parametrize(("task_id", "edit", "check", "shown"), [
    ("ir-server-logs", {"minutes_down": 1.0}, "minutes down", "received 1.0"),
    ("bo-reconcile", {"unpaid": ["INV-1"]}, "unpaid invoices", "received ['INV-1']"),
    ("ds-ab-playtest", {"p_value": 0.5}, "the gain is significant", "received 0.5"),
])
def test_a_wrong_value_in_a_file_is_named(tmp_path: Path, task_id: str, edit: dict[str, object], check: str,
                                          shown: str) -> None:
    answers = _solved(task_id, tmp_path)
    path = tmp_path / "result.json"
    path.write_text(json.dumps({**json.loads(path.read_text(encoding="utf-8")), **edit}), encoding="utf-8")
    result = _by_id(task_id).check(tmp_path, answers)
    assert check in result.failed() and "expected" in result.details[check] and shown in result.details[check]


def test_a_wrong_answer_read_from_the_chart_is_named(tmp_path: Path) -> None:
    write(tmp_path, "result.json", json.dumps({"top_gpu": "4090", "top_tps": 180, "bottom_gpu": "4090", "ratio": 6.0}))
    result = _by_id("vis-chart").check(tmp_path, ["any reply"])
    assert "received '4090'" in result.details["GPU with the highest TPS at 256k"]


def test_every_failed_check_of_the_data_tasks_explains_itself(tmp_path: Path) -> None:
    for task_id in ("ds-ab-playtest", "bo-pnl-runway", "bo-reconcile", "ds-sql-funnel", "ir-server-logs",
                    "ir-studio-wiki", "lc-changelog", "vis-chart", "cmp-handoff"):
        ws = tmp_path / task_id
        ws.mkdir()
        task = _by_id(task_id)
        task.setup(ws)
        result = task.check(ws, [""] * len(task.steps))
        unexplained = [name for name, ok in result.checks if not ok and name not in result.details]
        assert not unexplained, (task_id, unexplained)


def test_the_funnel_names_the_wrong_platform_and_shows_the_count(tmp_path: Path) -> None:
    answers = _solved("ds-sql-funnel", tmp_path)
    path = tmp_path / "result.json"
    got = json.loads(path.read_text(encoding="utf-8"))
    got["funnel"]["pc"]["tutorial_complete"] = 1
    path.write_text(json.dumps(got), encoding="utf-8")
    result = _by_id("ds-sql-funnel").check(tmp_path, answers)
    assert result.failed() == ["players per step on pc"]
    assert "'tutorial_complete': 1" in result.details["players per step on pc"]


def test_a_hidden_test_failure_reads_as_the_assertion_not_as_a_count(tmp_path: Path) -> None:
    gold = ("import unittest\n\nclass T(unittest.TestCase):\n    def test_doors(self):\n"
            "        self.assertEqual(7, 5, 'walked through the door')\n")
    ok, detail = run_hidden_tests(tmp_path, gold)
    assert not ok and "test_doors" in detail and "7 != 5" in detail and "Ran 1 test" not in detail


def _summary(*checks: dict[str, object]) -> str:
    return render_summary({"bench_version": "1.4.0", "date": "d", "agent": {"name": "a", "model": "m"},
                           "totals": {"score": 1.0, "correct": 1.0, "solved": 0, "total": 1, "judge": 1.0, "time_s": 1.0},
                           "tasks": [{"id": "t", "status": "ok", "flags": [], "c": 0.5, "agent_s": 1.0,
                                      "checks": list(checks)}]})


def test_the_summary_lists_failed_checks_with_their_reason() -> None:
    summary = _summary({"name": "good", "ok": True}, {"name": "bad", "ok": False, "detail": "expected 2, received 3"},
                       {"name": "older bundle", "ok": False})
    assert "## Failed checks" in summary
    assert "- `t` bad: expected 2, received 3\n" in summary and "- `t` older bundle\n" in summary
    assert "good" not in summary


def test_a_clean_run_has_no_failed_section() -> None:
    assert "Failed checks" not in _summary({"name": "good", "ok": True})


def test_a_detail_cannot_break_the_summary_lines() -> None:
    summary = _summary({"name": "bad", "ok": False, "detail": "expected 'a', received 'b\nc'"})
    assert "- `t` bad: expected 'a', received 'b c'\n" in summary


def test_result_json_keeps_the_detail_only_on_the_failure() -> None:
    check = CheckResult()
    check.add("good", True)
    check.add("bad", False, "expected 2, received 3")
    checks = _detail(_by_id("vis-chart"), TaskRunRecord(task_id="vis-chart", check=check))["checks"]
    assert checks == [{"name": "good", "ok": True, "mandatory": False},
                      {"name": "bad", "ok": False, "mandatory": False, "detail": "expected 2, received 3"}]


BFS = '''from collections import deque


def find_path(grid):
    cells = {(r, c): ch for r, row in enumerate(grid) for c, ch in enumerate(row)}
    start = next(k for k, v in cells.items() if v == "S")
    prev = {start: None}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        if cells[cell] == "G":
            path = []
            while cell is not None:
                path.append(cell)
                cell = prev[cell]
            return path[::-1]
        r, c = cell
        for nxt in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if cells.get(nxt, "#") != "#" and nxt not in prev:
                prev[nxt] = cell
                queue.append(nxt)
    return None
'''


def test_astar_splits_into_cases_a_person_can_read(tmp_path: Path) -> None:
    write(tmp_path, "pathfind.py", gamedev.ASTAR_REFERENCE)
    result = gamedev._astar_check(tmp_path, ["done"])
    assert [name for name, _ in result.checks] == [f"hidden {case}" for case, _ in gamedev.ASTAR_CASES]
    assert len(result.checks) >= 3 and result.passed


def test_fewest_steps_fails_only_the_door_cases(tmp_path: Path) -> None:
    write(tmp_path, "pathfind.py", BFS)
    result = gamedev._astar_check(tmp_path, ["done"])
    failed = result.failed()
    assert "hidden walks around a door when that is cheaper" in failed
    assert "hidden returns None when G is unreachable" not in failed and "hidden plain floor" not in failed
    assert 0.0 < result.score < 1.0
    assert "!=" in result.details["hidden walks around a door when that is cheaper"]


def test_a_stub_earns_nothing_on_astar(tmp_path: Path) -> None:
    write(tmp_path, "pathfind.py", gamedev.ASTAR_STUB)
    assert gamedev._astar_check(tmp_path, ["done"]).score == 0.0


def test_reconcile_keeps_its_rules_in_a_file_the_agent_must_read(tmp_path: Path) -> None:
    task = _by_id("bo-reconcile")
    task.setup(tmp_path)
    rules = (tmp_path / "backoffice/README.md").read_text(encoding="utf-8")
    assert "exclusive" in rules and "fees" in rules
    prompt = task.steps[0].prompt
    # #98: the brief points at the folder and its notes; the rules themselves stay in the file.
    assert "{WS}/backoffice" in prompt and "notes" in prompt and "exclusive" not in prompt and "fees" not in prompt


def test_reconcile_catches_a_duplicate_also_listed_as_mismatched(tmp_path: Path) -> None:
    answers = _solved("bo-reconcile", tmp_path)
    path = tmp_path / "result.json"
    got = json.loads(path.read_text(encoding="utf-8"))
    invoice = business.RECON["duplicated"][0]
    got["mismatched"].append({"id": invoice, "invoiced": 1.0, "paid": 2.0})
    path.write_text(json.dumps(got), encoding="utf-8")
    result = _by_id("bo-reconcile").check(tmp_path, answers)
    assert "mismatched amounts" in result.failed() and invoice in result.details["mismatched amounts"]


@pytest.mark.parametrize(("task_id", "hint"), [
    ("gd-astar-doors", "not just fewest steps"),
    ("lc-changelog", "beware"),
])
def test_prompts_do_not_hand_over_the_trap(task_id: str, hint: str) -> None:
    assert hint not in _by_id(task_id).steps[0].prompt


class _Votes:
    """A RubricJudge stand-in: the reference earns `solved`, the stub earns `stub`."""

    def __init__(self, solved: int, stub: int) -> None:
        self.solved, self.stub = solved, stub
        self.seen: list[tuple[str, bool]] = []

    def grade(self, context, workdir) -> TaskVerdict:
        done = any(answer.strip() for answer in context.answers)
        self.seen.append((context.task_id, done))
        return TaskVerdict(score=self.solved if done else self.stub, rationale="r")


def test_anchors_vote_the_reference_and_the_stub_of_each_task(tmp_path: Path) -> None:
    votes = _Votes(solved=70, stub=5)
    report = anchors.vote_anchors(votes, tmp_path)
    assert votes.seen == [(task_id, done) for task_id in anchors.ANCHOR_TASKS for done in (True, False)]
    assert report.ok and all(row.gap == 65 for row in report.rows)


def test_a_judge_that_cannot_tell_them_apart_fails_the_anchors(tmp_path: Path) -> None:
    assert not anchors.vote_anchors(_Votes(solved=60, stub=50), tmp_path).ok


def test_a_task_without_a_vote_fails_the_anchors(tmp_path: Path) -> None:
    class NoVote:
        def grade(self, context, workdir) -> TaskVerdict:
            return TaskVerdict(score=None, rationale="", errors=("attempt 0: no reply",))

    assert not anchors.vote_anchors(NoVote(), tmp_path).ok


def test_the_anchor_command_reports_and_exits_by_the_result(monkeypatch: pytest.MonkeyPatch,
                                                            capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(cli, "RubricJudge", lambda agent: _Votes(solved=60, stub=50))
    assert cli.main(["judge-anchors"]) == 1
    out = capsys.readouterr().out
    assert "FAILED" in out and "gd-astar-doors" in out
