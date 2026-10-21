"""Gold self-tests for the ported ir, longrepo and visual tasks.

Reference solution -> passes; untouched workspace + empty answers -> fails.
Visual tasks are graded on deterministic checks only, at run time too (#23).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench.core import EvalTask, run_hidden_tests
from mengine_bench.tasks import ir, longrepo
from mengine_bench.tasks import visual as visual_tasks

PART2 = (*ir.TASKS, *longrepo.TASKS, *visual_tasks.TASKS)


def solve(task: EvalTask, root: Path) -> tuple[bool, list[str]]:
    root.mkdir()
    task.setup(root)
    result = task.check(root, task.reference(root))
    return result.passed, result.failed()


@pytest.mark.parametrize("task", PART2, ids=lambda task: task.id)
def test_reference_passes_and_untouched_workspace_fails(task: EvalTask, tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    task.setup(empty)
    assert not task.check(empty, [""] * len(task.steps)).passed, f"{task.id}: gold passes an untouched workspace"
    passed, failed = solve(task, tmp_path / "solved")
    assert passed, f"{task.id}: reference fails {failed}"


def test_part2_ids_are_stable() -> None:
    by_id = {task.id: task for task in PART2}
    assert set(by_id) == {"ir-studio-wiki", "ir-server-logs", "gd-integration-repo",
                          "web-mondrian-landing", "3d-voxel-landscape"}


def test_prompts_are_english() -> None:
    for task in PART2:
        for step in task.steps:
            assert "{WS}" in step.prompt or task.id == task.id
            for word in (" voce ", " nao ", " arquivo", "Pesquise", "Crie ", "Escreva "):
                assert word not in step.prompt, f"{task.id}: untranslated {word!r}"


def test_longrepo_uses_neutral_profile() -> None:
    integration = longrepo.FILES["tests/integration/test_match_flow.py"]
    assert 'Profile("player1"' in integration and "player1.json" in integration


def test_landing_requires_new_subject_facts(tmp_path: Path) -> None:
    task = next(t for t in visual_tasks.TASKS if t.id == "web-mondrian-landing")
    passed, _ = solve(task, tmp_path / "ok")
    assert passed
    for fact in ("1930", "De Stijl", "Piet Mondrian"):
        ws = tmp_path / fact.replace(" ", "_")
        ws.mkdir()
        task.reference(ws)
        page = ws / visual_tasks.LANDING
        page.write_text(page.read_text(encoding="utf-8").replace(fact, "X"), encoding="utf-8")
        assert not task.check(ws, ["done"]).passed, f"landing without {fact!r} must fail"


def test_longrepo_untouched_tests_grant_no_correctness(tmp_path: Path) -> None:
    longrepo._setup(tmp_path)
    result = longrepo._check(tmp_path, [""])
    assert not result.passed
    assert result.score == 0
    assert result.mandatory == [("existing tests untouched", True)]


def test_longrepo_scores_hidden_scenarios_separately(tmp_path: Path) -> None:
    longrepo._setup(tmp_path)
    longrepo._reference(tmp_path)
    loader = "arena_server/config/loader.py"
    (tmp_path / loader).write_text(longrepo.FILES[loader], encoding="utf-8")
    result = longrepo._check(tmp_path, [""])
    checks = dict(result.checks)
    assert not checks["hidden config override and persistence"]
    assert not checks["hidden env float wins over file"]
    assert checks["hidden round trip keeps everything"]
    assert 0 < result.score < 1
    assert not result.passed


def test_longrepo_modified_existing_tests_fail_integrity(tmp_path: Path) -> None:
    longrepo._setup(tmp_path)
    longrepo._reference(tmp_path)
    (tmp_path / "tests/integration/test_match_flow.py").write_text("", encoding="utf-8")
    result = longrepo._check(tmp_path, [""])
    assert result.mandatory == [("existing tests untouched", False)]
    assert all(ok for _, ok in result.checks)
    assert not result.passed


def test_longrepo_fixture_already_rounds_halves_up(tmp_path: Path) -> None:
    longrepo._setup(tmp_path)
    rounding_test = """import unittest
from arena_server.economy.payout import match_payout

class PayoutContract(unittest.TestCase):
    def test_documented_half_up_examples(self):
        for raw, expected in ((1425, 1430), (1585, 1590)):
            cfg = {"win_base": raw, "loss_base": 600, "kill_bonus": 50, "event_multiplier": 1.0}
            self.assertEqual(match_payout(True, 0, cfg), expected)
"""
    ok, output = run_hidden_tests(tmp_path, rounding_test)
    assert ok, output


def test_longrepo_reference_fixes_only_two_modules(tmp_path: Path) -> None:
    longrepo._setup(tmp_path)
    answers = longrepo._reference(tmp_path)
    changed = {rel for rel, original in longrepo.FILES.items()
               if (tmp_path / rel).read_text(encoding="utf-8") != original}
    assert changed == {"arena_server/config/loader.py", "arena_server/persistence/codec.py"}
    assert longrepo._check(tmp_path, answers).passed


@pytest.mark.parametrize("task", (*ir.TASKS, *longrepo.TASKS), ids=lambda task: task.id)
def test_retrieval_and_integration_summaries_are_short_sentences(task: EvalTask) -> None:
    assert 0 < len(task.summary) <= 120
    assert task.summary.endswith(".") and task.summary.count(".") == 1
    assert "\n" not in task.summary
    assert task.provenance


@pytest.mark.parametrize("root_cause,ok", [
    ("The /data volume ran out of space, causing save failures", True),  # PR #25, issue #26
    ("Disk /data full: No space left on device", True),
    ("The data disk filled up and saves failed with no space left", True),
    # #28 B1: every storage noun and every way of saying "full" names the same cause.
    ("The /data partition filled up", True),
    ("The mount at /data reached 100% usage", True),
    ("Filesystem capacity exhausted on the data volume", True),
    ("The storage was exhausted by old backups", True),
    ("The server ran out of disk on /data", True),
    ("Saves hit ENOSPC on /data", True),
    ("The host was out of storage space", True),
    ("The /data mount was at 100.0% capacity", True),
    ("The disk was not full; a bad RCON password locked the server", False),
    ("Watchdog killed the server (exit code 137); the disk wasn't full", False),
    ("Watchdog restarted the unresponsive server", False),
    ("RCON auth failed from a bad password", False),
])
def test_logs_root_cause_accepts_every_out_of_space_wording(tmp_path: Path, root_cause: str, ok: bool) -> None:
    from mengine_bench.tasks import ir

    ir._logs_setup(tmp_path)
    answers = ir._logs_reference(tmp_path)
    incident = json.loads((tmp_path / "incident.json").read_text(encoding="utf-8"))
    incident["root_cause"] = root_cause
    (tmp_path / "incident.json").write_text(json.dumps(incident), encoding="utf-8")
    assert ir._logs_check(tmp_path, answers).passed is ok
