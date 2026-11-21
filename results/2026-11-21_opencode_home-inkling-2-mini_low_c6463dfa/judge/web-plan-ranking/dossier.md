# Dossier: Did Brazil's anti-inflation plans deliver?

Scoring rubric: annual IPCA (IBGE), inflation in year Y-1 (before) and year Y+1 (after); `score_drop = clamp(1 - after/before, 0, 1)`; `months_lasted` = whole calendar months to the next plan (Real: 60); `score = 0.7 * drop + 0.3 * min(months,60)/60`.

Annual IPCA (%), sourced from the Economy of Brazil table on Wikipedia (see sources): 1985 226.0 | 1986 147.1 | 1987 228.3 | 1988 629.1 | 1989 1430.7 | 1990 2947.7 | 1991 432.8 | 1992 952.0 | 1993 1927.4 | 1995 66.0. Launch dates from Wikipedia's timeline/Plano Collor/Real Plan articles.

| Plan | Launch | Before (Y-1) | After (Y+1) | Months | Drop | Score |
|---|---|---|---|---|---|---|
| Cruzado | 1986-02-28 | 226.0 (1985) | 228.3 (1987) | 15 | 0.00 | 0.075 |
| Bresser | 1987-06-12 | 147.1 (1986) | 629.1 (1988) | 19 | 0.00 | 0.095 |
| Verao | 1989-01-15 | 629.1 (1988) | 2947.7 (1990) | 14 | 0.00 | 0.070 |
| Collor I | 1990-03-16 | 1430.7 (1989) | 432.8 (1991) | 9 | 0.70 | 0.533 |
| Collor II | 1991-01-15 | 2947.7 (1990) | 952.0 (1992) | 41 | 0.68 | 0.679 |
| Real | 1994-07-01 | 1927.4 (1993) | 66.0 (1995) | 60 | 0.97 | 0.976 |

Top 3: **Real** (0.976) > **Collor II** (0.679) > **Collor I** (0.533).

Assumptions: "Collor II" treated as the second Collor plan in January 1991 (Wikipedia: "The second Collor Plan took place in January 1991"). Annual IPCA figures are taken as the values reported in the Wikipedia "Economy of Brazil" indicator table (the historical series is not IPCA-specific to 1985, but the table groups them as inflation; flagged as a caveat — IBGE's exact IPCA series should be re-pulled before publication). Months counted only when the next plan's launch date exists; Real uses the rubric's fallback of 60.

Bottom line: none of the 1980s plans delivered; the two Collor plans produced real post-launch declines but collapsed; only Real decisively delivered on inflation, and it is the clear leader.

Sources: timeline and plan dates — https://en.wikipedia.org/wiki/Timeline_of_Brazilian_economic_stabilization_plans ; Collor I/II/Real dates — https://en.wikipedia.org/wiki/Plano_Collor , https://en.wikipedia.org/wiki/Real_Plan ; annual inflation table — https://en.wikipedia.org/wiki/Economy_of_Brazil .
