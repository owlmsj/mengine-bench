# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **69.8** | 84.9 | 21/29 | 69.2 | 24.3 | 32 min 42 s | $0.00 (local) | 5.49M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715, THINKING OFF; runtime=SGLang lmsysorg/sglang:latest; quant=super-adapter merge, mixed NVFP4 (MLP NVFP4, attention + DeltaNet FP8); cache=fp8_e4m3; drafter=DFlash2 incoai (base-trained), 8 drafts; layout=TP 2x RTX 5090, chunked prefill 4096, mem-fraction-static 0.80; study=top-2 consistency (2026-11-22): sg run 1; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-22, started 2026-11-22T10:26:22Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 84 | 2 min 42 s | 0.0000 | 13 | 12 | 0.5 | 21.9k | 14.1k | 108 s |
| py-async-cancel | timeout (timeout) | 0% | 1/6 | 0 | 1 min 00 s | 0.0000 | 1 | 0 | - | - | - | - |
| ds-ab-playtest | ok | 100% | 5/5 | 82 | 42.9 s | 0.0000 | 5 | 5 | 0.4 | 3.2k | 1.3k | 30 s |
| bo-pnl-runway | ok | 100% | 6/6 | 79 | 1 min 07 s | 0.0000 | 13 | 15 | 0.5 | 10.3k | 6.0k | 14 s |
| bo-reconcile | ok | 100% | 5/5 | 85 | 43.5 s | 0.0000 | 8 | 9 | 0.5 | 6.7k | 4.8k | 20 s |
| cmp-handoff | ok | 91% | 11/12 | 64 | 27.8 s | 0.0000 | 9 | 7 | 0.5 | 3.5k | 1.3k | 7 s |
| cfg-source-drift | ok | 100% | 5/5 | 92 | 15.2 s | 0.0000 | 6 | 10 | 0.6 | 1.9k | 0.6k | 6 s |
| doc-lab-pdf | ok | 100% | 7/7 | 75 | 38.3 s | 0.0000 | 6 | 5 | 0.7 | 6.1k | 4.1k | 25 s |
| ds-sql-funnel | ok | 100% | 5/5 | 85 | 26.7 s | 0.0000 | 9 | 9 | 0.8 | 3.4k | 1.3k | 4 s |
| ue-packaged-bug | ok | 100% | 6/6 | 91 | 38.7 s | 0.0000 | 7 | 13 | 0.7 | 5.4k | 3.4k | 25 s |
| git-merge-conflict | ok | 100% | 7/7 | 94 | 12.8 s | 0.0000 | 6 | 5 | 0.8 | 1.4k | 0.4k | 6 s |
| infra-gpu-fit | ok | 100% | 7/7 | 84 | 21.9 s | 0.0000 | 6 | 7 | 0.3 | 3.3k | 1.7k | 11 s |
| ir-server-logs | ok | 100% | 7/7 | 94 | 40.4 s | 0.0000 | 9 | 12 | 0.6 | 5.5k | 3.4k | 32 s |
| gd-integration-repo | ok | 88% | 9/10 | 64 | 20.8 s | 0.0000 | 6 | 6 | 0.8 | 2.3k | 0.9k | 14 s |
| media-voice | ok | 100% | 4/4 | 76 | 34.4 s | 0.0000 | 12 | 11 | 0.9 | 4.0k | 1.7k | 5 s |
| file-media-edit | ok | 100% | 10/10 | 87 | 43.6 s | 0.0000 | 10 | 9 | 2.0 | 5.2k | 2.1k | 16 s |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 0 | 1 min 00 s | 0.0000 | 1 | 0 | - | - | - | - |
| rs-lock-bug | ok | 100% | 9/9 | 93 | 57.6 s | 0.0000 | 11 | 12 | 0.8 | 7.5k | 4.5k | 29 s |
| sec-leak-fix | ok | 100% | 10/10 | 92 | 30.6 s | 0.0000 | 8 | 10 | 0.3 | 3.7k | 2.0k | 16 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 93 | 48.1 s | 0.0000 | 29 | 30 | 0.1 | 4.7k | 1.9k | 4 s |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 22 | 1 min 00 s | 0.0000 | 5 | 4 | 1.0 | 7.4k | 6.0k | 31 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 84 | 54.8 s | 0.0000 | 11 | 13 | 0.6 | 6.6k | 3.2k | 8 s |
| ts-plugin-bug | timeout (timeout) | 100% | 8/8 | 58 | 1 min 00 s | 0.0000 | 12 | 15 | 0.6 | 6.3k | 4.1k | 9 s |
| web-mondrian-landing | ok | 100% | 11/11 | 83 | 1 min 57 s | 0.0000 | 9 | 8 | 0.8 | 18.1k | 11.9k | 77 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.369 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 50 | 5 min 01 s | 0.0000 | 23 | 29 | 0.9 | 41.4k | 31.1k | 72 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 12 | 1 min 00 s | 0.0000 | 4 | 8 | 0.8 | 5.6k | 4.9k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:59775", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 90 | 48.8 s | 0.0000 | 19 | 18 | 0.4 | 5.3k | 1.9k | - |
| web-plan-ranking | timeout (timeout) | 62% | 6/9 | 24 | 3 min 30 s | 0.0000 | 10 | 18 | 0.6 | 24.3k | 20.6k | 177 s |
| web-word-universe | ok | 100% | 9/9 | 70 | 2 min 38 s | 0.0000 | 29 | 34 | 0.7 | 20.3k | 7.6k | 23 s |

## Failed checks

- `py-async-cancel` jobs run side by side up to the limit: expected {'started': 2, 'finished': 2, 'cleaned': 2, 'peak': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` never more jobs at once than the limit: expected {'started': 2, 'finished': 2, 'cleaned': 2, 'peak': 1}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C below the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C at the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received 'scripts/measure_decode.ps1 -NPredict 1024'
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
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
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1]}, received {'Cruzado': [264.69, 412.43], 'Bresser': [756.98, 621.4], 'Verao': [621.4, 2853.51], 'Collor I': [1228.93, 470.83], 'Collor II': [285
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received ['Real', 'Collor II', 'Collor I']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 0, 'urls': 0, 'plans': []}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: not seen: wrote run.py; not seen: ran it
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 3); used the cash balance (call 4); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 2); recorded the result (call 7)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 3); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 4); recorded the result (call 10)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 5); committed (call 5)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 7)
- `ir-server-logs`: read the notes (call 3); read the logs (call 2); recorded the result (call 11)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 2); ran the whole suite (call 6)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 5); filled the permit (call 5)
- `txt-regex-log`: not seen: wrote the regex; not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 7)
- `sec-leak-fix`: read the service (call 2); read the config (call 4); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 3); opened the site (call 5); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 2)
- `hw-stutter-tuning`: read the frame capture (call 7); read the sensor log (call 7); read the settings (call 5); read the owner notes (call 3); recorded the result (call 11)
- `ts-plugin-bug`: read the bus (call 5); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 4); recorded the result (call 3)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 3)
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 5); replied (call 11)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 18); not seen: wrote the dossier; opened a source (call 3)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 11); wrote the page (call 13); looked at it in a browser (call 26); recorded the result (call 11)
