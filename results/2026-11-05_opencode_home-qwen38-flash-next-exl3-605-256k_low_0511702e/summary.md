# mengine-bench 2.6.0: opencode opencode v2.2.5 / home/qwen38-flash-next-exl3-605-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **71.6** | 94.8 | 22/28 | 79.0 | 18.6 | 25 min 21 s | $0.00 (price) | 5.60M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4; model=Qwen3.8-Flash-Next; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-6.05bpw; ctx=256k; drafter=MTP n6 dynamic; role=default; disk=Linux SSD; tier=2; temperature=0.5; cpu_profile=high; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-05, started 2026-11-05T19:02:13Z; bench at f343274bbb4f; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | ok | 100% | 6/6 | 86 | 31.4 s | 0.0000 | 4 | 4 | 0.0 | 3.5k | 0.0k | 14 s |
| ds-ab-playtest | ok | 100% | 5/5 | 92 | 19.4 s | 0.0000 | 8 | 8 | 0.3 | 1.8k | 0.0k | 6 s |
| bo-pnl-runway | ok | 100% | 6/6 | 81 | 35.3 s | 0.0000 | 7 | 8 | 0.0 | 4.4k | 0.0k | 10 s |
| bo-reconcile | ok | 100% | 5/5 | 88 | 16.1 s | 0.0000 | 5 | 6 | 0.0 | 1.6k | 0.0k | 7 s |
| cmp-handoff | ok | 100% | 12/12 | 81 | 35.0 s | 0.0000 | 11 | 10 | 0.2 | 3.7k | 0.0k | 12 s |
| cfg-source-drift | ok | 100% | 5/5 | 81 | 16.3 s | 0.0000 | 7 | 8 | 0.2 | 1.4k | 0.0k | 3 s |
| doc-lab-pdf | ok | 100% | 7/7 | 84 | 24.3 s | 0.0000 | 6 | 6 | 0.4 | 2.8k | 0.0k | - |
| ds-sql-funnel | ok | 25% | 2/5 | 40 | 21.5 s | 0.0000 | 7 | 7 | 0.3 | 2.3k | 0.0k | 2 s |
| ue-packaged-bug | ok | 100% | 6/6 | 90 | 21.1 s | 0.0000 | 6 | 9 | 0.0 | 2.3k | 0.0k | 10 s |
| git-merge-conflict | ok | 100% | 7/7 | 96 | 16.8 s | 0.0000 | 7 | 6 | 0.5 | 1.5k | 0.0k | 6 s |
| infra-gpu-fit | ok | 100% | 7/7 | 84 | 22.6 s | 0.0000 | 4 | 5 | 0.0 | 3.0k | 0.0k | 13 s |
| ir-server-logs | ok | 100% | 7/7 | 91 | 30.6 s | 0.0000 | 9 | 9 | 0.4 | 2.6k | 0.0k | 22 s |
| gd-integration-repo | ok | 88% | 9/10 | 73 | 38.6 s | 0.0000 | 15 | 21 | 0.1 | 4.2k | 0.0k | 24 s |
| media-voice | ok | 100% | 4/4 | 86 | 19.2 s | 0.0000 | 9 | 8 | 0.3 | 1.7k | 0.0k | 3 s |
| file-media-edit | ok | 100% | 10/10 | 86 | 1 min 06 s | 0.0000 | 16 | 18 | 0.5 | 7.0k | 0.0k | 33 s |
| txt-regex-log | ok | 100% | 5/5 | 93 | 49.6 s | 0.0000 | 8 | 7 | 0.0 | 7.0k | 0.0k | 20 s |
| rs-lock-bug | timeout (timeout) | 67% | 7/9 | 30 | 3 min 00 s | 0.0000 | 16 | 16 | 0.4 | 3.8k | 0.0k | 8 s |
| sec-leak-fix | ok | 100% | 10/10 | 89 | 23.5 s | 0.0000 | 8 | 13 | 0.1 | 2.2k | 0.0k | 7 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 84 | 53.0 s | 0.0000 | 42 | 42 | 0.0 | 5.3k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 100% | 6/6 | 78 | 1 min 00 s | 0.0000 | 9 | 8 | 0.4 | 7.1k | 0.0k | 13 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 93 | 49.0 s | 0.0000 | 12 | 13 | 0.4 | 5.5k | 0.0k | 13 s |
| ts-plugin-bug | ok | 100% | 8/8 | 92 | 38.5 s | 0.0000 | 12 | 14 | 0.0 | 3.9k | 0.0k | 9 s |
| web-mondrian-landing | ok | 100% | 11/11 | 84 | 45.7 s | 0.0000 | 10 | 10 | 0.1 | 5.8k | 0.0k | 27 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.328 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 74 | 3 min 37 s | 0.0000 | 25 | 33 | 0.1 | 29.9k | 0.0k | 74 s |
| web-fact-search | timeout (timeout) | 100% | 8/8 | 61 | 1 min 00 s | 0.0000 | 13 | 20 | 0.3 | 3.3k | 0.0k | 13 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:58749", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/156.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 93 | 55.0 s | 0.0000 | 30 | 29 | 0.0 | 6.2k | 0.0k | 22 s |
| web-plan-ranking | ok | 75% | 7/9 | 36 | 2 min 53 s | 0.0000 | 21 | 24 | 0.5 | 20.8k | 0.0k | 146 s |
| web-word-universe | ok (left running, not attributed: conhost.exe (3472)) | 100% | 9/9 | 66 | 1 min 43 s | 0.0000 | 35 | 35 | 0.3 | 11.8k | 0.0k | 18 s |

## Failed checks

- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `rs-lock-bug` hidden awards from many threads all count: expected 'awards_from_many_threads_all_count passed', received False
- `rs-lock-bug` hidden a transfer to the same player changes nothing: expected 'a_transfer_to_the_same_player_changes_nothing passed', received False
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7]}, received {'Cruzado': [226.03, 365.88], 'Bresser': [270.81, 933.32], 'Verao': [933.32, 1584.46], 'Collor I': [1764.95, 472.26]}
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 3151, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 4); removed duplicate sessions (call 5); tested significance (call 5); recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 4); recorded the result (call 9)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 4); recorded the result (call 6)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 4); recorded the result (call 8)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 5); committed (call 6)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 3); read the logs (call 1); recorded the result (call 8)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 5); ran the whole suite (call 5)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); made the feed photo (call 7); filled the permit (call 8)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 4)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 9)
- `sec-leak-fix`: read the service (call 4); read the config (call 3); ran the tests (call 10)
- `cu-social-cycle`: made the image (call 1); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 2)
- `hw-stutter-tuning`: read the frame capture (call 7); read the sensor log (call 7); read the settings (call 4); read the owner notes (call 5); recorded the result (call 12)
- `ts-plugin-bug`: read the bus (call 5); ran the tests (call 9)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 3); looked at it in a browser (call 4); recorded the result (call 2)
- `web-fact-search`: searched the web (call 12); recorded the result (call 9); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); replied (call 16)
- `web-plan-ranking`: read the rubric (call 2); not seen: searched the web; recorded the result (call 20); wrote the dossier (call 22); opened a source (call 4)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 5); wrote the page (call 16); looked at it in a browser (call 20); recorded the result (call 5)
