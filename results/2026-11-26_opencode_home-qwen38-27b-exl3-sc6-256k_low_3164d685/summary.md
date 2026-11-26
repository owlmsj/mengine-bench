# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **75.3** | 86.2 | 16/29 | 68.6 | 63.3 | 21 min 01 s | $0.00 (local) | 5.63M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of pilot7-a1-sft (step-34) on super-adapter merge; cache=FP16; drafter=MTP n4 dynamic; layout=native TP 2x RTX 5090; temperature=0.6; finetune=pilot7-a1-sft (step-34, val 0.1257) on super-adapter rev 3358a715, THINKING OFF; study=mengine-qlora#42 pilot 7 A1 SFT eval run 2; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-26, started 2026-11-26T03:59:29Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 83% | 7/8 | 65 | 1 min 06 s | 0.0000 | 12 | 11 | 0.1 | 7.9k | 0.0k | 35 s |
| py-async-cancel | timeout (timeout) | 80% | 5/6 | 42 | 1 min 00 s | 0.0000 | 20 | 20 | 0.0 | 6.7k | 0.0k | 1 s |
| ds-ab-playtest | ok | 100% | 5/5 | 77 | 53.3 s | 0.0000 | 9 | 10 | 0.2 | 3.1k | 0.0k | 31 s |
| bo-pnl-runway | ok | 40% | 3/6 | 47 | 19.3 s | 0.0000 | 6 | 8 | 0.0 | 2.0k | 0.0k | 8 s |
| bo-reconcile | ok | 100% | 5/5 | 82 | 22.9 s | 0.0000 | 10 | 12 | 0.0 | 2.2k | 0.0k | 6 s |
| cmp-handoff | ok | 91% | 11/12 | 66 | 37.1 s | 0.0000 | 18 | 16 | 0.0 | 3.7k | 0.0k | 7 s |
| cfg-source-drift | ok | 100% | 5/5 | 91 | 15.1 s | 0.0000 | 8 | 11 | 0.0 | 1.4k | 0.0k | 6 s |
| doc-lab-pdf | ok | 100% | 7/7 | 68 | 25.2 s | 0.0000 | 14 | 13 | 0.0 | 2.7k | 0.0k | 5 s |
| ds-sql-funnel | ok | 25% | 2/5 | 36 | 19.8 s | 0.0000 | 8 | 8 | 0.2 | 2.0k | 0.0k | 3 s |
| ue-packaged-bug | ok | 100% | 6/6 | 72 | 17.2 s | 0.0000 | 5 | 11 | 0.0 | 1.8k | 0.0k | 8 s |
| git-merge-conflict | ok | 100% | 7/7 | 94 | 16.2 s | 0.0000 | 8 | 7 | 0.5 | 1.1k | 0.0k | 7 s |
| infra-gpu-fit | ok | 100% | 7/7 | 88 | 13.7 s | 0.0000 | 5 | 6 | 0.1 | 1.5k | 0.0k | 5 s |
| ir-server-logs | ok | 100% | 7/7 | 85 | 31.9 s | 0.0000 | 6 | 6 | 0.0 | 1.3k | 0.0k | 25 s |
| gd-integration-repo | ok | 88% | 9/10 | 70 | 22.9 s | 0.0000 | 7 | 16 | 0.1 | 2.1k | 0.0k | 12 s |
| media-voice | ok | 100% | 4/4 | 78 | 23.0 s | 0.0000 | 9 | 8 | 0.7 | 1.6k | 0.0k | 10 s |
| file-media-edit | ok | 25% | 4/10 | 24 | 34.6 s | 0.0000 | 13 | 13 | 0.5 | 3.2k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 75% | 4/5 | 38 | 1 min 00 s | 0.0000 | 24 | 24 | 0.0 | 8.1k | 0.0k | 2 s |
| rs-lock-bug | ok | 83% | 8/9 | 70 | 29.8 s | 0.0000 | 9 | 10 | 0.3 | 2.4k | 0.0k | 6 s |
| sec-leak-fix | ok | 88% | 9/10 | 79 | 16.0 s | 0.0000 | 7 | 10 | 0.0 | 1.6k | 0.0k | 7 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 91 | 30.3 s | 0.0000 | 24 | 24 | 0.0 | 2.1k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 60% | 4/6 | 43 | 1 min 00 s | 0.0000 | 24 | 23 | 0.4 | 5.6k | 0.0k | 14 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 77 | 26.7 s | 0.0000 | 9 | 9 | 0.4 | 2.3k | 0.0k | 8 s |
| ts-plugin-bug | ok | 100% | 8/8 | 97 | 18.1 s | 0.0000 | 7 | 10 | 0.1 | 1.8k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 89 | 51.3 s | 0.0000 | 20 | 19 | 0.0 | 5.2k | 0.0k | 15 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.41 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 50 | 1 min 23 s | 0.0000 | 9 | 9 | 0.4 | 9.3k | 0.0k | 18 s |
| web-fact-search | ok | 100% | 8/8 | 69 | 29.0 s | 0.0000 | 9 | 13 | 0.2 | 1.5k | 0.0k | 20 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:57760", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 86 | 29.4 s | 0.0000 | 19 | 18 | 0.0 | 1.9k | 0.0k | - |
| web-plan-ranking | timeout (timeout) | 100% | 9/9 | 65 | 3 min 30 s | 0.0000 | 13 | 17 | 0.1 | 5.1k | 0.0k | 162 s |
| web-word-universe | ok | 62% | 6/9 | 51 | 2 min 19 s | 0.0000 | 40 | 40 | 0.0 | 12.8k | 0.0k | 7 s |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `bo-pnl-runway` ebitda per month: 2026-01: expected -210278.96, received -203812.19
- `bo-pnl-runway` 3-month average burn: expected 197288.23, received 190820.54
- `bo-pnl-runway` runway in months: expected 9.363713182484327, received 9.68
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received 'pwsh scripts/start_server.ps1 (local9 block, --no-mmproj-offload -ub 512) then decode benchmark at 128k ctx'
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'purchase', 'steamdeck': 'purchase'}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` balloon fully in frame and undistorted: expected 'the balloon clear of every edge', received {'bbox': (0, 137, 1079, 1214), 'size': (1080, 1350)}
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received ['2023-02-30', '2023-06-31', '2023-02-29', '2023-09-30', '2023-10-31']
- `rs-lock-bug` hidden a transfer to the same player changes nothing: expected 'a_transfer_to_the_same_player_changes_nothing passed', received False
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received ['lantern', 'rope coil']
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received ['tent stake', 'water filter']
- `web-word-universe` collected exactly the site's words: missing 52 (aflição, almoço, amanhã, angústia, açougueiro), extra 63 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acento: missing 1 (sílaba), extra 1 (silaba)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 256, 'relations': 764, 'most_connected': 'tempo'}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 2)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 4); used the chart of accounts (call 5); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 16)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 5)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 4); recorded the result (call 6)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 7); committed (call 6)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 2); read the policy (call 3); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); ran the whole suite (call 16)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 5)
- `file-media-edit`: read the details (call 2); made the feed photo (call 8); filled the permit (call 9)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 6)
- `sec-leak-fix`: read the service (call 3); read the config (call 2); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 5); read the settings (call 3); read the owner notes (call 2); recorded the result (call 8)
- `ts-plugin-bug`: read the bus (call 6); ran the tests (call 9)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 3); recorded the result (call 1)
- `web-fact-search`: not seen: searched the web; recorded the result (call 12); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 8); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 17); wrote the dossier (call 16); opened a source (call 3)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 4); wrote the page (call 11); looked at it in a browser (call 15); recorded the result (call 10)
