# Dossier: Which Brazilian anti-inflation plan delivered?

For the editor. Ranking built strictly from the rubric in RUBRIC.md (score =
0.7 x inflation-drop + 0.3 x durability, both 0-1). Every number below is
traceable to a public URL.

## Data and method

- Inflation = annual IPCA (IBGE), calendar year, % . Taken from the IBGE
  monthly IPCA series (BCB SGS series 433) and compounded per calendar year:
  https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv&dataInicial=01/01/1985&dataFinal=31/12/1995
  Cross-checked against IBGE SIDRA table 1737 (annual accumulated, December):
  https://sidra.ibge.gov.br/tabela/1737 (agrees within rounding: 1985 242.23,
  1986 79.66, 1987 363.41, 1988 980.21, 1989 1972.91, 1990 1620.97,
  1991 472.70, 1992 1119.10, 1993 2477.15, 1994 916.46, 1995 22.41).
- Launch dates from the official legal acts and the Wikipedia plan chronology
  (https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil):
  Cruzado 28/02/1986 (DL 2.283, http://www.planalto.gov.br/ccivil_03/decreto-lei/Del2283.htm),
  Bresser 12/06/1987 (DL 2.335, https://www2.camara.leg.br/legin/fed/declei/1980-1987/decreto-lei-2335-12-junho-1987-366920-publicacaooriginal-1-pe.html),
  Verao 15/01/1989 (MP 32, http://www.planalto.gov.br/ccivil_03/MPV/1988-1989/032impressao.htm),
  Collor I 16/03/1990 (MP 168, http://www.planalto.gov.br/ccivil_03/MPV/1990-1995/168.htm),
  Collor II 31/01/1991 (MP 294, converted as Lei 8.177, http://www.planalto.gov.br/ccivil_03/leis/L8177.htm),
  Real 01/07/1994 (MP 542, http://www.planalto.gov.br/ccivil_03/MPV/1990-1995/542.htm).
- months_lasted = whole calendar months to the next plan's launch; Real = 60 (no next plan).

## Scores (full table)

| Rank | Plan | Launched | IPCA year before | IPCA year after | Drop score | Months | Durability | Score |
|---|---|---|---|---|---|---|---|---|
| 1 | Real | 1994-07-01 | 2477.15 (1993) | 22.41 (1995) | 0.991 | 60 | 1.00 | **0.994** |
| 2 | Collor I | 1990-03-16 | 1972.91 (1989) | 472.69 (1991) | 0.760 | 10 | 0.17 | **0.582** |
| 3 | Collor II | 1991-01-31 | 1620.97 (1990) | 1119.09 (1992) | 0.310 | 41 | 0.68 | **0.422** |
| 4 | Bresser | 1987-06-12 | 79.66 (1986) | 980.22 (1988) | 0.000 | 19 | 0.32 | 0.095 |
| 5 | Cruzado | 1986-02-28 | 242.25 (1985) | 363.41 (1987) | 0.000 | 15 | 0.25 | 0.075 |
| 6 | Verao | 1989-01-15 | 980.22 (1988) | 1620.97 (1990) | 0.000 | 14 | 0.23 | 0.070 |

## Top 3, one line each

1. **Real (0.994)** - the only plan that killed inflation and stayed dead:
   2477% (1993) to 22.4% (1995), still running.
2. **Collor I (0.582)** - a real one-year drop (1973% to 473%) bought with the
   savings confiscation, but it collapsed in 10 months and inflation roared back.
3. **Collor II (0.422)** - a milder drop (1621% to 1119%) that at least lasted
   almost 3.5 years until the Real replaced it.

The freeze plans (Cruzado, Bresser, Verao) score near zero on the rubric: in
every case the calendar year after launch was more inflationary than the year
before, and none lasted two years.

## Assumptions stated

- "Annual IPCA" = Dec-over-Dec calendar-year variation of the current official
  IBGE series (legacy pre-2012 tables show slightly different values, e.g.
  1990 = 1120.66; the ranking and top 3 are unchanged under either series).
- Collor I launch = 16/03/1990 (announced and effective date; the MP is dated
  15/03/1990; month count is 10 either way).
- Real launch = 01/07/1994 (currency day), per the rubric's "Real (1994)" and
  the Wikipedia chronology.
- months_lasted counted as whole calendar months (a month counts only when its
  day-of-month has passed).