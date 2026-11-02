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


@pytest.mark.parametrize("wrong", ["rng_only", "constant", "crash", "test_edit"])
def test_desync_rejects_partial_or_fake_fix(wrong: str, tmp_path: Path) -> None:
    from mengine_bench.candidates.hard_context import SIM_BUGGY
    task = next(t for t in TASKS if t.id == "gd-lockstep-desync")
    task.setup(tmp_path)
    task.reference(tmp_path)
    path = tmp_path / "lockstep/sim.py"
    if wrong == "rng_only":
        path.write_text(SIM_BUGGY.replace("random.choice(list(enemies))", "self.rng.choice(list(enemies))"))
    if wrong == "constant":
        path.write_text("def simulate(seed, ticks): return 'constant'\n")
    if wrong == "crash":
        path.write_text("raise RuntimeError('broken')\n")
    if wrong == "test_edit":
        (tmp_path / "tests/test_replay.py").write_text("")
    assert not task.check(tmp_path, [""]).passed


@pytest.mark.parametrize("field,wrong", [
    ("preco_assento_mes", 150), ("preco_assento_mes", 180),
    ("desconto_volume_pct", 15), ("custo_anual", 37 * 165 * 12 * 0.85),
    ("custo_anual", 37 * 165 * 12 * 0.9),
])
def test_contract_rejects_wrong_terms(field: str, wrong: float, tmp_path: Path) -> None:
    task = next(t for t in TASKS if t.id == "lc-contract")
    task.reference(tmp_path)
    path = tmp_path / "result.json"
    outcome = json.loads(path.read_text())
    outcome[field] = wrong
    path.write_text(json.dumps(outcome))
    assert not task.check(tmp_path, [""]).passed


def test_contract_accepts_common_formats(tmp_path: Path) -> None:
    task = next(t for t in TASKS if t.id == "lc-contract")
    (tmp_path / "result.json").write_text(json.dumps({
        "preco_assento_mes": "R$ 165,00", "desconto_volume_pct": "0.10",
        "custo_anual": "R$ 62.637,30",
    }))
    assert task.check(tmp_path, [""]).passed


def test_candidate_ids() -> None:
    assert {t.id for t in TASKS} == {"bo-safe-conversion", "gd-lockstep-desync", "lc-contract"}
