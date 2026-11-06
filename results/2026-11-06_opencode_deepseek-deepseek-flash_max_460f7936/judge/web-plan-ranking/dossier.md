# Brazil's anti-inflation plans: which ones delivered

**For:** policy desk editor  
**Question:** rank Brazil's six stabilization plans on the RUBRIC.md formula, using public data.

## Bottom line

The Real is the only plan that clearly delivered. It cuts annual IPCA from 2,477.15% in 1993 to 22.41% in 1995 (https://sidra.ibge.gov.br/tabela/1737) and earns the full 60-month durability cap, for a score of 0.994. Collor I (0.582) and Collor II (0.422) complete a weak podium: both lowered inflation from a hyperinflationary base, but neither stabilized prices. Cruzado, Bresser and Verao score near zero because the rubric compares year Y-1 with Y+1, and inflation was higher two years after each launch.

## Ranking

| # | Plan | Score |
|---|---|---|
| 1 | Real | 0.994 |
| 2 | Collor I | 0.582 |
| 3 | Collor II | 0.422 |
| 4 | Bresser | 0.095 |
| 5 | Cruzado | 0.075 |
| 6 | Verao | 0.070 |

Scores are derived from the formula in RUBRIC.md; inputs and URLs are below.

## Scored plans

**Real** - launched 1 July 1994 (https://pt.wikipedia.org/wiki/Plano_Real). IPCA 1993: 2,477.15% and 1995: 22.41% (https://sidra.ibge.gov.br/tabela/1737). Drop 0.9910; durability 60/60 (no next plan, rubric cap). Score 0.7 x 0.9910 + 0.3 x 1.000 = **0.994**.

**Collor I** - launched 16 March 1990 (https://pt.wikipedia.org/wiki/Plano_Collor). IPCA 1989: 1,972.91% and 1991: 472.70% (https://sidra.ibge.gov.br/tabela/1737). Drop 0.7604; lasted 10 whole months to Collor II (31 January 1991, https://pt.wikipedia.org/wiki/Plano_Collor); durability 10/60 = 0.1667. Score 0.7 x 0.7604 + 0.3 x 0.1667 = **0.582**.

**Collor II** - launched 31 January 1991 (https://pt.wikipedia.org/wiki/Plano_Collor). IPCA 1990: 1,620.97% and 1992: 1,119.10% (https://sidra.ibge.gov.br/tabela/1737). Drop 0.3096; lasted 41 whole months to the Real (1 July 1994, https://pt.wikipedia.org/wiki/Plano_Real); durability 41/60 = 0.6833. Score 0.7 x 0.3096 + 0.3 x 0.6833 = **0.422**.

**Bresser** - launched 12 June 1987 (https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil). IPCA 1986: 79.66% and 1988: 980.21% (https://sidra.ibge.gov.br/tabela/1737). Drop clamped to 0; lasted 19 whole months to Verao (15 January 1989, https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil); durability 19/60 = 0.3167. Score 0.3 x 0.3167 = **0.095**.

**Cruzado** - launched 28 February 1986 (https://pt.wikipedia.org/wiki/Plano_Cruzado). IPCA 1985: 242.23% and 1987: 363.41% (https://sidra.ibge.gov.br/tabela/1737). Drop clamped to 0; lasted 15 whole months to Bresser (12 June 1987, https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil); durability 15/60 = 0.2500. Score 0.3 x 0.2500 = **0.075**.

**Verao** - launched 15 January 1989 (https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil). IPCA 1988: 980.21% and 1990: 1,620.97% (https://sidra.ibge.gov.br/tabela/1737). Drop clamped to 0; lasted 14 whole months to Collor I (16 March 1990, https://pt.wikipedia.org/wiki/Plano_Collor); durability 14/60 = 0.2333. Score 0.3 x 0.2333 = **0.070**.

## What the ranking actually measures

The rubric's `ipca_before`/`ipca_after` window is Y-1 to Y+1, not the inflation rate at launch versus the rate at the plan's end. Three consequences an editor should flag:

1. **The window flatters the Real and punishes the 1980s plans.** Cruzado, Bresser and Verao all cut monthly inflation sharply at first, but each was followed by re-acceleration, so annual IPCA two years later was higher than before. Their zero drop scores are a statement about durability, not about whether the initial shock worked.
2. **Collor I's second place rests on a high 1989 base.** Its 1990 IPCA (1,620.97%, https://sidra.ibge.gov.br/tabela/1737) was still extreme; the fall to 472.70% in 1991 is real disinflation but not stabilization. The plan also froze roughly 80% of financial assets (https://pt.wikipedia.org/wiki/Plano_Collor), a cost the score ignores.
3. **The durability term is capped at 60 months.** The Real gets the maximum because the rubric assigns it 60 months by rule, not because it was measured against a successor. Any plan lasting over five years would tie on this term.

## Assumptions I made

- **Annual IPCA** is IBGE's calendar-year accumulated IPCA, SIDRA table 1737, variable 69 ("IPCA - variacao acumulada no ano"). All annual values in this dossier come from one query: https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/198512,198612,198712,198812,198912,199012,199112,199212,199312,199412,199512?formato=json
- **Launch dates** use the public announcement/decree date for each plan. For the Real I used 1 July 1994, the currency launch, although the program formally began with MP 434 on 27 February 1994 (https://pt.wikipedia.org/wiki/Plano_Real). This choice only affects Collor II's duration: dating the Real to 27 February 1994 gives Collor II 37 months and a score of 0.398, still third.
- **months_lasted** is whole calendar months, rounded down, from launch date to the next plan's launch date, per RUBRIC.md.
- **Verao** is the plan the rubric calls "Verao" (Portuguese: Verao/Verão, January 1989).
- **Scores** are rounded to three decimals; the ranking is unaffected by rounding.
- **Excluded from the score:** the confiscation of savings under Collor I, wage and price freezes under all plans, and subsequent recessions. RUBRIC.md scores inflation and duration only.

## Sources

- IBGE, IPCA annual series (SIDRA table 1737): https://sidra.ibge.gov.br/tabela/1737
- IPCA query used for every annual figure: https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/198512,198612,198712,198812,198912,199012,199112,199212,199312,199412,199512?formato=json
- Plano Cruzado: https://pt.wikipedia.org/wiki/Plano_Cruzado
- Bresser and Verao dates: https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil
- Plano Collor (Collor I and II dates): https://pt.wikipedia.org/wiki/Plano_Collor
- Plano Real: https://pt.wikipedia.org/wiki/Plano_Real
