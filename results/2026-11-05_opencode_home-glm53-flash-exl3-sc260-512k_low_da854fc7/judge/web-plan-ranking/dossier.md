# Dossier: Brazil's anti-inflation plans, ranked by what they delivered

Prepared with the rubric in RUBRIC.md. All inflation figures are annual IPCA
(IBGE, Table 1737, 12-month accumulated variation at December, Brazil):
https://sidra.ibge.gov.br/tabela/1737 (values verified directly via
https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/198512,198612,198712,198812,198912,199012,199112,199212,199312,199412,199512/variaveis/2265?localidades=N1[all])

## Ranking

### 1. Plano Real (July 1, 1994) - score 0.99
Launched July 1, 1994 (currency launch; MP 542/Lei 9.069, https://www.planalto.gov.br/ccivil_03/leis/l9069.htm; chronology https://www.bcb.gov.br/controleinflacao/historico). IPCA fell from 2,477.15% (1993) to 22.41% (1995) - the only plan that produced durable disinflation. It never had a successor; 32+ years later the Real is still the currency.
- ipca_before 2,477.15% -> ipca_after 22.41%; months_lasted 60 (rubric cap); score = 0.9937.

### 2. Plano Cruzado (February 28, 1986) - score 0.77
Launched Feb 28, 1986 (Decreto-Lei 2.283, replaced by DL 2.284, https://www.planalto.gov.br/ccivil_03/decreto-lei/del2284.htm). IPCA dropped from 242.23% (1985) to 79.66% (1986) - a deep one-year cut, but the freeze broke and inflation surged back to 363.41% in 1987. Bresser followed on June 12, 1987.
- ipca_before 242.23% -> ipca_after 79.66%; months_lasted 15 (Feb 28, 1986 to Jun 12, 1987); score = 0.7698.

### 3. Plano Collor II (January 31, 1991) - score 0.70
Launched Jan 31, 1991 (MP 294, converted into Lei 8.177, https://www.planalto.gov.br/ccivil_03/leis/l8177.htm). It cut IPCA from 1,620.97% (1990) to 472.70% (1991). Because the rubric counts its life until the Real's launch (Jul 1, 1994) as 41 months, it scores high on durability even though inflation surged again in 1992 (1,119.10%) and 1993 (2,477.15%). Its high score partly rides the Real's success - a rubric artifact worth flagging to readers.
- ipca_before 1,620.97% -> ipca_after 472.70%; months_lasted 41; score = 0.7009.

### Also scored (below top 3)
- Plano Collor I (March 16, 1990; announced after the Mar 15 inauguration; MP 168/Lei 8.024, https://www.planalto.gov.br/ccivil_03/leis/l8024.htm): cut IPCA from 1,972.91% (1989) to 472.70% (1990), but could not hold it. Collor II arrived Jan 31, 1991. months_lasted 10; score = 0.5848.
- Plano Bresser (June 12, 1987; DL 2.335, https://www.planalto.gov.br/ccivil_03/decreto-lei/del2335.htm): rubric terms are before 1986 = 79.66% and after 1988 = 980.21% - inflation rose sharply after Bresser. months to Verao (Jan 15, 1989) = 19; score = 0.095.
- Plano Verao (January 15, 1989; MP 32/Lei 7.730, https://www.planalto.gov.br/ccivil_03/leis/l7730.htm): before 1988 = 980.21%, after 1990 = 1,620.97% - inflation rose, score_drop = 0. months to Collor I (Mar 16, 1990) = 14; score = 0.07.

## Editor's bottom line
Only the Real did what it promised: permanent disinflation at roughly 1% of the prior year's rate, and it stuck. Cruzado bought a year of relief and failed publicly; Collor I cut the rate but could not hold it; Collor II's third place is partly a rubric artifact of its durability window reaching the Real. Bresser and Verao made things worse within their own windows.

## Method and caveats
- IPCA figures are IBGE annual (Dec-Dec) rates, pulled and cross-checked from the IBGE API (URL above).
- Launch dates come from Planalto decrees/laws and the BCB chronology (URLs above).
- Collor I signed Mar 15 and announced Mar 16, 1990; scored as Mar 16. Real scored at its currency launch (Jul 1, 1994), the BCB convention. "Whole calendar months" per rubric.
- Scores computed exactly per rubric: Real 0.9937, Cruzado 0.7698, Collor II 0.7009, Collor I 0.5848, Bresser 0.095, Verao 0.07 (script output preserved in session; see result.json).