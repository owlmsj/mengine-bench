# Dossier: which Brazilian anti-inflation plan delivered?

Ranking (RUBRIC.md score, 0 to 1): 1. Real, 2. Collor I, 3. Collor II

| plan | launch | IPCA Y-1 % | IPCA Y+1 % | months | score |
|---|---|---|---|---|---|
| Real | 1994-07-01 | 2477.15 | 22.41 | 60 | 0.9937 |
| Collor I | 1990-03-16 | 1972.91 | 472.7 | 10 | 0.5823 |
| Collor II | 1991-01-31 | 1620.97 | 1119.1 | 41 | 0.4217 |
| Bresser | 1987-06-12 | 79.66 | 980.21 | 19 | 0.095 |
| Cruzado | 1986-02-28 | 242.23 | 363.41 | 15 | 0.075 |
| Verao | 1989-01-15 | 980.21 | 1620.97 | 14 | 0.07 |

## Sources (every number above)
- All IPCA figures: IBGE SIDRA table 1737, variable 69 (accumulated in year, December): https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/198512,198612,198712,198812,198912,199012,199112,199212,199312,199412,199512
- Launch dates Cruzado 28 Feb 1986, Bresser 12 Jun 1987, Verao 15 Jan 1989, Collor I 16 Mar 1990, Real 1 Jul 1994 (real replaces cruzeiro real): https://en.wikipedia.org/wiki/Hyperinflation_in_Brazil
- Launch dates Collor I 16 Mar 1990, Collor II 31 Jan 1991; Real alternative 27 Feb 1994 (URV): https://pt.wikipedia.org/wiki/Plano_Collor
- months and scores: computed from the above with the RUBRIC.md formula.

## Reading
- Real: IPCA 2477.15 (1993) to 22.41 (1995), the only plan with a lasting fall.
- Collor I: IPCA 1972.91 (1989) to 472.70 (1991), but replaced after 10 months.
- Collor II: IPCA 1620.97 (1990) to 1119.10 (1992); its score rests mostly on the 41 months before the Real.
- Cruzado, Bresser, Verao: IPCA was higher the year after than the year before, so score_drop = 0.

## Assumptions
- Real launch = 1 Jul 1994 (currency). Using 27 Feb 1994 (URV) gives Collor II 36 months and score 0.3967; ranking unchanged.
- Whole months = completed months between the two dates. Real uses 60 per rubric.
- Dates come from Wikipedia (secondary source); IPCA from IBGE (primary).
