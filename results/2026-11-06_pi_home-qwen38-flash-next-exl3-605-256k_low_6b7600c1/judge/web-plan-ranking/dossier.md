# Brazil's anti-inflation plans, scored on the rubric

One page for the editor. Inflation = annual IPCA (IBGE), calendar-year accumulated
variation as published for December of each year, read straight from the IBGE SIDRA
API (table 1737, variable 69):
https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/198512,198612,198712,198812,198912,199012,199112,199212,199312,199412,199512
(portal page: https://sidra.ibge.gov.br/tabela/1737)

## Ranking (score = 0.7 * drop + 0.3 * durability)

| # | Plan | Launch | IPCA year before | IPCA year after | drop | Months lasted | Durability | Score |
|---|------|--------|------------------|-----------------|------|---------------|------------|-------|
| 1 | Real | 1994-02-27 | 2477.15 (1993) | 22.41 (1995) | 0.991 | 60 (no next plan, rubric cap) | 1.000 | **0.994** |
| 2 | Collor I | 1990-03-16 | 1972.91 (1989) | 472.70 (1991) | 0.760 | 10 | 0.167 | **0.582** |
| 3 | Collor II | 1991-01-31 | 1620.97 (1990) | 1119.10 (1992) | 0.310 | 36 | 0.600 | **0.397** |
| 4 | Bresser | 1987-06-12 | 79.66 (1986) | 980.21 (1988) | 0.000 | 19 | 0.317 | 0.095 |
| 5 | Cruzado | 1986-02-28 | 242.23 (1985) | 363.41 (1987) | 0.000 | 15 | 0.250 | 0.075 |
| 6 | Verao | 1989-01-15 | 980.21 (1988) | 1620.97 (1990) | 0.000 | 14 | 0.233 | 0.070 |

Top 3: Real, Collor I, Collor II.

## The story in one paragraph

Only two plans cut inflation by the year after they launched, and only one kept it cut.
Real took annual IPCA from 2477.15% (1993) to 22.41% (1995), a 99% drop, and never had to
be replaced, so it scores near the ceiling. Collor I produced the second-biggest drop
(1972.91% in 1989 to 472.70% in 1991) but died in 10 months, and the freeze-style
liberalisation rebounded: IPCA was back to 1119.10% in 1992. Collor II is third only
because it lasted 36 months; its own drop was modest (1620.97% to 1119.10%) and it ended
inflation nowhere. Cruzado, Bresser and Verao score almost zero on impact: in every case
the calendar year after the plan was *more* inflationary than the year before, so the drop
term clamps to 0 and the score is pure durability. Cruzado's 15 months and Verao's 14 are
the shortest lives on the list.

## Sources for every number

Annual IPCA (all years in the table): IBGE SIDRA API call above, plus
https://sidra.ibge.gov.br/tabela/1737

Launch dates (legal acts published in the Diario Oficial da Uniao, Planalto):
- Cruzado, Decreto-Lei no 2.283 (1986-02-27/28): http://www.planalto.gov.br/ccivil_03/decreto-lei/1980-1988/del2283.htm
- Bresser, Decreto-Lei no 2.335 (1987-06-12): http://www.planalto.gov.br/ccivil_03/decreto-lei/1980-1988/del2335.htm
- Verao, MP no 32 (1989-01-15): http://www.planalto.gov.br/ccivil_03/mpv/1988-1989/032.htm
- Collor I (Plano Brasil Novo), MP no 168 (1990-03-16): http://www.planalto.gov.br/ccivil_03/mpv/1990-1995/168.htm
- Collor II, MP no 294 (1991-01-31): http://www.planalto.gov.br/ccivil_03/mpv/1990-1995/294.htm
- Real, MP no 434 (1994-02-27, URV phase): http://www.planalto.gov.br/ccivil_03/mpv/1990-1995/434.htm
  (currency phase, MP no 542, 1994-06-30: http://www.planalto.gov.br/ccivil_03/mpv/1990-1995/542.htm)

## Assumptions (state these if the piece is challenged)

1. IPCA = IBGE's own published "variacao acumulada no ano" for December, no re-basing or
   re-compounding. Consequence worth flagging: SIDRA's official 1986 figure is 79.66%,
   depressed by the Cruzado price freeze, which is why Bresser's "before" year looks low
   and its drop clamps to 0.
2. Launch date = the date the plan's founding act was signed/published. Real is dated
   1994-02-27 (URV / plan start, MP 434). Sensitivity: using the currency launch of
   1994-07-01 instead gives Collor II 41 months, durability 0.683 and score 0.422.
   Ranking unchanged.
3. months_lasted = whole calendar months between launch dates (anniversary rule, month-end
   clamped); Real uses the rubric's fixed 60.
4. The rubric is calendar-year based, so a plan launched mid-year is judged on a year that
   was partly already over. That is the main weakness of the ranking: it under-credits
   Cruzado's first months (a genuine inflation collapse under the freeze) and over-credits
   Collor II's longevity. Say "delivered" here means "lower IPCA in the following calendar
   year, and survived".