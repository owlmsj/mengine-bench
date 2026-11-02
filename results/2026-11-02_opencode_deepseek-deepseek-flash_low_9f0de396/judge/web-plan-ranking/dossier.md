# Dossier: which Brazilian anti-inflation plan delivered

**To:** Editor, policy newsletter · **Date:** 2 Nov 2026 · **Basis:** RUBRIC.md (0.7 × inflation drop + 0.3 × durability)

## Bottom line

Ranked by the rubric, the **Real** wins by a wide margin, **Collor I** is a distant second and **Collor II** third. Every plan before 1990 scores near zero, not because it did nothing, but because the rubric compares the launch year with the *following* year, when inflation had already rebounded.

| # | Plan | Launch | IPCA Y-1 (%) | IPCA Y+1 (%) | Drop score | Months | Durability | **Score** |
|---|---|---|---|---|---|---|---|---|
| 1 | Real | 1994-07-01 | [2477.15](https://sidra.ibge.gov.br/tabela/1737) | [22.41](https://sidra.ibge.gov.br/tabela/1737) | 0.991 | 60 (fixed) | 1.000 | **0.994** |
| 2 | Collor I | 1990-03-15 | [1972.91](https://sidra.ibge.gov.br/tabela/1737) | [472.70](https://sidra.ibge.gov.br/tabela/1737) | 0.760 | 10 | 0.167 | **0.582** |
| 3 | Collor II | 1991-01-31 | [1620.97](https://sidra.ibge.gov.br/tabela/1737) | [1119.10](https://sidra.ibge.gov.br/tabela/1737) | 0.310 | 41 | 0.683 | **0.422** |
| 4 | Bresser | 1987-06-12 | [79.66](https://sidra.ibge.gov.br/tabela/1737) | [980.21](https://sidra.ibge.gov.br/tabela/1737) | 0.000 | 19 | 0.317 | **0.095** |
| 5 | Cruzado | 1986-02-28 | [242.23](https://sidra.ibge.gov.br/tabela/1737) | [363.41](https://sidra.ibge.gov.br/tabela/1737) | 0.000 | 15 | 0.250 | **0.075** |
| 6 | Verão | 1989-01-15 | [980.21](https://sidra.ibge.gov.br/tabela/1737) | [1620.97](https://sidra.ibge.gov.br/tabela/1737) | 0.000 | 14 | 0.233 | **0.070** |

The IPCA figures are IBGE's annual accumulated variation (SIDRA table 1737, variable 69), pulled for December 1985–1995 from the [IBGE API endpoint](https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/198512%7C198612%7C198712%7C198812%7C198912%7C199012%7C199112%7C199212%7C199312%7C199412%7C199512/variaveis/69?localidades=N1[all]). Launch dates come from the plan decrees and the historical record: [Cruzado, 28 Feb 1986](https://pt.wikipedia.org/wiki/Plano_Cruzado) ([Decreto-Lei 2.283](http://www.planalto.gov.br/ccivil_03/decreto-lei/Del2283.htm)); [Bresser, 12 Jun 1987](https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil) ([Decreto-Lei 2.335](https://www2.camara.leg.br/legin/fed/declei/1980-1987/decreto-lei-2335-12-junho-1987-366920-publicacaooriginal-1-pe.html)); [Verão, 15 Jan 1989](https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil) ([MP 32/1989](http://www.planalto.gov.br/ccivil_03/MPV/1988-1989/032impressao.htm)); [Collor I, 15 Mar 1990](https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil) ([MP 168/1990](http://www.planalto.gov.br/ccivil_03/MPV/1990-1995/168.htm)); [Collor II, 31 Jan 1991](https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil); [Real, 1 Jul 1994](https://pt.wikipedia.org/wiki/Plano_Real).

## What the numbers actually say

- **Real (0.994).** Inflation fell from 2,477.15% in 1993 to 22.41% in 1995 — the only plan the rubric can score as a genuine drop — and it banks the full 60-month durability credit. The 1994 launch year itself ran at 916.46% ([IBGE](https://sidra.ibge.gov.br/tabela/1737)), so the victory is visible only against the following year, exactly as the rubric measures it.
- **Collor I (0.582).** The confiscation-era plan gets credit from the 1991 base effect: 472.70% against 1,972.91% in 1989. It lasted 10 months, the shortest of the six, which is why it cannot approach the Real. Its own year was still 1,620.97%.
- **Collor II (0.422).** Modest drop (1992: 1,119.10%) but the second-longest run, 41 months to the Real, carries a third of its score.
- **Cruzado, Bresser, Verão (0.07–0.10).** All three show a *higher* IPCA in Y+1 than in Y-1, so the drop term clamps to zero and only durability survives. Cruzado is the sharpest example: it cut 1986 inflation to 79.66% from 242.23%, but 1987 came in at 363.41%, so the rubric records no gain.

## Assumptions (stated, because the brief leaves them open)

1. **Launch date** = the date the plan took effect / its decree, not the date of the preceding announcement. Collor I uses 15 Mar 1990 (plan in force); the televised address was 16 Mar.
2. **Whole calendar months** between dates, ignoring the day fraction: e.g. Cruzado (28 Feb 1986) to Bresser (12 Jun 1987) = 15 complete months, since 12 Jun is 16 days short of the 28th.
3. **Annual IPCA** = IBGE's December "variação acumulada no ano", the official calendar-year figure, not a 12-month rolling rate. The values differ slightly from older published series (1985 is 242.23%, not the often-quoted 235%).
4. **Real durability** = 60 months, per the rubric's explicit rule; no successor plan exists.
5. **Drop is clamped** at 0 when Y+1 inflation exceeds Y-1, which is why three plans lose the 70% term entirely.

## Caveat for the editor

The rubric tests *the year after the launch year*, not the plan's own year, so it systematically rewards plans whose successor year happened to be calmer (Collor I benefits from 1991) and punishes plans that were followed by relapse (Cruzado). If the newsletter wants "did the plan deliver while it was in force," the ranking would look different — Cruzado's 1986 record is the obvious case. This dossier reports the rubric's ranking, and flags that distinction rather than hiding it.

All figures recomputed from the IBGE series above; scores rounded to three decimals.
