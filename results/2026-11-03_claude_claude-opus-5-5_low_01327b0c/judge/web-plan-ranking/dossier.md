# Brazil anti-inflation plans: who delivered? (rubric in RUBRIC.md)

IPCA annual % source for all inflation figures: IBGE, https://www.ibge.gov.br/explica/inflacao.php (series IPCA, 1985-1995). Launch dates: Wikipedia plan pages listed per row.

| rank | plan | launch | IPCA Y-1 | IPCA Y+1 | months | score | sources |
|---|---|---|---|---|---|---|---|
| 1 | Real | 1994-07-01 | 2477.15 (1993) | 22.41 (1995) | 60 (cap) | 0.994 | IBGE above; https://pt.wikipedia.org/wiki/Plano_Real |
| 2 | Collor I | 1990-03-16 | 1972.91 (1989) | 472.70 (1991) | 10 | 0.582 | IBGE; https://pt.wikipedia.org/wiki/Plano_Collor |
| 3 | Collor II | 1991-01-31 | 1620.97 (1990) | 1119.10 (1992) | 41 | 0.422 | IBGE; https://pt.wikipedia.org/wiki/Plano_Collor_II |
| 4 | Bresser | 1987-06-12 | 79.66 (1986) | 980.21 (1988) | 19 | 0.095 | IBGE; https://pt.wikipedia.org/wiki/Plano_Bresser |
| 5 | Cruzado | 1986-02-28 | 242.23 (1985) | 363.41 (1987) | 15 | 0.075 | IBGE; https://pt.wikipedia.org/wiki/Plano_Cruzado |
| 6 | Verao | 1989-01-16 | 980.21 (1988) | 1620.97 (1990) | 14 | 0.070 | IBGE; https://pt.wikipedia.org/wiki/Plano_Ver%C3%A3o |

Score = 0.7*clamp(1-after/before,0,1) + 0.3*min(months,60)/60.

Assumptions: months = whole calendar months between launch dates; Verao dated 1989-01-16 (announced 15th, both give 14 months).

Caveats for the editor: Collor I/II rank high on the rubric because 1989-1990 were hyperinflation peaks, not because they held prices (Collor I froze savings; inflation rebounded within months). Only Real produced durable disinflation. Figures were not re-fetched live in this session; verify against the IBGE SIDRA table 1737 (https://sidra.ibge.gov.br/tabela/1737) before print.
