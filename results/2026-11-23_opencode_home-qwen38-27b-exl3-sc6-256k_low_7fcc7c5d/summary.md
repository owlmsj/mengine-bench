# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **74.1** | 83.2 | 20/29 | 69.0 | 66.8 | 19 min 58 s | $0.00 (local) | 5.07M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715, THINKING OFF; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of super-adapter merge; cache=FP16; drafter=MTP n4 dynamic; layout=native TP 2x RTX 5090; sampling=temperature 0.65 (forced), top_k 20, top_p 0.95; study=temperature 0.65, binary search 0.6-0.7 (mengine#1090, 2026-11-23); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-23, started 2026-11-23T13:49:29Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 69 | 1 min 04 s | 0.0000 | 14 | 13 | 0.4 | 6.7k | 0.0k | 28 s |
| py-async-cancel | timeout (timeout) | 80% | 5/6 | 44 | 1 min 00 s | 0.0000 | 8 | 7 | 0.0 | 2.7k | 0.0k | 3 s |
| ds-ab-playtest | ok | 100% | 5/5 | 87 | 43.6 s | 0.0000 | 7 | 7 | 0.0 | 1.9k | 0.0k | 31 s |
| bo-pnl-runway | ok | 100% | 6/6 | 85 | 26.4 s | 0.0000 | 9 | 11 | 0.0 | 2.7k | 0.0k | 10 s |
| bo-reconcile | ok | 100% | 5/5 | 79 | 18.5 s | 0.0000 | 8 | 9 | 0.0 | 1.8k | 0.0k | 6 s |
| cmp-handoff | ok | 100% | 12/12 | 81 | 32.3 s | 0.0000 | 15 | 13 | 0.0 | 3.4k | 0.0k | 7 s |
| cfg-source-drift | ok | 100% | 5/5 | 96 | 15.3 s | 0.0000 | 8 | 11 | 0.0 | 1.4k | 0.0k | 6 s |
| doc-lab-pdf | ok | 100% | 7/7 | 80 | 21.6 s | 0.0000 | 10 | 9 | 0.0 | 2.4k | 0.0k | 5 s |
| ds-sql-funnel | ok | 100% | 5/5 | 85 | 31.1 s | 0.0000 | 12 | 12 | 0.0 | 3.7k | 0.0k | 3 s |
| ue-packaged-bug | ok | 100% | 6/6 | 89 | 18.9 s | 0.0000 | 5 | 12 | 0.0 | 2.0k | 0.0k | 10 s |
| git-merge-conflict | ok | 100% | 7/7 | 86 | 20.8 s | 0.0000 | 12 | 12 | 0.2 | 1.8k | 0.0k | 4 s |
| infra-gpu-fit | ok | 100% | 7/7 | 77 | 14.9 s | 0.0000 | 5 | 6 | 0.0 | 1.6k | 0.0k | 7 s |
| ir-server-logs | ok | 100% | 7/7 | 87 | 41.1 s | 0.0000 | 9 | 10 | 0.0 | 2.0k | 0.0k | 29 s |
| gd-integration-repo | ok | 75% | 8/10 | 54 | 28.1 s | 0.0000 | 14 | 28 | 0.0 | 3.2k | 0.0k | 16 s |
| media-voice | ok | 100% | 4/4 | 77 | 31.6 s | 0.0000 | 11 | 10 | 0.5 | 1.9k | 0.0k | - |
| file-media-edit | ok | 38% | 5/10 | 38 | 44.5 s | 0.0000 | 16 | 16 | 0.5 | 4.1k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 27 | 1 min 00 s | 0.0000 | 16 | 15 | 0.0 | 7.9k | 0.0k | 4 s |
| rs-lock-bug | ok | 100% | 9/9 | 82 | 19.4 s | 0.0000 | 8 | 11 | 0.0 | 1.8k | 0.0k | 7 s |
| sec-leak-fix | ok | 75% | 8/10 | 78 | 17.7 s | 0.0000 | 9 | 11 | 0.0 | 1.9k | 0.0k | 5 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 87 | 38.3 s | 0.0000 | 27 | 27 | 0.0 | 3.0k | 0.0k | 4 s |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 23 | 1 min 00 s | 0.0000 | 21 | 20 | 0.2 | 5.9k | 0.0k | 14 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 75 | 40.6 s | 0.0000 | 8 | 9 | 0.0 | 2.7k | 0.0k | 11 s |
| ts-plugin-bug | ok | 100% | 8/8 | 96 | 21.0 s | 0.0000 | 9 | 13 | 0.0 | 2.2k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 78 | 30.1 s | 0.0000 | 9 | 8 | 0.0 | 3.7k | 0.0k | 15 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.139 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 45 | 1 min 33 s | 0.0000 | 19 | 18 | 0.2 | 11.8k | 0.0k | 25 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 12 | 1 min 00 s | 0.0000 | 19 | 24 | 0.9 | 1.9k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:62503", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 81 | 1 min 07 s | 0.0000 | 32 | 32 | 0.0 | 6.9k | 0.0k | 29 s |
| web-plan-ranking | ok | 75% | 7/9 | 55 | 1 min 23 s | 0.0000 | 10 | 9 | 0.0 | 4.1k | 0.0k | 60 s |
| web-word-universe | ok | 50% | 5/9 | 47 | 1 min 34 s | 0.0000 | 28 | 29 | 0.0 | 11.7k | 0.0k | 8 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `gd-integration-repo` hidden half up tie rounds up: FAIL: test_half_up_tie_rounds_up (test_hidden_gold.Hidden.test_half_up_tie_rounds_up) | AssertionError: 1420 != 1430
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received ['2026-02-11', '198.18.7.9 fetched build 2025-08-14 then 2025-10-02', 'relay 172.31.4.4 and 172.31.4.5 agreed on 2024-06-30', 'window 2023-04-01', 'rotated 2022-12-25 k
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received ['203.0.113.200 ok 2024-09-09', 'peer 10.1.2.3 dropped 2025-01-23']
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received ['node 10.8.0.8 restarted 2023-02-29', 'node 10.8.0.9 restarted 2023-09-30', 'node 10.8.0.10 restarted 2023-10-31']
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received ['agent 10.0.9.5 ran 2024-03-18', 'user 3307-15-0042 from 10.0.9.7 ok 2024-03-20']
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `sec-leak-fix` the old token is out of the final answers: the token literal appears in answer(s) [0]; expected it in none
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
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2709, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 52 (aflição, almoço, amanhã, angústia, açougueiro), extra 60 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acento: missing 1 (sílaba), extra 1 (silaba)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 258, 'relations': 764, 'most_connected': 'tempo'}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=saudade does not show its 5 relations, missing esperança

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 7); tested significance (call 4); recorded the result (call 6)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 3); wrote the handoff (call 4); recorded the result (call 13)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 5); read the game mode (call 6); recorded the result (call 8)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 11); committed (call 10)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 6)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 7)
- `gd-integration-repo`: read the docs (call 3); ran the integration test (call 8); ran the whole suite (call 24)
- `media-voice`: used a speech engine (call 2); wrote the audio (call 9)
- `file-media-edit`: read the details (call 2); made the feed photo (call 6); filled the permit (call 8)
- `txt-regex-log`: wrote the regex (call 3); tried it in Python (call 5)
- `rs-lock-bug`: read the crate (call 7); ran the tests (call 9)
- `sec-leak-fix`: read the service (call 3); read the config (call 2); ran the tests (call 10)
- `cu-social-cycle`: made the image (call 1); opened the site (call 4); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 5); read the settings (call 3); read the owner notes (call 2); recorded the result (call 8)
- `ts-plugin-bug`: read the bus (call 7); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 4); recorded the result (call 3)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 10); replied (call 26)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 8); wrote the dossier (call 7); not seen: opened a source
- `web-word-universe`: walked the site (call 1); wrote words.json (call 4); wrote the page (call 7); looked at it in a browser (call 12); recorded the result (call 4)
