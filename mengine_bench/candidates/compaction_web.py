"""Compaction and historical web-research candidates, outside the catalog (#127)."""

from __future__ import annotations

import json
import random
import re
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path

from mengine_bench.core import CheckResult, EvalTask, Step, near, read, result_json, saw, write


def _date_matches(value: object, expected: str) -> bool:
    text = str(value).strip()
    if text.count("/") == 1:
        text += "/2026"
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%B %d, %Y", "%d %B %Y"):
        try:
            parsed = datetime.strptime(text, fmt)
        except ValueError:
            continue
        return parsed.date().isoformat() == expected
    return False


def _note_check(result: CheckResult, ws: Path, filename: str, limit: int) -> None:
    note = read(ws, filename)
    result.add("handoff fits the character budget", bool(note and note.strip()) and len(note or "") <= limit,
               saw(len(note or ""), f"a nonempty {filename} of at most {limit} characters"))


MEETING_TURNS = [
    "[Livia] Pro costs R$ 49/month today. Churn is low; acquisition costs are rising.",
    "[Caio] I propose R$ 59. Comparable plans cost 55 to 69.",
    "[Renata] Small studios would struggle with 59. I suggest 55 and six months of grandfathering.",
    "[Livia] Decision: Pro becomes R$ 55/month on 01/08/2026; existing customers keep R$ 49 until 31/01/2027.",
    "[Caio] Hiring proposal: three openings, SRE, backend developer and designer.",
    "[Livia] Decision: hiring freeze except one SRE. Owner: Livia. Open the role by 15/07/2026.",
    "[Renata] June cloud spending was R$ 71 thousand, driven by a forgotten test GPU.",
    "[Livia] Decision: cloud cap R$ 60 thousand/month, billing alert at 80%. Owner: Caio.",
    "[Caio] I will migrate manual billing to the hosted payment platform.",
    "[Livia] Decision: Caio migrates billing by 31/07/2026; Renata reconciles the first month.",
    "[Renata] The designer can open in Q4 only if monthly revenue exceeds R$ 300 thousand.",
]


def _meeting_setup(ws: Path) -> None:
    rng = random.Random(6330)
    slots = sorted(rng.sample(range(231), len(MEETING_TURNS)))
    decisions = iter(MEETING_TURNS)
    filler = ("[Caio] The meeting room needs maintenance.", "[Renata] The social event vote is still open.",
              "[Livia] Noted for a later meeting.", "[Caio] The dashboard cache is slow again.")
    turns = [next(decisions) if index in slots else rng.choice(filler) for index in range(231)]
    write(ws, "meetings/2026-06-30-ops.md", "# Fictional operations meeting, 30 June 2026\n\n" + "\n\n".join(turns))


def _meeting_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    _note_check(result, ws, "DECISIONS.md", 2000)
    got = result_json(ws)
    for key, expected in (("new_price_brl", 55), ("cloud_cap_brl", 60000)):
        result.add(f"answer {key}", near(got.get(key), expected, 0.01), saw(got.get(key), expected))
    for key, expected in (("starts_on", "2026-08-01"), ("billing_due", "2026-07-31")):
        result.add(f"answer {key}", _date_matches(got.get(key), expected), saw(got.get(key), expected))
    for key, expected in (("approved_role", "SRE"), ("role_owner", "Livia")):
        result.add(f"answer {key}", str(got.get(key, "")).strip().casefold() == expected.casefold(),
                   saw(got.get(key), expected))
    gate = got.get("designer_gate")
    gate = gate if isinstance(gate, dict) else {}
    result.add("answer designer_gate", str(gate.get("quarter", "")).strip().upper() == "Q4"
               and near(gate.get("revenue_above_brl"), 300000, 0.01),
               saw(got.get("designer_gate"), {"quarter": "Q4", "revenue_above_brl": 300000}))
    return result


def _meeting_reference(ws: Path) -> list[str]:
    write(ws, "DECISIONS.md", "Pro: R$ 55/month from 2026-08-01; existing customers R$ 49 until 2027-01-31.\n"
          "Hiring frozen except one SRE, owned by Livia, opening by July 15. Designer only in Q4 if revenue > R$ 300000/month.\n"
          "Cloud cap R$ 60000/month; 80% alert; Caio owns it. Caio migrates billing by 2026-07-31; Renata reconciles.\n")
    write(ws, "result.json", json.dumps({"new_price_brl": 55, "starts_on": "2026-08-01", "approved_role": "SRE",
          "role_owner": "Livia", "cloud_cap_brl": 60000, "billing_due": "2026-07-31",
          "designer_gate": {"quarter": "Q4", "revenue_above_brl": 300000}}))
    return ["Handoff ready.", "Decisions recorded."]


def _trajectory_setup(ws: Path) -> None:
    rng = random.Random(6331)
    files = ("server/net/replication.cpp", "server/net/serializer.cpp", "server/sim/tick.cpp", "tests/net_test.cpp")
    milestones: dict[int, dict[str, object]] = {
        30: {"tool": "bash", "cmd": "tools/bench_tick.sh", "result": "tick p99 = 14.2 ms"},
        55: {"tool": "note", "text": "Trying SIMD (AVX2) serializer for delta compression."},
        78: {"tool": "bash", "cmd": "tools/bench_tick.sh", "result": "tick p99 = 13.6 ms"},
        96: {"tool": "note", "text": "Abandoning SIMD serializer: crashes in dedicated-server ARM64 build; reverted."},
        120: {"tool": "bash", "cmd": "tools/bench_tick.sh", "result": "tick p99 = 12.9 ms"},
        150: {"tool": "bash", "cmd": "tools/bench_tick.sh", "result": "tick p99 = 11.8 ms"},
        157: {"tool": "edit", "file": "server/net/replication.cpp"},
        158: {"tool": "read", "file": "tests/net_test.cpp"},
        159: {"tool": "bash", "cmd": "ctest -R Net --output-on-failure",
              "result": "1 failed: ReplicationTest.DeltaCompression"},
    }
    events: list[str] = []
    for index in range(160):
        kind = rng.choice(("read", "grep", "bash", "edit"))
        entry: dict[str, object] = {"tool": kind, "file": rng.choice(files[1:] if kind == "edit" else files)}
        if kind == "bash":
            entry = {"tool": kind, "cmd": "ctest -R Net --output-on-failure", "result": "12 passed"}
        events.append(json.dumps({"step": index, **milestones.get(index, entry)}))
    write(ws, "agent/trajectory.jsonl", "\n".join(events) + "\n")


def _trajectory_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    _note_check(result, ws, "STATE.md", 1800)
    got = result_json(ws)
    path = str(got.get("last_edited_file", "")).strip().replace("\\", "/").removeprefix("./")
    result.add("answer last_edited_file", path == "server/net/replication.cpp",
               saw(got.get("last_edited_file"), "server/net/replication.cpp"))
    result.add("answer failing_test", str(got.get("failing_test", "")).strip() == "ReplicationTest.DeltaCompression",
               saw(got.get("failing_test"), "ReplicationTest.DeltaCompression"))
    result.add("answer last_p99_ms", near(got.get("last_p99_ms"), 11.8, 0.005), saw(got.get("last_p99_ms"), 11.8))
    approach = str(got.get("abandoned_approach", ""))
    reason = str(got.get("abandonment_reason", ""))
    result.add("answer abandoned_approach", bool(re.search(r"\b(?:SIMD|AVX2?)\b", approach, re.I)),
               saw(approach, "SIMD / AVX2 serializer"))
    result.add("answer abandonment_reason", bool(re.search(r"\bARM(?:64)?\b", reason, re.I))
               and bool(re.search(r"\bcrash\w*\b", reason, re.I)), saw(reason, "crashes on ARM64"))
    return result


def _trajectory_reference(ws: Path) -> list[str]:
    write(ws, "STATE.md", "Last measured tick p99: 11.8 ms (tools/bench_tick.sh). SIMD/AVX2 serializer reverted "
          "because it crashes on dedicated-server ARM64. Last edit: server/net/replication.cpp; "
          "last read: tests/net_test.cpp. Current failure: ReplicationTest.DeltaCompression.\n")
    write(ws, "result.json", json.dumps({"last_edited_file": "server/net/replication.cpp",
          "failing_test": "ReplicationTest.DeltaCompression", "last_p99_ms": 11.8,
          "abandoned_approach": "SIMD AVX2 serializer", "abandonment_reason": "crash on ARM64"}))
    return ["State handed over.", "Current state recorded."]


TASKS: list[EvalTask] = [
    EvalTask(
        id="cmp-meeting-decisions", category="compaction",
        provenance="mengine evals/suite/tasks_compaction.py at d8344f72; fictional operations decisions (#127)",
        summary="Hand over an operations meeting so a colleague can act on its decisions without the transcript.",
        setup=_meeting_setup, check=_meeting_check, reference=_meeting_reference, timeout_s=180,
        steps=(
            Step("You are handing operations work to a colleague who will never see {WS}/meetings/2026-06-30-ops.md. "
                 "Write {WS}/DECISIONS.md, at most 2000 characters, so they can act on the meeting's decisions."),
            Step("You have taken over operations. Your only context is {WS}/DECISIONS.md. Record the decisions in "
                 "{WS}/result.json: new_price_brl (monthly), starts_on, approved_role, role_owner, cloud_cap_brl "
                 "(monthly), billing_due, designer_gate (quarter and revenue_above_brl, monthly).",
                 fresh_session=True, hide=("meetings/2026-06-30-ops.md",), carry=("DECISIONS.md",)),
        ),
    ),
    EvalTask(
        id="cmp-agent-trajectory", category="compaction",
        provenance="mengine evals/suite/tasks_compaction.py at d8344f72; AMA-Bench-style 160-event trajectory (#127)",
        summary="Hand over a tool-call history so a colleague can resume debugging from the current state.",
        setup=_trajectory_setup, check=_trajectory_check, reference=_trajectory_reference, timeout_s=180,
        steps=(
            Step("A colleague needs to resume the debugging work in {WS}/agent/trajectory.jsonl without that history. "
                 "Write {WS}/STATE.md, at most 1800 characters, so they can continue from the current state."),
            Step("You are resuming debugging with only {WS}/STATE.md. Record the current state in {WS}/result.json: "
                 "last_edited_file, failing_test, last_p99_ms, abandoned_approach, abandonment_reason.",
                 fresh_session=True, hide=("agent/trajectory.jsonl",), carry=("STATE.md",)),
        ),
    ),
]
