"""Web research: the only eval where the agent under test uses the open web (#124).

The agent researches Brazil's anti-inflation plans, scores them with a rubric
shipped in the workspace and delivers a ranking plus a sourced dossier. The
gold below is fixed and offline: no check fetches the web. Anchors are
stable public facts, each with the URL it was confirmed at (2026-11-02).
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from mengine_bench.core import (
    Checkpoint,
    CheckResult,
    EvalTask,
    ReferenceAnswers,
    Step,
    ToolCall,
    TraceCheck,
    WROTE_RESULT,
    checkpoints,
    number,
    read,
    result_json,
    saw,
    write,
)
from mengine_bench.runner.trace import fetched_hosts, fetched_urls, host_key, url_key

RUBRIC_FILE = "RUBRIC.md"
DOSSIER_FILE = "dossier.md"

# Annual IPCA (IBGE), % in the calendar year (12 months to December).
# Source: IBGE SIDRA table 1737, variable 2265, confirmed via
# https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/2265/p/198512,198612,198712,198812,198912,199012,199112,199212,199312,199412,199512
WEB_IPCA_ANNUAL: dict[int, float] = {
    1985: 242.23,   # SIDRA 198512; yahii.com.br gives 242.25, ecalculos.com.br 233.65 (index reset of 1986)
    1986: 79.66,    # SIDRA 198612; ecalculos.com.br gives 76.61 (index reset of 1986)
    1987: 363.41,   # SIDRA 198712
    1988: 980.21,   # SIDRA 198812 (yahii: 980.22)
    1989: 1972.91,  # SIDRA 198912
    1990: 1620.97,  # SIDRA 199012
    1991: 472.70,   # SIDRA 199112
    1992: 1119.10,  # SIDRA 199212
    1993: 2477.15,  # SIDRA 199312
    1994: 916.46,   # SIDRA 199412
    1995: 22.41,    # SIDRA 199512
}
WEB_IPCA_TOL = 0.03
# 1985 and 1986 differ by up to ~3.8% between published tables (the IPCA was rebased with the Cruzado), so they
# get a wider band; both only feed plans whose inflation drop is 0 under any of those values (#124).
WEB_IPCA_WIDE_TOL: dict[int, float] = {1985: 0.05, 1986: 0.05}
WEB_DATE_TOL_DAYS = 7
WEB_MONTHS_TOL = 1
WEB_SCORE_TOL = 0.01
WEB_DROP_WEIGHT = 0.7
WEB_DURABILITY_WEIGHT = 0.3
WEB_MONTHS_CAP = 60


@dataclass(frozen=True)
class WebPlan:
    name: str
    aliases: tuple[str, ...]
    launches: tuple[date, ...]  # every accepted launch date; the first is the reference one
    source: str


# Launch dates, each confirmed on the page in `source`.
WEB_PLANS: tuple[WebPlan, ...] = (
    # "lancado ... em 28 de fevereiro de 1986, com base no decreto-lei no 2.283, de 27 de fevereiro de 1986"
    WebPlan("Cruzado", ("cruzado", "cruzado1", "cruzadoi"), (date(1986, 2, 28),), "https://pt.wikipedia.org/wiki/Plano_Cruzado"),
    # "instituido em 12 de junho de 1987, atraves dos Decretos-Lei no 2.335/87"
    WebPlan("Bresser", ("bresser",), (date(1987, 6, 12),), "https://pt.wikipedia.org/wiki/Plano_Bresser"),
    # "instituido em 15 de janeiro de 1989, atraves da medida provisoria no 32"
    WebPlan("Verao", ("verao",), (date(1989, 1, 15),), "https://pt.wikipedia.org/wiki/Plano_Ver%C3%A3o"),
    # "16 de marco de 1990 a janeiro de 1991"
    WebPlan("Collor I", ("collori", "collor1"), (date(1990, 3, 16),), "https://pt.wikipedia.org/wiki/Plano_Collor"),
    # "31 de janeiro de 1991 a 9 de maio de 1991"
    WebPlan("Collor II", ("collorii", "collor2"), (date(1991, 1, 31),), "https://pt.wikipedia.org/wiki/Plano_Collor"),
    # URV "lancada no dia primeiro de marco de 1994"; "Em 1o de julho de 1994 ... o lancamento da nova moeda, o real"
    WebPlan("Real", ("real",), (date(1994, 3, 1), date(1994, 7, 1)), "https://pt.wikipedia.org/wiki/Plano_Real"),
)
WEB_TOP3 = ("Real", "Collor I", "Collor II")

WEB_RUBRIC = f"""# Rubric: did the plan deliver?

Score each plan below from public data. Inflation is the annual IPCA (IBGE), in % for the calendar year.

| plan | next plan |
|---|---|
| Cruzado (1986) | Bresser |
| Bresser (1987) | Verao |
| Verao (1989) | Collor I |
| Collor I (1990) | Collor II |
| Collor II (1991) | Real |
| Real (1994) | none |

For a plan launched in year Y:

- ipca_before = annual IPCA of year Y-1; ipca_after = annual IPCA of year Y+1.
- score_drop = clamp(1 - ipca_after / ipca_before, 0, 1)
- months_lasted = whole calendar months from the plan's launch date to the next plan's launch date
  (Real: no next plan, use {WEB_MONTHS_CAP}).
- score_durability = min(months_lasted, {WEB_MONTHS_CAP}) / {WEB_MONTHS_CAP}
- score = {WEB_DROP_WEIGHT} * score_drop + {WEB_DURABILITY_WEIGHT} * score_durability (0 to 1)

The top 3 are the three highest scores, best first.
"""


def _web_plan_key(text: object) -> str:
    """'Plano Verão', 'verao plan', 'Collor 1' -> a key compared against the aliases (#124)."""
    plain = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode().lower()
    plain = re.sub(r"\(.*?\)|\b(plano|plan|de|do)\b|\b(19|20)\d\d\b", " ", plain)
    return re.sub(r"[^a-z0-9]", "", plain)


def _web_plan_named(text: object) -> WebPlan | None:
    key = _web_plan_key(text)
    return next((plan for plan in WEB_PLANS if key in plan.aliases), None)


MONTHS_EN_PT = {name: index for index, names in enumerate((
    ("jan", "january", "janeiro"), ("feb", "february", "fev", "fevereiro"), ("mar", "march", "marco"),
    ("apr", "april", "abr", "abril"), ("may", "mai", "maio"), ("jun", "june", "junho"), ("jul", "july", "julho"),
    ("aug", "august", "ago", "agosto"), ("sep", "sept", "september", "set", "setembro"),
    ("oct", "october", "out", "outubro"), ("nov", "november", "novembro"), ("dec", "december", "dez", "dezembro"),
), start=1) for name in names}


def _web_date(value: object) -> date | None:
    """2026-style ISO, 28/02/1986 (day first, as Brazil writes it) or 'February 28, 1986' / '28 de fevereiro de 1986'."""
    text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode().lower()
    found = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", text)
    if found:
        year, month, day = map(int, found.groups())
    elif found := re.search(r"(\d{1,2})[/.](\d{1,2})[/.](\d{4})", text):
        day, month, year = map(int, found.groups())
    else:
        words = re.findall(r"[a-z]+|\d+", text)
        months = [MONTHS_EN_PT[w] for w in words if w in MONTHS_EN_PT]
        numbers = [int(w) for w in words if w.isdigit()]
        years = [n for n in numbers if n > 1900]
        days = [n for n in numbers if n <= 31]
        if not (months and years and days):
            return None
        year, month, day = years[0], months[0], days[0]
    try:
        return date(year, month, day)
    except ValueError:
        return None


def _web_months_between(start: date, end: date) -> int:
    return (end.year - start.year) * 12 + end.month - start.month - (end.day < start.day)


def web_expected_months(plan: WebPlan) -> set[int]:
    """Every months_lasted the rubric yields for the accepted launch dates of this plan and the next."""
    index = WEB_PLANS.index(plan)
    if index == len(WEB_PLANS) - 1:
        return {WEB_MONTHS_CAP}
    following = WEB_PLANS[index + 1]
    return {_web_months_between(start, end) for start in plan.launches for end in following.launches}


def web_rubric_score(ipca_before: float, ipca_after: float, months: float) -> float:
    drop = min(max(1 - ipca_after / ipca_before, 0.0), 1.0) if ipca_before else 0.0
    return WEB_DROP_WEIGHT * drop + WEB_DURABILITY_WEIGHT * min(max(months, 0.0), WEB_MONTHS_CAP) / WEB_MONTHS_CAP


def web_reference_rows() -> list[dict[str, object]]:
    rows = []
    for plan in WEB_PLANS:
        year = plan.launches[0].year
        before, after = WEB_IPCA_ANNUAL[year - 1], WEB_IPCA_ANNUAL[year + 1]
        months = min(web_expected_months(plan))
        rows.append({"plan": plan.name, "launch_date": plan.launches[0].isoformat(), "ipca_before": before,
                     "ipca_after": after, "months_lasted": months,
                     "score": round(web_rubric_score(before, after, months), 3),
                     "sources": [plan.source, "https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/2265"]})
    return rows


def _web_ipca_ok(value: object, year: int) -> bool:
    got = number(value)
    want = WEB_IPCA_ANNUAL[year]
    tol = WEB_IPCA_WIDE_TOL.get(year, WEB_IPCA_TOL)
    # A rate may come as 22.41 (%) or 0.2241 (fraction); the rubric's ratio is the same either way.
    return got is not None and any(abs(got - scale * want) <= tol * scale * want for scale in (1.0, 0.01))


def _web_date_ok(value: object, plan: WebPlan) -> bool:
    found = _web_date(value)
    return found is not None and any(abs((found - launch).days) <= WEB_DATE_TOL_DAYS for launch in plan.launches)


def _web_rows(got: Mapping[str, object]) -> dict[str, Mapping[str, object]]:
    """Delivered rows by canonical plan name; the first row naming a plan wins."""
    rows = got.get("plans")
    found: dict[str, Mapping[str, object]] = {}
    for row in rows if isinstance(rows, list) else []:
        plan = _web_plan_named(row.get("plan")) if isinstance(row, dict) else None
        if plan is not None:
            found.setdefault(plan.name, row)
    return found


def _web_row_score_ok(row: Mapping[str, object]) -> bool:
    before, after, months, score = (number(row.get(key)) for key in ("ipca_before", "ipca_after", "months_lasted", "score"))
    if None in (before, after, months, score):
        return False
    want = web_rubric_score(before, after, months)
    # "0.58", "58" or "58%": the rubric's 0..1 score in either unit.
    return abs(score - want) <= WEB_SCORE_TOL or abs(score / 100 - want) <= WEB_SCORE_TOL


def _web_cited_urls(text: str) -> set[str]:
    urls: set[str] = set()
    for url in re.findall(r'''https?://[^\s<>\]"']+''', text):
        url = url.rstrip(".,;:")
        # #164: prose punctuation and Markdown's closing parenthesis are not part of a cited URL.
        while url.endswith(")") and url.count(")") > url.count("("):
            url = url[:-1]
        urls.add(url)
    return urls


def _web_has_url(row: Mapping[str, object], fetched: set[str]) -> bool:
    sources = row.get("sources")
    items = sources if isinstance(sources, list) else [sources]
    return any(host_key(url) in fetched for item in items for url in _web_cited_urls(str(item or "")))


@TraceCheck
def _web_check(ws: Path, answers: Sequence[str], trace: Sequence[ToolCall]) -> CheckResult:
    result = CheckResult()
    got = result_json(ws)
    rows = _web_rows(got)
    names = [plan.name for plan in WEB_PLANS]
    missing = [name for name in names if name not in rows]
    result.add("all six plans recorded", not missing, saw(sorted(rows), names))
    bad_dates = [plan.name for plan in WEB_PLANS if not _web_date_ok(rows.get(plan.name, {}).get("launch_date"), plan)]
    result.add("launch dates", not missing and not bad_dates,
               saw({name: rows.get(name, {}).get("launch_date") for name in bad_dates or missing},
                   {plan.name: [d.isoformat() for d in plan.launches] for plan in WEB_PLANS if plan.name in (bad_dates or missing)}))
    bad_ipca = [plan.name for plan in WEB_PLANS if not (
        _web_ipca_ok(rows.get(plan.name, {}).get("ipca_before"), plan.launches[0].year - 1)
        and _web_ipca_ok(rows.get(plan.name, {}).get("ipca_after"), plan.launches[0].year + 1))]
    result.add("inflation before and after", not bad_ipca,
               saw({name: [rows.get(name, {}).get(k) for k in ("ipca_before", "ipca_after")] for name in bad_ipca},
                   {plan.name: [WEB_IPCA_ANNUAL[plan.launches[0].year - 1], WEB_IPCA_ANNUAL[plan.launches[0].year + 1]]
                    for plan in WEB_PLANS if plan.name in bad_ipca}))
    bad_months = []
    for plan in WEB_PLANS:
        months = number(rows.get(plan.name, {}).get("months_lasted"))
        wants = web_expected_months(plan)
        # Real has no next plan: any count up to today is true, and the rubric caps it.
        ok = months is not None and (months >= WEB_MONTHS_CAP - WEB_MONTHS_TOL if wants == {WEB_MONTHS_CAP}
                                     else any(abs(months - want) <= WEB_MONTHS_TOL for want in wants))
        if not ok:
            bad_months.append(plan.name)
    result.add("months lasted", not bad_months,
               saw({name: rows.get(name, {}).get("months_lasted") for name in bad_months},
                   {plan.name: sorted(web_expected_months(plan)) for plan in WEB_PLANS if plan.name in bad_months}))
    bad_scores = [name for name in names if name not in rows or not _web_row_score_ok(rows[name])]
    result.add("scores follow the rubric", not bad_scores,
               saw({name: rows.get(name, {}).get("score") for name in bad_scores}, "0.7*drop + 0.3*durability from the row's own numbers"))
    top = got.get("top3")
    top_names = [p.name if (p := _web_plan_named(item)) else str(item) for item in top] if isinstance(top, list) else top
    result.add("top 3", top_names == list(WEB_TOP3), saw(top, list(WEB_TOP3)))
    fetched = fetched_hosts(trace)
    unsourced = [name for name in names if name not in rows or not _web_has_url(rows[name], fetched)]
    result.add("every plan has a source", not unsourced, saw(unsourced, "a cited http(s) URL on a fetched host for every plan"))
    dossier = read(ws, DOSSIER_FILE) or ""
    cited = {url for url in _web_cited_urls(dossier) if host_key(url) in fetched}
    urls = {url_key(url) for url in cited}
    hosts = {host_key(url) for url in cited}
    opened_urls = urls & fetched_urls(trace)
    plain = unicodedata.normalize("NFKD", dossier).encode("ascii", "ignore").decode().lower()
    plans_named = sorted(word for word in ("cruzado", "bresser", "verao", "collor", "real") if re.search(rf"\b{word}\b", plain))
    result.add("dossier", len(dossier) >= 600 and len(urls) >= 3 and max(len(hosts), len(opened_urls)) >= 3 and len(plans_named) >= 3,
               saw({"chars": len(dossier), "urls": len(urls), "fetched_hosts": len(hosts), "fetched_urls": len(opened_urls), "plans": plans_named},
                   "600+ chars, 3+ URLs spanning 3+ fetched hosts or distinct fetched URLs, 3+ plans"))
    return result


def _web_setup(ws: Path) -> None:
    write(ws, RUBRIC_FILE, WEB_RUBRIC)


def _web_reference(ws: Path) -> list[str]:
    rows = web_reference_rows()
    write(ws, "result.json", json.dumps({"plans": rows, "top3": list(WEB_TOP3)}, indent=2))
    lines = ["# Which Brazilian anti-inflation plan delivered?", "",
             "Scored with RUBRIC.md: 70% inflation drop (annual IPCA, year before vs year after launch), "
             "30% durability (months until the next plan, capped at 60).", "",
             "| plan | launch | IPCA before % | IPCA after % | months | score | source |", "|---|---|---|---|---|---|---|"]
    lines += [f"| {r['plan']} | {r['launch_date']} | {r['ipca_before']} | {r['ipca_after']} | {r['months_lasted']} | "
              f"{r['score']} | {r['sources'][0]} |" for r in rows]
    lines += ["", f"Top 3: {', '.join(WEB_TOP3)}. Only the Real both cut inflation for good and lasted; the Collor plans "
              "cut the annual rate but were followed by a new plan within three years.", "",
              "IPCA series: https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/2265"]
    write(ws, DOSSIER_FILE, "\n".join(lines) + "\n")
    urls = {str(url) for row in rows for url in row["sources"]}
    urls.add("https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/2265")
    return ReferenceAnswers(["done"], [ToolCall("WebFetch", {"url": url}) for url in sorted(urls)])


TASKS = [
    EvalTask(
        id="web-plan-ranking", category="web-research", needs=frozenset({"web"}),
        provenance="Policy newsletter fact-check: rank Brazil's 1986-1994 anti-inflation plans from public sources",
        summary="Research Brazil's anti-inflation plans on the web and rank which delivered, with sources.",
        setup=_web_setup, check=_web_check, reference=_web_reference, timeout_s=210,
        deliverables=(DOSSIER_FILE,),
        checkpoints=checkpoints(("read the rubric", r"RUBRIC"), ("searched the web", r"web_?search|search_query|google|bing|duckduckgo"),
                                WROTE_RESULT, ("wrote the dossier", r"dossier\.md"))
                    + (Checkpoint("opened a source", r"https?://", fetch_only=True),),
        steps=(Step("A policy newsletter is running a piece on which of Brazil's anti-inflation plans delivered what it "
                    "promised, and wants a ranking it can defend. Research the plans in {WS}/RUBRIC.md on the open web: "
                    "this one needs public sources, and you are allowed to browse. Score every plan with that rubric, "
                    "rank the top 3, and write a one-page dossier for the editor in {WS}/dossier.md. Every number must "
                    "carry the URL it came from. Record the result in {WS}/result.json: plans (one entry per plan with "
                    "plan, launch_date, ipca_before, ipca_after, months_lasted, score and sources, a list of URLs) and "
                    "top3 (plan names, best first)."),),
    ),
]
