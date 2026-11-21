# Editor dossier: which stabilization plans delivered?

## Finding

The rubric puts **Real (1994)** first, followed by **Collor I (1990)** and **Collor II (1991)**. Real is the clear outlier: annual IPCA falls from 2,477.15% in the year before launch to 9.56% in the year after, and receives the rubric’s full 60-month durability allowance. These annual figures are December-to-December IPCA attributed to IBGE/SNIPC in [Ipeadata’s annual series](https://www.ipeadata.gov.br/ExibeSerie.aspx?module=M&serid=1410807112); Real began in July 1994 according to the [Banco Central history](https://www.bcb.gov.br/controleinflacao/30anosreal?modalAberto=30anosreal_noticia2).

## Ranked results

1. **Real (1994), 0.9993.** 2,477.15% before versus 9.56% after, with 60 months credited. [IPCA values](https://www.ipeadata.gov.br/ExibeSerie.aspx?module=M&serid=1410807112); [launch history](https://www.bcb.gov.br/controleinflacao/30anosreal?modalAberto=30anosreal_noticia2).
2. **Collor I (1990), 0.6981.** 1,972.91% before versus 472.70% after, but only 10 months to Collor II. [IPCA values](https://www.ipeadata.gov.br/ExibeSerie.aspx?module=M&serid=1410807112); [BCB research chronology](https://www.bcb.gov.br/pre/sobre/PremioBCB/1_PriceSetting_JuliaAraujoMauroRodrigues.pdf).
3. **Collor II (1991), 0.4380.** 1,620.97% before versus 1,119.10% after, with 42 months to Real. [IPCA values](https://www.ipeadata.gov.br/ExibeSerie.aspx?module=M&serid=1410807112); [BCB plan chronology](https://www.bcb.gov.br/content/publicacoes/notastecnicas/Nota_tecnica_49_jan_2019.pdf).

## Method and caveats

I applied the formula exactly: `0.7 × clamp(1 − after/before, 0, 1) + 0.3 × min(months, 60)/60`. For launch dates I use exact dates in Banco Central’s chronology when stated; the official BCB technical note gives month and year for all plans. Months lasted are counted by calendar month, so day-level differences do not affect the duration. Real gets 60 months as directed. This is a mechanical association, not causal proof: the year-after measure reflects other policies and shocks too. Cruzado II intervened between Cruzado and Bresser, but is not a scored plan in the supplied rubric.

The machine-readable inputs and source URL list for all six plans are in [result.json](./result.json).

