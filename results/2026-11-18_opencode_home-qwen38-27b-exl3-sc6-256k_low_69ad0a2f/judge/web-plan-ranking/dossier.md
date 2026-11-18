# Dossier: Which Brazilian anti-inflation plan delivered?

**For the editor.** One page. Ranking is fully reproducible from the rubric in `RUBRIC.md` plus two public sources.

## Method (assumptions stated)
- Inflation = annual IPCA (IBGE), in % for the calendar year. Annual figures are the geometric product of the 12 monthly IPCA values from the official Banco Central do Brasil series 433 (the IBGE IPCA), which is how IBGE itself publishes the annual.
- `ipca_before` = annual IPCA of year Y-1; `ipca_after` = annual IPCA of year Y+1, where Y is the launch year.
- `score_drop = clamp(1 - ipca_after/ipca_before, 0, 1)`; `score_durability = min(months_lasted,60)/60`; `score = 0.7*score_drop + 0.3*score_durability`.
- Launch dates (public): Cruzado 28 Feb 1986; Bresser 12 Jun 1987; Verao 15 Jan 1989; Collor I 16 Mar 1990; Collor II 31 Jan 1991; Real 1 Jul 1994. `months_lasted` = whole calendar months launch-to-next-launch; Real = 60 (rubric).
- Assumption: "Verao" = Plano Verão (1989); "Collor I/II" are the two Collor packages, not Plano Marcílio (which the rubric does not list).

## Annual IPCA (IBGE, % per calendar year)
| 1985 | 1986 | 1987 | 1988 | 1989 | 1990 | 1991 | 1992 | 1993 | 1994 | 1995 |
|---|---|---|---|---|---|---|---|---|---|---|
| 242.25 | 79.66 | 363.41 | 980.22 | 1972.91 | 1620.97 | 472.69 | 1119.09 | 2477.15 | 916.43 | 22.41 |

Source for all monthly IPCA (1980-2026): https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json

## Scores
| Plan | Launch | IPCA before | IPCA after | Months | score_drop | score_dur | **score** |
|---|---|---|---|---|---|---|---|
| Real | 1994-07-01 | 2477.15 | 22.41 | 60 | 0.991 | 1.000 | **0.9937** |
| Collor I | 1990-03-16 | 1972.91 | 472.69 | 10 | 0.760 | 0.167 | **0.5823** |
| Collor II | 1991-01-31 | 1620.97 | 1119.09 | 42 | 0.310 | 0.700 | **0.4267** |
| Bresser | 1987-06-12 | 79.66 | 980.22 | 19 | 0.000 | 0.317 | **0.095** |
| Cruzado | 1986-02-28 | 242.25 | 363.41 | 16 | 0.000 | 0.267 | **0.080** |
| Verao | 1989-01-15 | 980.22 | 1620.97 | 14 | 0.000 | 0.233 | **0.070** |

## Top 3 (best first)
1. **Real** (0.9937) - cut annual IPCA from 2477.15% (1993) to 22.41% (1995) and stayed in force for the full 60-month cap. The only plan that both crushed inflation and lasted.
2. **Collor I** (0.5823) - cut annual IPCA from 1972.91% (1989) to 472.69% (1991), a big drop, but lasted only 10 months before Collor II.
3. **Collor II** (0.4267) - cut 1620.97% (1990) to 1119.09% (1992) and lasted 42 months; durability carried it past Bresser/Cruzado/Verao, whose `ipca_after` exceeded `ipca_before` (score_drop clamped to 0).

## Why the bottom three are near zero
Cruzado, Bresser and Verao all saw the following year's annual IPCA *higher* than the prior year's (price-freeze plans that failed, then re-accelerated), so `score_drop` clamps to 0 and only durability (short months) survives. That is the rubric's intended reading: they did not deliver.

## Sources (every number traced)
- Monthly IPCA 1980-2026 (all annual figures above): https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json
- Cruzado launch 28 Feb 1986: https://pt.wikipedia.org/wiki/Plano_Cruzado
- Bresser launch 12 Jun 1987; Verao launch 15 Jan 1989: https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil
- Collor I 16 Mar 1990; Collor II 31 Jan 1991: https://pt.wikipedia.org/wiki/Plano_Collor
- Real launch 1 Jul 1994: https://pt.wikipedia.org/wiki/Plano_Real