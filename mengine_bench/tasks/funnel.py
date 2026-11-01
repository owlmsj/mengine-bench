"""SQL funnel task with ordered events, duplicates and test accounts."""

from __future__ import annotations

import json
import random
import sqlite3
from collections.abc import Sequence
from datetime import datetime, timedelta
from pathlib import Path

from mengine_bench.core import (
    CheckResult,
    EvalTask,
    Step,
    WROTE_RESULT,
    checkpoints,
    near,
    result_json,
    saw,
    write,
)

METRICS = """# How we report the funnel

Steps, in order: install, tutorial_complete, first_match, purchase.
A step counts only at or after the same player's previous step, with no time limit; its time is the first valid occurrence.
Test accounts and events from unknown players do not count.
A step's conversion is its players over the previous step's players. The biggest drop is the step with the lowest conversion.
"""

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
    write(ws, "METRICS.md", METRICS)


def _biggest_drops() -> dict[str, str]:
    rows = _funnel_expected()
    return {platform: min((row for row in rows if row[0] == platform and row[1] != FUNNEL[0]), key=lambda row: row[3])[1]
            for platform in ("pc", "steamdeck")}


def _players(row: dict[str, object]) -> object:
    return next((row[key] for key in ("players", "users", "count") if key in row), None)


def _funnel_counts(got: object, platform: str) -> dict[str, object]:
    """Users per step of a platform, from {step: users} or a list of rows: the brief fixes the facts, not the shape."""
    if isinstance(got, list):
        got = {platform: [row for row in got if isinstance(row, dict) and row.get("platform") == platform]}
    entry = got.get(platform) if isinstance(got, dict) else None
    if isinstance(entry, list):
        return {str(row.get("step")): _players(row) for row in entry if isinstance(row, dict)}
    return {step: _players(value) if isinstance(value, dict) else value for step, value in entry.items()} if isinstance(entry, dict) else {}


def _funnel_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    got = result_json(ws)
    for platform in ("pc", "steamdeck"):
        want = {row[1]: row[2] for row in _funnel_expected() if row[0] == platform}
        counts = _funnel_counts(got.get("funnel"), platform)
        result.add(f"players per step on {platform}", all(near(counts.get(step), want[step], 0) for step in FUNNEL), saw(counts, want))
    drops = got.get("biggest_drop")
    drops = drops if isinstance(drops, dict) else {}
    gold = _biggest_drops()
    result.add("biggest drop on each platform", all(str(drops.get(platform)).strip().lower() == gold[platform] for platform in gold), saw(drops, gold))
    return result


def _funnel_reference(ws: Path) -> list[str]:
    funnel: dict[str, dict[str, int]] = {}
    for platform, step, users, _ in _funnel_expected():
        funnel.setdefault(platform, {})[step] = users
    write(ws, "result.json", json.dumps({"funnel": funnel, "biggest_drop": _biggest_drops()}))
    return ["done"]


TASKS = [
    EvalTask(
        id="ds-sql-funnel", category="data-science",
        provenance="Product funnel in SQLite: ordered steps, test accounts, dupes, out-of-order events",
        summary="Find where players drop off on each platform from a product analytics database.",
        setup=_funnel_setup, check=_funnel_check, reference=_funnel_reference, timeout_s=180,
        checkpoints=checkpoints(("read the rules", r"METRICS"), ("looked at the schema", r"sqlite_master|\.schema|PRAGMA"), ("excluded test accounts", r"is_test"), WROTE_RESULT),
        steps=(Step("Product wants to know where players drop off on each platform. The data is in {WS}/analytics.db and our "
                    "reporting rules are in {WS}/METRICS.md. Where do we lose the most players? Record it in "
                    "{WS}/result.json: funnel (per platform, players at each step) and biggest_drop (per platform, the step)."),),
    ),
]
