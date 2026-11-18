# mengine-bench 2.8.0: opencode opencode v2.2.5 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **66.6** | 78.2 | 18/29 | 63.3 | 45.3 | 26 min 25 s | >= $0.00 | 7.07M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; model=Qwen3.8-27B; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of pi-adapted merge; ctx=256k; cache=FP16; layout=native TP 2x RTX 5090; drafter=MTP n4 dynamic; tier=2; temperature=0.6; finetune=harness-hub/Qwen3.8-27B-pi-adapted rev e786f849 (AsyncGRPO LoRA r32), THINKING OFF (Tabby enable_thinking false); mengine=2.8.0 installed; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-18, started 2026-11-18T12:08:38Z; bench at ac16be22ea10 (dirty tree); submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 51 | 1 min 21 s | 0.0000 | 10 | 9 | 0.4 | 9.5k | 0.0k | 0 s |
| py-async-cancel | ok | 100% | 6/6 | 67 | 56.6 s | 0.0000 | 12 | 11 | 0.6 | 6.5k | 0.0k | 0 s |
| ds-ab-playtest | ok | 100% | 5/5 | 83 | 43.3 s | 0.0000 | 9 | 9 | 0.0 | 1.8k | 0.0k | 34 s |
| bo-pnl-runway | ok | 40% | 3/6 | 52 | 30.4 s | 0.0000 | 8 | 10 | 0.0 | 4.0k | 0.0k | 10 s |
| bo-reconcile | ok | 100% | 5/5 | 84 | 28.1 s | 0.0000 | 14 | 15 | 0.0 | 3.4k | 0.0k | 7 s |
| cmp-handoff | timeout (timeout) | 27% | 4/12 | 19 | 1 min 30 s | - | 37 | 37 | 0.0 | 15.0k | 0.0k | 7 s |
| cfg-source-drift | ok | 100% | 5/5 | 93 | 14.0 s | 0.0000 | 9 | 12 | 0.0 | 1.4k | 0.0k | 6 s |
| doc-lab-pdf | ok | 100% | 7/7 | 63 | 24.0 s | 0.0000 | 11 | 11 | 0.3 | 2.7k | 0.0k | 7 s |
| ds-sql-funnel | ok | 100% | 5/5 | 87 | 28.8 s | 0.0000 | 12 | 13 | 0.3 | 3.3k | 0.0k | 4 s |
| ue-packaged-bug | ok | 100% | 6/6 | 91 | 24.3 s | 0.0000 | 8 | 12 | 0.0 | 3.0k | 0.0k | 7 s |
| git-merge-conflict | ok | 100% | 7/7 | 90 | 15.5 s | 0.0000 | 9 | 8 | 0.3 | 1.3k | 0.0k | 8 s |
| infra-gpu-fit | ok | 17% | 2/7 | 17 | 15.5 s | 0.0000 | 7 | 8 | 0.0 | 1.7k | 0.0k | 2 s |
| ir-server-logs | ok | 83% | 6/7 | 53 | 20.6 s | 0.0000 | 8 | 9 | 0.0 | 2.0k | 0.0k | 10 s |
| gd-integration-repo | ok | 88% | 9/10 | 69 | 30.5 s | 0.0000 | 13 | 31 | 0.0 | 4.1k | 0.0k | 15 s |
| media-voice | ok | 100% | 4/4 | 78 | 30.6 s | 0.0000 | 16 | 16 | 0.3 | 2.8k | 0.0k | 14 s |
| file-media-edit | ok | 62% | 7/10 | 49 | 48.1 s | 0.0000 | 16 | 16 | 0.4 | 5.1k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 19 | 1 min 00 s | - | 23 | 22 | 0.3 | 7.6k | 0.0k | 3 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (20744)) | 100% | 9/9 | 78 | 29.5 s | 0.0000 | 7 | 8 | 0.2 | 3.7k | 0.0k | 22 s |
| sec-leak-fix | ok | 88% | 9/10 | 81 | 15.0 s | 0.0000 | 8 | 12 | 0.0 | 1.7k | 0.0k | 4 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 85 | 1 min 17 s | 0.0000 | 43 | 42 | 0.0 | 6.8k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 20 | 1 min 00 s | - | 8 | 7 | 0.3 | 4.9k | 0.0k | 37 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 80 | 1 min 00 s | 0.0000 | 17 | 18 | 0.0 | 7.0k | 0.0k | 11 s |
| ts-plugin-bug | ok | 100% | 8/8 | 82 | 12.1 s | 0.0000 | 5 | 8 | 0.0 | 1.0k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 66 | 58.9 s | 0.0000 | 18 | 18 | 0.1 | 7.7k | 0.0k | 27 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.323 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 66 | 3 min 45 s | 0.0000 | 22 | 22 | 0.0 | 32.2k | 0.0k | 79 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 6 | 1 min 00 s | - | 23 | 27 | 0.3 | 2.3k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:57058", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 82 | 33.9 s | 0.0000 | 27 | 26 | 0.0 | 3.0k | 0.0k | - |
| web-plan-ranking | ok | 100% | 9/9 | 73 | 2 min 21 s | 0.0000 | 13 | 16 | 0.3 | 7.6k | 0.0k | 75 s |
| web-word-universe | ok | 62% | 6/9 | 53 | 2 min 52 s | 0.0000 | 22 | 26 | 0.0 | 20.9k | 0.0k | 16 s |

## Failed checks

- `bo-pnl-runway` ebitda per month: 2026-01: expected -210278.96, received -203812.19
- `bo-pnl-runway` 3-month average burn: expected 197288.23, received 190820.54
- `bo-pnl-runway` runway in months: expected 9.363713182484327, received 9.68
- `cmp-handoff` summary exists and fits in 1000 characters: 1141 characters
- `cmp-handoff` answer file_line: expected 'a match for \\bstart_server\\.ps1\\b.{0,40}?\\b165\\b', received None
- `cmp-handoff` answer final_decode: expected 'a match for ^(?!.*37[.,]8)(?=.*(?<![\\w.,+-])38(?:[.,]0+)?(?!\\d|[.,]\\d))', received None
- `cmp-handoff` answer final_vram_mib: expected 'a match for (?<![\\w.,+-])7697(?:[.,]0+)?(?!\\w|[.,]\\d)', received ''
- `cmp-handoff` answer discarded_quant: expected 'a match for ^(?=.*\\bQ6(?:_?K)?\\b)(?!.*\\b(?!Q6(?:_?K)?\\b)(?:I?Q\\d+[A-Z0-9_]*|BF16|FP(?:16|32)|F(?:16|32))\\b)', received None
- `cmp-handoff` answer pending: expected 'a match for ^(?!.*\\broot\\b)(?=.*\\bREADME\\b)(?=.*\\b(?:update|fix|remove|edit|replace|check_vision|evals|stale|out of date))', received None
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received None
- `cmp-handoff` does not repeat the spilled VRAM as final: expected 'not 7881', received None
- `infra-gpu-fit` KV cache size: expected 42.95, received 4.294967296
- `infra-gpu-fit` total memory needed: expected 120.95, received 82.294967296
- `infra-gpu-fit` cheapest feasible offer: expected 'of-117', received 'of-101'
- `infra-gpu-fit` hourly price: expected 3.58, received 1.79
- `infra-gpu-fit` monthly price: expected 2613.4, received 1306.7
- `ir-server-logs` June availability: expected 99.9170910493827, received 99.974
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received ['2025-08-14', '2024-06-30', '2021-07-19', '2019-05-31']
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received ['2024-09-09']
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received []
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received ['2024-03-18']
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
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
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 8 (corações, em-construção, link-antigo, pagina-removida, paixões)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'advogado: missing 0 (none), extra 1 (corações)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 249, 'relations': 762, 'most_connected': 'tempo'}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 2)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 5); tested significance (call 4); recorded the result (call 7)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 3); used the chart of accounts (call 4); used the cash balance (call 5); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 4); read the statement (call 2); recorded the result (call 12)
- `cmp-handoff`: read the session (call 3); wrote the handoff (call 4); not seen: recorded the result
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 3); recorded the result (call 6)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 6); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 6); read the game mode (call 3); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 8); committed (call 7)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 7)
- `gd-integration-repo`: read the docs (call 3); ran the integration test (call 8); ran the whole suite (call 30)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 10)
- `file-media-edit`: read the details (call 2); made the feed photo (call 8); filled the permit (call 10)
- `txt-regex-log`: wrote the regex (call 3); tried it in Python (call 4)
- `rs-lock-bug`: read the crate (call 6); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 12)
- `cu-social-cycle`: made the image (call 7); opened the site (call 1); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 5); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 4); read the settings (call 3); read the owner notes (call 2); recorded the result (call 15)
- `ts-plugin-bug`: read the bus (call 6); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 3); looked at it in a browser (call 7); recorded the result (call 4)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 2)
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 8); replied (call 16)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 12); wrote the dossier (call 15); opened a source (call 2)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 7); wrote the page (call 17); looked at it in a browser (call 18); recorded the result (call 7)
