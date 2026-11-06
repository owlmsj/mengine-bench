# mengine-bench 2.7.0: opencode opencode v2.2.5 / deepseek/deepseek-flash (max)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **71.8** | 88.8 | 17/28 | 78.3 | 0.0 | 45 min 57 s | >= $0.14 (harness) | 4.44M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=deepseek-api; model=DeepSeek-V4.1-Flash-1017; tier=1; role=default; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-06, started 2026-11-06T19:31:22Z; bench at d810059f6015; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | timeout (timeout) | 0% | 1/6 | 2 | 1 min 00 s | - | 2 | 2 | 0.3 | 0.9k | 0.8k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 87 | 1 min 47 s | 0.0094 | 12 | 15 | 0.6 | 13.1k | 7.9k | 10 s |
| bo-pnl-runway | ok | 100% | 6/6 | 89 | 2 min 15 s | 0.0150 | 18 | 22 | 0.8 | 20.5k | 12.3k | 12 s |
| bo-reconcile | ok | 100% | 5/5 | 94 | 28.3 s | 0.0035 | 8 | 11 | 0.5 | 3.4k | 1.4k | 16 s |
| cmp-handoff | ok | 100% | 12/12 | 86 | 57.4 s | 0.0070 | 16 | 16 | 0.5 | 7.1k | 4.1k | 18 s |
| cfg-source-drift | ok | 100% | 5/5 | 98 | 32.9 s | 0.0038 | 11 | 17 | 0.5 | 3.4k | 1.2k | 9 s |
| doc-lab-pdf | timeout (timeout) | 100% | 7/7 | 77 | 1 min 00 s | - | 14 | 16 | 0.9 | 7.2k | 3.5k | 38 s |
| ds-sql-funnel | ok | 100% | 5/5 | 96 | 1 min 02 s | 0.0072 | 15 | 16 | 0.6 | 8.2k | 3.6k | 4 s |
| ue-packaged-bug | ok | 100% | 6/6 | 91 | 50.0 s | 0.0054 | 6 | 13 | 0.6 | 6.7k | 5.2k | 22 s |
| git-merge-conflict | ok | 100% | 7/7 | 95 | 27.1 s | 0.0030 | 11 | 16 | 0.5 | 2.3k | 0.7k | 13 s |
| infra-gpu-fit | ok | 100% | 7/7 | 89 | 16.0 s | 0.0021 | 4 | 5 | 0.5 | 2.0k | 0.9k | 6 s |
| ir-server-logs | timeout (timeout) | 100% | 7/7 | 83 | 1 min 00 s | - | 12 | 11 | 0.8 | 6.4k | 4.7k | 39 s |
| gd-integration-repo | ok | 88% | 9/10 | 70 | 54.5 s | 0.0072 | 12 | 30 | 0.8 | 7.2k | 3.6k | 22 s |
| media-voice | timeout (timeout) | 100% | 4/4 | 72 | 1 min 00 s | - | 12 | 12 | 1.4 | 3.9k | 1.5k | - |
| file-media-edit | ok | 100% | 10/10 | 96 | 1 min 13 s | 0.0066 | 18 | 23 | 0.8 | 6.9k | 3.6k | 14 s |
| txt-regex-log | ok | 100% | 5/5 | 96 | 34.5 s | 0.0039 | 4 | 3 | 0.7 | 5.0k | 3.8k | 19 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (14572)) | 100% | 9/9 | 93 | 50.8 s | 0.0054 | 12 | 15 | 0.8 | 6.0k | 2.8k | 17 s |
| sec-leak-fix | timeout (timeout) | 100% | 10/10 | 76 | 1 min 30 s | - | 18 | 27 | 0.6 | 12.0k | 7.8k | 28 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 88 | 2 min 50 s | 0.0132 | 47 | 55 | 0.3 | 11.1k | 5.4k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 12 | 1 min 00 s | - | 5 | 5 | 0.9 | 7.7k | 6.7k | - |
| hw-stutter-tuning | timeout (timeout) | 0% | 1/7 | 23 | 1 min 30 s | - | 9 | 10 | 0.5 | 8.9k | 7.1k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 90 | 35.4 s | 0.0043 | 7 | 11 | 0.7 | 5.0k | 2.4k | 13 s |
| web-mondrian-landing | timeout (timeout) | 100% | 11/11 | 83 | 5 min 00 s | - | 24 | 24 | 0.4 | 36.6k | 22.7k | 169 s |
| 3d-print-homage | timeout (timeout, blue-layout similarity to the print: 0.0 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 68 | 7 min 00 s | - | 7 | 9 | 0.8 | 70.5k | 55.8k | 317 s |
| web-fact-search | ok | 100% | 8/8 | 93 | 16.3 s | 0.0063 | 5 | 7 | 0.7 | 1.6k | 0.5k | 8 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:61581", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/156.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 88 | 1 min 15 s | 0.0076 | 30 | 31 | 0.5 | 6.3k | 1.8k | - |
| web-plan-ranking | ok | 100% | 9/9 | 83 | 2 min 51 s | 0.0254 | 19 | 31 | 1.0 | 27.3k | 17.1k | 27 s |
| web-word-universe | timeout (timeout) | 100% | 9/9 | 75 | 6 min 00 s | - | 45 | 54 | 0.7 | 49.4k | 24.0k | 15 s |

## Failed checks

- `py-async-cancel` jobs run side by side up to the limit: expected {'started': 2, 'finished': 2, 'cleaned': 2, 'peak': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` never more jobs at once than the limit: expected {'started': 2, 'finished': 2, 'cleaned': 2, 'peak': 1}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C below the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C at the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `hw-stutter-tuning` average FPS: expected 137.3, received None
- `hw-stutter-tuning` 1% low FPS: expected 45.4, received None
- `hw-stutter-tuning` cause named: expected "the GPU link's power-saving state (ASPM L1 on its root port)", received None
- `hw-stutter-tuning` ASPM off on the GPU root port: expected 'pcie_aspm_rp1_gpu -> disabled', received []
- `hw-stutter-tuning` GPU link speed kept: expected 'changes that leave the link speed alone', received []
- `hw-stutter-tuning` BIOS overclock kept: expected 'no XMP, PBO or core ratio change', received []

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: not seen: wrote run.py; not seen: ran it
- `ds-ab-playtest`: read the notes (call 3); read the data (call 4); removed duplicate sessions (call 5); tested significance (call 9); recorded the result (call 13)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 2); recorded the result (call 7)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 4); read the statement (call 5); recorded the result (call 8)
- `cmp-handoff`: read the session (call 3); wrote the handoff (call 6); recorded the result (call 15)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 2); extracted the text (call 4); recorded the result (call 10)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 4); excluded test accounts (call 7); recorded the result (call 13)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 5); recorded the result (call 12)
- `git-merge-conflict`: merged the branch (call 10); ran the tests (call 13); committed (call 14)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 2); read the policy (call 1); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 9)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 7); ran the whole suite (call 19)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 5)
- `file-media-edit`: read the details (call 2); made the feed photo (call 11); filled the permit (call 12)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 3); read the config (call 4); ran the tests (call 10)
- `cu-social-cycle`: made the image (call 11); opened the site (call 4); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 5); read the settings (call 3); read the owner notes (call 2); not seen: recorded the result
- `ts-plugin-bug`: read the bus (call 5); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 4); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 3); looked at it in a browser (call 5); recorded the result (call 4)
- `web-fact-search`: not seen: searched the web; recorded the result (call 6); opened a source (call 1)
- `cu-webmail`: opened the mail app (call 3); downloaded the invoice (call 12); replied (call 24)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 6); wrote the dossier (call 7); opened a source (call 3)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 15); wrote the page (call 20); looked at it in a browser (call 22); recorded the result (call 15)
