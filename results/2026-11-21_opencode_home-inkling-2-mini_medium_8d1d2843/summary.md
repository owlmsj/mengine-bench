# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/inkling-2-mini (medium)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **80.0** | 91.4 | 25/29 | 72.2 | 66.0 | 20 min 13 s | $0.00 (local) | 14.29M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Inkling-2-Mini; runtime=SGLang lmsysorg/sglang:inkling-2-mini (0.0.0.dev1+inkling2); quant=native NVFP4 experts + MXFP8 (original release, rev ed40e7da); ctx=256k; cache=BF16; layout=TP 2x RTX 5090, fa4 attention; drafter=DSpark n8 (bundled mtp.safetensors); temperature=1.0 (model default); reasoning_effort=medium; study=inkling 2 mini engine+quant pick, run 1; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-21, started 2026-11-21T16:12:16Z; bench at 8584f70e1346 (dirty tree); submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 78 | 1 min 11 s | 0.0000 | 15 | 14 | 0.6 | 15.1k | 1.9k | 40 s |
| py-async-cancel | ok | 100% | 6/6 | 86 | 18.2 s | 0.0000 | 9 | 8 | 0.4 | 3.5k | 1.5k | 9 s |
| ds-ab-playtest | ok | 100% | 5/5 | 80 | 14.7 s | 0.0000 | 7 | 6 | 0.4 | 1.6k | 0.3k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 70 | 17.6 s | 0.0000 | 11 | 10 | 0.4 | 4.1k | 0.9k | 8 s |
| bo-reconcile | ok | 100% | 5/5 | 79 | 15.8 s | 0.0000 | 10 | 9 | 0.4 | 2.9k | 1.7k | 10 s |
| cmp-handoff | timeout (timeout) | 0% | 1/12 | 4 | 1 min 30 s | 0.0000 | 8 | 7 | 0.4 | 0.7k | 0.5k | - |
| cfg-source-drift | ok | 100% | 5/5 | 83 | 11.1 s | 0.0000 | 10 | 9 | 0.4 | 1.5k | 0.8k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 77 | 18.2 s | 0.0000 | 10 | 10 | 0.4 | 3.3k | 2.6k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 79 | 14.7 s | 0.0000 | 11 | 10 | 0.4 | 2.8k | 0.8k | 9 s |
| ue-packaged-bug | ok | 100% | 6/6 | 85 | 14.8 s | 0.0000 | 9 | 8 | 0.4 | 2.0k | 1.2k | - |
| git-merge-conflict | ok | 100% | 7/7 | 88 | 19.1 s | 0.0000 | 17 | 16 | 0.5 | 2.5k | 1.5k | 11 s |
| infra-gpu-fit | ok | 100% | 7/7 | 76 | 10.0 s | 0.0000 | 6 | 5 | 0.4 | 1.4k | 0.8k | - |
| ir-server-logs | ok | 100% | 7/7 | 81 | 16.1 s | 0.0000 | 11 | 10 | 0.4 | 2.1k | 0.9k | 12 s |
| gd-integration-repo | ok | 88% | 9/10 | 61 | 1 min 58 s | 0.0000 | 124 | 123 | 0.4 | 16.0k | 9.3k | - |
| media-voice | ok | 100% | 4/4 | 75 | 23.6 s | 0.0000 | 15 | 14 | 0.7 | 2.1k | 0.9k | - |
| file-media-edit | ok | 100% | 10/10 | 87 | 37.8 s | 0.0000 | 18 | 17 | 0.7 | 6.2k | 4.4k | - |
| txt-regex-log | ok | 100% | 5/5 | 91 | 49.1 s | 0.0000 | 13 | 12 | 0.4 | 11.2k | 9.4k | 25 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (27904)) | 100% | 9/9 | 74 | 18.5 s | 0.0000 | 9 | 8 | 0.5 | 3.2k | 1.1k | 13 s |
| sec-leak-fix | ok | 100% | 10/10 | 77 | 21.4 s | 0.0000 | 15 | 15 | 0.4 | 4.1k | 1.5k | 9 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 79 | 39.7 s | 0.0000 | 40 | 39 | 0.0 | 4.6k | 2.7k | 10 s |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 12 | 1 min 00 s | 0.0000 | 19 | 18 | 0.4 | 12.5k | 9.9k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 84 | 29.0 s | 0.0000 | 15 | 14 | 0.6 | 3.7k | 2.4k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 87 | 14.0 s | 0.0000 | 8 | 7 | 0.4 | 2.4k | 0.8k | 7 s |
| web-mondrian-landing | ok | 100% | 11/11 | 55 | 46.5 s | 0.0000 | 28 | 27 | 0.0 | 9.3k | 2.3k | 20 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.323 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 50 | 1 min 49 s | 0.0000 | 23 | 22 | 1.0 | 12.5k | 10.1k | 53 s |
| web-fact-search | ok | 100% | 8/8 | 83 | 22.8 s | 0.0000 | 8 | 9 | 0.5 | 1.4k | 0.4k | 19 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:54561", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 76 | 34.9 s | 0.0000 | 30 | 29 | 0.0 | 3.8k | 2.1k | - |
| web-plan-ranking | ok | 100% | 9/9 | 69 | 1 min 38 s | 0.0000 | 26 | 25 | 0.4 | 12.0k | 5.2k | 91 s |
| web-word-universe | ok | 62% | 6/9 | 68 | 2 min 39 s | 0.0000 | 61 | 60 | 0.4 | 33.0k | 12.0k | 15 s |

## Failed checks

- `cmp-handoff` summary exists and fits in 1000 characters: no summary file
- `cmp-handoff` summary keeps `--no-mmproj-offload`: `--no-mmproj-offload` is not in the summary
- `cmp-handoff` summary keeps `-ub 512`: `-ub 512` is not in the summary
- `cmp-handoff` summary keeps `7697`: `7697` is not in the summary
- `cmp-handoff` answer file_line: expected 'a match for \\bstart_server\\.ps1\\b.{0,40}?\\b165\\b', received None
- `cmp-handoff` answer final_decode: expected 'a match for ^(?!.*37[.,]8)(?=.*(?<![\\w.,+-])38(?:[.,]0+)?(?!\\d|[.,]\\d))', received None
- `cmp-handoff` answer final_vram_mib: expected 'a match for (?<![\\w.,+-])7697(?:[.,]0+)?(?!\\w|[.,]\\d)', received ''
- `cmp-handoff` answer discarded_quant: expected 'a match for ^(?=.*\\bQ6(?:_?K)?\\b)(?!.*\\b(?!Q6(?:_?K)?\\b)(?:I?Q\\d+[A-Z0-9_]*|BF16|FP(?:16|32)|F(?:16|32))\\b)', received None
- `cmp-handoff` answer pending: expected 'a match for ^(?!.*\\broot\\b)(?=.*\\bREADME\\b)(?=.*\\b(?:update|fix|remove|edit|replace|check_vision|evals|stale|out of date))', received None
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received None
- `cmp-handoff` does not repeat the spilled VRAM as final: expected 'not 7881', received None
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `web-word-universe` collected exactly the site's words: missing 52 (aflição, almoço, amanhã, angústia, açougueiro), extra 52 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acento: missing 1 (sílaba), extra 1 (silaba)'
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 4); looked at it in a browser (call 5)
- `py-async-cancel`: wrote run.py (call 3); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 2); removed duplicate sessions (call 4); tested significance (call 6); recorded the result (call 6)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 3); used the chart of accounts (call 3); used the cash balance (call 3); recorded the result (call 7)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 6)
- `cmp-handoff`: read the session (call 1); not seen: wrote the handoff; not seen: recorded the result
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 6); recorded the result (call 10)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 8); recorded the result (call 8)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 2); recorded the result (call 7)
- `git-merge-conflict`: merged the branch (call 6); ran the tests (call 9); not seen: committed
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 3); read the logs (call 1); recorded the result (call 9)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 2); ran the whole suite (call 9)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 13)
- `file-media-edit`: read the details (call 2); made the feed photo (call 13); filled the permit (call 14)
- `txt-regex-log`: wrote the regex (call 5); tried it in Python (call 6)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 6)
- `sec-leak-fix`: read the service (call 3); read the config (call 3); ran the tests (call 4)
- `cu-social-cycle`: made the image (call 7); opened the site (call 11); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 4); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 4); read the settings (call 3); read the owner notes (call 3); recorded the result (call 14)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 4)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 6); looked at it in a browser (call 7); recorded the result (call 19)
- `web-fact-search`: not seen: searched the web; recorded the result (call 9); opened a source (call 3)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 11); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 21); wrote the dossier (call 23); opened a source (call 4)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 25); wrote the page (call 36); looked at it in a browser (call 46); recorded the result (call 25)
