# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **67.1** | 82.1 | 18/29 | 70.1 | 12.3 | 36 min 18 s | $0.00 (local) | 7.90M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715, THINKING OFF; runtime=SGLang lmsysorg/sglang:latest; quant=super-adapter merge, mixed NVFP4 (MLP NVFP4, attention + DeltaNet FP8); cache=fp8_e4m3; drafter=DFlash2 incoai (base-trained), 8 drafts; layout=TP 2x RTX 5090, chunked prefill 4096, mem-fraction-static 0.80; study=top-2 consistency (2026-11-22): sg run 3; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-22, started 2026-11-22T11:27:51Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 83% | 7/8 | 83 | 3 min 27 s | 0.0000 | 23 | 22 | 0.6 | 27.0k | 14.2k | 99 s |
| py-async-cancel | ok | 80% | 5/6 | 67 | 29.0 s | 0.0000 | 11 | 10 | 0.8 | 3.1k | 0.7k | 4 s |
| ds-ab-playtest | ok | 100% | 5/5 | 82 | 54.2 s | 0.0000 | 6 | 7 | 0.7 | 4.9k | 2.5k | 34 s |
| bo-pnl-runway | ok | 100% | 6/6 | 79 | 34.2 s | 0.0000 | 7 | 9 | 0.4 | 5.1k | 2.2k | 13 s |
| bo-reconcile | ok | 100% | 5/5 | 84 | 36.5 s | 0.0000 | 8 | 9 | 0.5 | 6.6k | 4.5k | 16 s |
| cmp-handoff | ok | 100% | 12/12 | 88 | 29.3 s | 0.0000 | 8 | 6 | 0.7 | 3.8k | 1.8k | 14 s |
| cfg-source-drift | ok | 100% | 5/5 | 93 | 15.3 s | 0.0000 | 6 | 7 | 0.5 | 1.7k | 0.5k | 8 s |
| doc-lab-pdf | ok | 67% | 5/7 | 52 | 18.6 s | 0.0000 | 5 | 4 | 0.7 | 2.5k | 1.4k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 82 | 28.2 s | 0.0000 | 11 | 11 | 0.8 | 3.7k | 1.2k | 3 s |
| ue-packaged-bug | ok | 100% | 6/6 | 95 | 59.3 s | 0.0000 | 6 | 11 | 0.5 | 8.4k | 6.4k | 46 s |
| git-merge-conflict | ok | 100% | 7/7 | 91 | 22.5 s | 0.0000 | 8 | 7 | 0.6 | 2.5k | 1.2k | 13 s |
| infra-gpu-fit | ok | 100% | 7/7 | 90 | 15.6 s | 0.0000 | 4 | 5 | 0.5 | 2.4k | 1.1k | 7 s |
| ir-server-logs | ok | 100% | 7/7 | 86 | 23.5 s | 0.0000 | 7 | 8 | 0.8 | 3.0k | 1.4k | 17 s |
| gd-integration-repo | ok | 88% | 9/10 | 70 | 37.8 s | 0.0000 | 6 | 6 | 1.3 | 5.3k | 3.4k | 26 s |
| media-voice | ok | 100% | 4/4 | 79 | 19.4 s | 0.0000 | 6 | 5 | 0.9 | 2.3k | 1.1k | - |
| file-media-edit | timeout (timeout) | 38% | 5/10 | 43 | 1 min 30 s | 0.0000 | 11 | 11 | 1.3 | 11.5k | 8.7k | 34 s |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 2 | 1 min 00 s | 0.0000 | 2 | 1 | 0.1 | 0.1k | 0.0k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (18104)) | 100% | 9/9 | 89 | 1 min 30 s | 0.0000 | 12 | 13 | 0.8 | 13.1k | 9.5k | 57 s |
| sec-leak-fix | ok | 75% | 8/10 | 78 | 40.5 s | 0.0000 | 8 | 12 | 0.4 | 5.6k | 4.0k | 20 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 84 | 49.9 s | 0.0000 | 26 | 27 | 0.1 | 5.4k | 2.5k | 7 s |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 8 | 1 min 00 s | 0.0000 | 4 | 3 | 1.2 | 5.1k | 4.6k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 87 | 1 min 05 s | 0.0000 | 10 | 11 | 0.7 | 8.4k | 5.5k | 22 s |
| ts-plugin-bug | ok | 100% | 8/8 | 97 | 31.6 s | 0.0000 | 9 | 12 | 0.6 | 4.2k | 1.5k | 11 s |
| web-mondrian-landing | ok | 100% | 11/11 | 82 | 1 min 54 s | 0.0000 | 9 | 8 | 0.2 | 18.7k | 13.5k | 85 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.393 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 57 | 5 min 20 s | 0.0000 | 19 | 18 | 1.5 | 45.1k | 34.7k | 147 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 10 | 1 min 00 s | 0.0000 | 9 | 13 | 0.6 | 4.0k | 2.8k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:61502", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 71 | 1 min 15 s | 0.0000 | 18 | 17 | 0.5 | 5.7k | 2.2k | - |
| web-plan-ranking | ok | 88% | 8/9 | 45 | 2 min 23 s | 0.0000 | 8 | 16 | 0.6 | 16.2k | 11.5k | 125 s |
| web-word-universe | ok | 62% | 6/9 | 60 | 5 min 50 s | 0.0000 | 51 | 55 | 1.1 | 40.6k | 20.6k | 25 s |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {'2026-02-10': 5.4, '2026-08-18': 5.82}
- `doc-lab-pdf` leaves out what stayed in range: expected ['glucose', 'ldl'], received ['Glicose em jejum (mg/dL)', 'Colesterol LDL (mg/dL)', 'Hemoglobina glicada HbA1c (%)']
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
- `sec-leak-fix` the old token is out of the final answers: the token literal appears in answer(s) [0]; expected it in none
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
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1], 'Real': [2477.15, 22.41]}, received {'Cruzado': [235.47, 180.25], 'Bresser': [76.45, 145.55], 'Verao': [145.55, 1422.58], 'Collor I': [2039.32,
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'avó: missing 2 (avô, pai), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 734, 'most_connected': 'tempo'}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 2); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 5); read the ledger (call 3); used the chart of accounts (call 4); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 9)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 6)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 3)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 5); read the game mode (call 4); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 4); ran the tests (call 6); not seen: committed
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 2); recorded the result (call 8)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 2); ran the whole suite (call 6)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 2)
- `file-media-edit`: read the details (call 2); made the feed photo (call 4); filled the permit (call 6)
- `txt-regex-log`: not seen: wrote the regex; not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 7)
- `sec-leak-fix`: read the service (call 4); read the config (call 2); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 5); not seen: deleted the test post
- `ds-sqlite-recover`: not seen: read the raw bytes; not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 5); read the settings (call 2); read the owner notes (call 3); recorded the result (call 10)
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 1)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); replied (call 11)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 14); wrote the dossier (call 13); opened a source (call 4)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 10); wrote the page (call 16); looked at it in a browser (call 21); recorded the result (call 10)
