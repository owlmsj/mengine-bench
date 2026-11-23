# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **72.5** | 82.9 | 17/29 | 65.3 | 66.1 | 20 min 10 s | $0.00 (local) | 4.59M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715, THINKING OFF; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of super-adapter merge; cache=FP16; drafter=MTP n4 dynamic; layout=native TP 2x RTX 5090; sampling=temperature 0.7 (forced), top_k 20, top_p 0.95; study=temperature 0.7 vs 0.6 (mengine#1090, 2026-11-23); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-23, started 2026-11-23T13:11:07Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 59 | 1 min 16 s | 0.0000 | 11 | 10 | 0.5 | 7.2k | 0.0k | 35 s |
| py-async-cancel | ok | 80% | 5/6 | 60 | 15.3 s | 0.0000 | 4 | 3 | 0.0 | 1.4k | 0.0k | 3 s |
| ds-ab-playtest | ok | 100% | 5/5 | 90 | 40.7 s | 0.0000 | 6 | 6 | 0.0 | 1.6k | 0.0k | 31 s |
| bo-pnl-runway | ok | 40% | 3/6 | 48 | 19.6 s | 0.0000 | 7 | 8 | 0.0 | 2.0k | 0.0k | 9 s |
| bo-reconcile | ok | 100% | 5/5 | 87 | 26.4 s | 0.0000 | 8 | 9 | 0.0 | 3.4k | 0.0k | 6 s |
| cmp-handoff | ok | 100% | 12/12 | 82 | 26.9 s | 0.0000 | 12 | 10 | 0.0 | 2.5k | 0.0k | 7 s |
| cfg-source-drift | ok | 100% | 5/5 | 94 | 15.8 s | 0.0000 | 7 | 12 | 0.0 | 1.7k | 0.0k | 6 s |
| doc-lab-pdf | ok | 100% | 7/7 | 66 | 28.5 s | 0.0000 | 9 | 9 | 0.0 | 3.6k | 0.0k | 3 s |
| ds-sql-funnel | ok | 50% | 3/5 | 48 | 18.8 s | 0.0000 | 7 | 8 | 0.2 | 2.0k | 0.0k | 3 s |
| ue-packaged-bug | ok | 80% | 5/6 | 37 | 30.9 s | 0.0000 | 11 | 15 | 0.0 | 3.6k | 0.0k | 17 s |
| git-merge-conflict | ok | 100% | 7/7 | 89 | 18.9 s | 0.0000 | 10 | 9 | 0.4 | 1.4k | 0.0k | 9 s |
| infra-gpu-fit | ok | 100% | 7/7 | 81 | 18.8 s | 0.0000 | 6 | 7 | 0.0 | 2.2k | 0.0k | 8 s |
| ir-server-logs | ok | 100% | 7/7 | 88 | 34.1 s | 0.0000 | 7 | 7 | 0.0 | 1.5k | 0.0k | 23 s |
| gd-integration-repo | ok | 88% | 9/10 | 64 | 21.3 s | 0.0000 | 6 | 15 | 0.0 | 2.0k | 0.0k | 12 s |
| media-voice | ok | 100% | 4/4 | 80 | 23.6 s | 0.0000 | 7 | 6 | 0.6 | 1.3k | 0.0k | - |
| file-media-edit | timeout (timeout, evidence 'out/feed-photo.jpg' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes, evidence 'out/permit-filled.pdf' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes) | 0% | 2/10 | 6 | 1 min 30 s | 0.0000 | 3 | 3 | 0.5 | 0.2k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 75% | 4/5 | 58 | 1 min 00 s | 0.0000 | 19 | 18 | 0.0 | 7.1k | 0.0k | 2 s |
| rs-lock-bug | ok | 100% | 9/9 | 76 | 25.8 s | 0.0000 | 12 | 13 | 0.0 | 2.6k | 0.0k | 7 s |
| sec-leak-fix | ok | 88% | 9/10 | 70 | 21.7 s | 0.0000 | 9 | 11 | 0.1 | 2.3k | 0.0k | 5 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 85 | 30.3 s | 0.0000 | 24 | 24 | 0.0 | 2.2k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 80% | 5/6 | 47 | 1 min 00 s | 0.0000 | 26 | 25 | 0.4 | 5.2k | 0.0k | 20 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 89 | 53.9 s | 0.0000 | 9 | 11 | 0.0 | 2.3k | 0.0k | 34 s |
| ts-plugin-bug | ok | 100% | 8/8 | 84 | 12.3 s | 0.0000 | 5 | 8 | 0.0 | 1.0k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 72 | 36.7 s | 0.0000 | 12 | 11 | 0.0 | 4.3k | 0.0k | 17 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.382 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 50 | 1 min 24 s | 0.0000 | 14 | 13 | 0.0 | 11.0k | 0.0k | 28 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 6 | 1 min 00 s | 0.0000 | 18 | 22 | 1.1 | 1.9k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:60451", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 85 | 45.4 s | 0.0000 | 30 | 29 | 0.0 | 3.7k | 0.0k | 28 s |
| web-plan-ranking | ok | 75% | 7/9 | 50 | 1 min 57 s | 0.0000 | 13 | 12 | 0.0 | 5.0k | 0.0k | 91 s |
| web-word-universe | ok | 50% | 5/9 | 43 | 1 min 37 s | 0.0000 | 23 | 23 | 0.4 | 8.7k | 0.0k | 14 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `bo-pnl-runway` ebitda per month: 2026-01: expected -210278.96, received -203812.19
- `bo-pnl-runway` 3-month average burn: expected 197288.23, received 190820.54
- `bo-pnl-runway` runway in months: expected 9.363713182484327, received 9.68
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 268}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 60}
- `ue-packaged-bug` crash fixed: the score tracker survives garbage collection: ScoreTracker is not kept alive by UPROPERTY, TStrongObjectPtr, AddToRoot or a reported reference
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` photo is a JPEG: expected 'a readable JPEG', received 'FileNotFoundError reading out/feed-photo.jpg'
- `file-media-edit` photo is exactly 1080x1350: expected 'a readable JPEG', received 'FileNotFoundError reading out/feed-photo.jpg'
- `file-media-edit` balloon fully in frame and undistorted: expected 'a readable JPEG', received 'FileNotFoundError reading out/feed-photo.jpg'
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'no out/permit-filled.pdf'
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received ['2024-09-09', '2025-01-23', '2025-02-02', '2025-02-03']
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `web-fact-search` sqlite_3_40_0_release_date value: expected '2022-11-16', received None
- `web-fact-search` sqlite_3_40_0_release_date primary source: expected 'an http(s) URL on sqlite.org', received None
- `web-fact-search` postgresql_15_0_release_date value: expected '2022-10-13', received None
- `web-fact-search` postgresql_15_0_release_date primary source: expected 'an http(s) URL on postgresql.org', received None
- `web-fact-search` unicode_15_0_characters_added value: expected 4489, received None
- `web-fact-search` unicode_15_0_characters_added primary source: expected 'an http(s) URL on unicode.org', received None
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 3432, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 58 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acento: missing 0 (none), extra 1 (silaba)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 691, 'most_connected': 'tempo', 'most_connected_count': 13}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=saudade does not show its 5 relations, missing esperança

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 3); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 10)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 4); recorded the result (call 6)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 8); recorded the result (call 13)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 8); committed (call 9)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 2); read the policy (call 3); recorded the result (call 7)
- `ir-server-logs`: read the notes (call 3); read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); ran the whole suite (call 15)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 2)
- `file-media-edit`: read the details (call 2); not seen: made the feed photo; not seen: filled the permit
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 4); read the config (call 2); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); wrote the JSON (call 5)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 4); read the settings (call 2); read the owner notes (call 3); recorded the result (call 10)
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: searched the web (call 14); not seen: recorded the result; opened a source (call 1)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 7); replied (call 7)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 10); wrote the dossier (call 11); not seen: opened a source
- `web-word-universe`: walked the site (call 2); wrote words.json (call 4); wrote the page (call 6); looked at it in a browser (call 10); recorded the result (call 4)
