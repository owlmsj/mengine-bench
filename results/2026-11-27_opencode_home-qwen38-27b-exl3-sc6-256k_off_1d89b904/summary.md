# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (off)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **76.4** | 84.3 | 19/29 | 69.1 | 79.3 | 16 min 13 s | >= $0.00 | 4.31M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-27, started 2026-11-27T16:07:33Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 83% | 7/8 | 57 | 49.7 s | 0.0000 | 11 | 10 | 0.1 | 6.2k | 0.0k | 25 s |
| py-async-cancel | timeout (timeout) | 80% | 5/6 | 42 | 1 min 00 s | - | 9 | 8 | 0.0 | 2.2k | 0.0k | 2 s |
| ds-ab-playtest | ok | 100% | 5/5 | 82 | 37.8 s | 0.0000 | 6 | 6 | 0.0 | 1.4k | 0.0k | 29 s |
| bo-pnl-runway | ok | 100% | 6/6 | 82 | 26.1 s | 0.0000 | 13 | 15 | 0.0 | 2.8k | 0.0k | 8 s |
| bo-reconcile | ok | 100% | 5/5 | 86 | 17.5 s | 0.0000 | 8 | 9 | 0.0 | 1.8k | 0.0k | 6 s |
| cmp-handoff | ok | 100% | 12/12 | 78 | 38.6 s | 0.0000 | 20 | 18 | 0.0 | 4.3k | 0.0k | 6 s |
| cfg-source-drift | ok | 100% | 5/5 | 89 | 15.7 s | 0.0000 | 9 | 12 | 0.0 | 1.6k | 0.0k | 6 s |
| doc-lab-pdf | ok | 100% | 7/7 | 80 | 19.4 s | 0.0000 | 9 | 8 | 0.2 | 2.1k | 0.0k | 7 s |
| ds-sql-funnel | ok | 25% | 2/5 | 28 | 27.6 s | 0.0000 | 13 | 13 | 0.0 | 3.1k | 0.0k | 2 s |
| ue-packaged-bug | ok | 100% | 6/6 | 82 | 19.8 s | 0.0000 | 8 | 14 | 0.0 | 2.1k | 0.0k | 8 s |
| git-merge-conflict | ok | 100% | 7/7 | 90 | 13.5 s | 0.0000 | 7 | 6 | 0.4 | 0.9k | 0.0k | 7 s |
| infra-gpu-fit | ok | 100% | 7/7 | 84 | 13.1 s | 0.0000 | 5 | 6 | 0.0 | 1.4k | 0.0k | 5 s |
| ir-server-logs | ok | 100% | 7/7 | 84 | 37.7 s | 0.0000 | 10 | 10 | 0.0 | 1.9k | 0.0k | 23 s |
| gd-integration-repo | ok | 88% | 9/10 | 61 | 28.5 s | 0.0000 | 9 | 19 | 0.0 | 2.5k | 0.0k | 13 s |
| media-voice | ok | 100% | 4/4 | 84 | 19.0 s | 0.0000 | 8 | 7 | 0.3 | 1.9k | 0.0k | 11 s |
| file-media-edit | ok | 62% | 7/10 | 35 | 24.9 s | 0.0000 | 10 | 11 | 0.4 | 2.9k | 0.0k | 10 s |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 17 | 1 min 00 s | - | 29 | 28 | 0.0 | 8.9k | 0.0k | 3 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (9672)) | 100% | 9/9 | 93 | 23.5 s | 0.0000 | 10 | 12 | 0.0 | 2.4k | 0.0k | 6 s |
| sec-leak-fix | ok | 88% | 9/10 | 77 | 15.1 s | 0.0000 | 8 | 11 | 0.0 | 1.5k | 0.0k | 5 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 85 | 29.0 s | 0.0000 | 27 | 27 | 0.0 | 2.2k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 14 | 1 min 00 s | - | 13 | 12 | 0.3 | 7.7k | 0.0k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 81 | 23.4 s | 0.0000 | 9 | 14 | 0.0 | 2.2k | 0.0k | 10 s |
| ts-plugin-bug | ok | 100% | 8/8 | 100 | 21.8 s | 0.0000 | 9 | 13 | 0.0 | 2.4k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 79 | 30.1 s | 0.0000 | 8 | 7 | 0.4 | 3.6k | 0.0k | 13 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.589 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 50 | 1 min 01 s | 0.0000 | 12 | 11 | 0.0 | 7.9k | 0.0k | 2 s |
| web-fact-search | ok | 100% | 8/8 | 86 | 32.9 s | 0.0000 | 9 | 11 | 0.2 | 1.4k | 0.0k | 20 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:56674", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 82 | 40.0 s | 0.0000 | 23 | 22 | 0.0 | 3.6k | 0.0k | - |
| web-plan-ranking | ok | 50% | 5/9 | 44 | 1 min 03 s | 0.0000 | 12 | 11 | 0.0 | 4.3k | 0.0k | 5 s |
| web-word-universe | ok | 50% | 5/9 | 51 | 1 min 03 s | 0.0000 | 12 | 12 | 0.2 | 7.3k | 0.0k | 14 s |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'purchase', 'steamdeck': 'purchase'}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` balloon fully in frame and undistorted: expected 'a round, whole balloon', received {'bbox': (286, 278, 794, 1073), 'size': (1080, 1350), 'width/height': 0.64, 'fill': 0.78}
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received 'Saturday 5 December 2026'
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received ['2026-02-11', '198.18.7.9 fetched build 2025-08-14', 'relay 172.31.4.4 and 172.31.4.5 agreed on 2024-06-30', 'window 2023-04-01', 'rotated 2022-12-25', 'probe 0.0.0.0
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received ['203.0.113.200 ok 2024-09-09', 'peer 10.1.2.3 dropped 2025-01-23']
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received ['node 10.8.0.8 restarted 2023-02-29', 'node 10.8.0.9 restarted 2023-09-30', 'node 10.8.0.10 restarted 2023-10-31']
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received ['agent 10.0.9.5 ran 2024-03-18', 'user 3307-15-0042 from 10.0.9.7 ok 2024-03-20']
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor II': ['1991-01-31']}, received {'Cruzado': '1986-02-15', 'Bresser': '1987-02-15', 'Verao': '1989-03-15', 'Collor II': '1991-03-15'}
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Verao': [14], 'Collor I': [10], 'Collor II': [37, 41]}, received {'Cruzado': 12, 'Bresser': 25, 'Verao': 12, 'Collor I': 12, 'Collor II': 35}
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2395, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 62 (aflição, almoço, amanhã, angústia, avó), extra 63 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acento: missing 1 (sílaba), extra 1 (silaba)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 251, 'relations': 743, 'most_connected': {'word': 'palavra', 'count': 16}}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 4)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 4); used the chart of accounts (call 5); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 18)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 4); recorded the result (call 11)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 6); committed (call 6)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 2); read the policy (call 3); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); ran the whole suite (call 16)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 2)
- `file-media-edit`: read the details (call 2); made the feed photo (call 6); filled the permit (call 6)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 10)
- `cu-social-cycle`: made the image (call 1); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); wrote the JSON (call 8)
- `hw-stutter-tuning`: read the frame capture (call 8); read the sensor log (call 9); read the settings (call 4); read the owner notes (call 3); recorded the result (call 13)
- `ts-plugin-bug`: read the bus (call 7); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 3); recorded the result (call 1)
- `web-fact-search`: not seen: searched the web; recorded the result (call 10); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 8); replied (call 18)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 10); wrote the dossier (call 9); not seen: opened a source
- `web-word-universe`: walked the site (call 1); wrote words.json (call 4); wrote the page (call 8); looked at it in a browser (call 10); recorded the result (call 4)
