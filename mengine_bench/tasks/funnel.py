"""SQL funnel task with ordered events, duplicates and test accounts."""

from __future__ import annotations

import csv
import io
import random
import sqlite3
from collections.abc import Sequence
from datetime import datetime, timedelta
from pathlib import Path

from mengine_bench.core import (
    CheckResult,
    EvalTask,
    Step,
    close,
    read,
    write,
)

RULES = "Write your files inside {WS}. Do not ask for confirmation; finish and summarize in 2 lines."

# ------------------------------------------------------------ ds-sql-funnel --

FUNNEL = ("install", "tutorial_complete", "first_match", "purchase")


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
            candidates = [t for t, n in evs if n == step and (prev_time is None or t >= prev_time)]
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


TASKS = [
    EvalTask(
        id="ds-sql-funnel", category="data-science",
        provenance="Product funnel in SQL: ordered steps, test accounts, dupes, out-of-order events",
        summary="Count players at each ordered funnel step in SQLite, excluding test accounts and duplicates, by platform.",
        setup=_funnel_setup, check=_funnel_check, reference=_funnel_reference, timeout_s=420,
        steps=(Step("In {WS}/analytics.db (SQLite: users, events) compute the funnel install -> tutorial_complete -> "
                    "first_match -> purchase per platform. Rules: ignore users with is_test=1 and events whose user_id is "
                    "not in users; a step only counts at or after the same user's previous step, with no time limit; "
                    "use the first valid occurrence of each step. Write {WS}/funnel.csv "
                    "with platform,step,users,conv_from_prev (4 decimals; 1.0 on install), platform pc first then "
                    "steamdeck, steps in funnel order. " + RULES),),
    ),
]
