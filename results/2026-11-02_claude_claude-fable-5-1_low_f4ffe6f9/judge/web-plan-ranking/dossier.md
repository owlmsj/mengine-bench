# Brazil's anti-inflation plans: which one delivered?

Scoring follows RUBRIC.md: score = 0.7 x inflation drop (annual IPCA of the year after launch vs the year before, clamped to 0..1) + 0.3 x durability (whole months until the next plan, capped at 60; Real fixed at 60). Annual IPCA (IBGE, % per calendar year) from https://www.portalbrasil.net/ipca.htm. Launch dates from Portuguese Wikipedia (URLs per row).

| Rank | Plan | Launch | IPCA year before | IPCA year after | Months lasted | Drop score | Score |
|---|---|---|---|---|---|---|---|
| 1 | Real | 1994-07-01 (https://pt.wikipedia.org/wiki/Plano_Real) | 1993: 2477.15% | 1995: 22.41% | 60 (rubric) | 0.991 | 0.994 |
| 2 | Collor I | 1990-03-16 (https://pt.wikipedia.org/wiki/Plano_Collor) | 1989: 1972.91% | 1991: 472.69% | 10 (to Collor II, 1991-01-31) | 0.760 | 0.582 |
| 3 | Collor II | 1991-01-31 (https://pt.wikipedia.org/wiki/Plano_Collor) | 1990: 1620.96% | 1992: 1119.09% | 41 (to Real, 1994-07-01) | 0.310 | 0.422 |
| 4 | Bresser | 1987-06-12 (https://pt.wikipedia.org/wiki/Plano_Bresser) | 1986: 79.65% | 1988: 980.22% | 19 (to Verao, 1989-01-15) | 0 | 0.095 |
| 5 | Cruzado | 1986-02-28 (https://pt.wikipedia.org/wiki/Plano_Cruzado) | 1985: 242.24% | 1987: 363.41% | 15 (to Bresser, 1987-06-12) | 0 | 0.075 |
| 6 | Verao | 1989-01-15 (https://pt.wikipedia.org/wiki/Plano_Ver%C3%A3o) | 1988: 980.22% | 1990: 1620.96% | 14 (to Collor I, 1990-03-16) | 0 | 0.070 |

All IPCA figures: https://www.portalbrasil.net/ipca.htm (IBGE series, "acumulado no ano").

## Top 3, best first

1. **Real (1994)**: the only plan whose year-after inflation was lower than the year before by more than 90 percent. Inflation fell from 2477.15% (1993) to 22.41% (1995) and the plan was never replaced. Score 0.994.
2. **Collor I (1990)**: inflation dropped from 1972.91% (1989) to 472.69% (1991), a 76 percent fall, but the plan lasted only 10 months before Collor II. Score 0.582.
3. **Collor II (1991)**: a 31 percent fall (1620.96% in 1990 to 1119.09% in 1992) and 41 months until the Real. Score 0.422.

## What the ranking does not say

- The three Sarney-era plans (Cruzado, Bresser, Verao) all score zero on the drop term because inflation in the year after each launch was higher than the year before. Their small scores come from durability only.
- Collor I's drop partly reflects the 1990 asset freeze; the rubric does not judge the cost of the method, only the IPCA outcome.
- Collor II's "41 months" measures time until the Real, not time the plan actually worked; 1992 and 1993 inflation rose again.

## Assumptions

- Plano Real launch date = 1 July 1994 (the real currency enters circulation, per https://pt.wikipedia.org/wiki/Plano_Real). The URV phase began 27 February 1994 (per https://pt.wikipedia.org/wiki/Plano_Collor). Using 27 Feb 1994 would cut Collor II to 36 months (score 0.397) and change no rank. The Real's own score is unaffected because the rubric fixes it at 60 months.
- "Whole calendar months" = full months elapsed between the two dates (day-of-month aware).
- Collor II launch = 31 January 1991 (date of the provisional measure), as stated on https://pt.wikipedia.org/wiki/Plano_Collor.
- IPCA figures were cross-checked against the known IBGE series; portalbrasil.net reproduces the IBGE table. IBGE's own page returned HTTP 403 to automated fetching, so it is not cited directly.
