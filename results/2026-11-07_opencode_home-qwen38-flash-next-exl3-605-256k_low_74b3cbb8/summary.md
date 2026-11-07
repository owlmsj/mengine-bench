# mengine-bench 2.8.0: opencode opencode v2.2.5 / home/qwen38-flash-next-exl3-605-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **86.8** | 99.1 | 26/29 | 84.3 | 52.3 | 24 min 19 s | $0.00 (price) | 6.58M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4; model=Qwen3.8-Flash-Next; runtime=exllamav3 dev 0c325eff + TabbyAPI 8f92fac5; quant=turboderp-6.05bpw; ctx=256k; cache=Q8; drafter=MTP n6 dynamic; role=default; disk=Linux SSD; tier=2; temperature=0.6; mengine=2.7.0 main 73182691 (policy local protocol v5, #949); host_load=idle Claude Code session on the laptop; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-07, started 2026-11-07T22:56:52Z; bench at 045ec87e7bd7; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 81 | 2 min 08 s | 0.0000 | 25 | 29 | 1.3 | 15.8k | 0.0k | 56 s |
| py-async-cancel | timeout (timeout) | 100% | 6/6 | 74 | 1 min 00 s | 0.0000 | 7 | 7 | 1.0 | 6.7k | 0.0k | 43 s |
| ds-ab-playtest | ok | 100% | 5/5 | 92 | 32.9 s | 0.0000 | 16 | 15 | 0.5 | 3.7k | 0.0k | 10 s |
| bo-pnl-runway | ok | 100% | 6/6 | 84 | 33.3 s | 0.0000 | 9 | 10 | 0.6 | 4.6k | 0.0k | 9 s |
| bo-reconcile | ok | 100% | 5/5 | 84 | 14.9 s | 0.0000 | 6 | 7 | 0.3 | 1.8k | 0.0k | 6 s |
| cmp-handoff | ok | 100% | 12/12 | 85 | 30.3 s | 0.0000 | 10 | 8 | 0.5 | 3.6k | 0.0k | 11 s |
| cfg-source-drift | ok | 100% | 5/5 | 96 | 17.5 s | 0.0000 | 8 | 9 | 0.6 | 2.0k | 0.0k | 5 s |
| doc-lab-pdf | ok | 100% | 7/7 | 81 | 19.1 s | 0.0000 | 7 | 7 | 0.4 | 2.4k | 0.0k | 11 s |
| ds-sql-funnel | ok | 100% | 5/5 | 87 | 24.4 s | 0.0000 | 9 | 9 | 0.6 | 2.7k | 0.0k | 2 s |
| ue-packaged-bug | ok | 100% | 6/6 | 90 | 30.1 s | 0.0000 | 8 | 11 | 0.5 | 3.5k | 0.0k | 14 s |
| git-merge-conflict | ok | 100% | 7/7 | 91 | 22.0 s | 0.0000 | 10 | 9 | 0.7 | 2.3k | 0.0k | 11 s |
| infra-gpu-fit | ok | 100% | 7/7 | 91 | 13.8 s | 0.0000 | 5 | 6 | 0.6 | 1.8k | 0.0k | 7 s |
| ir-server-logs | ok | 100% | 7/7 | 88 | 23.8 s | 0.0000 | 8 | 7 | 0.7 | 2.6k | 0.0k | - |
| gd-integration-repo | ok | 88% | 9/10 | 74 | 31.7 s | 0.0000 | 10 | 19 | 0.3 | 3.8k | 0.0k | 22 s |
| media-voice | ok | 100% | 4/4 | 84 | 17.6 s | 0.0000 | 5 | 4 | 1.9 | 1.8k | 0.0k | - |
| file-media-edit | ok | 88% | 9/10 | 80 | 27.6 s | 0.0000 | 9 | 8 | 1.3 | 2.6k | 0.0k | - |
| txt-regex-log | ok | 100% | 5/5 | 94 | 56.0 s | 0.0000 | 9 | 8 | 0.8 | 7.7k | 0.0k | 28 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (5576)) | 100% | 9/9 | 68 | 1 min 33 s | 0.0000 | 12 | 11 | 1.3 | 5.8k | 0.0k | 20 s |
| sec-leak-fix | ok | 100% | 10/10 | 86 | 20.0 s | 0.0000 | 6 | 10 | 0.3 | 2.3k | 0.0k | 10 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 90 | 35.8 s | 0.0000 | 25 | 26 | 0.2 | 3.5k | 0.0k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 83 | 40.4 s | 0.0000 | 8 | 7 | 0.6 | 5.0k | 0.0k | 18 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 90 | 1 min 01 s | 0.0000 | 14 | 13 | 0.7 | 7.3k | 0.0k | 10 s |
| ts-plugin-bug | ok | 100% | 8/8 | 93 | 42.3 s | 0.0000 | 11 | 15 | 0.8 | 5.2k | 0.0k | 13 s |
| web-mondrian-landing | ok | 100% | 11/11 | 77 | 1 min 03 s | 0.0000 | 13 | 13 | 0.2 | 8.3k | 0.0k | 44 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.464 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 60 | 3 min 10 s | 0.0000 | 23 | 34 | 1.4 | 25.4k | 0.0k | 57 s |
| web-fact-search | ok | 100% | 8/8 | 88 | 20.7 s | 0.0000 | 7 | 7 | 0.6 | 1.8k | 0.0k | 14 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:62119", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 95 | 45.3 s | 0.0000 | 24 | 23 | 0.6 | 5.5k | 0.0k | 21 s |
| web-plan-ranking | ok | 100% | 9/9 | 83 | 2 min 46 s | 0.0000 | 23 | 29 | 1.8 | 22.1k | 0.0k | 116 s |
| web-word-universe | ok | 100% | 9/9 | 77 | 1 min 37 s | 0.0000 | 22 | 22 | 0.8 | 12.3k | 0.0k | 14 s |

## Failed checks

- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received 'Saturday 5 December 2026'

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 4); removed duplicate sessions (call 6); tested significance (call 6); recorded the result (call 6)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 3); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 3); recorded the result (call 7)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 4); recorded the result (call 5)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 6); read the game mode (call 4); recorded the result (call 10)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 7); committed (call 7)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 2); read the policy (call 1); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 7)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 5); not seen: ran the whole suite
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); made the feed photo (call 4); filled the permit (call 6)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 2)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 4)
- `sec-leak-fix`: read the service (call 3); read the config (call 4); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 3); opened the site (call 4); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); wrote the JSON (call 4)
- `hw-stutter-tuning`: read the frame capture (call 3); read the sensor log (call 3); read the settings (call 2); read the owner notes (call 2); recorded the result (call 12)
- `ts-plugin-bug`: read the bus (call 6); ran the tests (call 9)
- `web-mondrian-landing`: read the fact sheet (call 2); wrote the page (call 3); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 5); recorded the result (call 1)
- `web-fact-search`: not seen: searched the web; recorded the result (call 6); opened a source (call 1)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 8); not seen: replied
- `web-plan-ranking`: read the rubric (call 2); not seen: searched the web; recorded the result (call 17); wrote the dossier (call 18); opened a source (call 4)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 3); wrote the page (call 11); looked at it in a browser (call 12); recorded the result (call 6)
