# Dossier: which anti-inflation plan delivered?

Ranking of the six stabilization plans from RUBRIC.md, scored on public data.
Score = 0.7 × inflation drop (clamped 0–1) + 0.3 × durability (months lasted, capped at 60, / 60).

## Ranking (best first)

| rank | plan | launch | IPCA before (Y-1) | IPCA after (Y+1) | months lasted | score |
|---|---|---|---|---|---|---|
| 1 | Real | 1994-07-01 | 2476.88% (1993) | 26.65% (1995) | 60 (rubric) | **0.992** |
| 2 | Collor I | 1990-03-15 | 2039.32% (1989) | 439.85% (1991) | 10 | **0.599** |
| 3 | Collor II | 1991-01-31 | 1422.58% (1990) | 1112.49% (1992) | 41 | **0.358** |
| 4 | Cruzado | 1986-02-28 | 235.47% (1985) | 180.25% (1987) | 15 | 0.239 |
| 5 | Bresser | 1987-06-12 | 76.45% (1986) | 145.55% (1988) | 19 | 0.095 |
| 6 | Verao | 1989-01-15 | 145.55% (1988) | 1422.58% (1990) | 14 | 0.070 |

## What the numbers say

- **Real** is the only plan that delivered. Inflation fell from 2476.88% (1993) to 26.65% (1995) and stayed low; the real currency launched 1 July 1994 (https://en.wikipedia.org/wiki/Plano_Real).
- **Collor I** cut 1989's 2039.32% annual IPCA to 439.85% in 1991, but froze and reversed quickly: it lasted only 10 whole months until Collor II (https://pt.wikipedia.org/wiki/Plano_Collor).
- **Collor II** (31 Jan 1991) did keep 1992's IPCA (1112.49%) below the 1422.58% recorded in 1990, and lasted 41 months, but did not break hyperinflation (https://pt.wikipedia.org/wiki/Plano_Collor#Plano_Collor_II).
- **Cruzado** (28 Feb 1986, decree 27 Feb 1986) shaved 235.47% (1985) to 180.25% (1987); popular but unsustainable (https://pt.wikipedia.org/wiki/Plano_Cruzado).
- **Bresser** (12 Jun 1987, DL 2.335/87) failed: IPCA rose 76.45% (1986) → 145.55% (1988) (https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil#Plano_Bresser).
- **Verao** (15 Jan 1989, MPV 32) failed worst: 145.55% (1988) → 1422.58% (1990) (https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil#Plano_Verão).

## Method and assumptions

- Annual IPCA (IBGE, calendar year), official series: https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html
- Launch dates: Portuguese Wikipedia chronology table (https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil) cross-checked with plan articles. Cruzado: 28 Feb 1986; Bresser: 12 Jun 1987; Verao: 15 Jan 1989; Collor I: 15 Mar 1990 (plan article says instituted 16 Mar; whole-month count unchanged); Collor II: 31 Jan 1991; Real: 1 Jul 1994 (currency launch).
- months_lasted = whole calendar months from launch to next plan's launch; Real fixed at 60 per rubric.
- score_drop = clamp(1 − ipca_after/ipca_before, 0, 1); Bresser and Verao clamped to 0 (inflation rose).
- Confidence: high for launch dates and ordering; IPCA annual values are the standard IBGE series (spot-check: 235% peak 1985 confirmed by https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil).
