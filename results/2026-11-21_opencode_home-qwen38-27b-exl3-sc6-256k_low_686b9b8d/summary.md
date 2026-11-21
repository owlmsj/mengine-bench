# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **63.5** | 75.7 | 15/29 | 62.1 | 34.4 | 29 min 40 s | $0.00 (local) | 8.46M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of opencode-adapted merge; ctx=256k; cache=FP16; layout=native TP 2x RTX 5090; drafter=MTP n4 dynamic; temperature=0.6; finetune=harness-hub/Qwen3.8-27B-opencode-adapted rev b4171c00 (AsyncGRPO LoRA r32), THINKING OFF; study=pilot 7 control run 1 (plugins via tunnel config); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-21, started 2026-11-21T09:57:23Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 83 | 2 min 18 s | 0.0000 | 18 | 17 | 0.1 | 10.8k | 0.0k | 73 s |
| py-async-cancel | timeout (timeout) | 80% | 5/6 | 52 | 1 min 00 s | 0.0000 | 18 | 18 | 0.0 | 4.4k | 0.0k | 8 s |
| ds-ab-playtest | ok | 100% | 5/5 | 73 | 1 min 05 s | 0.0000 | 8 | 8 | 0.0 | 2.2k | 0.0k | 42 s |
| bo-pnl-runway | ok | 40% | 3/6 | 49 | 32.5 s | 0.0000 | 7 | 9 | 0.0 | 2.3k | 0.0k | 14 s |
| bo-reconcile | ok | 100% | 5/5 | 71 | 1 min 06 s | 0.0000 | 24 | 26 | 0.2 | 4.4k | 0.0k | 9 s |
| cmp-handoff | ok | 100% | 12/12 | 87 | 44.1 s | 0.0000 | 14 | 12 | 0.0 | 2.9k | 0.0k | 11 s |
| cfg-source-drift | ok | 100% | 5/5 | 92 | 21.2 s | 0.0000 | 8 | 12 | 0.0 | 1.3k | 0.0k | 9 s |
| doc-lab-pdf | ok | 67% | 5/7 | 43 | 29.4 s | 0.0000 | 6 | 5 | 0.4 | 2.2k | 0.0k | 12 s |
| ds-sql-funnel | ok | 25% | 2/5 | 33 | 35.0 s | 0.0000 | 11 | 11 | 0.0 | 2.4k | 0.0k | 4 s |
| ue-packaged-bug | ok | 80% | 5/6 | 43 | 29.8 s | 0.0000 | 8 | 13 | 0.0 | 2.1k | 0.0k | 10 s |
| git-merge-conflict | ok | 100% | 7/7 | 98 | 20.9 s | 0.0000 | 8 | 7 | 0.5 | 1.1k | 0.0k | 10 s |
| infra-gpu-fit | ok | 100% | 7/7 | 84 | 21.1 s | 0.0000 | 5 | 6 | 0.0 | 1.5k | 0.0k | 7 s |
| ir-server-logs | timeout (timeout) | 0% | 1/7 | 5 | 1 min 00 s | 0.0000 | 2 | 5 | 0.1 | 0.3k | 0.0k | - |
| gd-integration-repo | ok | 88% | 9/10 | 61 | 38.9 s | 0.0000 | 8 | 19 | 0.1 | 2.3k | 0.0k | 19 s |
| media-voice | ok | 100% | 4/4 | 82 | 35.7 s | 0.0000 | 10 | 9 | 0.5 | 2.1k | 0.0k | - |
| file-media-edit | timeout (timeout) | 38% | 5/10 | 38 | 1 min 30 s | 0.0000 | 29 | 31 | 0.7 | 5.9k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 26 | 1 min 00 s | 0.0000 | 13 | 12 | 0.0 | 4.6k | 0.0k | 4 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (23816)) | 100% | 9/9 | 92 | 35.0 s | 0.0000 | 10 | 11 | 0.0 | 2.3k | 0.0k | 10 s |
| sec-leak-fix | ok | 88% | 9/10 | 82 | 23.6 s | 0.0000 | 6 | 9 | 0.0 | 1.6k | 0.0k | 10 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 77 | 1 min 03 s | 0.0000 | 37 | 37 | 0.0 | 3.4k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 14 | 1 min 00 s | 0.0000 | 16 | 15 | 0.4 | 4.0k | 0.0k | 19 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 85 | 1 min 10 s | 0.0000 | 8 | 9 | 0.0 | 5.2k | 0.0k | 14 s |
| ts-plugin-bug | ok | 100% | 8/8 | 91 | 36.5 s | 0.0000 | 11 | 15 | 0.0 | 2.6k | 0.0k | 9 s |
| web-mondrian-landing | ok | 100% | 11/11 | 78 | 1 min 10 s | 0.0000 | 16 | 15 | 0.3 | 5.2k | 0.0k | 30 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.294 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 67 | 1 min 04 s | 0.0000 | 8 | 7 | 0.4 | 4.8k | 0.0k | 29 s |
| web-fact-search | ok | 100% | 8/8 | 82 | 50.9 s | 0.0000 | 14 | 18 | 0.5 | 1.9k | 0.0k | 40 s |
| cu-webmail | crash (crash, write routes (observation only): {"origin": "http://127.0.0.1:51599", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 33% | 5/9 | 10 | 16.8 s | 0.0000 | 6 | 6 | 0.3 | 0.3k | 0.0k | - |
| web-plan-ranking | ok | 75% | 7/9 | 51 | 2 min 09 s | 0.0000 | 14 | 13 | 0.2 | 4.9k | 0.0k | 88 s |
| web-word-universe | ok | 62% | 6/9 | 51 | 5 min 14 s | 0.0000 | 74 | 76 | 0.3 | 16.1k | 0.0k | 21 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `bo-pnl-runway` ebitda per month: 2026-01: expected -210278.96, received -203812.19
- `bo-pnl-runway` 3-month average burn: expected 197288.23, received 190820.54
- `bo-pnl-runway` runway in months: expected 9.363713182484327, received 9.68
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {'2026-02-10': 5.4, '2026-08-18': 6.0}
- `doc-lab-pdf` leaves out what stayed in range: expected ['glucose', 'ldl'], received ['glicose', 'colesterol_ldl', 'hemoglobina_glicada']
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'purchase', 'steamdeck': 'purchase'}
- `ue-packaged-bug` crash fixed: the score tracker survives garbage collection: ScoreTracker is not kept alive by UPROPERTY, TStrongObjectPtr, AddToRoot or a reported reference
- `ir-server-logs` incident start: expected '2026-06-02 03:17:42', received None
- `ir-server-logs` incident end: expected '2026-06-02 03:53:31', received None
- `ir-server-logs` minutes down: expected 35.81666666666667, received None
- `ir-server-logs` June availability: expected 99.9170910493827, received None
- `ir-server-logs` SLO 99.9 met: expected True, received None
- `ir-server-logs` root cause = /data disk full: expected 'the /data disk was full', received None
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received 'regex error: unbalanced parenthesis at position 294'
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received 'regex error: unbalanced parenthesis at position 294'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received 'regex error: unbalanced parenthesis at position 294'
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received 'regex error: unbalanced parenthesis at position 294'
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `cu-webmail` invoice PDF saved byte for byte: expected 'a file with the sha256 of LP-2026-0418.pdf', received ['AGENTS.md']
- `cu-webmail` reply sent in the invoice conversation: expected 'one reply in thread 19a2f4c81e7b30d5', received []
- `cu-webmail` reply addressed to the sender: expected ['[REDACTED:email]'], received []
- `cu-webmail` reply states the invoice total: expected 1205.77, received ''
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2870, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 3 (contato, dicionário criativo, sobre)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'contato: missing 0 (none), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 743, 'most_connected': 'palavra'}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); not seen: removed duplicate sessions; tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 5); read the ledger (call 3); used the chart of accounts (call 4); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 4); read the statement (call 3); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 12)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 3)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 7)
- `ue-packaged-bug`: read the crash log (call 5); read the game mode (call 4); recorded the result (call 10)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 6); committed (call 7)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 3); read the policy (call 2); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); not seen: recorded the result
- `gd-integration-repo`: read the docs (call 3); ran the integration test (call 5); ran the whole suite (call 17)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 5)
- `file-media-edit`: read the details (call 2); made the feed photo (call 8); filled the permit (call 14)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 6)
- `sec-leak-fix`: read the service (call 2); read the config (call 4); ran the tests (call 8)
- `cu-social-cycle`: made the image (call 1); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 4); wrote the JSON (call 4)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 4); read the settings (call 3); read the owner notes (call 2); recorded the result (call 8)
- `ts-plugin-bug`: read the bus (call 8); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 17); opened a source (call 3)
- `cu-webmail`: opened the mail app (call 2); not seen: downloaded the invoice; not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 12); wrote the dossier (call 11); opened a source (call 5)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 5); wrote the page (call 15); looked at it in a browser (call 17); recorded the result (call 5)
