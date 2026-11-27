# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **75.8** | 87.3 | 18/29 | 69.7 | 59.3 | 22 min 12 s | $0.00 (local) | 8.35M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of pilot7-a1-sft (step-34) on super-adapter merge; cache=FP16; drafter=MTP n4 dynamic; layout=native TP 2x RTX 5090; temperature=0.6; finetune=pilot7-a1-sft (step-34, val 0.1257) on super-adapter rev 3358a715, THINKING OFF; study=mengine-qlora#42 pilot 7 A1 SFT eval run 1; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-26, started 2026-11-26T03:34:03Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 74 | 1 min 15 s | 0.0000 | 14 | 13 | 0.1 | 8.6k | 0.0k | 40 s |
| py-async-cancel | ok | 80% | 5/6 | 66 | 22.7 s | 0.0000 | 6 | 5 | 0.0 | 2.4k | 0.0k | 1 s |
| ds-ab-playtest | ok | 100% | 5/5 | 90 | 47.3 s | 0.0000 | 6 | 6 | 0.1 | 1.8k | 0.0k | 32 s |
| bo-pnl-runway | ok | 100% | 6/6 | 82 | 20.7 s | 0.0000 | 6 | 9 | 0.1 | 2.0k | 0.0k | 8 s |
| bo-reconcile | ok | 100% | 5/5 | 81 | 19.7 s | 0.0000 | 7 | 8 | 0.0 | 1.9k | 0.0k | 6 s |
| cmp-handoff | ok | 91% | 11/12 | 70 | 27.1 s | 0.0000 | 10 | 8 | 0.0 | 2.5k | 0.0k | 7 s |
| cfg-source-drift | ok | 100% | 5/5 | 90 | 16.1 s | 0.0000 | 9 | 12 | 0.0 | 1.6k | 0.0k | 6 s |
| doc-lab-pdf | ok | 100% | 7/7 | 84 | 24.8 s | 0.0000 | 10 | 9 | 0.4 | 2.7k | 0.0k | 5 s |
| ds-sql-funnel | ok | 25% | 2/5 | 29 | 24.2 s | 0.0000 | 10 | 10 | 0.2 | 2.4k | 0.0k | 3 s |
| ue-packaged-bug | ok | 100% | 6/6 | 89 | 16.7 s | 0.0000 | 6 | 10 | 0.0 | 1.7k | 0.0k | 6 s |
| git-merge-conflict | ok | 100% | 7/7 | 91 | 16.5 s | 0.0000 | 7 | 6 | 0.5 | 1.2k | 0.0k | 7 s |
| infra-gpu-fit | ok | 100% | 7/7 | 82 | 14.0 s | 0.0000 | 5 | 6 | 0.1 | 1.4k | 0.0k | 5 s |
| ir-server-logs | ok | 100% | 7/7 | 94 | 38.7 s | 0.0000 | 8 | 8 | 0.0 | 1.6k | 0.0k | 31 s |
| gd-integration-repo | ok | 88% | 9/10 | 63 | 19.5 s | 0.0000 | 7 | 7 | 0.0 | 1.4k | 0.0k | 8 s |
| media-voice | ok | 67% | 3/4 | 34 | 24.1 s | 0.0000 | 11 | 10 | 0.7 | 1.9k | 0.0k | 4 s |
| file-media-edit | ok | 38% | 5/10 | 26 | 37.9 s | 0.0000 | 12 | 11 | 1.4 | 2.8k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 100% | 5/5 | 58 | 1 min 00 s | 0.0000 | 22 | 21 | 0.0 | 7.3k | 0.0k | 3 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (24272)) | 100% | 9/9 | 89 | 50.8 s | 0.0000 | 9 | 11 | 0.0 | 6.3k | 0.0k | 29 s |
| sec-leak-fix | ok | 88% | 9/10 | 75 | 16.0 s | 0.0000 | 8 | 10 | 0.0 | 1.6k | 0.0k | 7 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 85 | 32.2 s | 0.0000 | 25 | 24 | 0.0 | 2.2k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 15 | 1 min 00 s | 0.0000 | 13 | 13 | 0.4 | 8.1k | 0.0k | 3 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 89 | 23.0 s | 0.0000 | 7 | 8 | 0.2 | 1.9k | 0.0k | 9 s |
| ts-plugin-bug | ok | 100% | 8/8 | 92 | 22.4 s | 0.0000 | 10 | 14 | 0.0 | 2.3k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 56 | 2 min 06 s | 0.0000 | 30 | 29 | 0.0 | 19.7k | 0.0k | 18 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.185 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 42 | 1 min 32 s | 0.0000 | 13 | 12 | 0.2 | 12.9k | 0.0k | 2 s |
| web-fact-search | ok | 100% | 8/8 | 85 | 34.9 s | 0.0000 | 6 | 8 | 0.3 | 1.2k | 0.0k | 29 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:61174", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 78 | 39.0 s | 0.0000 | 25 | 24 | 0.0 | 3.1k | 0.0k | - |
| web-plan-ranking | ok | 75% | 7/9 | 56 | 2 min 01 s | 0.0000 | 10 | 9 | 0.0 | 5.8k | 0.0k | 90 s |
| web-word-universe | ok | 62% | 6/9 | 55 | 3 min 28 s | 0.0000 | 92 | 92 | 0.4 | 21.0k | 0.0k | 14 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received 'scripts/measure_decode.ps1 -NPredict 1024'
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'purchase', 'steamdeck': 'purchase'}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `media-voice` lasts 4 to 8 s: expected (4.0, 8.0), received 3.23
- `file-media-edit` balloon fully in frame and undistorted: expected 'a round, whole balloon', received {'bbox': (540, 169, 872, 438), 'size': (1080, 1350), 'width/height': 1.23, 'fill': 0.78}
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 3178, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 11 (contato, coracoes, dicionário criativo, em-construcao, link-antigo)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'advogado: missing 0 (none), extra 1 (coracoes)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 743, 'most_connected': 'tempo'}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 2); removed duplicate sessions (call 6); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 4); used the chart of accounts (call 5); used the cash balance (call 3); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 8)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 2); extracted the text (call 2); recorded the result (call 3)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 4); recorded the result (call 6)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 5); committed (call 5)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 6)
- `ir-server-logs`: read the notes (call 3); read the logs (call 1); recorded the result (call 7)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 2); ran the whole suite (call 7)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 6); filled the permit (call 6)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 6); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 3); read the config (call 2); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 3); opened the site (call 2); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); wrote the JSON (call 6)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 4); read the settings (call 3); read the owner notes (call 2); recorded the result (call 7)
- `ts-plugin-bug`: read the bus (call 8); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 3); recorded the result (call 1)
- `web-fact-search`: not seen: searched the web; recorded the result (call 8); opened a source (call 3)
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 2); replied (call 17)
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 7); recorded the result (call 8); wrote the dossier (call 7); not seen: opened a source
- `web-word-universe`: walked the site (call 1); wrote words.json (call 4); wrote the page (call 6); looked at it in a browser (call 14); recorded the result (call 4)
