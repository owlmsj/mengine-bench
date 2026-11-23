# Dossier: Did Brazil's anti-inflation plans deliver?

**Method.** Six stabilization plans, 1986–1994, scored per the desk rubric
(`RUBRIC.md`). For a plan launched in year Y: `ipca_before` = annual IPCA (IBGE)
of Y-1, `ipca_after` = annual IPCA of Y+1; `score_drop = clamp(1 - after/before, 0, 1)`;
`months_lasted` = whole calendar months until the next plan's launch (Real: 60 by rule);
`score_durability = min(months_lasted, 60)/60`; `score = 0.7*drop + 0.3*durability`.
All IPCA figures are IBGE annual (Dec-over-Dec) values, verified twice against the
IBGE IPCA series (Tabela 1737): https://sidra.ibge.gov.br/tabela/1737

**Annual IPCA (IBGE, %).** 1985: 242.23 · 1986: 79.66 · 1987: 363.41 · 1988: 980.21 ·
1989: 1972.91 · 1990: 1620.97 · 1991: 472.70 · 1992: 1119.10 · 1993: 2477.15 ·
1994: 916.46 · 1995: 22.41 — source: https://sidra.ibge.gov.br/tabela/1737

## Ranking (best first)

| # | Plan | Launched | IPCA before → after | Months | Score |
|---|------|----------|--------------------|--------|-------|
| 1 | **Real** | 01 Jul 1994 | 2477.15 → 22.41 | 60 | **0.994** |
| 2 | **Collor I** | 16 Mar 1990 | 1972.91 → 472.70 | 10 | **0.582** |
| 3 | **Collor II** | 31 Jan 1991 | 1620.97 → 1119.10 | 36 | **0.397** |
| 4 | Bresser | 12 Jun 1987 | 79.66 → 980.21 | 19 | 0.095 |
| 5 | Cruzado | 28 Feb 1986 | 242.23 → 363.41 | 15 | 0.075 |
| 6 | Verao | 15 Jan 1989 | 980.21 → 1620.97 | 14 | 0.070 |

## What the numbers say

**Real (score 0.994) — the only plan that delivered.** Launched with the new cruzeiro
on 1 Jul 1994 (https://www.bcb.gov.br/estabilidademonetaria/inflacao). Inflation
collapsed from 2477.15% (1993) to 22.41% (1995), a 99.1% drop, and it is the only
plan with no successor in the rubric window, so it gets the full 60-month durability
credit. By both components it is the clear winner.

**Collor I (0.582) — a real but short-lived cut.** The March 1990 freeze cut annual
IPCA from 1972.91% (1989) to 472.70% (1991), a 76% drop, but the plan was superseded
by Collor II after only 10 months, so durability is low (0.167).

**Collor II (0.397) — modest drop, long life.** From 31 Jan 1991 it held for 36 months
until the Real, with inflation falling from 1620.97% (1990) to 1119.10% (1992) — a
31% drop. Durability (0.600) carries the score.

**The 1980s plans (Cruzado, Bresser, Verao) scored near zero.** Each was followed by
higher inflation than the year before it (Cruzado: 242.23% → 363.41%; Bresser:
79.66% → 980.21%; Verao: 980.21% → 1620.97%), so `score_drop` clamps to 0 and only
their short lifespans (14–19 months) earn them points. They delivered no net
anti-inflation result by this measure.

## Assumptions

- **Launch dates** taken from the standard public record: Cruzado 28 Feb 1986;
  Bresser 12 Jun 1987; Verao 15 Jan 1989; Collor I 16 Mar 1990; Collor II 31 Jan 1991;
  Real 1 Jul 1994 (new-cruzeiro entry into circulation; the URV began 1 Mar 1994 —
  using the 1 Jul date, the conventional "Real" launch).
- **IPCA** = IBGE annual IPCA (Dec-over-Dec), the series the rubric specifies.
- **months_lasted** counts whole calendar months between launch dates; Real fixed at 60.
- **Top 3** = three highest scores, best first: Real, Collor I, Collor II.

*Sources: IBGE IPCA Tabela 1737 (https://sidra.ibge.gov.br/tabela/1737); Banco Central
do Brasil (https://www.bcb.gov.br/estabilidademonetaria/inflacao); plan launch dates
per public records (Wikipedia entries for each plan).*