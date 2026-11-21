# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **69.9** | 88.5 | 19/29 | 69.1 | 10.8 | 36 min 46 s | $0.00 (local) | 7.10M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of opencode-adapted merge; ctx=256k; cache=FP16; layout=native TP 2x RTX 5090; drafter=MTP n4 dynamic; temperature=0.6; finetune=harness-hub/Qwen3.8-27B-opencode-adapted rev b4171c00 (AsyncGRPO LoRA r32), THINKING OFF; study=pilot 7 control run 2 (plugins via tunnel config); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-21, started 2026-11-21T10:28:40Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 78 | 4 min 57 s | 0.0000 | 56 | 55 | 0.8 | 14.1k | 0.0k | 57 s |
| py-async-cancel | ok | 80% | 5/6 | 61 | 31.4 s | 0.0000 | 5 | 4 | 0.0 | 2.1k | 0.0k | 7 s |
| ds-ab-playtest | ok | 100% | 5/5 | 91 | 58.9 s | 0.0000 | 6 | 7 | 0.0 | 1.9k | 0.0k | 42 s |
| bo-pnl-runway | ok | 100% | 6/6 | 74 | 27.7 s | 0.0000 | 6 | 8 | 0.0 | 2.0k | 0.0k | 12 s |
| bo-reconcile | ok | 100% | 5/5 | 88 | 30.6 s | 0.0000 | 9 | 10 | 0.0 | 2.0k | 0.0k | 9 s |
| cmp-handoff | ok | 100% | 12/12 | 91 | 39.1 s | 0.0000 | 12 | 10 | 0.0 | 2.5k | 0.0k | 10 s |
| cfg-source-drift | ok | 100% | 5/5 | 87 | 28.7 s | 0.0000 | 9 | 13 | 0.1 | 1.9k | 0.0k | 8 s |
| doc-lab-pdf | ok | 100% | 7/7 | 79 | 22.9 s | 0.0000 | 7 | 6 | 0.5 | 1.5k | 0.0k | 11 s |
| ds-sql-funnel | ok | 50% | 3/5 | 36 | 46.8 s | 0.0000 | 17 | 17 | 0.0 | 3.4k | 0.0k | 4 s |
| ue-packaged-bug | ok | 80% | 5/6 | 42 | 31.5 s | 0.0000 | 8 | 14 | 0.0 | 2.2k | 0.0k | 11 s |
| git-merge-conflict | ok | 100% | 7/7 | 94 | 25.5 s | 0.0000 | 9 | 9 | 0.4 | 1.4k | 0.0k | 11 s |
| infra-gpu-fit | ok | 100% | 7/7 | 87 | 20.3 s | 0.0000 | 5 | 6 | 0.0 | 1.5k | 0.0k | 8 s |
| ir-server-logs | ok | 100% | 7/7 | 84 | 48.1 s | 0.0000 | 8 | 8 | 0.0 | 1.6k | 0.0k | 33 s |
| gd-integration-repo | timeout (timeout) | 50% | 6/10 | 40 | 2 min 30 s | 0.0000 | 9 | 20 | 0.1 | 3.6k | 0.0k | 21 s |
| media-voice | ok | 100% | 4/4 | 68 | 43.2 s | 0.0000 | 13 | 12 | 0.6 | 1.9k | 0.0k | 23 s |
| file-media-edit | timeout (timeout) | 50% | 6/10 | 42 | 1 min 30 s | 0.0000 | 31 | 31 | 0.4 | 6.6k | 0.0k | 9 s |
| txt-regex-log | timeout (timeout) | 100% | 5/5 | 49 | 1 min 00 s | 0.0000 | 16 | 16 | 0.0 | 5.1k | 0.0k | 6 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (10484)) | 100% | 9/9 | 88 | 31.2 s | 0.0000 | 6 | 7 | 0.0 | 2.2k | 0.0k | 11 s |
| sec-leak-fix | ok | 100% | 10/10 | 85 | 33.2 s | 0.0000 | 11 | 14 | 0.0 | 2.3k | 0.0k | 8 s |
| cu-social-cycle | timeout (timeout, route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 58 | 3 min 00 s | 0.0000 | 114 | 114 | 0.0 | 9.9k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 16 | 1 min 00 s | 0.0000 | 11 | 11 | 0.4 | 4.4k | 0.0k | 16 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 70 | 46.6 s | 0.0000 | 10 | 13 | 0.0 | 2.9k | 0.0k | 13 s |
| ts-plugin-bug | ok | 100% | 8/8 | 95 | 32.4 s | 0.0000 | 9 | 12 | 0.1 | 2.3k | 0.0k | 9 s |
| web-mondrian-landing | ok | 100% | 11/11 | 79 | 1 min 11 s | 0.0000 | 15 | 14 | 0.4 | 5.4k | 0.0k | 33 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.116 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 50 | 2 min 17 s | 0.0000 | 16 | 15 | 0.1 | 10.1k | 0.0k | 38 s |
| web-fact-search | ok | 100% | 8/8 | 91 | 42.6 s | 0.0000 | 8 | 9 | 0.4 | 1.1k | 0.0k | 32 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:61420", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 82 | 1 min 20 s | 0.0000 | 34 | 33 | 0.4 | 4.1k | 0.0k | - |
| web-plan-ranking | ok | 88% | 8/9 | 56 | 2 min 55 s | 0.0000 | 22 | 23 | 0.2 | 6.6k | 0.0k | 90 s |
| web-word-universe | ok | 50% | 5/9 | 43 | 4 min 25 s | 0.0000 | 49 | 50 | 0.1 | 13.7k | 0.0k | 15 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 263}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 59}
- `ue-packaged-bug` crash fixed: the score tracker survives garbage collection: ScoreTracker is not kept alive by UPROPERTY, TStrongObjectPtr, AddToRoot or a reported reference
- `gd-integration-repo` hidden config override and persistence: FAIL: test_config_override_and_persistence (test_hidden_gold.Hidden.test_config_override_and_persistence) | AssertionError: 1694 != 1690
- `gd-integration-repo` hidden half up tie rounds up: FAIL: test_half_up_tie_rounds_up (test_hidden_gold.Hidden.test_half_up_tie_rounds_up) | AssertionError: 1425 != 1430
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1495 != 1500
- `gd-integration-repo` existing test suite passes
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2914, 'urls': 1, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 3 (contato, dicionário criativo, sobre)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'açougueiro: missing 1 (enfermeira), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 734, 'most_connected': ['tempo']}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país does not show its 5 relations, missing nação

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 4)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); not seen: removed duplicate sessions; tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 3); wrote the handoff (call 4); recorded the result (call 10)
- `cfg-source-drift`: read the readme (call 4); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 3); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 5); read the game mode (call 4); recorded the result (call 10)
- `git-merge-conflict`: merged the branch (call 6); ran the tests (call 9); committed (call 8)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 8)
- `gd-integration-repo`: read the docs (call 3); ran the integration test (call 5); ran the whole suite (call 17)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 7)
- `file-media-edit`: read the details (call 2); made the feed photo (call 9); filled the permit (call 12)
- `txt-regex-log`: wrote the regex (call 3); tried it in Python (call 4)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 7)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 10)
- `cu-social-cycle`: made the image (call 3); opened the site (call 2); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); wrote the JSON (call 8)
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 6); read the settings (call 4); read the owner notes (call 3); recorded the result (call 12)
- `ts-plugin-bug`: read the bus (call 5); ran the tests (call 9)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 8); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); replied (call 7)
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 3); recorded the result (call 19); wrote the dossier (call 20); opened a source (call 3)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 9); wrote the page (call 11); looked at it in a browser (call 12); recorded the result (call 9)
