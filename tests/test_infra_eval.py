"""#124: infra-gpu-fit grades the sizes and the one cheapest offer the policy allows."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.tasks import infra

TASK = next(task for task in catalog.all_tasks() if task.id == "infra-gpu-fit")
GOOD = {"weights_gb": 70, "kv_cache_gb": 42.95, "total_gb": 120.95, "offer_id": "of-117",
        "usd_per_hour": 3.58, "usd_per_month": 2613.4}


def _deliver(ws: Path, payload: object) -> None:
    (ws / "result.json").write_text(json.dumps(payload), encoding="utf-8")


def _workspace(tmp_path: Path) -> Path:
    TASK.setup(tmp_path)
    return tmp_path


def test_the_reference_passes_and_the_untouched_folder_fails(tmp_path: Path) -> None:
    (tmp_path / "bare").mkdir()
    (tmp_path / "solved").mkdir()
    TASK.setup(tmp_path / "bare")
    bare = TASK.check(tmp_path / "bare", [""])
    assert not bare.passed and bare.score == 0
    TASK.setup(tmp_path / "solved")
    result = TASK.check(tmp_path / "solved", TASK.reference(tmp_path / "solved"))
    assert result.passed, result.failed()


def test_the_fixture_has_one_cheapest_feasible_offer() -> None:
    exp = infra._gpu_fit_expected()
    assert exp["offer_id"] == infra.GPU_FIT_ANSWER
    cheaper = [row for row in infra.GPU_FIT_OFFERS if row[6] < float(exp["usd_per_hour"])]
    # Every cheaper offer breaks exactly one rule: stock, region or memory once the KV cache counts.
    reasons = {row[0]: (row[7] != "yes", row[2] not in infra.GPU_FIT_REGIONS, row[4] * row[5] < float(exp["total_gb"]))
               for row in cheaper}
    assert all(sum(broken) == 1 for broken in reasons.values()), reasons
    assert any(row[4] * row[5] >= float(exp["weights_gb"]) + infra.GPU_FIT_OVERHEAD_GB for row in cheaper
               if row[4] * row[5] < float(exp["total_gb"]))


@pytest.mark.parametrize("payload", [
    GOOD,
    {**GOOD, "weights_gb": "70 GB", "kv_cache_gb": "42.9 GB", "total_gb": "121 GB", "offer_id": " OF-117 ",
     "usd_per_hour": "US$ 3.58", "usd_per_month": "US$ 2,613.40"},
    {**GOOD, "kv_cache_gb": 42.94967296, "total_gb": "120,95", "usd_per_month": "2613"},
])
def test_every_valid_format_passes(tmp_path: Path, payload: dict[str, object]) -> None:
    ws = _workspace(tmp_path)
    _deliver(ws, payload)
    result = TASK.check(ws, [""])
    assert result.passed, (result.failed(), result.details)


@pytest.mark.parametrize(("key", "wrong", "check"), [
    ("weights_gb", 140, "weights size"),
    ("weights_gb", 65.19, "weights size"),
    ("kv_cache_gb", 40.0, "KV cache size"),
    ("kv_cache_gb", 10.74, "KV cache size"),
    ("total_gb", 78, "total memory needed"),
    ("offer_id", "of-101", "cheapest feasible offer"),
    ("offer_id", "of-108", "cheapest feasible offer"),
    ("offer_id", "of-111", "cheapest feasible offer"),
    ("offer_id", "of-120", "cheapest feasible offer"),
    ("usd_per_hour", 1.79, "hourly price"),
    ("usd_per_month", 2490.12, "monthly price"),
])
def test_each_check_fails_on_its_own_wrong_answer(tmp_path: Path, key: str, wrong: object, check: str) -> None:
    ws = _workspace(tmp_path)
    _deliver(ws, {**GOOD, key: wrong})
    result = TASK.check(ws, [""])
    assert result.failed() == [check], result.failed()
    assert check in result.details


def test_the_brief_does_not_hand_over_the_rules() -> None:
    prompt = TASK.steps[0].prompt.lower()
    for word in ("stock", "region", "4/h", "us$ 4", "730", "tensor", "1e9", "10^9", "of-117", "h100"):
        assert word not in prompt, word
    for key in GOOD:
        assert key in prompt, key


def test_a_correct_answer_only_in_the_chat_earns_nothing(tmp_path: Path) -> None:
    ws = _workspace(tmp_path)
    result = TASK.check(ws, [json.dumps(GOOD)])
    assert not result.passed and result.score == 0
