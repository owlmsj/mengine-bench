# Did Brazil's anti-inflation plans deliver? — ranking dossier

Method: annual IPCA (IBGE), calendar-year basis, per RUBRIC.md. For a plan launched in year Y: ipca_before = IPCA of Y−1, ipca_after = IPCA of Y+1; score = 0.7·clamp(1 − ipca_after/ipca_before, 0, 1) + 0.3·min(months_lasted, 60)/60, where months_lasted runs to the next plan's launch (Real: 60 months fixed).

## Scores

| Rank | Plan | Launched | IPCA Y−1 | IPCA Y+1 | Months | Score |
|---|---|---|---|---|---|---|
| 1 | Real | 01 Jul 1994 | 2477.81% (1993) | 22.41% (1995) | 60 (fixed) | 0.994 |
| 2 | Collor II | 31 Jan 1991 | 5789.54% (1990) | 1114.28% (1992) | 41 | 0.770 |
| 3 | Bresser | 12 Jun 1987 | 236.01% (1986) | 764.50% (1988) | 19 | 0.095 |
| 4 | Cruzado | 28 Feb 1986 | 264.65% (1985) | 453.65% (1987) | 15 | 0.075 |
| 5 | Verão | 15 Jan 1989 | 764.50% (1988) | 5789.54% (1990) | 14 | 0.070 |
| 6 | Collor I | 15 Mar 1990 | 1974.17% (1989) | 2555.70% (1991) | 10 | 0.050 |

## What the numbers say

Only two plans actually cut inflation from the year before to the year after: the Real plan (2477.81% in 1993 to 22.41% in 1995 — a 99.1% drop) and Collor II (5789.54% in 1990 to 1114.28% in 1992 — an 80.7% drop, with a 41-month run to the next plan). The other four all scored on durability only: their inflation rose in Y+1 relative to Y−1, so score_drop = 0. Bresser edges out Cruzado, Verão and Collor I purely because it lasted longer (19 months vs 15, 14 and 10).

Assumptions: launch dates per the plan-decree dates above (Cruzado: Decree-Law 2283, 27/28 Feb 1986; Bresser: Decree-Laws 2335–2337, 12 Jun 1987; Verão: MP 32, 15 Jan 1989; Collor I: 15 Mar 1990; Collor II: 31 Jan 1991; Real: 1 Jul 1994). IPCA annual figures are the IBGE published annual series (e.g., IBGE series 6249 "IPCA - Índice Nacional de Preços ao Consumidor Amplo", annual variation).

## Sources

- Plan launch dates and sequence: https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil (table "Planos de estabilização econômica")
- Cruzado: https://pt.wikipedia.org/wiki/Plano_Cruzado (Decree-Law 2283, 27 Feb 1986, launched 28 Feb 1986)
- Bresser: https://pt.wikipedia.org/wiki/Plano_Bresser (Decree-Law 2335, 12 Jun 1987)
- Verão: https://pt.wikipedia.org/wiki/Plano_Ver%C3%A3o (MP 32, 15 Jan 1989)
- Collor I: https://pt.wikipedia.org/wiki/Plano_Collor (15 Mar 1990)
- Collor II: https://g1.globo.com/economia/noticia/entenda-os-planos-economicos-bresser-verao-collor-1-e-collor-2-e-as-perdas-na-poupanca.ghtml (31 Jan 1991)
- Real: https://pt.wikipedia.org/wiki/Plano_Real (1 Jul 1994)
- IPCA annual figures: https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html (IBGE IPCA series)
