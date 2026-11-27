# Dossier: which Brazilian anti-inflation plans delivered?

**Method.** Scored per RUBRIC.md: annual IPCA (IBGE) of the year before (Y-1) and after (Y+1) each plan's launch year; score = 0.7 x clamp(1 - ipca_after/ipca_before, 0, 1) + 0.3 x min(months_lasted, 60)/60. IPCA annual values from StatBureau's IPCA table (https://www.statbureau.org/en/brazil/inflation-tables); launch dates from pt-Wikipedia's hyperinflation plan table (https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil).

| Plan | Launch | IPCA Y-1 | IPCA Y+1 | Months | Score |
|---|---|---|---|---|---|
| Real | 1994-07-01 | 2477.15% (1993) | 22.41% (1995) | 60 (cap) | **0.994** |
| Collor I | 1990-03-15 | 1972.91% (1989) | 472.70% (1991) | 10 | **0.582** |
| Collor II | 1991-01-31 | 1620.97% (1990) | 1119.10% (1992) | 42 | **0.427** |
| Bresser | 1987-06-12 | 79.66% (1986) | 980.21% (1988) | 19 | 0.095 |
| Cruzado | 1986-02-28 | 242.23% (1985) | 363.41% (1987) | 16 | 0.080 |
| Verao | 1989-01-15 | 980.21% (1988) | 1620.97% (1990) | 14 | 0.070 |

**Top 3 (best first): Real, Collor I, Collor II.**

**Reading.** Only the Real plan both cut inflation and held: 1993 IPCA of 2477.15% fell to 22.41% by 1995 and the plan was still in force at the 60-month cap. Collor I delivered the biggest one-year drop after the Cruzado-era peak (1972.91% to 472.70%) but lasted only 10 months until Collor II. Collor II kept inflation falling (1620.97% to 1119.10%) and lasted 42 months. The 1986-89 plans (Cruzado, Bresser, Verao) all ended with higher inflation than they started with, so their drop scores are zero and only durability counts.

**Assumptions.** (1) "Months lasted" = whole calendar months from launch to the next plan's launch, per RUBRIC.md; Real capped at 60. (2) Launch dates as listed in the pt-Wikipedia plan table: Cruzado 28/02/1986, Bresser 12/06/1987, Verao 15/01/1989, Collor I 15/03/1990, Collor II 31/01/1991, Real 01/07/1994. (3) IPCA is the IBGE annual calendar-year rate as tabulated by StatBureau; the BCB calculator was used as a cross-check for 1985 (342.25% incl. the Feb-1986 currency change) but StatBureau's clean annual series is the source of record.