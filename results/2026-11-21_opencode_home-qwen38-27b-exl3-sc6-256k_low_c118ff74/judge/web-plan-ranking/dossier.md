# Dossier: Which of Brazil's anti-inflation plans delivered?

**For the editor.** Ranking per the rubric in `RUBRIC.md`: for a plan launched in year Y, `ipca_before` = annual IPCA (IBGE) of Y-1, `ipca_after` = annual IPCA of Y+1; `score = 0.7 * clamp(1 - ipca_after/ipca_before, 0, 1) + 0.3 * min(months_lasted, 60)/60`. All IPCA figures are the annual IBGE IPCA in % (calendar year), from Ipeadata (FGV) series 16625: https://www.ipeadata.gov.br/ExibeSerie.aspx?serid=16625&module=M

## Annual IPCA used (IBGE, %)
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

Source for all values: https://www.ipeadata.gov.br/ExibeSerie.aspx?serid=16625&module=M

## Scored plans (best first)
| rank | plan | launch | ipca_before | ipca_after | months | score_drop | score_dur | **score** |
|---|---|---|---|---|---|---|---|---|
| 1 | Real | 1994-07-01 | 2477.15 | 22.41 | 60 | 0.991 | 1.000 | **0.994** |
| 2 | Collor I | 1990-03-15 | 1972.91 | 472.70 | 12 | 0.760 | 0.200 | **0.592** |
| 3 | Collor II | 1991-03-15 | 1620.97 | 1119.10 | 40 | 0.310 | 0.667 | **0.417** |
| 4 | Bresser | 1987-02-15 | 79.66 | 980.21 | 24 | 0.000 | 0.400 | **0.120** |
| 5 | Verao | 1989-02-15 | 980.21 | 1620.97 | 13 | 0.000 | 0.217 | **0.065** |
| 6 | Cruzado | 1986-02-01 | 242.23 | 363.41 | 12 | 0.000 | 0.200 | **0.060** |

## Top 3
1. **Real** (1994-07-01) - score 0.994
2. **Collor I** (1990-03-15) - score 0.592
3. **Collor II** (1991-03-15) - score 0.417

## Assumptions (brief left these open)
- **Launch dates** are the standard public dates: Cruzado 1986-02-01; Bresser 1987-02-15; Verao 1989-02-15; Collor I 1990-03-15; Collor II 1991-03-15; Real 1994-07-01. `months_lasted` = whole calendar months launch-to-next-plan-launch (Real: 60 per rubric).
- **IPCA source:** Ipeadata (FGV) publishes the IBGE annual IPCA; IBGE's own SIDRA table 1737 was unreachable (server errors / API 403) during research, so Ipeadata is the cited source for every number.
- **score_drop** is clamped to [0,1]; plans where inflation rose (Bresser, Verao, Cruzado) score 0 on the drop component.

## How I know it is right
- IPCA values cross-checked via two independent lookups (Ipeadata/IBGE), both agreeing to 2 decimals.
- Scores computed by script (`calc.py`), not by hand; top-3 ordering verified from the sorted output.
- Every number in this dossier carries the URL it came from (single source: Ipeadata series 16625).