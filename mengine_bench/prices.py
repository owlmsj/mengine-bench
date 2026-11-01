"""The board's Est. price: a run's tokens at public API list prices (#76).

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


LIST_PRICES: Mapping[str, ListPrice] = {
    # Input at the 1 h cache write price: Claude Code caches nearly all its uncached input.
    # On the published Opus and Sonnet runs this lands within 0.1% of total_cost_usd.
    "claude-opus-5-5": ListPrice(8.0, 0.20, 20.0),
    "claude-sonnet-5-5": ListPrice(4.0, 0.10, 10.0),
    "gpt-6-astra": ListPrice(10.0, 1.0, 50.0),
    "gpt-6.1-sol": ListPrice(2.0, 0.10, 10.0),
    "zai/glm-5.3-flash": ListPrice(0.15, 0.03, 0.50),
    # Off-peak; peak hours cost twice this. Gemini's rise on 2026-12-01 is not applied.
    "deepseek/deepseek-flash": ListPrice(0.15, 0.003, 0.60),
    "gemini-4-argon": ListPrice(2.0, 0.10, 10.0),
}
FAST_PRICES: Mapping[str, ListPrice] = {
    "gpt-6-astra": ListPrice(20.0, 2.0, 100.0),
    "gpt-6.1-sol": ListPrice(4.0, 0.20, 20.0),
}
_SMALLEST_SHOWN = 0.01


def _mapping(value: object) -> Mapping[str, object]:
    return value if isinstance(value, dict) else {}


def _list_price(result: Mapping[str, object]) -> ListPrice | None:
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
    uncached = int(tokens.get("input") or 0) - cached
    return round((uncached * price.input + cached * price.cached + output * price.output) / 1e6, 6)


def price_text(result: Mapping[str, object]) -> str:
    """'~$2.04', '< $0.01', '$0.00 (local)' when the submitter declared it free, or 'n/a'."""
    usd = estimated_usd(result)
    if usd is None:
        declared = _mapping(result.get("price_per_mtok"))
        return "$0.00 (local)" if declared and not any(declared.values()) else "n/a"
    return f"~${usd:.2f}" if usd >= _SMALLEST_SHOWN else f"< ${_SMALLEST_SHOWN:.2f}"
