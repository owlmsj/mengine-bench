# Dossier: Brazil's anti-inflation plans, scored

**To:** Policy newsletter editor
**From:** Research desk
**Re:** Which plan delivered what it promised

## Method

Each plan is scored with the supplied rubric against annual IPCA (IBGE) figures taken from SIDRA Table 1737 (variable 2265, December accumulated variation). [Source](https://sidra.ibge.gov.br/tabela/1737). For a plan launched in year Y, `ipca_before` is the IPCA of year Y-1 and `ipca_after` the IPCA of year Y+1.

```
score_drop       = clamp(1 - ipca_after/ipca_before, 0, 1)
months_lasted    = whole calendar months from launch to the next plan's launch
score_durability = min(months_lasted, 60)/60
score            = 0.7*score_drop + 0.3*score_durability
```

Launch dates are the official decree/MP dates: Cruzado 28 Feb 1986 (Decreto-Lei 2.283), Bresser 12 Jun 1987 (DL 2.335), Verao 15 Jan 1989 (MP 32), Collor I 16 Mar 1990 (MP 168), Collor II 31 Jan 1991 (MP 294), Real 1 Jul 1994 (MP 542, effective in circulation). Source: Planalto legislative archive.

## Assumptions stated up front

- **Annual IPCA is the calendar-year figure.** For a plan launched in year Y, `ipca_before` is the full-year IPCA of year Y-1 and `ipca_after` the full-year IPCA of year Y+1. No prorating even where a plan landed mid-year, per the rubric.
- **`months_lasted` counts whole calendar months wholly inside the interval** between a plan's launch and its successor's launch (partial leading/trailing months discarded). For the Real there is no successor, so the rubric assigns 60.
- A plan whose `ipca_after` exceeded its `ipca_before` takes `score_drop` = 0; this is why several 1980s plans collapse despite lasting many months.

## Full field, ranked

| Rank | Plan | Launch | IPCA before (Y-1) | IPCA after (Y+1) | Months lasted | Score |
|------|------|--------|-------------------|------------------|---------------|-------|
| 1 | Real | 1 Jul 1994 | 2477.15 (1993) | 22.41 (1995) | 60 | **0.994** |
| 2 | Collor I | 16 Mar 1990 | 1972.91 (1989) | 472.70 (1991) | 10 | **0.582** |
| 3 | Collor II | 31 Jan 1991 | 1620.97 (1990) | 1119.10 (1992) | 41 | **0.422** |
| 4 | Bresser | 12 Jun 1987 | 79.66 (1986) | 980.21 (1988) | 18 | 0.090 |
| 5 | Cruzado | 28 Feb 1986 | 242.23 (1985) | 363.41 (1987) | 15 | 0.075 |
| 6 | Verao | 15 Jan 1989 | 980.21 (1988) | 1620.97 (1990) | 13 | 0.065 |

### Worked example (Real)
drop = 1 - 22.41/2477.15 = 0.991; durability = min(60,60)/60 = 1.0; score = 0.7*0.991 + 0.3*1.0 = 0.994. All four digits traceable to the two source lines above.

## Narrative for the piece

Only the Real cleared the bar the rubric sets. Its annual inflation went from 2477.15% (1993) to 22.41% (1995), a 99.1% proportional drop, and because it outlasted every predecessor without a successor it also maxes the durability term at 1.0. It is the single plan the data unambiguously supports as having "delivered."

Collor I ranks second on arithmetic alone. Annual inflation did fall sharply from the 1989 spike (1972.91% -> 472.70%), earning a solid drop term, but the effect reversed within a year (1992 was back up to 1119.10%) and the plan lasted only ten whole months before Collor II replaced it. Defensible as a short-run shock, not as a fix.

Collor II lands third by being the rare case where neither term dominates: it bought time (41 months before the Real) and cut inflation partway (1620.97% -> 1119.10%), but never close. The 1980s plans all collapse to near zero because their post-plan inflation exploded, erasing any durability credit.

## Sources (every number traceable to a URL)

IPCA series (SIDRA Table 1737, variable 2265): https://sidra.ibge.gov.br/tabela/1737
Launch dates / underlying decrees and MPs (Planalto):
- Cruzado (Decreto-Lei 2.283, 28 Feb 1986): https://www.planalto.gov.br/ccivil_03/decreto-lei/del2283.htm
- Bresser (Decreto-Lei 2.335, 12 Jun 1987): https://www.planalto.gov.br/ccivil_03/decreto-lei/del2335.htm
- Verao (Medida Provisoria 32, 15 Jan 1989): https://www.planalto.gov.br/ccivil_03/mpv/1988-1990/rmpv.htm
- Collor I (Medida Provisoria 168, 16 Mar 1990): https://www.planalto.gov.br/ccivil_03/mpv/antigas/168.htm
- Collor II (Medida Provisoria 294, 31 Jan 1991): https://www.planalto.gov.br/ccivil_03/mpv/antigas/294.htm
- Real (Medida Provisoria 542, 30 Jun 1994; currency in circulation 1 Jul 1994): https://www.planalto.gov.br/ccivil_03/mpv/1699.htm
