"""HARD tasks: one per core theme, built so the obvious fix is not enough.

- gd-lockstep-desync: fixing the global RNG passes the visible test; the set
  iteration bug only shows across processes (PYTHONHASHSEED), like a real desync.
- ds-sql-funnel: ordered funnel with a 7-day window per step, test accounts,
  duplicates and out-of-order events in SQLite.
- bo-safe-conversion: priced round with post-money pool top-up and SAFE
  conversion; price, pool and SAFE shares depend on each other (fixed point).
"""

from __future__ import annotations

import csv
import io
import json
import os
import random
import sqlite3
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from datetime import datetime, timedelta
from pathlib import Path

from mengine_bench.core import (
    FAST,
    FULL,
    CheckResult,
    EvalTask,
    Step,
    close,
    read,
    read_json,
    scratch_root,
    write,
)

RULES = "Write your files inside {WS}. Do not ask for confirmation; finish and summarize in 2 lines."

# ------------------------------------------------------- gd-lockstep-desync --

SIM_BUGGY = '''"""Lockstep simulation of a Pixel Arena bot skirmish.

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


def _hash_in_process(ws: Path, seed: int, hash_seed: str) -> str:
    code = f"from lockstep.sim import simulate; print(simulate({seed}, 60))"
    env = {**os.environ, "PYTHONPATH": str(ws), "PYTHONHASHSEED": hash_seed, "PYTHONDONTWRITEBYTECODE": "1"}
    proc = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, timeout=60, check=False)
    return proc.stdout.strip() if proc.returncode == 0 else f"error:{proc.stderr.strip()[-120:]}"


def _canonical_hashes() -> dict[int, str]:
    with tempfile.TemporaryDirectory(prefix="bench-lockstep-", dir=scratch_root()) as tmp:
        ws = Path(tmp)
        write(ws, "lockstep/__init__.py", "")
        write(ws, "lockstep/sim.py", _sim_fixed())
        return {seed: _hash_in_process(ws, seed, "0") for seed in (7, 99)}


def _desync_setup(ws: Path) -> None:
    write(ws, "lockstep/__init__.py", "")
    write(ws, "lockstep/sim.py", SIM_BUGGY)
    write(ws, "tests/test_replay.py", SIM_VISIBLE)
    write(ws, "BUG.md", "QA report: two clients in the same match (same seed and same inputs) end with a different "
          "state_hash after a few dozen ticks. The local test sometimes passes. We need determinism across "
          "machines/processes without changing the game rules.\n")


def _desync_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    canonical = _canonical_hashes()
    for seed, expected in canonical.items():
        got = {_hash_in_process(ws, seed, hs) for hs in ("1", "2", "3")}
        result.add(f"seed {seed}: same hash across processes with different PYTHONHASHSEED", len(got) == 1)
        result.add(f"seed {seed}: rules preserved (canonical contract hash)", got == {expected})
    return result


def _desync_reference(ws: Path) -> list[str]:
    write(ws, "lockstep/sim.py", _sim_fixed())
    return ["fixed: world RNG + sorted iteration"]


# ------------------------------------------------------------ ds-sql-funnel --

FUNNEL = ("install", "tutorial_complete", "first_match", "purchase")
WINDOW = timedelta(days=7)


def _funnel_rows() -> tuple[list[tuple[str, str, int]], list[tuple[str, str, str]]]:
    rng = random.Random(6334)
    users, events = [], []
    base = datetime(2026, 6, 1, 12, 0, 0)
    for i in range(900):
        uid = f"p{i:04d}"
        platform = rng.choice(["pc", "pc", "steamdeck"])
        is_test = int(rng.random() < 0.04)
        users.append((uid, platform, is_test))
        t = base + timedelta(hours=rng.randint(0, 24 * 20))
        for step in FUNNEL:
            if rng.random() > (0.82 if platform == "pc" else 0.7):
                break
            events.append((uid, step, t.isoformat(sep=" ")))
            if rng.random() < 0.1:
                events.append((uid, step, (t + timedelta(minutes=5)).isoformat(sep=" ")))
            gap = timedelta(hours=rng.randint(1, 24 * 9))
            t += gap
        if rng.random() < 0.08:
            events.append((uid, "purchase", (base - timedelta(days=2)).isoformat(sep=" ")))
    events += [(f"ghost{j}", "install", base.isoformat(sep=" ")) for j in range(15)]
    rng.shuffle(events)
    return users, events


def _funnel_expected() -> list[tuple[str, str, int, float]]:
    users, events = _funnel_rows()
    info = {u: (p, t) for u, p, t in users}
    by_user: dict[str, list[tuple[datetime, str]]] = {}
    for uid, name, ts in events:
        if uid in info and not info[uid][1]:
            by_user.setdefault(uid, []).append((datetime.fromisoformat(ts), name))
    reached: dict[tuple[str, str], int] = {}
    for uid, evs in by_user.items():
        evs.sort()
        prev_time = None
        for step in FUNNEL:
            candidates = [t for t, n in evs if n == step and (prev_time is None or prev_time <= t <= prev_time + WINDOW)]
            if not candidates:
                break
            prev_time = min(candidates)
            key = (info[uid][0], step)
            reached[key] = reached.get(key, 0) + 1
    rows = []
    for platform in ("pc", "steamdeck"):
        prev = None
        for step in FUNNEL:
            n = reached.get((platform, step), 0)
            rows.append((platform, step, n, round(n / prev, 4) if prev else 1.0))
            prev = n
    return rows


def _funnel_setup(ws: Path) -> None:
    users, events = _funnel_rows()
    db = ws / "analytics.db"
    con = sqlite3.connect(db)
    con.execute("create table users (user_id text primary key, platform text, is_test integer)")
    con.execute("create table events (user_id text, name text, ts text)")
    con.executemany("insert into users values (?, ?, ?)", users)
    con.executemany("insert into events values (?, ?, ?)", events)
    con.commit()
    con.close()


def _funnel_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    exp = _funnel_expected()
    got = list(csv.DictReader(io.StringIO(read(ws, "funnel.csv") or "")))
    keys = [(g.get("platform"), g.get("step")) for g in got]
    result.add("platform x step rows in funnel order", keys == [(e[0], e[1]) for e in exp])
    result.add("users per step", len(got) == len(exp) and all(str(g.get("users")) == str(e[2]) for g, e in zip(got, exp, strict=False)))
    result.add("conversion from previous step", len(got) == len(exp) and all(close(g.get("conv_from_prev"), e[3], 1e-4) for g, e in zip(got, exp, strict=False)))
    return result


def _funnel_reference(ws: Path) -> list[str]:
    lines = ["platform,step,users,conv_from_prev"] + [f"{p},{s},{n},{c:.4f}" for p, s, n, c in _funnel_expected()]
    write(ws, "funnel.csv", "\n".join(lines) + "\n")
    return ["done"]


# ------------------------------------------------------- bo-safe-conversion --

# Fictional holders; numbers unchanged from the private v1 suite.
CAP_TABLE = [("Founder Alice", "common", 4_200_000), ("Founder Bruno", "common", 3_300_000),
             ("Diego (exercised options)", "common", 250_000), ("Outstanding options", "options", 850_000),
             ("Unallocated pool", "pool", 400_000)]
SAFES = [("Kestrel Angels", 500_000, 12_000_000, 0.20), ("Coruja Ventures", 1_200_000, 16_000_000, 0.15),
         ("BH Accelerator", 150_000, 8_000_000, 0.25)]
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
    founders = sum(n for name, _, n in CAP_TABLE if name.startswith("Founder"))
    return {"price_per_share": price, "new_pool_shares": x, "safe_shares": safe_shares,
            "new_investor_shares": NEW_MONEY / price, "post_money_fd": post,
            "founders_ownership_pct": founders / post * 100}


def _money(value: float) -> str:
    return f"{value:,.0f}"


def _safe_setup(ws: Path) -> None:
    write(ws, "round/cap_table.csv", "holder,class,shares\n" + "".join(f"{a},{b},{c}\n" for a, b, c in CAP_TABLE))
    write(ws, "round/safes.csv", "investor,amount,valuation_cap,discount\n" + "".join(f"{a},{b},{c},{d}\n" for a, b, c, d in SAFES))
    write(ws, "round/term_sheet.md", f"""# Term sheet - Series A (legal summary)

- Pre-money: BRL {_money(PRE_MONEY)}. New money: BRL {_money(NEW_MONEY)} from the lead investor.
- Pre-round capitalization (C0) = all rows of cap_table.csv (shares, outstanding options and unallocated pool).
- Pool: after the round, the UNALLOCATED pool must be {POOL_TARGET:.0%} of the post-round fully diluted. The pool
  top-up goes into the pre-money (it dilutes only current holders and the SAFEs).
- SAFEs convert at the lower of: valuation_cap / C0, and round price x (1 - discount).
- Round price = pre-money / (C0 + pool top-up + SAFE shares).
- Lead investor shares = new money / round price.
""")


def _safe_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    exp = _safe_solution()
    got = read_json(ws, "round_result.json")
    got = got if isinstance(got, dict) else {}
    result.add("price per share", close(got.get("price_per_share"), float(str(exp["price_per_share"])), 1e-3))
    result.add("pool top-up", close(got.get("new_pool_shares"), float(str(exp["new_pool_shares"])), 50))
    safes = got.get("safe_shares")
    safes = safes if isinstance(safes, dict) else {}
    expected_safes = exp["safe_shares"]
    if not isinstance(expected_safes, dict):
        raise TypeError(f"gold safe_shares received {expected_safes!r}; expected dict investor -> shares")
    result.add("shares of each SAFE", all(close(safes.get(name), shares, 50) for name, shares in expected_safes.items()))
    result.add("lead investor shares", close(got.get("new_investor_shares"), float(str(exp["new_investor_shares"])), 50))
    result.add("founders post-round ownership",
               close(got.get("founders_ownership_pct"), float(str(exp["founders_ownership_pct"])), 0.02))
    return result


def _safe_reference(ws: Path) -> list[str]:
    write(ws, "round_result.json", json.dumps(_safe_solution()))
    return ["done"]


# Weight 2: HARD tasks. par_s: DeepSeek V4.1 Flash wall times from the
# maintainers' v1 FAST run (2026-09-23), rounded up to whole seconds.
TASKS = [
    EvalTask(
        id="gd-lockstep-desync", category="gamedev", suites=frozenset({FAST, FULL}),
        provenance="Multiplayer lockstep desync: two nondeterminism sources, one invisible in-process (hash seed)",
        summary="HARD: make a lockstep simulation deterministic across processes without changing the rules",
        setup=_desync_setup, check=_desync_check, reference=_desync_reference, timeout_s=420, weight=2, par_s=52,
        steps=(Step("Read {WS}/BUG.md and the determinism contract in the docstring of {WS}/lockstep/sim.py. Fix the code "
                    "so the same seed yields the same state_hash on any machine and process, without changing the rules. "
                    "Validate by running the simulation in separate processes. " + RULES),),
    ),
    EvalTask(
        id="ds-sql-funnel", category="data-science", suites=frozenset({FAST, FULL}),
        provenance="Product funnel in SQL: ordered steps, 7-day window per step, test accounts, dupes, out-of-order events",
        summary="HARD: ordered funnel with a 7-day window per step in SQLite, per platform",
        setup=_funnel_setup, check=_funnel_check, reference=_funnel_reference, timeout_s=420, weight=2, par_s=23,
        steps=(Step("In {WS}/analytics.db (SQLite: users, events) compute the funnel install -> tutorial_complete -> "
                    "first_match -> purchase per platform. Rules: ignore users with is_test=1 and events whose user_id is "
                    "not in users; a step only counts if it happens within 7 days (inclusive) after the same user's "
                    "previous step, never before it; use the first valid occurrence of each step. Write {WS}/funnel.csv "
                    "with platform,step,users,conv_from_prev (4 decimals; 1.0 on install), platform pc first then "
                    "steamdeck, steps in funnel order. " + RULES),),
    ),
    EvalTask(
        id="bo-safe-conversion", category="backoffice", suites=frozenset({FAST, FULL}),
        provenance="Series A math: post-money pool top-up in the pre-money plus SAFE conversion (circular, fixed point)",
        summary="HARD: Series A round with pool top-up and conversion of 3 SAFEs (circular computation)",
        setup=_safe_setup, check=_safe_check, reference=_safe_reference, timeout_s=420, weight=2, par_s=51,
        steps=(Step("Follow {WS}/round/term_sheet.md with {WS}/round/cap_table.csv and {WS}/round/safes.csv. Write "
                    "{WS}/round_result.json with price_per_share, new_pool_shares, safe_shares (object investor -> "
                    "shares), new_investor_shares, founders_ownership_pct (both founders combined, % of the post-round "
                    "fully diluted). Do not round numbers to integers. " + RULES),),
    ),
]
