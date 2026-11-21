# Which of Brazil's anti-inflation plans delivered?

**Method.** Each plan is scored per RUBRIC.md from public data. Inflation is the
annual IPCA (IBGE, calendar year, %). For a plan launched in year Y:
`ipca_before` = IPCA of Y-1, `ipca_after` = IPCA of Y+1.
`score = 0.7 * clamp(1 - ipca_after/ipca_before, 0, 1) + 0.3 * min(months_lasted,60)/60`,
where `months_lasted` is whole calendar months to the next plan's launch
(Real: 60 by rubric). All IPCA figures from IBGE SIDRA table 1737
(https://sidra.ibge.gov.br/tabela/1737). Launch dates from FGV CPDOC Atlas
Histórico (https://atlas.fgv.br/verbete/6306) and Banco Central do Brasil
(https://www.bcb.gov.br/detalhenoticia/355/noticia).

## Scores

| Rank | Plan | Launch | IPCA before | IPCA after | Months | Score |
|---|---|---|---|---|---|---|
| 1 | Real | 01/07/1994 | 2477.15% (1993) | 22.41% (1995) | 60 | **0.9937** |
| 2 | Collor I | 16/03/1990 | 1972.91% (1989) | 472.70% (1991) | 10 | **0.5823** |
| 3 | Collor II | 31/01/1991 | 1620.97% (1990) | 1119.10% (1992) | 42 | **0.4267** |
| 4 | Bresser | 12/06/1987 | 79.66% (1986) | 980.21% (1988) | 19 | 0.095 |
| 5 | Cruzado | 28/02/1986 | 242.23% (1985) | 363.41% (1987) | 16 | 0.08 |
| 6 | Verao | 15/01/1989 | 980.21% (1988) | 1620.97% (1990) | 14 | 0.07 |

## Top 3

1. **Real (1994)** — the only plan that actually cut inflation. Annual IPCA
   fell from 2477.15% (1993) to 22.41% (1995), a 99.1% drop, and it is the
   reference case for durable stabilization. Score 0.9937.
2. **Collor I (1990)** — the asset freeze broke the 1989 hyperinflation
   spiral: IPCA fell from 1972.91% to 472.70%. It lasted only 10 months
   before Collor II, so durability is low. Score 0.5823.
3. **Collor II (1991)** — a partial, short-lived improvement (1620.97% to
   1119.10%) that held for 42 months until Real. Score 0.4267.

## What the numbers say

The Cruzado, Bresser and Verao plans all *failed* the drop test: in each case
the year after launch was more inflationary than the year before (Cruzado
242→363%, Bresser 80→980%, Verao 980→1621%), so their drop scores are zero and
their totals come only from a few months of life. Only the two Collor plans and
the Real plan reduced inflation. The Real plan is the clear winner: it is the
only one that both cut inflation by more than 99% and was durable.

## Assumptions

- "Launch date" = the plan's official start (Cruzado 28/02/1986; Bresser
  12/06/1987; Verao 15/01/1989; Collor I 16/03/1990; Collor II 31/01/1991;
  Real 01/07/1994, the currency's entry into circulation, not the 27/02/1994
  URV decree).
- `months_lasted` counts whole calendar months between launch dates, per rubric.
- IPCA values are IBGE's final annual series; no re-basing applied.

## Sources

- IPCA annual series (all figures): https://sidra.ibge.gov.br/tabela/1737
- Plan launch dates: https://atlas.fgv.br/verbete/6306 ;
  https://www.bcb.gov.br/detalhenoticia/355/noticia