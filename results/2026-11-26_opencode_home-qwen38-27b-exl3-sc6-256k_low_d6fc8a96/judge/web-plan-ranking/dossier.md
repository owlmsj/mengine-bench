# Dossier: which anti-inflation plan delivered?

For the editor. One page. Method: RUBRIC.md — score = 0.7 * drop in annual IPCA
(Y-1 to Y+1) + 0.3 * durability (whole months until the next plan, capped at 60).

## Data

Annual IPCA (IBGE, % per calendar year): 1985: 242.23; 1986: 79.66; 1987: 363.41;
1988: 980.21; 1989: 1972.91; 1990: 1620.97; 1991: 472.70; 1992: 1119.10;
1993: 2477.15; 1994: 916.46; 1995: 22.41.
Source: https://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1410807112&oper=view

Launch dates: Cruzado 28/02/1986; Bresser 12/06/1987; Verao 15/01/1989;
Collor I 16/03/1990; Collor II 31/01/1991; Real 01/07/1994.
Sources: https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFW4mOtzaI48ow8Zj1jvNiyaVozf2KptIK0IE9N8vQzAj9udyqFAeG079hDDB0NqK6yzHTU7xXF1dC61lWZOrcChTxnqDmpE58HHOVd8LPawUUwxvT4ODg= (Cruzado),
https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEL8D-IJXgcWwJ1KNW4-0R68NDG7MhW-0LtbK6PQbUHDm0iFy8qMhukVpLbS-0UrskhpIA_SfSG4-s_ABdulfWOSJUKhZ6gy3JZU6GdXVCdwEHTeeV0fC8G4Tp28fFpN5RaEkuVYOv4NMIE9AF-T3mCgDfypC5ryFQctvTeSo80o1KoyVEyKQHpTkNckjZFGRi7IDPBaJky1AFZW-kE628qPEG1JTRfzCw1CQ== (Bresser),
https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHt7o-RiFIfaP_5OAPc7oAStsSfkWy05naJl31X0p-KoJJKEYacL4bQz6qrhWYKfswQ_YHF1GuHBHZhwtT-9g-3ZfhhD6dP6_szz_JcTibNsU0WOn3IOOeopH43JW7uiBY2_bGDhB42sp9ohfnxLNwM3ZT9VAibPpBETnXqdgylLeQvbFfWfMY= (Verao),
https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFocH1ngNn1vXrVZB9X9FG67jrZ_6PQDwVvWPkRisHJHvvRBqVS4rQXdSoR5zbA0AYGU4ZV2iHWMH_mJaZm-7dPmPbXsIM9uDZzWQk58NqJwd82_ZxYsNveC7JjQT2NtA== (Collor I),
https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF23KwQGplBJKHtp35O6wG-rYwe3PMrkANVUIg17QP0J4F45cZQA3E9omUcj_ZcySKFyYeUzqtRY-QeQnXiRU8lVWy2moFEgZTjtep-SNWjH_gySShHiA== (Collor II),
https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFrEk2SqOIJL_M9XtYwlUZK45ylpqZDkgcPNf0WtQgzVrcLmH4M1PoLfxsZpvx4Sa6mQUqC1oLxZrYEq1PZt4CnMDp1ZcS2DclnAHF4D_4y_3Uk1g_3MR7HJbC-pV-LQFjisaUu4SEXOhsKfAyLPUeeCOyIYQrcqRdy-M2hmVy54VtXbw== (Real).

## Scores

| plan | launch | ipca_before | ipca_after | months_lasted | score |
|---|---|---|---|---|---|
| Real | 1994-07-01 | 2477.15 | 22.41 | 60 | 0.9937 |
| Collor I | 1990-03-16 | 1972.91 | 472.70 | 10 | 0.5823 |
| Collor II | 1991-01-31 | 1620.97 | 1119.10 | 42 | 0.4267 |
| Bresser | 1987-06-12 | 79.66 | 980.21 | 19 | 0.0950 |
| Cruzado | 1986-02-28 | 242.23 | 363.41 | 16 | 0.0800 |
| Verao | 1989-01-15 | 980.21 | 1620.97 | 14 | 0.0700 |

## Top 3 (best first)

1. Real (0.9937) — IPCA fell from 2477.15% (1993) to 22.41% (1995); no next plan, durability capped at 60 months.
2. Collor I (0.5823) — IPCA fell from 1972.91% (1989) to 472.70% (1991); lasted 10 months.
3. Collor II (0.4267) — IPCA fell from 1620.97% (1990) to 1119.10% (1992); lasted 42 months.

## Assumptions

- "Verao" = Plano Verão (1989), per the rubric table.
- months_lasted = whole calendar months between launch dates (date arithmetic on day/month/year), per RUBRIC.md.
- Real has no next plan: months_lasted = 60 per RUBRIC.md.
- IPCA values are annual (Dec-to-Dec) calendar-year figures, per RUBRIC.md.