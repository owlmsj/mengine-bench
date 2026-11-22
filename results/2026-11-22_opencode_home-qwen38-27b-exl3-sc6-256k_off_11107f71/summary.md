# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (off)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **67.4** | 77.6 | 16/29 | 63.3 | 55.7 | 23 min 17 s | $0.00 (local) | 6.62M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715, THINKING OFF; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=EXL3 8.0 bpw, head 8 bits, of super-adapter merge; cache=FP16; drafter=MTP n4 dynamic; layout=native TP 2x RTX 5090; sampling=temperature 0.6 (forced), top_k 20, top_p 0.95; study=EXL3 8 bpw vs 6 bpw (2026-11-22); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-22, started 2026-11-22T16:17:10Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 83% | 7/8 | 68 | 59.5 s | 0.0000 | 12 | 11 | 0.1 | 6.7k | 0.0k | 28 s |
| py-async-cancel | ok | 40% | 3/6 | 41 | 38.0 s | 0.0000 | 13 | 12 | 0.4 | 4.0k | 0.0k | 6 s |
| ds-ab-playtest | ok | 100% | 5/5 | 77 | 47.8 s | 0.0000 | 5 | 5 | 0.0 | 2.6k | 0.0k | 37 s |
| bo-pnl-runway | ok | 40% | 3/6 | 40 | 18.1 s | 0.0000 | 6 | 8 | 0.0 | 1.7k | 0.0k | 8 s |
| bo-reconcile | ok | 100% | 5/5 | 83 | 18.9 s | 0.0000 | 6 | 8 | 0.0 | 1.9k | 0.0k | 7 s |
| cmp-handoff | ok | 91% | 11/12 | 68 | 29.8 s | 0.0000 | 12 | 11 | 0.0 | 2.7k | 0.0k | 8 s |
| cfg-source-drift | ok | 100% | 5/5 | 93 | 15.5 s | 0.0000 | 8 | 11 | 0.0 | 1.4k | 0.0k | 7 s |
| doc-lab-pdf | ok | 100% | 7/7 | 72 | 27.6 s | 0.0000 | 10 | 9 | 0.3 | 2.7k | 0.0k | 10 s |
| ds-sql-funnel | ok | 25% | 2/5 | 30 | 23.9 s | 0.0000 | 9 | 9 | 0.0 | 2.5k | 0.0k | 3 s |
| ue-packaged-bug | ok | 60% | 4/6 | 30 | 20.1 s | 0.0000 | 8 | 14 | 0.0 | 2.1k | 0.0k | 6 s |
| git-merge-conflict | ok | 100% | 7/7 | 89 | 18.7 s | 0.0000 | 7 | 6 | 0.4 | 1.7k | 0.0k | 10 s |
| infra-gpu-fit | ok | 100% | 7/7 | 81 | 13.5 s | 0.0000 | 4 | 5 | 0.0 | 1.5k | 0.0k | 7 s |
| ir-server-logs | timeout (timeout) | 0% | 1/7 | 6 | 1 min 00 s | 0.0000 | 2 | 5 | 0.0 | 0.3k | 0.0k | - |
| gd-integration-repo | ok | 88% | 9/10 | 69 | 47.3 s | 0.0000 | 13 | 25 | 0.0 | 4.8k | 0.0k | 19 s |
| media-voice | ok | 100% | 4/4 | 80 | 24.6 s | 0.0000 | 9 | 8 | 0.8 | 2.1k | 0.0k | 4 s |
| file-media-edit | ok | 88% | 9/10 | 63 | 1 min 07 s | 0.0000 | 21 | 22 | 0.5 | 7.1k | 0.0k | - |
| txt-regex-log | ok | 100% | 5/5 | 66 | 42.6 s | 0.0000 | 13 | 12 | 0.0 | 5.1k | 0.0k | 3 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (17876)) | 100% | 9/9 | 81 | 16.0 s | 0.0000 | 6 | 8 | 0.0 | 1.6k | 0.0k | 7 s |
| sec-leak-fix | ok | 75% | 8/10 | 70 | 15.4 s | 0.0000 | 8 | 11 | 0.0 | 1.6k | 0.0k | 5 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 84 | 41.1 s | 0.0000 | 33 | 33 | 0.0 | 2.8k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 20 | 1 min 00 s | 0.0000 | 8 | 7 | 0.4 | 3.6k | 0.0k | 31 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 69 | 26.3 s | 0.0000 | 8 | 9 | 0.0 | 2.4k | 0.0k | 13 s |
| ts-plugin-bug | ok | 100% | 8/8 | 95 | 26.9 s | 0.0000 | 9 | 12 | 0.0 | 2.7k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 77 | 51.9 s | 0.0000 | 12 | 11 | 0.1 | 5.1k | 0.0k | 14 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.288 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 49 | 1 min 23 s | 0.0000 | 19 | 18 | 0.0 | 9.5k | 0.0k | 22 s |
| web-fact-search | ok | 100% | 8/8 | 88 | 55.0 s | 0.0000 | 8 | 11 | 0.4 | 1.4k | 0.0k | 34 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:65399", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 87 | 38.0 s | 0.0000 | 20 | 20 | 0.0 | 3.2k | 0.0k | - |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 11 | 3 min 30 s | 0.0000 | 6 | 8 | 0.5 | 0.8k | 0.0k | - |
| web-word-universe | ok | 62% | 6/9 | 48 | 3 min 20 s | 0.0000 | 60 | 60 | 0.0 | 21.0k | 0.0k | 16 s |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]
- `py-async-cancel` Ctrl+C below the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 2, 'cleaned': 2}
- `py-async-cancel` Ctrl+C at the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 2, 'cleaned': 2}
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 2, 'cleaned': 2}
- `bo-pnl-runway` ebitda per month: 2026-01: expected -210278.96, received -203812.19
- `bo-pnl-runway` 3-month average burn: expected 197288.23, received 190820.54
- `bo-pnl-runway` runway in months: expected 9.363713182484327, received 9.68
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received 'llama-server --no-mmproj-offload -ub 512'
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 302}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 77}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'tutorial_complete', 'steamdeck': 'tutorial_complete'}
- `ue-packaged-bug` crash fixed: the score tracker survives garbage collection: ScoreTracker is not kept alive by UPROPERTY, TStrongObjectPtr, AddToRoot or a reported reference
- `ue-packaged-bug` the plain C++ pointer stays out of reflection: UPROPERTY on FArenaStats stops the build: it is not a reflected type
- `ir-server-logs` incident start: expected '2026-06-02 03:17:42', received None
- `ir-server-logs` incident end: expected '2026-06-02 03:53:31', received None
- `ir-server-logs` minutes down: expected 35.81666666666667, received None
- `ir-server-logs` June availability: expected 99.9170910493827, received None
- `ir-server-logs` SLO 99.9 met: expected True, received None
- `ir-server-logs` root cause = /data disk full: expected 'the /data disk was full', received None
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received 'Saturday 5 December 2026'
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `sec-leak-fix` the old token is out of the final answers: the token literal appears in answer(s) [0]; expected it in none
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
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 3 (contato, dicionário criativo, sobre)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'contato: missing 0 (none), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 743, 'most_connected': 'palavra'}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); not seen: removed duplicate sessions; tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 4); used the chart of accounts (call 5); used the cash balance (call 3); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 4); recorded the result (call 11)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 5); recorded the result (call 11)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 5); committed (call 6)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); not seen: recorded the result
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); ran the whole suite (call 19)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 4)
- `file-media-edit`: read the details (call 2); made the feed photo (call 5); filled the permit (call 8)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 5)
- `rs-lock-bug`: read the crate (call 6); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 4); read the config (call 2); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 2); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 4); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 4); read the settings (call 3); read the owner notes (call 2); recorded the result (call 8)
- `ts-plugin-bug`: read the bus (call 6); ran the tests (call 9)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 10); opened a source (call 1)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); replied (call 15)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: recorded the result; not seen: wrote the dossier; not seen: opened a source
- `web-word-universe`: walked the site (call 1); wrote words.json (call 4); wrote the page (call 6); looked at it in a browser (call 9); recorded the result (call 4)
