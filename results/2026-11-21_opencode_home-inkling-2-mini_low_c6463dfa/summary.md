# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/inkling-2-mini (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **82.4** | 91.4 | 24/29 | 70.8 | 86.9 | 13 min 56 s | $0.00 (local) | 9.24M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Inkling-2-Mini; runtime=SGLang lmsysorg/sglang:inkling-2-mini (0.0.0.dev1+inkling2); quant=native NVFP4 experts + MXFP8 (original release, rev ed40e7da); ctx=256k; cache=BF16; layout=TP 2x RTX 5090, fa4 attention; drafter=DSpark n8 (bundled mtp.safetensors); temperature=1.0 (model default); reasoning_effort=low; study=inkling 2 mini engine+quant pick, run 3; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-21, started 2026-11-21T17:38:38Z; bench at 8584f70e1346 (dirty tree); submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 71 | 1 min 00 s | 0.0000 | 18 | 17 | 0.8 | 9.9k | 1.0k | 29 s |
| py-async-cancel | ok | 80% | 5/6 | 69 | 12.7 s | 0.0000 | 7 | 7 | 0.5 | 2.4k | 0.8k | 7 s |
| ds-ab-playtest | ok | 0% | 0/5 | 33 | 13.0 s | 0.0000 | 9 | 8 | 0.4 | 1.8k | 0.6k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 66 | 19.3 s | 0.0000 | 18 | 17 | 0.4 | 3.1k | 2.2k | 7 s |
| bo-reconcile | ok | 100% | 5/5 | 83 | 14.3 s | 0.0000 | 10 | 9 | 0.4 | 2.7k | 0.9k | 10 s |
| cmp-handoff | ok | 100% | 12/12 | 76 | 23.1 s | 0.0000 | 16 | 14 | 0.4 | 3.0k | 0.8k | - |
| cfg-source-drift | ok | 100% | 5/5 | 90 | 10.1 s | 0.0000 | 7 | 6 | 0.4 | 0.9k | 0.4k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 70 | 14.6 s | 0.0000 | 11 | 11 | 0.4 | 2.0k | 1.4k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 75 | 19.8 s | 0.0000 | 15 | 14 | 0.4 | 3.5k | 1.2k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 73 | 18.9 s | 0.0000 | 11 | 10 | 0.4 | 2.9k | 1.4k | - |
| git-merge-conflict | ok | 100% | 7/7 | 90 | 14.2 s | 0.0000 | 10 | 9 | 0.5 | 2.3k | 0.8k | 9 s |
| infra-gpu-fit | ok | 100% | 7/7 | 63 | 11.1 s | 0.0000 | 6 | 5 | 0.4 | 1.4k | 0.9k | - |
| ir-server-logs | ok | 100% | 7/7 | 86 | 11.9 s | 0.0000 | 9 | 8 | 0.4 | 1.3k | 0.5k | - |
| gd-integration-repo | ok | 88% | 9/10 | 57 | 27.1 s | 0.0000 | 22 | 21 | 0.4 | 4.8k | 2.4k | 19 s |
| media-voice | ok | 100% | 4/4 | 81 | 10.6 s | 0.0000 | 8 | 7 | 0.5 | 0.9k | 0.4k | - |
| file-media-edit | ok | 100% | 10/10 | 81 | 40.1 s | 0.0000 | 30 | 29 | 0.5 | 6.1k | 3.4k | - |
| txt-regex-log | ok | 100% | 5/5 | 74 | 58.0 s | 0.0000 | 14 | 13 | 0.4 | 14.1k | 12.1k | 52 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (12012)) | 100% | 9/9 | 79 | 14.4 s | 0.0000 | 7 | 6 | 0.5 | 2.6k | 1.0k | 8 s |
| sec-leak-fix | ok | 100% | 10/10 | 80 | 10.5 s | 0.0000 | 8 | 7 | 0.4 | 1.9k | 0.3k | 6 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 85 | 41.9 s | 0.0000 | 53 | 52 | 0.0 | 4.4k | 2.6k | - |
| ds-sqlite-recover | ok | 20% | 2/6 | 18 | 43.5 s | 0.0000 | 15 | 14 | 0.4 | 9.0k | 7.1k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 78 | 21.9 s | 0.0000 | 14 | 13 | 0.4 | 3.1k | 2.1k | 18 s |
| ts-plugin-bug | ok | 100% | 8/8 | 87 | 12.2 s | 0.0000 | 8 | 7 | 0.4 | 2.0k | 0.5k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 72 | 23.0 s | 0.0000 | 11 | 10 | 0.4 | 4.8k | 0.5k | 13 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.227 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 57 | 1 min 09 s | 0.0000 | 16 | 15 | 0.4 | 9.9k | 1.0k | 44 s |
| web-fact-search | ok | 100% | 8/8 | 80 | 32.3 s | 0.0000 | 19 | 19 | 0.3 | 1.8k | 0.7k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:61371", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 73 | 48.8 s | 0.0000 | 31 | 30 | 0.0 | 4.0k | 1.4k | - |
| web-plan-ranking | ok | 62% | 6/9 | 43 | 35.5 s | 0.0000 | 18 | 17 | 0.1 | 5.8k | 3.1k | 29 s |
| web-word-universe | ok | 100% | 9/9 | 62 | 1 min 45 s | 0.0000 | 54 | 53 | 0.4 | 19.3k | 8.5k | 15 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `ds-ab-playtest` no writes outside the task workspace: expected "no filesystem changes outside the workspace, in the task's parent and run directories", received ['parent/result.json']
- `ds-ab-playtest` deduplicated session counts: expected {'sessions_a': 900, 'sessions_b': 900}, received {'sessions_a': None, 'sessions_b': None}
- `ds-ab-playtest` completion rates: expected (0.38, 0.4666666666666667), received {'completion_rate_a': None, 'completion_rate_b': None}
- `ds-ab-playtest` the gain is significant: expected '0.000198469 +/- 0.00015 (pooled two-sided z-test or equivalent), or a containing upper bound <= 0.001', received None
- `ds-ab-playtest` ship decision: expected True, received None
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received [('first aid kit?', 7.0), ('compass@/', 7.0), ('camp stove', 2.0), ('sleeping bag', 2.0)]
- `web-plan-ranking` launch dates: expected {'Collor II': ['1991-01-31']}, received {'Collor II': '1991-01-15'}
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1], 'Real': [2477.15, 22.41]}, received {'Cruzado': [226.0, 228.3], 'Bresser': [147.1, 629.1], 'Verao': [629.1, 2947.7], 'Collor I': [1430.7, 432.8
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received ['Real', 'Collor II', 'Collor I']

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 4); looked at it in a browser (call 5)
- `py-async-cancel`: wrote run.py (call 2); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 5); recorded the result (call 8)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 2); used the chart of accounts (call 2); used the cash balance (call 2); recorded the result (call 15)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 6); recorded the result (call 14)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 8); recorded the result (call 11)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 4); excluded test accounts (call 11); recorded the result (call 13)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 2); recorded the result (call 10)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 8); committed (call 9)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 8)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 2); ran the whole suite (call 5)
- `media-voice`: used a speech engine (call 2); wrote the audio (call 5)
- `file-media-edit`: read the details (call 2); made the feed photo (call 15); filled the permit (call 18)
- `txt-regex-log`: wrote the regex (call 5); tried it in Python (call 6)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 4)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 5)
- `cu-social-cycle`: made the image (call 1); opened the site (call 8); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); wrote the JSON (call 14)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 5); read the settings (call 4); read the owner notes (call 4); recorded the result (call 12)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 4); looked at it in a browser (call 5)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 6); recorded the result (call 14)
- `web-fact-search`: not seen: searched the web; recorded the result (call 19); opened a source (call 3)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 11); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 2); wrote the dossier (call 17); opened a source (call 4)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 14); wrote the page (call 18); looked at it in a browser (call 23); recorded the result (call 14)
