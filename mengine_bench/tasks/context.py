"""Long-context and vision tasks.

Long context goes INLINE in the prompt and the source file leaves the
workspace first, so the model must hold the document, not grep it (AA-LCR
style: aggregation and multi-hop, not a single needle). Vision uses the
golden images in mengine_bench/assets/vision.
"""

from __future__ import annotations

import json
import random
import re
import shutil
from collections.abc import Sequence
from datetime import date, timedelta
from pathlib import Path

from mengine_bench.core import (
    CheckResult,
    EvalTask,
    Step,
    answer_json,
    close,
    has,
    only_number,
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
    # #59: the format is the judge's to grade; here it counts that the answer names that one build.
    texts = {key: json.dumps(got.get(key, "")) for key in ("build_change", "build_revert")}
    builds = {key: [] if has(text, r"\bnot") else re.findall(r"\d+\.\d+\.\d+", text) for key, text in texts.items()}
    result.add("build that changed recoil_multiplier (not _ads)", builds["build_change"] == [gold["build_change"]])
    result.add("build that reverted it", builds["build_revert"] == [gold["build_revert"]])
    result.add("revert date", str(got.get("revert_date")) == gold["revert_date"])
    result.add("revert approver", str(got.get("revert_approver", "")).strip().lower() == str(gold["revert_approver"]).lower())
    result.add("builds between the two (exclusive)", close(only_number(got.get("builds_between")), 162, 0))
    return result


def _changelog_reference(ws: Path) -> list[str]:
    return [json.dumps(_changelog()[1])]


# ----------------------------------------------------------------- vision --


def _copy_assets(ws: Path, *names: str) -> None:
    for name in names:
        target = ws / "images" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ASSETS / name, target)


def _gpu_name(value: object) -> str:
    # #28: the chart labels say "B200"; "NVIDIA B200" or "A100 GPU" name the same bar.
    name = "".join(str(value or "").split()).upper()
    return re.sub(r"GPU$", "", re.sub(r"^(NVIDIA)?(TESLA)?", "", name))


def _chart_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    got = answer_json(answers)
    # #59: read from the axis, so the values take a reading margin of a fifth of a grid step. The 8k bars answer
    # differently, and the old chart printed sorted values that no run in 16 got wrong.
    result.add("GPU with the highest TPS at 256k", _gpu_name(got.get("top_gpu")) == "H200")
    result.add("value of that bar", close(only_number(got.get("top_tps")), 180, 10))
    result.add("GPU with the lowest TPS at 256k", _gpu_name(got.get("bottom_gpu")) == "4090")
    result.add("ratio top/bottom", close(only_number(got.get("ratio")), 6.0, 1.2))
    return result


VISION_PROMPT = "Reply ONLY with a JSON object. The image(s) are attached."
LC_PROMPT = "Reply ONLY with a JSON object. The document is below; it is not on disk."

TASKS = [
    EvalTask(
        id="lc-changelog", category="long-context",
        provenance="AA-LCR style multi-hop over a long build changelog with near-duplicate distractor keys",
        summary="Find when a setting changed and was restored in a long changelog, including who approved the change.",
        setup=_changelog_setup, check=_changelog_check, reference=_changelog_reference, timeout_s=120,
        steps=(Step("Keys: build_change (build that changed recoil_multiplier from 1.0 to 0.85; beware of parameters "
                    "with similar names), build_revert (build that set it back to 1.0), revert_date (YYYY-MM-DD), "
                    "revert_approver, builds_between (how many builds lie between the two, exclusive). " + LC_PROMPT,
                    inline=("_inline/changelog.md",), hide=("_inline",)),),
    ),
    EvalTask(
        id="vis-chart", category="vision", needs=frozenset({"vision"}),
        provenance="ChartQA style bar chart (golden image chart.png)",
        summary="Read a bar chart to identify the fastest and slowest GPUs and compare their speeds.",
        setup=lambda ws: _copy_assets(ws, "chart.png"), check=_chart_check,
        reference=lambda ws: [json.dumps({"top_gpu": "H200", "top_tps": 180, "bottom_gpu": "4090", "ratio": 6.0})],
        timeout_s=120,
        steps=(Step("Use only the 256k context bars. Keys: top_gpu (highest TPS), top_tps (its value), bottom_gpu "
                    "(lowest TPS), ratio (top TPS / bottom TPS). " + VISION_PROMPT,
                    attach=("images/chart.png",)),),
    ),
]
