"""Data science + startup backoffice tasks.

Messy-but-real inputs on purpose: duplicated telemetry rows, a Brazilian
ledger with `;` and `1.234,56`, bank memos in three formats. The gold is the
number a careful analyst gets by any valid route (#98): rounding, units and
number formats are tolerated, a wrong answer is not.
"""

from __future__ import annotations

import csv
import io
import json
import math
import random
from collections import defaultdict
from collections.abc import Mapping, Sequence
from datetime import date
from pathlib import Path

from mengine_bench.core import (
    CheckResult,
    EvalTask,
    Step,
    WROTE_RESULT,
    checkpoints,
    is_yes,
    near,
    near_share,
    number,
    result_json,
    saw,
    write,
)

# ----------------------------------------------------------- ds-ab-playtest --


def _ab_rows() -> list[dict[str, str]]:
    rng = random.Random(6321)
    rows = []
    for i in range(1800):
        variant = "A" if i % 2 == 0 else "B"
        rate = 0.41 if variant == "A" else 0.47
        rows.append({
            "session_id": f"s{i:05d}",
            "variant": rng.choice([variant, variant.lower(), f" {variant}"]),
            "player_id": f"p{rng.randint(1, 900):04d}",
            "completed_tutorial": str(int(rng.random() < rate)),
            "match_minutes": f"{max(1.0, rng.gauss(14 if variant == 'A' else 15.5, 4)):.1f}",
        })
    rows += [dict(rows[j]) for j in rng.sample(range(1800), 70)]
    rng.shuffle(rows)
    return rows


def _ab_expected() -> dict[str, float]:
    # ints and the ship_b bool fit float; ship_b is compared by identity in the check.
    seen: dict[str, dict[str, str]] = {}
    for row in _ab_rows():
        seen.setdefault(row["session_id"], row)
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in seen.values():
        groups[row["variant"].strip().upper()].append(row)
    na, nb = len(groups["A"]), len(groups["B"])
    ca = sum(int(r["completed_tutorial"]) for r in groups["A"])
    cb = sum(int(r["completed_tutorial"]) for r in groups["B"])
    pa, pb = ca / na, cb / nb
    pool = (ca + cb) / (na + nb)
    z = (pb - pa) / math.sqrt(pool * (1 - pool) * (1 / na + 1 / nb))
    p_value = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return {
        "sessions_a": na, "sessions_b": nb, "rate_a": pa, "rate_b": pb,
        "abs_lift": pb - pa, "rel_lift": (pb - pa) / pa, "p_value": p_value,
        "ship_b": bool(p_value < 0.05 and pb > pa),
        "mean_minutes_a": sum(float(r["match_minutes"]) for r in groups["A"]) / na,
        "mean_minutes_b": sum(float(r["match_minutes"]) for r in groups["B"]) / nb,
    }


def _ab_setup(ws: Path) -> None:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(_ab_rows()[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(_ab_rows())
    write(ws, "telemetry/playtest_ab.csv", buf.getvalue())
    write(ws, "telemetry/README.md",
          "# Playtest A/B - Pixel Arena tutorial\n\nExport from arena-panel. The ETL resends sessions: "
          "`session_id` is the unique key (repeated rows are the same session). `variant` may come lowercase "
          "or with a leading space. `completed_tutorial` is 0/1.\n\n"
          "Release rule: a variant ships only when its gain in tutorial completion is statistically significant at the "
          "5% level.\n")


def _seen(got: Mapping[str, object], exp: Mapping[str, object], *keys: str) -> str:
    return saw({key: got.get(key) for key in keys}, {key: exp.get(key) for key in keys})


def _ab_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    exp = _ab_expected()
    got = result_json(ws)
    result.add("deduplicated session counts", near(got.get("sessions_a"), exp["sessions_a"], 0) and near(got.get("sessions_b"), exp["sessions_b"], 0),
               _seen(got, exp, "sessions_a", "sessions_b"))
    result.add("completion rates", near_share(got.get("completion_rate_a"), float(exp["rate_a"]), 2e-3)
               and near_share(got.get("completion_rate_b"), float(exp["rate_b"]), 2e-3),
               saw({key: got.get(key) for key in ("completion_rate_a", "completion_rate_b")}, (exp["rate_a"], exp["rate_b"])))
    # #98: which valid test is the agent's call (z, chi-squared, Fisher); all put this gap well under 5%.
    p_value = number(got.get("p_value"))
    result.add("the gain is significant", p_value is not None and 0 <= p_value < 0.05, saw(got.get("p_value"), f"about {exp['p_value']:.4f}"))
    result.add("ship decision", is_yes(got.get("ship_b")), saw(got.get("ship_b"), True))
    return result


def _ab_reference(ws: Path) -> list[str]:
    exp = _ab_expected()
    write(ws, "result.json", json.dumps({"ship_b": exp["ship_b"], "sessions_a": exp["sessions_a"], "sessions_b": exp["sessions_b"],
                                         "completion_rate_a": exp["rate_a"], "completion_rate_b": exp["rate_b"], "p_value": exp["p_value"]}))
    return ["done"]


MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]


# ------------------------------------------------------- bo-pnl-runway --

PNL_LINES = ["revenue", "cogs", "gross_profit", "gross_margin_pct", "sales_marketing", "rnd", "ga", "ebitda"]
CHART = [
    ("3.1.01", "SaaS subscriptions", "revenue"), ("3.1.02", "Onboarding services", "revenue"),
    ("3.1.09", "Refunds and cancellations", "revenue"), ("4.1.01", "Production cloud and GPUs", "cogs"),
    ("4.1.02", "Customer support", "cogs"), ("5.1.01", "Paid media", "sales_marketing"),
    ("5.1.02", "Sales team", "sales_marketing"), ("5.2.01", "Engineering", "rnd"),
    ("5.2.02", "Dev tools", "rnd"), ("5.3.01", "Admin and accounting", "ga"),
    ("5.3.02", "Rent and office", "ga"), ("6.1.01", "Investment income", "financial"),
    ("6.1.02", "Interest and IOF tax", "financial"),
]
CASH = 1_847_350.40
# #41: the older line a careless read picks up; the close is at the end of June.
CASH_MAY = CASH * 1.25


def _brl(value: float) -> str:
    # The ledger keeps Brazilian number format on purpose: parsing it is part of the task.
    sign = "-" if value < 0 else ""
    whole, cents = f"{abs(value):.2f}".split(".")
    return f"{sign}{int(whole):,}".replace(",", ".") + f",{cents}"


def _ledger() -> list[tuple[date, str, str, float]]:
    rng = random.Random(6323)
    rows = []
    base = {"3.1.01": 182_000, "3.1.02": 21_000, "4.1.01": -48_000, "4.1.02": -17_500, "5.1.01": -61_000,
            "5.1.02": -74_000, "5.2.01": -158_000, "5.2.02": -12_300, "5.3.01": -26_500, "5.3.02": -18_000,
            "6.1.01": 9_400, "6.1.02": -3_100}
    for m in range(1, 7):
        growth = 1 + 0.06 * (m - 1)
        for code, amount in base.items():
            for part in range(2 if code in ("3.1.01", "5.2.01") else 1):
                value = round(amount * (growth if code.startswith("3") else 1 + 0.02 * (m - 1)) * rng.uniform(0.9, 1.1) / (2 if code in ("3.1.01", "5.2.01") else 1), 2)
                rows.append((date(2026, m, rng.randint(2, 27)), code, f"{code} entry {part + 1}", value))
        if m in (3, 5):
            rows.append((date(2026, m, 28), "3.1.09", "Refund customer Kestrel", -round(rng.uniform(4_000, 9_000), 2)))
    rng.shuffle(rows)
    return rows


def _pnl_expected() -> tuple[dict[str, dict[str, float]], dict[str, float]]:
    line_of = {code: line for code, _, line in CHART}
    sums: dict[str, dict[str, float]] = {ym: defaultdict(float) for ym in MONTHS}
    for day, code, _, value in _ledger():
        sums[f"{day.year}-{day.month:02d}"][line_of[code]] += value
    table: dict[str, dict[str, float]] = {line: {} for line in PNL_LINES}
    for ym in MONTHS:
        s = sums[ym]
        revenue, cogs = s["revenue"], -s["cogs"]
        sm, rnd, ga = -s["sales_marketing"], -s["rnd"], -s["ga"]
        values = {"revenue": revenue, "cogs": cogs, "gross_profit": revenue - cogs,
                  "gross_margin_pct": (revenue - cogs) / revenue * 100, "sales_marketing": sm, "rnd": rnd, "ga": ga,
                  "ebitda": revenue - cogs - sm - rnd - ga}
        for line in PNL_LINES:
            table[line][ym] = values[line]
    burn = -sum(table["ebitda"][ym] for ym in MONTHS[-3:]) / 3
    return table, {"burn_avg_3m": burn, "runway_months": CASH / burn}


def _pnl_setup(ws: Path) -> None:
    ledger = "date;account;description;amount\n" + "".join(
        f"{d.strftime('%d/%m/%Y')};{c};{desc};{_brl(v)}\n" for d, c, desc, v in _ledger())
    write(ws, "finance/ledger.csv", ledger)
    write(ws, "finance/README.md", "# Finance notes\n\nThe board reads burn as the average monthly negative EBITDA of the "
          "last three closed months. Runway is the latest closing cash balance divided by that burn.\n")
    write(ws, "finance/chart_of_accounts.csv", "account;name;pnl_line\n" + "".join(f"{c};{n};{line}\n" for c, n, line in CHART))
    write(ws, "finance/cash_balance.txt", f"Consolidated balance on 31/05/2026: R$ {_brl(CASH_MAY)}\n"
                                          f"Consolidated balance on 30/06/2026: R$ {_brl(CASH)}\n")


def _pnl_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    table, runway = _pnl_expected()
    got = result_json(ws)
    for line in ("revenue", "gross_margin_pct", "ebitda"):
        series = got.get(line)
        series = series if isinstance(series, dict) else {}
        if line == "gross_margin_pct":
            wrong = next((ym for ym in MONTHS if not near_share(series.get(ym), table[line][ym] / 100, 1e-3)), None)
        else:
            wrong = next((ym for ym in MONTHS if not near(series.get(ym), table[line][ym], 1.0)), None)
        result.add(f"{line} per month", wrong is None, f"{wrong}: {saw(series.get(wrong), table[line].get(wrong))}")
    burn = number(got.get("burn"))
    # #98: a burn of 197288 or -197288 says the same thing.
    result.add("3-month average burn", burn is not None and abs(abs(burn) - runway["burn_avg_3m"]) <= 1.0, saw(got.get("burn"), runway["burn_avg_3m"]))
    result.add("runway in months", near(got.get("runway_months"), runway["runway_months"], 0.1), saw(got.get("runway_months"), runway["runway_months"]))
    return result


def _pnl_reference(ws: Path) -> list[str]:
    table, runway = _pnl_expected()
    write(ws, "result.json", json.dumps({**{line: {ym: round(table[line][ym], 2) for ym in MONTHS} for line in ("revenue", "gross_margin_pct", "ebitda")},
                                         "burn": round(runway["burn_avg_3m"], 2), "runway_months": round(runway["runway_months"], 1)}))
    return ["done"]


# ------------------------------------------------------- bo-reconcile --


def _invoices() -> list[tuple[str, str, float]]:
    rng = random.Random(6324)
    customers = ["Kestrel Games", "Coruja Labs", "Arena Studio", "Pampa Foods", "Ateliê Norte", "Vetor BI"]
    return [(f"INV-{1001 + i}", customers[i % 6], round(rng.uniform(800, 24_000), 2)) for i in range(40)]


RECON = {"unpaid": ["INV-1008", "INV-1030", "INV-1033"], "duplicated": ["INV-1015"], "mismatched": ["INV-1021", "INV-1036"]}


def _bank_rows() -> list[tuple[str, str, float]]:
    rng = random.Random(6325)
    rows = []
    for inv, customer, amount in _invoices():
        if inv in RECON["unpaid"]:
            continue
        number = inv.split("-")[1]
        memo = rng.choice([f"PIX {inv} {customer.upper()}", f"TED invoice {number} {customer}", f"inv{number} payment"])
        paid = round(amount - 250.0, 2) if inv == "INV-1021" else round(amount * 0.9, 2) if inv == "INV-1036" else amount
        rows.append((f"2026-06-{rng.randint(1, 28):02d}", memo, paid))
        if inv in RECON["duplicated"]:
            rows.append((f"2026-06-{rng.randint(1, 28):02d}", f"PIX {inv} resend", paid))
    rows += [("2026-06-05", "BANK SERVICE PACKAGE FEE", -89.90), ("2026-06-30", "CDB INTEREST", 1_204.33),
             ("2026-06-12", "PIX received unidentified 1099", 1_500.00)]
    rng.shuffle(rows)
    return rows


RECON_RULES = """# How we reconcile receivables

- The bank memo cites the invoice in different formats.
- Ignore fees, interest and PIX transfers without an identifiable invoice.
- unpaid: invoices with no payment. duplicated: invoices paid more than once.
- mismatched: a single payment whose amount differs from its invoice.
- The three categories are exclusive: a duplicated invoice is never also mismatched.
"""


def _recon_setup(ws: Path) -> None:
    write(ws, "backoffice/README.md", RECON_RULES)
    write(ws, "backoffice/invoices.csv", "id,customer,amount,due_date\n" + "".join(
        f"{i},{c},{v:.2f},2026-06-20\n" for i, c, v in _invoices()))
    write(ws, "backoffice/bank_statement_june.csv", "date,memo,amount\n" + "".join(
        f"{d},{m},{v:.2f}\n" for d, m, v in _bank_rows()))


def _recon_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    got = result_json(ws)
    for key, label in (("unpaid", "unpaid invoices"), ("duplicated", "duplicated payments")):
        entries = got.get(key)
        ids = sorted(str(entry.get("id") if isinstance(entry, dict) else entry)
                     for entry in entries) if isinstance(entries, list) else []
        result.add(label, ids == RECON[key], saw(ids, RECON[key]))
    mism = got.get("mismatched")
    valid_mismatches = isinstance(mism, list) and all(isinstance(m, dict) for m in mism)
    mism = mism if valid_mismatches else []
    ids = sorted(str(m.get("id")) for m in mism)
    result.add("mismatched amounts", valid_mismatches and ids == RECON["mismatched"], saw(ids, RECON["mismatched"]))
    invoiced = {i: v for i, _, v in _invoices()}
    paid = {"INV-1021": round(invoiced["INV-1021"] - 250.0, 2), "INV-1036": round(invoiced["INV-1036"] * 0.9, 2)}
    result.add("invoiced vs paid on mismatches", valid_mismatches and ids == RECON["mismatched"] and all(
        near(m.get("invoiced"), invoiced[str(m.get("id"))], 0.01)
        and near(m.get("paid"), paid[str(m.get("id"))], 0.01) for m in mism),
        saw(mism, [{"id": i, "invoiced": invoiced[i], "paid": paid[i]} for i in RECON["mismatched"]]))
    return result


def _recon_reference(ws: Path) -> list[str]:
    invoiced = {i: v for i, _, v in _invoices()}
    paid = {"INV-1021": invoiced["INV-1021"] - 250.0, "INV-1036": round(invoiced["INV-1036"] * 0.9, 2)}
    write(ws, "result.json", json.dumps({
        "unpaid": RECON["unpaid"], "duplicated": RECON["duplicated"],
        "mismatched": [{"id": i, "invoiced": invoiced[i], "paid": paid[i]} for i in RECON["mismatched"]]}))
    return ["done"]


TASKS = [
    EvalTask(
        id="ds-ab-playtest", category="data-science",
        provenance="Pixel Arena playtest A/B (arena-panel telemetry); a release decision from a dirty export",
        summary="Decide from player data whether a new game tutorial should replace the current one.",
        setup=_ab_setup, check=_ab_check, reference=_ab_reference, timeout_s=300,
        checkpoints=checkpoints(("read the notes", r"telemetry.{1,4}README"), ("read the data", r"playtest_ab"),
                                ("removed duplicate sessions", r"session_id.{0,300}(seen|dedup|drop_duplicates|distinct|unique|set\(|setdefault)|(seen|dedup|drop_duplicates|distinct|unique|setdefault).{0,300}session_id"),
                                ("tested significance", r"erfc|ztest|z_test|chi2|chisq|norm\.|fisher|p_value"), WROTE_RESULT),
        steps=(Step("We playtested two versions of the Pixel Arena tutorial and have to pick one for the next release. "
                    "The export and its notes are in {WS}/telemetry. Should we ship B instead of A? Give a recommendation "
                    "a skeptical lead would accept. Record it in {WS}/result.json with ship_b, sessions_a, sessions_b, "
                    "completion_rate_a, completion_rate_b and p_value."),),
    ),
    EvalTask(
        id="bo-pnl-runway", category="backoffice",
        provenance="Startup half-year close from a Brazilian-format ledger and a chart of accounts, for an investor meeting",
        summary="Close a startup's half-year from its ledger and say how long the cash lasts.",
        setup=_pnl_setup, check=_pnl_check, reference=_pnl_reference, timeout_s=300,
        checkpoints=checkpoints(("read the notes", r"finance.{1,4}README"), ("read the ledger", r"ledger"), ("used the chart of accounts", r"chart_of_accounts"),
                                ("used the cash balance", r"cash_balance"), WROTE_RESULT),
        steps=(Step("The investors meet tomorrow and want the first half of 2026 closed. The books and the board's notes "
                    "are in {WS}/finance. How did each month go, and how many months of cash do we have left at the current "
                    "burn? Prepare what the CFO needs to present. Record the key figures in {WS}/result.json: revenue, "
                    "gross_margin_pct and ebitda, each mapping 2026-01 to 2026-06 to its value, plus burn and runway_months."),),
    ),
    EvalTask(
        id="bo-reconcile", category="backoffice",
        provenance="Accounts receivable reconciliation: invoices vs bank statement with PIX/TED memo variants and noise",
        summary="Find what finance still has to collect or fix after comparing invoices with bank payments.",
        setup=_recon_setup, check=_recon_check, reference=_recon_reference, timeout_s=300,
        checkpoints=checkpoints(("read the notes", r"backoffice.{1,4}README"), ("read the invoices", r"invoices"), ("read the statement", r"bank_statement"), WROTE_RESULT),
        steps=(Step("Finance has to chase June's receivables. The invoices, the bank statement and our reconciliation notes "
                    "are in {WS}/backoffice. What do we still have to collect or fix? Record it in {WS}/result.json: unpaid "
                    "and duplicated (invoice ids) and mismatched (id, invoiced, paid)."),),
    ),
]
