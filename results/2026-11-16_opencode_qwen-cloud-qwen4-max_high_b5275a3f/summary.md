# mengine-bench 2.8.0: opencode opencode v2.2.5 / qwen-cloud/qwen4-max (high)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **63.7** | 79.3 | 10/29 | 68.7 | 0.0 | 61 min 52 s | >= ~$1.25 | 1.45M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=qwen-cloud; opencode_config=managed + qwen4-max entry (copy of qwen3.8-max); part=2 of 2 (tasks 5-29; tasks 1-4 in the killed run log); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-16, started 2026-11-16T03:02:48Z; bench at 5ac8e8e88a8a (dirty tree); submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | timeout (timeout, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 8/8 | 77 | 5 min 00 s | - | 7 | 8 | 2.4 | 16.5k | 4.3k | 247 s |
| py-async-cancel | timeout (timeout, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 80% | 5/6 | 47 | 1 min 00 s | - | 3 | 2 | 10.5 | 1.8k | 0.7k | 23 s |
| ds-ab-playtest | ok (redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 5/5 | 93 | 2 min 24 s | 0.0000 | 9 | 9 | 1.1 | 5.9k | 2.9k | 30 s |
| bo-pnl-runway | timeout (timeout, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 6/6 | 84 | 2 min 30 s | - | 5 | 9 | 1.2 | 7.2k | 3.3k | 66 s |
| bo-reconcile | ok | 100% | 5/5 | 81 | 1 min 15 s | 0.0000 | 5 | 6 | 0.7 | 4.0k | 2.9k | 61 s |
| cmp-handoff | timeout (timeout) | 36% | 5/12 | 40 | 1 min 30 s | - | 9 | 9 | 0.6 | 3.0k | 1.9k | 40 s |
| cfg-source-drift | ok | 100% | 5/5 | 100 | 45.3 s | 0.0000 | 7 | 8 | 0.9 | 1.4k | 0.4k | 16 s |
| doc-lab-pdf | timeout (timeout) | 100% | 7/7 | 69 | 1 min 00 s | - | 6 | 6 | 0.8 | 1.4k | 0.8k | 30 s |
| ds-sql-funnel | ok | 100% | 5/5 | 97 | 1 min 23 s | 0.0000 | 9 | 9 | 0.9 | 3.0k | 1.1k | 8 s |
| ue-packaged-bug | ok | 100% | 6/6 | 93 | 55.2 s | 0.0000 | 6 | 10 | 1.0 | 2.0k | 0.5k | 19 s |
| git-merge-conflict | ok | 100% | 7/7 | 93 | 1 min 06 s | 0.0000 | 8 | 8 | 0.9 | 1.9k | 0.9k | 31 s |
| infra-gpu-fit | ok | 100% | 7/7 | 90 | 57.3 s | 0.0000 | 5 | 6 | 0.5 | 2.7k | 1.4k | 29 s |
| ir-server-logs | timeout (timeout) | 0% | 1/7 | 25 | 1 min 00 s | - | 7 | 7 | 1.2 | 1.9k | 1.4k | - |
| gd-integration-repo | ok | 100% | 10/10 | 93 | 1 min 51 s | 0.0000 | 10 | 22 | 1.1 | 4.4k | 2.4k | 65 s |
| media-voice | timeout (timeout) | 100% | 4/4 | 71 | 1 min 00 s | - | 7 | 6 | 2.3 | 1.9k | 0.8k | 18 s |
| file-media-edit | timeout (timeout) | 88% | 9/10 | 61 | 1 min 30 s | - | 5 | 7 | 1.6 | 4.0k | 2.4k | 69 s |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 0 | 1 min 00 s | - | 1 | 0 | - | - | - | - |
| rs-lock-bug | timeout (timeout) | 100% | 9/9 | 80 | 3 min 00 s | - | 10 | 15 | 1.6 | 8.0k | 5.4k | 112 s |
| sec-leak-fix | timeout (timeout) | 100% | 10/10 | 83 | 1 min 30 s | - | 9 | 15 | 1.0 | 3.6k | 2.0k | 41 s |
| cu-social-cycle | timeout (timeout) | 44% | 6/11 | 26 | 3 min 00 s | - | 13 | 17 | 1.3 | 8.1k | 3.4k | 74 s |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 14 | 1 min 00 s | - | 5 | 4 | 0.7 | 1.6k | 0.5k | 32 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 86 | 1 min 21 s | 0.0000 | 8 | 10 | 0.9 | 3.7k | 1.5k | 62 s |
| ts-plugin-bug | timeout (timeout) | 100% | 8/8 | 84 | 1 min 00 s | - | 7 | 12 | 0.8 | 2.5k | 0.9k | 21 s |
| web-mondrian-landing | timeout (timeout) | 100% | 11/11 | 78 | 5 min 00 s | - | 18 | 19 | 1.1 | 14.0k | 6.3k | 124 s |
| 3d-print-homage | timeout (timeout, blue-layout similarity to the print: 0.42 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 65 | 7 min 00 s | - | 9 | 23 | 12.9 | 19.5k | 9.1k | 218 s |
| web-fact-search | ok | 100% | 8/8 | 92 | 42.6 s | 0.0000 | 4 | 5 | 2.1 | 1.5k | 0.6k | 26 s |
| cu-webmail | timeout (timeout, write routes (observation only): {"origin": "http://127.0.0.1:53450", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 84 | 3 min 00 s | - | 21 | 27 | 1.0 | 4.3k | 1.4k | - |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 23 | 3 min 30 s | - | 9 | 9 | 3.0 | 9.6k | 7.5k | - |
| web-word-universe | ok | 50% | 5/9 | 63 | 5 min 43 s | 0.0000 | 20 | 23 | 1.1 | 16.7k | 5.8k | 58 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
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
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received 'Saturday 5 December 2026'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received 'no pattern in regex.txt'
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received 'no pattern in regex.txt'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received 'no pattern in regex.txt'
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received 'no pattern in regex.txt'
- `cu-social-cycle` test post published with the exact text: expected 'Testing the new Bluehaze uploader: Harbor Day is on.', received []
- `cu-social-cycle` test post carries cover.png: expected ['6d701c83ae34ab0c8a7412db4a72d00affba030d5e359ca306d06cb45c44a157'], received []
- `cu-social-cycle` image has the given alt text: expected ['Poster with the title Harbor Day 2026.'], received []
- `cu-social-cycle` test post deleted: expected 'deleted', received 'never posted'
- `cu-social-cycle` post, then delete: expected 'post < delete in the journal', received [-1, None]
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `web-plan-ranking` all six plans recorded: expected ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real'], received []
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor I': ['1990-03-16'], 'Collor II': ['1991-01-31'], 'Real': ['1994-03-01', '1994-07-01']}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1], 'Real': [2477.15, 22.41]}, received {'Cruzado': [None, None], 'Bresser': [None, None], 'Verao': [None, None], 'Collor I': [None, None], 'Collor
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Verao': [14], 'Collor I': [10], 'Collor II': [37, 41], 'Real': [60]}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` scores follow the rubric: expected "0.7*drop + 0.3*durability from the row's own numbers", received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received None
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 0, 'urls': 0, 'plans': []}
- `web-word-universe` collected exactly the site's words: missing 52 (aflição, almoço, amanhã, angústia, açougueiro), extra 55 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acento: missing 1 (sílaba), extra 1 (silaba)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 757, 'most_connected': 'palavra'}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 1)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 5); tested significance (call 5); recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 6); used the chart of accounts (call 4); used the cash balance (call 5); recorded the result (call 7)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 6)
- `cmp-handoff`: read the session (call 3); wrote the handoff (call 4); not seen: recorded the result
- `cfg-source-drift`: read the readme (call 4); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 1); not seen: extracted the text; recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 5); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 7); committed (call 8)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); not seen: recorded the result
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); ran the whole suite (call 18)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 3); made the feed photo (call 6); filled the permit (call 6)
- `txt-regex-log`: not seen: wrote the regex; not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 4); read the config (call 3); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 6); opened the site (call 1); deleted the test post (call 8)
- `ds-sqlite-recover`: read the raw bytes (call 3); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 5); read the settings (call 3); read the owner notes (call 2); recorded the result (call 9)
- `ts-plugin-bug`: read the bus (call 5); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 3); looked at it in a browser (call 4); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 5); opened a source (call 1)
- `cu-webmail`: opened the mail app (call 10); downloaded the invoice (call 11); replied (call 22)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: recorded the result; not seen: wrote the dossier; not seen: opened a source
- `web-word-universe`: walked the site (call 3); wrote words.json (call 7); wrote the page (call 10); looked at it in a browser (call 12); recorded the result (call 7)
