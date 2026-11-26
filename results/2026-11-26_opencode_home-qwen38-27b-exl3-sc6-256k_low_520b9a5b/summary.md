# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **71.8** | 79.1 | 17/29 | 66.7 | 74.9 | 17 min 32 s | $0.00 (local) | 5.84M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of pilot7-b-dpo (step-15) on pilot7-a1-sft merge; cache=FP16; drafter=MTP n4 dynamic; layout=native TP 2x RTX 5090; temperature=0.6; finetune=pilot7-b-dpo (step-15, val 0.6484, acc 66.7%, margin +0.106) on pilot7-a1-sft, THINKING OFF; study=mengine-qlora#42 pilot 7 B DPO eval run 2; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-26, started 2026-11-26T21:56:19Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 77 | 55.9 s | 0.0000 | 12 | 11 | 0.2 | 7.0k | 0.0k | 30 s |
| py-async-cancel | ok | 100% | 6/6 | 69 | 49.1 s | 0.0000 | 15 | 14 | 0.9 | 5.5k | 0.0k | 5 s |
| ds-ab-playtest | ok | 100% | 5/5 | 89 | 44.6 s | 0.0000 | 6 | 6 | 0.0 | 2.1k | 0.0k | 34 s |
| bo-pnl-runway | ok | 40% | 3/6 | 52 | 19.0 s | 0.0000 | 6 | 8 | 0.0 | 2.1k | 0.0k | 8 s |
| bo-reconcile | ok | 100% | 5/5 | 77 | 19.6 s | 0.0000 | 9 | 10 | 0.0 | 1.9k | 0.0k | 6 s |
| cmp-handoff | ok | 100% | 12/12 | 87 | 33.7 s | 0.0000 | 15 | 13 | 0.0 | 3.5k | 0.0k | 7 s |
| cfg-source-drift | ok | 100% | 5/5 | 90 | 17.7 s | 0.0000 | 9 | 12 | 0.0 | 1.6k | 0.0k | 8 s |
| doc-lab-pdf | ok | 100% | 7/7 | 76 | 15.1 s | 0.0000 | 5 | 4 | 0.4 | 1.6k | 0.0k | 8 s |
| ds-sql-funnel | ok | 25% | 2/5 | 39 | 19.3 s | 0.0000 | 8 | 8 | 0.2 | 2.1k | 0.0k | 2 s |
| ue-packaged-bug | ok | 100% | 6/6 | 91 | 16.7 s | 0.0000 | 6 | 10 | 0.0 | 1.8k | 0.0k | 6 s |
| git-merge-conflict | ok | 0% | 5/7 | 22 | 15.6 s | 0.0000 | 8 | 7 | 0.4 | 1.3k | 0.0k | 4 s |
| infra-gpu-fit | ok | 100% | 7/7 | 83 | 12.6 s | 0.0000 | 4 | 5 | 0.0 | 1.3k | 0.0k | 4 s |
| ir-server-logs | ok | 100% | 7/7 | 84 | 17.8 s | 0.0000 | 8 | 7 | 0.0 | 1.7k | 0.0k | 9 s |
| gd-integration-repo | ok | 88% | 9/10 | 69 | 31.6 s | 0.0000 | 11 | 20 | 0.1 | 3.1k | 0.0k | 12 s |
| media-voice | ok | 100% | 4/4 | 56 | 46.7 s | 0.0000 | 15 | 14 | 0.3 | 3.1k | 0.0k | 7 s |
| file-media-edit | crash (crash) | 0% | 0/0 | 60 | - | 0.0000 | 0 | 0 | - | - | - | - |
| txt-regex-log | ok | 0% | 1/5 | 10 | 43.1 s | 0.0000 | 3 | 2 | 0.0 | 7.9k | 0.0k | 2 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (16568)) | 100% | 9/9 | 94 | 21.7 s | 0.0000 | 8 | 9 | 0.0 | 2.4k | 0.0k | 7 s |
| sec-leak-fix | ok | 88% | 9/10 | 80 | 15.5 s | 0.0000 | 7 | 10 | 0.0 | 1.7k | 0.0k | 7 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 84 | 32.2 s | 0.0000 | 26 | 26 | 0.0 | 2.4k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 100% | 6/6 | 66 | 1 min 00 s | 0.0000 | 21 | 20 | 0.2 | 6.4k | 0.0k | 15 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 73 | 23.6 s | 0.0000 | 8 | 9 | 0.0 | 2.3k | 0.0k | 11 s |
| ts-plugin-bug | ok | 100% | 8/8 | 98 | 15.3 s | 0.0000 | 5 | 8 | 0.0 | 1.4k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 70 | 56.8 s | 0.0000 | 14 | 13 | 0.0 | 7.3k | 0.0k | 22 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.079 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 90% | 11/12 | 37 | 49.5 s | 0.0000 | 11 | 10 | 0.2 | 5.6k | 0.0k | 19 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 13 | 1 min 00 s | 0.0000 | 29 | 33 | 0.0 | 3.1k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:57920", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 80 | 29.1 s | 0.0000 | 19 | 19 | 0.0 | 1.9k | 0.0k | - |
| web-plan-ranking | ok | 75% | 7/9 | 51 | 1 min 14 s | 0.0000 | 10 | 9 | 0.0 | 5.3k | 0.0k | 48 s |
| web-word-universe | ok | 88% | 8/9 | 57 | 2 min 36 s | 0.0000 | 64 | 68 | 0.0 | 14.7k | 0.0k | 15 s |

## Failed checks

- `bo-pnl-runway` ebitda per month: 2026-01: expected -210278.96, received -203812.19
- `bo-pnl-runway` 3-month average burn: expected 197288.23, received 190820.54
- `bo-pnl-runway` runway in months: expected 9.363713182484327, received 9.68
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'purchase', 'steamdeck': 'purchase'}
- `git-merge-conflict` visible tests left untouched
- `git-merge-conflict` main is a merge commit of the old main and the branch: expected "a merge in main's ancestry with parents ['1fd1a0574f6f43fdb28ac67cbaf7f8aa7e874fb8', 'b24e86bca76d6922a26109b3561fc797f6a5b718']", received []
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received ['2019-05-31']
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received ['2025-01-27']
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received ['2023-10-31']
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received ['2024-03-20']
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `3d-print-homage` counted the boats in the print: expected 3, received 9
- `web-fact-search` sqlite_3_40_0_release_date value: expected '2022-11-16', received None
- `web-fact-search` sqlite_3_40_0_release_date primary source: expected 'an http(s) URL on sqlite.org', received None
- `web-fact-search` postgresql_15_0_release_date value: expected '2022-10-13', received None
- `web-fact-search` postgresql_15_0_release_date primary source: expected 'an http(s) URL on postgresql.org', received None
- `web-fact-search` unicode_15_0_characters_added value: expected 4489, received None
- `web-fact-search` unicode_15_0_characters_added primary source: expected 'an http(s) URL on unicode.org', received None
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor II': ['1991-01-31']}, received {'Cruzado': '1986-02-01', 'Bresser': '1987-02-01', 'Verao': '1989-03-15', 'Collor II': '1991-03-15'}
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Verao': [14], 'Collor I': [10]}, received {'Cruzado': 12, 'Bresser': 25, 'Verao': 12, 'Collor I': 12}
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 668, 'most_connected': 'palavra'}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 2)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 2); not seen: removed duplicate sessions; tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 4); read the ledger (call 3); used the chart of accounts (call 5); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 4); read the invoices (call 3); read the statement (call 2); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 12)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 3)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 4); recorded the result (call 8)
- `git-merge-conflict`: not seen: merged the branch; ran the tests (call 4); committed (call 5)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 2); read the policy (call 3); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); not seen: ran the whole suite
- `media-voice`: used a speech engine (call 1); wrote the audio (call 11)
- `file-media-edit`: not seen: read the details; not seen: made the feed photo; not seen: filled the permit
- `txt-regex-log`: wrote the regex (call 2); not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 6)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 4); read the settings (call 3); read the owner notes (call 2); recorded the result (call 8)
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 7); wrote the dossier (call 8); opened a source (call 4)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 5); wrote the page (call 12); looked at it in a browser (call 20); recorded the result (call 5)
