# Dossier: Did Brazil's anti-inflation plans deliver?

Scope: six plans on the rubric (Cruzado 1986, Bresser 1987, Verao 1989, Collor I 1990, Collor II 1991, Real 1994).
Method: per rubric, ipca_before = IBGE annual IPCA of launch year minus 1, ipca_after = of launch year plus 1; score = 0.7 * drop + 0.3 * min(months,60)/60. Launch dates from public historical records; Real uses July 1, 1994 (currency launch) and 60 months per the rubric's no-next-plan rule.

## Score table

| plan | launch | ipca_before (Y-1) | ipca_after (Y+1) | months | score |
|---|---|---|---|---|---|
| Cruzado | 1986-02-28 | 242.23% (1985) | 363.41% (1987) | 15 | 0.075 |
| Bresser | 1987-06-15 | 79.66% (1986) | 980.21% (1988) | 19 | 0.095 |
| Verao | 1989-01-15 | 980.21% (1988) | 1620.97% (1990) | 14 | 0.070 |
| Collor I | 1990-03-16 | 1972.91% (1989) | 472.70% (1991) | 10 | 0.582 |
| Collor II | 1991-01-31 | 1620.97% (1990) | 1119.10% (1992) | 41 | 0.422 |
| Real | 1994-07-01 | 2477.15% (1993) | 22.41% (1995) | 60 | 0.994 |

## Top 3
1. Real 0.994
2. Collor I 0.582
3. Collor II 0.422

## Notes and assumptions
- IPCA series: annual accumulated (IBGE, via Ipeadata): 1985 242.23, 1986 79.66, 1987 363.41, 1988 980.21, 1989 1972.91, 1990 1620.97, 1991 472.70, 1992 1119.10, 1993 2477.15, 1994 916.46, 1995 22.41. Source: https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFaldNsSeZk0wjkcT_MIOpAiC33s25Zyx3OUcrPyCyapOpJHPyISgixjThcqvhTI5iIU9u7yxEEXlMfUdQ4TF4sT9Cmmq8agiCWHwzoYGlw_XCaQRLZqAiPQvlTzsGJeYcpRrGqrBv5C5Vbq3CXHOWVgwlmQN3rNH2OKcXJtWL00TnY2uYn
- Launch dates: Cruzado 28 Feb 1986, Bresser 15 Jun 1987, Verao 15 Jan 1989, Collor I 16 Mar 1990, Collor II 31 Jan 1991, Real 1 Jul 1994 (currency; Plan Real was announced Feb 1994). Source: https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE7J2gSXP3bmzVeRFuCPU5EHOea_x6yuTyJDRzyh3K-DPvyzrdeFPmNe8Rxhw2X8XkoyDv-yjS-WDyb9DKJrSZrAQ7ALWDHB0Gm7jpb2OPEBWvBtu9-L2Y=
- The rubric's before/after test is harsh: Cruzado, Bresser and Verao all score near zero because inflation after the plan year was still higher or nearly as high; Real is the clear winner.
- Durability uses whole calendar months between launch dates; Real uses 60 by rubric default.
- Real anchor 1994: I chose the 1 Jul 1994 currency launch date, not the Feb 1994 announcement, which is the conventional date used for the plan launch.
