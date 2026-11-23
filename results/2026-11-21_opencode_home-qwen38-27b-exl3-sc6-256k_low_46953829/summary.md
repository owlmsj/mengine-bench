# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **65.1** | 78.6 | 16/29 | 65.6 | 24.2 | 32 min 45 s | $0.00 (local) | 4.92M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of pi-adapted merge; ctx=256k; cache=FP16; layout=native TP 2x RTX 5090; drafter=MTP n4 dynamic; temperature=0.6; finetune=harness-hub/Qwen3.8-27B-pi rev e786f849, THINKING OFF; study=pilot 7 control: pi-adapted run 1 (plugins via tunnel config); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-21, started 2026-11-21T11:08:07Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 75 | 1 min 44 s | 0.0000 | 9 | 8 | 0.8 | 6.2k | 0.0k | 49 s |
| py-async-cancel | timeout (timeout) | 80% | 5/6 | 44 | 1 min 00 s | 0.0000 | 7 | 6 | 0.6 | 1.7k | 0.0k | 6 s |
| ds-ab-playtest | ok | 100% | 5/5 | 95 | 1 min 12 s | 0.0000 | 7 | 7 | 0.0 | 3.0k | 0.0k | 49 s |
| bo-pnl-runway | ok | 100% | 6/6 | 84 | 50.6 s | 0.0000 | 11 | 13 | 0.0 | 3.9k | 0.0k | 18 s |
| bo-reconcile | ok | 25% | 2/5 | 26 | 29.9 s | 0.0000 | 8 | 10 | 0.0 | 2.0k | 0.0k | 9 s |
| cmp-handoff | timeout (timeout) | 27% | 4/12 | 25 | 1 min 30 s | 0.0000 | 23 | 23 | 0.0 | 8.6k | 0.0k | 11 s |
| cfg-source-drift | ok | 100% | 5/5 | 90 | 22.9 s | 0.0000 | 8 | 12 | 0.0 | 1.6k | 0.0k | 8 s |
| doc-lab-pdf | ok | 100% | 7/7 | 74 | 47.7 s | 0.0000 | 11 | 10 | 0.3 | 3.8k | 0.0k | 14 s |
| ds-sql-funnel | ok | 25% | 2/5 | 38 | 34.5 s | 0.0000 | 9 | 9 | 0.0 | 2.4k | 0.0k | 4 s |
| ue-packaged-bug | ok | 100% | 6/6 | 86 | 28.6 s | 0.0000 | 7 | 12 | 0.1 | 1.9k | 0.0k | 12 s |
| git-merge-conflict | ok | 100% | 7/7 | 94 | 39.0 s | 0.0000 | 12 | 14 | 0.4 | 2.3k | 0.0k | 22 s |
| infra-gpu-fit | ok | 100% | 7/7 | 81 | 19.0 s | 0.0000 | 5 | 6 | 0.0 | 1.3k | 0.0k | 7 s |
| ir-server-logs | timeout (timeout) | 0% | 1/7 | 6 | 1 min 00 s | 0.0000 | 2 | 5 | 0.0 | 0.3k | 0.0k | - |
| gd-integration-repo | ok | 88% | 9/10 | 71 | 42.8 s | 0.0000 | 13 | 27 | 0.0 | 3.0k | 0.0k | 24 s |
| media-voice | ok | 100% | 4/4 | 80 | 39.9 s | 0.0000 | 13 | 12 | 0.6 | 2.1k | 0.0k | 24 s |
| file-media-edit | ok | 100% | 10/10 | 82 | 1 min 24 s | 0.0000 | 27 | 29 | 0.5 | 5.5k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 28 | 1 min 00 s | 0.0000 | 12 | 11 | 0.0 | 5.0k | 0.0k | 4 s |
| rs-lock-bug | ok | 100% | 9/9 | 88 | 1 min 11 s | 0.0000 | 19 | 20 | 0.0 | 5.6k | 0.0k | 12 s |
| sec-leak-fix | ok | 75% | 8/10 | 71 | 31.4 s | 0.0000 | 8 | 11 | 0.0 | 2.1k | 0.0k | 10 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 89 | 1 min 02 s | 0.0000 | 25 | 24 | 0.2 | 2.4k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 20 | 1 min 00 s | 0.0000 | 8 | 7 | 0.4 | 2.1k | 0.0k | 28 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 78 | 48.2 s | 0.0000 | 8 | 10 | 0.0 | 2.9k | 0.0k | 18 s |
| ts-plugin-bug | ok | 100% | 8/8 | 96 | 34.8 s | 0.0000 | 9 | 13 | 0.1 | 2.5k | 0.0k | 10 s |
| web-mondrian-landing | ok | 100% | 11/11 | 75 | 1 min 27 s | 0.0000 | 16 | 15 | 0.0 | 5.1k | 0.0k | 25 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.289 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 90% | 11/12 | 39 | 3 min 12 s | 0.0000 | 19 | 18 | 0.4 | 17.1k | 0.0k | 47 s |
| web-fact-search | timeout (timeout) | 100% | 8/8 | 74 | 1 min 00 s | 0.0000 | 5 | 8 | 0.4 | 0.8k | 0.0k | 30 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:51685", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 89 | 1 min 33 s | 0.0000 | 31 | 30 | 0.1 | 5.8k | 0.0k | 56 s |
| web-plan-ranking | ok | 75% | 7/9 | 54 | 2 min 32 s | 0.0000 | 12 | 11 | 0.4 | 5.2k | 0.0k | 111 s |
| web-word-universe | ok | 75% | 7/9 | 50 | 3 min 07 s | 0.0000 | 20 | 20 | 0.4 | 13.6k | 0.0k | 21 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `bo-reconcile` unpaid invoices: expected ['INV-1008', 'INV-1030', 'INV-1033'], received ['INV-1002', 'INV-1003', 'INV-1004', 'INV-1005', 'INV-1006', 'INV-1007', 'INV-1008', 'INV-1009', 'INV-1010', 'INV-1013', 'INV-1017', 'INV-1019', 'INV-1023', 'INV-1026', 'INV-1029', 'INV-1030', 'INV-1031', 'INV-1032', 'INV-1033', 'INV-1035', 'IN
- `bo-reconcile` mismatched amounts: expected ['INV-1021', 'INV-1036'], received ['INV-1021']
- `bo-reconcile` invoiced vs paid on mismatches: expected [{'id': 'INV-1021', 'invoiced': 21320.36, 'paid': 21070.36}, {'id': 'INV-1036', 'invoiced': 8619.16, 'paid': 7757.24}], received [{'id': 'INV-1021', 'invoiced': '21320.36', 'paid': '21070.36'}]
- `cmp-handoff` summary exists and fits in 1000 characters: 1197 characters
- `cmp-handoff` answer file_line: expected 'a match for \\bstart_server\\.ps1\\b.{0,40}?\\b165\\b', received None
- `cmp-handoff` answer final_decode: expected 'a match for ^(?!.*37[.,]8)(?=.*(?<![\\w.,+-])38(?:[.,]0+)?(?!\\d|[.,]\\d))', received None
- `cmp-handoff` answer final_vram_mib: expected 'a match for (?<![\\w.,+-])7697(?:[.,]0+)?(?!\\w|[.,]\\d)', received ''
- `cmp-handoff` answer discarded_quant: expected 'a match for ^(?=.*\\bQ6(?:_?K)?\\b)(?!.*\\b(?!Q6(?:_?K)?\\b)(?:I?Q\\d+[A-Z0-9_]*|BF16|FP(?:16|32)|F(?:16|32))\\b)', received None
- `cmp-handoff` answer pending: expected 'a match for ^(?!.*\\broot\\b)(?=.*\\bREADME\\b)(?=.*\\b(?:update|fix|remove|edit|replace|check_vision|evals|stale|out of date))', received None
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received None
- `cmp-handoff` does not repeat the spilled VRAM as final: expected 'not 7881', received None
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'purchase', 'steamdeck': 'purchase'}
- `ir-server-logs` incident start: expected '2026-06-02 03:17:42', received None
- `ir-server-logs` incident end: expected '2026-06-02 03:53:31', received None
- `ir-server-logs` minutes down: expected 35.81666666666667, received None
- `ir-server-logs` June availability: expected 99.9170910493827, received None
- `ir-server-logs` SLO 99.9 met: expected True, received None
- `ir-server-logs` root cause = /data disk full: expected 'the /data disk was full', received None
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received ['2026', '2025', '2024', '2022', '2021', '2020', '2019']
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received ['2025']
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received ['2023', '2023']
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received ['2024', '2024']
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `sec-leak-fix` the old token is out of the final answers: the token literal appears in answer(s) [0]; expected it in none
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `3d-print-homage` counted the boats in the print: expected 3, received {'count': 9, 'arrangement': '3 groups of 3 boats each: left group under the great wave, middle group in the trough, right group on the right swell', 'type': 'fishing boats (oshiokuri-bune) with crew of 3 each, low-poly hulls with trim, cabin, mast and sail'}
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 3050, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'avó: missing 1 (pai), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 754, 'most_connected': ['palavra', 'tempo']}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); not seen: removed duplicate sessions; tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 3); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 4); not seen: recorded the result
- `cfg-source-drift`: read the readme (call 4); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 4); recorded the result (call 10)
- `git-merge-conflict`: merged the branch (call 9); ran the tests (call 12); committed (call 13)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); not seen: recorded the result
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 9); ran the whole suite (call 27)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 9)
- `file-media-edit`: read the details (call 2); made the feed photo (call 5); filled the permit (call 11)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 4); read the config (call 3); ran the tests (call 8)
- `cu-social-cycle`: made the image (call 1); opened the site (call 4); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 4); read the settings (call 2); read the owner notes (call 3); recorded the result (call 8)
- `ts-plugin-bug`: read the bus (call 6); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 3); looked at it in a browser (call 5); recorded the result (call 4)
- `web-fact-search`: not seen: searched the web; recorded the result (call 7); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 7); replied (call 7)
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 5); recorded the result (call 8); wrote the dossier (call 9); not seen: opened a source
- `web-word-universe`: walked the site (call 1); wrote words.json (call 4); wrote the page (call 11); looked at it in a browser (call 14); recorded the result (call 6)
