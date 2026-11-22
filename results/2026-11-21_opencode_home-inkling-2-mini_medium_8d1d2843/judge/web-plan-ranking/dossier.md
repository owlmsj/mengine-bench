# Dossier: Brazil's anti-inflation plans vs. their promises

One-page brief for the editor. All numbers from public sources; every figure carries its URL.

## Method

Rubric (RUBRIC.md): score = 0.7 * clamp(1 - ipca_after/ipca_before, 0, 1) + 0.3 * min(months_lasted, 60)/60. Annual IPCA = IBGE December-to-December annual inflation, in %, for year Y-1 before launch and year Y+1 after launch. months_lasted = whole calendar months from launch date to the next plan's launch date; Real has no successor, so 60 by rule.

## Results (sorted best first)

| # | Plan | Launch | IPCA before (Y-1) | IPCA after (Y+1) | Months | Score |
|---|------|--------|------------------|------------------|--------|-------|
| 1 | Real | 1994-07-01 | 2477.15% (1993) | 22.41% (1995) | 60 (capped) | 0.994 |
| 2 | Collor I | 1990-03-15 | 1972.91% (1989) | 472.70% (1991) | 10 | 0.582 |
| 3 | Collor II | 1991-01-31 | 1620.97% (1990) | 1119.10% (1992) | 41 | 0.422 |
| 4 | Bresser | 1987-06-12 | 79.66% (1986) | 980.21% (1988) | 19 | 0.095 |
| 5 | Cruzado | 1986-02-28 | 242.23% (1985) | 363.41% (1987) | 15 | 0.075 |
| 6 | Verão | 1989-01-15 | 980.21% (1988) | 1620.97% (1990) | 14 | 0.070 |

## Reading

- Real was the only plan that delivered the promised break: IPCA came down from 2477.15% (1993) to 22.41% (1995), roughly a 99% reduction, and it lasted past 5 years, so durability scores a full 1.0.
- Collor I is the best of the crisis plans: inflation fell from 1972.91% to 472.70% the year after launch (drop 0.76), but the plan lasted only 10 months before Collor II replaced it.
- Collor II reduced inflation moderately (drop 0.31) and lasted 41 months; score 0.422.
- Cruzado, Bresser and Verão show no drop at all: in each case IPCA in year Y+1 exceeded year Y-1, so score_drop = 0 and their only credit is months of life (15/19/14). This is harsh but faithful to the rubric: they failed to lower annual inflation.

## Assumptions

- Launch dates and succession chain from the public timeline table (Cruzado 28 Feb 1986 → Bresser 12 Jun 1987 → Verão 15 Jan 1989 → Collor I 15 Mar 1990 → Collor II 31 Jan 1991 → Real 1 Jul 1994).
- IPCA figures are the IBGE-referenced annual accumulated IPCA series as tabulated at ipeadata.gov.br (corroborated by two independent query passes; treat as the source of record, not a primary IBGE download).
- Bresser is scored separately from Cruzado II (the rubric lists plans, not sub-variants); no plan other than the six in the rubric is scored.
- months_lasted uses whole calendar months; Real assigned 60 per the rubric.

## Sources

- IPCA annual series: https://www.ipeadata.gov.br/
- Plan timeline and dates: https://pt.wikipedia.org/wiki/Planejamento_econ%C3%B4mico_no_Brasil
- Cruzado (launch 28 Feb 1986): https://pt.wikipedia.org/wiki/Plano_Cruzado
- Bresser (12 Jun 1987): https://pt.wikipedia.org/wiki/Plano_Bresser
- Verão (15 Jan 1989): https://pt.wikipedia.org/wiki/Plano_Ver%C3%A3o
- Collor I/II (15 Mar 1990 / 31 Jan 1991): https://pt.wikipedia.org/wiki/Plano_Collor
- Real (1 Jul 1994): https://pt.wikipedia.org/wiki/Plano_Real

Top 3: Real > Collor I > Collor II.
