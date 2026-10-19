"""Long-context and vision tasks.

Long context goes INLINE in the prompt and the source file leaves the
workspace first, so the model must hold the document, not grep it (AA-LCR
style: aggregation and multi-hop, not a single needle). Vision uses the
golden images in mengine_bench/assets/vision.
"""

from __future__ import annotations

import json
import random
import shutil
from collections.abc import Sequence
from datetime import date, timedelta
from pathlib import Path

from mengine_bench.core import (
    FAST,
    FULL,
    CheckResult,
    EvalTask,
    Step,
    answer_json,
    close,
    has,
    write,
)

ASSETS = Path(__file__).resolve().parents[1] / "assets" / "vision"
# Same list length as the v1 suite so the seeded draws (and the gold) keep their shape.
APPROVERS = ["Alice Sato", "Bruno Brandao", "Carla Quintela", "Diego Mello", "Elena Reis"]
CHANGES = [
    "lobby: region filter persists across sessions", "HUD: ammo counter with outline",
    "audio: footsteps occluded on Neoplastic", "net: delta compression on the player snapshot",
    "bots: patrol avoids the corners of the Broadway map", "UI: weapon tooltip shows DPS",
    "perf: culling of distant decals", "anticheat: heartbeat every 30 s",
    "store: 3D skin preview", "matchmaking: region weight 0.7",
]

# ------------------------------------------------------------ lc-changelog --

CHANGELOG_GOLD = {"build_change": "0.9.214", "build_revert": "0.9.377", "builds_between": 162}


def _changelog() -> tuple[str, dict[str, object]]:
    rng = random.Random(6332)
    day = date(2025, 9, 1)
    lines = ["# Pixel Arena - internal changelog for the 0.9 line\n"]
    revert_meta: dict[str, object] = {}
    for n in range(1, 641):
        day += timedelta(days=rng.choice([0, 1, 1, 2]))
        approver = rng.choice(APPROVERS)
        items = rng.sample(CHANGES, 2)
        if n == 180:
            items.append("tuning: recoil_multiplier_ads 1.0 -> 0.85 (aim)")
        if n == 214:
            items.append("tuning: recoil_multiplier 1.0 -> 0.85 (SMG, all modes)")
        if n == 377:
            items.append("revert: recoil_multiplier back from 0.85 to 1.0 (ranked complaints)")
            revert_meta = {"revert_date": day.isoformat(), "revert_approver": approver}
        if n == 402:
            items.append("tuning: recoil_multiplier_sniper 1.2 -> 1.1")
        lines.append(f"### Build 0.9.{n} - {day.isoformat()} - approved by {approver}")
        lines.extend(f"- {item}" for item in items)
        lines.append("")
    return "\n".join(lines) + "\n", {**CHANGELOG_GOLD, **revert_meta}


def _changelog_setup(ws: Path) -> None:
    write(ws, "_inline/changelog.md", _changelog()[0])


def _changelog_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    gold = _changelog()[1]
    got = answer_json(answers)
    result.add("build that changed recoil_multiplier (not _ads)", str(got.get("build_change")) == gold["build_change"])
    result.add("build that reverted it", str(got.get("build_revert")) == gold["build_revert"])
    result.add("revert date", str(got.get("revert_date")) == gold["revert_date"])
    result.add("revert approver", str(got.get("revert_approver", "")).strip().lower() == str(gold["revert_approver"]).lower())
    result.add("builds between the two (exclusive)", close(got.get("builds_between"), 162, 0))
    return result


def _changelog_reference(ws: Path) -> list[str]:
    return [json.dumps(_changelog()[1])]


# ------------------------------------------------------------- lc-contract --

CONTRACT_TOTAL = round(37 * 165 * 12 * 0.90 * 0.95, 2)


def _contract() -> str:
    rng = random.Random(6333)
    boiler = [
        "The parties undertake to comply with the provisions of this instrument in good faith, subject to applicable law.",
        "No tolerance by one party of a breach by the other shall constitute novation or waiver of rights.",
        "Notices shall be given in writing, by email with read receipt, to the addresses in the preamble.",
        "The PROVIDER shall maintain security controls consistent with ISO/IEC 27001 throughout the term.",
        "Personal data shall be processed under the LGPD, as processor, solely to provide the service.",
        "The monthly service level is 99.5% availability, excluding announced maintenance windows.",
        "SLA credits do not accumulate and are limited to 10% of the fee for the affected month.",
        "The chosen venue is the courts of Belo Horizonte/MG, waiving any other.",
    ]
    key = {
        7: "7.1 The Pro plan seat price is BRL 180.00 per month per seat. 7.2 The Team plan costs BRL 95.00 per month per seat.",
        14: "14.1 Volume discount on the current list price: 10% for 25 to 49 seats; 15% for 50 or more seats.",
        22: "22.1 Annual prepayment receives an additional 5% discount, applied AFTER the volume discount.",
    }
    sections = []
    for number in range(1, 46):
        paras = [rng.choice(boiler) for _ in range(rng.randint(16, 24))]
        if number in key:
            paras.insert(rng.randint(3, len(paras) - 3), key[number])
        sections.append(f"## Clause {number}\n\n" + "\n\n".join(f"{number}.{i + 10} {p}" for i, p in enumerate(paras)))
    annexes = [
        "## Annex B - UNSIGNED DRAFT\n\nCommercial proposal under negotiation: Pro at BRL 150.00 per seat. "
        "This annex has no effect without the signature of the parties.",
        "## Annex C - Amendment signed on 2026-03-15\n\nC.1 From 2026-04-01 the list price of the Pro seat becomes "
        "BRL 165.00 per month, replacing clause 7.1. All other clauses remain unchanged.",
    ]
    return "# SaaS license agreement - Kestrel Games x Arena Tools\n\n" + "\n\n".join(sections + annexes) + "\n"


def _contract_setup(ws: Path) -> None:
    write(ws, "_inline/contract.md", _contract())


def _contract_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    got = answer_json(answers)
    result.add("current unit price (amendment C, not draft B)", close(got.get("seat_price_month"), 165.0, 0.01))
    result.add("applicable volume discount", close(got.get("volume_discount_pct"), 10.0, 0.01))
    result.add("total annual cost", close(got.get("annual_cost"), CONTRACT_TOTAL, 0.5))
    return result


def _contract_reference(ws: Path) -> list[str]:
    return [json.dumps({"seat_price_month": 165, "volume_discount_pct": 10, "annual_cost": CONTRACT_TOTAL})]


# ----------------------------------------------------------------- vision --


def _copy_assets(ws: Path, *names: str) -> None:
    for name in names:
        target = ws / "images" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ASSETS / name, target)


def _chart_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    got = answer_json(answers)
    result.add("GPU with the highest TPS", has(str(got.get("top_gpu", "")), r"B200"))
    result.add("value of the tallest bar", close(got.get("top_tps"), 210, 0))
    result.add("GPU with the lowest TPS", has(str(got.get("bottom_gpu", "")), r"A100"))
    result.add("ratio top/bottom (2 decimals)", close(got.get("ratio"), 210 / 71, 0.011))
    return result


VISION_PROMPT = "Reply ONLY with a JSON object. The image(s) are attached."
LC_PROMPT = "Reply ONLY with a JSON object. The document is below; it is not on disk."

# par_s: DeepSeek V4.1 Flash wall times from the maintainers' v1 FAST run
# (2026-09-23), rounded up. lc-contract was not in that run: 2x lc-changelog
# (3.6 s), the closest long-context task.
TASKS = [
    EvalTask(
        id="lc-changelog", category="long-context", suites=frozenset({FAST, FULL}),
        provenance="AA-LCR style multi-hop over a long build changelog with near-duplicate distractor keys",
        summary="Find the change and revert of a parameter in a 640-build changelog and cross-reference date/approver",
        setup=_changelog_setup, check=_changelog_check, reference=_changelog_reference, timeout_s=300, par_s=4,
        steps=(Step("Keys: build_change (build that changed recoil_multiplier from 1.0 to 0.85; beware of parameters "
                    "with similar names), build_revert (build that set it back to 1.0), revert_date (YYYY-MM-DD), "
                    "revert_approver, builds_between (how many builds lie between the two, exclusive). " + LC_PROMPT,
                    inline=("_inline/changelog.md",), hide=("_inline",)),),
    ),
    EvalTask(
        id="lc-contract", category="long-context", suites=frozenset({FULL}),
        provenance="Contract review over a long agreement: price amendment supersedes a clause, unsigned draft is a trap",
        summary="Compute the annual cost of 37 seats in a long contract with an amendment and a trap draft",
        setup=_contract_setup, check=_contract_check, reference=_contract_reference, timeout_s=600, par_s=8,
        steps=(Step("Kestrel Games will buy 37 seats of the Pro plan, with annual prepayment, for 12 months starting "
                    "2026-05-01. Keys: seat_price_month (current list price), volume_discount_pct, annual_cost (final "
                    "amount in BRL, 2 decimals). " + LC_PROMPT,
                    inline=("_inline/contract.md",), hide=("_inline",)),),
    ),
    EvalTask(
        id="vis-chart", category="vision", suites=frozenset({FAST, FULL}), needs=frozenset({"vision"}),
        provenance="ChartQA style bar chart (golden image chart.png)",
        summary="Read a bar chart: highest/lowest GPU, value and ratio",
        setup=lambda ws: _copy_assets(ws, "chart.png"), check=_chart_check,
        reference=lambda ws: [json.dumps({"top_gpu": "B200", "top_tps": 210, "bottom_gpu": "A100", "ratio": 2.96})],
        timeout_s=240, par_s=3,
        steps=(Step("Keys: top_gpu, top_tps, bottom_gpu, ratio (top_tps / bottom_tps, 2 decimals). " + VISION_PROMPT,
                    attach=("images/chart.png",)),),
    ),
]
