# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **75.0** | 85.1 | 16/29 | 65.3 | 75.3 | 17 min 24 s | $0.00 (local) | 5.13M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of pilot7-a1-dpo50 (50% step-15 DPO on A1 SFT); cache=FP16; drafter=MTP n4 dynamic; layout=native TP 2x RTX 5090; temperature=0.6; finetune=pilot7-a1-dpo50 (0.5x B DPO step-15 on pilot7-a1-sft), THINKING OFF; study=mengine-qlora#42 pilot 7 A1+50%DPO eval run 2; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-26, started 2026-11-26T23:46:57Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 60 | 1 min 29 s | 0.0000 | 22 | 21 | 0.4 | 8.5k | 0.0k | 33 s |
| py-async-cancel | ok | 80% | 5/6 | 65 | 15.5 s | 0.0000 | 6 | 5 | 0.0 | 1.6k | 0.0k | 2 s |
| ds-ab-playtest | ok | 100% | 5/5 | 85 | 45.0 s | 0.0000 | 7 | 7 | 0.0 | 2.1k | 0.0k | 32 s |
| bo-pnl-runway | ok | 100% | 6/6 | 69 | 26.8 s | 0.0000 | 11 | 15 | 0.0 | 2.9k | 0.0k | 8 s |
| bo-reconcile | ok | 100% | 5/5 | 86 | 16.9 s | 0.0000 | 6 | 7 | 0.0 | 1.7k | 0.0k | 7 s |
| cmp-handoff | ok | 100% | 12/12 | 86 | 31.1 s | 0.0000 | 15 | 13 | 0.0 | 2.8k | 0.0k | 7 s |
| cfg-source-drift | ok | 100% | 5/5 | 91 | 16.6 s | 0.0000 | 11 | 11 | 0.0 | 1.5k | 0.0k | 4 s |
| doc-lab-pdf | ok | 100% | 7/7 | 62 | 20.5 s | 0.0000 | 9 | 8 | 0.2 | 2.2k | 0.0k | 4 s |
| ds-sql-funnel | ok | 25% | 2/5 | 23 | 20.2 s | 0.0000 | 8 | 8 | 0.2 | 2.2k | 0.0k | 3 s |
| ue-packaged-bug | ok | 80% | 5/6 | 39 | 19.4 s | 0.0000 | 8 | 13 | 0.1 | 2.1k | 0.0k | 6 s |
| git-merge-conflict | ok | 100% | 7/7 | 93 | 18.5 s | 0.0000 | 9 | 8 | 0.4 | 1.3k | 0.0k | 10 s |
| infra-gpu-fit | ok | 100% | 7/7 | 82 | 13.9 s | 0.0000 | 5 | 6 | 0.1 | 1.4k | 0.0k | 6 s |
| ir-server-logs | ok | 100% | 7/7 | 85 | 17.4 s | 0.0000 | 8 | 7 | 0.0 | 1.6k | 0.0k | 9 s |
| gd-integration-repo | ok | 88% | 9/10 | 55 | 20.6 s | 0.0000 | 6 | 16 | 0.0 | 1.9k | 0.0k | 12 s |
| media-voice | ok | 100% | 4/4 | 70 | 27.3 s | 0.0000 | 11 | 10 | 0.9 | 2.0k | 0.0k | 4 s |
| file-media-edit | ok | 38% | 5/10 | 37 | 37.4 s | 0.0000 | 15 | 15 | 0.5 | 3.6k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 28 | 1 min 00 s | 0.0000 | 25 | 24 | 0.3 | 7.5k | 0.0k | 3 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (4124)) | 83% | 8/9 | 54 | 20.5 s | 0.0000 | 8 | 10 | 0.0 | 2.3k | 0.0k | 7 s |
| sec-leak-fix | ok | 88% | 9/10 | 80 | 15.8 s | 0.0000 | 7 | 12 | 0.0 | 1.6k | 0.0k | 6 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 91 | 32.6 s | 0.0000 | 27 | 27 | 0.0 | 2.6k | 0.0k | - |
| ds-sqlite-recover | ok | 80% | 5/6 | 45 | 44.2 s | 0.0000 | 12 | 11 | 0.3 | 4.9k | 0.0k | 15 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 69 | 38.2 s | 0.0000 | 14 | 16 | 0.2 | 3.7k | 0.0k | 13 s |
| ts-plugin-bug | ok | 100% | 8/8 | 98 | 22.4 s | 0.0000 | 9 | 13 | 0.0 | 2.5k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 80 | 45.8 s | 0.0000 | 12 | 11 | 0.1 | 4.7k | 0.0k | 16 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.29 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 42 | 45.7 s | 0.0000 | 10 | 9 | 0.0 | 5.5k | 0.0k | 18 s |
| web-fact-search | timeout (timeout) | 100% | 8/8 | 65 | 1 min 00 s | 0.0000 | 20 | 19 | 0.2 | 2.3k | 0.0k | 1 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:57085", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 83% | 8/9 | 45 | 39.4 s | 0.0000 | 23 | 22 | 0.0 | 3.6k | 0.0k | - |
| web-plan-ranking | ok | 75% | 7/9 | 54 | 1 min 19 s | 0.0000 | 10 | 9 | 0.0 | 4.7k | 0.0k | 53 s |
| web-word-universe | ok | 50% | 5/9 | 55 | 1 min 44 s | 0.0000 | 29 | 30 | 0.2 | 10.5k | 0.0k | 14 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "AttributeError: 'coroutine' object has no attribute 'cancel'"
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 302}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 77}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'tutorial_complete', 'steamdeck': 'tutorial_complete'}
- `ue-packaged-bug` crash fixed: the score tracker survives garbage collection: ScoreTracker is not kept alive by UPROPERTY, TStrongObjectPtr, AddToRoot or a reported reference
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received ['2026-02-11']
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received []
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received []
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received []
- `rs-lock-bug` hidden a transfer to the same player changes nothing: expected 'a_transfer_to_the_same_player_changes_nothing passed', received False
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `cu-webmail` invoice PDF saved byte for byte: expected 'a file with the sha256 of LP-2026-0418.pdf', received ['AGENTS.md', 'LP-2026-0418.pdf']
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 3103, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 62 (aflição, almoço, amanhã, angústia, avó), extra 63 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acento: missing 1 (sílaba), extra 1 (silaba)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 251, 'relations': 756, 'most_connected': ['palavra', 'tempo']}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=saudade does not show its 5 relations, missing esperança

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 3); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 12)
- `cfg-source-drift`: not seen: read the readme; ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 3)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 5); recorded the result (call 11)
- `git-merge-conflict`: merged the branch (call 5); ran the tests (call 7); committed (call 7)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 5); ran the whole suite (call 16)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 5); filled the permit (call 8)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 6); ran the tests (call 9)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 11)
- `cu-social-cycle`: made the image (call 1); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 4); read the settings (call 3); read the owner notes (call 2); recorded the result (call 15)
- `ts-plugin-bug`: read the bus (call 6); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 1); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 8); wrote the dossier (call 7); not seen: opened a source
- `web-word-universe`: walked the site (call 1); wrote words.json (call 4); wrote the page (call 6); looked at it in a browser (call 9); recorded the result (call 4)
