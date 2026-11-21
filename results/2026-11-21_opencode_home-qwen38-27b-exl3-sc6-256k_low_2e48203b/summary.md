# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **67.0** | 82.5 | 17/29 | 62.8 | 30.5 | 30 min 52 s | $0.00 (local) | 5.10M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of super-adapter merge; ctx=256k; cache=FP16; layout=native TP 2x RTX 5090; drafter=MTP n4 dynamic; temperature=0.6; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715 (pi+hermes+opencode at 1/2), THINKING OFF; study=pilot 7 control: super-adapter off run 1; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-21, started 2026-11-21T13:09:51Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 80 | 2 min 26 s | 0.0000 | 19 | 18 | 0.4 | 11.1k | 0.0k | 76 s |
| py-async-cancel | ok | 80% | 5/6 | 55 | 23.1 s | 0.0000 | 5 | 4 | 0.3 | 1.6k | 0.0k | 5 s |
| ds-ab-playtest | ok | 100% | 5/5 | 86 | 56.4 s | 0.0000 | 6 | 6 | 0.0 | 1.7k | 0.0k | 42 s |
| bo-pnl-runway | ok | 100% | 6/6 | 84 | 36.2 s | 0.0000 | 9 | 10 | 0.0 | 2.5k | 0.0k | 16 s |
| bo-reconcile | ok | 100% | 5/5 | 75 | 21.0 s | 0.0000 | 6 | 7 | 0.0 | 1.4k | 0.0k | 9 s |
| cmp-handoff | ok | 100% | 12/12 | 82 | 52.8 s | 0.0000 | 19 | 17 | 0.0 | 3.7k | 0.0k | 10 s |
| cfg-source-drift | ok | 100% | 5/5 | 90 | 24.3 s | 0.0000 | 8 | 12 | 0.1 | 1.5k | 0.0k | 10 s |
| doc-lab-pdf | timeout (timeout) | 83% | 6/7 | 40 | 1 min 00 s | 0.0000 | 16 | 15 | 0.0 | 4.9k | 0.0k | 13 s |
| ds-sql-funnel | ok | 100% | 5/5 | 89 | 43.0 s | 0.0000 | 10 | 10 | 0.2 | 3.4k | 0.0k | 5 s |
| ue-packaged-bug | ok | 80% | 5/6 | 40 | 33.5 s | 0.0000 | 10 | 14 | 0.0 | 2.4k | 0.0k | 10 s |
| git-merge-conflict | ok | 100% | 7/7 | 86 | 24.6 s | 0.0000 | 10 | 9 | 0.0 | 1.3k | 0.0k | 7 s |
| infra-gpu-fit | ok | 100% | 7/7 | 93 | 24.4 s | 0.0000 | 6 | 7 | 0.0 | 1.8k | 0.0k | 9 s |
| ir-server-logs | ok | 83% | 6/7 | 45 | 49.0 s | 0.0000 | 8 | 8 | 0.0 | 1.7k | 0.0k | 34 s |
| gd-integration-repo | ok | 100% | 10/10 | 84 | 33.5 s | 0.0000 | 7 | 17 | 0.1 | 2.2k | 0.0k | 21 s |
| media-voice | ok | 100% | 4/4 | 83 | 27.6 s | 0.0000 | 9 | 8 | 0.9 | 1.4k | 0.0k | 8 s |
| file-media-edit | timeout (timeout) | 88% | 9/10 | 55 | 1 min 30 s | 0.0000 | 18 | 19 | 0.6 | 6.7k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 75% | 4/5 | 46 | 1 min 00 s | 0.0000 | 12 | 11 | 0.0 | 4.7k | 0.0k | 4 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (17520)) | 100% | 9/9 | 78 | 41.6 s | 0.0000 | 12 | 14 | 0.0 | 3.3k | 0.0k | 15 s |
| sec-leak-fix | ok | 88% | 9/10 | 74 | 23.6 s | 0.0000 | 7 | 10 | 0.0 | 1.7k | 0.0k | 10 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 92 | 56.7 s | 0.0000 | 23 | 23 | 0.0 | 2.1k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 4 | 1 min 00 s | 0.0000 | 2 | 1 | 0.5 | 0.2k | 0.0k | - |
| hw-stutter-tuning | ok | 67% | 5/7 | 33 | 45.3 s | 0.0000 | 9 | 10 | 0.0 | 3.2k | 0.0k | 15 s |
| ts-plugin-bug | ok | 100% | 8/8 | 84 | 33.5 s | 0.0000 | 11 | 14 | 0.1 | 2.3k | 0.0k | 9 s |
| web-mondrian-landing | ok | 100% | 11/11 | 70 | 1 min 07 s | 0.0000 | 10 | 9 | 0.2 | 5.1k | 0.0k | 37 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.246 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 41 | 2 min 36 s | 0.0000 | 25 | 24 | 0.0 | 11.1k | 0.0k | 28 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 13 | 1 min 00 s | 0.0000 | 16 | 21 | 0.6 | 1.6k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:52818", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 73 | 1 min 27 s | 0.0000 | 29 | 28 | 0.4 | 3.4k | 0.0k | - |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 7 | 3 min 30 s | 0.0000 | 10 | 16 | 0.2 | 1.5k | 0.0k | - |
| web-word-universe | ok | 50% | 5/9 | 38 | 3 min 26 s | 0.0000 | 43 | 46 | 0.5 | 13.5k | 0.0k | 13 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `doc-lab-pdf` leaves out what stayed in range: expected ['glucose', 'ldl'], received ['glicose em jejum', 'colesterol ldl', 'hemoglobina glicada (hba1c)']
- `ue-packaged-bug` crash fixed: the score tracker survives garbage collection: ScoreTracker is not kept alive by UPROPERTY, TStrongObjectPtr, AddToRoot or a reported reference
- `ir-server-logs` June availability: expected 99.9170910493827, received 99.9745
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received ['2023-02-30', '2023-06-31', '2023-02-29', '2023-09-30', '2023-10-31']
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `hw-stutter-tuning` cause named: expected "the GPU link's power-saving state (ASPM L1 on its root port)", received 'Windows Defender real-time protection (MsMpEng.exe) scanning the game: the sensor log shows Defender becoming the top CPU process at seconds 43-45 with DPC latency spiking from ~50-90us to ~400-455us and disk activity
- `hw-stutter-tuning` ASPM off on the GPU root port: expected 'pcie_aspm_rp1_gpu -> disabled', received [('defender_exclusions', "['Arena.exe']")]
- `web-fact-search` sqlite_3_40_0_release_date value: expected '2022-11-16', received None
- `web-fact-search` sqlite_3_40_0_release_date primary source: expected 'an http(s) URL on sqlite.org', received None
- `web-fact-search` postgresql_15_0_release_date value: expected '2022-10-13', received None
- `web-fact-search` postgresql_15_0_release_date primary source: expected 'an http(s) URL on postgresql.org', received None
- `web-fact-search` unicode_15_0_characters_added value: expected 4489, received None
- `web-fact-search` unicode_15_0_characters_added primary source: expected 'an http(s) URL on unicode.org', received None
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-plan-ranking` all six plans recorded: expected ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real'], received []
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor I': ['1990-03-16'], 'Collor II': ['1991-01-31'], 'Real': ['1994-03-01', '1994-07-01']}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1], 'Real': [2477.15, 22.41]}, received {'Cruzado': [None, None], 'Bresser': [None, None], 'Verao': [None, None], 'Collor I': [None, None], 'Collor
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Verao': [14], 'Collor I': [10], 'Collor II': [37, 41], 'Real': [60]}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` scores follow the rubric: expected "0.7*drop + 0.3*durability from the row's own numbers", received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received None
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 0, 'urls': 0, 'plans': []}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 60 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acento: missing 0 (none), extra 1 (silaba)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 252, 'relations': 1113, 'most_connected': 'palavra'}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=saudade does not show its 5 relations, missing carinho, esperança, nostalgia

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 2)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 3); used the cash balance (call 4); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 3); recorded the result (call 17)
- `cfg-source-drift`: read the readme (call 4); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 6); read the game mode (call 4); recorded the result (call 12)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 9); committed (call 9)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 2); read the policy (call 3); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 3); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); ran the whole suite (call 17)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 5)
- `file-media-edit`: read the details (call 2); made the feed photo (call 5); filled the permit (call 8)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 11)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: not seen: read the raw bytes; not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 6); read the settings (call 3); read the owner notes (call 4); recorded the result (call 9)
- `ts-plugin-bug`: read the bus (call 7); ran the tests (call 9)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); replied (call 21)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: recorded the result; not seen: wrote the dossier; opened a source (call 2)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 4); wrote the page (call 7); looked at it in a browser (call 10); recorded the result (call 6)
