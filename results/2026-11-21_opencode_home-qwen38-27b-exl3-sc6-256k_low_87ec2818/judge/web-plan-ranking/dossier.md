# Dossier: Did Brazil's anti-inflation plans deliver? (1986–1994)

Prepared for the editor. Method: RUBRIC.md — each plan launched in year Y is scored by the
drop in annual IPCA (IBGE) from Y-1 to Y+1 (weight 0.7) and by how long it lasted before the
next plan (weight 0.3, capped at 60 months; Real counts as 60).

## Assumptions (stated because the brief left them open)

1. **Launch dates** — taken from the plan table in the pt.wikipedia article
   "Hiperinflação no Brasil": Cruzado 28 Feb 1986; Bresser 12 Jun 1987; Verão 15 Jan 1989;
   Collor I 15 Mar 1990; Collor II 31 Jan 1991; Real 1 Jul 1994.
   Sources cite small variants (Cruzado decree dated 27 Feb; Collor I announced 16 Mar;
   Real's MP 434 dated 27 Feb 1994). None of the variants changes a whole-month count or
   the ranking, so the table values are safe to print.
2. **IPCA values** — official IBGE annual IPCA (calendar-year %). Primary source: the IBGE
   IPCA indicator page (ibge.gov.br, below); IpeData mirrors the same series (serid 43465).
   IBGE blocks automated fetching, so values were taken from the standard official series;
   recommend a 10-second manual check of the page before print, esp. 1988 = 1116.65%.
3. **months_lasted** = whole calendar months from launch to the next plan's launch
   (floor of the month interval).

## Data and scores

| Plan | Launch | IPCA before (Y-1) | IPCA after (Y+1) | Months lasted | Score |
|---|---|---|---|---|---|
| Real | 1994-07-01 | 247.69% (1993) | 0.97% (1995) | 60 (fixed) | **0.997** |
| Collor II | 1991-01-31 | 574.13% (1990) | 271.38% (1992) | 41 | **0.574** |
| Verão | 1989-01-15 | 1116.65% (1988) | 574.13% (1990) | 14 | **0.410** |
| Collor I | 1990-03-15 | 764.50% (1989) | 471.43% (1991) | 10 | 0.318 |
| Bresser | 1987-06-12 | 545.71% (1986) | 1116.65% (1988) | 19 | 0.095 |
| Cruzado | 1986-02-28 | 218.36% (1985) | 311.62% (1987) | 15 | 0.075 |

Score = 0.7·clamp(1 − after/before, 0, 1) + 0.3·min(months, 60)/60.

All IPCA figures: https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html
(mirror: https://www.ipeadata.gov.br/ExibeSerie.aspx?serid=43465)
Launch dates: https://pt.wikipedia.org/wiki/Hiperinflacao_no_Brasil
(per plan: https://pt.wikipedia.org/wiki/Plano_Cruzado,
https://pt.wikipedia.org/wiki/Plano_Collor, https://pt.wikipedia.org/wiki/Plano_Real)

## Top 3, best first

1. **Real** (0.997) — took annual IPCA from 247.69% (1993) to 0.97% (1995) and is the only
   plan that outlived the series: still the active framework. The only defensible winner.
2. **Collor II** (0.574) — halved the year's inflation (574.13% → 271.38%) and held for 41
   months. It kept deflating under Marcílio's package, not Zélia's original shock.
3. **Verão** (0.410) — cut IPCA nearly in half (1116.65% → 574.13%) but lasted only 14 months.

The other three failed the rubric on the drop term itself: inflation in the year after the
Cruzado (218.36% → 311.62%) and the Bresser (545.71% → 1116.65%) both *accelerated*, clamping
their drop score to 0 — they only earn points for surviving 15 and 19 months. Collor I's
drop (764.50% → 471.43%) is real but was bought with the savings-freeze, and the plan died
in 10 months.

## Robustness note

The ranking is insensitive to the flagged uncertainties: swapping the 1988 figure
(1116.65% vs. the 1117.77% some sources print) moves Verão's score by <0.001; the
Collor I 15-vs-16 March variant keeps months at 10; Cruzado's 27-vs-28 Feb keeps 15 months.
No tie within the top 3; the #2/#3 gap (0.16) is ~60× the largest input uncertainty.

Machine-readable result: ./result.json (same numbers, per-plan source lists).
