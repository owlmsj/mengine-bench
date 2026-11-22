# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **73.8** | 87.6 | 21/29 | 73.9 | 31.8 | 30 min 28 s | $0.00 (local) | 5.38M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; runtime=SGLang lmsysorg/sglang:latest; quant=super-adapter merge requantized with ModelOpt 0.47 (NVIDIA mixed recipe: MLP NVFP4 W4A4, attention + DeltaNet main projections FP8, vision/MTP/lm_head BF16; 64 calibration trajectories); ctx=256k; cache=fp8_e4m3; layout=TP 2x RTX 5090, flashinfer attention, chunked prefill 4096, mem-fraction-static 0.80; drafter=DFlash2 incoai/Qwen3.8-27B-DFlash2 (trained on the base), 8 drafts; temperature=model generation_config; clock_cap=2900 MHz both GPUs; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715, THINKING OFF; study=engine speed A/B: super-adapter on SGLang NVFP4 mixed + DFlash2; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-22, started 2026-11-22T04:09:31Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 81 | 2 min 29 s | 0.0000 | 18 | 17 | 0.4 | 20.1k | 9.7k | 68 s |
| py-async-cancel | ok | 100% | 6/6 | 94 | 48.9 s | 0.0000 | 4 | 3 | 2.3 | 6.7k | 5.1k | 33 s |
| ds-ab-playtest | ok | 100% | 5/5 | 83 | 39.8 s | 0.0000 | 5 | 5 | 0.3 | 2.5k | 0.9k | 29 s |
| bo-pnl-runway | ok | 100% | 6/6 | 81 | 32.4 s | 0.0000 | 8 | 9 | 0.3 | 4.8k | 1.7k | 12 s |
| bo-reconcile | ok | 100% | 5/5 | 87 | 32.9 s | 0.0000 | 9 | 10 | 0.5 | 5.3k | 3.4k | 15 s |
| cmp-handoff | ok | 91% | 11/12 | 76 | 26.9 s | 0.0000 | 7 | 6 | 0.5 | 3.6k | 2.0k | 12 s |
| cfg-source-drift | ok | 100% | 5/5 | 93 | 18.0 s | 0.0000 | 6 | 10 | 0.5 | 2.0k | 0.6k | 10 s |
| doc-lab-pdf | ok | 100% | 7/7 | 77 | 39.3 s | 0.0000 | 9 | 9 | 0.6 | 5.8k | 3.6k | 7 s |
| ds-sql-funnel | ok | 25% | 2/5 | 39 | 33.1 s | 0.0000 | 12 | 12 | 0.7 | 4.4k | 1.9k | 3 s |
| ue-packaged-bug | ok | 100% | 6/6 | 79 | 22.7 s | 0.0000 | 5 | 10 | 0.6 | 3.0k | 1.4k | 13 s |
| git-merge-conflict | ok | 100% | 7/7 | 92 | 16.7 s | 0.0000 | 6 | 5 | 0.7 | 1.9k | 0.8k | 8 s |
| infra-gpu-fit | ok | 100% | 7/7 | 82 | 19.9 s | 0.0000 | 6 | 7 | 0.5 | 2.8k | 1.2k | 11 s |
| ir-server-logs | ok | 100% | 7/7 | 92 | 28.0 s | 0.0000 | 8 | 7 | 0.4 | 3.5k | 1.9k | 23 s |
| gd-integration-repo | ok | 88% | 9/10 | 66 | 34.0 s | 0.0000 | 9 | 21 | 0.5 | 4.8k | 2.4k | 21 s |
| media-voice | timeout (timeout) | 100% | 4/4 | 69 | 1 min 00 s | 0.0000 | 11 | 11 | 1.0 | 5.5k | 3.4k | 22 s |
| file-media-edit | ok | 38% | 5/10 | 37 | 1 min 24 s | 0.0000 | 17 | 17 | 0.8 | 10.6k | 6.4k | 19 s |
| txt-regex-log | timeout (timeout) | 100% | 5/5 | 59 | 1 min 00 s | 0.0000 | 3 | 2 | 0.8 | 8.7k | 8.2k | 49 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (29192)) | 100% | 9/9 | 94 | 48.2 s | 0.0000 | 13 | 17 | 0.7 | 6.2k | 2.7k | 16 s |
| sec-leak-fix | ok | 100% | 10/10 | 90 | 33.0 s | 0.0000 | 6 | 11 | 0.6 | 4.2k | 2.4k | 17 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 78 | 53.9 s | 0.0000 | 26 | 27 | 0.1 | 5.2k | 2.4k | 7 s |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 4 | 1 min 00 s | 0.0000 | 3 | 2 | 0.7 | 0.7k | 0.6k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 88 | 1 min 07 s | 0.0000 | 12 | 13 | 0.7 | 6.4k | 3.2k | 12 s |
| ts-plugin-bug | ok | 100% | 8/8 | 99 | 26.7 s | 0.0000 | 6 | 9 | 0.6 | 3.0k | 0.9k | 9 s |
| web-mondrian-landing | ok | 100% | 11/11 | 81 | 1 min 29 s | 0.0000 | 12 | 11 | 0.6 | 13.1k | 7.6k | 47 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.583 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 60 | 1 min 46 s | 0.0000 | 11 | 11 | 1.6 | 13.3k | 7.3k | 53 s |
| web-fact-search | ok | 100% | 8/8 | 83 | 54.5 s | 0.0000 | 10 | 11 | 0.6 | 4.8k | 3.2k | 46 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:53632", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 86 | 2 min 13 s | 0.0000 | 36 | 35 | 0.7 | 15.0k | 8.7k | 106 s |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 18 | 3 min 30 s | 0.0000 | 6 | 10 | 0.7 | 20.7k | 19.0k | - |
| web-word-universe | ok | 100% | 9/9 | 76 | 3 min 20 s | 0.0000 | 27 | 31 | 0.8 | 26.1k | 13.0k | 57 s |

## Failed checks

- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received 'scripts/measure_decode.ps1'
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `web-plan-ranking` all six plans recorded: expected ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real'], received []
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor I': ['1990-03-16'], 'Collor II': ['1991-01-31'], 'Real': ['1994-03-01', '1994-07-01']}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1], 'Real': [2477.15, 22.41]}, received {'Cruzado': [None, None], 'Bresser': [None, None], 'Verao': [None, None], 'Collor I': [None, None], 'Collor
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Verao': [14], 'Collor I': [10], 'Collor II': [37, 41], 'Real': [60]}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` scores follow the rubric: expected "0.7*drop + 0.3*durability from the row's own numbers", received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received None
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 0, 'urls': 0, 'plans': []}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 9)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 3); recorded the result (call 6)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 4); recorded the result (call 8)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 6); recorded the result (call 10)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 5); committed (call 5)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 7)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 7)
- `gd-integration-repo`: read the docs (call 3); ran the integration test (call 9); ran the whole suite (call 21)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 8); filled the permit (call 8)
- `txt-regex-log`: wrote the regex (call 2); not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 6); ran the tests (call 9)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 2); opened the site (call 5); not seen: deleted the test post
- `ds-sqlite-recover`: not seen: read the raw bytes; not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 6); read the settings (call 4); read the owner notes (call 3); recorded the result (call 12)
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 9)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 4); recorded the result (call 3)
- `web-fact-search`: not seen: searched the web; recorded the result (call 10); opened a source (call 1)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); replied (call 27)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: recorded the result; not seen: wrote the dossier; opened a source (call 4)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 5); wrote the page (call 19); looked at it in a browser (call 22); recorded the result (call 24)
