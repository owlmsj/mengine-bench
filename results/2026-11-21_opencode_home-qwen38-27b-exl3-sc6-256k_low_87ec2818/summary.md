# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **66.5** | 82.9 | 21/29 | 70.4 | 2.9 | 39 min 07 s | $0.00 (local) | 6.35M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; runtime=SGLang lmsysorg/sglang:latest; quant=nvidia/Qwen3.8-27B-NVFP4 (ModelOpt W4A4 MLP + FP8 attention), base model, no fine-tune; ctx=256k; cache=fp8_e4m3; layout=TP 2x RTX 5090, flashinfer attention, chunked prefill 4096, mem-fraction-static 0.80; drafter=DFlash2 incoai/Qwen3.8-27B-DFlash2, 12 drafts; temperature=model generation_config; clock_cap=2900 MHz both GPUs; thinking=LOW (server default enable_thinking true, OpenCode #low); study=engine speed A/B: tuned fastest 27B config, thinking low; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-21, started 2026-11-22T01:51:23Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | timeout (timeout) | 83% | 7/8 | 66 | 5 min 00 s | 0.0000 | 1 | 1 | 48.6 | 45.5k | 34.5k | 291 s |
| py-async-cancel | timeout (timeout) | 0% | 1/6 | 0 | 1 min 00 s | 0.0000 | 1 | 0 | - | - | - | - |
| ds-ab-playtest | ok | 100% | 5/5 | 93 | 57.3 s | 0.0000 | 6 | 6 | 0.4 | 4.7k | 2.6k | 39 s |
| bo-pnl-runway | ok | 100% | 6/6 | 72 | 59.0 s | 0.0000 | 8 | 10 | 0.5 | 8.5k | 4.6k | 19 s |
| bo-reconcile | ok | 100% | 5/5 | 88 | 49.2 s | 0.0000 | 8 | 10 | 0.4 | 7.8k | 5.5k | 21 s |
| cmp-handoff | ok | 100% | 12/12 | 88 | 1 min 10 s | 0.0000 | 17 | 17 | 0.7 | 10.5k | 6.9k | 17 s |
| cfg-source-drift | ok | 100% | 5/5 | 100 | 26.2 s | 0.0000 | 6 | 10 | 0.7 | 3.4k | 1.9k | 14 s |
| doc-lab-pdf | ok | 100% | 7/7 | 77 | 24.1 s | 0.0000 | 6 | 5 | 0.6 | 3.7k | 1.4k | 11 s |
| ds-sql-funnel | ok | 100% | 5/5 | 69 | 21.1 s | 0.0000 | 8 | 8 | 0.6 | 2.6k | 0.9k | 4 s |
| ue-packaged-bug | ok | 100% | 6/6 | 89 | 46.7 s | 0.0000 | 5 | 11 | 0.9 | 6.8k | 4.4k | 33 s |
| git-merge-conflict | ok | 100% | 7/7 | 96 | 38.6 s | 0.0000 | 8 | 8 | 0.7 | 5.0k | 3.5k | 28 s |
| infra-gpu-fit | ok | 100% | 7/7 | 86 | 19.6 s | 0.0000 | 5 | 6 | 0.3 | 2.8k | 1.2k | 9 s |
| ir-server-logs | ok | 100% | 7/7 | 85 | 26.7 s | 0.0000 | 9 | 8 | 0.3 | 3.9k | 2.1k | 11 s |
| gd-integration-repo | ok | 88% | 9/10 | 62 | 34.5 s | 0.0000 | 8 | 17 | 0.7 | 4.8k | 2.7k | 26 s |
| media-voice | ok | 100% | 4/4 | 94 | 43.3 s | 0.0000 | 8 | 7 | 0.9 | 2.3k | 1.3k | 7 s |
| file-media-edit | timeout (timeout, evidence 'out/permit-filled.pdf' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes) | 38% | 5/10 | 38 | 1 min 30 s | 0.0000 | 7 | 11 | 1.3 | 9.2k | 7.6k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 3 | 1 min 00 s | 0.0000 | 3 | 2 | 0.4 | 0.2k | 0.1k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (17224)) | 100% | 9/9 | 95 | 39.5 s | 0.0000 | 11 | 13 | 0.4 | 5.2k | 2.4k | 16 s |
| sec-leak-fix | ok | 100% | 10/10 | 94 | 41.9 s | 0.0000 | 6 | 10 | 0.6 | 5.5k | 3.5k | 20 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 88 | 1 min 09 s | 0.0000 | 27 | 27 | 0.4 | 5.8k | 2.6k | 9 s |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 28 | 1 min 00 s | 0.0000 | 12 | 11 | 1.0 | 7.2k | 4.5k | 46 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 85 | 56.6 s | 0.0000 | 11 | 13 | 0.7 | 6.8k | 3.6k | 17 s |
| ts-plugin-bug | ok | 100% | 8/8 | 94 | 46.0 s | 0.0000 | 13 | 18 | 0.5 | 5.8k | 2.2k | 12 s |
| web-mondrian-landing | ok | 100% | 11/11 | 83 | 1 min 32 s | 0.0000 | 9 | 8 | 0.5 | 13.8k | 8.1k | 60 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.621 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 62 | 4 min 33 s | 0.0000 | 16 | 26 | 1.1 | 32.4k | 22.4k | 90 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 14 | 1 min 00 s | 0.0000 | 8 | 15 | 0.6 | 4.8k | 3.5k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:49751", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 82 | 56.7 s | 0.0000 | 24 | 23 | 0.2 | 5.7k | 2.1k | - |
| web-plan-ranking | ok | 75% | 7/9 | 36 | 2 min 50 s | 0.0000 | 10 | 18 | 0.6 | 19.6k | 14.8k | 111 s |
| web-word-universe | ok | 100% | 9/9 | 75 | 5 min 57 s | 0.0000 | 39 | 48 | 0.8 | 44.8k | 23.1k | 30 s |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]
- `py-async-cancel` jobs run side by side up to the limit: expected {'started': 2, 'finished': 2, 'cleaned': 2, 'peak': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` never more jobs at once than the limit: expected {'started': 2, 'finished': 2, 'cleaned': 2, 'peak': 1}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C below the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C at the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'no out/permit-filled.pdf'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received 'no pattern in regex.txt'
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received 'no pattern in regex.txt'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received 'no pattern in regex.txt'
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received 'no pattern in regex.txt'
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
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1], 'Real': [2477.15, 22.41]}, received {'Cruzado': [218.36, 311.62], 'Bresser': [545.71, 1116.65], 'Verao': [1116.65, 574.13], 'Collor I': [764.5,
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received ['Real', 'Collor II', 'Verao']

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 1)
- `py-async-cancel`: not seen: wrote run.py; not seen: ran it
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 3); used the chart of accounts (call 5); used the cash balance (call 4); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 5); recorded the result (call 15)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 3)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 5); read the game mode (call 4); recorded the result (call 7)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 7); committed (call 7)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 8)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); ran the whole suite (call 17)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 2)
- `file-media-edit`: read the details (call 3); made the feed photo (call 10); not seen: filled the permit
- `txt-regex-log`: not seen: wrote the regex; not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 2); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 9); wrote the JSON (call 9)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 5); read the settings (call 2); read the owner notes (call 3); recorded the result (call 12)
- `ts-plugin-bug`: read the bus (call 7); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 12); looked at it in a browser (call 14); recorded the result (call 13)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 3)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 9); replied (call 14)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 15); wrote the dossier (call 17); opened a source (call 2)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 7); wrote the page (call 30); looked at it in a browser (call 36); recorded the result (call 7)
