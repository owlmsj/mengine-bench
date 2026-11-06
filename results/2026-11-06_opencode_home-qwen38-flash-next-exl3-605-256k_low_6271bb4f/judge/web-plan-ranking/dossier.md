# Dossier: which Brazilian anti-inflation plan delivered?

For the editor. Scores follow the house rubric (RUBRIC.md): 70% weight on the
drop in annual IPCA from the year before to the year after launch, 30% on how
many months the plan survived until the next one (capped at 60). IPCA figures
are the official IBGE calendar-year series (table 1737, "IPCA - Variação
acumulada em 12 meses", December).

## Ranking

| # | Plan | Launched | IPCA year before (%) | IPCA year after (%) | Months until next plan | Score |
|---|------|----------|---------------------|--------------------|-----------------------|-------|
| 1 | Real | 1994-07-01 | 2477.15 (1993) | 22.41 (1995) | 60 (no successor) | 0.994 |
| 2 | Collor I | 1990-03-16 | 1972.91 (1989) | 472.70 (1991) | 10 | 0.582 |
| 3 | Collor II | 1991-01-31 | 1620.97 (1990) | 1119.10 (1992) | 41 | 0.422 |
| 4 | Bresser | 1987-06-12 | 79.66 (1986) | 980.21 (1988) | 19 | 0.095 |
| 5 | Cruzado | 1986-02-28 | 242.23 (1985) | 363.41 (1987) | 15 | 0.075 |
| 6 | Verao | 1989-01-15 | 980.21 (1988) | 1620.97 (1990) | 14 | 0.070 |

## The story in one paragraph

Only the Real Plan actually delivered: annual inflation fell from 2477.15% in
1993 to 22.41% in 1995 and stayed low
(https://en.wikipedia.org/wiki/Hyperinflation_in_Brazil).
Collor I (1990) scored the only other real drop, 1972.91% in 1989 to 472.70%
in 1991, but the freeze collapsed within months and inflation was back to 20%
a month by January 1991 (https://en.wikipedia.org/wiki/Plano_Collor).
Collor II bought time rather than results: inflation was still above 1000%
the year after it launched, yet the plan window lasted 41 months, which lifts
its durability score. Cruzado, Bresser and Verao all ended with annual
inflation higher than before they started; on this rubric they score on
durability only. Note the trap in the numbers: 1986, the Cruzado freeze year,
shows a low 79.66%, which makes Bresser's "before" year look flattering and
its failure look worse; the freeze years flatter the plan that follows.

## Sources

- Annual IPCA, official IBGE aggregated series (table 1737, variable 2265,
  12-month variation at December of each year):
  https://sidra.ibge.gov.br/tabela/1737 and the API call that returned every
  figure used here:
  https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/198512,198612,198712,198812,198912,199012,199112,199212,199312,199412,199512/variaveis/2265?localidades=N1%5Ball%5D
  (returned 1985 242.23, 1986 79.66, 1987 363.41, 1988 980.21, 1989 1972.91,
  1990 1620.97, 1991 472.70, 1992 1119.10, 1993 2477.15, 1994 916.46,
  1995 22.41).
- Launch dates (Cruzado 1986-02-28, Bresser 1987-06-12, Verao 1989-01-15,
  Collor I 1990-03-16, Real 1994-07-01):
  https://en.wikipedia.org/wiki/Hyperinflation_in_Brazil
- Collor I announced 16 March 1990; Collor II "January 1991" (MP 294 of
  1991-01-31): https://en.wikipedia.org/wiki/Plano_Collor

## Assumptions (state these if challenged)

1. Collor II is dated 1991-01-31 (Medida Provisória nº 294, later Lei
   8.177). English Wikipedia only says "January 1991"; any date in January
   1991 gives the same 41-month figure used here, so the score is insensitive
   to this choice.
2. Real has no successor plan, so months_lasted = 60 per the rubric.
3. IPCA figures are the current official IBGE series (SIDRA table 1737).
   Older print sources show slightly different revisions (e.g. 1989 1764.98);
   we use the official API values, which are what IBGE publishes today.
4. Months_lasted counts whole calendar months between launch dates
   (e.g. Cruzado 1986-02-28 to Bresser 1987-06-12 = 15).