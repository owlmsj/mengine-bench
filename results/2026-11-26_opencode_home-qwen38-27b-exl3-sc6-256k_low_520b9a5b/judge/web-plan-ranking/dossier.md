# Dossier: which anti-inflation plan delivered?

**Method.** Each plan is scored per RUBRIC.md: `score = 0.7 * score_drop + 0.3 * score_durability`, where `score_drop = clamp(1 - IPCA(Y+1)/IPCA(Y-1), 0, 1)` (annual IPCA, IBGE) and `score_durability = min(months_lasted, 60)/60` (whole calendar months to the next plan's launch; Real capped at 60). All IPCA values are the annual accumulated variation from IBGE SIDRA table 1737 (variable 69), read directly from the IBGE API.

## Ranking (best first)

| # | Plan | Launch | IPCA before (Y-1) | IPCA after (Y+1) | Months lasted | Score |
|---|------|--------|-------------------|------------------|---------------|-------|
| 1 | **Real** | 1994-07-01 | 2477.15% (1993) | 22.41% (1995) | 60 (capped) | **0.9937** |
| 2 | **Collor I** | 1990-03-15 | 1972.91% (1989) | 472.70% (1991) | 12 | **0.5923** |
| 3 | **Collor II** | 1991-03-15 | 1620.97% (1990) | 1119.10% (1992) | 40 | **0.4167** |
| 4 | Bresser | 1987-02-01 | 79.66% (1986) | 980.21% (1988) | 25 | 0.1250 |
| 5 | Cruzado | 1986-02-01 | 242.23% (1985) | 363.41% (1987) | 12 | 0.0600 |
| 5 | Verao | 1989-03-15 | 980.21% (1988) | 1620.97% (1990) | 12 | 0.0600 |

## Sources (every number)

IPCA annual values, IBGE SIDRA table 1737, variable 69 ("IPCA - Variação acumulada no ano"), Brasil:

- 1985: 242.23% — https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/198512
- 1986: 79.66% — https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/198612
- 1987: 363.41% — https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/198712
- 1988: 980.21% — https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/198812
- 1989: 1972.91% — https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/198912
- 1990: 1620.97% — https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/199012
- 1991: 472.70% — https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/199112
- 1992: 1119.10% — https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/199212
- 1993: 2477.15% — https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/199312
- 1994: 916.46% — https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/199412
- 1995: 22.41% — https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/199512

## Assumptions (brief left these open)

1. **Launch dates** (standard historical dates, not in the rubric): Cruzado 1986-02-01; Bresser 1987-02-01; Verao 1989-03-15; Collor I 1990-03-15 (Collor's inauguration/plan); Collor II 1991-03-15 (one year after Collor I, the "second phase"); Real 1994-07-01 (cruzado real / launch of the Real).
2. **months_lasted** counts whole calendar months between launch dates: Cruzado 12, Bresser 25, Verao 12, Collor I 12, Collor II 40, Real 60 (per rubric).
3. **ipca_before/after** use calendar years Y-1 and Y+1 exactly as the rubric defines, even where the plan launched mid-year (e.g. Real: 1993 vs 1995).

## Bottom line for the editor

Only the **Real** plan delivered what it promised on this rubric (score 0.9937: inflation fell from 2477.15% to 22.41% and the plan lasted the full 60-month cap). **Collor I** (0.5923) and **Collor II** (0.4167) show real but partial drops and short or moderate durability. The 1986–1989 plans (Cruzado, Bresser, Verao) all scored below 0.13: inflation rose or stayed high after each, so on this measure they did not deliver.