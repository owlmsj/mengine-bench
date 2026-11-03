"""Web fact search: three pinned facts, each proved by a primary source the agent finds on the open web (#153).

The second web task after `web-plan-ranking`: short lookups, no analysis. Every answer is a fact that cannot change
(a tagged release's date, a published standard's count), and every check is offline: the value is compared with the
gold below, and the proof URL by its domain and fetch trace. Values confirmed on 2026-11-03 at the URL beside each fact.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

from mengine_bench.core import (
    Checkpoint, CheckResult, EvalTask, ReferenceAnswers, Step, ToolCall, TraceCheck,
    WROTE_RESULT, checkpoints, number, result_json, saw, write,
)
from mengine_bench.runner.trace import fetched_urls, url_key
from mengine_bench.tasks.webresearch import _web_date


@dataclass(frozen=True)
class WebFact:
    key: str
    question: str
    answer: date | int
    domains: tuple[str, ...]  # the project's or standards body's own site; subdomains count
    source: str


WEB_FACTS: tuple[WebFact, ...] = (
    # "### 2022-11-16 (3.40.0)"
    WebFact("sqlite_3_40_0_release_date", "the release date of SQLite 3.40.0", date(2022, 11, 16),
            ("sqlite.org",), "https://www.sqlite.org/changes.html"),
    # "Release date: 2022-10-13"
    WebFact("postgresql_15_0_release_date", "the release date of PostgreSQL 15.0", date(2022, 10, 13),
            ("postgresql.org",), "https://www.postgresql.org/docs/release/15.0/"),
    # "Unicode 15.0 adds 4,489 characters, for a total of 149,186 characters."
    WebFact("unicode_15_0_characters_added", "how many characters Unicode 15.0 added", 4489,
            ("unicode.org",), "https://www.unicode.org/versions/Unicode15.0.0/"),
)

WEB_FACTS_PROMPT = ("A database newsletter's fact-check desk needs three facts confirmed before Friday's issue goes out, "
                    "each against a primary source: the project's or the standards body's own website, not a wiki or a "
                    "news story. This one needs the open web, and you are allowed to browse.\n\n"
                    + "\n".join(f"- `{fact.key}`: {fact.question}" for fact in WEB_FACTS)
                    + "\n\nRecord them in {WS}/result.json, one entry per key above, each an object with `value` (a date "
                    "as YYYY-MM-DD, a count as a number) and `url` (the primary-source page that shows it).")


def _webfacts_host_ok(url: object, domains: Sequence[str]) -> bool:
    text = str(url or "").strip()
    if not re.match(r"https?://", text):
        return False
    host = (urlsplit(text).hostname or "").lower().rstrip(".")
    return any(host == domain or host.endswith("." + domain) for domain in domains)


def _webfacts_value_ok(value: object, fact: WebFact) -> bool:
    if isinstance(fact.answer, date):
        return _web_date(value) == fact.answer
    got = number(value)
    return got is not None and got == fact.answer


def _webfacts_entry(got: Mapping[str, object], key: str) -> Mapping[str, object]:
    entry = got.get(key)
    return entry if isinstance(entry, dict) else {}


@TraceCheck
def _webfacts_check(ws: Path, answers: Sequence[str], trace: Sequence[ToolCall]) -> CheckResult:
    result = CheckResult()
    got = result_json(ws)
    for fact in WEB_FACTS:
        entry = _webfacts_entry(got, fact.key)
        want = fact.answer.isoformat() if isinstance(fact.answer, date) else fact.answer
        result.add(f"{fact.key} value", _webfacts_value_ok(entry.get("value"), fact), saw(entry.get("value"), want))
        result.add(f"{fact.key} primary source", _webfacts_host_ok(entry.get("url"), fact.domains),
                   saw(entry.get("url"), f"an http(s) URL on {' or '.join(fact.domains)}"))
    fetched = fetched_urls(trace)
    missing = [fact.key for fact in WEB_FACTS if url_key(_webfacts_entry(got, fact.key).get("url")) not in fetched]
    result.add("cited primary sources were fetched", not missing,
               saw(missing, "each cited URL's host and path in a fetch action"))
    return result


def _webfacts_setup(ws: Path) -> None:
    """Nothing to start from: the brief is the whole input."""
    ws.mkdir(parents=True, exist_ok=True)


def _webfacts_reference(ws: Path) -> list[str]:
    facts = {fact.key: {"value": fact.answer.isoformat() if isinstance(fact.answer, date) else fact.answer,
                        "url": fact.source} for fact in WEB_FACTS}
    write(ws, "result.json", json.dumps(facts, indent=2))
    return ReferenceAnswers(["done"], [ToolCall("WebFetch", {"url": fact.source}) for fact in WEB_FACTS])


TASKS = [
    EvalTask(
        id="web-fact-search", category="web-research", needs=frozenset({"web"}),
        provenance="new for bench#153: newsletter fact-check of three pinned facts against primary sources",
        summary="Look up three fixed facts on the web and give each with the official page that proves it.",
        setup=_webfacts_setup, check=_webfacts_check, reference=_webfacts_reference, timeout_s=60,
        checkpoints=checkpoints(("searched the web", r"web_?search|search_query|google|bing|duckduckgo"),
                                WROTE_RESULT) + (Checkpoint("opened a source", r"https?://", fetch_only=True),),
        steps=(Step(WEB_FACTS_PROMPT),),
    ),
]
