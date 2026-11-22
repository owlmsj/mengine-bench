# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **63.0** | 76.9 | 19/29 | 66.3 | 12.0 | 36 min 25 s | $0.00 (local) | 5.60M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; runtime=SGLang lmsysorg/sglang:latest; quant=super-adapter merge in FP8 (ModelOpt 0.47 FP8 e4m3 on all linears; vision/MTP/lm_head/DeltaNet in_proj_a,b BF16); ctx=256k; cache=fp8_e4m3; layout=TP 2x RTX 5090, chunked prefill 4096, mem-fraction-static 0.80; drafter=DFlash2 incoai (base-trained), 8 drafts; clock_cap=2900 MHz both GPUs; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715, THINKING OFF; study=super-adapter FP8 vs NVFP4 vs EXL3 (2026-11-22): fp8 run 1; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-22, started 2026-11-22T12:37:03Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 80 | 4 min 00 s | 0.0000 | 21 | 20 | 0.5 | 27.5k | 18.8k | 119 s |
| py-async-cancel | timeout (timeout, retried once: the first attempt got no reply from the model before its limit) | 0% | 1/6 | 0 | 1 min 00 s | 0.0000 | 1 | 0 | - | - | - | - |
| ds-ab-playtest | ok | 100% | 5/5 | 82 | 1 min 12 s | 0.0000 | 13 | 13 | 0.9 | 6.0k | 2.3k | 35 s |
| bo-pnl-runway | ok | 100% | 6/6 | 78 | 38.4 s | 0.0000 | 10 | 9 | 0.5 | 4.0k | 1.8k | 13 s |
| bo-reconcile | ok | 100% | 5/5 | 77 | 31.3 s | 0.0000 | 8 | 9 | 0.4 | 4.0k | 2.2k | 12 s |
| cmp-handoff | ok | 100% | 12/12 | 86 | 49.7 s | 0.0000 | 10 | 9 | 0.7 | 5.9k | 3.2k | 20 s |
| cfg-source-drift | ok | 100% | 5/5 | 94 | 16.4 s | 0.0000 | 6 | 10 | 0.7 | 1.6k | 0.3k | 6 s |
| doc-lab-pdf | ok | 100% | 7/7 | 78 | 29.5 s | 0.0000 | 6 | 5 | 0.6 | 3.8k | 2.2k | 19 s |
| ds-sql-funnel | ok | 50% | 3/5 | 41 | 35.9 s | 0.0000 | 13 | 13 | 0.6 | 4.3k | 1.5k | 3 s |
| ue-packaged-bug | ok | 100% | 6/6 | 85 | 1 min 13 s | 0.0000 | 7 | 14 | 0.7 | 8.5k | 6.4k | 56 s |
| git-merge-conflict | ok | 100% | 7/7 | 91 | 24.1 s | 0.0000 | 6 | 5 | 0.9 | 2.4k | 1.1k | 12 s |
| infra-gpu-fit | ok | 100% | 7/7 | 62 | 14.0 s | 0.0000 | 3 | 4 | 0.4 | 2.0k | 1.1k | 8 s |
| ir-server-logs | ok | 100% | 7/7 | 88 | 33.7 s | 0.0000 | 8 | 9 | 0.5 | 3.8k | 1.9k | 22 s |
| gd-integration-repo | ok | 88% | 9/10 | 73 | 38.6 s | 0.0000 | 7 | 16 | 0.8 | 4.4k | 2.3k | 25 s |
| media-voice | ok | 100% | 4/4 | 71 | 28.9 s | 0.0000 | 3 | 2 | 1.7 | 3.4k | 2.2k | - |
| file-media-edit | ok | 38% | 5/10 | 45 | 1 min 12 s | 0.0000 | 11 | 12 | 2.2 | 8.0k | 4.2k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 14 | 1 min 00 s | 0.0000 | 2 | 2 | 0.6 | 9.2k | 8.9k | 54 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (16456)) | 100% | 9/9 | 90 | 1 min 22 s | 0.0000 | 10 | 14 | 1.4 | 10.2k | 6.5k | 49 s |
| sec-leak-fix | ok | 100% | 10/10 | 95 | 33.7 s | 0.0000 | 8 | 11 | 0.5 | 3.7k | 1.9k | 16 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 90 | 1 min 08 s | 0.0000 | 31 | 33 | 0.2 | 6.7k | 3.1k | 8 s |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 5 | 1 min 00 s | 0.0000 | 4 | 3 | 1.5 | 1.0k | 0.3k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 83 | 47.6 s | 0.0000 | 11 | 12 | 0.7 | 5.2k | 2.8k | 18 s |
| ts-plugin-bug | ok | 100% | 8/8 | 92 | 39.5 s | 0.0000 | 11 | 14 | 0.7 | 4.0k | 1.2k | 10 s |
| web-mondrian-landing | ok | 100% | 11/11 | 82 | 1 min 49 s | 0.0000 | 12 | 11 | 0.5 | 13.7k | 7.4k | 64 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.296 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 80% | 10/12 | 61 | 5 min 12 s | 0.0000 | 16 | 26 | 1.3 | 38.2k | 29.1k | 138 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 17 | 1 min 00 s | 0.0000 | 6 | 12 | 1.0 | 4.4k | 3.5k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:60661", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 84 | 1 min 11 s | 0.0000 | 23 | 22 | 0.2 | 7.1k | 3.5k | - |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 14 | 3 min 30 s | 0.0000 | 9 | 14 | 0.9 | 15.9k | 12.9k | 157 s |
| web-word-universe | ok | 75% | 7/9 | 65 | 2 min 53 s | 0.0000 | 22 | 24 | 1.0 | 21.0k | 10.1k | 32 s |

## Failed checks

- `py-async-cancel` jobs run side by side up to the limit: expected {'started': 2, 'finished': 2, 'cleaned': 2, 'peak': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` never more jobs at once than the limit: expected {'started': 2, 'finished': 2, 'cleaned': 2, 'peak': 1}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C below the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C at the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 268}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 60}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received ['2026-02-11 sync from 10.20.30.40 ok', '198.18.7.9 fetched build 2025-08-14 then 2025-10-02', 'relay 172.31.4.4 and 172.31.4.5 agreed on 2024-06-30', 'window 2023-04-0
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received ['203.0.113.200 ok 2024-09-09', 'peer 10.1.2.3 dropped 2025-01-23']
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received ['node 10.8.0.8 restarted 2023-02-29', 'node 10.8.0.9 restarted 2023-09-30', 'node 10.8.0.10 restarted 2023-10-31']
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received ['agent 10.0.9.2 tag v2024-03-16 pushed', 'agent 10.0.9.4 order 12024-03-17 placed', 'agent 10.0.9.5 ran 2024-03-18 fine', 'user 3307-15-0042 from 10.0.9.7 ok 2024-03-20']
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `3d-print-homage` counted the boats in the print: expected 3, received None
- `3d-print-homage` named the mountain: expected 'Mount Fuji', received None
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
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'avó: missing 1 (avô), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 742, 'most_connected': 'tempo'}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: not seen: wrote run.py; not seen: ran it
- `ds-ab-playtest`: read the notes (call 3); read the data (call 2); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 10)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 2); used the chart of accounts (call 2); used the cash balance (call 2); recorded the result (call 3)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 4); recorded the result (call 9)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); not seen: extracted the text; recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 5); recorded the result (call 8)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 5); committed (call 5)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 3); read the policy (call 2); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 8)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); ran the whole suite (call 16)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 6); filled the permit (call 7)
- `txt-regex-log`: wrote the regex (call 2); not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 14)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 10)
- `cu-social-cycle`: made the image (call 2); opened the site (call 8); not seen: deleted the test post
- `ds-sqlite-recover`: not seen: read the raw bytes; not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 5); read the settings (call 4); read the owner notes (call 3); recorded the result (call 12)
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 8); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: recorded the result; not seen: wrote the dossier; opened a source (call 2)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 4); wrote the page (call 18); looked at it in a browser (call 17); recorded the result (call 4)
