"""The board's estimated price: a run's tokens at public API list prices, never part of the Score (#76)."""

from __future__ import annotations

from mengine_bench.prices import LIST_PRICES, estimated_usd, price_text


def _result(model: str, input_tokens: int, cached: int, output: int, generated: int | None = None,
            **fields: object) -> dict[str, object]:
    totals: dict[str, object] = {"tokens": {"input": input_tokens, "cached_input": cached, "output": output, "reasoning": 0}}
    if generated is not None:
        totals["stats"] = {"generated_tokens": generated}
    return {"agent": {"model": model}, "totals": totals, **fields}


def test_the_claude_estimate_matches_what_the_harness_reported() -> None:
    # Published runs: Opus low reported $5.1489, Sonnet medium $2.0348 in total_cost_usd.
    opus = _result("claude-opus-5-5", 2_423_493, 2_013_287, 73_256)
    sonnet = _result("claude-sonnet-5-5", 1_747_511, 1_404_619, 52_300)
    assert abs(estimated_usd(opus) - 5.1489) < 0.01
    assert abs(estimated_usd(sonnet) - 2.0348) < 0.01


def test_reasoning_reported_apart_from_output_is_billed_as_output() -> None:
    # opencode counts it apart; stats.generated_tokens holds both on every harness.
    run = _result("zai/glm-5.3-flash", 1_000_000, 0, 10_000, generated=1_000_000)
    assert estimated_usd(run) == 0.65


def test_cached_tokens_pay_the_cached_price() -> None:
    assert estimated_usd(_result("deepseek/deepseek-flash", 1_000_000, 1_000_000, 0)) == 0.003


def test_the_fast_tier_costs_what_openai_lists_for_it() -> None:
    standard = _result("gpt-6.1-sol", 1_000_000, 0, 1_000_000)
    fast = _result("gpt-6.1-sol", 1_000_000, 0, 1_000_000, config={"service_tier": "fast"})
    assert estimated_usd(standard) == 12.0
    assert estimated_usd(fast) == 24.0
    assert estimated_usd(_result("gpt-6-astra", 1_000_000, 0, 0, config={"service_tier": "fast"})) == 20.0


def test_every_model_on_the_board_has_a_price() -> None:
    assert set(LIST_PRICES) == {"claude-opus-5-5", "claude-sonnet-5-5", "gpt-6-astra", "gpt-6.1-sol", "zai/glm-5.3-flash",
                                "deepseek/deepseek-flash", "gemini-4-argon"}


def test_the_cell_says_it_is_an_estimate() -> None:
    assert price_text(_result("claude-sonnet-5-5", 1_747_511, 1_404_619, 52_300)) == "~$2.04"


def test_a_cent_is_the_smallest_estimate_shown() -> None:
    assert price_text(_result("deepseek/deepseek-flash", 1_000, 1_000, 0)) == "< $0.01"


def test_a_model_with_no_known_price_is_not_shown_as_free() -> None:
    assert estimated_usd(_result("someone/else", 1_000, 0, 1_000)) is None
    assert price_text(_result("someone/else", 1_000, 0, 1_000)) == "n/a"


def test_a_run_without_tokens_has_no_estimate() -> None:
    assert price_text({"agent": {"model": "gpt-6.1-sol"}, "totals": {"tokens": None}}) == "n/a"


def test_local_inference_declared_free_says_so() -> None:
    free = {"input": 0.0, "cached": 0.0, "output": 0.0}
    assert price_text(_result("home/qwen38-flash-next-exl3-605-256k", 1_000, 0, 1_000, price_per_mtok=free)) == "$0.00 (local)"
