# mengine-bench 2.8.0: opencode opencode v2.2.5 / qwen-cloud/qwen4-max (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **59.3** | 74.5 | 9/29 | 62.9 | 0.0 | 61 min 16 s | >= ~$0.90 | 0.75M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=qwen-cloud; opencode_config=managed + qwen4-max entry (copy of qwen3.8-max); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-16, started 2026-11-16T13:17:44Z; bench at 7c7dbc71c209; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | timeout (timeout) | 100% | 8/8 | 75 | 5 min 00 s | - | 4 | 4 | 5.4 | 17.6k | 3.5k | 262 s |
| py-async-cancel | timeout (timeout) | 100% | 6/6 | 88 | 1 min 00 s | - | 3 | 3 | 13.0 | 2.3k | 1.1k | 41 s |
| ds-ab-playtest | ok | 100% | 5/5 | 90 | 1 min 19 s | 0.0000 | 7 | 7 | 0.9 | 2.6k | 0.7k | 31 s |
| bo-pnl-runway | ok | 100% | 6/6 | 87 | 2 min 18 s | 0.0000 | 8 | 11 | 0.9 | 6.1k | 2.5k | 40 s |
| bo-reconcile | ok | 100% | 5/5 | 84 | 1 min 00 s | 0.0000 | 4 | 5 | 0.7 | 2.3k | 1.4k | - |
| cmp-handoff | timeout (timeout) | 27% | 4/12 | 34 | 1 min 30 s | - | 8 | 8 | 0.9 | 3.5k | 2.3k | 35 s |
| cfg-source-drift | timeout (timeout) | 100% | 5/5 | 83 | 1 min 00 s | - | 8 | 13 | 0.9 | 1.9k | 0.7k | 13 s |
| doc-lab-pdf | timeout (timeout) | 100% | 7/7 | 57 | 1 min 00 s | - | 3 | 4 | 0.7 | 2.1k | 1.4k | 49 s |
| ds-sql-funnel | ok | 100% | 5/5 | 74 | 1 min 28 s | 0.0000 | 9 | 9 | 1.6 | 3.2k | 1.0k | 13 s |
| ue-packaged-bug | ok | 100% | 6/6 | 93 | 58.2 s | 0.0000 | 5 | 10 | 1.6 | 1.9k | 0.5k | 29 s |
| git-merge-conflict | timeout (timeout) | 100% | 7/7 | 91 | 1 min 30 s | - | 10 | 13 | 1.3 | 1.8k | 0.6k | 37 s |
| infra-gpu-fit | ok | 100% | 7/7 | 85 | 47.7 s | 0.0000 | 4 | 5 | 0.8 | 1.6k | 0.6k | - |
| ir-server-logs | timeout (timeout) | 0% | 1/7 | 35 | 1 min 00 s | - | 6 | 6 | 2.1 | 1.6k | 0.9k | - |
| gd-integration-repo | ok | 100% | 10/10 | 92 | 2 min 19 s | 0.0000 | 9 | 22 | 1.3 | 4.9k | 3.1k | 95 s |
| media-voice | ok | 100% | 4/4 | 79 | 37.0 s | 0.0000 | 3 | 2 | 3.8 | 1.1k | 0.5k | - |
| file-media-edit | timeout (timeout, evidence 'out/feed-photo.jpg' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes, evidence 'out/permit-filled.pdf' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes) | 0% | 2/10 | 7 | 1 min 30 s | - | 6 | 7 | 1.5 | 1.4k | 0.8k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 0 | 1 min 00 s | - | 1 | 0 | - | - | - | - |
| rs-lock-bug | timeout (timeout) | 100% | 9/9 | 76 | 3 min 00 s | - | 5 | 7 | 1.0 | 3.1k | 1.4k | 62 s |
| sec-leak-fix | ok | 88% | 9/10 | 83 | 1 min 15 s | 0.0000 | 7 | 10 | 1.2 | 2.4k | 1.0k | 29 s |
| cu-social-cycle | timeout (timeout) | 44% | 6/11 | 20 | 3 min 00 s | - | 9 | 9 | 1.6 | 7.8k | 4.7k | 80 s |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 6 | 1 min 00 s | - | 4 | 3 | 2.7 | 0.6k | 0.2k | - |
| hw-stutter-tuning | timeout (timeout) | 0% | 1/7 | 25 | 1 min 30 s | - | 9 | 10 | 0.8 | 2.9k | 1.5k | - |
| ts-plugin-bug | timeout (timeout) | 100% | 8/8 | 75 | 1 min 00 s | - | 7 | 13 | 0.8 | 2.0k | 0.7k | 25 s |
| web-mondrian-landing | timeout (timeout) | 100% | 11/11 | 76 | 5 min 00 s | - | 10 | 14 | 2.2 | 13.1k | 6.7k | 143 s |
| 3d-print-homage | timeout (timeout, blue-layout similarity to the print: 0.252 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 68 | 7 min 00 s | - | 17 | 26 | 1.3 | 18.2k | 8.0k | 143 s |
| web-fact-search | ok | 100% | 8/8 | 82 | 42.3 s | 0.0000 | 3 | 5 | 2.6 | 1.3k | 0.5k | 19 s |
| cu-webmail | timeout (timeout, write routes (observation only): {"origin": "http://127.0.0.1:55183", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 75 | 3 min 00 s | - | 16 | 19 | 1.7 | 5.2k | 2.0k | - |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 12 | 3 min 30 s | - | 5 | 4 | 5.0 | 6.2k | 4.9k | - |
| web-word-universe | timeout (timeout) | 100% | 9/9 | 73 | 6 min 00 s | - | 14 | 23 | 1.4 | 16.5k | 6.5k | 80 s |

## Failed checks

- `cmp-handoff` summary exists and fits in 1000 characters: 1001 characters
- `cmp-handoff` answer file_line: expected 'a match for \\bstart_server\\.ps1\\b.{0,40}?\\b165\\b', received None
- `cmp-handoff` answer final_decode: expected 'a match for ^(?!.*37[.,]8)(?=.*(?<![\\w.,+-])38(?:[.,]0+)?(?!\\d|[.,]\\d))', received None
- `cmp-handoff` answer final_vram_mib: expected 'a match for (?<![\\w.,+-])7697(?:[.,]0+)?(?!\\w|[.,]\\d)', received ''
- `cmp-handoff` answer discarded_quant: expected 'a match for ^(?=.*\\bQ6(?:_?K)?\\b)(?!.*\\b(?!Q6(?:_?K)?\\b)(?:I?Q\\d+[A-Z0-9_]*|BF16|FP(?:16|32)|F(?:16|32))\\b)', received None
- `cmp-handoff` answer pending: expected 'a match for ^(?!.*\\broot\\b)(?=.*\\bREADME\\b)(?=.*\\b(?:update|fix|remove|edit|replace|check_vision|evals|stale|out of date))', received None
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received None
- `cmp-handoff` does not repeat the spilled VRAM as final: expected 'not 7881', received None
- `ir-server-logs` incident start: expected '2026-06-02 03:17:42', received None
- `ir-server-logs` incident end: expected '2026-06-02 03:53:31', received None
- `ir-server-logs` minutes down: expected 35.81666666666667, received None
- `ir-server-logs` June availability: expected 99.9170910493827, received None
- `ir-server-logs` SLO 99.9 met: expected True, received None
- `ir-server-logs` root cause = /data disk full: expected 'the /data disk was full', received None
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
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `cu-social-cycle` test post published with the exact text: expected 'Testing the new Bluehaze uploader: Harbor Day is on.', received []
- `cu-social-cycle` test post carries cover.png: expected ['aba004cc26d10c8aaeddb9b9f94574a886a83c73c41eadaf441e22436095c8ed'], received []
- `cu-social-cycle` image has the given alt text: expected ['Poster with the title Harbor Day 2026.'], received []
- `cu-social-cycle` test post deleted: expected 'deleted', received 'never posted'
- `cu-social-cycle` post, then delete: expected 'post < delete in the journal', received [-1, None]
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
- `web-plan-ranking` all six plans recorded: expected ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real'], received []
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor I': ['1990-03-16'], 'Collor II': ['1991-01-31'], 'Real': ['1994-03-01', '1994-07-01']}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1], 'Real': [2477.15, 22.41]}, received {'Cruzado': [None, None], 'Bresser': [None, None], 'Verao': [None, None], 'Collor I': [None, None], 'Collor
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Verao': [14], 'Collor I': [10], 'Collor II': [37, 41], 'Real': [60]}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` scores follow the rubric: expected "0.7*drop + 0.3*durability from the row's own numbers", received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received None
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 0, 'urls': 0, 'plans': []}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 3)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 5); tested significance (call 5); recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 6); used the chart of accounts (call 4); used the cash balance (call 5); recorded the result (call 8)
- `bo-reconcile`: read the notes (call 4); read the invoices (call 3); read the statement (call 2); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); not seen: recorded the result
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); not seen: extracted the text; recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 3); excluded test accounts (call 6); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 6); read the game mode (call 4); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 8); ran the tests (call 10); committed (call 12)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 3); read the policy (call 2); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); not seen: recorded the result
- `gd-integration-repo`: read the docs (call 5); ran the integration test (call 4); ran the whole suite (call 16)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); not seen: made the feed photo; not seen: filled the permit
- `txt-regex-log`: not seen: wrote the regex; not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 7)
- `sec-leak-fix`: read the service (call 4); read the config (call 3); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 4); opened the site (call 1); deleted the test post (call 5)
- `ds-sqlite-recover`: not seen: read the raw bytes; not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 5); read the settings (call 3); read the owner notes (call 4); not seen: recorded the result
- `ts-plugin-bug`: read the bus (call 7); ran the tests (call 12)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 4); looked at it in a browser (call 5)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 5); recorded the result (call 3)
- `web-fact-search`: not seen: searched the web; recorded the result (call 4); opened a source (call 1)
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 6); replied (call 6)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: recorded the result; not seen: wrote the dossier; not seen: opened a source
- `web-word-universe`: walked the site (call 2); wrote words.json (call 10); wrote the page (call 12); looked at it in a browser (call 15); recorded the result (call 10)
