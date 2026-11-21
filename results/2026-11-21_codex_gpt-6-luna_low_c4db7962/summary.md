# mengine-bench 2.8.0: codex codex-cli 0.167.0 / gpt-6-luna (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **75.9** | 86.6 | 17/29 | 67.2 | 70.2 | 18 min 56 s | n/a | 6.16M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Cost warning: no list price for gpt-6-luna; add it to prices.py
- Config: service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-21, started 2026-11-21T12:45:56Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 83% | 7/8 | 70 | 1 min 24 s | - | 1 | 6 | - | 6.1k | 0.0k | - |
| py-async-cancel | ok | 100% | 6/6 | 89 | 25.5 s | - | 1 | 5 | - | 1.4k | 0.0k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 76 | 26.3 s | - | 1 | 7 | - | 1.2k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 72 | 20.4 s | - | 1 | 3 | - | 1.1k | 0.0k | - |
| bo-reconcile | ok | 100% | 5/5 | 73 | 26.0 s | - | 1 | 4 | - | 1.5k | 0.0k | - |
| cmp-handoff | ok | 91% | 11/12 | 71 | 30.5 s | - | 2 | 6 | - | 1.5k | 0.0k | - |
| cfg-source-drift | ok | 100% | 5/5 | 83 | 20.5 s | - | 1 | 4 | - | 1.0k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 70 | 19.2 s | - | 1 | 5 | - | 0.9k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 78 | 21.3 s | - | 1 | 4 | - | 0.9k | 0.0k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 87 | 21.5 s | - | 1 | 5 | - | 1.1k | 0.0k | - |
| git-merge-conflict | ok | 0% | 6/7 | 50 | 30.6 s | - | 1 | 8 | - | 1.4k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 82 | 13.2 s | - | 1 | 2 | - | 0.6k | 0.0k | - |
| ir-server-logs | ok | 100% | 7/7 | 84 | 23.6 s | - | 1 | 5 | - | 1.0k | 0.0k | - |
| gd-integration-repo | ok | 88% | 9/10 | 57 | 23.6 s | - | 1 | 6 | - | 1.1k | 0.0k | - |
| media-voice | ok | 100% | 4/4 | 83 | 19.7 s | - | 1 | 5 | - | 0.7k | 0.0k | - |
| file-media-edit | ok | 88% | 9/10 | 51 | 1 min 08 s | - | 1 | 11 | - | 3.4k | 0.0k | - |
| txt-regex-log | ok | 100% | 5/5 | 86 | 18.8 s | - | 1 | 3 | - | 1.1k | 0.0k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (4760)) | 100% | 9/9 | 79 | 23.6 s | - | 1 | 6 | - | 1.2k | 0.0k | - |
| sec-leak-fix | ok | 88% | 9/10 | 78 | 17.8 s | - | 1 | 4 | - | 0.8k | 0.0k | - |
| cu-social-cycle | ok | 44% | 6/11 | 28 | 1 min 13 s | - | 1 | 14 | - | 1.7k | 0.0k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 74 | 57.5 s | - | 1 | 10 | - | 2.8k | 0.0k | - |
| hw-stutter-tuning | ok | 67% | 5/7 | 31 | 45.9 s | - | 1 | 7 | - | 1.7k | 0.0k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 85 | 17.3 s | - | 1 | 4 | - | 0.6k | 0.0k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 86 | 41.9 s | - | 1 | 5 | - | 2.8k | 0.0k | - |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.449 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 51 | 1 min 32 s | - | 1 | 10 | - | 6.2k | 0.0k | - |
| web-fact-search | ok | 86% | 7/8 | 51 | 17.7 s | - | 1 | 2 | - | 0.7k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:64039", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36 Edg/157."}) | 67% | 7/9 | 32 | 1 min 27 s | - | 1 | 28 | - | 2.4k | 0.0k | - |
| web-plan-ranking | ok | 50% | 5/9 | 29 | 1 min 02 s | - | 1 | 5 | - | 4.1k | 0.0k | - |
| web-word-universe | ok | 62% | 6/9 | 64 | 1 min 48 s | - | 1 | 10 | - | 7.6k | 0.7k | - |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received 'Not specified in HANDOFF.md; it only records recipe flags --no-mmproj-offload and -ub 512, so exact benchmark command cannot be recovered fro
- `git-merge-conflict` visible tests left untouched
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `cu-social-cycle` test post published with the exact text: expected 'Testing the new Bluehaze uploader: Harbor Day is on.', received []
- `cu-social-cycle` test post carries cover.png: expected ['4e132b0d618df79cda7573a70ad302c4d21f0da301532acc116121c7a701d331'], received []
- `cu-social-cycle` image has the given alt text: expected ['Poster with the title Harbor Day 2026.'], received []
- `cu-social-cycle` test post deleted: expected 'deleted', received 'never posted'
- `cu-social-cycle` post, then delete: expected 'post < delete in the journal', received [-1, None]
- `hw-stutter-tuning` cause named: expected "the GPU link's power-saving state (ASPM L1 on its root port)", received 'Windows Defender MsMpEng.exe real-time scanning coincides with the 43-45 s hitch window: disk activity rises to 80-94% and DPC latency to 396-455 us; the frame-time tail is 22.049 ms at p99 (max 23.68 ms).'
- `hw-stutter-tuning` ASPM off on the GPU root port: expected 'pcie_aspm_rp1_gpu -> disabled', received [('defender_exclusions', "['Arena.exe and its game content directory']"), ('defender_scheduled_scan', 'daily 21:00, quick, outside play sessions')]
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `cu-webmail` invoice PDF saved byte for byte: expected 'a file with the sha256 of LP-2026-0418.pdf', received ['AGENTS.md']
- `cu-webmail` reply states the invoice total: expected 1205.77, received 'Thanks for sending invoice LP-2026-0418. We confirm receipt of the invoice for the October print run.'
- `web-plan-ranking` inflation before and after: expected {'Real': [2477.15, 22.41]}, received {'Real': [2477.15, 9.56]}
- `web-plan-ranking` scores follow the rubric: expected "0.7*drop + 0.3*durability from the row's own numbers", received {'Collor I': 0.75, 'Collor II': 0.21}
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2285, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 3 (contato, dicionário criativo, sobre)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'contato: missing 0 (none), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 743, 'most_connected': ['palavra', 'tempo']}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 2); looked at it in a browser (call 3)
- `py-async-cancel`: wrote run.py (call 3); ran it (call 2)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 2); not seen: removed duplicate sessions; tested significance (call 5); recorded the result (call 7)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 2); used the chart of accounts (call 2); used the cash balance (call 2); recorded the result (call 3)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 6)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 3); recorded the result (call 4)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 2); recorded the result (call 1)
- `git-merge-conflict`: merged the branch (call 4); ran the tests (call 7); committed (call 7)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 2); not seen: ran the whole suite
- `media-voice`: used a speech engine (call 1); wrote the audio (call 5)
- `file-media-edit`: read the details (call 2); made the feed photo (call 5); filled the permit (call 5)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 6)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 4)
- `cu-social-cycle`: made the image (call 7); opened the site (call 5); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); wrote the JSON (call 7)
- `hw-stutter-tuning`: read the frame capture (call 3); read the sensor log (call 3); read the settings (call 2); read the owner notes (call 2); recorded the result (call 7)
- `ts-plugin-bug`: read the bus (call 3); ran the tests (call 4)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 3); looked at it in a browser (call 5); recorded the result (call 3)
- `web-fact-search`: not seen: searched the web; recorded the result (call 2); not seen: opened a source
- `cu-webmail`: opened the mail app (call 5); downloaded the invoice (call 1); replied (call 20)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 3); wrote the dossier (call 3); not seen: opened a source
- `web-word-universe`: walked the site (call 3); wrote words.json (call 5); wrote the page (call 5); not seen: looked at it in a browser; recorded the result (call 5)
