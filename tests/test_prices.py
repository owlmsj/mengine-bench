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
    terra_fast = _result("gpt-6.1-terra", 1_000_000, 0, 1_000_000, config={"service_tier": "fast"})
    assert estimated_usd(terra_fast) == 12.0


def test_every_model_on_the_board_has_a_price() -> None:
    assert set(LIST_PRICES) == {"claude-opus-5-5", "claude-sonnet-5-5", "gpt-6-astra", "gpt-6.1-sol", "gpt-6.1-terra",
                                "zai/glm-5.3-flash", "deepseek/deepseek-flash", "gemini-4-argon"}


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


def test_declared_price_estimates_the_existing_token_scope() -> None:
    declared = {'input': 0.15, 'cached': 0.016, 'output': 0.47}
    run = _result('unknown/model', 1_000_000, 500_000, 10, generated=100_000, price_per_mtok=declared)
    assert estimated_usd(run) == 0.13
    assert price_text(run) == '~$0.13'


def test_declared_price_overrides_list_price_and_zero_stays_local() -> None:
    run = _result('gpt-6-astra', 1_000_000, 0, 1_000_000,
                  price_per_mtok={'input': 1.0, 'cached': 0.1, 'output': 2.0})
    assert estimated_usd(run) == 3.0
    run['price_per_mtok'] = {'input': 0.0, 'cached': 0.0, 'output': 0.0}
    assert estimated_usd(run) == 0.0
    assert price_text(run) == '$0.00 (local)'


def test_run_cost_snapshot_is_stable_after_price_table_changes(monkeypatch) -> None:
    from mengine_bench.prices import finalize_run_cost, run_cost_text
    result = _result("gpt-6.1-terra", 1_000_000, 0, 100_000)
    result["totals"].update(cost_usd=None, cost_basis="n/a", cost_lower_bound=False)
    result["tasks"] = [{"steps": [{"usage": {"input_tokens": 1_000_000, "cached_input_tokens": 0, "output_tokens": 100_000,
                                                "cost_usd": None}}]}]
    finalize_run_cost(result)
    assert result["totals"]["cost_basis"] == "list-price"
    assert result["totals"]["cost_usd"] == 1.5
    assert result["cost_price"]["source_url"] and result["cost_price"]["read_date"]
    monkeypatch.setitem(LIST_PRICES, "gpt-6.1-terra", LIST_PRICES["gpt-6-astra"])
    assert run_cost_text(result) == "~$1.50"


def test_partial_harness_cost_stays_a_lower_bound() -> None:
    from mengine_bench.prices import finalize_run_cost, run_cost_text
    result = _result("gpt-6.1-terra", 1_000_000, 0, 100_000)
    result["totals"].update(cost_usd=None, cost_basis="n/a", cost_lower_bound=False)
    result["tasks"] = [{"steps": [{"usage": {"input_tokens": 100, "cached_input_tokens": 0, "output_tokens": 10, "cost_usd": 0.25}},
                                    {"usage": {"input_tokens": 100, "cached_input_tokens": 0, "output_tokens": 10, "cost_usd": None}}]}]
    finalize_run_cost(result)
    assert run_cost_text(result) == ">= $0.25"


def test_missing_usage_is_not_priced_as_zero() -> None:
    from mengine_bench.prices import finalize_run_cost, run_cost_text
    result = _result("gpt-6.1-terra", 0, 0, 0)
    result["totals"].update(cost_usd=None, cost_basis="n/a", cost_lower_bound=True)
    result["tasks"] = [{"steps": [{"usage": None}]}]
    finalize_run_cost(result)
    assert result["totals"]["cost_usd"] is None
    assert run_cost_text(result) == "n/a"


def test_bundle_and_redo_use_the_snapshotted_rate_after_table_changes(monkeypatch) -> None:
    from mengine_bench import redo
    from mengine_bench.report import RunMeta, build_results, render_summary, usage_record
    from mengine_bench.runner.agents import Usage
    from mengine_bench.runner.stats import RunStats
    from mengine_bench.scoring import TaskOutcome, score_run

    usage = Usage(1_000_000, 0, 100_000, None, None, "none")
    outcome = TaskOutcome("task", "ok", 1.0, True, 10.0, step_usages=(usage,))
    detail = {"steps": [{"usage": usage_record(usage)}], "grading_s": 0.0, "checks": [], "flags": [],
              "error": None, "answers": [], "usage": usage_record(usage), "stats": RunStats()}
    meta = RunMeta("2026-11-07", "codex", "gpt-6.1-terra", "low", None, "run", "start", "end")
    result = build_results(meta, score_run([outcome]), {"task": detail}, {}, {})
    assert result["totals"]["cost_usd"] == 1.5
    assert result["totals"]["cost_basis"] == "list-price"
    assert "~$1.50" in render_summary(result)
    original = result["cost_price"].copy()
    monkeypatch.setitem(LIST_PRICES, "gpt-6.1-terra", LIST_PRICES["gpt-6-astra"])
    redo._rescore(result, None)
    assert result["cost_price"] == original
    assert result["totals"]["cost_usd"] == 1.5
    assert "~$1.50" in render_summary(result)


def test_unpriced_model_warns_and_never_invents_cost() -> None:
    from mengine_bench.prices import finalize_run_cost, missing_price_warning, run_cost_text
    result = _result("unknown/model", 1000, 0, 100)
    result["totals"].update(cost_usd=None, cost_basis="n/a")
    result["tasks"] = [{"steps": [{"usage": {"input_tokens": 1000, "cached_input_tokens": 0, "output_tokens": 100, "cost_usd": None}}]}]
    finalize_run_cost(result)
    assert run_cost_text(result) == "n/a"
    assert missing_price_warning("unknown/model", {}) == "no list price for unknown/model; add it to prices.py"


def test_price_rows_have_provider_and_observation_date() -> None:
    from mengine_bench.prices import FAST_PRICES
    for price in (*LIST_PRICES.values(), *FAST_PRICES.values()):
        assert price.source_url.startswith("https://")
        assert price.read_date == "2026-11-07"


def test_summary_warns_for_unpriced_tokens_but_not_for_missing_usage(tmp_path) -> None:
    from mengine_bench.report import render_summary
    from test_bundle_leaderboard import _write_result
    import json
    bundle = _write_result(tmp_path / "results", "run", 90.0, model="unknown/model")
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    result["tasks"] = []
    result["totals"].update(cost_usd=None, cost_basis="n/a")
    assert "no list price for unknown/model; add it to prices.py" in render_summary(result)
    result["totals"]["tokens"] = None
    result["totals"]["stats"] = {}
    assert "no list price" not in render_summary(result)


def test_harness_cost_wins_over_available_price() -> None:
    from mengine_bench.prices import finalize_run_cost, run_cost_text
    result = _result("gpt-6.1-terra", 1_000_000, 0, 100_000)
    result["totals"].update(cost_usd=3.25, cost_basis="harness", cost_lower_bound=False)
    result["tasks"] = [{"steps": [{"usage": {"input_tokens": 1_000_000, "cached_input_tokens": 0, "output_tokens": 100_000,
                                                "cost_usd": 3.25}}]}]
    finalize_run_cost(result)
    assert run_cost_text(result) == "$3.25"
    assert "cost_price" not in result


def test_fast_tier_is_snapshotted_and_zero_price_remains_local() -> None:
    from mengine_bench.prices import finalize_run_cost, run_cost_text
    result = _result("gpt-6.1-terra", 1_000_000, 0, 100_000, config={"service_tier": "fast"})
    result["totals"].update(cost_usd=None, cost_basis="n/a", cost_lower_bound=False)
    result["tasks"] = [{"steps": [{"usage": {"input_tokens": 1_000_000, "cached_input_tokens": 0, "output_tokens": 100_000,
                                                "cost_usd": None}}]}]
    finalize_run_cost(result)
    assert result["cost_price"]["tier"] == "fast"
    assert run_cost_text(result) == "~$3.00"
    result["price_per_mtok"] = {"input": 0.0, "cached": 0.0, "output": 0.0}
    assert run_cost_text(result) == "$0.00 (local)"


def test_zero_harness_with_declared_price_is_snapshotted_even_below_one_cent() -> None:
    from mengine_bench.prices import finalize_run_cost, run_cost_text
    result = _result("unpriced/model", 1000, 0, 0, price_per_mtok={"input": 1.0, "cached": 0.1, "output": 5.0})
    result["totals"].update(cost_usd=0.0, cost_basis="harness", cost_lower_bound=True)
    result["tasks"] = [{"steps": [{"usage": {"input_tokens": 1000, "cached_input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}}]}]
    finalize_run_cost(result)
    assert result["totals"]["cost_basis"] == "price"
    assert result["totals"]["cost_usd"] == 0.001
    assert run_cost_text(result) == ">= ~$0.001"


def test_zero_tokens_do_not_become_a_list_price_cost() -> None:
    from mengine_bench.prices import finalize_run_cost, run_cost_text
    result = _result("gpt-6.1-terra", 0, 0, 0)
    result["totals"].update(cost_usd=None, cost_basis="n/a", cost_lower_bound=False)
    result["tasks"] = [{"steps": [{"usage": {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0, "cost_usd": None}}]}]
    finalize_run_cost(result)
    assert result["totals"]["cost_usd"] is None
    assert run_cost_text(result) == "n/a"


def test_cli_preflight_warns_about_unpriced_model(capsys, monkeypatch) -> None:
    from mengine_bench import cli
    monkeypatch.setattr(cli, "shell_problems", lambda: [])
    assert cli.main(["run", "--agent", "codex", "--model", "unpriced/model", "--dry-run"]) == 0
    import json
    plan = json.loads(capsys.readouterr().out)
    assert plan["warnings"] == ["no list price for unpriced/model; add it to prices.py"]


def test_summary_warns_when_only_generated_tokens_are_reported(tmp_path) -> None:
    import json
    from mengine_bench.report import render_summary
    from test_bundle_leaderboard import _write_result
    bundle = _write_result(tmp_path / "results", "run", 90.0, model="unknown/model")
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    result["tasks"] = []
    result["totals"].update(cost_usd=None, cost_basis="n/a", tokens={"input": 0, "output": 0},
                            stats={"generated_tokens": 100})
    assert "no list price for unknown/model" in render_summary(result)


def test_declared_price_counts_all_generated_tokens_in_persisted_total() -> None:
    from mengine_bench.prices import finalize_run_cost, run_cost_text
    result = _result("model", 1_000_000, 0, 10_000, generated=100_000,
                     price_per_mtok={"input": 1.0, "cached": 0.1, "output": 5.0})
    result["totals"].update(cost_usd=1.05, cost_basis="price", cost_lower_bound=False)
    result["tasks"] = [{"stats": {"generated_tokens": 100_000}, "steps": [{"usage": {"input_tokens": 1_000_000, "cached_input_tokens": 0, "output_tokens": 10_000,
                                                "cost_usd": None}}]}]
    finalize_run_cost(result)
    assert result["totals"]["cost_usd"] == 1.5
    assert run_cost_text(result) == "~$1.50"


def test_partially_measured_tokens_produce_a_lower_bound() -> None:
    from mengine_bench.prices import finalize_run_cost, run_cost_text
    result = _result("gpt-6.1-terra", 1_000_000, 0, 0)
    result["totals"].update(cost_usd=None, cost_basis="n/a", cost_lower_bound=False)
    result["tasks"] = [{"steps": [{"usage": {"input_tokens": 1_000_000, "cached_input_tokens": 0, "output_tokens": None,
                                                "cost_usd": None}}]}]
    finalize_run_cost(result)
    assert result["totals"]["cost_usd"] == 1.0
    assert result["totals"]["cost_lower_bound"] is True
    assert run_cost_text(result) == ">= ~$1.00"


def test_bundle_prices_declared_generated_and_partial_tokens() -> None:
    from mengine_bench.report import RunMeta, build_results, render_summary, usage_record
    from mengine_bench.runner.agents import Usage
    from mengine_bench.runner.stats import RunStats
    from mengine_bench.scoring import Price, TaskOutcome, score_run

    for usage, stats, price, expected in [
        (Usage(1_000_000, 0, 10_000, 90_000, None, "none"), RunStats(generated_tokens=100_000),
         Price(1.0, 0.1, 5.0), "~$1.50"),
        (Usage(1_000_000, 0, None, None, None, "none"), RunStats(), None, ">= ~$1.00"),
    ]:
        outcome = TaskOutcome("task", "ok", 1.0, True, 10.0, step_usages=(usage,))
        detail = {"steps": [{"usage": usage_record(usage)}], "grading_s": 0.0, "checks": [], "flags": [],
                  "error": None, "answers": [], "usage": usage_record(usage), "stats": stats}
        meta = RunMeta("2026-11-07", "opencode", "gpt-6.1-terra", "low", None, "run", "start", "end", price=price)
        result = build_results(meta, score_run([outcome], price), {"task": detail}, {}, {})
        assert expected in render_summary(result)


def test_generated_only_usage_is_a_lower_bound_not_na() -> None:
    from mengine_bench.prices import finalize_run_cost, run_cost_text
    result = _result("gpt-6.1-terra", 0, 0, 0, generated=100_000)
    result["totals"].update(cost_usd=None, cost_basis="n/a", cost_lower_bound=True)
    result["tasks"] = [{"stats": {"generated_tokens": 100_000}, "steps": [{"usage": None}]}]
    finalize_run_cost(result)
    assert result["totals"]["cost_usd"] == 0.5
    assert run_cost_text(result) == ">= ~$0.50"


def test_known_cache_without_input_never_produces_a_negative_cost() -> None:
    from mengine_bench.report import RunMeta, build_results, render_summary, usage_record
    from mengine_bench.runner.agents import Usage
    from mengine_bench.runner.stats import RunStats
    from mengine_bench.scoring import TaskOutcome, score_run
    usage = Usage(None, 1_000_000, 100_000, None, None, "none")
    outcome = TaskOutcome("task", "ok", 1.0, True, 10.0, step_usages=(usage,))
    detail = {"steps": [{"usage": usage_record(usage)}], "grading_s": 0.0, "checks": [], "flags": [],
              "error": None, "answers": [], "usage": usage_record(usage), "stats": RunStats()}
    meta = RunMeta("2026-11-07", "codex", "gpt-6.1-terra", "low", None, "run", "start", "end")
    result = build_results(meta, score_run([outcome]), {"task": detail}, {}, {})
    assert result["totals"]["cost_usd"] == 0.55
    assert ">= ~$0.55" in render_summary(result)


def test_cache_only_usage_is_a_lower_bound() -> None:
    from mengine_bench.prices import finalize_run_cost, run_cost_text
    result = _result("gpt-6.1-terra", 0, 1_000_000, 0)
    result["totals"].update(cost_usd=None, cost_basis="n/a", cost_lower_bound=False)
    result["tasks"] = [{"steps": [{"usage": {"input_tokens": None, "cached_input_tokens": 1_000_000,
                                                "output_tokens": None, "cost_usd": None}}]}]
    finalize_run_cost(result)
    assert result["totals"]["cost_usd"] == 0.05
    assert run_cost_text(result) == ">= ~$0.05"


def test_unknown_cache_prices_known_input_at_a_real_lower_bound() -> None:
    from mengine_bench.report import RunMeta, build_results, render_summary, usage_record
    from mengine_bench.runner.agents import Usage
    from mengine_bench.runner.stats import RunStats
    from mengine_bench.scoring import TaskOutcome, score_run
    usage = Usage(1_000_000, None, 0, None, None, "none")
    outcome = TaskOutcome("task", "ok", 1.0, True, 10.0, step_usages=(usage,))
    detail = {"steps": [{"usage": usage_record(usage)}], "grading_s": 0.0, "checks": [], "flags": [],
              "error": None, "answers": [], "usage": usage_record(usage), "stats": RunStats()}
    meta = RunMeta("2026-11-07", "codex", "gpt-6.1-terra", "low", None, "run", "start", "end")
    result = build_results(meta, score_run([outcome]), {"task": detail}, {}, {})
    assert result["totals"]["cost_usd"] == 0.05
    assert result["totals"]["cost_lower_bound"] is True
    assert ">= ~$0.05" in render_summary(result)


def test_partial_task_stats_do_not_drop_another_tasks_output() -> None:
    from mengine_bench.report import RunMeta, build_results, render_summary, usage_record
    from mengine_bench.runner.agents import Usage
    from mengine_bench.runner.stats import RunStats
    from mengine_bench.scoring import TaskOutcome, score_run
    usage = Usage(0, 0, 100_000, None, None, "none")
    outcomes = [TaskOutcome(name, "ok", 1.0, True, 10.0, step_usages=(usage,)) for name in ("a", "b")]
    def detail(stats):
        return {"steps": [{"usage": usage_record(usage)}], "grading_s": 0.0, "checks": [], "flags": [],
                "error": None, "answers": [], "usage": usage_record(usage), "stats": stats}
    details = {"a": detail(RunStats(generated_tokens=100_000)), "b": detail(RunStats())}
    meta = RunMeta("2026-11-07", "codex", "gpt-6.1-terra", "low", None, "run", "start", "end")
    result = build_results(meta, score_run(outcomes), details, {}, {})
    assert result["totals"]["cost_usd"] == 1.0
    assert "~$1.00" in render_summary(result)
