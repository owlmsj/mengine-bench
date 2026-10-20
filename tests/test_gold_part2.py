"""Gold self-tests for the ported ir, longrepo and visual tasks.

Reference solution -> passes; untouched workspace + empty answers -> fails.
Visual tasks are graded on their deterministic checks only here: CI has no
browser and no judge, and the gold must not depend on either.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from mengine_bench import visual
from mengine_bench.core import FAST, FULL, EvalTask
from mengine_bench.tasks import ir, longrepo
from mengine_bench.tasks import visual as visual_tasks

PART2 = (*ir.TASKS, *longrepo.TASKS, *visual_tasks.TASKS)
PAR_FROM_RUNS = {"gd-integration-repo": 89.0, "web-mondrian-landing": 345.0, "3d-voxel-landscape": 295.0}


@pytest.fixture
def no_browser(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(visual, "RENDER", lambda html, png: visual.NO_BROWSER)


def solve(task: EvalTask, root: Path) -> tuple[bool, list[str]]:
    root.mkdir()
    task.setup(root)
    result = task.check(root, task.reference(root))
    return result.passed, result.failed()


@pytest.mark.usefixtures("no_browser")
@pytest.mark.parametrize("task", PART2, ids=lambda task: task.id)
def test_reference_passes_and_untouched_workspace_fails(task: EvalTask, tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    task.setup(empty)
    assert not task.check(empty, [""] * len(task.steps)).passed, f"{task.id}: gold passes an untouched workspace"
    passed, failed = solve(task, tmp_path / "solved")
    assert passed, f"{task.id}: reference fails {failed}"


def test_part2_ids_suites_and_weights_are_stable() -> None:
    by_id = {task.id: task for task in PART2}
    assert set(by_id) == {"ir-studio-wiki", "ir-server-logs", "gd-integration-repo",
                          "web-mondrian-landing", "3d-voxel-landscape"}
    fast = {task.id for task in PART2 if FAST in task.suites}
    assert fast == {"ir-studio-wiki", "gd-integration-repo", "web-mondrian-landing", "3d-voxel-landscape"}
    assert all(FULL in task.suites for task in PART2)
    assert {tid for tid, task in by_id.items() if task.weight == 2} == set(PAR_FROM_RUNS)
    for tid, par in PAR_FROM_RUNS.items():
        assert by_id[tid].par_s == par


def test_prompts_are_english() -> None:
    for task in PART2:
        for step in task.steps:
            assert "{WS}" in step.prompt or task.id == task.id
            for word in (" voce ", " nao ", " arquivo", "Pesquise", "Crie ", "Escreva "):
                assert word not in step.prompt, f"{task.id}: untranslated {word!r}"


def test_longrepo_uses_neutral_profile() -> None:
    integration = longrepo.FILES["tests/integration/test_match_flow.py"]
    assert 'Profile("player1"' in integration and "player1.json" in integration


@pytest.mark.usefixtures("no_browser")
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
    assert not checks["hidden visible scenario"]
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
