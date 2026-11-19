# Dossier: which Brazilian anti-inflation plan delivered?

**For:** newsletter editor · **Date:** 19 Nov 2026 · **Method:** RUBRIC.md applied to IBGE IPCA annual rates

## Bottom line

Only the Real cut inflation and held it. Measured by the rubric (70% fall in annual IPCA two years on, 30% duration), the ranking is:

| # | Plan | Score | IPCA before | IPCA year+1 | Months |
|---|---|---|---|---|---|
| 1 | Real (1994) | 0.994 | 2,477.15% (1993) | 22.41% (1995) | 60 |
| 2 | Collor I (1990) | 0.582 | 1,972.91% (1989) | 472.70% (1991) | 10 |
| 3 | Collor II (1991) | 0.422 | 1,620.97% (1990) | 1,119.10% (1992) | 41 |
| 4 | Bresser (1987) | 0.095 | 79.66% (1986) | 980.21% (1988) | 19 |
| 5 | Cruzado (1986) | 0.075 | 242.23% (1985) | 363.41% (1987) | 15 |
| 6 | Verão (1989) | 0.070 | 980.21% (1988) | 1,620.97% (1990) | 14 |

Scores: 0.7 × clamp(1 − IPCA_after/IPCA_before, 0, 1) + 0.3 × min(months, 60)/60.

## What the numbers say

**Real — the only pass.** Launched 1 July 1994, it took annual IPCA from 2,477.15% in 1993 to 22.41% in 1995, a 99.1% fall, and never had a successor plan, so the rubric grants full durability. Score 0.9937. The caveat for the piece: the drop is measured against hyperinflation, so a large percentage fall is arithmetically easy; the achievement is that it stayed down.

**Collor I — a big fall, a short life.** The March 1990 freeze and confiscation cut 1989's 1,972.91% to 472.70% in 1991 (drop 0.760), but the plan was replaced by Collor II after 10 months. Score 0.5823. It ranks second on the strength of the drop alone; durability contributes only 0.05 of the score.

**Collor II — long, but inflation re-accelerated.** It lasted 41 months (to the Real), which is why it beats Bresser, Cruzado and Verão despite a weak drop: 1,620.97% (1990) to 1,119.10% (1992), drop 0.310. Score 0.4217.

**Cruzado, Bresser, Verão — negative on the rubric.** In all three cases annual IPCA two years later was higher than the year before launch, so score_drop clamps to 0 and the score is purely durability (0.07–0.095). The Cruzado's freeze did crush monthly inflation in 1986, but the rubric's year-on-year window captures the rebound, which is the point of the exercise.

## Assumptions (state these in the piece)

1. **IPCA annual rate** = December-to-December change in the IBGE IPCA number-index (base Dec/1993 = 100), from IBGE's SIDRA table 1737 API. This reproduces the published annual series (e.g. 1989 = 1,972.91%, 1994 = 916.46%).
2. **Launch date** = the date the plan was announced and took effect, per the linked Wikipedia articles. For the Real, 1 July 1994 is the currency launch; the URV phase from 27 Feb 1994 is treated as pre-launch.
3. **months_lasted** counts whole calendar months between launch dates, as the rubric specifies; the Real uses the fixed 60.
4. Collor I's *after* year is 1991, which overlaps Collor II's launch (31 Jan 1991); the rubric's Y+1 rule is applied mechanically, so Collor I is partly credited with its successor's year.

## Sources

- IPCA series (table 1737, variable 2266): https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/all/variaveis/2266?localidades=N1[all] · table page: https://sidra.ibge.gov.br/tabela/1737
- Cruzado, 28 Feb 1986: https://pt.wikipedia.org/wiki/Plano_Cruzado
- Bresser, 12 Jun 1987: https://pt.wikipedia.org/wiki/Plano_Bresser
- Verão, 15 Jan 1989: https://pt.wikipedia.org/wiki/Plano_Ver%C3%A3o
- Collor I, 16 Mar 1990 and Collor II, 31 Jan 1991: https://pt.wikipedia.org/wiki/Plano_Collor
- Real, 1 Jul 1994: https://pt.wikipedia.org/wiki/Plano_Real
