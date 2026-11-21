# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **58.5** | 72.2 | 15/29 | 64.1 | 0.0 | 46 min 41 s | $0.00 (local) | 4.18M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of super-adapter merge; ctx=256k; cache=FP16; layout=native TP 2x RTX 5090; drafter=MTP n4 dynamic; temperature=0.6; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715 (pi+hermes+opencode at 1/2), thinking low (enable_thinking true, OpenCode #low); study=pilot 7 control: super-adapter low run 1; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-21, started 2026-11-21T14:11:42Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | timeout (timeout) | 100% | 8/8 | 76 | 5 min 00 s | 0.0000 | 6 | 5 | 2.0 | 23.5k | 0.0k | 235 s |
| py-async-cancel | ok | 80% | 5/6 | 76 | 35.4 s | 0.0000 | 3 | 3 | 0.0 | 2.7k | 0.0k | 24 s |
| ds-ab-playtest | ok | 100% | 5/5 | 86 | 1 min 43 s | 0.0000 | 13 | 14 | 0.0 | 5.1k | 0.0k | 61 s |
| bo-pnl-runway | ok | 100% | 6/6 | 86 | 1 min 05 s | 0.0000 | 10 | 12 | 0.0 | 4.8k | 0.0k | 23 s |
| bo-reconcile | ok | 100% | 5/5 | 86 | 1 min 04 s | 0.0000 | 9 | 10 | 0.0 | 6.1k | 0.0k | 36 s |
| cmp-handoff | ok | 100% | 12/12 | 85 | 1 min 14 s | 0.0000 | 13 | 12 | 0.0 | 6.0k | 0.0k | 24 s |
| cfg-source-drift | ok | 100% | 5/5 | 93 | 38.5 s | 0.0000 | 8 | 12 | 0.0 | 2.8k | 0.0k | 16 s |
| doc-lab-pdf | timeout (timeout) | 0% | 1/7 | 10 | 1 min 00 s | 0.0000 | 6 | 6 | 0.1 | 0.7k | 0.0k | 8 s |
| ds-sql-funnel | ok | 25% | 2/5 | 42 | 44.7 s | 0.0000 | 10 | 11 | 0.4 | 3.3k | 0.0k | 7 s |
| ue-packaged-bug | ok | 100% | 6/6 | 91 | 43.3 s | 0.0000 | 5 | 11 | 0.0 | 3.4k | 0.0k | 29 s |
| git-merge-conflict | ok | 100% | 7/7 | 91 | 49.6 s | 0.0000 | 10 | 11 | 0.5 | 3.4k | 0.0k | 29 s |
| infra-gpu-fit | ok | 100% | 7/7 | 84 | 40.8 s | 0.0000 | 7 | 8 | 0.0 | 3.3k | 0.0k | 22 s |
| ir-server-logs | timeout (timeout) | 0% | 1/7 | 17 | 1 min 00 s | 0.0000 | 5 | 6 | 0.0 | 2.6k | 0.0k | - |
| gd-integration-repo | ok | 88% | 9/10 | 71 | 42.3 s | 0.0000 | 7 | 16 | 0.1 | 3.0k | 0.0k | 31 s |
| media-voice | ok | 100% | 4/4 | 84 | 26.3 s | 0.0000 | 3 | 2 | 1.0 | 1.8k | 0.0k | - |
| file-media-edit | timeout (timeout, evidence 'out/permit-filled.pdf' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes) | 38% | 5/10 | 33 | 1 min 30 s | 0.0000 | 8 | 8 | 0.3 | 4.0k | 0.0k | 11 s |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 0 | 1 min 00 s | 0.0000 | 1 | 0 | - | - | - | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (15824)) | 100% | 9/9 | 89 | 1 min 38 s | 0.0000 | 8 | 9 | 0.0 | 7.6k | 0.0k | 58 s |
| sec-leak-fix | ok | 75% | 8/10 | 77 | 1 min 18 s | 0.0000 | 8 | 14 | 0.0 | 6.4k | 0.0k | 51 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 86 | 2 min 03 s | 0.0000 | 28 | 28 | 0.3 | 7.9k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 16 | 1 min 00 s | 0.0000 | 8 | 7 | 0.4 | 2.9k | 0.0k | 23 s |
| hw-stutter-tuning | timeout (timeout) | 100% | 7/7 | 76 | 1 min 30 s | 0.0000 | 10 | 12 | 0.0 | 7.1k | 0.0k | 19 s |
| ts-plugin-bug | ok | 100% | 8/8 | 97 | 49.2 s | 0.0000 | 9 | 13 | 0.0 | 3.5k | 0.0k | 15 s |
| web-mondrian-landing | ok | 100% | 11/11 | 80 | 2 min 26 s | 0.0000 | 9 | 8 | 0.6 | 11.8k | 0.0k | 102 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.289 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 54 | 5 min 31 s | 0.0000 | 15 | 14 | 0.0 | 27.2k | 0.0k | 101 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 19 | 1 min 00 s | 0.0000 | 5 | 9 | 0.7 | 1.6k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:60380", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 82 | 1 min 26 s | 0.0000 | 19 | 19 | 0.0 | 6.2k | 0.0k | 46 s |
| web-plan-ranking | timeout (timeout) | 38% | 4/9 | 9 | 3 min 30 s | 0.0000 | 5 | 5 | 0.0 | 12.3k | 0.0k | 130 s |
| web-word-universe | ok | 50% | 5/9 | 62 | 4 min 31 s | 0.0000 | 18 | 22 | 0.0 | 18.5k | 0.0k | 103 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {}
- `doc-lab-pdf` glucose history: expected {'2026-02-10': 92.0, '2026-08-18': 109.9}, received {}
- `doc-lab-pdf` ldl history: expected {'2026-02-10': 118.0, '2026-08-18': 143.08}, received {}
- `doc-lab-pdf` creatinine history: expected {'2026-02-10': 0.95, '2026-08-18': 0.86}, received {}
- `doc-lab-pdf` flags what got worse and left the range: expected ['glucose', 'ldl'], received None
- `doc-lab-pdf` leaves out what stayed in range: expected ['glucose', 'ldl'], received None
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 282}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 67}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'tutorial_complete', 'steamdeck': 'tutorial_complete'}
- `ir-server-logs` incident start: expected '2026-06-02 03:17:42', received None
- `ir-server-logs` incident end: expected '2026-06-02 03:53:31', received None
- `ir-server-logs` minutes down: expected 35.81666666666667, received None
- `ir-server-logs` June availability: expected 99.9170910493827, received None
- `ir-server-logs` SLO 99.9 met: expected True, received None
- `ir-server-logs` root cause = /data disk full: expected 'the /data disk was full', received None
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
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
- `sec-leak-fix` the old token is out of the final answers: the token literal appears in answer(s) [0]; expected it in none
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `web-fact-search` sqlite_3_40_0_release_date value: expected '2022-11-16', received None
- `web-fact-search` sqlite_3_40_0_release_date primary source: expected 'an http(s) URL on sqlite.org', received None
- `web-fact-search` postgresql_15_0_release_date value: expected '2022-10-13', received None
- `web-fact-search` postgresql_15_0_release_date primary source: expected 'an http(s) URL on postgresql.org', received None
- `web-fact-search` unicode_15_0_characters_added value: expected 4489, received None
- `web-fact-search` unicode_15_0_characters_added primary source: expected 'an http(s) URL on unicode.org', received None
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor II': ['1991-01-31']}, received {'Cruzado': '1986-02-15', 'Bresser': '1987-03-01', 'Verao': '1989-02-15', 'Collor II': '1991-10-15'}
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7]}, received {'Cruzado': [211.1, 249.2], 'Bresser': [764.5, 1116.4], 'Verao': [1116.4, 1597.1], 'Collor I': [1597.1, 472.7]}
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Collor I': [10], 'Collor II': [37, 41]}, received {'Cruzado': 12, 'Bresser': 23, 'Collor I': 19, 'Collor II': 32}
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 0, 'urls': 0, 'plans': []}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 3 (contato, dicionário criativo, sobre)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'contato: missing 0 (none), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 743, 'most_connected': 'palavra'}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 14); tested significance (call 5); recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 3); used the cash balance (call 4); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 9)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 3); recorded the result (call 11)
- `cfg-source-drift`: read the readme (call 4); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 4); not seen: recorded the result
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 5); recorded the result (call 7)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 10); committed (call 11)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 7)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); ran the whole suite (call 16)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 7); not seen: filled the permit
- `txt-regex-log`: not seen: wrote the regex; not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 7)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 10)
- `cu-social-cycle`: made the image (call 1); opened the site (call 2); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 6); read the settings (call 4); read the owner notes (call 3); recorded the result (call 11)
- `ts-plugin-bug`: read the bus (call 6); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 3)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 9); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 5); not seen: wrote the dossier; not seen: opened a source
- `web-word-universe`: walked the site (call 1); wrote words.json (call 6); wrote the page (call 6); looked at it in a browser (call 14); recorded the result (call 6)
