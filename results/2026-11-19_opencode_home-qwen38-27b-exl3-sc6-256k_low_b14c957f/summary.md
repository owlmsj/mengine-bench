# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **71.0** | 82.3 | 16/29 | 62.8 | 63.4 | 20 min 59 s | >= $0.00 | 6.15M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; model=Qwen3.8-27B; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of opencode-adapted merge; ctx=256k; cache=FP16; layout=native TP 2x RTX 5090; drafter=MTP n4 dynamic; tier=2; temperature=0.6; finetune=harness-hub/Qwen3.8-27B-opencode-adapted rev b4171c00 (AsyncGRPO LoRA r32), THINKING OFF (Tabby enable_thinking false); mengine=2.9.0 installed; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-19, started 2026-11-19T17:46:55Z; bench at ac16be22ea10 (dirty tree); submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 75 | 1 min 39 s | 0.0000 | 22 | 21 | 0.4 | 8.9k | 0.0k | 0 s |
| py-async-cancel | ok | 80% | 5/6 | 58 | 51.8 s | 0.0000 | 20 | 19 | 0.0 | 6.0k | 0.0k | 0 s |
| ds-ab-playtest | ok | 100% | 5/5 | 72 | 41.4 s | 0.0000 | 8 | 8 | 0.0 | 1.5k | 0.0k | 30 s |
| bo-pnl-runway | ok | 100% | 6/6 | 79 | 27.2 s | 0.0000 | 11 | 12 | 0.0 | 3.3k | 0.0k | 10 s |
| bo-reconcile | ok | 75% | 4/5 | 45 | 12.9 s | 0.0000 | 6 | 7 | 0.0 | 1.2k | 0.0k | 4 s |
| cmp-handoff | ok | 91% | 11/12 | 54 | 23.3 s | 0.0000 | 9 | 8 | 0.0 | 2.2k | 0.0k | 5 s |
| cfg-source-drift | ok | 100% | 5/5 | 91 | 10.2 s | 0.0000 | 6 | 7 | 0.0 | 0.7k | 0.0k | 3 s |
| doc-lab-pdf | ok | 100% | 7/7 | 58 | 18.2 s | 0.0000 | 8 | 7 | 0.0 | 2.0k | 0.0k | 5 s |
| ds-sql-funnel | ok | 100% | 5/5 | 83 | 14.3 s | 0.0000 | 7 | 7 | 0.3 | 1.3k | 0.0k | 4 s |
| ue-packaged-bug | ok | 100% | 6/6 | 78 | 19.3 s | 0.0000 | 7 | 11 | 0.0 | 2.1k | 0.0k | 5 s |
| git-merge-conflict | ok | 100% | 7/7 | 89 | 14.5 s | 0.0000 | 8 | 7 | 0.4 | 1.1k | 0.0k | 6 s |
| infra-gpu-fit | ok | 50% | 4/7 | 28 | 10.7 s | 0.0000 | 5 | 6 | 0.0 | 1.0k | 0.0k | 2 s |
| ir-server-logs | ok | 83% | 6/7 | 42 | 31.7 s | 0.0000 | 6 | 6 | 0.0 | 1.4k | 0.0k | 21 s |
| gd-integration-repo | ok | 88% | 9/10 | 66 | 21.8 s | 0.0000 | 8 | 18 | 0.0 | 2.0k | 0.0k | 11 s |
| media-voice | ok | 100% | 4/4 | 79 | 14.7 s | 0.0000 | 8 | 7 | 0.7 | 0.9k | 0.0k | 6 s |
| file-media-edit | ok | 75% | 8/10 | 50 | 45.8 s | 0.0000 | 26 | 27 | 0.4 | 4.4k | 0.0k | 6 s |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 14 | 1 min 00 s | - | 7 | 6 | 0.0 | 10.2k | 0.0k | 2 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (28380)) | 100% | 9/9 | 90 | 30.9 s | 0.0000 | 14 | 16 | 0.0 | 3.6k | 0.0k | 8 s |
| sec-leak-fix | ok | 88% | 9/10 | 78 | 12.7 s | 0.0000 | 6 | 10 | 0.0 | 1.1k | 0.0k | 5 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 89% | 10/11 | 54 | 45.0 s | 0.0000 | 35 | 34 | 0.0 | 2.2k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 18 | 1 min 00 s | - | 21 | 20 | 0.3 | 6.7k | 0.0k | 7 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 83 | 25.1 s | 0.0000 | 11 | 12 | 0.4 | 2.3k | 0.0k | 15 s |
| ts-plugin-bug | ok | 100% | 8/8 | 95 | 15.0 s | 0.0000 | 7 | 11 | 0.0 | 1.4k | 0.0k | 5 s |
| web-mondrian-landing | ok | 100% | 11/11 | 78 | 25.4 s | 0.0000 | 10 | 9 | 0.0 | 3.0k | 0.0k | 11 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.382 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 54 | 1 min 37 s | 0.0000 | 16 | 15 | 0.0 | 14.1k | 0.0k | 22 s |
| web-fact-search | ok | 100% | 8/8 | 73 | 54.2 s | 0.0000 | 17 | 22 | 0.4 | 2.3k | 0.0k | 41 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:55968", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 80 | 51.4 s | 0.0000 | 33 | 32 | 0.2 | 5.0k | 0.0k | - |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 4 | 3 min 30 s | - | 69 | 73 | 0.1 | 16.1k | 0.0k | - |
| web-word-universe | ok | 50% | 5/9 | 53 | 1 min 56 s | 0.0000 | 40 | 40 | 0.0 | 12.0k | 0.0k | 7 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `bo-reconcile` unpaid invoices: expected ['INV-1008', 'INV-1030', 'INV-1033'], received ['INV-1008', 'INV-1030']
- `cmp-handoff` summary exists and fits in 1000 characters: 1066 characters
- `infra-gpu-fit` cheapest feasible offer: expected 'of-117', received 'of-111'
- `infra-gpu-fit` hourly price: expected 3.58, received 2.98
- `infra-gpu-fit` monthly price: expected 2613.4, received 2175.4
- `ir-server-logs` June availability: expected 99.9170910493827, received 99.975
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received 'Saturday 5 December 2026'
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received []
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received []
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received []
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received []
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `cu-social-cycle` cover.png is a 1200x675 PNG: expected (1200, 675), received (1672, 941)
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `web-plan-ranking` all six plans recorded: expected ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real'], received []
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor I': ['1990-03-16'], 'Collor II': ['1991-01-31'], 'Real': ['1994-03-01', '1994-07-01']}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1], 'Real': [2477.15, 22.41]}, received {'Cruzado': [None, None], 'Bresser': [None, None], 'Verao': [None, None], 'Collor I': [None, None], 'Collor
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Verao': [14], 'Collor I': [10], 'Collor II': [37, 41], 'Real': [60]}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` scores follow the rubric: expected "0.7*drop + 0.3*durability from the row's own numbers", received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received None
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 0, 'urls': 0, 'plans': []}
- `web-word-universe` collected exactly the site's words: missing 62 (aflição, almoço, amanhã, angústia, avó), extra 62 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acento: missing 1 (sílaba), extra 1 (silaba)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 743, 'most_connected': 'tempo'}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=saudade does not show its 5 relations, missing esperança

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 3)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 4)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 2); not seen: removed duplicate sessions; tested significance (call 6); recorded the result (call 6)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 3); recorded the result (call 9)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 4); read the statement (call 3); recorded the result (call 5)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 3); recorded the result (call 6)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 3); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 6); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 5); read the game mode (call 4); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 4); ran the tests (call 6); committed (call 7)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 3); read the policy (call 2); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); ran the whole suite (call 16)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 3)
- `file-media-edit`: read the details (call 2); made the feed photo (call 8); filled the permit (call 9)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 11)
- `sec-leak-fix`: read the service (call 2); read the config (call 4); ran the tests (call 8)
- `cu-social-cycle`: made the image (call 3); opened the site (call 2); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 4); wrote the JSON (call 4)
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 6); read the settings (call 4); read the owner notes (call 3); recorded the result (call 10)
- `ts-plugin-bug`: read the bus (call 7); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 5); recorded the result (call 2)
- `web-fact-search`: searched the web (call 11); recorded the result (call 16); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 8); replied (call 26)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: recorded the result; not seen: wrote the dossier; opened a source (call 2)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 3); wrote the page (call 10); looked at it in a browser (call 13); recorded the result (call 3)
