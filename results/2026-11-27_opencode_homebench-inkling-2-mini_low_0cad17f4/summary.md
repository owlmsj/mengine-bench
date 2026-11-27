# mengine-bench 2.8.0: opencode opencode v2.3.2 / homebench/inkling-2-mini (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **80.1** | 88.4 | 22/29 | 67.9 | 91.8 | 12 min 27 s | >= $0.00 | 5.80M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-27, started 2026-11-27T17:12:40Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 83% | 7/8 | 69 | 51.5 s | 0.0000 | 18 | 17 | 0.3 | 11.9k | 1.2k | 32 s |
| py-async-cancel | ok | 80% | 5/6 | 58 | 12.7 s | 0.0000 | 6 | 5 | 0.5 | 1.9k | 0.6k | 4 s |
| ds-ab-playtest | ok | 100% | 5/5 | 73 | 13.0 s | 0.0000 | 10 | 9 | 0.3 | 1.7k | 0.5k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 68 | 16.0 s | 0.0000 | 11 | 10 | 0.3 | 2.8k | 1.2k | - |
| bo-reconcile | ok | 100% | 5/5 | 75 | 8.0 s | 0.0000 | 5 | 4 | 0.3 | 1.2k | 0.3k | - |
| cmp-handoff | ok | 36% | 5/12 | 28 | 46.3 s | 0.0000 | 26 | 25 | 0.3 | 4.8k | 2.3k | 9 s |
| cfg-source-drift | ok | 100% | 5/5 | 89 | 6.9 s | 0.0000 | 5 | 4 | 0.4 | 0.7k | 0.3k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 72 | 12.7 s | 0.0000 | 7 | 6 | 0.3 | 2.2k | 1.8k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 79 | 15.9 s | 0.0000 | 13 | 12 | 0.4 | 2.9k | 1.6k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 62 | 16.8 s | 0.0000 | 10 | 12 | 0.3 | 3.1k | 1.4k | 13 s |
| git-merge-conflict | ok | 100% | 7/7 | 87 | 11.8 s | 0.0000 | 11 | 10 | 0.4 | 1.8k | 0.6k | 7 s |
| infra-gpu-fit | ok | 100% | 7/7 | 77 | 8.1 s | 0.0000 | 4 | 3 | 0.4 | 1.1k | 0.7k | - |
| ir-server-logs | ok | 100% | 7/7 | 84 | 11.8 s | 0.0000 | 11 | 10 | 0.3 | 1.4k | 0.6k | - |
| gd-integration-repo | ok | 88% | 9/10 | 63 | 17.4 s | 0.0000 | 11 | 10 | 0.3 | 2.6k | 1.2k | - |
| media-voice | ok | 100% | 4/4 | 82 | 10.8 s | 0.0000 | 8 | 7 | 0.6 | 1.0k | 0.2k | - |
| file-media-edit | ok | 100% | 10/10 | 79 | 43.0 s | 0.0000 | 35 | 34 | 0.4 | 6.8k | 4.2k | - |
| txt-regex-log | ok | 100% | 5/5 | 90 | 27.1 s | 0.0000 | 5 | 4 | 0.3 | 6.1k | 5.4k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (19532)) | 100% | 9/9 | 71 | 15.4 s | 0.0000 | 9 | 8 | 0.4 | 2.6k | 1.1k | 10 s |
| sec-leak-fix | ok | 100% | 10/10 | 80 | 15.6 s | 0.0000 | 11 | 11 | 0.5 | 3.1k | 0.8k | 8 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 82 | 25.1 s | 0.0000 | 39 | 38 | 0.0 | 3.4k | 2.3k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 9 | 1 min 00 s | - | 16 | 15 | 0.3 | 14.8k | 13.7k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 72 | 16.9 s | 0.0000 | 12 | 11 | 0.3 | 2.6k | 1.1k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 79 | 9.5 s | 0.0000 | 7 | 6 | 0.3 | 1.6k | 0.4k | 5 s |
| web-mondrian-landing | ok | 100% | 11/11 | 81 | 19.5 s | 0.0000 | 14 | 13 | 0.1 | 4.3k | 0.7k | 10 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.0 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 29 | 1 min 11 s | 0.0000 | 23 | 22 | 0.3 | 8.9k | 2.3k | 44 s |
| web-fact-search | ok | 0% | 1/8 | 24 | 33.7 s | 0.0000 | 10 | 12 | 0.4 | 1.4k | 0.6k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:60027", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 86 | 21.7 s | 0.0000 | 25 | 25 | 0.0 | 3.3k | 1.2k | - |
| web-plan-ranking | ok | 75% | 7/9 | 50 | 48.4 s | 0.0000 | 9 | 8 | 0.3 | 5.6k | 3.5k | - |
| web-word-universe | ok | 100% | 9/9 | 70 | 1 min 21 s | 0.0000 | 35 | 35 | 0.3 | 19.8k | 11.0k | 16 s |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `cmp-handoff` summary keeps `--no-mmproj-offload`: `--no-mmproj-offload` is not in the summary
- `cmp-handoff` summary keeps `-ub 512`: `-ub 512` is not in the summary
- `cmp-handoff` summary keeps `7697`: `7697` is not in the summary
- `cmp-handoff` answer final_decode: expected 'a match for ^(?!.*37[.,]8)(?=.*(?<![\\w.,+-])38(?:[.,]0+)?(?!\\d|[.,]\\d))', received 'not measured/verified - 37.8 t/s is stale and must not be used (WDDM ceiling 7881 MiB, 1494 MiB Shared Usage spill); transcript session/transcript.md is missing, nothing re-verified'
- `cmp-handoff` answer final_vram_mib: expected 'a match for (?<![\\w.,+-])7697(?:[.,]0+)?(?!\\w|[.,]\\d)', received '7881'
- `cmp-handoff` answer discarded_quant: expected 'a match for ^(?=.*\\bQ6(?:_?K)?\\b)(?!.*\\b(?!Q6(?:_?K)?\\b)(?:I?Q\\d+[A-Z0-9_]*|BF16|FP(?:16|32)|F(?:16|32))\\b)', received 'not recorded in HANDOFF.md or session transcript (missing)'
- `cmp-handoff` does not repeat the spilled VRAM as final: expected 'not 7881', received '7881'
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `web-fact-search` sqlite_3_40_0_release_date value: expected '2022-11-16', received None
- `web-fact-search` sqlite_3_40_0_release_date primary source: expected 'an http(s) URL on sqlite.org', received None
- `web-fact-search` postgresql_15_0_release_date value: expected '2022-10-13', received None
- `web-fact-search` postgresql_15_0_release_date primary source: expected 'an http(s) URL on postgresql.org', received None
- `web-fact-search` unicode_15_0_characters_added value: expected 4489, received None
- `web-fact-search` unicode_15_0_characters_added primary source: expected 'an http(s) URL on unicode.org', received None
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2374, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 3); looked at it in a browser (call 4)
- `py-async-cancel`: wrote run.py (call 2); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 2); removed duplicate sessions (call 4); tested significance (call 9); recorded the result (call 9)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 4); used the chart of accounts (call 3); used the cash balance (call 3); recorded the result (call 10)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 4)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 8); recorded the result (call 25)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); not seen: extracted the text; recorded the result (call 6)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 7); recorded the result (call 11)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 2); recorded the result (call 12)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 9); committed (call 10)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 3)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 10)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 5); ran the whole suite (call 7)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 7)
- `file-media-edit`: read the details (call 2); made the feed photo (call 20); filled the permit (call 22)
- `txt-regex-log`: wrote the regex (call 3); tried it in Python (call 4)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 5)
- `sec-leak-fix`: read the service (call 3); read the config (call 3); ran the tests (call 4)
- `cu-social-cycle`: made the image (call 1); opened the site (call 1); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 4); read the settings (call 3); read the owner notes (call 3); recorded the result (call 11)
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 4)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 4); looked at it in a browser (call 7)
- `3d-print-homage`: wrote the scene (call 5); looked at it in a browser (call 10); recorded the result (call 17)
- `web-fact-search`: not seen: searched the web; recorded the result (call 2); opened a source (call 4)
- `cu-webmail`: opened the mail app (call 3); downloaded the invoice (call 9); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 7); recorded the result (call 6); wrote the dossier (call 8); not seen: opened a source
- `web-word-universe`: walked the site (call 1); wrote words.json (call 10); wrote the page (call 14); looked at it in a browser (call 23); recorded the result (call 10)
