# mengine-bench 2.8.0: opencode opencode v2.2.5 / tencent-tokenhub/hy4-flash (high)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **61.1** | 75.7 | 13/29 | 66.3 | 0.0 | 54 min 36 s | >= $0.03 | 2.33M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=tencent-tokenhub; model=hy4-flash; tier=1; role=scout-r; opencode_config=managed + hy4-flash entry (#1029 projection); price_source=TokenHub console 2026-11-19, 50% off until 2026-11-30: 0.035 in / 0.1405 out / 0.0015 cache USD per Mtok; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-19, started 2026-11-19T12:01:21Z; bench at 891efeb85544; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | timeout (timeout) | 100% | 8/8 | 81 | 5 min 00 s | - | 21 | 22 | 0.6 | 21.6k | 9.3k | 101 s |
| py-async-cancel | timeout (timeout) | 100% | 6/6 | 59 | 1 min 00 s | - | 4 | 4 | 2.0 | 6.9k | 5.2k | 34 s |
| ds-ab-playtest | ok | 100% | 5/5 | 86 | 1 min 07 s | 0.0016 | 11 | 11 | 0.8 | 5.0k | 1.5k | 14 s |
| bo-pnl-runway | ok | 100% | 6/6 | 85 | 52.6 s | 0.0016 | 7 | 9 | 0.6 | 5.0k | 2.4k | 13 s |
| bo-reconcile | ok | 100% | 5/5 | 84 | 1 min 10 s | 0.0012 | 6 | 7 | 0.7 | 3.0k | 1.8k | 43 s |
| cmp-handoff | timeout (timeout, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 0% | 1/12 | 3 | 1 min 30 s | - | 2 | 2 | 0.8 | 0.2k | 0.0k | - |
| cfg-source-drift | ok (redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 5/5 | 97 | 35.9 s | 0.0010 | 7 | 11 | 0.6 | 1.9k | 0.7k | 11 s |
| doc-lab-pdf | ok (redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 7/7 | 70 | 37.0 s | 0.0010 | 7 | 7 | 0.6 | 2.3k | 1.2k | 24 s |
| ds-sql-funnel | ok (redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 5/5 | 93 | 1 min 08 s | 0.0012 | 11 | 11 | 0.5 | 2.7k | 0.8k | 4 s |
| ue-packaged-bug | ok (redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 6/6 | 91 | 54.2 s | 0.0015 | 10 | 17 | 0.5 | 4.4k | 2.4k | 24 s |
| git-merge-conflict | ok (redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 0% | 6/7 | 83 | 51.8 s | 0.0012 | 10 | 9 | 0.9 | 2.7k | 0.8k | 23 s |
| infra-gpu-fit | ok (redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 7/7 | 66 | 18.3 s | 0.0008 | 3 | 4 | 0.3 | 1.7k | 1.2k | 7 s |
| ir-server-logs | ok (redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 7/7 | 88 | 55.5 s | 0.0016 | 10 | 10 | 0.4 | 3.6k | 1.8k | 40 s |
| gd-integration-repo | ok (redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 88% | 9/10 | 69 | 1 min 39 s | 0.0021 | 17 | 16 | 0.6 | 5.9k | 3.9k | 50 s |
| media-voice | ok (redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 4/4 | 97 | 55.2 s | 0.0009 | 7 | 6 | 0.8 | 1.8k | 0.7k | - |
| file-media-edit | timeout (timeout, evidence 'out/feed-photo.jpg' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes, evidence 'out/permit-filled.pdf' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 0% | 2/10 | 10 | 1 min 30 s | - | 8 | 11 | 1.0 | 4.2k | 3.1k | - |
| txt-regex-log | timeout (timeout, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 5/5 | 56 | 1 min 00 s | - | 3 | 2 | 1.0 | 8.4k | 8.1k | 51 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (35936), redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 9/9 | 93 | 1 min 51 s | 0.0021 | 13 | 14 | 1.4 | 7.4k | 3.7k | 33 s |
| sec-leak-fix | ok (redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 88% | 9/10 | 83 | 1 min 26 s | 0.0017 | 12 | 15 | 0.8 | 5.4k | 3.4k | 30 s |
| cu-social-cycle | timeout (timeout, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 44% | 6/11 | 28 | 3 min 00 s | - | 16 | 21 | 0.3 | 3.3k | 2.0k | 38 s |
| ds-sqlite-recover | timeout (timeout, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 0% | 1/6 | 8 | 1 min 00 s | - | 5 | 4 | 1.0 | 1.3k | 0.8k | - |
| hw-stutter-tuning | timeout (timeout, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 0% | 1/7 | 4 | 1 min 30 s | - | 5 | 4 | 0.4 | 0.4k | 0.1k | - |
| ts-plugin-bug | timeout (timeout, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 8/8 | 90 | 1 min 00 s | - | 6 | 10 | 0.5 | 2.1k | 0.7k | 16 s |
| web-mondrian-landing | timeout (timeout, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 11/11 | 73 | 5 min 00 s | - | 33 | 34 | 0.2 | 21.4k | 11.4k | 81 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.333 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6), redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 12/12 | 77 | 5 min 36 s | 0.0068 | 18 | 19 | 1.1 | 29.3k | 18.7k | 99 s |
| web-fact-search | ok (redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 8/8 | 94 | 36.3 s | 0.0012 | 5 | 6 | 0.7 | 1.1k | 0.3k | 23 s |
| cu-webmail | timeout (timeout, write routes (observation only): {"origin": "http://127.0.0.1:53515", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 100% | 9/9 | 80 | 3 min 00 s | - | 27 | 31 | 0.3 | 6.4k | 2.5k | 104 s |
| web-plan-ranking | timeout (timeout, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 0% | 1/9 | 12 | 3 min 30 s | - | 18 | 23 | 0.7 | 15.8k | 13.1k | - |
| web-word-universe | timeout (timeout, redone by `mengine-bench redo` (#205); the first attempt is under `redo` in result.json) | 75% | 7/9 | 62 | 6 min 00 s | - | 18 | 22 | 0.9 | 19.9k | 6.9k | 39 s |

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
- `git-merge-conflict` visible tests left untouched
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` photo is a JPEG: expected 'a readable JPEG', received 'FileNotFoundError reading out/feed-photo.jpg'
- `file-media-edit` photo is exactly 1080x1350: expected 'a readable JPEG', received 'FileNotFoundError reading out/feed-photo.jpg'
- `file-media-edit` balloon fully in frame and undistorted: expected 'a readable JPEG', received 'FileNotFoundError reading out/feed-photo.jpg'
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'no out/permit-filled.pdf'
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `cu-social-cycle` test post published with the exact text: expected 'Testing the new Bluehaze uploader: Harbor Day is on.', received []
- `cu-social-cycle` test post carries cover.png: expected ['e33f6815d0d6ffbdd482e1b0c06d2c994390894a620f9b9635835c5ccb54fa77'], received []
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
- `web-word-universe` collected exactly the site's words: missing 52 (aflição, almoço, amanhã, angústia, açougueiro), extra 52 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acento: missing 1 (sílaba), extra 1 (silaba)'

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 3); looked at it in a browser (call 5)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 2); removed duplicate sessions (call 5); tested significance (call 7); recorded the result (call 9)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 4); used the chart of accounts (call 5); used the cash balance (call 3); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: not seen: read the session; not seen: wrote the handoff; not seen: recorded the result
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 4); recorded the result (call 6)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 7)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 7); recorded the result (call 11)
- `git-merge-conflict`: merged the branch (call 4); ran the tests (call 6); committed (call 8)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 2); read the policy (call 1); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 3); read the logs (call 1); recorded the result (call 9)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 2); ran the whole suite (call 4)
- `media-voice`: used a speech engine (call 2); wrote the audio (call 3)
- `file-media-edit`: read the details (call 2); not seen: made the feed photo; not seen: filled the permit
- `txt-regex-log`: wrote the regex (call 2); not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 9)
- `sec-leak-fix`: read the service (call 3); read the config (call 2); ran the tests (call 11)
- `cu-social-cycle`: made the image (call 7); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: not seen: read the raw bytes; not seen: wrote the JSON
- `hw-stutter-tuning`: not seen: read the frame capture; not seen: read the sensor log; not seen: read the settings; read the owner notes (call 4); not seen: recorded the result
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 4); looked at it in a browser (call 5)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 5); recorded the result (call 3)
- `web-fact-search`: not seen: searched the web; recorded the result (call 5); opened a source (call 1)
- `cu-webmail`: opened the mail app (call 4); downloaded the invoice (call 16); replied (call 8)
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 2); not seen: recorded the result; not seen: wrote the dossier; opened a source (call 2)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 14); wrote the page (call 19); looked at it in a browser (call 20); recorded the result (call 14)
