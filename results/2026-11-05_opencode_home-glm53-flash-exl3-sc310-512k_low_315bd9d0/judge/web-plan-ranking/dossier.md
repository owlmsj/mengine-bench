# Dossier: Did Brazil's anti-inflation plans deliver? (Editor's brief)

**Bottom line: only the Plano Real delivered what it promised.** All five 1986-1991 shock plans failed to durably cut inflation; the Real broke it for good.

## Method and assumptions
- Annual IPCA taken as the December-to-December change in the official IBGE IPCA series, pulled directly from Ipeadata (IBGE series `PRECOS12_IPCA12`): http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='PRECOS12_IPCA12'). Cross-check: this reproduces the widely published official annual figures (1989: 1972.9%, 1994: 916.5%, 1995: 22.4%, 1996: 9.6%). Assumption: for 1985-1988 the retroactive IBGE series (242.2, 79.7, 363.4, 980.2) is used; contemporaneous press figures of the era differ slightly because the index was rebased, but the rubric's ordering is unaffected.
- Launch dates (public record, Wikipedia articles on each plan): Cruzado 28 Feb 1986 (https://pt.wikipedia.org/wiki/Plano_Cruzado), Bresser 12 Jun 1987 (https://pt.wikipedia.org/wiki/Plano_Bresser), Verão 15 Jan 1989 (https://pt.wikipedia.org/wiki/Plano_Ver%C3%A3o), Collor I 16 Mar 1990 (https://pt.wikipedia.org/wiki/Plano_Collor), Collor II 31 Jan 1991 (https://pt.wikipedia.org/wiki/Plano_Collor), Real 1 Jul 1994 (https://pt.wikipedia.org/wiki/Plano_Real).
- Months lasted = calendar-month difference to next plan's launch; Real fixed at 60 per rubric. Score = 0.7*drop + 0.3*durability, exactly as in ./RUBRIC.md (computed in tmp_calc.py from the Ipeadata download).

## Ranking (rubric scores, 0-1)

| # | Plan | IPCA year before | IPCA year after | Lasted (months) | Score |
|---|------|------------------|-----------------|-----------------|-------|
| 1 | Plano Real | 2477.1% (1993) | 22.4% (1995) | 60 | 0.994 |
| 2 | Plano Collor I | 1972.9% (1989) | 472.7% (1991) | 10 | 0.582 |
| 3 | Plano Collor II | 1621.0% (1990) | 1119.1% (1992) | 41 | 0.422 |
| 4 | Plano Bresser | 79.7% (1986) | 980.2% (1988) | 19 | 0.095 |
| 5 | Plano Cruzado | 242.2% (1985) | 363.4% (1987) | 16 | 0.080 |
| 6 | Plano Verão | 980.2% (1988) | 1621.0% (1990) | 14 | 0.070 |

Numbers source (all): Ipeadata IPCA series URL above.

## What the editor can defend
- **Real (0.994)**: inflation fell 99% in one year (2477.1% -> 22.4%) and never returned; the plan's currency (real, July 1994) still circulates. Source: Ipeadata URL above; https://pt.wikipedia.org/wiki/Plano_Real.
- **Collor I (0.582)**: the only shock plan that actually cut inflation the following year (1972.9% -> 472.7%, a 76% drop), but it collapsed in 10 months; confisca of savings bought a brief disindexation, not stability. Sources: Ipeadata URL; https://pt.wikipedia.org/wiki/Plano_Collor.
- **Collor II (0.422)**: modest drop (1621.0% -> 1119.1%, ~31%) and longer life (41 months to the Real), mostly because it was the last failed plan before the Real, not because it worked. Sources: Ipeadata URL; https://pt.wikipedia.org/wiki/Plano_Collor.
- **Cruzado, Bresser, Verão (0.070-0.095)**: inflation was HIGHER the year after each launch. The Cruzado freeze even created a repressed-inflation boom that exploded in 1987 (79.7% -> 363.4%). These plans scored 0 on the inflation-drop component. Sources: Ipeadata URL; https://pt.wikipedia.org/wiki/Plano_Cruzado; https://pt.wikipedia.org/wiki/Plano_Bresser; https://pt.wikipedia.org/wiki/Plano_Ver%C3%A3o.

## Caveats
- 1985-1988 IPCA uses the rebased retroactive series; alternative contemporaneous figures (e.g., 235.1% for 1985) would not change the ranking because those plans score 0 on drop and their durability terms are unchanged.
- "Months lasted" counts calendar months between launches, so Collor I's 10 months reflects being replaced by Collor II, not an independent judgment of failure.
- machine-readable result: ./result.json