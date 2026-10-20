"""Data science + startup backoffice tasks.

Messy-but-real inputs on purpose: duplicated telemetry rows, a Brazilian
ledger with `;` and `1.234,56`, bank memos in three formats. The gold is the
exact number a careful analyst gets; rounding is tolerated, a different
method is not.
"""

from __future__ import annotations

import csv
import io
import json
import math
import random
from collections import defaultdict
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from mengine_bench.core import (
    FAST,
    FULL,
    CheckResult,
    EvalTask,
    Step,
    close,
    read,
    read_json,
    write,
)

RULES = "Write your files inside {WS}. Do not ask for confirmation."

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
          "or with a leading space. `completed_tutorial` is 0/1.\n")


def _ab_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    exp = _ab_expected()
    got = read_json(ws, "ab_result.json")
    got = got if isinstance(got, dict) else {}
    result.add("deduplicated session counts", got.get("sessions_a") == exp["sessions_a"] and got.get("sessions_b") == exp["sessions_b"])
    result.add("completion rates", close(got.get("rate_a"), float(exp["rate_a"]), 1e-3) and close(got.get("rate_b"), float(exp["rate_b"]), 1e-3))
    result.add("absolute and relative lift", close(got.get("abs_lift"), float(exp["abs_lift"]), 1e-3) and close(got.get("rel_lift"), float(exp["rel_lift"]), 2e-3))
    result.add("two-proportion z-test p-value", close(got.get("p_value"), float(exp["p_value"]), max(1e-3, float(exp["p_value"]) * 0.05)))
    result.add("ship decision", got.get("ship_b") is exp["ship_b"])
    result.add("mean match minutes", close(got.get("mean_minutes_a"), float(exp["mean_minutes_a"]), 0.02) and close(got.get("mean_minutes_b"), float(exp["mean_minutes_b"]), 0.02))
    return result


def _ab_reference(ws: Path) -> list[str]:
    write(ws, "ab_result.json", json.dumps(_ab_expected()))
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
    write(ws, "finance/chart_of_accounts.csv", "account;name;pnl_line\n" + "".join(f"{c};{n};{line}\n" for c, n, line in CHART))
    write(ws, "finance/cash_balance.txt", f"Consolidated balance on 30/06/2026: R$ {_brl(CASH)}\n")


def _pnl_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    table, runway = _pnl_expected()
    got = {row.get("line"): row for row in csv.DictReader(io.StringIO(read(ws, "pnl.csv") or ""))}
    result.add("pnl.csv lines in order", list(got) == PNL_LINES)
    for line in PNL_LINES:
        tol = 0.02 if line == "gross_margin_pct" else 1.0
        result.add(f"{line} per month", line in got and all(close(got[line].get(ym), table[line][ym], tol) for ym in MONTHS))
    rj = read_json(ws, "runway.json")
    rj = rj if isinstance(rj, dict) else {}
    result.add("3-month average burn", close(rj.get("burn_avg_3m"), runway["burn_avg_3m"], 1.0))
    result.add("runway in months", close(rj.get("runway_months"), runway["runway_months"], 0.051))
    return result


def _pnl_reference(ws: Path) -> list[str]:
    table, runway = _pnl_expected()
    lines = ["line," + ",".join(MONTHS)] + [f"{line}," + ",".join(f"{table[line][ym]:.2f}" for ym in MONTHS) for line in PNL_LINES]
    write(ws, "pnl.csv", "\n".join(lines) + "\n")
    write(ws, "runway.json", json.dumps({"burn_avg_3m": round(runway["burn_avg_3m"], 2), "runway_months": round(runway["runway_months"], 1)}))
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


def _recon_setup(ws: Path) -> None:
    write(ws, "backoffice/invoices.csv", "id,customer,amount,due_date\n" + "".join(
        f"{i},{c},{v:.2f},2026-06-20\n" for i, c, v in _invoices()))
    write(ws, "backoffice/bank_statement_june.csv", "date,memo,amount\n" + "".join(
        f"{d},{m},{v:.2f}\n" for d, m, v in _bank_rows()))


def _recon_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    got = read_json(ws, "reconciliation.json")
    got = got if isinstance(got, dict) else {}
    result.add("unpaid invoices", sorted(got.get("unpaid") or []) == RECON["unpaid"])
    result.add("duplicated payments", sorted(got.get("duplicated") or []) == RECON["duplicated"])
    mism = got.get("mismatched") or []
    ids = sorted(str(m.get("id")) for m in mism if isinstance(m, dict))
    result.add("mismatched amounts", ids == RECON["mismatched"])
    invoiced = {i: v for i, _, v in _invoices()}
    paid = {"INV-1021": round(invoiced["INV-1021"] - 250.0, 2), "INV-1036": round(invoiced["INV-1036"] * 0.9, 2)}
    result.add("invoiced vs paid on mismatches", ids == RECON["mismatched"] and all(
        close(m.get("invoiced"), invoiced[str(m.get("id"))], 0.01)
        and close(m.get("paid"), paid[str(m.get("id"))], 0.01) for m in mism if isinstance(m, dict)))
    return result


def _recon_reference(ws: Path) -> list[str]:
    invoiced = {i: v for i, _, v in _invoices()}
    paid = {"INV-1021": invoiced["INV-1021"] - 250.0, "INV-1036": round(invoiced["INV-1036"] * 0.9, 2)}
    write(ws, "reconciliation.json", json.dumps({
        "unpaid": RECON["unpaid"], "duplicated": RECON["duplicated"],
        "mismatched": [{"id": i, "invoiced": invoiced[i], "paid": paid[i]} for i in RECON["mismatched"]]}))
    return ["done"]


# par_s: DeepSeek V4.1 Flash wall times from the maintainers' v1 FAST run
# (2026-09-23), rounded up. bo-reconcile was not in that run: 2x bo-pnl-runway
# (27.5 s), the closest backoffice task.
TASKS = [
    EvalTask(
        id="ds-ab-playtest", category="data-science", suites=frozenset({FAST, FULL}),
        provenance="Pixel Arena playtest A/B (arena-panel telemetry); two-proportion z-test on a dirty export",
        summary="Compare two game tutorials using player data and decide which one to release.",
        setup=_ab_setup, check=_ab_check, reference=_ab_reference, timeout_s=300, par_s=25,
        steps=(Step("Read {WS}/telemetry/README.md and analyze {WS}/telemetry/playtest_ab.csv. Write {WS}/ab_result.json with "
                    "the keys sessions_a, sessions_b, rate_a, rate_b (tutorial completion), abs_lift (B-A), rel_lift "
                    "((B-A)/A), p_value (two-sided two-proportion z-test with pooled variance), ship_b (true if p<0.05 and "
                    "B>A), mean_minutes_a, mean_minutes_b. " + RULES),),
    ),
    EvalTask(
        id="bo-pnl-runway", category="backoffice", suites=frozenset({FAST, FULL}),
        provenance="Startup monthly close: P&L from a Brazilian-format ledger (`;`, 1.234,56) + chart of accounts, burn and runway",
        summary="Calculate monthly profit, cash burn and how long the business can keep running from its ledger.",
        setup=_pnl_setup, check=_pnl_check, reference=_pnl_reference, timeout_s=360, par_s=28,
        steps=(Step("Close the startup's half-year using {WS}/finance/ledger.csv (separator ;, Brazilian number format "
                    "1.234,56, dates dd/mm/yyyy, costs negative) and {WS}/finance/chart_of_accounts.csv. Write {WS}/pnl.csv "
                    "with header line,2026-01,...,2026-06 and these lines in this order: revenue (net of refunds), cogs, "
                    "gross_profit, gross_margin_pct (0-100), sales_marketing, rnd, ga, ebitda; costs as positive numbers, "
                    "2 decimals. Financial result does NOT go into EBITDA. Write {WS}/runway.json with burn_avg_3m (mean "
                    "of -ebitda from April to June) and runway_months (balance in {WS}/finance/cash_balance.txt / burn, "
                    "1 decimal). " + RULES),),
    ),
    EvalTask(
        id="bo-reconcile", category="backoffice", suites=frozenset({FULL}),
        provenance="Accounts receivable reconciliation: invoices vs bank statement with PIX/TED memo variants and noise",
        summary="Match invoices to bank payments and report missing, duplicate or incorrect payments.",
        setup=_recon_setup, check=_recon_check, reference=_recon_reference, timeout_s=300, par_s=55,
        steps=(Step("Reconcile {WS}/backoffice/invoices.csv with {WS}/backoffice/bank_statement_june.csv (the memo cites "
                    "the invoice in different formats; ignore fees, interest and PIX transfers without an identifiable "
                    "invoice). Write {WS}/reconciliation.json with unpaid (ids without payment), duplicated (ids paid more "
                    "than once) and mismatched (list of objects id, invoiced, paid when the paid amount differs). " + RULES),),
    ),
]
