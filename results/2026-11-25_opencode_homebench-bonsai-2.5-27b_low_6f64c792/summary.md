# mengine-bench 2.8.0: opencode opencode v2.3.2 / homebench/bonsai-2.5-27b (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **56.2** | 72.6 | 13/29 | 56.9 | 0.0 | 50 min 33 s | $0.00 (local) | 5.46M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=1x RTX 5090 (GPU 0); model=Ternary-Bonsai-2.5-27B; ctx=256k; cache=f16; runtime=PrismML llama.cpp fork prism-b12178-03ec600 (linux CUDA 12.8 build); quant=PTQ1_0 ternary 1.76 bpw, prism-ml/Ternary-Bonsai-2.5-27B-GGUF rev f71afa90, file sha256 e0fc5f3d; layout=single GPU, -ngl 99 -fa on -np 1, --jinja; drafter=MTP head in the -mtp GGUF (draft-mtp n 0..3, p-min 0.1, official RTX 5090 preset); temperature=0.6 (server default; top_p 0.95, top_k 20, min_p 0, Qwen3.8 production preset); reasoning_effort=low; provider_id=homebench: Home llama-server via tunnel 15000, outside the managed fichas catalog (mengine catalog policy 997); study=Bonsai 2.5 27B fastest official quant at T 0.6 low (owner 2026-11-24, mengine 1115); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-25, started 2026-11-25T03:30:49Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 41 | 4 min 19 s | 0.0000 | 13 | 12 | 1.3 | 61.6k | 0.0k | 182 s |
| py-async-cancel | timeout (timeout) | 80% | 5/6 | 49 | 1 min 00 s | 0.0000 | 7 | 6 | 1.2 | 12.1k | 0.0k | 38 s |
| ds-ab-playtest | ok | 100% | 5/5 | 89 | 2 min 18 s | 0.0000 | 18 | 19 | 0.7 | 21.8k | 0.0k | 36 s |
| bo-pnl-runway | ok | 100% | 6/6 | 73 | 1 min 40 s | 0.0000 | 16 | 18 | 0.7 | 23.4k | 0.0k | 35 s |
| bo-reconcile | ok | 100% | 5/5 | 79 | 34.6 s | 0.0000 | 6 | 7 | 0.3 | 7.5k | 0.0k | - |
| cmp-handoff | timeout (timeout) | 27% | 4/12 | 30 | 1 min 30 s | 0.0000 | 7 | 7 | 0.8 | 19.0k | 0.0k | 41 s |
| cfg-source-drift | ok | 100% | 5/5 | 93 | 28.0 s | 0.0000 | 8 | 13 | 0.6 | 4.5k | 0.0k | 10 s |
| doc-lab-pdf | ok | 83% | 6/7 | 54 | 43.6 s | 0.0000 | 10 | 10 | 0.7 | 8.3k | 0.0k | 31 s |
| ds-sql-funnel | ok | 100% | 5/5 | 89 | 40.5 s | 0.0000 | 13 | 14 | 0.7 | 7.5k | 0.0k | 3 s |
| ue-packaged-bug | timeout (timeout) | 20% | 2/6 | 6 | 1 min 30 s | 0.0000 | 3 | 7 | 0.5 | 0.4k | 0.0k | - |
| git-merge-conflict | ok | 100% | 7/7 | 92 | 29.8 s | 0.0000 | 13 | 12 | 0.7 | 4.4k | 0.0k | 17 s |
| infra-gpu-fit | ok | 100% | 7/7 | 79 | 24.2 s | 0.0000 | 5 | 6 | 0.5 | 4.6k | 0.0k | 14 s |
| ir-server-logs | ok | 100% | 7/7 | 80 | 29.2 s | 0.0000 | 9 | 11 | 0.4 | 4.5k | 0.0k | 21 s |
| gd-integration-repo | ok | 88% | 9/10 | 78 | 38.8 s | 0.0000 | 13 | 26 | 0.3 | 6.8k | 0.0k | 21 s |
| media-voice | timeout (timeout) | 100% | 4/4 | 67 | 1 min 00 s | 0.0000 | 16 | 15 | 1.0 | 7.7k | 0.0k | 7 s |
| file-media-edit | timeout (timeout) | 100% | 10/10 | 70 | 1 min 30 s | 0.0000 | 18 | 21 | 2.2 | 8.1k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 4 | 1 min 00 s | 0.0000 | 4 | 4 | 0.5 | 13.2k | 0.0k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (2340)) | 100% | 9/9 | 91 | 1 min 08 s | 0.0000 | 17 | 20 | 0.7 | 11.1k | 0.0k | 22 s |
| sec-leak-fix | ok | 88% | 9/10 | 84 | 38.2 s | 0.0000 | 6 | 11 | 0.5 | 7.4k | 0.0k | 21 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 85 | 56.1 s | 0.0000 | 34 | 35 | 0.1 | 9.6k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 9 | 1 min 00 s | 0.0000 | 6 | 5 | 0.8 | 2.5k | 0.0k | - |
| hw-stutter-tuning | timeout (timeout) | 0% | 1/7 | 11 | 1 min 30 s | 0.0000 | 6 | 9 | 0.5 | 18.2k | 0.0k | 83 s |
| ts-plugin-bug | ok | 100% | 8/8 | 96 | 42.8 s | 0.0000 | 13 | 18 | 0.7 | 7.8k | 0.0k | 18 s |
| web-mondrian-landing | ok | 100% | 11/11 | 73 | 3 min 50 s | 0.0000 | 25 | 26 | 0.4 | 50.8k | 0.0k | 149 s |
| 3d-print-homage | timeout (timeout, blue-layout similarity to the print: 0.301 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 43 | 7 min 00 s | 0.0000 | 20 | 26 | 0.7 | 46.5k | 0.0k | 225 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 11 | 1 min 00 s | 0.0000 | 32 | 36 | 0.9 | 5.8k | 0.0k | - |
| cu-webmail | timeout (timeout, write routes (observation only): {"origin": "http://127.0.0.1:49678", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 33% | 5/9 | 21 | 3 min 00 s | 0.0000 | 28 | 34 | 0.5 | 20.9k | 0.0k | 78 s |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 16 | 3 min 30 s | 0.0000 | 7 | 11 | 17.6 | 16.8k | 0.0k | - |
| web-word-universe | timeout (timeout) | 88% | 8/9 | 38 | 6 min 00 s | 0.0000 | 55 | 69 | 0.8 | 61.3k | 0.0k | 40 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `cmp-handoff` summary exists and fits in 1000 characters: 1071 characters
- `cmp-handoff` answer file_line: expected 'a match for \\bstart_server\\.ps1\\b.{0,40}?\\b165\\b', received None
- `cmp-handoff` answer final_decode: expected 'a match for ^(?!.*37[.,]8)(?=.*(?<![\\w.,+-])38(?:[.,]0+)?(?!\\d|[.,]\\d))', received None
- `cmp-handoff` answer final_vram_mib: expected 'a match for (?<![\\w.,+-])7697(?:[.,]0+)?(?!\\w|[.,]\\d)', received ''
- `cmp-handoff` answer discarded_quant: expected 'a match for ^(?=.*\\bQ6(?:_?K)?\\b)(?!.*\\b(?!Q6(?:_?K)?\\b)(?:I?Q\\d+[A-Z0-9_]*|BF16|FP(?:16|32)|F(?:16|32))\\b)', received None
- `cmp-handoff` answer pending: expected 'a match for ^(?!.*\\broot\\b)(?=.*\\bREADME\\b)(?=.*\\b(?:update|fix|remove|edit|replace|check_vision|evals|stale|out of date))', received None
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received None
- `cmp-handoff` does not repeat the spilled VRAM as final: expected 'not 7881', received None
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {'2026-02-10': 5.4, '2026-08-18': 3.38}
- `ue-packaged-bug` crash fixed: the score tracker survives garbage collection: ScoreTracker is not kept alive by UPROPERTY, TStrongObjectPtr, AddToRoot or a reported reference
- `ue-packaged-bug` colors fixed: the palette reaches the cook: /Game/Data/Palettes/DA_Primary is not cooked by the packaging settings (always-cook folder or bCookAll), the asset manager or a hard reference
- `ue-packaged-bug` the report names the crash cause: crash_cause: ''
- `ue-packaged-bug` the report names the color cause: no_colors_cause: ''
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received 'no pattern in regex.txt'
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received 'no pattern in regex.txt'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received 'no pattern in regex.txt'
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received 'no pattern in regex.txt'
- `sec-leak-fix` the old token is out of the final answers: the token literal appears in answer(s) [0]; expected it in none
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
- `cu-webmail` invoice PDF saved byte for byte: expected 'a file with the sha256 of LP-2026-0418.pdf', received ['AGENTS.md', 'LP-2026-0418.pdf', 'lp.b64']
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
- `web-word-universe` page runs without script errors: Uncaught TypeError: Cannot read properties of null (reading 'Raycaster')

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 4); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 4); removed duplicate sessions (call 6); tested significance (call 6); recorded the result (call 6)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 6); used the chart of accounts (call 5); used the cash balance (call 4); recorded the result (call 14)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 3); wrote the handoff (call 4); not seen: recorded the result
- `cfg-source-drift`: read the readme (call 4); ran the generator (call 8)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 5); recorded the result (call 9)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 3); excluded test accounts (call 7); recorded the result (call 11)
- `ue-packaged-bug`: read the crash log (call 5); read the game mode (call 6); not seen: recorded the result
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 11); committed (call 10)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 6)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 11)
- `gd-integration-repo`: read the docs (call 5); ran the integration test (call 4); ran the whole suite (call 24)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 3); made the feed photo (call 9); filled the permit (call 9)
- `txt-regex-log`: not seen: wrote the regex; not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 6); ran the tests (call 11)
- `sec-leak-fix`: read the service (call 4); read the config (call 3); ran the tests (call 10)
- `cu-social-cycle`: made the image (call 3); opened the site (call 4); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 6); read the settings (call 4); read the owner notes (call 3); not seen: recorded the result
- `ts-plugin-bug`: read the bus (call 8); ran the tests (call 11)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 6); looked at it in a browser (call 8); recorded the result (call 7)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 8)
- `cu-webmail`: opened the mail app (call 4); downloaded the invoice (call 10); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: recorded the result; not seen: wrote the dossier; opened a source (call 6)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 43); wrote the page (call 47); looked at it in a browser (call 52); recorded the result (call 43)
