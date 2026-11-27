# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (off)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **75.8** | 86.6 | 19/29 | 69.4 | 63.2 | 21 min 02 s | >= $0.00 | 5.24M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-27, started 2026-11-27T14:22:53Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 64 | 1 min 33 s | 0.0000 | 23 | 22 | 0.0 | 10.0k | 0.0k | 28 s |
| py-async-cancel | ok | 100% | 6/6 | 82 | 25.5 s | 0.0000 | 10 | 10 | 0.0 | 2.3k | 0.0k | 3 s |
| ds-ab-playtest | ok | 100% | 5/5 | 91 | 40.8 s | 0.0000 | 6 | 6 | 0.0 | 1.6k | 0.0k | 32 s |
| bo-pnl-runway | ok | 100% | 6/6 | 69 | 20.6 s | 0.0000 | 6 | 8 | 0.0 | 2.1k | 0.0k | 8 s |
| bo-reconcile | ok | 100% | 5/5 | 88 | 19.8 s | 0.0000 | 9 | 10 | 0.0 | 1.9k | 0.0k | 6 s |
| cmp-handoff | ok | 91% | 11/12 | 66 | 29.4 s | 0.0000 | 13 | 11 | 0.0 | 2.7k | 0.0k | 7 s |
| cfg-source-drift | ok | 100% | 5/5 | 94 | 15.2 s | 0.0000 | 7 | 11 | 0.1 | 1.4k | 0.0k | 5 s |
| doc-lab-pdf | ok | 100% | 7/7 | 76 | 24.9 s | 0.0000 | 11 | 10 | 0.2 | 2.4k | 0.0k | 11 s |
| ds-sql-funnel | ok | 25% | 2/5 | 32 | 37.9 s | 0.0000 | 16 | 16 | 0.2 | 4.6k | 0.0k | 2 s |
| ue-packaged-bug | ok | 100% | 6/6 | 91 | 17.8 s | 0.0000 | 5 | 11 | 0.0 | 1.8k | 0.0k | 9 s |
| git-merge-conflict | ok | 100% | 7/7 | 93 | 16.8 s | 0.0000 | 8 | 7 | 0.4 | 1.2k | 0.0k | 8 s |
| infra-gpu-fit | ok | 100% | 7/7 | 87 | 13.2 s | 0.0000 | 5 | 6 | 0.0 | 1.3k | 0.0k | 5 s |
| ir-server-logs | ok | 100% | 7/7 | 92 | 36.1 s | 0.0000 | 8 | 8 | 0.0 | 1.6k | 0.0k | 28 s |
| gd-integration-repo | timeout (timeout) | 100% | 10/10 | 42 | 2 min 30 s | - | 96 | 107 | 0.3 | 14.3k | 0.0k | 15 s |
| media-voice | ok | 100% | 4/4 | 74 | 38.5 s | 0.0000 | 11 | 10 | 0.6 | 2.3k | 0.0k | 16 s |
| file-media-edit | ok | 88% | 9/10 | 49 | 45.3 s | 0.0000 | 17 | 17 | 0.5 | 3.7k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 23 | 1 min 00 s | - | 28 | 27 | 0.3 | 7.5k | 0.0k | 3 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (16680)) | 83% | 8/9 | 57 | 25.3 s | 0.0000 | 11 | 14 | 0.0 | 2.5k | 0.0k | 7 s |
| sec-leak-fix | ok | 88% | 9/10 | 73 | 16.2 s | 0.0000 | 7 | 10 | 0.0 | 1.6k | 0.0k | 7 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 87 | 32.3 s | 0.0000 | 26 | 26 | 0.0 | 2.4k | 0.0k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 68 | 45.3 s | 0.0000 | 18 | 17 | 0.3 | 4.0k | 0.0k | 13 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 89 | 21.2 s | 0.0000 | 9 | 9 | 0.3 | 1.9k | 0.0k | 13 s |
| ts-plugin-bug | ok | 100% | 8/8 | 95 | 27.9 s | 0.0000 | 11 | 15 | 0.0 | 3.0k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 78 | 48.2 s | 0.0000 | 15 | 14 | 0.0 | 5.8k | 0.0k | 23 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.379 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 51 | 1 min 28 s | 0.0000 | 18 | 18 | 0.0 | 11.1k | 0.0k | 21 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 16 | 1 min 00 s | - | 19 | 26 | 0.4 | 2.2k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:52456", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 87 | 54.5 s | 0.0000 | 27 | 26 | 0.0 | 4.3k | 0.0k | 24 s |
| web-plan-ranking | ok | 75% | 7/9 | 58 | 1 min 14 s | 0.0000 | 11 | 10 | 0.2 | 4.9k | 0.0k | 45 s |
| web-word-universe | ok | 62% | 6/9 | 42 | 1 min 24 s | 0.0000 | 18 | 19 | 0.4 | 8.5k | 0.0k | 14 s |

## Failed checks

- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received 'scripts/start_server.ps1 (local9 block) with --no-mmproj-offload -ub 512, Ctx 131072, 1024 predict'
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 282}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 67}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'tutorial_complete', 'steamdeck': 'tutorial_complete'}
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received ['2026-02-11', '198.18.7.9 fetched build 2025-08-14', 'relay 172.31.4.4 and 172.31.4.5 agreed on 2024-06-30', 'window 2023-04-01', 'rotated 2022-12-25', 'probe 0.0.0.0
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received ['203.0.113.200 ok 2024-09-09', 'peer 10.1.2.3 dropped 2025-01-23']
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received ['node 10.8.0.9 restarted 2023-09-30', 'node 10.8.0.10 restarted 2023-10-31']
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received ['agent 10.0.9.5 ran 2024-03-18', 'user 3307-15-0042 from 10.0.9.7 ok 2024-03-20']
- `rs-lock-bug` hidden a transfer to the same player changes nothing: expected 'a_transfer_to_the_same_player_changes_nothing passed', received False
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `web-fact-search` sqlite_3_40_0_release_date value: expected '2022-11-16', received None
- `web-fact-search` sqlite_3_40_0_release_date primary source: expected 'an http(s) URL on sqlite.org', received None
- `web-fact-search` postgresql_15_0_release_date value: expected '2022-10-13', received None
- `web-fact-search` postgresql_15_0_release_date primary source: expected 'an http(s) URL on postgresql.org', received None
- `web-fact-search` unicode_15_0_characters_added value: expected 4489, received None
- `web-fact-search` unicode_15_0_characters_added primary source: expected 'an http(s) URL on unicode.org', received None
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2794, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'aflição: missing 2 (angústia, água), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 599, 'most_connected': {'word': 'palavra', 'degree': 9}}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=saudade does not show its 5 relations, missing carinho, esperança, nostalgia

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 5); read the ledger (call 3); used the chart of accounts (call 4); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 9)
- `cmp-handoff`: read the session (call 3); wrote the handoff (call 4); recorded the result (call 11)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 5)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 5); recorded the result (call 7)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 6); committed (call 6)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 7)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); not seen: ran the whole suite
- `media-voice`: used a speech engine (call 1); wrote the audio (call 4)
- `file-media-edit`: read the details (call 2); made the feed photo (call 5); filled the permit (call 9)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 3); read the config (call 2); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 4); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 5); read the settings (call 3); read the owner notes (call 2); recorded the result (call 8)
- `ts-plugin-bug`: read the bus (call 6); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 3); recorded the result (call 1)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 8); wrote the dossier (call 7); not seen: opened a source
- `web-word-universe`: walked the site (call 1); wrote words.json (call 5); wrote the page (call 9); looked at it in a browser (call 12); recorded the result (call 5)
