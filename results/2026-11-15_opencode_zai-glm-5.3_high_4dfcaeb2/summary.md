# mengine-bench 2.8.0: opencode opencode v2.2.5 / zai/glm-5.3 (high)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **48.2** | 60.4 | 12/29 | 51.3 | 0.0 | 59 min 22 s | >= $0.90 | 1.84M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: harness=opencode; tier=1; role=advisor; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-15, started 2026-11-15T16:11:39Z; bench at e0004beeea2e; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | timeout (timeout) | 0% | 1/5 | 0 | 5 min 00 s | - | 1 | 0 | - | - | - | - |
| py-async-cancel | timeout (timeout) | 80% | 5/6 | 50 | 1 min 00 s | - | 4 | 4 | 2.2 | 3.0k | 1.8k | 28 s |
| ds-ab-playtest | ok | 100% | 5/5 | 88 | 58.9 s | 0.0388 | 10 | 10 | 0.4 | 2.8k | 0.6k | 21 s |
| bo-pnl-runway | ok | 100% | 6/6 | 74 | 2 min 00 s | 0.0589 | 9 | 11 | 0.3 | 4.1k | 1.4k | 38 s |
| bo-reconcile | ok | 100% | 5/5 | 85 | 1 min 15 s | 0.0321 | 6 | 7 | 0.6 | 2.7k | 1.5k | 54 s |
| cmp-handoff | ok | 100% | 12/12 | 88 | 1 min 14 s | 0.0552 | 10 | 8 | 0.6 | 4.8k | 3.1k | 31 s |
| cfg-source-drift | ok | 100% | 5/5 | 95 | 36.1 s | 0.0304 | 8 | 14 | 0.2 | 1.8k | 0.9k | 13 s |
| doc-lab-pdf | timeout (timeout) | 0% | 1/7 | 7 | 1 min 00 s | - | 5 | 5 | 0.2 | 0.2k | 0.0k | - |
| ds-sql-funnel | timeout (timeout) | 75% | 4/5 | 60 | 1 min 30 s | - | 9 | 9 | 0.7 | 2.1k | 0.8k | 16 s |
| ue-packaged-bug | ok | 100% | 6/6 | 92 | 1 min 17 s | 0.0533 | 7 | 13 | 0.7 | 5.6k | 3.7k | 53 s |
| git-merge-conflict | timeout (timeout) | 100% | 7/7 | 82 | 1 min 30 s | - | 9 | 12 | 1.9 | 2.5k | 1.4k | 67 s |
| infra-gpu-fit | ok | 100% | 7/7 | 87 | 52.6 s | 0.0194 | 4 | 5 | 0.4 | 1.8k | 0.6k | 22 s |
| ir-server-logs | ok | 100% | 7/7 | 92 | 49.1 s | 0.1171 | 9 | 10 | 0.5 | 2.7k | 1.6k | 32 s |
| gd-integration-repo | timeout (timeout) | 0% | 2/10 | 9 | 2 min 30 s | - | 9 | 26 | 0.5 | 2.8k | 2.4k | - |
| media-voice | ok | 100% | 4/4 | 84 | 30.0 s | 0.0203 | 5 | 4 | 1.5 | 1.9k | 1.0k | - |
| file-media-edit | timeout (timeout, evidence 'out/feed-photo.jpg' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes, evidence 'out/permit-filled.pdf' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes) | 0% | 2/10 | 10 | 1 min 30 s | - | 7 | 10 | 2.0 | 1.2k | 0.5k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 3 | 1 min 00 s | - | 2 | 2 | 0.2 | 0.0k | 0.0k | - |
| rs-lock-bug | timeout (timeout, left running, not attributed: vctip.exe (19072)) | 50% | 6/9 | 33 | 3 min 00 s | - | 12 | 14 | 0.9 | 3.7k | 1.5k | 21 s |
| sec-leak-fix | timeout (timeout) | 12% | 3/10 | 4 | 1 min 30 s | - | 4 | 7 | 0.3 | 0.1k | 0.0k | - |
| cu-social-cycle | timeout (timeout, route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 76 | 3 min 00 s | - | 35 | 37 | 0.2 | 2.3k | 1.0k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 6 | 1 min 00 s | - | 3 | 2 | 0.9 | 1.4k | 1.3k | - |
| hw-stutter-tuning | timeout (timeout) | 0% | 1/7 | 16 | 1 min 30 s | - | 11 | 14 | 1.1 | 2.2k | 0.7k | 50 s |
| ts-plugin-bug | ok | 100% | 8/8 | 98 | 39.2 s | 0.0328 | 8 | 12 | 0.1 | 2.4k | 1.1k | 15 s |
| web-mondrian-landing | timeout (timeout) | 0% | 1/9 | 2 | 5 min 00 s | - | 2 | 2 | 0.3 | 0.0k | 0.0k | - |
| 3d-print-homage | timeout (timeout, blue-layout similarity to the print: 0.36 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 50 | 7 min 00 s | - | 15 | 14 | 1.6 | 12.8k | 6.2k | 172 s |
| web-fact-search | ok | 100% | 8/8 | 92 | 29.8 s | 0.0810 | 4 | 5 | 0.7 | 1.5k | 0.8k | 18 s |
| cu-webmail | timeout (timeout, write routes (observation only): {"origin": "http://127.0.0.1:64934", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 33% | 5/9 | 17 | 3 min 00 s | - | 21 | 22 | 0.9 | 6.7k | 1.7k | 55 s |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 8 | 3 min 30 s | - | 4 | 9 | 0.6 | 13.2k | 12.8k | - |
| web-word-universe | ok | 100% | 9/9 | 81 | 5 min 08 s | 0.3563 | 33 | 40 | 0.5 | 22.4k | 9.2k | 55 s |

## Failed checks

- `web-archery-game` index.html exists with content
- `web-archery-game` takes the mouse: press and release
- `web-archery-game` makes its own sound
- `web-archery-game` needs nothing beside the page: expected [], received []
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {}
- `doc-lab-pdf` glucose history: expected {'2026-02-10': 92.0, '2026-08-18': 109.9}, received {}
- `doc-lab-pdf` ldl history: expected {'2026-02-10': 118.0, '2026-08-18': 143.08}, received {}
- `doc-lab-pdf` creatinine history: expected {'2026-02-10': 0.95, '2026-08-18': 0.86}, received {}
- `doc-lab-pdf` flags what got worse and left the range: expected ['glucose', 'ldl'], received None
- `doc-lab-pdf` leaves out what stayed in range: expected ['glucose', 'ldl'], received None
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': {'step': 'purchase', 'conversion': {'tutorial_complete': 0.8276595744680851, 'first_match': 0.8380462724935732, 'purchase': 0.8251533742331288}}, 'steamdeck': {'step': 'tutorial_complete', 'conversion': {'tutorial_complet
- `gd-integration-repo` hidden config override and persistence: FAIL: test_config_override_and_persistence (test_hidden_gold.Hidden.test_config_override_and_persistence) | AssertionError: 0 != 1690
- `gd-integration-repo` hidden env float wins over file: FAIL: test_env_float_wins_over_file (test_hidden_gold.Hidden.test_env_float_wins_over_file) | AssertionError: 0 != 1050
- `gd-integration-repo` hidden round trip keeps everything: FAIL: test_round_trip_keeps_everything (test_hidden_gold.Hidden.test_round_trip_keeps_everything) | AssertionError: Tuples differ: (7, 0, ['a', 'b']) != (7, 640, ['a', 'b'])
- `gd-integration-repo` hidden half up tie rounds up: FAIL: test_half_up_tie_rounds_up (test_hidden_gold.Hidden.test_half_up_tie_rounds_up) | AssertionError: 0 != 1430
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 0 != 1500
- `gd-integration-repo` hidden persisted name survives: FAIL: test_persisted_name_survives (test_hidden_gold.Hidden.test_persisted_name_survives) | AssertionError: Tuples differ: ('Player One', 0) != ('Player One', 960)
- `gd-integration-repo` hidden real environment when env is none: FAIL: test_real_environment_when_env_is_none (test_hidden_gold.Hidden.test_real_environment_when_env_is_none) | AssertionError: 50 != 80
- `gd-integration-repo` existing test suite passes
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
- `rs-lock-bug` hidden awards from many threads all count: expected 'awards_from_many_threads_all_count passed', received False
- `rs-lock-bug` hidden opposite transfers do not hang: expected 'opposite_transfers_do_not_hang passed', received False
- `rs-lock-bug` hidden a transfer to the same player changes nothing: expected 'a_transfer_to_the_same_player_changes_nothing passed', received False
- `sec-leak-fix` hidden the HTTP client uploads without leaking the token: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: 'Bearer [REDACTED:bearer]' != 'Bearer [REDACTED:bearer]'
- `sec-leak-fix` hidden the upload uses the token from BACKUP_TOKEN: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: 'bk_test_ENV9Gh4Ns2Qw7Ub5Tc' not found in "(WindowsPath('archives/photos.tar.gz'), 'https://backup.example.invalid/v1/upload', 'bk_live_FAKE7Qx2Lm9Vt4Rk8Wn3Hd6Pz1Cy5Ja0'){}" : the upload did not receive the BACKUP_TOKEN value
- `sec-leak-fix` hidden the token stays out of every log: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: Lists differ: ['uploading archives\\photos.tar.gz with t[42 chars]Ja0'] != []
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `sec-leak-fix` hidden form input never runs as a command: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: Lists differ: ['canary1.txt', 'canary3.txt', 'canary3.tx[42 chars].gz'] != []
- `sec-leak-fix` hidden a folder with spaces still archives: ERROR: test_case (test_hidden_gold.HiddenCase.test_case)
- `sec-leak-fix` the old token is out of every file: expected [], received ['config.py']
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
- `web-mondrian-landing` index.html exists with content
- `web-mondrian-landing` has a page title and an h1
- `web-mondrian-landing` names the painting (Composition with Red, Blue and Yellow)
- `web-mondrian-landing` names the painter (Piet Mondrian)
- `web-mondrian-landing` states the year 1930
- `web-mondrian-landing` names the De Stijl movement
- `web-mondrian-landing` links to the fact sheet's source
- `web-mondrian-landing` CSS with the Mondrian palette (red, blue, yellow, black)
- `cu-webmail` invoice PDF saved byte for byte: expected 'a file with the sha256 of LP-2026-0418.pdf', received ['AGENTS.md', 'LP-2026-0418.pdf', 'tmp/att.b64', 'tmp/att.p1', 'tmp/att.p2']
- `cu-webmail` reply sent in the invoice conversation: expected 'one reply in thread 19a2f4c81e7b30d5', received []
- `cu-webmail` reply addressed to the sender: expected ['[REDACTED:email]'], received []
- `cu-webmail` reply states the invoice total: expected 1205.77, received ''
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

- `web-archery-game`: not seen: wrote the game; not seen: looked at it in a browser
- `py-async-cancel`: wrote run.py (call 1); ran it (call 2)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 5); tested significance (call 5); recorded the result (call 9)
- `bo-pnl-runway`: read the notes (call 4); read the ledger (call 6); used the chart of accounts (call 5); used the cash balance (call 3); recorded the result (call 7)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 7)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 7)
- `cfg-source-drift`: read the readme (call 5); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); not seen: extracted the text; not seen: recorded the result
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 3); excluded test accounts (call 6); recorded the result (call 8)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 3); recorded the result (call 10)
- `git-merge-conflict`: merged the branch (call 9); ran the tests (call 11); committed (call 11)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 2); read the policy (call 3); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 3); read the logs (call 1); recorded the result (call 9)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 9); ran the whole suite (call 26)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); not seen: made the feed photo; not seen: filled the permit
- `txt-regex-log`: not seen: wrote the regex; not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 9)
- `sec-leak-fix`: read the service (call 3); read the config (call 4); not seen: ran the tests
- `cu-social-cycle`: made the image (call 6); opened the site (call 4); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 1); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 5); read the settings (call 3); read the owner notes (call 4); not seen: recorded the result
- `ts-plugin-bug`: read the bus (call 7); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); not seen: wrote the page; not seen: looked at it in a browser
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 5); recorded the result (call 3)
- `web-fact-search`: not seen: searched the web; recorded the result (call 5); opened a source (call 1)
- `cu-webmail`: opened the mail app (call 3); downloaded the invoice (call 8); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: recorded the result; not seen: wrote the dossier; opened a source (call 4)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 11); wrote the page (call 24); looked at it in a browser (call 29); recorded the result (call 11)
