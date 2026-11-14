# mengine-bench 2.8.0: opencode opencode v2.2.5 / moonshotai/kimi-k3.1-pro-highspeed (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **85.3** | 94.2 | 24/29 | 81.7 | 67.8 | 19 min 39 s | $3.19 | 3.25M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=moonshotai; model=kimi-k3.1-pro-highspeed; tier=1; role=dev-r; price_source=models.dev catalog in OpenCode 2.2.5 (moonshotai, 2026-11-14); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-14, started 2026-11-14T16:55:22Z; bench at a46b3115d792; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 83% | 7/8 | 76 | 1 min 31 s | 0.2600 | 13 | 12 | 0.2 | 6.9k | 0.5k | 47 s |
| py-async-cancel | ok | 100% | 6/6 | 91 | 27.4 s | 0.0515 | 4 | 3 | 3.5 | 1.7k | 0.5k | 10 s |
| ds-ab-playtest | ok | 100% | 5/5 | 87 | 28.6 s | 0.0755 | 7 | 7 | 0.5 | 1.7k | 0.4k | 16 s |
| bo-pnl-runway | ok | 100% | 6/6 | 81 | 1 min 02 s | 0.1608 | 10 | 14 | 1.2 | 4.6k | 0.8k | 16 s |
| bo-reconcile | ok | 100% | 5/5 | 92 | 19.6 s | 0.0542 | 5 | 6 | 0.1 | 1.3k | 0.3k | 6 s |
| cmp-handoff | ok | 91% | 11/12 | 75 | 32.8 s | 0.0781 | 9 | 7 | 0.3 | 1.5k | 0.5k | 6 s |
| cfg-source-drift | ok | 100% | 5/5 | 94 | 16.9 s | 0.0352 | 5 | 7 | 0.3 | 0.8k | 0.1k | 6 s |
| doc-lab-pdf | ok | 100% | 7/7 | 82 | 25.7 s | 0.0525 | 7 | 7 | 0.9 | 1.4k | 0.2k | 13 s |
| ds-sql-funnel | ok | 100% | 5/5 | 84 | 27.5 s | 0.0566 | 5 | 5 | 1.4 | 1.7k | 0.4k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 90 | 18.5 s | 0.0497 | 5 | 12 | 0.3 | 1.1k | 0.1k | 8 s |
| git-merge-conflict | ok | 100% | 7/7 | 96 | 22.1 s | 0.0544 | 6 | 6 | 0.8 | 1.3k | 0.1k | 11 s |
| infra-gpu-fit | ok | 100% | 7/7 | 90 | 17.0 s | 0.0368 | 4 | 5 | 0.3 | 1.0k | 0.2k | 4 s |
| ir-server-logs | ok | 100% | 7/7 | 72 | 17.0 s | 0.3202 | 4 | 6 | 0.1 | 0.7k | 0.1k | 9 s |
| gd-integration-repo | ok | 100% | 10/10 | 92 | 33.6 s | 0.1078 | 9 | 23 | 0.4 | 2.2k | 0.4k | 20 s |
| media-voice | ok | 100% | 4/4 | 83 | 14.8 s | 0.0289 | 3 | 2 | 1.9 | 0.8k | 0.2k | - |
| file-media-edit | ok | 100% | 10/10 | 81 | 50.7 s | 0.1223 | 10 | 12 | 0.5 | 2.4k | 0.8k | - |
| txt-regex-log | ok | 100% | 5/5 | 92 | 19.8 s | 0.0407 | 4 | 3 | 0.8 | 1.2k | 0.4k | 7 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (3540)) | 100% | 9/9 | 89 | 30.4 s | 0.0699 | 8 | 11 | 0.3 | 1.8k | 0.3k | 8 s |
| sec-leak-fix | ok | 100% | 10/10 | 90 | 27.5 s | 0.0680 | 9 | 13 | 0.0 | 1.5k | 0.3k | 10 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 92 | 1 min 18 s | 0.1968 | 26 | 27 | 0.0 | 3.1k | 0.2k | - |
| ds-sqlite-recover | ok | 20% | 2/6 | 25 | 21.0 s | 0.0535 | 5 | 4 | 0.8 | 1.3k | 0.4k | 11 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 89 | 28.8 s | 0.1048 | 7 | 10 | 0.4 | 1.7k | 0.4k | 19 s |
| ts-plugin-bug | ok | 100% | 8/8 | 96 | 21.3 s | 0.0495 | 8 | 7 | 0.1 | 1.0k | 0.1k | 7 s |
| web-mondrian-landing | ok | 100% | 11/11 | 79 | 1 min 05 s | 0.1597 | 14 | 14 | 0.1 | 3.7k | 0.4k | 21 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.499 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 79 | 1 min 59 s | 0.2597 | 13 | 15 | 0.3 | 7.3k | 1.2k | 55 s |
| web-fact-search | ok | 100% | 8/8 | 81 | 19.8 s | 0.0817 | 6 | 7 | 0.4 | 1.0k | 0.2k | 8 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:52924", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 89 | 1 min 05 s | 0.1537 | 20 | 19 | 0.3 | 2.9k | 0.2k | - |
| web-plan-ranking | ok | 75% | 7/9 | 42 | 1 min 30 s | 0.1397 | 8 | 9 | 0.9 | 4.0k | 0.8k | 60 s |
| web-word-universe | ok | 62% | 6/9 | 59 | 1 min 28 s | 0.2630 | 16 | 15 | 0.5 | 5.9k | 0.4k | 12 s |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received 'Not specified in HANDOFF.md; re-run the full-context decode measurement after any config change and check Dedicated + Shared GPU memory.'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received ['lantern', 'rope coil']
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received ['water filter']
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received ['trail map']
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received [('matchbox', 13.0), ('tent stake', 3.5), ('sleeping bag', 280.0), ('camp stove', 54.0)]
- `web-plan-ranking` inflation before and after: expected {'Bresser': [79.66, 980.21], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1]}, received {'Bresser': [62.39, 980.21], 'Collor I': [1782.89, 472.7], 'Collor II': [1620.97, 2477.15]}
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 3211, 'urls': 1, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 2 (contato, sobre)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'açougueiro: missing 1 (enfermeira), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 252, 'relations': 734, 'most_connected': 'palavra'}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 6)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 2); recorded the result (call 6)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 5)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 4); recorded the result (call 6)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 3); recorded the result (call 3)
- `ue-packaged-bug`: read the crash log (call 6); read the game mode (call 4); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 4); ran the tests (call 6); committed (call 6)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 2); read the policy (call 1); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 3); ran the integration test (call 10); ran the whole suite (call 22)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 8); filled the permit (call 8)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 6); ran the tests (call 9)
- `sec-leak-fix`: read the service (call 6); read the config (call 5); ran the tests (call 13)
- `cu-social-cycle`: made the image (call 1); opened the site (call 2); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 5); read the settings (call 3); read the owner notes (call 2); recorded the result (call 9)
- `ts-plugin-bug`: read the bus (call 3); ran the tests (call 6)
- `web-mondrian-landing`: read the fact sheet (call 2); wrote the page (call 4); looked at it in a browser (call 5)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 6); recorded the result (call 5)
- `web-fact-search`: not seen: searched the web; recorded the result (call 5); opened a source (call 3)
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 8); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 5); wrote the dossier (call 7); opened a source (call 3)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 4); wrote the page (call 9); looked at it in a browser (call 10); recorded the result (call 4)
