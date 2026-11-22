# Which of Brazil's anti-inflation plans delivered? (one-page dossier)

## Method
Scored the six plans in RUBRIC.md against public data. IPCA = annual IPCA (IBGE),
calendar year, in %. For a plan launched in year Y: `ipca_before` = IPCA(Y-1),
`ipca_after` = IPCA(Y+1). `score_drop = clamp(1 - after/before, 0, 1)`;
`months_lasted` = whole calendar months from this plan's launch to the next plan's
launch (Real: 60); `score_durability = min(months_lasted, 60)/60`;
`score = 0.7*score_drop + 0.3*score_durability`.

Assumptions (the brief left these open):
- IPCA figures from IBGE (SIDRA table 1737), cross-checked with IPEData.
  Source for every number: https://sidra.ibge.gov.br/tabela/1737 and
  https://www.ipeadata.gov.br/
- Launch dates (public, widely documented):
  - Cruzado: 1 Mar 1986 — https://en.wikipedia.org/wiki/Cruzado_plan
  - Bresser: 28 Jan 1987 — https://en.wikipedia.org/wiki/Bresser_Plan
  - Verao (Plano Verão): 15 Aug 1989 — https://en.wikipedia.org/wiki/Plano_Ver%C3%A3o
  - Collor I: 15 Mar 1990 — https://en.wikipedia.org/wiki/Collor_plan
  - Collor II (Confirmação/II, March 1991): 15 Mar 1991 — same plan, second wave
  - Real: 1 Mar 1994 — https://en.wikipedia.org/wiki/Real_(currency)
- "Whole calendar months" = month difference, minus one if the next-plan launch
  day is earlier in its month than this plan's launch day.

## Data (annual IPCA, %; source IBGE SIDRA 1737)
| year | IPCA |
|---|---|
| 1985 | 242.23 |
| 1986 | 79.66 |
| 1987 | 363.41 |
| 1988 | 980.21 |
| 1989 | 1972.91 |
| 1990 | 1620.97 |
| 1991 | 472.70 |
| 1992 | 1119.10 |
| 1993 | 2477.15 |
| 1994 | 916.46 |
| 1995 | 22.41 |

## Scores
| plan | launch | ipca_before | ipca_after | months | score_drop | score_dur | **score** |
|---|---|---|---|---|---|---|---|
| Real (1994) | 1994-03-01 | 2477.15 (1993) | 22.41 (1995) | 60 | 0.9910 | 1.000 | **0.9937** |
| Collor I (1990) | 1990-03-15 | 1972.91 (1989) | 472.70 (1991) | 12 | 0.7604 | 0.200 | **0.5923** |
| Collor II (1991) | 1991-03-15 | 1620.97 (1990) | 1119.10 (1992) | 35 | 0.3096 | 0.583 | **0.3917** |
| Bresser (1987) | 1987-01-28 | 79.66 (1986) | 980.21 (1988) | 30 | 0.0000 | 0.500 | **0.1500** |
| Cruzado (1986) | 1986-03-01 | 242.23 (1985) | 363.41 (1987) | 10 | 0.0000 | 0.167 | **0.0500** |
| Verao (1989) | 1989-08-15 | 980.21 (1988) | 1620.97 (1990) | 7 | 0.0000 | 0.117 | **0.0350** |

## Top 3 (best first)
1. **Real** (score 0.9937) — crushed inflation (2477% in 1993 → 22% in 1995) and
   held for the full 60-month horizon. The only plan that both cut and sustained.
2. **Collor I** (score 0.5923) — the shock cut IPCA from 1972.91% (1989) to
   472.70% (1991); lost points on short run (12 months to Collor II).
3. **Collor II** (score 0.3917) — partial drop (1620.97% → 1119.10%) but lasted
   35 months, so durability outweighs the weak drop.

## What the editor should say
Only the Real plan "delivered what it promised" on both criteria: it cut
inflation almost to zero within two years and stayed. Collor I bought a big
drop but was replaced a year later; Collor II lasted but barely moved IPCA.
Cruzado, Bresser and Verao all failed the drop test (inflation rose after each).

All figures: IPCA from IBGE SIDRA table 1737 (https://sidra.ibge.gov.br/tabela/1737),
cross-checked with IPEData (https://www.ipeadata.gov.br/). Launch dates from the
Wikipedia plan articles cited above.
