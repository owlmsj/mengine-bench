# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/inkling-2-mini (high)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **72.9** | 92.2 | 24/29 | 73.2 | 8.7 | 37 min 23 s | $0.00 (local) | 9.20M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Inkling-2-Mini; runtime=SGLang lmsysorg/sglang:inkling-2-mini (0.0.0.dev1+inkling2); quant=native NVFP4 experts + MXFP8 (original release, rev ed40e7da); ctx=256k; cache=BF16; layout=TP 2x RTX 5090, fa4 attention; drafter=DSpark n8 (bundled mtp.safetensors); temperature=1.0 (model default); reasoning_effort=high; study=inkling 2 mini engine+quant pick, run 2; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-21, started 2026-11-21T16:46:58Z; bench at 8584f70e1346 (dirty tree); submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 80 | 4 min 46 s | 0.0000 | 41 | 40 | 2.0 | 37.0k | 15.1k | 62 s |
| py-async-cancel | ok | 100% | 6/6 | 84 | 43.3 s | 0.0000 | 12 | 11 | 0.4 | 10.2k | 5.7k | 18 s |
| ds-ab-playtest | ok | 100% | 5/5 | 82 | 39.1 s | 0.0000 | 19 | 18 | 0.4 | 8.4k | 4.0k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 65 | 33.0 s | 0.0000 | 23 | 22 | 0.3 | 6.5k | 2.7k | 9 s |
| bo-reconcile | ok | 100% | 5/5 | 76 | 17.9 s | 0.0000 | 8 | 7 | 0.4 | 3.7k | 2.4k | - |
| cmp-handoff | ok | 100% | 12/12 | 72 | 1 min 17 s | 0.0000 | 16 | 14 | 0.5 | 5.8k | 3.3k | 56 s |
| cfg-source-drift | ok | 100% | 5/5 | 88 | 14.8 s | 0.0000 | 10 | 9 | 0.4 | 1.9k | 0.9k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 81 | 55.4 s | 0.0000 | 12 | 12 | 0.4 | 4.5k | 3.2k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 80 | 23.2 s | 0.0000 | 15 | 14 | 0.4 | 4.5k | 1.8k | 12 s |
| ue-packaged-bug | ok | 100% | 6/6 | 79 | 51.8 s | 0.0000 | 16 | 15 | 0.4 | 10.4k | 9.3k | 38 s |
| git-merge-conflict | ok | 100% | 7/7 | 85 | 18.6 s | 0.0000 | 14 | 13 | 0.5 | 2.9k | 1.5k | 11 s |
| infra-gpu-fit | ok | 100% | 7/7 | 73 | 10.9 s | 0.0000 | 5 | 4 | 0.5 | 1.9k | 1.0k | - |
| ir-server-logs | ok | 100% | 7/7 | 85 | 17.7 s | 0.0000 | 10 | 9 | 0.4 | 2.3k | 1.2k | - |
| gd-integration-repo | ok | 88% | 9/10 | 50 | 41.2 s | 0.0000 | 27 | 26 | 0.4 | 6.6k | 5.0k | - |
| media-voice | ok | 100% | 4/4 | 82 | 19.4 s | 0.0000 | 12 | 11 | 0.5 | 2.6k | 1.2k | 8 s |
| file-media-edit | ok | 100% | 10/10 | 87 | 1 min 07 s | 0.0000 | 42 | 42 | 0.5 | 12.1k | 7.1k | 6 s |
| txt-regex-log | ok | 100% | 5/5 | 91 | 56.0 s | 0.0000 | 12 | 11 | 0.4 | 13.6k | 11.7k | 38 s |
| rs-lock-bug | ok | 100% | 9/9 | 93 | 19.1 s | 0.0000 | 9 | 8 | 0.5 | 3.4k | 1.3k | 10 s |
| sec-leak-fix | ok | 100% | 10/10 | 74 | 32.1 s | 0.0000 | 26 | 25 | 0.4 | 5.6k | 2.5k | 10 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 85 | 53.2 s | 0.0000 | 40 | 39 | 0.0 | 9.0k | 4.1k | 23 s |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 9 | 1 min 00 s | 0.0000 | 10 | 9 | 0.4 | 7.4k | 6.6k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 84 | 36.1 s | 0.0000 | 21 | 23 | 0.4 | 6.6k | 4.7k | 9 s |
| ts-plugin-bug | ok | 100% | 8/8 | 88 | 26.6 s | 0.0000 | 13 | 16 | 0.3 | 4.9k | 2.6k | 13 s |
| web-mondrian-landing | ok | 100% | 11/11 | 73 | 1 min 25 s | 0.0000 | 22 | 21 | 0.4 | 15.1k | 6.8k | 38 s |
| 3d-print-homage | timeout (timeout, blue-layout similarity to the print: 0.428 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 42 | 7 min 00 s | 0.0000 | 65 | 65 | 0.7 | 42.3k | 28.7k | 72 s |
| web-fact-search | ok | 100% | 8/8 | 87 | 29.7 s | 0.0000 | 10 | 11 | 0.4 | 2.1k | 1.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:62448", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 79 | 38.5 s | 0.0000 | 29 | 28 | 0.0 | 5.1k | 2.6k | - |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 8 | 3 min 30 s | 0.0000 | 31 | 32 | 0.2 | 13.6k | 11.5k | - |
| web-word-universe | timeout (timeout) | 88% | 8/9 | 61 | 6 min 00 s | 0.0000 | 76 | 75 | 0.4 | 93.4k | 29.9k | 38 s |

## Failed checks

- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
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
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 3); looked at it in a browser (call 4)
- `py-async-cancel`: wrote run.py (call 3); ran it (call 2)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 2); removed duplicate sessions (call 7); tested significance (call 18); recorded the result (call 18)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 4); used the chart of accounts (call 3); used the cash balance (call 3); recorded the result (call 13)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 3); read the statement (call 3); recorded the result (call 7)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 5); recorded the result (call 14)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 8); recorded the result (call 11)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 4); excluded test accounts (call 6); recorded the result (call 9)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 4); recorded the result (call 14)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 12); not seen: committed
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 9)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 3); ran the whole suite (call 5)
- `media-voice`: used a speech engine (call 4); wrote the audio (call 4)
- `file-media-edit`: read the details (call 2); made the feed photo (call 16); filled the permit (call 21)
- `txt-regex-log`: wrote the regex (call 6); tried it in Python (call 7)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 4)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 5)
- `cu-social-cycle`: made the image (call 8); opened the site (call 1); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 7); read the sensor log (call 6); read the settings (call 5); read the owner notes (call 2); recorded the result (call 22)
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 13)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 4); looked at it in a browser (call 5)
- `3d-print-homage`: wrote the scene (call 5); looked at it in a browser (call 7); recorded the result (call 6)
- `web-fact-search`: not seen: searched the web; recorded the result (call 11); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 3); downloaded the invoice (call 10); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 25); not seen: recorded the result; not seen: wrote the dossier; opened a source (call 3)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 17); wrote the page (call 63); looked at it in a browser (call 13); recorded the result (call 24)
