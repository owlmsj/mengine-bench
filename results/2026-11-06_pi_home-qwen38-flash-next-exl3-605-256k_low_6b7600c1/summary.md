# mengine-bench 2.6.0: pi 1.5.0 / home/qwen38-flash-next-exl3-605-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **68.8** | 96.3 | 21/28 | 82.8 | 0.0 | 30 min 32 s | $0.00 (price) | 4.77M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4; model=Qwen3.8-Flash-Next; runtime=exllamav3 dev 0c325eff + TabbyAPI 8f92fac5; quant=turboderp-6.05bpw; ctx=256k; cache=Q8; drafter=MTP n6 dynamic; role=default; disk=Linux SSD; tier=2; temperature=0.5; harness=pi 1.5.0 + mengine 5afb4eb7 assets (guide, skills, hardblocks extension, mengine-cu MCP); personal_instructions=~/.pi/agent/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-06, started 2026-11-06T14:17:38Z; bench at d3f7084ef728; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | timeout (timeout) | 100% | 6/6 | 72 | 1 min 00 s | 0.0000 | 12 | 12 | 0.7 | 6.7k | 0.0k | - |
| ds-ab-playtest | ok | 75% | 4/5 | 76 | 2 min 13 s | 0.0000 | 16 | 16 | 0.3 | 9.3k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 85 | 50.1 s | 0.0000 | 9 | 8 | 0.4 | 6.4k | 0.0k | - |
| bo-reconcile | ok | 100% | 5/5 | 82 | 13.3 s | 0.0000 | 4 | 5 | 0.0 | 1.5k | 0.0k | - |
| cmp-handoff | ok | 100% | 12/12 | 81 | 36.3 s | 0.0000 | 12 | 11 | 0.2 | 4.0k | 0.0k | - |
| cfg-source-drift | ok | 100% | 5/5 | 93 | 31.8 s | 0.0000 | 10 | 9 | 0.4 | 3.2k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 87 | 34.6 s | 0.0000 | 8 | 7 | 0.2 | 4.4k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 93 | 22.6 s | 0.0000 | 7 | 6 | 0.2 | 2.6k | 0.0k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 93 | 22.1 s | 0.0000 | 6 | 10 | 0.0 | 2.4k | 0.0k | - |
| git-merge-conflict | ok | 100% | 7/7 | 99 | 29.6 s | 0.0000 | 11 | 10 | 0.6 | 2.6k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 90 | 15.8 s | 0.0000 | 5 | 6 | 0.0 | 1.9k | 0.0k | - |
| ir-server-logs | ok | 100% | 7/7 | 84 | 20.4 s | 0.0000 | 7 | 7 | 0.3 | 2.1k | 0.0k | - |
| gd-integration-repo | ok | 100% | 10/10 | 89 | 1 min 23 s | 0.0000 | 21 | 20 | 0.3 | 9.7k | 0.0k | - |
| media-voice | ok | 100% | 4/4 | 95 | 34.6 s | 0.0000 | 7 | 7 | 0.4 | 1.6k | 0.0k | - |
| file-media-edit | ok | 100% | 10/10 | 85 | 54.1 s | 0.0000 | 11 | 15 | 0.3 | 6.6k | 0.0k | - |
| txt-regex-log | ok | 100% | 5/5 | 94 | 45.0 s | 0.0000 | 5 | 4 | 0.2 | 6.3k | 0.0k | - |
| rs-lock-bug | timeout (timeout) | 100% | 9/9 | 74 | 3 min 00 s | 0.0000 | 10 | 10 | 0.2 | 3.5k | 0.0k | - |
| sec-leak-fix | ok | 100% | 10/10 | 87 | 49.6 s | 0.0000 | 12 | 15 | 0.1 | 6.3k | 0.0k | - |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 86 | 1 min 00 s | 0.0000 | 21 | 58 | 0.0 | 6.8k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 60% | 4/6 | 39 | 1 min 00 s | 0.0000 | 3 | 3 | 0.2 | 6.1k | 0.0k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 89 | 45.0 s | 0.0000 | 12 | 11 | 0.1 | 5.2k | 0.0k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 92 | 37.6 s | 0.0000 | 7 | 10 | 0.0 | 5.1k | 0.0k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 87 | 1 min 56 s | 0.0000 | 25 | 25 | 0.0 | 14.4k | 0.0k | - |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.376 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 63 | 2 min 39 s | 0.0000 | 15 | 28 | 0.1 | 20.1k | 0.0k | - |
| web-fact-search | ok | 86% | 7/8 | 86 | 31.8 s | 0.0000 | 6 | 9 | 1.2 | 2.9k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:54673", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/156.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 87 | 1 min 16 s | 0.0000 | 26 | 51 | 0.1 | 8.6k | 0.0k | - |
| web-plan-ranking | ok | 88% | 8/9 | 70 | 1 min 57 s | 0.0000 | 11 | 11 | 0.2 | 9.4k | 0.0k | - |
| web-word-universe | ok | 88% | 8/9 | 60 | 3 min 34 s | 0.0000 | 36 | 35 | 0.2 | 25.8k | 0.0k | - |

## Failed checks

- `ds-ab-playtest` the gain is significant: expected '0.000198469 +/- 0.00015 (pooled two-sided z-test or equivalent), or a containing upper bound <= 0.001', received 0.0006
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received [('lantern', 0.0), ('rope coil', 0.0), ('sleeping bag', 0.0), ('camp stove', 1.0)]
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['unicode_15_0_characters_added']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 4275, 'urls': 1, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 2); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 6); tested significance (call 7); recorded the result (call 10)
- `bo-pnl-runway`: read the notes (call 7); read the ledger (call 2); used the chart of accounts (call 2); used the cash balance (call 2); recorded the result (call 5)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 4); recorded the result (call 10)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 5)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 3); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 3); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 5); ran the tests (call 4); committed (call 8)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); ran the whole suite (call 4)
- `media-voice`: used a speech engine (call 2); wrote the audio (call 3)
- `file-media-edit`: read the details (call 1); made the feed photo (call 9); filled the permit (call 11)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 7)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 8)
- `cu-social-cycle`: made the image (call 11); opened the site (call 7); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 3); read the sensor log (call 3); read the settings (call 2); read the owner notes (call 2); recorded the result (call 10)
- `ts-plugin-bug`: read the bus (call 3); ran the tests (call 9)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 5)
- `3d-print-homage`: wrote the scene (call 3); looked at it in a browser (call 5); recorded the result (call 1)
- `web-fact-search`: not seen: searched the web; recorded the result (call 1); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 12); downloaded the invoice (call 7); replied (call 20)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 9); wrote the dossier (call 10); opened a source (call 6)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 6); wrote the page (call 15); looked at it in a browser (call 16); recorded the result (call 8)
