"""Information retrieval tasks: multi-hop over a studio wiki, log forensics on a
game server.

Distractors are planted on purpose (a near-identical bug id, a deprecated map
page, an unrelated ERROR) so grep-and-guess fails and reading wins.
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
    close,
    has,
    read_json,
    write,
)

RULES = "Write your files inside {WS}. Do not ask for confirmation."

# ------------------------------------------------------------ ir-studio-wiki --

WIKI_FACTS = {
    "bugs/BUG-4471.md": """# BUG-4471 - crash when switching weapons during respawn

Severity: S1. Platform: Win64 shipping. Reported by QA on 2026-05-02.

Repro: die holding the sniper, press Q on the respawn frame. The
`UWeaponSwapComponent` still references the old pawn.

Fix: PR #812 (branch `fix/respawn-swap`), merged into `release/0.14`.
See the 0.14 changelog for the build it shipped in.
""",
    "bugs/BUG-4417.md": """# BUG-4417 - crosshair texture disappears at 21:9

Severity: S3. Fixed by PR #805. Do not confuse with BUG-4471.
""",
    "releases/changelog-0.14.md": """# Changelog 0.14.x

## 0.14.1
- PR #790 SMG recoil balancing
- PR #795 lobby: region filter

## 0.14.2
- PR #805 fixes BUG-4417 (ultrawide crosshair)
- PR #807 tutorial telemetry for the stats-panel

## 0.14.2.1 (hotfix, cherry-pick of #809 only)
- PR #809 fixes audio crash on Linux

## 0.14.3
- PR #812 fixes weapon swap crash during respawn
- PR #815 new ranked map in rotation
""",
    "releases/approvals.md": """# Release approvals

| Build | Approved by | Date |
|---|---|---|
| 0.14.1 | Bruno Costa | 2026-04-22 |
| 0.14.2 | Carla Mendes | 2026-05-06 |
| 0.14.2.1 | Bruno Costa | 2026-05-09 |
| 0.14.3 | Alice Sato | 2026-05-19 |
| 0.15.0 | Carla Mendes | 2026-06-10 |
""",
    "maps/neoplastic.md": """# Neoplastic map (current)

Red/blue/yellow grid; black lines are cover walls.

| Mode | Max players | Round time |
|---|---|---|
| Casual | 16 | 10 min |
| Ranked | 10 | 2 min 30 s |
""",
    "maps/neoplastic-v1-deprecated.md": """# Neoplastic v1 (DEPRECATED - see maps/neoplastic.md)

Ranked: 12 players. Casual: 20 players. Values from before the April rework.
""",
    "postmortems/PM-12.md": """# PM-12 - high-ping ranked queues (2026-05-28)

Timeline: 18:02 deploy of config `live-0528`; 18:40 lag complaints.
Cause: `matchmaking.max_ping_ms` went from 120 to 250 to fill SA-East queues.
Mitigation: rolled the flag back to its previous value (120) at 19:15.
Action: no change to `matchmaking.region_weight`.
""",
}

FILLER_TOPICS = [
    ("pipeline/build-farm.md", "Build farm", "Horde agents with UE 5.8, shared DDC cache, 4 Win64 agents."),
    ("pipeline/perforce.md", "Perforce", "mainline/release streams; shelve before cherry-pick."),
    ("pipeline/cook.md", "Cook", "Incremental cook per platform; pak chunking per map."),
    ("art/palette.md", "Palette", "Red #D40920, blue #1356A2, yellow #F7D842, black #000000."),
    ("art/lod.md", "LODs", "Nanite for environments, manual LODs for first-person weapons."),
    ("design/weapons.md", "Weapons", "SMG, rifle, sniper, shotgun, LMG; recoil by curve."),
    ("design/economy.md", "Economy", "Credits per round: 900 win, 600 loss."),
    ("ops/servers.md", "Servers", "SA-East and US-East regions; tick 64."),
    ("ops/oncall.md", "On-call", "Weekly rotation; pager for S1."),
    ("people/directory.md", "Directory", "Alice Sato (producer), Bruno Costa (lead eng), Carla Mendes (QA lead)."),
    ("qa/regression.md", "Regression", "Smoke suite per build; S1 blocks release."),
    ("qa/platforms.md", "Platforms", "Win64 and Linux server; Steam Deck under evaluation."),
    ("telemetry/events.md", "Events", "tutorial_complete, match_end, weapon_swap."),
    ("telemetry/panel.md", "Panel", "stats-panel with SSO login; A/B by player_id hash."),
    ("releases/process.md", "Release process", "RC on Tuesday, producer approval before the Steam push."),
    ("releases/changelog-0.13.md", "Changelog 0.13", "PR #702 bot respawn crash (a different bug), PR #733 HUD."),
    ("bugs/BUG-4390.md", "BUG-4390", "Bot respawn crash, fixed in PR #702 (0.13.4)."),
    ("design/maps.md", "Maps", "Neoplastic, Broadway, Composition II."),
]

FILLER_SENTENCES = [
    "Updated after the sprint retro; see the #eng channel for context.",
    "Checklist reviewed by the area lead; mismatches go to the backlog.",
    "Performance numbers measured on the build farm, not on a dev machine.",
    "Any change here needs a PR reviewed by two people.",
    "History before 0.12 was archived in the old wiki.",
]


def _wiki_setup(ws: Path) -> None:
    rng = random.Random(6327)
    for rel, text in WIKI_FACTS.items():
        write(ws, f"wiki/{rel}", text)
    for rel, title, fact in FILLER_TOPICS:
        paras = [f"# {title}\n", fact]
        paras.extend(rng.choice(FILLER_SENTENCES) for _ in range(rng.randint(6, 12)))
        write(ws, f"wiki/{rel}", "\n\n".join(paras) + "\n")


WIKI_GOLD = {"build": "0.14.3", "approver": "Alice Sato", "neoplastic_ranked_max": 10,
             "flag": "matchmaking.max_ping_ms", "restored_value": 120}
WIKI_SOURCES = ("bugs/BUG-4471.md", "releases/changelog-0.14.md", "releases/approvals.md",
                "maps/neoplastic.md", "postmortems/PM-12.md")


def _wiki_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    got = read_json(ws, "answers.json")
    got = got if isinstance(got, dict) else {}
    result.add("build with the BUG-4471 fix", str(got.get("build")) == WIKI_GOLD["build"])
    result.add("who approved that build", str(got.get("approver", "")).strip().lower() == "alice sato")
    result.add("ranked max on the current Neoplastic", close(got.get("neoplastic_ranked_max"), 10, 0))
    result.add("flag reverted in PM-12", str(got.get("flag")) == WIKI_GOLD["flag"])
    result.add("restored value", close(got.get("restored_value"), 120, 0))
    sources = " ".join(str(s) for s in (got.get("sources") or []))
    result.add("sources cited", all(src.split("/")[-1] in sources for src in WIKI_SOURCES))
    return result


def _wiki_reference(ws: Path) -> list[str]:
    write(ws, "answers.json", json.dumps({**WIKI_GOLD, "sources": [f"wiki/{s}" for s in WIKI_SOURCES]}))
    return ["done"]


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


def _logs_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    exp = _logs_expected()
    got = read_json(ws, "incident.json")
    got = got if isinstance(got, dict) else {}
    result.add("incident start", str(got.get("start", "")).replace("T", " ") == exp["start"])
    result.add("incident end", str(got.get("end", "")).replace("T", " ") == exp["end"])
    result.add("minutes down", close(got.get("minutes_down"), float(str(exp["minutes_down"])), 0.05))
    result.add("June availability",
               close(got.get("availability_june_pct"), float(str(exp["availability_june_pct"])), 0.001))
    result.add("SLO 99.9 met", got.get("slo_999_ok") is exp["slo_999_ok"])
    result.add("root cause = /data disk full", _names_disk_full(str(got.get("root_cause", ""))))
    return result


# #26, #28: every storage noun and every way of saying "full" name the same cause.
DISK_FULL_CAUSE = (r"(disk|disco|volume|partition|mount|file\s?system|storage|/data)\b.{0,40}"
                   r"(full|cheio|fill|capacity|exhaust|100(\.0+)?\s?%|space|espa)"
                   r"|out of (disk |storage )?space|ran out of (disk|space|storage)|no space left|\benospc\b")
# #28: "the disk was not full; ...RCON" names the disk only to rule it out.
DISK_FULL_NEGATION = r"\b(not|never|without)\b|n't\b"


def _names_disk_full(root_cause: str) -> bool:
    clauses = re.split(r"[;!?]|\.\s|\bbut\b", root_cause)
    return any(has(clause, DISK_FULL_CAUSE) and not has(clause, DISK_FULL_NEGATION) for clause in clauses)


def _logs_reference(ws: Path) -> list[str]:
    write(ws, "incident.json", json.dumps({**_logs_expected(), "root_cause": "/data disk full (No space left on device)"}))
    return ["done"]


TASKS = [
    EvalTask(
        id="ir-studio-wiki", category="retrieval",
        provenance="Internal-wiki QA with multi-hop (bug -> changelog -> approvals) and planted distractors",
        summary="Find release and game details across a studio wiki and cite the files that support each answer.",
        setup=_wiki_setup, check=_wiki_check, reference=_wiki_reference, timeout_s=300,
        steps=(Step("Use the wiki in {WS}/wiki to answer: (1) in which build the fix for BUG-4471 first shipped and "
                    "(2) who approved that build; (3) the maximum number of players in ranked mode on the current "
                    "Neoplastic map; (4) which flag was reverted in PM-12 and (5) to which value. Write "
                    "{WS}/answers.json with build, approver, neoplastic_ranked_max, flag, restored_value and sources "
                    "(list of the wiki files used). " + RULES),),
    ),
    EvalTask(
        id="ir-server-logs", category="retrieval",
        provenance="Game server ops: incident window, root cause and monthly SLO from 3 days of logs",
        summary="Read game server logs to explain an outage and calculate downtime and monthly availability.",
        setup=_logs_setup, check=_logs_check, reference=_logs_reference, timeout_s=360,
        steps=(Step("Read {WS}/logs/README.md and investigate the logs in {WS}/logs. Write {WS}/incident.json with "
                    "start and end (format 'YYYY-MM-DD HH:MM:SS'), minutes_down (2 decimals), availability_june_pct "
                    "(3 decimals), slo_999_ok (bool) and root_cause (one sentence). " + RULES),),
    ),
]
