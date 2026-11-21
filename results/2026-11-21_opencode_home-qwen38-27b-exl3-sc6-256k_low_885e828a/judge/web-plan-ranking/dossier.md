# Dossier: Which of Brazil's anti-inflation plans delivered?

**For the editor — one page. Method: RUBRIC.md, scored from public data.**

## The ranking (top 3, best first)

| Rank | Plan | Launched | IPCA before (Y-1) | IPCA after (Y+1) | Months lasted | Score |
|---|---|---|---|---|---|---|
| 1 | **Real** | 1 Jul 1994 | 2477.15% (1993) | 22.41% (1995) | 60 (capped) | **0.994** |
| 2 | **Collor I** | 15 Mar 1990 | 1972.91% (1989) | 472.69% (1991) | 10 | **0.582** |
| 3 | **Collor II** | 31 Jan 1991 | 1620.97% (1990) | 1119.09% (1992) | 41 | **0.422** |

Full table (all six):

| Plan | Launched | IPCA before | IPCA after | Months | drop | dur | Score |
|---|---|---|---|---|---|---|---|
| Real | 1994-07-01 | 2477.15 | 22.41 | 60 | 0.9910 | 1.0000 | 0.9937 |
| Collor I | 1990-03-15 | 1972.91 | 472.69 | 10 | 0.7604 | 0.1667 | 0.5823 |
| Collor II | 1991-01-31 | 1620.97 | 1119.09 | 41 | 0.3096 | 0.6833 | 0.4217 |
| Bresser | 1987-06-12 | 79.66 | 980.22 | 19 | 0.0000 | 0.3167 | 0.0950 |
| Cruzado | 1986-02-28 | 242.25 | 363.41 | 15 | 0.0000 | 0.2500 | 0.0750 |
| Verao | 1989-01-15 | 980.22 | 1620.97 | 14 | 0.0000 | 0.2333 | 0.0700 |

## How it was scored (per RUBRIC.md)
- `ipca_before` = annual IPCA of Y-1; `ipca_after` = annual IPCA of Y+1 (IBGE, calendar year, %).
- `score_drop = clamp(1 - ipca_after/ipca_before, 0, 1)`; `score_durability = min(months,60)/60`.
- `score = 0.7*drop + 0.3*durability`. `months_lasted` = whole calendar months from launch to the next plan's launch (Real: 60, no next plan).

## The story
The **Real** is the only plan that actually delivered: it cut 1995 inflation (22.41%) to under 1% of the 1993 peak (2477.15%) and held, earning a near-perfect 0.994. **Collor I** got the biggest single-year drop of the 1990s (1989→1991) but lasted only 10 months before Collor II replaced it, so durability capped it at 0.582. **Collor II** outlived Collor I (41 months) but its 1992 inflation (1119.09%) was still more than double the 1990 level, so the drop score is weak. The 1980s plans — **Cruzado, Bresser, Verao** — all *failed*: the year after each launched, inflation was higher than the year before (drop clamped to 0), and none lasted past 19 months.

## Sources
- Annual IPCA (IBGE), 1985–1996: IpeData series 433 (IPCA, monthly) and IBGE IPCA page.
  - https://ipeadata.gov.br/series.aspx?p=209
  - https://www.ibge.gov.br/estatisticas/economicas/28728/ipca.html
- Plan launch dates: Wikipedia, "Hiperinflação no Brasil" (stabilization-plan table) and "Plano Cruzado".
  - https://pt.wikipedia.org/wiki/Hiperinfla%C3%A7%C3%A3o_no_Brasil
  - https://pt.wikipedia.org/wiki/Plano_Cruzado

## Assumptions
- "Verao" = Plano Verão (15 Jan 1989). "Collor I" = Plano Collor (15 Mar 1990); "Collor II" = 31 Jan 1991.
- Real launch = 1 Jul 1994 (currency introduction; URV phase began Feb 1994). Using 1 Jul keeps months_lasted at the 60 cap either way.
- IPCA figures as published by IBGE/IpeData; small rounding differences between mirrors (e.g. 1985 = 242.25 vs 242.23) do not change any score or the ranking.