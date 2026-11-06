# mengine-bench 2.6.0: opencode opencode v2.2.5 / deepseek/deepseek-flash (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **68.4** | 95.7 | 23/28 | 82.2 | 0.0 | 36 min 08 s | >= $0.15 (harness) | 5.23M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=deepseek-api; model=DeepSeek-V4.1-Flash-1017; tier=1; role=default; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-06, started 2026-11-06T16:34:36Z; bench at a7b75f4662c2; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | ok | 80% | 5/6 | 77 | 39.3 s | 0.0041 | 10 | 9 | 0.8 | 4.5k | 2.1k | 10 s |
| ds-ab-playtest | ok | 100% | 5/5 | 84 | 34.3 s | 0.0035 | 9 | 9 | 0.8 | 4.0k | 0.9k | 24 s |
| bo-pnl-runway | ok | 100% | 6/6 | 80 | 1 min 22 s | 0.0098 | 14 | 17 | 1.1 | 12.6k | 3.5k | 39 s |
| bo-reconcile | ok | 100% | 5/5 | 75 | 19.0 s | 0.0025 | 7 | 9 | 0.4 | 1.9k | 0.5k | 9 s |
| cmp-handoff | ok | 100% | 12/12 | 87 | 43.2 s | 0.0050 | 16 | 14 | 0.5 | 3.8k | 1.4k | 10 s |
| cfg-source-drift | ok | 100% | 5/5 | 96 | 44.7 s | 0.0042 | 15 | 15 | 0.6 | 3.8k | 1.1k | 8 s |
| doc-lab-pdf | ok | 100% | 7/7 | 84 | 23.4 s | 0.0024 | 8 | 7 | 0.6 | 2.1k | 0.8k | 15 s |
| ds-sql-funnel | ok | 100% | 5/5 | 94 | 36.9 s | 0.0047 | 11 | 11 | 0.8 | 4.2k | 1.1k | 6 s |
| ue-packaged-bug | ok | 100% | 6/6 | 89 | 28.3 s | 0.0033 | 7 | 8 | 0.8 | 3.2k | 0.9k | - |
| git-merge-conflict | ok | 100% | 7/7 | 97 | 25.8 s | 0.0025 | 10 | 9 | 0.6 | 1.9k | 0.4k | 12 s |
| infra-gpu-fit | ok | 100% | 7/7 | 68 | 11.1 s | 0.0017 | 3 | 4 | 0.4 | 1.4k | 0.4k | 4 s |
| ir-server-logs | ok | 100% | 7/7 | 87 | 32.9 s | 0.0040 | 10 | 13 | 0.7 | 3.0k | 1.1k | 23 s |
| gd-integration-repo | ok | 100% | 10/10 | 86 | 49.7 s | 0.0061 | 15 | 16 | 0.8 | 5.1k | 1.9k | 26 s |
| media-voice | ok | 100% | 4/4 | 97 | 42.8 s | 0.0021 | 9 | 9 | 0.8 | 1.7k | 0.3k | 4 s |
| file-media-edit | timeout (timeout) | 100% | 10/10 | 73 | 1 min 30 s | - | 21 | 20 | 0.8 | 7.1k | 2.8k | - |
| txt-regex-log | ok | 100% | 5/5 | 91 | 31.3 s | 0.0034 | 6 | 6 | 0.5 | 4.1k | 2.2k | 14 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (8004)) | 100% | 9/9 | 90 | 42.3 s | 0.0042 | 8 | 9 | 0.6 | 4.9k | 1.1k | 14 s |
| sec-leak-fix | ok | 100% | 10/10 | 85 | 40.7 s | 0.0045 | 12 | 15 | 1.0 | 4.9k | 1.2k | 10 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 86 | 1 min 43 s | 0.0104 | 44 | 53 | 0.3 | 7.4k | 1.6k | 23 s |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 9 | 1 min 00 s | - | 7 | 6 | 0.6 | 5.5k | 4.9k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 88 | 1 min 16 s | 0.0082 | 8 | 10 | 1.0 | 10.1k | 7.1k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 98 | 26.3 s | 0.0029 | 8 | 11 | 0.7 | 2.8k | 0.5k | 7 s |
| web-mondrian-landing | timeout (timeout, workspace archive repacked without tmp/edgeprofile (#205)) | 100% | 11/11 | 74 | 5 min 00 s | - | 39 | 43 | 0.7 | 37.0k | 22.9k | 120 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.621 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 76 | 5 min 26 s | 0.0350 | 27 | 51 | 1.4 | 47.9k | 22.2k | 98 s |
| web-fact-search | ok | 100% | 8/8 | 86 | 52.2 s | 0.0070 | 6 | 8 | 1.6 | 1.3k | 0.3k | 43 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:63849", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/156.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 91 | 1 min 02 s | 0.0061 | 25 | 31 | 0.4 | 4.7k | 1.2k | - |
| web-plan-ranking | ok | 100% | 9/9 | 80 | 1 min 24 s | 0.0149 | 16 | 23 | 0.8 | 11.8k | 5.5k | 69 s |
| web-word-universe | timeout (timeout, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 9/9 | 73 | 6 min 00 s | - | 51 | 74 | 1.1 | 47.2k | 20.4k | 130 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 8); recorded the result (call 8)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 4); used the chart of accounts (call 5); used the cash balance (call 3); recorded the result (call 7)
- `bo-reconcile`: read the notes (call 4); read the invoices (call 3); read the statement (call 5); recorded the result (call 7)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 4); recorded the result (call 13)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 3); recorded the result (call 6)
- `ds-sql-funnel`: read the rules (call 1); not seen: looked at the schema; excluded test accounts (call 3); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 5); read the game mode (call 4); recorded the result (call 7)
- `git-merge-conflict`: merged the branch (call 4); ran the tests (call 7); committed (call 8)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 3); read the logs (call 1); recorded the result (call 11)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 4); ran the whole suite (call 4)
- `media-voice`: used a speech engine (call 2); wrote the audio (call 3)
- `file-media-edit`: read the details (call 2); made the feed photo (call 15); filled the permit (call 16)
- `txt-regex-log`: wrote the regex (call 3); tried it in Python (call 4)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 7)
- `sec-leak-fix`: read the service (call 3); read the config (call 4); ran the tests (call 8)
- `cu-social-cycle`: made the image (call 10); opened the site (call 2); deleted the test post (call 37)
- `ds-sqlite-recover`: read the raw bytes (call 1); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 4); read the settings (call 3); read the owner notes (call 2); recorded the result (call 10)
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 3); looked at it in a browser (call 5); recorded the result (call 4)
- `web-fact-search`: not seen: searched the web; recorded the result (call 7); opened a source (call 1)
- `cu-webmail`: opened the mail app (call 4); downloaded the invoice (call 12); replied (call 17)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 18); wrote the dossier (call 19); opened a source (call 3)
- `web-word-universe`: walked the site (call 3); wrote words.json (call 15); wrote the page (call 16); looked at it in a browser (call 21); recorded the result (call 15)
