# Dossier: Which Brazilian anti-inflation plan delivered?

Prepared for the editor. Question: of the six stabilization plans from Cruzado to Real, which delivered what it promised? Method fixed by ./RUBRIC.md: score = 0.7 × inflation drop + 0.3 × durability.

## Method and assumptions
- Inflation = annual IPCA (IBGE), calendar year, %.
- For a plan launched in year Y: ipca_before = IPCA of Y−1; ipca_after = IPCA of Y+1; score_drop = clamp(1 − ipca_after/ipca_before, 0, 1).
- months_lasted = whole calendar months from launch to the next plan's launch (Real: 60 per rubric); score_durability = min(months, 60)/60.
- Assumptions stated: IPCA series is IBGE SIDRA table 1737 (the current revised series, 1985: 242.23%, 1986: 79.66%, 1988: 980.21%, 1990: 1,620.97%, 1991: 472.70%); Collor I dated 16 Mar 1990 (MP 168, measures effective 15–16 Mar; one source says 15 Mar, another 16 Mar — the ranking does not change either way); Real dated 1 Jul 1994 (currency launch; URV began 1 Mar 1994 but the plan is counted from the Real's circulation).

## The data
IPCA annual (IBGE, table 1737): 1985: 242.23 | 1986: 79.66 | 1987: 363.41 | 1988: 980.21 | 1989: 1,972.91 | 1990: 1,620.97 | 1991: 472.70 | 1992: 1,119.10 | 1993: 2,477.15 | 1994: 916.46 | 1995: 22.41

Launch dates: Cruzado 28 Feb 1986 (Decreto-Lei 2.283); Bresser 12 Jun 1987; Verão 15 Jan 1989 (MP 32); Collor I 16 Mar 1990 (MP 168); Collor II 31 Jan 1991; Real 1 Jul 1994.

## Scores
| plan | ipca_before | ipca_after | months | drop | durability | score |
|---|---|---|---|---|---|---|
| Real | 2,477.15 (1993) | 22.41 (1995) | 60 | 0.991 | 1.000 | **0.994** |
| Collor I | 1,972.91 (1989) | 472.70 (1991) | 10 | 0.760 | 0.167 | **0.582** |
| Collor II | 1,620.97 (1990) | 1,119.10 (1992) | 41 | 0.310 | 0.683 | **0.422** |
| Bresser | 79.66 (1986) | 980.21 (1988) | 19 | 0 | 0.317 | 0.095 |
| Cruzado | 242.23 (1985) | 363.41 (1987) | 15 | 0 | 0.250 | 0.075 |
| Verão | 980.21 (1988) | 1,620.97 (1990) | 14 | 0 | 0.233 | 0.070 |

## Ranking: the top 3
1. **Real (0.994).** The only plan that delivered both halves of the promise: IPCA fell from 2,477.15% (1993) to 22.41% (1995) and it has held — scored the full 60 months by rubric, and the currency is still in circulation.
2. **Collor I (0.582).** Confiscated savings and broke the spiral: IPCA fell ~76% (1,972.91% → 472.70%) — but only for 10 months before Collor II was needed.
3. **Collor II (0.374 → 0.422 with the revised series).** A weak drop (1,620.97% → 1,119.10%, ~31%) but it lasted 41 months, right up to the Real.

The other three score 0 on inflation drop: after each one, IPCA the following year was higher than the year before (Cruzado 242.23 → 363.41; Bresser 79.66 → 980.21; Verão 980.21 → 1,620.97). Their scores are durability only.

## Editor's caveats
- Earlier plans' scores depend entirely on the durability term; the drop term floors at 0.
- IPCA values differ across references (older literature cites 1985: 227.6%, 1986: 59.8%, 1990: 1,474.1%); we use the current IBGE SIDRA series consistently. Collor I vs Collor II swap would require a different dating of Collor II, not just the Mar 15/16 discrepancy.

## Sources (each figure)
- IPCA 1985–1995, annual: https://sidra.ibge.gov.br/tabela/1737 (IBGE SIDRA table 1737, IPCA accumulated yearly variation); same series listed at https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html
- Plan dates: https://pt.wikipedia.org/wiki/Plano_Cruzado · https://pt.wikipedia.org/wiki/Plano_Bresser · https://pt.wikipedia.org/wiki/Plano_Ver%C3%A3o · https://pt.wikipedia.org/wiki/Plano_Collor · https://pt.wikipedia.org/wiki/Plano_Real
