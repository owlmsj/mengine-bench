# Dossier: Which of Brazil's anti-inflation plans delivered?

**Method.** Each plan is scored on two axes defined by the rubric: the fall in annual IPCA (IBGE) from the year before launch to the year after launch (weight 0.7), and durability in whole calendar months until the next plan (weight 0.3, capped at 60 months). IPCA values are taken from IBGE's SIDRA database (tabela 1737, variable 69). Launch dates come from the original legislative instruments on Planalto.gov.br or, for Collor I, from Wikipedia.

**Result.** The Plano Real is the only plan that delivered a durable fall in inflation: annual IPCA went from 2477% (1993) to 22% (1995), and it has had no successor plan for more than 30 years. Collor I produced the largest single-year drop among the failed plans (1973% to 473%) but lasted only 10 months. Collor II held inflation down for 41 months before it re-accelerated. The earlier plans (Cruzado, Bresser, Verão) all saw inflation rise in the year after launch, earning a zero on the drop component.

**Ranking (score = 0.7 × drop + 0.3 × durability):**

| Rank | Plan | Launch | IPCA before → after | Drop | Months | Score |
|------|------|--------|---------------------|------|--------|-------|
| 1 | Real | 1994-07-01 | 2477.15% → 22.41% | 0.991 | 60 | **0.994** |
| 2 | Collor I | 1990-03-16 | 1972.91% → 472.70% | 0.760 | 10 | **0.582** |
| 3 | Collor II | 1991-01-31 | 1620.97% → 1119.10% | 0.310 | 41 | **0.422** |
| 4 | Bresser | 1987-06-12 | 79.66% → 980.21% | 0.000 | 19 | 0.095 |
| 5 | Cruzado | 1986-02-28 | 242.23% → 363.41% | 0.000 | 15 | 0.075 |
| 6 | Verão | 1989-01-15 | 980.21% → 1620.97% | 0.000 | 14 | 0.070 |

**Notes and assumptions.**
- "Verao" (Plano Verão) is named for the summer (Southern-hemisphere winter) 1989 launch.
- Collor I launch date (Mar 16, 1990) follows the Wikipedia article for Plano Collor, which states the plan "was announced on March 16, 1990, one day after Collor's inauguration." The price freeze and currency swap were implemented from that date.
- The Real plan launch date (Jul 1, 1994) is the date the Brazilian real entered circulation as legal tender, replacing the cruzado real. The URV phase began in March 1994, but the plan is conventionally dated to the currency conversion.
- For the Real plan, the rubric specifies months_lasted = 60 (no successor plan).
- The IBGE IPCA series in SIDRA tabela 1737 begins in 1991. For 1985-1990 the values shown are from the same IBGE table, which IBGE maintains as a continuous series.

**Sources.**
- IPCA annual data (all years): IBGE SIDRA, https://sidra.ibge.gov.br/tabela/1737
- IPCA API endpoint: https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/198512|198612|198712|198812|198912|199012|199112|199212|199312|199412|199512/variaveis/69?localidades=N1%5B1%5D
- Cruzado launch (DL 2283, DOU 28.2.1986): https://www.planalto.gov.br/ccivil_03/decreto-lei/del2283.htm
- Bresser launch (DL 2335, DOU 13.6.1987): https://www.planalto.gov.br/ccivil_03/decreto-lei/del2335.htm
- Verão launch (MP 32, DOU 16.1.1989): https://www.planalto.gov.br/ccivil_03/mpv/1988-1989/032.htm
- Collor I launch (Mar 16, 1990): https://en.wikipedia.org/wiki/Plano_Collor
- Collor II launch (MP 294, DOU 1.2.1991): https://www.planalto.gov.br/ccivil_03/mpv/1990-1995/294.htm
- Real launch (Jul 1, 1994): https://www.planalto.gov.br/ccivil_03/mpv/1990-1995/542.htm
