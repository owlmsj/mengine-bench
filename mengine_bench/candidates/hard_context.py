"""Offline ports of the private suite, held outside the catalog (#127)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import CheckResult, EvalTask, Step, near, near_share, read_json, write

CAP_TABLE = [("Fundador A", "common", 4_200_000), ("Fundadora B", "common", 3_300_000),
             ("Employee options exercised", "common", 250_000), ("Opcoes em aberto", "options", 850_000),
             ("Pool nao alocado", "pool", 400_000)]
SAFES = [("Investor A", 500_000, 12_000_000, 0.20), ("Investor B", 1_200_000, 16_000_000, 0.15),
         ("Investor C", 150_000, 8_000_000, 0.25)]
PRE_MONEY, NEW_MONEY, POOL_TARGET = 40_000_000.0, 8_000_000.0, 0.12


def _safe_solution() -> dict[str, object]:
    c0 = sum(n for _, _, n in CAP_TABLE)
    unissued = next(n for _, kind, n in CAP_TABLE if kind == "pool")
    x = 0.0
    safe_shares: dict[str, float] = {}
    price = PRE_MONEY / c0
    for _ in range(500):
        safe_shares = {name: amount / min(cap / c0, price * (1 - disc)) for name, amount, cap, disc in SAFES}
        s = sum(safe_shares.values())
        price = PRE_MONEY / (c0 + x + s)
        new = NEW_MONEY / price
        post = c0 + x + s + new
        x = max(0.0, POOL_TARGET * post - unissued)
    founders = sum(n for name, _, n in CAP_TABLE if name.startswith("Fundador"))
    return {"preco_por_acao": price, "novas_acoes_pool": x, "acoes_safe": safe_shares,
            "acoes_investidor_novo": NEW_MONEY / price, "post_money_fd": post,
            "participacao_fundadores_pct": founders / post * 100}


def _brl_int(value: float) -> str:
    return f"{value:,.0f}".replace(",", ".")


def _safe_setup(ws: Path) -> None:
    write(ws, "rodada/cap_table.csv", "titular,classe,acoes\n" + "".join(f"{a},{b},{c}\n" for a, b, c in CAP_TABLE))
    write(ws, "rodada/safes.csv", "investidor,valor,valuation_cap,desconto\n" + "".join(f"{a},{b},{c},{d}\n" for a, b, c, d in SAFES))
    write(ws, "rodada/term_sheet.md", f"""# Term sheet - Serie A (resumo juridico)

- Pre-money: R$ {_brl_int(PRE_MONEY)}. Dinheiro novo: R$ {_brl_int(NEW_MONEY)} do investidor lider.
- Capitalizacao pre-rodada (C0) = todas as linhas de cap_table.csv (acoes, opcoes em aberto e pool nao alocado).
- Pool: apos a rodada, o pool NAO ALOCADO deve ser {POOL_TARGET:.0%} do fully diluted pos-rodada. O aumento de pool
  entra no pre-money (dilui so os acionistas atuais e os SAFEs).
- SAFEs convertem ao menor entre: valuation_cap / C0, e preco da rodada x (1 - desconto).
- Preco da rodada = pre-money / (C0 + aumento de pool + acoes dos SAFEs).
- Acoes do investidor lider = dinheiro novo / preco da rodada.
""")


def _safe_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    exp = _safe_solution()
    got = read_json(ws, "result.json")
    got = got if isinstance(got, dict) else {}
    result.add("preco por acao", near(got.get("preco_por_acao"), float(str(exp["preco_por_acao"])), 0.005))
    result.add("aumento do pool", near(got.get("novas_acoes_pool"), float(str(exp["novas_acoes_pool"])), 50))
    safes = got.get("acoes_safe") if isinstance(got.get("acoes_safe"), dict) else {}
    assert isinstance(safes, dict)
    expected_safes = exp["acoes_safe"]
    assert isinstance(expected_safes, dict)
    result.add("acoes de cada SAFE", all(near(safes.get(name), shares, 50) for name, shares in expected_safes.items()))
    result.add("acoes do investidor lider", near(got.get("acoes_investidor_novo"), float(str(exp["acoes_investidor_novo"])), 50))
    result.add("participacao dos fundadores pos-rodada", near_share(got.get("participacao_fundadores_pct"), float(str(exp["participacao_fundadores_pct"])) / 100, 0.0002))
    return result


def _safe_reference(ws: Path) -> list[str]:
    write(ws, "result.json", json.dumps(_safe_solution()))
    return ["done"]

SIM_BUGGY = '''"""Lockstep simulation of a a fictional bot skirmish.

Determinism contract (every client must produce the same hash):
- The match RNG is `random.Random(seed)`, owned by World; nothing else draws randomness.
- Every tick, living units act in ascending unit id order.
"""

import hashlib
import random


class World:
    def __init__(self, seed: int) -> None:
        self.rng = random.Random(seed)
        self.units = {}
        for i in range(12):
            uid = f"u{i:02d}"
            self.units[uid] = {"team": i % 2, "hp": 100, "x": float(i * 3), "kills": 0}
        self.alive = set(self.units)

    def enemies_of(self, uid):
        team = self.units[uid]["team"]
        return {other for other in self.alive if self.units[other]["team"] != team}

    def tick(self) -> None:
        for uid in list(self.alive):
            if uid not in self.alive:
                continue
            enemies = self.enemies_of(uid)
            if not enemies:
                return
            target = random.choice(list(enemies))
            damage = self.rng.randint(8, 22)
            unit, victim = self.units[uid], self.units[target]
            unit["x"] += (victim["x"] - unit["x"]) * 0.1
            victim["hp"] -= damage
            if victim["hp"] <= 0:
                self.alive.discard(target)
                unit["kills"] += 1

    def state_hash(self) -> str:
        blob = repr(sorted((uid, u["hp"], round(u["x"], 6), u["kills"]) for uid, u in self.units.items()))
        return hashlib.sha256(blob.encode()).hexdigest()[:16]


def simulate(seed: int, ticks: int) -> str:
    world = World(seed)
    for _ in range(ticks):
        world.tick()
    return world.state_hash()
'''

SIM_VISIBLE = '''import unittest

from lockstep.sim import simulate


class ReplayTest(unittest.TestCase):
    def test_same_seed_same_hash(self):
        self.assertEqual(simulate(7, 40), simulate(7, 40))


if __name__ == "__main__":
    unittest.main()
'''


def _sim_fixed() -> str:
    return (SIM_BUGGY
            .replace("        for uid in list(self.alive):", "        for uid in sorted(self.alive):")
            .replace("            target = random.choice(list(enemies))", "            target = self.rng.choice(sorted(enemies))"))


def _desync_setup(ws: Path) -> None:
    write(ws, "lockstep/__init__.py", "")
    write(ws, "lockstep/sim.py", SIM_BUGGY)
    write(ws, "tests/test_replay.py", SIM_VISIBLE)
    write(ws, "RULES.md", "The match owns its seeded RNG. Living units act in ascending ID order. "
          "Target selection draws from enemies in ascending ID order, then damage is drawn. "
          "Preserve movement, damage, death, kill counting and state hashing as implemented.\n")


def _desync_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    result.mandatory.append(("existing replay test unchanged",
                             (ws / "tests/test_replay.py").read_text(encoding="utf-8") == SIM_VISIBLE
                             if (ws / "tests/test_replay.py").is_file() else False))
    canonical: dict[str, object] = {}
    exec(_sim_fixed(), canonical)
    cases = [(7, 0), (7, 1), (7, 60), (99, 60), (123, 12)]
    expected = [canonical["simulate"](seed, ticks) for seed, ticks in cases]
    outputs: list[object] = []
    code = ("import json, random; from lockstep.sim import simulate; random.seed(918); "
            f"print(json.dumps([simulate(s,t) for s,t in {cases!r}]))")
    for hash_seed in ("1", "2", "3"):
        env = {**os.environ, "PYTHONHASHSEED": hash_seed, "PYTHONDONTWRITEBYTECODE": "1"}
        try:
            proc = subprocess.run([sys.executable, "-c", code], cwd=ws, env=env,
                                  capture_output=True, text=True, timeout=10, check=False)
            outputs.append(json.loads(proc.stdout) if proc.returncode == 0 else None)
        except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
            outputs.append(None)
    result.add("replay agrees across processes", all(isinstance(o, list) for o in outputs)
               and outputs[0] == outputs[1] == outputs[2])
    result.add("game rules preserved", all(o == expected for o in outputs))
    return result


def _desync_reference(ws: Path) -> list[str]:
    write(ws, "lockstep/sim.py", _sim_fixed())
    return ["Fixed deterministic replays."]


TASKS: list[EvalTask] = [
    EvalTask(
        id="bo-safe-conversion", category="backoffice",
        provenance="Port of evals/suite/tasks_hard.py at d8344f72 (#127).",
        summary="Calculate ownership after a funding round with SAFE conversions and an option pool increase.",
        setup=_safe_setup, check=_safe_check, reference=_safe_reference, timeout_s=180,
        deliverables=("result.json",),
        steps=(Step("The founders need the ownership outcome of the round documented in rodada/. "
                    "Write result.json with preco_por_acao, novas_acoes_pool, acoes_safe "
                    "(investor name to shares), acoes_investidor_novo, and participacao_fundadores_pct. "
                    "You have 3 minutes. Finish once correct, with at most 2 rounds of revision."),),
    ),
]

TASKS.append(EvalTask(
    id="gd-lockstep-desync", category="gamedev",
    provenance="Port of evals/suite/tasks_hard.py at d8344f72 (#127).",
    summary="Fix a simulation whose clients disagree on the same match outcome.",
    setup=_desync_setup, check=_desync_check, reference=_desync_reference, timeout_s=300,
    deliverables=("lockstep/sim.py",),
    steps=(Step("Clients playing the same match end with different state hashes. Repair lockstep/ "
                "so replays agree and gameplay follows RULES.md. Keep the existing test intact. "
                "You have 5 minutes. Finish once correct, with at most 2 rounds of revision."),),
))
