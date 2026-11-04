"""Information retrieval: log forensics on a game server.

Distractors are planted on purpose (an unrelated ERROR) so grep-and-guess fails and reading wins.
Ported from the private suite with neutral names and public facts.
"""

from __future__ import annotations

import json
import random
import re
from collections.abc import Sequence
from datetime import datetime, timedelta
from pathlib import Path

from mengine_bench.core import (
    CheckResult,
    EvalTask,
    Step,
    has,
    WROTE_RESULT,
    checkpoints,
    is_no,
    is_yes,
    near,
    near_share,
    result_json,
    saw,
    write,
)


# ------------------------------------------------------------ ir-server-logs --

OUTAGE_START = datetime(2026, 6, 2, 3, 17, 42)
OUTAGE_END = datetime(2026, 6, 2, 3, 53, 31)


def _log_line(rng: random.Random, roll: float, t: datetime, players: int) -> tuple[str, int]:
    if roll < 0.55:
        return f"{t:%Y-%m-%d %H:%M:%S} INFO heartbeat players={players} tick=64 mem_gb={rng.uniform(21, 29):.1f}", players
    if roll < 0.75:
        players = min(32, players + 1)
        return f"{t:%Y-%m-%d %H:%M:%S} INFO player joined steam_{rng.randint(10**15, 10**16 - 1)} players={players}", players
    if roll < 0.93:
        players = max(0, players - 1)
        return f"{t:%Y-%m-%d %H:%M:%S} INFO player left players={players}", players
    return f"{t:%Y-%m-%d %H:%M:%S} INFO autosave ok {rng.randint(180, 420)} ms", players


def _log_lines(day: int) -> list[str]:
    rng = random.Random(6328 + day)
    t = datetime(2026, 6, day, 0, 0, 5)
    end = datetime(2026, 6, day, 23, 59, 30)
    lines = []
    players = 0
    while t < end:
        roll = rng.random()
        if day == 2 and OUTAGE_START <= t < OUTAGE_END:
            # The first save error is appended at exactly OUTAGE_START below.
            if t > OUTAGE_START + timedelta(seconds=30):
                lines.append(f"{t:%Y-%m-%d %H:%M:%S} WARN watchdog: restart attempt, server exited code 137")
            t += timedelta(seconds=rng.randint(20, 90))
            continue
        line, players = _log_line(rng, roll, t, players)
        lines.append(line)
        t += timedelta(seconds=rng.randint(20, 75))
    if day == 1:
        # Unrelated ERROR (documentation-range IP, RFC 5737) the forensics must ignore.
        lines.insert(len(lines) // 3, "2026-06-01 09:12:40 ERROR RCON auth failed from 203.0.113.12 (bad password)")
    if day == 2:
        lines.append("2026-06-02 03:10:02 WARN disk /data usage 97% (free 3.1 GB)")
        save_error = "ERROR SaveGame failed: write /data/game/Saved/Level.sav: No space left on device"
        lines.append(f"{OUTAGE_START:%Y-%m-%d %H:%M:%S} {save_error}")
        lines.append(f"{OUTAGE_START + timedelta(seconds=18):%Y-%m-%d %H:%M:%S} {save_error}")
        lines.append("2026-06-02 03:18:05 FATAL watchdog: server unresponsive for 20s, restarting")
        lines.append("2026-06-02 03:52:10 INFO backup rotation freed 38.2 GB on /data")
        lines.append(f"{OUTAGE_END:%Y-%m-%d %H:%M:%S} INFO server ready, accepting players")
    # Day 1 too: the planted RCON line went in out of order (#59).
    lines.sort()
    return lines


def _logs_expected() -> dict[str, object]:
    minutes = (OUTAGE_END - OUTAGE_START).total_seconds() / 60
    availability = (1 - minutes / (30 * 24 * 60)) * 100
    return {"start": "2026-06-02 03:17:42", "end": "2026-06-02 03:53:31", "minutes_down": minutes,
            "availability_june_pct": availability, "slo_999_ok": availability >= 99.9}


def _logs_setup(ws: Path) -> None:
    for day in (1, 2, 3):
        write(ws, f"logs/gameserver-2026-06-0{day}.log", "\n".join(_log_lines(day)) + "\n")
    write(ws, "logs/README.md", "Dedicated game server. Monthly availability SLO: 99.9%. "
          "Down = from the first save error to the 'server ready' line. June has 30 days; there is only one incident.\n")


def _minutes(value: object) -> object:
    """Minutes from 35.82, "35 min 49 s" or "00:35:49"."""
    text = str(value)
    clock = re.search(r"\b(\d+):(\d{2}):(\d{2})\b", text)
    if clock:
        return int(clock[1]) * 60 + int(clock[2]) + int(clock[3]) / 60
    spoken = re.search(r"(\d+)\s*m(?:in\w*)?\s*(\d+)\s*s", text)
    return int(spoken[1]) + int(spoken[2]) / 60 if spoken else value


def _logs_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    exp = _logs_expected()
    got = result_json(ws)
    # #98: the moment, in any common writing ("2026-06-02T03:17:42Z").
    result.add("incident start", str(exp["start"]) in str(got.get("start", "")).replace("T", " "), saw(got.get("start"), exp["start"]))
    result.add("incident end", str(exp["end"]) in str(got.get("end", "")).replace("T", " "), saw(got.get("end"), exp["end"]))
    # #98: the exact window is checked above, so a whole minute here is rounding, not a wrong outage.
    result.add("minutes down", near(_minutes(got.get("minutes_down")), float(str(exp["minutes_down"])), 0.5),
               saw(got.get("minutes_down"), exp["minutes_down"]))
    result.add("June availability",
               near_share(got.get("availability_june_pct"), float(str(exp["availability_june_pct"])) / 100, 5e-5),
               saw(got.get("availability_june_pct"), exp["availability_june_pct"]))
    result.add("SLO 99.9 met", (is_yes if exp["slo_999_ok"] else is_no)(got.get("slo_999_ok")), saw(got.get("slo_999_ok"), exp["slo_999_ok"]))
    result.add("root cause = /data disk full", _names_disk_full(str(got.get("root_cause", ""))),
               saw(got.get("root_cause"), "the /data disk was full"))
    return result


# #26, #28: every storage noun and every way of saying "full" name the same cause.
# #59: "space" alone also fits "the disk had free space", which rules the cause out.
_STORAGE = r"(disk|disco|volume|partition|mount|file\s?system|storage|/data)"
# #164: bare "capacity" also fits "the disk had sufficient capacity"; only a capacity that was reached counts.
_CAPACITY_REACHED = r"\b(reach\w*|hit|at|over|exceed\w*|out of)\s+(\w+\s+)?capacity|capacity\s+(was\s+)?(reached|hit|exceeded)"
_FULL = rf"(full|cheio|fill\w*|{_CAPACITY_REACHED}|exhaust\w*|100(\.0+)?\s?%|sem espa\w*)"
DISK_FULL_CAUSE = (rf"{_STORAGE}\b.{{0,40}}{_FULL}|\b{_FULL}.{{0,40}}{_STORAGE}"
                   r"|out of (disk |storage )?space|ran out of (disk|space|storage)|no space left"
                   r"|(not enough|insufficient|without|no) (free |disk )?space|\benospc\b")
# #28: "the disk was not full; ...RCON" names the disk only to rule it out. The negation must sit right
# before "full"/"the cause": "couldn't save because the disk was full" still names the disk.
DISK_FULL_NEGATION = r"(\bnot|\bnever|n't)\s+(\w+\s+){0,2}?(full|out of|the (root )?cause)"


def _names_disk_full(root_cause: str) -> bool:
    clauses = re.split(r"[;!?]|\.\s|\bbut\b", root_cause)
    return any(has(clause, DISK_FULL_CAUSE) and not has(clause, DISK_FULL_NEGATION) for clause in clauses)


def _logs_reference(ws: Path) -> list[str]:
    write(ws, "result.json", json.dumps({**_logs_expected(), "root_cause": "/data disk full (No space left on device)"}))
    return ["done"]


TASKS = [
    EvalTask(
        id="ir-server-logs", category="retrieval",
        provenance="Game server ops: incident window, root cause and monthly SLO from 3 days of logs",
        summary="Investigate a game server outage from its logs and report what happened.",
        setup=_logs_setup, check=_logs_check, reference=_logs_reference, timeout_s=60,
        checkpoints=checkpoints(("read the notes", r"logs.{1,4}README"), ("read the logs", r"gameserver|logs"), WROTE_RESULT),
        steps=(Step("The game went down in June and we owe the team an incident report. The logs and their notes are in "
                    "{WS}/logs. When did it start and end, how long was it, did we keep our monthly availability target, and "
                    "why did it happen? Record it in {WS}/result.json: start, end, minutes_down, availability_june_pct, "
                    "slo_999_ok, root_cause."),),
    ),
]
