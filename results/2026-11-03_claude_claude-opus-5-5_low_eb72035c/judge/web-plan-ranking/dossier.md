# Which Brazilian anti-inflation plan delivered? (RUBRIC.md scoring)

Score = 0.7*clamp(1 - IPCA(Y+1)/IPCA(Y-1),0,1) + 0.3*min(months,60)/60. IPCA annual % (IBGE, https://www.ibge.gov.br/explica/inflacao.php). Launch dates: plan pages cited per row.

| Rank | Plan | Launch | IPCA Y-1 | IPCA Y+1 | Months | Score |
|---|---|---|---|---|---|---|
| 1 | Real | 1994-07-01 (https://en.wikipedia.org/wiki/Plano_Real) | 2477.15 (1993) | 22.41 (1995) | 60 (cap) | 0.994 |
| 2 | Collor I | 1990-03-16 (https://en.wikipedia.org/wiki/Collor_Plan) | 1972.91 (1989) | 472.70 (1991) | 10 | 0.582 |
| 3 | Collor II | 1991-01-31 (https://en.wikipedia.org/wiki/Collor_Plan) | 1620.97 (1990) | 1119.10 (1992) | 41 | 0.422 |
| 4 | Bresser | 1987-06-12 (https://pt.wikipedia.org/wiki/Plano_Bresser) | 79.66 (1986) | 980.21 (1988) | 19 | 0.095 |
| 5 | Cruzado | 1986-02-28 (https://en.wikipedia.org/wiki/Cruzado_Plan) | 242.23 (1985) | 363.41 (1987) | 15 | 0.075 |
| 6 | Verao | 1989-01-15 (https://pt.wikipedia.org/wiki/Plano_Ver%C3%A3o) | 980.21 (1988) | 1620.97 (1990) | 14 | 0.070 |

All IPCA values: https://www.ibge.gov.br/explica/inflacao.php (IBGE historical series).

## Caveats for the editor
- Only Real truly ended high inflation. Collor I/II rank high partly because the rubric compares Y-1 to Y+1 and 1989-91 baselines were extreme; Collor II's 41 months reflects no new plan until Real, not success.
- Cruzado, Bresser, Verao score ~0: inflation was higher the year after.
- Months = whole calendar months between launch dates.
- Values were not re-fetched live in this run (3.5 min budget); figures are the standard IBGE annual IPCA series and should be spot-checked against the IBGE link before print.
