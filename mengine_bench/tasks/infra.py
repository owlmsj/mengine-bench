"""Infra task: rent the cheapest GPU offer that serves a model under a spending policy (#124).

Mirrors the owner's tier-3 rentals: size weights plus KV cache plus runtime overhead,
then filter offers by stock, region and the US$ 4/h cap. The docs fix GB = 1e9 bytes,
so there is one right size and one right offer; every decoy fails exactly one rule.
"""

from __future__ import annotations

import json
import re
from collections.abc import Sequence
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

GPU_FIT_PARAMS_B = 70
GPU_FIT_WEIGHT_BITS = 8
GPU_FIT_KV_BYTES_PER_TOKEN = 327_680  # 80 layers x 8 KV heads x 128 dims x (K, V) x 2 bytes.
GPU_FIT_CONTEXT_TOKENS = 32_768
GPU_FIT_SEQUENCES = 4
GPU_FIT_OVERHEAD_GB = 8.0
GPU_FIT_CAP_USD_H = 4.0
GPU_FIT_HOURS_PER_MONTH = 730
GPU_FIT_REGIONS = ("us-east", "us-central", "eu-west")
GPU_FIT_ANSWER = "of-117"

# (offer_id, provider, region, gpu, gpu_count, vram_gb_per_gpu, usd_per_hour, in_stock) and the one rule it breaks.
GPU_FIT_OFFERS: tuple[tuple[str, str, str, str, int, int, float, str], ...] = (
    ("of-101", "cloudnine", "us-east", "RTX PRO 6000", 1, 96, 1.79, "yes"),   # fits weights, not the KV cache
    ("of-104", "cloudnine", "us-east", "A100 80GB", 1, 80, 1.29, "yes"),      # fits weights, not the KV cache
    ("of-108", "gridrent", "eu-west", "H100 80GB", 2, 80, 3.10, "no"),        # out of stock
    ("of-111", "gridrent", "ap-southeast", "RTX PRO 6000", 2, 96, 2.98, "yes"),  # region not allowed
    ("of-113", "voltbay", "us-central", "L40S", 2, 48, 1.84, "yes"),          # short even before the KV cache
    ("of-117", "voltbay", "us-central", "H100 80GB", 2, 80, 3.58, "yes"),     # the answer
    ("of-120", "cloudnine", "eu-west", "H200", 1, 141, 3.79, "yes"),          # feasible, dearer
    ("of-124", "gridrent", "us-east", "L40S", 4, 48, 3.92, "yes"),            # feasible, dearer
    ("of-129", "voltbay", "us-east", "B200", 1, 180, 4.89, "yes"),            # feasible, over the cap
    ("of-133", "cloudnine", "us-central", "H200", 2, 141, 7.10, "yes"),       # feasible, over the cap
    ("of-137", "gridrent", "sa-east", "H100 80GB", 2, 80, 3.20, "yes"),       # region not allowed
)

GPU_FIT_MODEL_MD = f"""# Model to serve: arena-coder-70b

| property | value |
| --- | --- |
| parameters | {GPU_FIT_PARAMS_B} billion |
| weight precision | {GPU_FIT_WEIGHT_BITS}-bit (FP8) |
| KV cache | {GPU_FIT_KV_BYTES_PER_TOKEN:,} bytes per token (FP16, all layers, K and V) |
| context we want per sequence | {GPU_FIT_CONTEXT_TOKENS:,} tokens |
| concurrent sequences | {GPU_FIT_SEQUENCES} |
| runtime overhead | {GPU_FIT_OVERHEAD_GB:g} GB for the whole deployment (CUDA context, activations), whatever the GPU count |

Every sequence must be able to hold its full context at the same time.
The runtime shards weights and KV cache across all GPUs of one offer (tensor parallel),
so an offer's usable memory is gpu_count x vram_gb_per_gpu.

Units: GB = 10^9 bytes everywhere in these docs and in offers.csv.
"""

GPU_FIT_POLICY_MD = f"""# Rental policy

- Hourly cap: US$ {GPU_FIT_CAP_USD_H:g} per hour for the whole deployment. Nothing above it is rented.
- Rent only offers that are in stock now (`in_stock` = yes).
- Allowed regions: {", ".join(GPU_FIT_REGIONS)}.
- `usd_per_hour` in offers.csv is the price of the whole offer (all its GPUs), not per GPU.
- One offer per deployment; we do not combine offers.
- Monthly cost = hourly price x {GPU_FIT_HOURS_PER_MONTH} hours.
"""


def _gpu_fit_expected() -> dict[str, float | str]:
    weights = GPU_FIT_PARAMS_B * 1e9 * GPU_FIT_WEIGHT_BITS / 8 / 1e9
    kv = GPU_FIT_KV_BYTES_PER_TOKEN * GPU_FIT_CONTEXT_TOKENS * GPU_FIT_SEQUENCES / 1e9
    total = weights + kv + GPU_FIT_OVERHEAD_GB
    feasible = [row for row in GPU_FIT_OFFERS if row[7] == "yes" and row[2] in GPU_FIT_REGIONS
                and row[4] * row[5] >= total and row[6] <= GPU_FIT_CAP_USD_H]
    best = min(feasible, key=lambda row: row[6])
    return {"weights_gb": weights, "kv_cache_gb": kv, "total_gb": total, "offer_id": best[0],
            "usd_per_hour": best[6], "usd_per_month": best[6] * GPU_FIT_HOURS_PER_MONTH}


def _gpu_fit_setup(ws: Path) -> None:
    header = "offer_id,provider,region,gpu,gpu_count,vram_gb_per_gpu,usd_per_hour,in_stock\n"
    write(ws, "offers.csv", header + "".join(",".join(map(str, row)) + "\n" for row in GPU_FIT_OFFERS))
    write(ws, "MODEL.md", GPU_FIT_MODEL_MD)
    write(ws, "POLICY.md", GPU_FIT_POLICY_MD)


def _gpu_fit_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    exp = _gpu_fit_expected()
    got = result_json(ws)
    # #124: GB = 1e9 is fixed by MODEL.md, so a GiB answer (65.2 / 40.0) is a different number.
    result.add("weights size", near(got.get("weights_gb"), float(exp["weights_gb"]), 0.5),
               saw(got.get("weights_gb"), exp["weights_gb"]))
    result.add("KV cache size", near(got.get("kv_cache_gb"), float(exp["kv_cache_gb"]), 0.5),
               saw(got.get("kv_cache_gb"), round(float(exp["kv_cache_gb"]), 2)))
    result.add("total memory needed", near(got.get("total_gb"), float(exp["total_gb"]), 0.8),
               saw(got.get("total_gb"), round(float(exp["total_gb"]), 2)))
    offer = str(got.get("offer_id") or "").strip().lower()
    result.add("cheapest feasible offer", re.fullmatch(r"(offer[ _-]?)?of-117", offer) is not None,
               saw(got.get("offer_id"), exp["offer_id"]))
    result.add("hourly price", near(got.get("usd_per_hour"), float(exp["usd_per_hour"]), 0.005),
               saw(got.get("usd_per_hour"), exp["usd_per_hour"]))
    result.add("monthly price", near(got.get("usd_per_month"), float(exp["usd_per_month"]), 1.0),
               saw(got.get("usd_per_month"), round(float(exp["usd_per_month"]), 2)))
    return result


def _gpu_fit_reference(ws: Path) -> list[str]:
    exp = _gpu_fit_expected()
    write(ws, "result.json", json.dumps({key: round(value, 2) if isinstance(value, float) else value
                                         for key, value in exp.items()}))
    return ["done"]


TASKS = [
    EvalTask(
        id="infra-gpu-fit", category="infra",
        provenance="Renting GPUs to serve a 70B model under the owner's US$ 4/h cap (mengine tier 3, #623)",
        summary="Pick the cheapest rented GPU offer that can serve a model within a spending policy.",
        setup=_gpu_fit_setup, check=_gpu_fit_check, reference=_gpu_fit_reference, timeout_s=180,
        checkpoints=checkpoints(("read the offers", r"offers\.csv"), ("read the model", r"MODEL\.md"),
                                ("read the policy", r"POLICY\.md"), WROTE_RESULT),
        steps=(Step("We want to serve the model described in {WS}/MODEL.md on rented GPUs. Today's offers are in "
                    "{WS}/offers.csv and our rental rules in {WS}/POLICY.md. Pick the cheapest way to serve it under "
                    "the policy and justify the choice. Record it in {WS}/result.json with weights_gb, kv_cache_gb, "
                    "total_gb, offer_id, usd_per_hour and usd_per_month."),),
    ),
]
