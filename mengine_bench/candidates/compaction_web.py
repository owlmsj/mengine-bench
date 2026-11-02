"""Compaction and historical web-research candidates, outside the catalog (#127)."""

from __future__ import annotations

import json
import random
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
]
