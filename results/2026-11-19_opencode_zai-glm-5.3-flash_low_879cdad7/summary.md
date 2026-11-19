# mengine-bench 2.8.0: opencode opencode v2.2.5 / zai/glm-5.3-flash (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **62.4** | 81.0 | 16/29 | 62.6 | 0.0 | 43 min 20 s | >= $0.14 | 2.29M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=zai; tier=1; role=dev; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-19, started 2026-11-19T15:41:36Z; bench at 0b7d01bbdec2; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 83% | 7/8 | 70 | 3 min 42 s | 0.0142 | 15 | 14 | 1.0 | 8.4k | 0.6k | 92 s |
| py-async-cancel | timeout (timeout) | 80% | 5/6 | 45 | 1 min 00 s | - | 5 | 5 | 1.3 | 2.1k | 0.8k | 12 s |
| ds-ab-playtest | ok | 100% | 5/5 | 76 | 32.8 s | 0.0096 | 5 | 5 | 0.3 | 0.8k | 0.0k | 13 s |
| bo-pnl-runway | ok | 40% | 3/6 | 61 | 56.4 s | 0.0040 | 7 | 8 | 0.6 | 2.3k | 0.6k | 35 s |
| bo-reconcile | ok | 100% | 5/5 | 62 | 30.8 s | 0.0024 | 3 | 2 | 2.1 | 1.2k | 0.5k | 14 s |
| cmp-handoff | ok | 91% | 11/12 | 71 | 58.3 s | 0.0050 | 9 | 7 | 0.6 | 1.6k | 0.3k | 11 s |
| cfg-source-drift | ok | 100% | 5/5 | 91 | 23.6 s | 0.0023 | 5 | 6 | 0.4 | 0.4k | 0.0k | 7 s |
| doc-lab-pdf | ok | 100% | 7/7 | 66 | 42.9 s | 0.0037 | 5 | 5 | 0.6 | 1.8k | 0.3k | 22 s |
| ds-sql-funnel | ok | 25% | 2/5 | 41 | 1 min 04 s | 0.0041 | 10 | 11 | 1.2 | 1.8k | 0.3k | 9 s |
| ue-packaged-bug | ok | 100% | 6/6 | 76 | 45.3 s | 0.0032 | 5 | 9 | 0.7 | 1.6k | 0.2k | 19 s |
| git-merge-conflict | ok | 100% | 7/7 | 92 | 47.3 s | 0.0042 | 9 | 8 | 1.1 | 1.0k | 0.0k | 21 s |
| infra-gpu-fit | ok | 100% | 7/7 | 68 | 26.3 s | 0.0019 | 3 | 4 | 0.3 | 0.9k | 0.2k | 8 s |
| ir-server-logs | ok | 100% | 7/7 | 72 | 33.0 s | 0.0030 | 5 | 5 | 0.9 | 0.9k | 0.2k | 14 s |
| gd-integration-repo | ok | 88% | 9/10 | 72 | 1 min 11 s | 0.0076 | 10 | 18 | 0.7 | 2.3k | 1.2k | 48 s |
| media-voice | ok | 100% | 4/4 | 76 | 34.7 s | 0.0024 | 5 | 4 | 2.6 | 1.0k | 0.1k | - |
| file-media-edit | timeout (timeout, evidence 'out/feed-photo.jpg' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes, evidence 'out/permit-filled.pdf' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes) | 0% | 2/10 | 6 | 1 min 30 s | - | 16 | 15 | 1.0 | 1.3k | 0.0k | 12 s |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 0 | 1 min 00 s | - | 1 | 0 | - | - | - | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (32536)) | 100% | 9/9 | 82 | 1 min 28 s | 0.0067 | 16 | 16 | 1.4 | 2.6k | 0.4k | 8 s |
| sec-leak-fix | ok | 100% | 10/10 | 88 | 47.1 s | 0.0060 | 10 | 12 | 0.4 | 1.0k | 0.5k | 8 s |
| cu-social-cycle | timeout (timeout, route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 50 | 3 min 00 s | - | 45 | 47 | 0.5 | 3.2k | 1.0k | 106 s |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 16 | 1 min 00 s | - | 5 | 4 | 1.5 | 0.9k | 0.4k | - |
| hw-stutter-tuning | ok | 83% | 6/7 | 35 | 59.0 s | 0.0037 | 6 | 7 | 1.3 | 1.5k | 0.3k | 32 s |
| ts-plugin-bug | ok | 100% | 8/8 | 100 | 45.5 s | 0.0042 | 8 | 11 | 0.2 | 0.9k | 0.2k | 17 s |
| web-mondrian-landing | ok | 100% | 11/11 | 78 | 1 min 18 s | 0.0058 | 8 | 7 | 0.8 | 3.5k | 0.1k | 42 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.309 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 60 | 6 min 00 s | 0.0243 | 18 | 20 | 6.9 | 15.0k | 2.6k | 79 s |
| web-fact-search | ok | 100% | 8/8 | 88 | 22.8 s | 0.0051 | 4 | 5 | 1.4 | 0.7k | 0.1k | 11 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:52748", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 76 | 1 min 43 s | 0.0090 | 22 | 22 | 0.4 | 1.2k | 0.1k | - |
| web-plan-ranking | ok | 75% | 7/9 | 45 | 3 min 18 s | 0.0113 | 9 | 9 | 3.2 | 6.6k | 4.4k | 36 s |
| web-word-universe | timeout (timeout) | 62% | 6/9 | 51 | 6 min 00 s | - | 34 | 37 | 1.2 | 15.6k | 3.3k | 42 s |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `bo-pnl-runway` revenue per month: 2026-01: expected 200510.87, received None
- `bo-pnl-runway` gross_margin_pct per month: 2026-01: expected 70.0305923564144, received None
- `bo-pnl-runway` ebitda per month: 2026-01: expected -210278.96, received None
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received 'Not named in HANDOFF.md; re-measure by launching the server per scripts/start_server.ps1 with --no-mmproj-offload -ub 512 at 131072 ctx and b
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 268}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 60}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'first_match', 'steamdeck': 'tutorial_complete'}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` photo is a JPEG: expected 'a readable JPEG', received 'FileNotFoundError reading out/feed-photo.jpg'
- `file-media-edit` photo is exactly 1080x1350: expected 'a readable JPEG', received 'FileNotFoundError reading out/feed-photo.jpg'
- `file-media-edit` balloon fully in frame and undistorted: expected 'a readable JPEG', received 'FileNotFoundError reading out/feed-photo.jpg'
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'no out/permit-filled.pdf'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received 'no pattern in regex.txt'
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received 'no pattern in regex.txt'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received 'no pattern in regex.txt'
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received 'no pattern in regex.txt'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `hw-stutter-tuning` ASPM off on the GPU root port: expected 'pcie_aspm_rp1_gpu -> disabled', received [('defender_exclusions', "['C:\\\\Games\\\\Arena', 'Arena.exe']")]
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 3684, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 3 (contato, dicionário criativo, sobre)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'contato: missing 0 (none), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 743, 'most_connected': [{'word': 'palavra', 'relations': 16}, {'word': 'tempo', 'relations': 16}, {'word': 'madrugada', 'relations': 9}, {'word': 'advogado', 'relations': 8}, {'wor

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); not seen: removed duplicate sessions; tested significance (call 5); recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 3); recorded the result (call 7)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); not seen: read the statement; recorded the result (call 2)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 2); recorded the result (call 5)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); not seen: extracted the text; recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 3); excluded test accounts (call 6); recorded the result (call 9)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 5); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 7); committed (call 6)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 2); read the policy (call 3); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 4); ran the integration test (call 3); ran the whole suite (call 14)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); not seen: made the feed photo; not seen: filled the permit
- `txt-regex-log`: not seen: wrote the regex; not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 7)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 10)
- `cu-social-cycle`: made the image (call 3); opened the site (call 2); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 4); read the settings (call 3); read the owner notes (call 2); recorded the result (call 7)
- `ts-plugin-bug`: read the bus (call 6); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 3); looked at it in a browser (call 4); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 5); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 4); replied (call 7)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 5); wrote the dossier (call 5); not seen: opened a source
- `web-word-universe`: walked the site (call 1); wrote words.json (call 8); wrote the page (call 18); looked at it in a browser (call 23); recorded the result (call 12)
