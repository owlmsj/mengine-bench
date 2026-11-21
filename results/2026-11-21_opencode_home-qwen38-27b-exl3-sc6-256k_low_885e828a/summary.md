# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **72.8** | 87.5 | 21/29 | 70.9 | 32.4 | 30 min 17 s | $0.00 (local) | 6.14M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of pi-adapted merge; ctx=256k; cache=FP16; layout=native TP 2x RTX 5090; drafter=MTP n4 dynamic; temperature=0.6; finetune=harness-hub/Qwen3.8-27B-pi rev e786f849, THINKING OFF; study=pilot 7 control: pi-adapted run 2 (plugins via tunnel config); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-21, started 2026-11-21T11:43:15Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 62 | 2 min 13 s | 0.0000 | 15 | 14 | 0.5 | 10.6k | 0.0k | 77 s |
| py-async-cancel | ok | 80% | 5/6 | 69 | 54.1 s | 0.0000 | 13 | 12 | 0.0 | 4.0k | 0.0k | 4 s |
| ds-ab-playtest | ok | 100% | 5/5 | 87 | 1 min 01 s | 0.0000 | 6 | 6 | 0.0 | 2.0k | 0.0k | 44 s |
| bo-pnl-runway | ok | 100% | 6/6 | 88 | 52.8 s | 0.0000 | 8 | 10 | 0.0 | 4.0k | 0.0k | 14 s |
| bo-reconcile | ok | 100% | 5/5 | 92 | 35.1 s | 0.0000 | 9 | 10 | 0.0 | 2.5k | 0.0k | 11 s |
| cmp-handoff | ok | 100% | 12/12 | 84 | 1 min 01 s | 0.0000 | 22 | 20 | 0.2 | 4.1k | 0.0k | 11 s |
| cfg-source-drift | ok | 100% | 5/5 | 87 | 21.8 s | 0.0000 | 8 | 12 | 0.0 | 1.5k | 0.0k | 9 s |
| doc-lab-pdf | ok | 100% | 7/7 | 68 | 24.6 s | 0.0000 | 8 | 7 | 0.0 | 1.8k | 0.0k | 7 s |
| ds-sql-funnel | ok | 25% | 2/5 | 35 | 45.6 s | 0.0000 | 13 | 13 | 0.0 | 3.2k | 0.0k | 5 s |
| ue-packaged-bug | ok | 100% | 6/6 | 90 | 35.5 s | 0.0000 | 8 | 14 | 0.0 | 2.5k | 0.0k | 14 s |
| git-merge-conflict | ok | 100% | 7/7 | 90 | 28.1 s | 0.0000 | 9 | 8 | 0.5 | 1.6k | 0.0k | 13 s |
| infra-gpu-fit | ok | 100% | 7/7 | 84 | 24.7 s | 0.0000 | 6 | 7 | 0.0 | 1.8k | 0.0k | 8 s |
| ir-server-logs | ok | 100% | 7/7 | 85 | 27.5 s | 0.0000 | 7 | 9 | 0.1 | 1.7k | 0.0k | 17 s |
| gd-integration-repo | ok | 88% | 9/10 | 54 | 57.3 s | 0.0000 | 13 | 24 | 0.1 | 3.9k | 0.0k | 23 s |
| media-voice | ok | 100% | 4/4 | 85 | 16.8 s | 0.0000 | 5 | 4 | 0.6 | 0.9k | 0.0k | - |
| file-media-edit | ok | 88% | 9/10 | 68 | 1 min 13 s | 0.0000 | 22 | 23 | 0.5 | 4.9k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 5 | 1 min 00 s | 0.0000 | 3 | 2 | 0.0 | 4.6k | 0.0k | 45 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (4324)) | 100% | 9/9 | 78 | 32.9 s | 0.0000 | 9 | 10 | 0.0 | 2.1k | 0.0k | 13 s |
| sec-leak-fix | ok | 88% | 9/10 | 81 | 24.3 s | 0.0000 | 9 | 11 | 0.0 | 1.6k | 0.0k | 8 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 88 | 1 min 06 s | 0.0000 | 29 | 29 | 0.2 | 2.6k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 19 | 1 min 00 s | 0.0000 | 13 | 12 | 0.4 | 3.6k | 0.0k | 25 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 82 | 57.9 s | 0.0000 | 10 | 11 | 0.4 | 3.4k | 0.0k | 17 s |
| ts-plugin-bug | ok | 100% | 8/8 | 97 | 31.3 s | 0.0000 | 9 | 13 | 0.0 | 2.2k | 0.0k | 10 s |
| web-mondrian-landing | ok | 100% | 11/11 | 67 | 1 min 28 s | 0.0000 | 13 | 12 | 0.2 | 6.2k | 0.0k | 39 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.311 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 44 | 1 min 52 s | 0.0000 | 10 | 9 | 0.8 | 8.7k | 0.0k | 34 s |
| web-fact-search | ok | 100% | 8/8 | 83 | 44.1 s | 0.0000 | 7 | 10 | 0.5 | 1.3k | 0.0k | 33 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:61069", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 81 | 1 min 45 s | 0.0000 | 37 | 36 | 0.0 | 5.1k | 0.0k | - |
| web-plan-ranking | ok | 100% | 9/9 | 64 | 3 min 08 s | 0.0000 | 25 | 32 | 0.3 | 8.2k | 0.0k | 133 s |
| web-word-universe | ok | 50% | 5/9 | 40 | 3 min 16 s | 0.0000 | 32 | 34 | 0.0 | 13.5k | 0.0k | 15 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'purchase', 'steamdeck': 'purchase'}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received 'no pattern in regex.txt'
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received 'no pattern in regex.txt'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received 'no pattern in regex.txt'
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received 'no pattern in regex.txt'
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 55 (acougueiro, aflicao, agua, almoco, amanha)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acougueiro: missing 0 (none), extra 3 (enfermeira, pescador, tarde)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 255, 'relations': 766, 'most_connected': [{'word': 'palavra', 'degree': 16}, {'word': 'tempo', 'degree': 16}, {'word': 'madrugada', 'degree': 9}]}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país does not show its 5 relations, missing nação

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); not seen: removed duplicate sessions; tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 4); read the invoices (call 2); read the statement (call 3); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 16)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 3)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 7); recorded the result (call 12)
- `git-merge-conflict`: merged the branch (call 5); ran the tests (call 7); committed (call 7)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 2); read the policy (call 3); recorded the result (call 6)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 9)
- `gd-integration-repo`: read the docs (call 3); ran the integration test (call 5); ran the whole suite (call 18)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 3)
- `file-media-edit`: read the details (call 2); made the feed photo (call 6); filled the permit (call 8)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 2)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 7)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 10)
- `cu-social-cycle`: made the image (call 3); opened the site (call 4); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 4); wrote the JSON (call 4)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 5); read the settings (call 2); read the owner notes (call 3); recorded the result (call 10)
- `ts-plugin-bug`: read the bus (call 7); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 9); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 7); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 31); wrote the dossier (call 30); opened a source (call 5)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 5); wrote the page (call 10); looked at it in a browser (call 11); recorded the result (call 5)
