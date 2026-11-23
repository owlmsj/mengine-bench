# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **75.4** | 88.8 | 20/29 | 71.6 | 44.9 | 26 min 31 s | $0.00 (local) | 4.68M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of super-adapter merge; ctx=256k; cache=FP16; layout=native TP 2x RTX 5090; drafter=MTP n4 dynamic; temperature=0.6; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715 (pi+hermes+opencode at 1/2), THINKING OFF; study=pilot 7 control: super-adapter off run 2; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-21, started 2026-11-21T13:42:25Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 49 | 2 min 56 s | 0.0000 | 18 | 17 | 2.2 | 8.7k | 0.0k | 60 s |
| py-async-cancel | ok | 80% | 5/6 | 66 | 37.2 s | 0.0000 | 9 | 8 | 0.0 | 2.7k | 0.0k | 6 s |
| ds-ab-playtest | ok | 100% | 5/5 | 85 | 57.7 s | 0.0000 | 5 | 5 | 0.0 | 1.8k | 0.0k | 44 s |
| bo-pnl-runway | ok | 100% | 6/6 | 76 | 32.1 s | 0.0000 | 9 | 10 | 0.0 | 2.2k | 0.0k | 13 s |
| bo-reconcile | ok | 100% | 5/5 | 76 | 22.7 s | 0.0000 | 6 | 7 | 0.0 | 1.6k | 0.0k | 9 s |
| cmp-handoff | ok | 82% | 10/12 | 50 | 26.7 s | 0.0000 | 7 | 5 | 0.0 | 1.5k | 0.0k | 9 s |
| cfg-source-drift | ok | 100% | 5/5 | 93 | 20.7 s | 0.0000 | 8 | 11 | 0.0 | 1.3k | 0.0k | 9 s |
| doc-lab-pdf | ok | 100% | 7/7 | 72 | 38.5 s | 0.0000 | 8 | 7 | 0.4 | 3.2k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 80 | 23.9 s | 0.0000 | 7 | 7 | 0.4 | 1.6k | 0.0k | 4 s |
| ue-packaged-bug | ok | 100% | 6/6 | 89 | 28.8 s | 0.0000 | 7 | 12 | 0.0 | 2.0k | 0.0k | 13 s |
| git-merge-conflict | ok | 100% | 7/7 | 95 | 24.2 s | 0.0000 | 9 | 8 | 0.5 | 1.3k | 0.0k | 11 s |
| infra-gpu-fit | ok | 100% | 7/7 | 88 | 20.2 s | 0.0000 | 5 | 6 | 0.0 | 1.4k | 0.0k | 7 s |
| ir-server-logs | ok | 100% | 7/7 | 88 | 52.3 s | 0.0000 | 7 | 8 | 0.0 | 1.6k | 0.0k | 42 s |
| gd-integration-repo | ok | 88% | 9/10 | 75 | 26.8 s | 0.0000 | 6 | 14 | 0.1 | 1.7k | 0.0k | 17 s |
| media-voice | ok | 100% | 4/4 | 88 | 24.3 s | 0.0000 | 7 | 6 | 1.1 | 0.9k | 0.0k | - |
| file-media-edit | ok | 38% | 5/10 | 44 | 1 min 09 s | 0.0000 | 20 | 19 | 0.5 | 5.1k | 0.0k | 9 s |
| txt-regex-log | timeout (timeout) | 75% | 4/5 | 57 | 1 min 00 s | 0.0000 | 15 | 14 | 0.0 | 4.3k | 0.0k | 10 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (30880)) | 100% | 9/9 | 81 | 24.6 s | 0.0000 | 6 | 8 | 0.0 | 1.8k | 0.0k | 13 s |
| sec-leak-fix | ok | 88% | 9/10 | 76 | 21.9 s | 0.0000 | 6 | 9 | 0.0 | 1.5k | 0.0k | 9 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 90 | 52.0 s | 0.0000 | 23 | 23 | 0.0 | 2.0k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 10 | 1 min 00 s | 0.0000 | 5 | 4 | 0.2 | 1.7k | 0.0k | 26 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 80 | 37.7 s | 0.0000 | 8 | 9 | 0.0 | 2.4k | 0.0k | 14 s |
| ts-plugin-bug | ok | 100% | 8/8 | 82 | 18.9 s | 0.0000 | 6 | 10 | 0.0 | 1.1k | 0.0k | 9 s |
| web-mondrian-landing | ok | 100% | 11/11 | 80 | 1 min 40 s | 0.0000 | 14 | 13 | 0.5 | 7.5k | 0.0k | 50 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.417 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 48 | 1 min 19 s | 0.0000 | 11 | 11 | 0.0 | 6.0k | 0.0k | 33 s |
| web-fact-search | ok | 100% | 8/8 | 84 | 43.4 s | 0.0000 | 6 | 9 | 0.6 | 1.2k | 0.0k | 29 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:55695", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 86 | 1 min 39 s | 0.0000 | 31 | 30 | 0.5 | 5.1k | 0.0k | - |
| web-plan-ranking | ok | 62% | 6/9 | 41 | 2 min 53 s | 0.0000 | 21 | 20 | 0.4 | 5.9k | 0.0k | 132 s |
| web-word-universe | ok | 62% | 6/9 | 47 | 2 min 21 s | 0.0000 | 17 | 18 | 0.2 | 11.1k | 0.0k | 22 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `cmp-handoff` answer final_decode: expected 'a match for ^(?!.*37[.,]8)(?=.*(?<![\\w.,+-])38(?:[.,]0+)?(?!\\d|[.,]\\d))', received '37.8-38.0 t/s'
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received '--no-mmproj-offload -ub 512'
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received ['2023-02-30', '2023-02-29', '2023-09-30']
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor II': ['1991-01-31']}, received {'Cruzado': '1986-02-01', 'Bresser': '1987-02-15', 'Verao': '1989-02-15', 'Collor II': '1991-03-15'}
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Collor I': [10]}, received {'Cruzado': 12, 'Bresser': 24, 'Collor I': 12}
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2566, 'urls': 1, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 3 (coracoes, paixoes, saudades)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'advogado: missing 0 (none), extra 1 (coracoes)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 757, 'most_connected': [{'word': 'palavra', 'links': 16}, {'word': 'tempo', 'links': 16}, {'word': 'madrugada', 'links': 9}, {'word': 'violão', 'links': 8}, {'word': 'pulmão', 'lin

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 5)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 5); recorded the result (call 10)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 7); committed (call 7)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 8)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); ran the whole suite (call 14)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 5)
- `file-media-edit`: read the details (call 2); made the feed photo (call 9); filled the permit (call 9)
- `txt-regex-log`: wrote the regex (call 12); tried it in Python (call 2)
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 3); read the config (call 2); ran the tests (call 8)
- `cu-social-cycle`: made the image (call 1); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: not seen: read the raw bytes; not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 5); read the settings (call 2); read the owner notes (call 3); recorded the result (call 8)
- `ts-plugin-bug`: read the bus (call 6); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 4); recorded the result (call 3)
- `web-fact-search`: not seen: searched the web; recorded the result (call 9); opened a source (call 3)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 18); wrote the dossier (call 19); opened a source (call 5)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 4); wrote the page (call 6); looked at it in a browser (call 13); recorded the result (call 4)
