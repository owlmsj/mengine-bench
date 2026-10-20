"""Gold self-tests for the ported ir, longrepo and visual tasks.

Reference solution -> passes; untouched workspace + empty answers -> fails.
Visual tasks are graded on deterministic checks only, at run time too (#23).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench.core import EvalTask
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
    assert set(by_id) == {"ir-studio-wiki", "ir-server-logs", "ir-web-facts", "gd-integration-repo",
                          "web-mondrian-landing", "3d-voxel-landscape"}


def test_prompts_are_english() -> None:
    for task in PART2:
        for step in task.steps:
            assert "{WS}" in step.prompt or task.id == "ir-web-facts", task.id
            for word in (" voce ", " nao ", " arquivo", "Pesquise", "Crie ", "Escreva "):
                assert word not in step.prompt, f"{task.id}: untranslated {word!r}"


def test_web_facts_gold_uses_neutral_facts() -> None:
    task = next(t for t in ir.TASKS if t.id == "ir-web-facts")
    answers = task.reference(Path("."))
    assert task.check(Path("."), answers).passed
    payload = json.loads(answers[0])
    payload["sources"] = payload["sources"][:2]
    assert not task.check(Path("."), [json.dumps(payload)]).passed, "fewer than 3 source URLs must fail"
    wrong = answers[0].replace('"tux"', '"penguin"')
    assert not task.check(Path("."), [wrong]).passed


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
