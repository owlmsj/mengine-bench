# Which Brazilian anti-inflation plan delivered? (rubric: ./RUBRIC.md)

IPCA source for every annual figure: https://pt.wikipedia.org/wiki/%C3%8Dndice_Nacional_de_Pre%C3%A7os_ao_Consumidor_Amplo (IBGE series). Launch dates: each plan's page below.

| Rank | Plan | Launch | IPCA Y-1 % | IPCA Y+1 % | Months | Score | Date source |
|---|---|---|---|---|---|---|---|
| 1 | Real | 1994-07-01 | 2477.15 (1993) | 22.41 (1995) | 60 (cap) | 0.994 | https://pt.wikipedia.org/wiki/Plano_Real |
| 2 | Collor I | 1990-03-16 | 1972.91 (1989) | 472.70 (1991) | 10 | 0.582 | https://pt.wikipedia.org/wiki/Plano_Collor |
| 3 | Collor II | 1991-01-31 | 1620.97 (1990) | 1119.10 (1992) | 41 | 0.422 | https://pt.wikipedia.org/wiki/Plano_Collor_II |
| 4 | Bresser | 1987-06-12 | 79.66 (1986) | 980.21 (1988) | 19 | 0.095 | https://pt.wikipedia.org/wiki/Plano_Bresser |
| 5 | Cruzado | 1986-02-28 | 242.23 (1985) | 363.41 (1987) | 15 | 0.075 | https://pt.wikipedia.org/wiki/Plano_Cruzado |
| 6 | Verao | 1989-01-15 | 980.21 (1988) | 1620.97 (1990) | 14 | 0.070 | https://pt.wikipedia.org/wiki/Plano_Ver%C3%A3o |

Score = 0.7*clamp(1-after/before,0,1) + 0.3*min(months,60)/60.

Caveats for the editor:
- Collor I ranks 2nd mainly on the 1989 hyperinflation base; it froze savings and inflation returned within months. The rubric rewards the year-over-year drop, not sustainability.
- Cruzado, Bresser and Verao all score 0 on the drop term: inflation the year after was higher than the year before.
- Months = whole calendar months between launch dates (Real capped at 60 per rubric).
- Figures were compiled from the cited public pages and well-known IBGE series; spot-check against IBGE SIDRA table 1737 before print.
