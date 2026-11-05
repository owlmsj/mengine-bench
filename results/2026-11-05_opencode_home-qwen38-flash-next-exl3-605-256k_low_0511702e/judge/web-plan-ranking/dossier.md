# Dossier: which Brazilian anti-inflation plan delivered?

For the editor. Ranking produced with the house rubric (RUBRIC.md): score =
0.7 x inflation drop + 0.3 x durability, using annual IPCA (IBGE) for the
calendar year before (Y-1) and after (Y+1) each plan's launch year, and whole
calendar months from launch to the next plan.

## Ranking (best first)

| # | Plan | Launch | IPCA before (Y-1) | IPCA after (Y+1) | Months | Score |
|---|------|--------|-------------------|------------------|--------|-------|
| 1 | Real | 1994-07-01 | 2476.95 (1993) | 22.41 (1995) | 60 (no successor) | 0.9937 |
| 2 | Collor I | 1990-03-16 | 1764.95 (1989) | 472.26 (1991) | 10 | 0.5627 |
| 3 | Collor II | 1991-01-31 | 1584.46 (1990) | 1119.14 (1992) | 41 | 0.4106 |
| 4 | Bresser | 1987-06-12 | 270.81 (1986) | 933.32 (1988) | 19 | 0.095 |
| 5 | Cruzado | 1986-02-28 | 226.03 (1985) | 365.88 (1987) | 15 | 0.075 |
| 6 | Verao | 1989-01-15 | 933.32 (1988) | 1584.46 (1990) | 14 | 0.07 |

Sources for every number: annual IPCA from IBGE SIDRA table 1330
(https://sidra.ibge.gov.br/tabela/1330); launch dates from the plan articles
at pt.wikipedia.org (Plano_Cruzado, Plano_Bresser, Plano_Ver%C3%A3o,
Plano_Collor, Plano_Real, URLs listed per plan in result.json).

## The story in one paragraph

Only the Real Plan delivered what it promised: annual IPCA fell from 2476.95%
(1993) to 22.41% (1995), a 99% reduction, and it never had a successor plan
(scoring the full durability credit). Collor I looks strong on the drop
(1764.95% in 1989 to 472.26% in 1991) but was frozen out after 10 months and
inflation stayed in the triple digits. Collor II gets its points mostly from
durability (41 months) despite a modest drop. Cruzado, Bresser and Verao score
near zero: in each case the calendar-year IPCA two years later was higher than
before the plan, so the drop term is zero and only partial durability counts.

## Assumptions (stated for the record)

- Annual IPCA = IBGE calendar-year variation, as published in SIDRA table 1330.
- Launch dates: Cruzado 28 Feb 1986; Bresser 12 Jun 1987; Verao 15 Jan 1989;
  Collor I 16 Mar 1990; Collor II 31 Jan 1991; Real 1 Jul 1994 (currency
  launch day). Verao is cited as 15 or 16 Jan 1989 in sources; either gives
  14 months.
- months_lasted = whole calendar months between launch dates (a month counts
  only when the day-of-month has passed); Real uses 60 per the rubric.
- Collor I and Collor II are treated as separate plans per the rubric table.

## Caveats for the piece

- The rubric compares calendar years around the launch, so a plan launched
  mid-year gets "credited" with the following calendar year's inflation
  (e.g. Real's 1994 IPCA of 916.08% still reflects pre-Real months). This
  favors plans launched early in a year and is the same for all plans only
  approximately.
- Collor I's drop owes much to the collateral blockade, not a durable
  monetary regime; the durability term captures that it did not last.
- Figures were read from the public IBGE SIDRA table page; if the editor
  wants a primary citation in print, cite "IBGE, SIDRA table 1330, IPCA
  annual variation" with the URL above.