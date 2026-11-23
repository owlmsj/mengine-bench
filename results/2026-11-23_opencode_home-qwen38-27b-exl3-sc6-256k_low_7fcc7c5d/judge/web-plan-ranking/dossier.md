# Dossier: Brazil's anti-inflation plans, ranked by delivery

**Method.** Each plan is scored 0–1 from public data: 70% weight on how much
annual IPCA (IBGE) fell between the year before and the year after launch
(score_drop, clamped to 0–1), 30% on durability in whole calendar months until
the next plan (score_durability, capped at 60 months). IPCA values: IBGE SIDRA
table 1737 (https://sidra.ibge.gov.br/tabela/1737). Launch dates: official
decrees/MPs as cited below.

## Ranking (best first)

| # | Plan | Launched | IPCA before | IPCA after | Months lasted | Score |
|---|------|----------|-------------|------------|---------------|-------|
| 1 | Real | 1994-07-01 | 2,477.15% (1993) | 22.41% (1995) | 60 (cap) | 0.994 |
| 2 | Collor I | 1990-03-15 | 1,972.91% (1989) | 472.70% (1991) | 10 | 0.582 |
| 3 | Collor II | 1991-01-31 | 1,620.97% (1990) | 1,119.10% (1992) | 42 | 0.427 |

Full field: Cruzado 0.080, Bresser 0.095, Verao 0.070 — all three saw
inflation accelerate after launch (score_drop = 0); they rank only on
durability.

## What the numbers say

- **Real (0.994)** is the only plan that delivered: IPCA collapsed from
  2,477.15% in 1993 to 22.41% in 1995 (https://sidra.ibge.gov.br/tabela/1737).
  Launched 1 July 1994 (Banco Central do Brasil,
  https://www.bcb.gov.br/en/content/1488).
- **Collor I (0.582)** cut IPCA from 1,972.91% (1989) to 472.70% (1991)
  (https://sidra.ibge.gov.br/tabela/1737) but lasted only 10 months before
  Collor II replaced it (MP 168, 15 Mar 1990; FGV CPDOC,
  https://cpdoc.fgv.br/producao-academica/planos-economicos).
- **Collor II (0.427)** reduced IPCA from 1,620.97% (1990) to 1,119.10% (1992)
  (https://sidra.ibge.gov.br/tabela/1737) and held 42 months, but the drop was
  modest and inflation re-accelerated by 1993 (2,477.15%).
- **Cruzado, Bresser, Verao** all failed the drop test: IPCA after launch was
  higher than before (363.41% vs 242.23%; 980.21% vs 79.66%; 1,620.97% vs
  980.21%), so their scores come entirely from durability (16, 19 and 14
  months respectively).

## Sources

- IPCA annual series 1985–1996: IBGE SIDRA table 1737,
  https://sidra.ibge.gov.br/tabela/1737
- Plan launch dates: official decrees/MPs (Cruzado: DL 2.283, 27/02/1986;
  Bresser: DL 2.335, 12/06/1987; Verao: MP 32, 15/01/1989; Collor I: MP 168,
  15/03/1990; Collor II: MP 294/295, 31/01/1991; Real: 01/07/1994, BCB
  https://www.bcb.gov.br/en/content/1488)

## Assumptions

- "Launch date" = the decree/MP date, not the DOU publication date (one day
  later in most cases); does not affect month counts.
- Real's "next plan" is none, so months_lasted = 60 per the rubric.
- IPCA values are the official IBGE annual figures as compiled in SIDRA 1737.