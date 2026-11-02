# Brazil's anti-inflation plans: did they deliver?

Ranking per the house rubric (RUBRIC.md): score = 0.7 x inflation-drop + 0.3 x durability.
Inflation-drop compares the calendar-year IPCA before launch (Y-1) with the year after (Y+1);
durability is whole calendar months the plan survived until the next plan (Real: no successor, capped at 60).

## Top 3

1. **Real (1994) - score 0.99.** Annual IPCA fell from 2476.92% (1993) to 22.41% (1995)
   (https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json&dataInicial=01/01/1985&dataFinal=31/12/1995).
   Launched 1 July 1994 (https://pt.wikipedia.org/wiki/Plano_Real); no successor, full durability credit.
   The only plan that both crushed inflation and stayed crushed.
2. **Collor I (1990) - score 0.56.** IPCA 1764.92% (1989) to 472.26% (1991) (same BCB/IBGE series, URL above).
   Launched 16 March 1990 (https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil);
   lasted only 10 months before Collor II replaced it. The drop is real but inflation was still ~470% a year,
   and the plan's price controls were relaxed from July 1990.
3. **Collor II (1991) - score 0.41.** IPCA 1620.66% (1990) to 1154.39% (1992) (same URL).
   Launched 31 January 1991 (https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil);
   survived 41 months, but annual inflation stayed above 1000% throughout.

## Full table

| Plan | Launched | IPCA Y-1 (%) | IPCA Y+1 (%) | Months lasted | Score |
|---|---|---|---|---|---|
| Real | 1994-07-01 | 2476.92 (1993) | 22.41 (1995) | 60 (cap) | 0.99 |
| Collor I | 1990-03-16 | 1764.92 (1989) | 472.26 (1991) | 10 | 0.56 |
| Collor II | 1991-01-31 | 1620.66 (1990) | 1154.39 (1992) | 41 | 0.41 |
| Bresser | 1987-06-12 | 27.10 (1986) | 933.34 (1988) | 19 | 0.10 |
| Cruzado | 1986-02-28 | 235.65 (1985) | 228.61 (1987) | 15 | 0.08 |
| Verao | 1989-01-15 | 933.34 (1988) | 1620.66 (1990) | 14 | 0.07 |

IPCA figures: annual values compounded from IBGE monthly IPCA, Central Bank of Brazil SGS series 433
(https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json&dataInicial=01/01/1985&dataFinal=31/12/1995).
Launch dates: https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil,
https://pt.wikipedia.org/wiki/Plano_Cruzado (Cruzado), https://pt.wikipedia.org/wiki/Plano_Real (Real).

## What the numbers say

The freeze plans (Cruzado, Bresser, Verao) all score near zero: each ended with inflation higher a year later
than before it began, and none lasted two years. The Cruzado's own-year figure (27.10% in 1986) shows the freeze
worked for months, but 1987 rebounded to 228.61% - the rubric's Y+1 window captures exactly that collapse.
Collor I and Collor II earn partial credit for big base-effect drops but never exited hyperinflation.
Only the Real, which de-indexed the economy via the URV before issuing the currency rather than freezing prices,
delivered what it promised: single-digit-era inflation within a year, and it held.

## Method notes and assumptions

- Annual IPCA = product of the 12 monthly IBGE variations minus 1, from the BCB SGS 433 API (IBGE data);
  the computed years match IBGE's published annual figures (e.g. 1994: 927.27%, 1995: 22.41%).
- Months lasted = whole calendar months between launch dates (a month counts only when the day-of-month
  has passed), per RUBRIC.md; Real capped at 60 as the last plan.
- Real's launch is taken as 1 July 1994, the day the real replaced the cruzeiro real
  (https://pt.wikipedia.org/wiki/Plano_Real); the programme's URV stage began earlier (MP 434, 27 February 1994).
  This choice does not change Real's score (capped), and only slightly affects Collor II's durability.
- Verao is spelled as in the rubric table; plan names otherwise follow the rubric.