# Which Brazilian anti-inflation plan delivered? A scoreable ranking

**To:** Editor, policy desk
**From:** Research desk
**Date:** 6 November 2026

## The short answer

Ranked by the rubric (70% fall in annual inflation from the year before to the year after, 30% duration):

1. **Real (1994)** — score 0.994
2. **Collor I (1990)** — score 0.582
3. **Collor II (1991)** — score 0.422

The remaining three — Bresser (0.090), Cruzado (0.075) and Verao (0.070) — all fail the inflation test outright: annual IPCA was higher two years after each launch than in the year before it.

## How the score works

For a plan launched in year Y, `ipca_before` is calendar-year IPCA in Y-1 and `ipca_after` is IPCA in Y+1. `score = 0.7 * clamp(1 - after/before, 0, 1) + 0.3 * min(months_lasted, 60)/60`. Annual IPCA is read from IBGE's monthly IPCA number index (base Dec 1993 = 100) as the December-over-December change.[IBGE] Launch dates and the next plan's launch date come from the published chronology.[TL]

| Plan | Launched | IPCA Y-1 (%) | IPCA Y+1 (%) | Months | Score |
|---|---|---|---|---|---|
| Real | 1994-07-01[TL] | 2477.15 (1993)[IBGE] | 22.41 (1995)[IBGE] | 60[rule] | **0.9937** |
| Collor I | 1990-03-16[COLLOR] | 1972.91 (1989)[IBGE] | 472.70 (1991)[IBGE] | 10[COLLOR] | **0.5823** |
| Collor II | 1991-01-31[COLLOR] | 1620.97 (1990)[IBGE] | 1119.10 (1992)[IBGE] | 41[TL] | **0.4217** |
| Bresser | 1987-06-12[TL] | 79.66 (1986)[IBGE] | 980.21 (1988)[IBGE] | 18[TL] | 0.0900 |
| Cruzado | 1986-02-28[TL] | 242.23 (1985)[IBGE] | 363.41 (1987)[IBGE] | 15[TL] | 0.0750 |
| Verao | 1989-01-15[TL] | 980.21 (1988)[IBGE] | 1620.97 (1990)[IBGE] | 14[TL] | 0.0700 |

## What the ranking means

**The Real is in a class of its own.** Annual IPCA fell from 2477.15% in 1993[IBGE] to 22.41% in 1995[IBGE], a 99.1% drop, and the plan had no successor inside the 60-month window: the rubric credits it with the full 60 months and therefore the maximum durability component (1.0). Its 0.9937 is close to the scale ceiling; no other plan comes within 0.41 of it.

**Collor I is the best of the failures, and that is the story.** It froze roughly 80% of financial assets and cut monthly inflation sharply, but annual IPCA was still 472.70% in 1991[IBGE], against 1972.91% in 1989[IBGE]. The 76% fall earns most of its score; its short life (10 months to Collor II)[COLLOR] costs it the durability component (0.167). It ranks second on the strength of the drop alone.

**Collor II is third only because of duration.** Its inflation record is weak: IPCA fell from 1620.97% in 1990[IBGE] to 1119.10% in 1992[IBGE], a 31% drop, but from a base distorted by Collor I's confiscation and recession. What lifts it above Bresser and Cruzado is that it was not replaced until the Real on 1 July 1994, 41 whole months later[TL], giving it 0.683 of the durability component. A plan that "lasted" mainly because the next plan took three and a half years to arrive still scores 0.4217.

**The three 1980s shocks score near zero.** Cruzado, Bresser and Verao each left annual IPCA higher two years on, so the drop term is clamped at zero; their scores are pure duration (0.075, 0.090, 0.070). The Bresser plan's 1988 IPCA of 980.21%[IBGE] against 79.66% in 1986[IBGE] is the clearest single indictment.

## Caveats the editor should keep

- **Hyperinflation distorts ratios.** A fall from 2477% to 22% is not comparable in welfare terms to a fall from 242% to 363%; the rubric measures proportional change, so late plans start from mechanically larger bases. This favours Collor I and the Real.
- **Base-year effects.** `ipca_after` for Collor I is 1991, the year Collor II launched, so the two Collor plans are partly measuring the same disinflation.
- **Date conventions.** Collor I is dated 16 March 1990 here (the plan page's institution date)[COLLOR]; the English chronology says 15 March 1990[TL]. The Real is dated 1 July 1994 (currency launch)[TL]; its URV phase began 27 February 1994. Using 27 February would cut Collor II to 37 months and its score to about 0.402, which does not change the top three.
- **IPCA, not IGP or INPC.** The rubric specifies IPCA; the pre-1994 IBGE series is used consistently rather than splicing in another index.

## Sources

- [IBGE] IBGE, IPCA monthly number index (base Dec 1993 = 100), SIDRA aggregate 1737, variable 2266, Brazil: https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/all/variaveis/2266?localidades=N1[all] — annual figures are the Dec/Dec change, e.g. 1993 = 2477.15%, 1995 = 22.41%.
- [TL] Wikipedia, "Timeline of Brazilian economic stabilization plans": https://en.wikipedia.org/wiki/Timeline_of_Brazilian_economic_stabilization_plans — Cruzado 28 Feb 1986, Bresser 12 Jun 1987, Verao 15 Jan 1989, Real 1 Jul 1994.
- [COLLOR] Wikipedia (pt), "Plano Collor": https://pt.wikipedia.org/wiki/Plano_Collor — Collor I instituted 16 Mar 1990, Collor II from 31 Jan 1991.
- [rule] Rubric in `RUBRIC.md`: Real has no successor, so months_lasted = 60.

*Prepared from public sources only; all inflation figures are IBGE IPCA. Scoring arithmetic is reproducible from the table above.*
