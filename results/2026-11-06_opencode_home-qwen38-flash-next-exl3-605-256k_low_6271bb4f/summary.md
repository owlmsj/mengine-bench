# mengine-bench 2.6.0: opencode opencode v2.2.5 / home/qwen38-flash-next-exl3-605-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **72.1** | 96.2 | 23/28 | 80.6 | 16.1 | 25 min 58 s | $0.00 (price) | 4.33M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4; model=Qwen3.8-Flash-Next; runtime=exllamav3 dev 0c325eff + TabbyAPI 8f92fac5; quant=turboderp-6.05bpw; ctx=256k; cache=Q8; drafter=MTP n6 dynamic; role=default; disk=Linux SSD; tier=2; temperature=0.5; host_load=UE automation gate from another session on the laptop; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-06, started 2026-11-06T12:38:56Z; bench at 054cfd609ddc; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | ok | 80% | 5/6 | 68 | 28.9 s | 0.0000 | 7 | 6 | 1.4 | 3.2k | 0.0k | 8 s |
| ds-ab-playtest | ok | 100% | 5/5 | 82 | 1 min 04 s | 0.0000 | 16 | 17 | 1.4 | 7.0k | 0.0k | 7 s |
| bo-pnl-runway | ok | 100% | 6/6 | 79 | 29.4 s | 0.0000 | 7 | 10 | 0.4 | 3.9k | 0.0k | 8 s |
| bo-reconcile | ok | 100% | 5/5 | 78 | 39.3 s | 0.0000 | 10 | 11 | 0.5 | 4.8k | 0.0k | 8 s |
| cmp-handoff | ok | 100% | 12/12 | 89 | 32.8 s | 0.0000 | 12 | 10 | 0.9 | 3.8k | 0.0k | 10 s |
| cfg-source-drift | ok | 100% | 5/5 | 93 | 16.8 s | 0.0000 | 9 | 10 | 0.6 | 1.6k | 0.0k | 7 s |
| doc-lab-pdf | ok | 100% | 7/7 | 74 | 17.8 s | 0.0000 | 6 | 6 | 0.7 | 2.1k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 83 | 25.6 s | 0.0000 | 8 | 8 | 0.6 | 2.4k | 0.0k | 2 s |
| ue-packaged-bug | ok | 100% | 6/6 | 88 | 18.6 s | 0.0000 | 5 | 9 | 0.9 | 2.1k | 0.0k | 10 s |
| git-merge-conflict | ok | 100% | 7/7 | 93 | 19.4 s | 0.0000 | 8 | 7 | 0.7 | 1.9k | 0.0k | 9 s |
| infra-gpu-fit | ok | 100% | 7/7 | 92 | 14.2 s | 0.0000 | 5 | 6 | 0.7 | 1.7k | 0.0k | 7 s |
| ir-server-logs | ok | 100% | 7/7 | 89 | 16.4 s | 0.0000 | 7 | 7 | 0.6 | 1.6k | 0.0k | 9 s |
| gd-integration-repo | ok | 88% | 9/10 | 65 | 36.6 s | 0.0000 | 11 | 20 | 0.5 | 4.2k | 0.0k | 21 s |
| media-voice | ok | 100% | 4/4 | 86 | 21.0 s | 0.0000 | 13 | 12 | 0.6 | 1.8k | 0.0k | 3 s |
| file-media-edit | ok | 100% | 10/10 | 86 | 1 min 15 s | 0.0000 | 25 | 24 | 0.8 | 8.7k | 0.0k | 32 s |
| txt-regex-log | timeout (timeout) | 75% | 4/5 | 42 | 1 min 00 s | 0.0000 | 6 | 5 | 1.1 | 7.2k | 0.0k | 31 s |
| rs-lock-bug | ok (left running, not attributed: python.exe (19300)) | 100% | 9/9 | 82 | 1 min 26 s | 0.0000 | 12 | 13 | 1.1 | 4.2k | 0.0k | 7 s |
| sec-leak-fix | ok | 88% | 9/10 | 71 | 16.4 s | 0.0000 | 6 | 11 | 0.3 | 1.6k | 0.0k | 7 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 87 | 38.4 s | 0.0000 | 31 | 32 | 0.2 | 3.8k | 0.0k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 91 | 42.0 s | 0.0000 | 10 | 9 | 1.2 | 5.4k | 0.0k | 29 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 91 | 43.0 s | 0.0000 | 15 | 14 | 0.7 | 4.9k | 0.0k | 9 s |
| ts-plugin-bug | ok | 100% | 8/8 | 96 | 24.2 s | 0.0000 | 5 | 10 | 0.9 | 2.9k | 0.0k | 14 s |
| web-mondrian-landing | ok | 100% | 11/11 | 79 | 1 min 20 s | 0.0000 | 15 | 17 | 0.7 | 10.5k | 0.0k | 48 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.304 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 59 | 2 min 54 s | 0.0000 | 18 | 31 | 1.4 | 19.9k | 0.0k | 53 s |
| web-fact-search | ok | 100% | 8/8 | 91 | 21.1 s | 0.0000 | 6 | 8 | 0.7 | 1.8k | 0.0k | 11 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:49690", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/156.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 87 | 50.6 s | 0.0000 | 28 | 27 | 0.5 | 5.9k | 0.0k | 18 s |
| web-plan-ranking | ok | 100% | 9/9 | 77 | 1 min 46 s | 0.0000 | 15 | 18 | 1.4 | 15.7k | 0.0k | 60 s |
| web-word-universe | timeout (timeout) | 62% | 6/9 | 59 | 6 min 00 s | 0.0000 | 73 | 82 | 0.5 | 35.4k | 0.0k | 22 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received ['2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31']
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `web-word-universe` collected exactly the site's words: missing 52 (aflição, almoço, amanhã, angústia, açougueiro), extra 52 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acento: missing 1 (sílaba), extra 1 (silaba)'
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 1); ran it (call 4)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 4); removed duplicate sessions (call 5); tested significance (call 5); recorded the result (call 14)
- `bo-pnl-runway`: read the notes (call 4); read the ledger (call 6); used the chart of accounts (call 5); used the cash balance (call 3); recorded the result (call 7)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 4); read the statement (call 5); recorded the result (call 6)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 4); recorded the result (call 8)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 4); recorded the result (call 6)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 3); recorded the result (call 8)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 6); committed (call 7)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 2); read the policy (call 1); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 3); not seen: ran the whole suite
- `media-voice`: used a speech engine (call 1); wrote the audio (call 4)
- `file-media-edit`: read the details (call 1); made the feed photo (call 6); filled the permit (call 6)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 6)
- `sec-leak-fix`: read the service (call 3); read the config (call 4); ran the tests (call 10)
- `cu-social-cycle`: made the image (call 1); opened the site (call 4); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 6)
- `hw-stutter-tuning`: read the frame capture (call 3); read the sensor log (call 3); read the settings (call 2); read the owner notes (call 2); recorded the result (call 11)
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 3); recorded the result (call 1)
- `web-fact-search`: not seen: searched the web; recorded the result (call 7); opened a source (call 3)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 8); replied (call 19)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 12); wrote the dossier (call 13); opened a source (call 4)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 7); wrote the page (call 21); looked at it in a browser (call 27); recorded the result (call 17)
