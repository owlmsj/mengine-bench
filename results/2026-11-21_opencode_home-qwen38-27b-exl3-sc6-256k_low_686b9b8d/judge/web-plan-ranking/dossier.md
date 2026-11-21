# Dossier: Which anti-inflation plan delivered?

**Method.** Rubric in `RUBRIC.md`. IPCA = annual IBGE inflation, calendar year (%). For a plan launched in year Y: `ipca_before` = IPCA of Y-1, `ipca_after` = IPCA of Y+1. `score_drop = clamp(1 - ipca_after/ipca_before, 0, 1)`; `months_lasted` = whole calendar months from launch to the next plan's launch (Real: 60); `score_durability = min(months, 60)/60`; `score = 0.7*drop + 0.3*durability`.

**Data sources.** IPCA annual series (IBGE, via Ipeadata): https://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1410807112&oper=view . Plan launch dates: Cruzado 1986-02-28 (Decreto-Lei 2.283/1986), Bresser 1987-06-12 (Decreto-Lei 2.335/1987), Verao 1989-01-15 (MP 32/1989, Lei 7.730/1989), Collor I 1990-03-16 (MP 168/1990, Lei 8.024/1990), Collor II 1991-01-31 (MP 294/1991, Lei 8.177/1991), Real 1994-07-01 (MP 542/1994) — https://www.planalto.gov.br .

**IPCA used (%):** 1985: 242.23, 1986: 79.66, 1987: 363.41, 1988: 980.21, 1989: 1972.91, 1990: 1620.97, 1991: 472.70, 1992: 1119.10, 1993: 2477.15, 1994: 916.46, 1995: 22.41, 1996: 9.56.

| Plan | Launch | IPCA before | IPCA after | Months | score_drop | score_dur | **Score** |
|---|---|---|---|---|---|---|---|
| Real | 1994-07-01 | 2477.15 (1993) | 22.41 (1995) | 60 | 0.9910 | 1.0000 | **0.9937** |
| Collor I | 1990-03-16 | 1972.91 (1989) | 472.70 (1991) | 11 | 0.7604 | 0.1833 | **0.5873** |
| Collor II | 1991-01-31 | 1620.97 (1990) | 1119.10 (1992) | 42 | 0.3096 | 0.7000 | **0.4267** |
| Bresser | 1987-06-12 | 79.66 (1986) | 980.21 (1988) | 20 | 0.0000 | 0.3333 | **0.1000** |
| Cruzado | 1986-02-28 | 242.23 (1985) | 363.41 (1987) | 16 | 0.0000 | 0.2667 | **0.0800** |
| Verao | 1989-01-15 | 980.21 (1988) | 1620.97 (1990) | 15 | 0.0000 | 0.2500 | **0.0750** |

**Top 3 (best first):** 1. Real (0.9937), 2. Collor I (0.5873), 3. Collor II (0.4267).

**Reading.** The Real plan is the only one that cut inflation it was judged on: 1993's 2477.15% down to 1995's 22.41%, and it held for the full 60-month cap. Collor I produced the sharpest short-lived drop (1989's 1972.91% to 1991's 472.70%) but lasted only 11 months before its successor. Collor II was middling on both axes. The 1986-1989 plans (Cruzado, Bresser, Verao) all show zero drop: the year after each launch was more inflationary than the year before, so they score on durability alone.

**Assumptions.** (1) "Launch date" = the plan's effective date as commonly cited (Cruzado 28 Feb 1986; Bresser 12 Jun 1987; Verao 15 Jan 1989; Collor I 16 Mar 1990; Collor II 31 Jan 1991; Real 1 Jul 1994). (2) Whole calendar months = month difference plus one if the end day is on/after the start day. (3) IPCA values are IBGE's published annual (Dec-vs-Dec) series; pre-1991 figures come from the same IBGE series (IPCA15) as published by Ipeadata. (4) Real's `months_lasted` fixed at 60 per rubric.