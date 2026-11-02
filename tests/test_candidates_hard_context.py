"""Candidate gold regression tests (#127)."""
import json
from pathlib import Path

import pytest

from mengine_bench.candidates.hard_context import TASKS
from mengine_bench.catalog import all_tasks


@pytest.mark.parametrize("task", TASKS, ids=lambda task: task.id)
def test_reference_and_untouched(task, tmp_path: Path) -> None:
    task.setup(tmp_path)
    assert not task.check(tmp_path, [""]).passed
    assert task.check(tmp_path, task.reference(tmp_path)).passed


def test_candidates_not_in_catalog() -> None:
    assert not {task.id for task in TASKS} & {task.id for task in all_tasks()}


@pytest.mark.parametrize("field", ["preco_por_acao", "novas_acoes_pool", "acoes_safe",
                                   "acoes_investidor_novo", "participacao_fundadores_pct"])
def test_safe_rejects_wrong_outcome(field: str, tmp_path: Path) -> None:
    task = TASKS[0]
    task.setup(tmp_path)
    task.reference(tmp_path)
    path = tmp_path / "result.json"
    outcome = json.loads(path.read_text())
    outcome[field] = {"Investor A": 375000} if field == "acoes_safe" else outcome[field] * 0.9
    path.write_text(json.dumps(outcome))
    assert not task.check(tmp_path, [""]).passed


def test_safe_accepts_rounding_and_fraction(tmp_path: Path) -> None:
    task = TASKS[0]
    task.reference(tmp_path)
    path = tmp_path / "result.json"
    outcome = json.loads(path.read_text())
    outcome["preco_por_acao"] = f'{outcome["preco_por_acao"]:.2f}'
    outcome["participacao_fundadores_pct"] /= 100
    path.write_text(json.dumps(outcome))
    assert task.check(tmp_path, [""]).passed
