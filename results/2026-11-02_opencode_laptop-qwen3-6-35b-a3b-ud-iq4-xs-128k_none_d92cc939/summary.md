# mengine-bench 2.1.0: opencode opencode v2.2.5 / laptop/qwen3-6-35b-a3b-ud-iq4-xs-128k (default effort)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **29.3** | 41.1 | 0/20 | 30.9 | 0.0 | 47 min 48 s | $0.00 (price) | 0.15M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=opencode; tier=4; role=default; provider=local; server_gpu=RTX 4070 Laptop 8 GB + CPU offload; model=Qwen3.6-35B-A3B; runtime=llama.cpp; quant=UD-IQ4_XS; ctx=128k; thinking=on, budget 2048 (ficha default); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-03T00:11:12Z; bench at a27408ad0009; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | timeout (timeout) | 0% | 0/4 | 9 | 3 min 00 s | 0.0000 | 5 | 6 | 1.5k | 0.0k | 118 s |
| bo-pnl-runway | ok | 0% | 0/5 | 30 | 2 min 17 s | 0.0000 | 11 | 14 | 3.5k | 0.0k | 77 s |
| bo-reconcile | timeout (timeout) | 0% | 0/4 | 20 | 1 min 30 s | 0.0000 | 5 | 6 | 1.4k | 0.0k | 49 s |
| cmp-handoff | timeout (timeout) | 27% | 3/11 | 27 | 1 min 30 s | 0.0000 | 8 | 10 | 2.1k | 0.0k | 59 s |
| cfg-source-drift | timeout (timeout) | 100% | 3/3 | 63 | 1 min 00 s | 0.0000 | 5 | 17 | 1.5k | 0.0k | 43 s |
| doc-lab-pdf | timeout (timeout) | 0% | 0/6 | 9 | 1 min 00 s | 0.0000 | 7 | 7 | 1.2k | 0.0k | 42 s |
| ds-sql-funnel | timeout (timeout) | 0% | 0/3 | 6 | 1 min 30 s | 0.0000 | 7 | 7 | 2.3k | 0.0k | 26 s |
| ue-packaged-bug | timeout (timeout) | 40% | 2/5 | 31 | 1 min 30 s | 0.0000 | 9 | 18 | 2.3k | 0.0k | 63 s |
| git-merge-conflict | timeout (timeout) | 100% | 6/6 | 67 | 1 min 30 s | 0.0000 | 10 | 11 | 2.0k | 0.0k | 45 s |
| infra-gpu-fit | timeout (timeout) | 0% | 0/6 | 8 | 1 min 00 s | 0.0000 | 3 | 4 | 1.7k | 0.0k | - |
| ir-server-logs | timeout (timeout) | 0% | 0/6 | 6 | 1 min 00 s | 0.0000 | 2 | 6 | 0.4k | 0.0k | - |
| gd-integration-repo | timeout (timeout) | 100% | 8/8 | 81 | 2 min 30 s | 0.0000 | 9 | 21 | 3.5k | 0.0k | 126 s |
| rs-lock-bug | timeout (timeout) | 75% | 5/6 | 38 | 3 min 00 s | 0.0000 | 10 | 11 | 4.8k | 0.0k | 77 s |
| sec-leak-fix | timeout (timeout) | 100% | 8/8 | 46 | 1 min 30 s | 0.0000 | 5 | 10 | 2.4k | 0.0k | 50 s |
| hw-stutter-tuning | timeout (timeout) | 0% | 0/6 | 3 | 1 min 30 s | 0.0000 | 2 | 5 | 0.3k | 0.0k | - |
| ts-plugin-bug | timeout (timeout) | 100% | 7/7 | 64 | 1 min 00 s | 0.0000 | 4 | 9 | 1.4k | 0.0k | 55 s |
| web-mondrian-landing | timeout (timeout) | 100% | 10/10 | 62 | 5 min 00 s | 0.0000 | 13 | 14 | 4.5k | 0.0k | 119 s |
| 3d-print-homage | timeout (timeout) | 80% | 9/11 | 24 | 7 min 00 s | 0.0000 | 9 | 10 | 8.0k | 0.0k | 292 s |
| web-plan-ranking | timeout (timeout) | 0% | 0/8 | 8 | 3 min 30 s | 0.0000 | 8 | 13 | 3.4k | 0.0k | - |
| web-word-universe | timeout (timeout) | 0% | 0/6 | 17 | 6 min 00 s | 0.0000 | 13 | 19 | 4.0k | 0.0k | - |

## Failed checks

- `ds-ab-playtest` deduplicated session counts: expected {'sessions_a': 900, 'sessions_b': 900}, received {'sessions_a': None, 'sessions_b': None}
- `ds-ab-playtest` completion rates: expected (0.38, 0.4666666666666667), received {'completion_rate_a': None, 'completion_rate_b': None}
- `ds-ab-playtest` the gain is significant: expected 'about 0.0002', received None
- `ds-ab-playtest` ship decision: expected True, received None
- `bo-pnl-runway` revenue per month: 2026-01: expected 200510.87, received None
- `bo-pnl-runway` gross_margin_pct per month: 2026-01: expected 70.0305923564144, received None
- `bo-pnl-runway` ebitda per month: 2026-01: expected -210278.96, received None
- `bo-pnl-runway` 3-month average burn: expected 197288.23, received 190820.54
- `bo-pnl-runway` runway in months: expected 9.363713182484327, received 9.68
- `bo-reconcile` unpaid invoices: expected ['INV-1008', 'INV-1030', 'INV-1033'], received []
- `bo-reconcile` duplicated payments: expected ['INV-1015'], received []
- `bo-reconcile` mismatched amounts: expected ['INV-1021', 'INV-1036'], received []
- `bo-reconcile` invoiced vs paid on mismatches: expected [{'id': 'INV-1021', 'invoiced': 21320.36, 'paid': 21070.36}, {'id': 'INV-1036', 'invoiced': 8619.16, 'paid': 7757.24}], received []
- `cmp-handoff` summary exists and fits in 1000 characters: 1127 characters
- `cmp-handoff` answer file_line: expected 'a match for \\bstart_server\\.ps1\\b.{0,40}?\\b165\\b', received None
- `cmp-handoff` answer final_decode: expected 'a match for ^(?!.*37[.,]8)(?=.*(?<![\\w.,+-])38(?:[.,]0+)?(?!\\d|[.,]\\d))', received None
- `cmp-handoff` answer final_vram_mib: expected 'a match for (?<![\\w.,+-])7697(?:[.,]0+)?(?!\\w|[.,]\\d)', received ''
- `cmp-handoff` answer discarded_quant: expected 'a match for \\bQ6(?:_?K)?\\b', received None
- `cmp-handoff` answer pending: expected 'a match for ^(?!.*\\broot\\b)(?=.*\\bREADME\\b)(?=.*\\b(?:update|fix|remove|edit|replace|check_vision|evals|stale|out of date))', received None
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received None
- `cmp-handoff` does not repeat the spilled VRAM as final: expected 'not 7881', received None
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {}
- `doc-lab-pdf` glucose history: expected {'2026-02-10': 92.0, '2026-08-18': 109.9}, received {}
- `doc-lab-pdf` ldl history: expected {'2026-02-10': 118.0, '2026-08-18': 143.08}, received {}
- `doc-lab-pdf` creatinine history: expected {'2026-02-10': 0.95, '2026-08-18': 0.86}, received {}
- `doc-lab-pdf` flags what got worse and left the range: expected ['glucose', 'ldl'], received None
- `doc-lab-pdf` leaves out what stayed in range: expected ['glucose', 'ldl'], received None
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {}
- `ue-packaged-bug` crash fixed: the score tracker survives garbage collection: ScoreTracker is not kept alive by UPROPERTY, TStrongObjectPtr, AddToRoot or a reported reference
- `ue-packaged-bug` the report names the crash cause: crash_cause: ''
- `ue-packaged-bug` the report names the color cause: no_colors_cause: ''
- `infra-gpu-fit` weights size: expected 70.0, received None
- `infra-gpu-fit` KV cache size: expected 42.95, received None
- `infra-gpu-fit` total memory needed: expected 120.95, received None
- `infra-gpu-fit` cheapest feasible offer: expected 'of-117', received None
- `infra-gpu-fit` hourly price: expected 3.58, received None
- `infra-gpu-fit` monthly price: expected 2613.4, received None
- `ir-server-logs` incident start: expected '2026-06-02 03:17:42', received None
- `ir-server-logs` incident end: expected '2026-06-02 03:53:31', received None
- `ir-server-logs` minutes down: expected 35.81666666666667, received None
- `ir-server-logs` June availability: expected 99.9170910493827, received None
- `ir-server-logs` SLO 99.9 met: expected True, received None
- `ir-server-logs` root cause = /data disk full: expected 'the /data disk was full', received None
- `rs-lock-bug` hidden opposite transfers do not hang: opposite_transfers_do_not_hang failed
- `hw-stutter-tuning` average FPS: expected 137.3, received None
- `hw-stutter-tuning` 1% low FPS: expected 45.4, received None
- `hw-stutter-tuning` cause named: expected "the GPU link's power-saving state (ASPM L1 on its root port)", received None
- `hw-stutter-tuning` ASPM off on the GPU root port: expected 'pcie_aspm_rp1_gpu -> disabled', received []
- `hw-stutter-tuning` GPU link speed kept: expected 'changes that leave the link speed alone', received []
- `hw-stutter-tuning` BIOS overclock kept: expected 'no XMP, PBO or core ratio change', received []
- `3d-print-homage` counted the boats in the print: expected 3, received None
- `3d-print-homage` named the mountain: expected 'Mount Fuji', received None
- `web-plan-ranking` all six plans recorded: expected ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real'], received []
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor I': ['1990-03-16'], 'Collor II': ['1991-01-31'], 'Real': ['1994-03-01', '1994-07-01']}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1], 'Real': [2477.15, 22.41]}, received {'Cruzado': [None, None], 'Bresser': [None, None], 'Verao': [None, None], 'Collor I': [None, None], 'Collor
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Verao': [14], 'Collor I': [10], 'Collor II': [37, 41], 'Real': [60]}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` scores follow the rubric: expected "0.7*drop + 0.3*durability from the row's own numbers", received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received None
- `web-plan-ranking` every plan has a source: expected 'an http(s) URL in sources for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ URLs, 3+ plans', received {'chars': 0, 'urls': 0, 'plans': []}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 70 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: saudade: missing 2 (esperança, nostalgia), extra 6 (amor, cafe, casa, esperanca, mar)
- `web-word-universe` no relation from a sidebar or a footer: 725 false pairs, such as ['acento - amor', 'acento - casa', 'acento - mar']
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'relations': 1901, 'most_connected': 'palavra', 'words': 255}
- `web-word-universe` the page has a search field: no input, contenteditable or searchbox in universe/index.html
- `web-word-universe` opening the page with ?word= shows that word's relations: no universe/index.html

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 2); read the data (call 1); removed duplicate sessions (call 3); tested significance (call 5); recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 2); used the chart of accounts (call 2); used the cash balance (call 2); recorded the result (call 8)
- `bo-reconcile`: read the notes (call 4); read the invoices (call 1); read the statement (call 1); not seen: recorded the result
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 7); not seen: recorded the result
- `cfg-source-drift`: not seen: read the readme; not seen: ran the generator
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 3); not seen: recorded the result
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 3); excluded test accounts (call 5); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 5); not seen: recorded the result
- `git-merge-conflict`: merged the branch (call 4); not seen: ran the tests; committed (call 10)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 3); read the policy (call 2); not seen: recorded the result
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); not seen: recorded the result
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 2); ran the whole suite (call 3)
- `rs-lock-bug`: read the crate (call 1); ran the tests (call 5)
- `sec-leak-fix`: read the service (call 1); read the config (call 1); ran the tests (call 3)
- `hw-stutter-tuning`: read the frame capture (call 1); read the sensor log (call 1); read the settings (call 1); read the owner notes (call 1); not seen: recorded the result
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 5); looked at it in a browser (call 9); recorded the result (call 6)
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 10); opened a source (call 6); not seen: recorded the result; not seen: wrote the dossier
- `web-word-universe`: walked the site (call 1); wrote words.json (call 11); not seen: wrote the page; not seen: looked at it in a browser; recorded the result (call 11)
