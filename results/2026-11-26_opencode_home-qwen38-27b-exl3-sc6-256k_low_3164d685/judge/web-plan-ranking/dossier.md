# Dossier: which of Brazil's anti-inflation plans delivered?

For the editor's ranking piece. Rubric: ./RUBRIC.md. Inflation = annual IPCA (IBGE), calendar year.
For a plan launched in year Y: ipca_before = IPCA(Y-1), ipca_after = IPCA(Y+1);
score = 0.7 * clamp(1 - ipca_after/ipca_before, 0, 1) + 0.3 * min(months_lasted, 60)/60.

## Assumptions (brief left these open)
- Launch dates taken from the plan's own enactment (Wikipedia, cross-checked across the
  Hiperinflação no Brasil table): Cruzado 28/02/1986, Bresser 12/06/1987, Verão 15/01/1989,
  Collor I 16/03/1990, Collor II 31/01/1991, Real 01/07/1994 (real currency launch; the URV
  phase began 27/02/1994, but the plan's effective stabilization is the 01/07/1994 switch).
- "Next plan" per the rubric table; months_lasted = whole calendar months between launches.
  Real has no next plan: 60 months by the rubric.
- Annual IPCA computed by compounding the official monthly IPCA series (Banco Central do
  Brasil, série 433), which reproduces IBGE's published annual figures.

## Scores (all plans)

| plan | launch | IPCA before | IPCA after | months | score |
|---|---|---|---|---|---|
| Real | 1994-07-01 | 2477.15 (1993) | 22.41 (1995) | 60 | **0.9937** |
| Collor I | 1990-03-16 | 1972.91 (1989) | 472.69 (1991) | 10 | **0.5823** |
| Collor II | 1991-01-31 | 1620.97 (1990) | 1119.09 (1992) | 42 | **0.4267** |
| Bresser | 1987-06-12 | 79.66 (1986) | 980.22 (1988) | 19 | 0.0950 |
| Cruzado | 1986-02-28 | 242.25 (1985) | 363.41 (1987) | 16 | 0.0800 |
| Verão | 1989-01-15 | 980.22 (1988) | 1620.97 (1990) | 14 | 0.0700 |

## Top 3 (best first)
1. **Real** — 0.9937. The only plan that actually delivered: annual IPCA fell from
   2477.15% (1993) to 22.41% (1995) and stayed there.
2. **Collor I** — 0.5823. Big one-year drop (1972.91% to 472.69%) but it lasted only 10
   months before Collor II.
3. **Collor II** — 0.4267. Moderate drop (1620.97% to 1119.09%) but it held for 42 months.

The Sarney-era plans (Cruzado, Bresser, Verão) all score under 0.10: each was replaced
before its "after" year, and inflation in the following year was always higher than before.

## Sources
- Annual IPCA (compounded from monthly, série 433):
  https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json
- Plan launch dates (table "Planos de estabilização econômica"):
  https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil
- Cruzado (28/02/1986): https://pt.wikipedia.org/wiki/Plano_Cruzado
- Collor I (16/03/1990) and Collor II (31/01/1991): https://pt.wikipedia.org/wiki/Plano_Collor
- Real (01/07/1994): https://pt.wikipedia.org/wiki/Plano_Real
- Bresser (12/06/1987) and Verão (15/01/1989): decree-law dates in
  https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil (DL 2.335/87; MP 32/89)