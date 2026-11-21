# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **59.2** | 73.9 | 17/29 | 63.5 | 0.0 | 45 min 29 s | $0.00 (local) | 3.05M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of super-adapter merge; ctx=256k; cache=FP16; layout=native TP 2x RTX 5090; drafter=MTP n4 dynamic; temperature=0.6; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715 (pi+hermes+opencode at 1/2), thinking low (enable_thinking true, OpenCode #low); study=pilot 7 control: super-adapter low run 2; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-21, started 2026-11-21T14:59:52Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | timeout (timeout) | 0% | 1/5 | 0 | 5 min 00 s | 0.0000 | 1 | 0 | - | - | - | - |
| py-async-cancel | timeout (timeout) | 80% | 5/6 | 59 | 1 min 00 s | 0.0000 | 3 | 3 | 0.0 | 4.3k | 0.0k | 43 s |
| ds-ab-playtest | ok | 100% | 5/5 | 80 | 1 min 19 s | 0.0000 | 6 | 6 | 0.0 | 3.4k | 0.0k | 50 s |
| bo-pnl-runway | ok | 100% | 6/6 | 73 | 1 min 19 s | 0.0000 | 10 | 12 | 0.0 | 6.6k | 0.0k | 17 s |
| bo-reconcile | ok | 100% | 5/5 | 75 | 51.9 s | 0.0000 | 5 | 6 | 0.0 | 4.9k | 0.0k | 34 s |
| cmp-handoff | ok | 100% | 12/12 | 88 | 45.2 s | 0.0000 | 7 | 6 | 0.0 | 3.4k | 0.0k | 17 s |
| cfg-source-drift | ok | 100% | 5/5 | 93 | 31.6 s | 0.0000 | 8 | 12 | 0.0 | 2.2k | 0.0k | 15 s |
| doc-lab-pdf | ok | 100% | 7/7 | 80 | 48.6 s | 0.0000 | 7 | 6 | 0.5 | 4.0k | 0.0k | 33 s |
| ds-sql-funnel | ok | 25% | 2/5 | 40 | 42.8 s | 0.0000 | 8 | 8 | 0.2 | 3.3k | 0.0k | 5 s |
| ue-packaged-bug | ok | 100% | 6/6 | 91 | 47.8 s | 0.0000 | 7 | 16 | 0.0 | 4.0k | 0.0k | 34 s |
| git-merge-conflict | ok | 100% | 7/7 | 98 | 40.6 s | 0.0000 | 11 | 10 | 0.5 | 2.6k | 0.0k | 23 s |
| infra-gpu-fit | ok | 100% | 7/7 | 83 | 29.4 s | 0.0000 | 6 | 7 | 0.0 | 2.3k | 0.0k | 11 s |
| ir-server-logs | timeout (timeout) | 0% | 1/7 | 8 | 1 min 00 s | 0.0000 | 3 | 5 | 0.0 | 0.5k | 0.0k | - |
| gd-integration-repo | ok | 88% | 9/10 | 66 | 59.0 s | 0.0000 | 11 | 24 | 0.0 | 4.7k | 0.0k | 45 s |
| media-voice | ok | 100% | 4/4 | 80 | 30.4 s | 0.0000 | 4 | 3 | 0.4 | 2.3k | 0.0k | - |
| file-media-edit | timeout (timeout) | 100% | 10/10 | 79 | 1 min 30 s | 0.0000 | 12 | 15 | 0.5 | 7.0k | 0.0k | 73 s |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 0 | 1 min 00 s | 0.0000 | 1 | 0 | - | - | - | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (28648)) | 100% | 9/9 | 93 | 57.5 s | 0.0000 | 8 | 11 | 0.0 | 4.4k | 0.0k | 30 s |
| sec-leak-fix | ok | 88% | 9/10 | 79 | 56.6 s | 0.0000 | 6 | 9 | 0.0 | 4.5k | 0.0k | 42 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 93 | 1 min 20 s | 0.0000 | 24 | 24 | 0.1 | 3.8k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 6 | 1 min 00 s | 0.0000 | 3 | 2 | 0.5 | 1.0k | 0.0k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 86 | 1 min 08 s | 0.0000 | 11 | 10 | 0.4 | 4.5k | 0.0k | 28 s |
| ts-plugin-bug | ok | 100% | 8/8 | 95 | 49.7 s | 0.0000 | 9 | 13 | 0.0 | 3.7k | 0.0k | 17 s |
| web-mondrian-landing | ok | 100% | 11/11 | 88 | 3 min 23 s | 0.0000 | 12 | 11 | 0.0 | 16.5k | 0.0k | 90 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.339 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 57 | 4 min 35 s | 0.0000 | 11 | 10 | 0.6 | 22.1k | 0.0k | 126 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 12 | 1 min 00 s | 0.0000 | 5 | 6 | 0.5 | 0.9k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:61899", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 84 | 1 min 35 s | 0.0000 | 24 | 24 | 0.4 | 6.4k | 0.0k | - |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 6 | 3 min 30 s | 0.0000 | 5 | 7 | 0.2 | 10.8k | 0.0k | - |
| web-word-universe | timeout (timeout) | 62% | 6/9 | 49 | 6 min 00 s | 0.0000 | 31 | 33 | 0.1 | 27.8k | 0.0k | 43 s |

## Failed checks

- `web-archery-game` index.html exists with content
- `web-archery-game` takes the mouse: press and release
- `web-archery-game` makes its own sound
- `web-archery-game` needs nothing beside the page: expected [], received []
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'purchase', 'steamdeck': 'purchase'}
- `ir-server-logs` incident start: expected '2026-06-02 03:17:42', received None
- `ir-server-logs` incident end: expected '2026-06-02 03:53:31', received None
- `ir-server-logs` minutes down: expected 35.81666666666667, received None
- `ir-server-logs` June availability: expected 99.9170910493827, received None
- `ir-server-logs` SLO 99.9 met: expected True, received None
- `ir-server-logs` root cause = /data disk full: expected 'the /data disk was full', received None
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received 'no pattern in regex.txt'
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received 'no pattern in regex.txt'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received 'no pattern in regex.txt'
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received 'no pattern in regex.txt'
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
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
- `web-plan-ranking` all six plans recorded: expected ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real'], received []
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor I': ['1990-03-16'], 'Collor II': ['1991-01-31'], 'Real': ['1994-03-01', '1994-07-01']}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1], 'Real': [2477.15, 22.41]}, received {'Cruzado': [None, None], 'Bresser': [None, None], 'Verao': [None, None], 'Collor I': [None, None], 'Collor
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Verao': [14], 'Collor I': [10], 'Collor II': [37, 41], 'Real': [60]}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` scores follow the rubric: expected "0.7*drop + 0.3*durability from the row's own numbers", received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received None
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 0, 'urls': 0, 'plans': []}
- `web-word-universe` collected exactly the site's words: missing 52 (aflição, almoço, amanhã, angústia, açougueiro), extra 57 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acento: missing 1 (sílaba), extra 1 (silaba)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 255, 'relations': 750, 'most_connected': 'palavra'}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: not seen: wrote the game; not seen: looked at it in a browser
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 2); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 3); used the cash balance (call 4); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 3); recorded the result (call 6)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 9); read the game mode (call 10); recorded the result (call 12)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 8); committed (call 9)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); not seen: recorded the result
- `gd-integration-repo`: read the docs (call 5); ran the integration test (call 9); ran the whole suite (call 24)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 8); filled the permit (call 12)
- `txt-regex-log`: not seen: wrote the regex; not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 7)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 5); read the settings (call 3); read the owner notes (call 3); recorded the result (call 8)
- `ts-plugin-bug`: read the bus (call 7); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 4); recorded the result (call 3)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 1)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 8); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: recorded the result; not seen: wrote the dossier; opened a source (call 2)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 6); wrote the page (call 19); looked at it in a browser (call 21); recorded the result (call 6)
