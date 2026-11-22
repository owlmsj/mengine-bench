# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **69.3** | 78.2 | 16/29 | 64.0 | 66.1 | 20 min 10 s | $0.00 (local) | 4.71M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715, THINKING OFF; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of super-adapter merge; cache=FP16; drafter=MTP n4 dynamic; layout=native TP 2x RTX 5090; study=top-2 consistency (2026-11-22): exl3 run 2; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-22, started 2026-11-22T11:01:12Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 83% | 7/8 | 55 | 1 min 15 s | 0.0000 | 16 | 15 | 0.4 | 8.0k | 0.0k | 35 s |
| py-async-cancel | ok | 80% | 5/6 | 46 | 32.3 s | 0.0000 | 10 | 9 | 0.7 | 3.3k | 0.0k | 2 s |
| ds-ab-playtest | ok | 100% | 5/5 | 87 | 47.2 s | 0.0000 | 8 | 8 | 0.0 | 2.4k | 0.0k | 33 s |
| bo-pnl-runway | ok | 40% | 3/6 | 46 | 26.7 s | 0.0000 | 9 | 12 | 0.0 | 2.7k | 0.0k | 9 s |
| bo-reconcile | ok | 100% | 5/5 | 85 | 16.9 s | 0.0000 | 6 | 7 | 0.0 | 1.7k | 0.0k | 7 s |
| cmp-handoff | ok | 100% | 12/12 | 84 | 31.6 s | 0.0000 | 15 | 13 | 0.0 | 2.9k | 0.0k | 8 s |
| cfg-source-drift | ok | 100% | 5/5 | 92 | 15.1 s | 0.0000 | 7 | 11 | 0.0 | 1.5k | 0.0k | 5 s |
| doc-lab-pdf | timeout (timeout) | 83% | 6/7 | 43 | 1 min 00 s | 0.0000 | 7 | 7 | 0.3 | 2.5k | 0.0k | 9 s |
| ds-sql-funnel | ok | 25% | 2/5 | 30 | 1 min 05 s | 0.0000 | 9 | 9 | 0.0 | 2.5k | 0.0k | 6 s |
| ue-packaged-bug | ok | 100% | 6/6 | 82 | 15.6 s | 0.0000 | 6 | 11 | 0.0 | 1.5k | 0.0k | 7 s |
| git-merge-conflict | ok | 100% | 7/7 | 93 | 14.0 s | 0.0000 | 7 | 6 | 0.5 | 1.0k | 0.0k | 5 s |
| infra-gpu-fit | ok | 100% | 7/7 | 86 | 13.0 s | 0.0000 | 4 | 5 | 0.1 | 1.3k | 0.0k | 4 s |
| ir-server-logs | ok | 100% | 7/7 | 89 | 40.6 s | 0.0000 | 10 | 10 | 0.0 | 2.0k | 0.0k | 27 s |
| gd-integration-repo | ok | 88% | 9/10 | 68 | 19.2 s | 0.0000 | 6 | 15 | 0.0 | 1.7k | 0.0k | 12 s |
| media-voice | ok | 100% | 4/4 | 83 | 19.1 s | 0.0000 | 10 | 10 | 0.5 | 1.5k | 0.0k | 6 s |
| file-media-edit | ok | 38% | 5/10 | 28 | 40.5 s | 0.0000 | 15 | 15 | 0.5 | 3.3k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 23 | 1 min 00 s | 0.0000 | 13 | 12 | 0.3 | 7.4k | 0.0k | 8 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (30392)) | 100% | 9/9 | 88 | 31.2 s | 0.0000 | 11 | 13 | 0.0 | 3.6k | 0.0k | 9 s |
| sec-leak-fix | ok | 88% | 9/10 | 76 | 17.0 s | 0.0000 | 8 | 10 | 0.0 | 1.7k | 0.0k | 5 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 77 | 55.8 s | 0.0000 | 41 | 43 | 0.0 | 4.5k | 0.0k | 4 s |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 10 | 1 min 00 s | 0.0000 | 11 | 10 | 0.3 | 5.8k | 0.0k | 29 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 73 | 24.4 s | 0.0000 | 8 | 9 | 0.0 | 2.4k | 0.0k | 15 s |
| ts-plugin-bug | ok | 100% | 8/8 | 97 | 20.7 s | 0.0000 | 8 | 12 | 0.0 | 2.2k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 74 | 54.8 s | 0.0000 | 15 | 14 | 0.0 | 7.3k | 0.0k | 25 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.377 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 44 | 1 min 05 s | 0.0000 | 10 | 9 | 0.3 | 8.3k | 0.0k | 24 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 6 | 1 min 00 s | 0.0000 | 19 | 23 | 1.2 | 2.0k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:52743", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 85 | 1 min 13 s | 0.0000 | 24 | 23 | 0.0 | 2.7k | 0.0k | - |
| web-plan-ranking | ok | 75% | 7/9 | 55 | 1 min 20 s | 0.0000 | 10 | 9 | 0.0 | 4.3k | 0.0k | 55 s |
| web-word-universe | ok | 50% | 5/9 | 51 | 1 min 16 s | 0.0000 | 21 | 21 | 0.0 | 9.0k | 0.0k | 7 s |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `bo-pnl-runway` ebitda per month: 2026-01: expected -210278.96, received -203812.19
- `bo-pnl-runway` 3-month average burn: expected 197288.23, received 190820.54
- `bo-pnl-runway` runway in months: expected 9.363713182484327, received 9.68
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {'2026-02-10': 5.4, '2026-08-18': 3.6}
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'purchase', 'steamdeck': 'purchase'}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received 'no pattern in regex.txt'
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received 'no pattern in regex.txt'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received 'no pattern in regex.txt'
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received 'no pattern in regex.txt'
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `web-fact-search` sqlite_3_40_0_release_date value: expected '2022-11-16', received None
- `web-fact-search` sqlite_3_40_0_release_date primary source: expected 'an http(s) URL on sqlite.org', received None
- `web-fact-search` postgresql_15_0_release_date value: expected '2022-10-13', received None
- `web-fact-search` postgresql_15_0_release_date primary source: expected 'an http(s) URL on postgresql.org', received None
- `web-fact-search` unicode_15_0_characters_added value: expected 4489, received None
- `web-fact-search` unicode_15_0_characters_added primary source: expected 'an http(s) URL on unicode.org', received None
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2750, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 2 (contato, sobre)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'aflição: missing 2 (angústia, água), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 252, 'relations': 669, 'most_connected': 'tempo'}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=saudade does not show its 5 relations, missing esperança

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 2)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 2); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 4); read the ledger (call 5); used the chart of accounts (call 2); used the cash balance (call 3); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 13)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 5); read the game mode (call 4); recorded the result (call 7)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 6); committed (call 5)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 2); read the policy (call 3); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); ran the whole suite (call 15)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 7)
- `file-media-edit`: read the details (call 2); made the feed photo (call 5); filled the permit (call 8)
- `txt-regex-log`: not seen: wrote the regex; tried it in Python (call 2)
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 5); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); wrote the JSON (call 5)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 4); read the settings (call 3); read the owner notes (call 2); recorded the result (call 8)
- `ts-plugin-bug`: read the bus (call 6); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 4); recorded the result (call 3)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 3)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); replied (call 16)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 8); wrote the dossier (call 7); not seen: opened a source
- `web-word-universe`: walked the site (call 1); wrote words.json (call 4); wrote the page (call 6); looked at it in a browser (call 10); recorded the result (call 4)
