"""The board's estimated Cost: a run's tokens at public API list prices (#76, #162).

A subscription hides what a run would cost, so the Cost column is mostly n/a. This
puts every run on one scale; it never counts toward the Score. USD per million
tokens, read on 2026-10-31 from each provider's pricing page (docs/SCORING.md).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class ListPrice:
    input: float
    cached: float
    output: float
    source_url: str = ""
    read_date: str = ""


ANTHROPIC_PRICING = "https://platform.claude.com/docs/en/about-claude/pricing"
OPENAI_PRICING = "https://developers.openai.com/api/docs/pricing"
ZAI_PRICING = "https://docs.z.ai/guides/overview/pricing"
DEEPSEEK_PRICING = "https://api-docs.deepseek.com/quick_start/pricing/"
GOOGLE_PRICING = "https://ai.google.dev/gemini-api/docs/pricing"
PRICE_READ_DATE = "2026-11-07"
PRICE_READ_DATE_1110 = "2026-11-10"
PRICE_READ_DATE_1113 = "2026-11-13"

LIST_PRICES: Mapping[str, ListPrice] = {
    # Input at the 1 h cache write price: Claude Code caches nearly all its uncached input.
    # On the published Opus and Sonnet runs this lands within 0.1% of total_cost_usd.
    "claude-opus-5-5": ListPrice(8.0, 0.20, 20.0, ANTHROPIC_PRICING, PRICE_READ_DATE),
    "claude-sonnet-5-5": ListPrice(4.0, 0.10, 10.0, ANTHROPIC_PRICING, PRICE_READ_DATE),
    "claude-fable-5-2": ListPrice(16.0, 0.20, 40.0, ANTHROPIC_PRICING, PRICE_READ_DATE_1110),
    "gpt-6-astra": ListPrice(10.0, 1.0, 50.0, OPENAI_PRICING, PRICE_READ_DATE),
    "gpt-6.1-sol": ListPrice(2.0, 0.10, 10.0, OPENAI_PRICING, PRICE_READ_DATE),
    "gpt-6.1-terra": ListPrice(1.0, 0.05, 5.0, OPENAI_PRICING, PRICE_READ_DATE),
    "zai/glm-5.3-flash": ListPrice(0.15, 0.03, 0.50, ZAI_PRICING, PRICE_READ_DATE),
    # Off-peak; peak hours cost twice this. Gemini's rise on 2026-12-01 is not applied.
    "deepseek/deepseek-flash": ListPrice(0.15, 0.003, 0.60, DEEPSEEK_PRICING, PRICE_READ_DATE),
    "gemini-4-argon": ListPrice(2.0, 0.10, 10.0, GOOGLE_PRICING, PRICE_READ_DATE),
    "gemini-4-carbon": ListPrice(2.0, 0.10, 10.0, GOOGLE_PRICING, PRICE_READ_DATE_1110),
    # Implicit caching only; no date range on the AI Studio page.
    "gemini-4-hydrogen": ListPrice(1.50, 0.075, 7.50, GOOGLE_PRICING, PRICE_READ_DATE_1113),
}
FAST_PRICES: Mapping[str, ListPrice] = {
    "gpt-6-astra": ListPrice(20.0, 2.0, 100.0, OPENAI_PRICING, PRICE_READ_DATE),
    "gpt-6.1-sol": ListPrice(4.0, 0.20, 20.0, OPENAI_PRICING, PRICE_READ_DATE),
    "gpt-6.1-terra": ListPrice(2.0, 0.10, 10.0, OPENAI_PRICING, PRICE_READ_DATE),
}
_SMALLEST_SHOWN = 0.01


def _mapping(value: object) -> Mapping[str, object]:
    return value if isinstance(value, dict) else {}


def _list_price(result: Mapping[str, object]) -> ListPrice | None:
    declared = _mapping(result.get("cost_price")) or _mapping(result.get("price_per_mtok"))
    if declared:
        return ListPrice(float(declared["input"]), float(declared["cached"]), float(declared["output"]))
    model = str(_mapping(result.get("agent")).get("model"))
    if _mapping(result.get("config")).get("service_tier") == "fast" and model in FAST_PRICES:
        return FAST_PRICES[model]
    return LIST_PRICES.get(model)


def estimated_usd(result: Mapping[str, object]) -> float | None:
    """`((input - cached) x X + cached x Y + generated x Z) / 1,000,000`, or None with no price or no tokens."""
    price = _list_price(result)
    totals = _mapping(result.get("totals"))
    tokens = _mapping(totals.get("tokens"))
    if price is None or not tokens:
        return None
    cached = int(tokens.get("cached_input") or 0)
    # opencode reports reasoning apart from output; generated_tokens holds both on every harness.
    generated = _mapping(totals.get("stats")).get("generated_tokens")
    output = generated if isinstance(generated, int) else int(tokens.get("output") or 0)
    uncached = max(0, int(tokens.get("input") or 0) - cached)
    return round((uncached * price.input + cached * price.cached + output * price.output) / 1e6, 6)


def price_text(result: Mapping[str, object]) -> str:
    """'~$2.04', '< $0.01', '$0.00 (local)' when the submitter declared it free, or 'n/a'."""
    declared = _mapping(result.get("price_per_mtok"))
    if declared and not any(declared.values()):
        return "$0.00 (local)"
    usd = estimated_usd(result)
    if usd is None:
        return "n/a"
    return f"~${usd:.2f}" if usd >= _SMALLEST_SHOWN else f"< ${_SMALLEST_SHOWN:.2f}"


def run_cost_text(result: Mapping[str, object]) -> str:
    """One cost display for a run, including historical bundles (#195)."""
    totals = _mapping(result.get("totals"))
    usd, estimate = totals.get("cost_usd"), price_text(result)
    if estimate == "$0.00 (local)":
        return estimate
    bound = ">= " if totals.get("cost_lower_bound") else ""
    if result.get("cost_policy") == "run-v1" and totals.get("cost_basis") == "n/a":
        return "n/a"
    stored_estimate = totals.get("cost_basis") == "list-price" or (
        totals.get("cost_basis") == "price" and (result.get("cost_policy") == "run-v1" or not totals.get("tokens")))
    if stored_estimate and isinstance(usd, (int, float)):
        return _estimated_cost_text(float(usd), bool(bound))
    harness_unpriced = usd == 0 and bool(result.get("price_per_mtok")) and estimate.startswith("~")
    if totals.get("cost_basis") == "harness" and isinstance(usd, (int, float)) and not harness_unpriced:
        return f"{bound}${usd:.2f}"
    if estimate.startswith("<") and bound:
        calculated = estimated_usd(result)
        return _estimated_cost_text(calculated, True) if calculated is not None else estimate
    return bound + estimate if estimate.startswith("~") else estimate


def _estimated_cost_text(usd: float, lower_bound: bool) -> str:
    if lower_bound and usd < _SMALLEST_SHOWN:
        precise = f"{usd:.6f}".rstrip("0").rstrip(".")
        return f">= ~${precise}"
    if usd < _SMALLEST_SHOWN:
        return f"< ${_SMALLEST_SHOWN:.2f}"
    return f"{'>= ' if lower_bound else ''}~${usd:.2f}"


def _measured_cost(result: Mapping[str, object], price: ListPrice, rows: list[object]) -> tuple[float | None, bool]:
    """Price each task's observed tokens conservatively when measurements are incomplete (#195)."""
    value = 0.0
    known_tokens = 0
    incomplete = not rows
    agent = _mapping(result.get("agent")).get("name")
    for row in rows:
        if not isinstance(row, dict):
            incomplete = True
            continue
        usages = [step.get("usage") for step in row.get("steps", []) if isinstance(step, dict)]
        incomplete |= not usages
        task_output = 0
        for usage in usages:
            if not isinstance(usage, dict):
                incomplete = True
                continue
            inp, cached, output = usage.get("input_tokens"), usage.get("cached_input_tokens"), usage.get("output_tokens")
            if inp is None or output is None:
                incomplete = True
            task_output += int(output or 0)
            if agent == "opencode":
                reasoning = usage.get("reasoning_tokens")
                task_output += int(reasoning or 0)
                incomplete |= reasoning is None and bool(output)
            if cached is None:
                if isinstance(inp, int) and inp > 0:
                    value += inp * min(price.input, price.cached)
                    known_tokens += inp
                    incomplete = True
                continue
            cached = int(cached)
            known_tokens += cached
            value += cached * price.cached
            if isinstance(inp, int):
                uncached = max(0, inp - cached)
                known_tokens += uncached
                value += uncached * price.input
                incomplete |= cached > inp
        generated = _mapping(row.get("stats")).get("generated_tokens")
        if isinstance(generated, int):
            incomplete |= generated < task_output
            task_output = max(generated, task_output)
        known_tokens += task_output
        value += task_output * price.output
    return (round(value / 1_000_000, 6) if known_tokens else None, incomplete)


def finalize_run_cost(result: dict[str, object]) -> None:
    """Record the cost and rate chosen for this run; preserve a prior rate on redo (#195)."""
    totals = result["totals"]
    assert isinstance(totals, dict)
    result["cost_policy"] = "run-v1"
    tasks = result.get("tasks")
    rows = tasks if isinstance(tasks, list) else []
    usages = [step.get("usage") for row in rows if isinstance(row, dict)
              for step in row.get("steps", []) if isinstance(step, dict)]
    measured = [usage for usage in usages if isinstance(usage, dict)]
    reported = [float(usage["cost_usd"]) for usage in measured if isinstance(usage.get("cost_usd"), (int, float))]
    declared = _mapping(result.get("price_per_mtok"))
    old_price = _mapping(result.get("cost_price"))
    price = _list_price(result)
    estimate, incomplete = _measured_cost(result, price, rows) if price is not None else (None, False)
    if (totals.get("cost_basis") == "harness" and totals.get("cost_usd") == 0
            and declared and any(declared.values()) and estimate is not None):
        totals.update(cost_usd=estimate, cost_basis="price",
                      cost_lower_bound=bool(totals.get("cost_lower_bound")) or incomplete)
        return
    if reported and totals.get("cost_basis") == "n/a":
        totals.update(cost_usd=round(sum(reported), 4), cost_basis="harness", cost_lower_bound=True)
        return
    if totals.get("cost_basis") == "harness":
        return
    if totals.get("cost_basis") == "price":
        if declared and any(declared.values()):
            totals.update(cost_usd=estimate, cost_basis="price" if estimate is not None else "n/a",
                          cost_lower_bound=bool(totals.get("cost_lower_bound")) or incomplete)
        return
    if price is None or estimate is None:
        return
    if not old_price and not declared:
        agent = _mapping(result.get("agent"))
        result["cost_price"] = {"model": agent.get("model"), "tier": _mapping(result.get("config")).get("service_tier"),
                                "input": price.input, "cached": price.cached, "output": price.output,
                                "source_url": price.source_url, "read_date": price.read_date}
    totals.update(cost_usd=estimate, cost_basis="price" if declared and not old_price else "list-price",
                  cost_lower_bound=bool(totals.get("cost_lower_bound")) or incomplete)


def missing_price_warning(model: str, config: Mapping[str, object], declared: object = None) -> str | None:
    """Warn before a run, even when a harness may later report the cost (#195)."""
    if _list_price({"agent": {"model": model}, "config": config, "price_per_mtok": declared}) is None:
        return f"no list price for {model}; add it to prices.py"
    return None
