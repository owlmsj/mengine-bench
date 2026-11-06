# mengine-bench 2.6.1: opencode opencode v2.2.5 / home/qwen38-flash-next-exl3-605-256k (xhigh)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **70.6** | 93.6 | 21/28 | 78.5 | 17.9 | 25 min 32 s | $0.00 (price) | 5.21M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4; model=Qwen3.8-Flash-Next; runtime=exllamav3 dev 0c325eff + TabbyAPI 8f92fac5; quant=turboderp-6.05bpw; ctx=256k; cache=Q8; drafter=MTP n6 dynamic; role=default; disk=Linux SSD; tier=2; temperature=0.5; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-06, started 2026-11-06T18:00:48Z; bench at e43a7e9b84f7; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | timeout (timeout) | 100% | 6/6 | 61 | 1 min 00 s | 0.0000 | 6 | 7 | 1.3 | 7.6k | 0.0k | 27 s |
| ds-ab-playtest | ok | 100% | 5/5 | 91 | 30.2 s | 0.0000 | 8 | 8 | 0.8 | 3.1k | 0.0k | 10 s |
| bo-pnl-runway | ok | 100% | 6/6 | 84 | 39.8 s | 0.0000 | 13 | 12 | 0.4 | 5.2k | 0.0k | 10 s |
| bo-reconcile | ok | 100% | 5/5 | 94 | 18.4 s | 0.0000 | 7 | 9 | 0.4 | 2.2k | 0.0k | 7 s |
| cmp-handoff | ok | 100% | 12/12 | 91 | 34.0 s | 0.0000 | 11 | 9 | 0.6 | 4.1k | 0.0k | 12 s |
| cfg-source-drift | ok | 100% | 5/5 | 98 | 18.7 s | 0.0000 | 8 | 9 | 0.5 | 2.2k | 0.0k | 4 s |
| doc-lab-pdf | ok | 100% | 7/7 | 78 | 28.1 s | 0.0000 | 8 | 9 | 0.7 | 3.5k | 0.0k | 14 s |
| ds-sql-funnel | ok | 75% | 4/5 | 57 | 27.9 s | 0.0000 | 9 | 9 | 0.7 | 3.4k | 0.0k | 2 s |
| ue-packaged-bug | ok | 100% | 6/6 | 92 | 25.0 s | 0.0000 | 8 | 12 | 0.5 | 2.8k | 0.0k | 13 s |
| git-merge-conflict | ok | 100% | 7/7 | 90 | 20.5 s | 0.0000 | 9 | 8 | 0.6 | 2.3k | 0.0k | 10 s |
| infra-gpu-fit | ok | 100% | 7/7 | 86 | 14.4 s | 0.0000 | 5 | 6 | 0.7 | 1.8k | 0.0k | 7 s |
| ir-server-logs | ok | 100% | 7/7 | 91 | 23.7 s | 0.0000 | 9 | 10 | 0.6 | 2.7k | 0.0k | 16 s |
| gd-integration-repo | ok | 100% | 10/10 | 88 | 51.8 s | 0.0000 | 14 | 22 | 0.8 | 6.4k | 0.0k | 26 s |
| media-voice | ok | 100% | 4/4 | 68 | 19.5 s | 0.0000 | 8 | 7 | 0.7 | 1.9k | 0.0k | 3 s |
| file-media-edit | ok | 88% | 9/10 | 74 | 52.0 s | 0.0000 | 14 | 17 | 1.1 | 5.9k | 0.0k | 4 s |
| txt-regex-log | ok | 75% | 4/5 | 71 | 35.9 s | 0.0000 | 6 | 6 | 0.9 | 5.1k | 0.0k | 15 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (15964)) | 100% | 9/9 | 94 | 1 min 41 s | 0.0000 | 12 | 12 | 1.6 | 4.3k | 0.0k | 10 s |
| sec-leak-fix | ok | 100% | 10/10 | 90 | 24.0 s | 0.0000 | 5 | 9 | 0.4 | 2.7k | 0.0k | 14 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 87 | 43.1 s | 0.0000 | 26 | 29 | 0.3 | 4.3k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 26 | 1 min 00 s | 0.0000 | 9 | 8 | 0.6 | 5.5k | 0.0k | 5 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 85 | 1 min 11 s | 0.0000 | 16 | 16 | 0.7 | 9.0k | 0.0k | 13 s |
| ts-plugin-bug | timeout (timeout) | 100% | 8/8 | 84 | 1 min 00 s | 0.0000 | 15 | 19 | 0.7 | 7.2k | 0.0k | 21 s |
| web-mondrian-landing | ok | 100% | 11/11 | 75 | 2 min 00 s | 0.0000 | 28 | 33 | 0.8 | 16.0k | 0.0k | 27 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.321 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 58 | 2 min 45 s | 0.0000 | 22 | 32 | 1.4 | 19.5k | 0.0k | 44 s |
| web-fact-search | ok | 100% | 8/8 | 85 | 54.1 s | 0.0000 | 6 | 10 | 0.8 | 2.2k | 0.0k | 45 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:55435", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/156.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 92 | 48.3 s | 0.0000 | 23 | 25 | 0.7 | 5.6k | 0.0k | - |
| web-plan-ranking | ok | 62% | 6/9 | 32 | 2 min 29 s | 0.0000 | 11 | 18 | 0.9 | 21.6k | 0.0k | 44 s |
| web-word-universe | ok | 100% | 9/9 | 76 | 2 min 16 s | 0.0000 | 26 | 30 | 0.8 | 15.9k | 0.0k | 14 s |

## Failed checks

- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': {'step': 'purchase', 'conversion': 0.8252, 'dropped_players': 57}, 'steamdeck': {'step': 'tutorial_complete', 'conversion': 0.6667, 'dropped_players': 64}}
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received '2026-12-05 (Saturday 5 December 2026)'
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received ['2026-03-03', '2024-09-09', '2025-01-23']
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received [("\x00'\x07first aid", 2.615078678784749e+209), ('\x00\x1b\x07comp', 2.734523893790785e+161), ('\x00!\x02camp st', 28534.0), ('\x00%\x02sleeping', 25185.0)]
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7]}, received {'Cruzado': [226.22, 236.62], 'Bresser': [77.38, 933.42], 'Verao': [933.42, 1589.83], 'Collor I': [1764.98, 472.26]}
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 3821, 'urls': 1, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 2); not seen: removed duplicate sessions; tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 2); used the chart of accounts (call 2); used the cash balance (call 2); recorded the result (call 4)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 4); read the statement (call 5); recorded the result (call 6)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 4); recorded the result (call 8)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 2); extracted the text (call 4); recorded the result (call 6)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 6); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 8); read the game mode (call 5); recorded the result (call 11)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 4); committed (call 7)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 3); read the policy (call 1); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 9)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 9); ran the whole suite (call 14)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 4)
- `file-media-edit`: read the details (call 1); made the feed photo (call 10); filled the permit (call 11)
- `txt-regex-log`: wrote the regex (call 3); tried it in Python (call 4)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 7)
- `sec-leak-fix`: read the service (call 4); read the config (call 3); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 3); opened the site (call 4); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 6)
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 6); read the settings (call 5); read the owner notes (call 4); recorded the result (call 12)
- `ts-plugin-bug`: read the bus (call 8); ran the tests (call 14)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 5); recorded the result (call 3)
- `web-fact-search`: not seen: searched the web; recorded the result (call 9); opened a source (call 3)
- `cu-webmail`: opened the mail app (call 4); downloaded the invoice (call 10); not seen: replied
- `web-plan-ranking`: read the rubric (call 2); not seen: searched the web; recorded the result (call 16); wrote the dossier (call 14); opened a source (call 4)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 5); wrote the page (call 14); looked at it in a browser (call 16); recorded the result (call 5)
