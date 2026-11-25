# Dossier: Brazilian anti-inflation plans, scored by the rubric

Method. Per RUBRIC.md: annual IPCA (IBGE, % p.a.). For a plan launched in year Y: ipca_before = Y-1, ipca_after = Y+1. score_drop = clamp(1 - ipca_after/ipca_before, 0, 1); months_lasted = whole calendar months to the next plan's launch (Real: 60); durability = min(months,60)/60; score = 0.7*drop + 0.3*durability.

IPCA values (annual, Dec-to-Dec, %): 1985 242.23; 1986 79.66; 1987 363.41; 1988 980.21; 1989 1,972.91; 1990 1,620.97; 1991 472.70; 1992 1,119.10; 1993 2,477.15; 1994 916.46; 1995 22.41. Source: Ipeadata PRECOS_IPCAG series (IBGE data): https://www.ipeadata.gov.br/

Launch dates: Cruzado Feb 28 1986; Bresser Jun 12 1987; Verao Jan 15 1989; Collor I Mar 15 1990; Collor II Jan 31 1991; Real Jul 1 1994. Sources: https://senado.leg.br/ ; https://www.bcb.gov.br/

| Plan | Launch | Before | After | Months | Drop | Durability | Score |
|---|---|---|---|---|---|---|---|
| Cruzado | 1986-02-28 | 242.23 (1985) | 363.41 (1987) | 15 | 0.000 | 0.25 | 0.075 |
| Bresser | 1987-06-12 | 79.66 (1986) | 980.21 (1988) | 19 | 0.000 | 0.317 | 0.095 |
| Verao | 1989-01-15 | 980.21 (1988) | 1,620.97 (1990) | 14 | 0.000 | 0.233 | 0.070 |
| Collor I | 1990-03-15 | 1,972.91 (1989) | 472.70 (1991) | 10 | 0.760 | 0.167 | 0.582 |
| Collor II | 1991-01-31 | 1,620.97 (1990) | 1,119.10 (1992) | 41 | 0.310 | 0.683 | 0.422 |
| Real | 1994-07-01 | 2,477.15 (1993) | 22.41 (1995) | 60 | 0.991 | 1.000 | 0.994 |

Top 3 (best first): Real, Collor I, Collor II.

Finding. None of the four pre-Real plans improved beyond prediction by the rubric: in every case inflation after the plan (Y+1) exceeded before, so score_drop clamped to 0 for Cruzado, Bresser and Verao. Collor I delivered a 76.0% relative drop in the following year but only lasted 10 months. Collor II cut inflation 31.0% and lasted 41 months. Real is the standout: 2,477.15% to 22.41%, a 99.1% drop, with a 60-month durability cap and score 0.994.

Assumptions: launch dates use the conventional effective-date (Cruzado Feb 1986, Bresser Jun 1987, Verao Jan 1989, Collor I Mar 1990, Collor II Jan 1991, Real Jul 1994 — Real counted from currency launch, per the rubric convention that months are measured to the next plan launch). Real's 60-month cap per the rubric. Weather: Bresser listed June 12 1987 per Decree-Law 2,335; sources acknowledge alternative announcement dates.
