# mengine-bench 2.8.0: opencode opencode v2.3.2 / homebench/inkling-2-mini (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **79.3** | 87.7 | 21/29 | 70.1 | 83.0 | 15 min 06 s | $0.00 (local) | 7.90M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Inkling-2-Mini; ctx=256k; cache=BF16; runtime=SGLang lmsysorg/sglang:inkling-2-mini (0.0.0.dev1+inkling2); quant=native NVFP4 experts + MXFP8 (original release, rev ed40e7da); layout=TP 2x RTX 5090, fa4 attention; drafter=DSpark n8 (bundled mtp.safetensors); temperature=0.6 (server preferred params; top_p 1.0, top_k 0, min_p 0 as the vendor default); reasoning_effort=low; provider_id=homebench: same Home SGLang via tunnel 15000, outside the managed fichas catalog (mengine catalog policy 997 admits only ficha models under home); study=inkling 2 mini at T 0.6 (owner 2026-11-24), vs c6463dfa at T 1.0; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-25, started 2026-11-25T03:01:07Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 83% | 7/8 | 74 | 53.6 s | 0.0000 | 17 | 16 | 0.6 | 8.5k | 7.5k | 23 s |
| py-async-cancel | ok | 80% | 5/6 | 71 | 17.9 s | 0.0000 | 6 | 6 | 0.6 | 2.1k | 0.6k | 5 s |
| ds-ab-playtest | ok | 100% | 5/5 | 77 | 11.8 s | 0.0000 | 7 | 6 | 0.5 | 1.5k | 0.2k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 75 | 19.2 s | 0.0000 | 6 | 5 | 0.5 | 2.0k | 0.4k | - |
| bo-reconcile | ok | 100% | 5/5 | 82 | 8.8 s | 0.0000 | 4 | 3 | 0.6 | 1.1k | 0.2k | - |
| cmp-handoff | ok | 27% | 4/12 | 21 | 26.1 s | 0.0000 | 11 | 9 | 0.5 | 2.7k | 0.9k | 7 s |
| cfg-source-drift | ok | 100% | 5/5 | 96 | 8.8 s | 0.0000 | 8 | 7 | 0.3 | 0.8k | 0.3k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 75 | 30.9 s | 0.0000 | 9 | 10 | 0.3 | 2.3k | 1.3k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 76 | 19.8 s | 0.0000 | 17 | 16 | 0.4 | 3.2k | 2.5k | 5 s |
| ue-packaged-bug | ok | 100% | 6/6 | 81 | 17.6 s | 0.0000 | 10 | 9 | 0.4 | 2.5k | 1.7k | - |
| git-merge-conflict | ok | 0% | 6/7 | 57 | 19.6 s | 0.0000 | 16 | 15 | 0.5 | 2.8k | 2.0k | 14 s |
| infra-gpu-fit | ok | 100% | 7/7 | 77 | 9.1 s | 0.0000 | 5 | 4 | 0.5 | 1.1k | 0.7k | - |
| ir-server-logs | ok | 100% | 7/7 | 84 | 13.2 s | 0.0000 | 10 | 9 | 0.4 | 1.4k | 0.7k | - |
| gd-integration-repo | ok | 88% | 9/10 | 64 | 17.4 s | 0.0000 | 10 | 9 | 0.4 | 2.2k | 1.2k | - |
| media-voice | ok | 100% | 4/4 | 81 | 10.6 s | 0.0000 | 7 | 6 | 0.7 | 0.7k | 0.3k | - |
| file-media-edit | ok | 100% | 10/10 | 76 | 40.0 s | 0.0000 | 27 | 26 | 0.6 | 5.9k | 3.0k | - |
| txt-regex-log | ok | 100% | 5/5 | 84 | 38.2 s | 0.0000 | 10 | 9 | 0.4 | 8.8k | 6.3k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (20280)) | 100% | 9/9 | 68 | 22.0 s | 0.0000 | 12 | 11 | 0.6 | 3.9k | 1.3k | 11 s |
| sec-leak-fix | ok | 100% | 10/10 | 83 | 11.0 s | 0.0000 | 8 | 8 | 0.5 | 2.1k | 0.3k | 7 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 79 | 18.5 s | 0.0000 | 32 | 31 | 0.0 | 2.2k | 1.6k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 10 | 1 min 00 s | 0.0000 | 15 | 14 | 0.4 | 11.3k | 9.6k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 75 | 19.0 s | 0.0000 | 12 | 11 | 0.5 | 2.6k | 1.9k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 80 | 16.2 s | 0.0000 | 11 | 10 | 0.4 | 2.1k | 1.2k | 10 s |
| web-mondrian-landing | ok | 100% | 11/11 | 76 | 27.4 s | 0.0000 | 12 | 11 | 0.0 | 7.0k | 1.0k | 16 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.0 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 90% | 11/12 | 45 | 1 min 06 s | 0.0000 | 19 | 18 | 0.3 | 8.9k | 4.8k | 42 s |
| web-fact-search | ok | 100% | 8/8 | 80 | 23.1 s | 0.0000 | 9 | 13 | 0.5 | 1.7k | 0.6k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:64012", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 78 | 24.6 s | 0.0000 | 25 | 24 | 0.0 | 3.6k | 1.4k | - |
| web-plan-ranking | ok | 75% | 7/9 | 50 | 1 min 27 s | 0.0000 | 14 | 13 | 0.4 | 5.1k | 3.2k | 84 s |
| web-word-universe | ok | 100% | 9/9 | 58 | 2 min 49 s | 0.0000 | 92 | 91 | 0.3 | 31.7k | 12.7k | 16 s |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `cmp-handoff` summary exists and fits in 1000 characters: 1402 characters
- `cmp-handoff` summary keeps `--no-mmproj-offload`: `--no-mmproj-offload` is not in the summary
- `cmp-handoff` summary keeps `-ub 512`: `-ub 512` is not in the summary
- `cmp-handoff` summary keeps `7697`: `7697` is not in the summary
- `cmp-handoff` answer final_decode: expected 'a match for ^(?!.*37[.,]8)(?=.*(?<![\\w.,+-])38(?:[.,]0+)?(?!\\d|[.,]\\d))', received '37.8 t/s (UNVERIFIED per HANDOFF; transcript figure, not re-measured here)'
- `cmp-handoff` answer final_vram_mib: expected 'a match for (?<![\\w.,+-])7697(?:[.,]0+)?(?!\\w|[.,]\\d)', received '7881'
- `cmp-handoff` answer discarded_quant: expected 'a match for ^(?=.*\\bQ6(?:_?K)?\\b)(?!.*\\b(?!Q6(?:_?K)?\\b)(?:I?Q\\d+[A-Z0-9_]*|BF16|FP(?:16|32)|F(?:16|32))\\b)', received None
- `cmp-handoff` does not repeat the spilled VRAM as final: expected 'not 7881', received '7881'
- `git-merge-conflict` visible tests left untouched
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `3d-print-homage` counted the boats in the print: expected 3, received None
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2401, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 3); looked at it in a browser (call 4)
- `py-async-cancel`: wrote run.py (call 2); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 5); recorded the result (call 6)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 2); used the chart of accounts (call 2); used the cash balance (call 2); recorded the result (call 5)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 4); recorded the result (call 9)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); not seen: extracted the text; recorded the result (call 10)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 4); excluded test accounts (call 9); recorded the result (call 10)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 3); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 9); committed (call 15)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 9)
- `gd-integration-repo`: read the docs (call 4); ran the integration test (call 4); ran the whole suite (call 6)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 3)
- `file-media-edit`: read the details (call 2); made the feed photo (call 7); filled the permit (call 9)
- `txt-regex-log`: wrote the regex (call 6); tried it in Python (call 5)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 5)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 4)
- `cu-social-cycle`: made the image (call 4); opened the site (call 6); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 5); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 4); read the settings (call 3); read the owner notes (call 3); recorded the result (call 10)
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 5)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 6); looked at it in a browser (call 13); recorded the result (call 10)
- `web-fact-search`: not seen: searched the web; recorded the result (call 13); opened a source (call 5)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 11); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 12); wrote the dossier (call 13); not seen: opened a source
- `web-word-universe`: walked the site (call 1); wrote words.json (call 10); wrote the page (call 48); looked at it in a browser (call 49); recorded the result (call 72)
