# mengine-bench 2.8.0: opencode opencode v2.2.5 / qwen-cloud/qwen3.8-flash (medium)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **61.5** | 80.5 | 14/29 | 60.6 | 0.0 | 53 min 55 s | >= ~$0.41 | 2.34M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=qwen-cloud; tier=1; role=scout-r; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-19, started 2026-11-19T14:33:31Z; bench at 0b7d01bbdec2; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | timeout (timeout) | 83% | 7/8 | 67 | 5 min 00 s | - | 16 | 19 | 1.0 | 16.7k | 3.1k | 175 s |
| py-async-cancel | timeout (timeout) | 100% | 6/6 | 54 | 1 min 00 s | - | 3 | 3 | 8.5 | 2.7k | 1.3k | 35 s |
| ds-ab-playtest | ok | 100% | 5/5 | 83 | 2 min 02 s | 0.0000 | 12 | 11 | 1.1 | 6.0k | 1.3k | 105 s |
| bo-pnl-runway | ok | 100% | 6/6 | 74 | 55.5 s | 0.0000 | 7 | 8 | 0.6 | 3.0k | 1.0k | 42 s |
| bo-reconcile | ok | 100% | 5/5 | 78 | 1 min 01 s | 0.0000 | 7 | 8 | 0.6 | 3.1k | 1.6k | 34 s |
| cmp-handoff | ok | 100% | 12/12 | 87 | 1 min 08 s | 0.0000 | 12 | 10 | 1.0 | 3.0k | 1.1k | 14 s |
| cfg-source-drift | ok | 100% | 5/5 | 86 | 35.7 s | 0.0000 | 7 | 7 | 0.8 | 1.2k | 0.5k | 7 s |
| doc-lab-pdf | timeout (timeout) | 0% | 1/7 | 3 | 1 min 00 s | - | 8 | 7 | 1.4 | 1.2k | 0.7k | - |
| ds-sql-funnel | timeout (timeout) | 75% | 4/5 | 49 | 1 min 30 s | - | 13 | 14 | 1.4 | 5.3k | 1.6k | 5 s |
| ue-packaged-bug | ok | 100% | 6/6 | 75 | 49.1 s | 0.0000 | 5 | 9 | 1.3 | 2.3k | 1.0k | 35 s |
| git-merge-conflict | ok | 100% | 7/7 | 91 | 32.8 s | 0.0000 | 7 | 6 | 1.1 | 1.2k | 0.3k | 14 s |
| infra-gpu-fit | ok | 100% | 7/7 | 66 | 28.2 s | 0.0000 | 3 | 4 | 1.4 | 1.5k | 0.6k | 12 s |
| ir-server-logs | timeout (timeout) | 100% | 7/7 | 60 | 1 min 00 s | - | 8 | 7 | 1.3 | 2.5k | 1.7k | 48 s |
| gd-integration-repo | ok | 88% | 9/10 | 69 | 1 min 25 s | 0.0000 | 12 | 12 | 0.9 | 4.6k | 2.8k | 41 s |
| media-voice | timeout (timeout) | 100% | 4/4 | 71 | 1 min 00 s | - | 11 | 11 | 2.0 | 2.3k | 0.7k | 11 s |
| file-media-edit | ok | 100% | 10/10 | 89 | 1 min 29 s | 0.0000 | 14 | 17 | 1.1 | 3.8k | 1.8k | 63 s |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 7 | 1 min 00 s | - | 4 | 3 | 3.0 | 1.6k | 0.9k | 14 s |
| rs-lock-bug | timeout (timeout, left running, not attributed: vctip.exe (35524)) | 100% | 9/9 | 79 | 3 min 00 s | - | 15 | 15 | 1.3 | 5.3k | 2.0k | 26 s |
| sec-leak-fix | ok | 100% | 10/10 | 89 | 36.4 s | 0.0000 | 6 | 9 | 0.8 | 1.7k | 0.6k | 15 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 69 | 2 min 56 s | 0.0000 | 28 | 29 | 0.3 | 3.9k | 1.4k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 15 | 1 min 00 s | - | 5 | 5 | 1.1 | 2.6k | 1.5k | - |
| hw-stutter-tuning | timeout (timeout) | 0% | 1/7 | 17 | 1 min 30 s | - | 10 | 11 | 1.1 | 2.8k | 1.4k | - |
| ts-plugin-bug | timeout (timeout) | 100% | 8/8 | 67 | 1 min 00 s | - | 11 | 12 | 0.7 | 1.8k | 0.9k | 14 s |
| web-mondrian-landing | ok | 100% | 11/11 | 81 | 3 min 46 s | 0.0000 | 20 | 23 | 0.9 | 12.9k | 3.5k | 60 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.342 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 71 | 5 min 08 s | 0.0000 | 11 | 15 | 3.7 | 20.3k | 11.2k | 111 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 7 | 1 min 00 s | - | 6 | 12 | 2.3 | 2.0k | 0.6k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:49670", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 85 | 2 min 31 s | 0.0000 | 25 | 26 | 0.5 | 4.4k | 0.9k | 65 s |
| web-plan-ranking | timeout (timeout) | 88% | 8/9 | 29 | 3 min 30 s | - | 5 | 7 | 1.0 | 9.3k | 7.3k | 205 s |
| web-word-universe | timeout (timeout) | 100% | 9/9 | 40 | 6 min 00 s | - | 34 | 49 | 1.5 | 19.2k | 6.9k | 26 s |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [None, None, None, None, None, None]
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {}
- `doc-lab-pdf` glucose history: expected {'2026-02-10': 92.0, '2026-08-18': 109.9}, received {}
- `doc-lab-pdf` ldl history: expected {'2026-02-10': 118.0, '2026-08-18': 143.08}, received {}
- `doc-lab-pdf` creatinine history: expected {'2026-02-10': 0.95, '2026-08-18': 0.86}, received {}
- `doc-lab-pdf` flags what got worse and left the range: expected ['glucose', 'ldl'], received None
- `doc-lab-pdf` leaves out what stayed in range: expected ['glucose', 'ldl'], received None
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': {'step': 'purchase', 'conversion': 0.8252}, 'steamdeck': {'step': 'tutorial_complete', 'conversion': 0.6667}}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received 'regex error: bad character range 2-( at position 258'
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received 'regex error: bad character range 2-( at position 258'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received 'regex error: bad character range 2-( at position 258'
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received 'regex error: bad character range 2-( at position 258'
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
- `web-fact-search` sqlite_3_40_0_release_date value: expected '2022-11-16', received None
- `web-fact-search` sqlite_3_40_0_release_date primary source: expected 'an http(s) URL on sqlite.org', received None
- `web-fact-search` postgresql_15_0_release_date value: expected '2022-10-13', received None
- `web-fact-search` postgresql_15_0_release_date primary source: expected 'an http(s) URL on postgresql.org', received None
- `web-fact-search` unicode_15_0_characters_added value: expected 4489, received None
- `web-fact-search` unicode_15_0_characters_added primary source: expected 'an http(s) URL on unicode.org', received None
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 0, 'urls': 0, 'plans': []}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 3); looked at it in a browser (call 4)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 4); removed duplicate sessions (call 5); tested significance (call 6); recorded the result (call 10)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 3); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 6)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 9)
- `cfg-source-drift`: not seen: read the readme; ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 5); extracted the text (call 4); not seen: recorded the result
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 4); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 5); committed (call 6)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 7)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 6); ran the whole suite (call 9)
- `media-voice`: used a speech engine (call 2); wrote the audio (call 3)
- `file-media-edit`: read the details (call 3); made the feed photo (call 9); filled the permit (call 13)
- `txt-regex-log`: wrote the regex (call 2); not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 9)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 4); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 8); read the settings (call 3); read the owner notes (call 2); not seen: recorded the result
- `ts-plugin-bug`: read the bus (call 5); ran the tests (call 9)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 2)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 1)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 2)
- `cu-webmail`: opened the mail app (call 3); downloaded the invoice (call 8); not seen: replied
- `web-plan-ranking`: read the rubric (call 2); not seen: searched the web; recorded the result (call 7); not seen: wrote the dossier; opened a source (call 6)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 5); wrote the page (call 16); looked at it in a browser (call 19); recorded the result (call 5)
