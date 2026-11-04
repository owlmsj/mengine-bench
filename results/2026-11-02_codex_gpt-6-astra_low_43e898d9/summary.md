# mengine-bench 2.1.0: codex codex-cli 0.165.0 / gpt-6-astra (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **57.7** | 81.0 | 14/20 | 68.8 | 0.0 | 33 min 08 s | n/a | 2.00M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=codex default clean install; service_tier=fast; personal_instructions=none
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-03T02:21:49Z; bench at 5e5aa6e24c77; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 88 | 1 min 06 s | - | 1 | 5 | - | 1.9k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 5/5 | 86 | 1 min 58 s | - | 1 | 4 | - | 2.9k | 0.1k | - |
| bo-reconcile | ok | 100% | 4/4 | 85 | 28.1 s | - | 1 | 3 | - | 0.8k | 0.0k | - |
| cmp-handoff | ok | 100% | 11/11 | 91 | 48.3 s | - | 2 | 8 | - | 1.1k | 0.0k | - |
| cfg-source-drift | ok | 100% | 3/3 | 100 | 29.1 s | - | 1 | 3 | - | 0.6k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 6/6 | 75 | 38.9 s | - | 1 | 4 | - | 1.2k | 0.0k | - |
| ds-sql-funnel | timeout (timeout) | 0% | 0/3 | 0 | 1 min 30 s | - | 0 | 0 | - | - | - | - |
| ue-packaged-bug | timeout (timeout) | 20% | 1/5 | 10 | 1 min 30 s | - | 0 | 2 | - | - | - | - |
| git-merge-conflict | ok | 100% | 6/6 | 93 | 39.5 s | - | 1 | 5 | - | 1.3k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 6/6 | 81 | 28.4 s | - | 1 | 2 | - | 1.0k | 0.0k | - |
| ir-server-logs | ok | 100% | 6/6 | 88 | 30.9 s | - | 1 | 4 | - | 0.8k | 0.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 93 | 55.8 s | - | 1 | 8 | - | 2.0k | 0.1k | - |
| rs-lock-bug | ok | 100% | 6/6 | 87 | 58.7 s | - | 1 | 4 | - | 1.9k | 0.1k | - |
| sec-leak-fix | timeout (timeout) | 100% | 8/8 | 81 | 1 min 30 s | - | 0 | 3 | - | - | - | - |
| hw-stutter-tuning | timeout (timeout) | 0% | 0/6 | 0 | 1 min 30 s | - | 0 | 0 | - | - | - | - |
| ts-plugin-bug | timeout (timeout) | 0% | 2/7 | 0 | 1 min 00 s | - | 0 | 0 | - | - | - | - |
| web-mondrian-landing | timeout (timeout) | 100% | 10/10 | 83 | 5 min 00 s | - | 0 | 7 | - | - | - | - |
| 3d-print-homage | ok | 100% | 11/11 | 82 | 4 min 30 s | - | 1 | 11 | - | 7.2k | 0.7k | - |
| web-plan-ranking | ok | 100% | 8/8 | 69 | 2 min 36 s | - | 1 | 7 | - | 4.4k | 0.1k | - |
| web-word-universe | ok | 100% | 8/8 | 83 | 5 min 01 s | - | 1 | 12 | - | 9.4k | 0.3k | - |

## Failed checks

- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {}
- `ue-packaged-bug` crash fixed: the score tracker survives garbage collection: ScoreTracker is not kept alive by UPROPERTY, TStrongObjectPtr, AddToRoot or a reported reference
- `ue-packaged-bug` colors fixed: the palette reaches the cook: /Game/Data/Palettes/DA_Primary is not always cooked from the packaging settings, the asset manager or a hard reference
- `ue-packaged-bug` the report names the crash cause: crash_cause: ''
- `ue-packaged-bug` the report names the color cause: no_colors_cause: ''
- `hw-stutter-tuning` average FPS: expected 137.3, received None
- `hw-stutter-tuning` 1% low FPS: expected 45.4, received None
- `hw-stutter-tuning` cause named: expected "the GPU link's power-saving state (ASPM L1 on its root port)", received None
- `hw-stutter-tuning` ASPM off on the GPU root port: expected 'pcie_aspm_rp1_gpu -> disabled', received []
- `hw-stutter-tuning` GPU link speed kept: expected 'changes that leave the link speed alone', received []
- `hw-stutter-tuning` BIOS overclock kept: expected 'no XMP, PBO or core ratio change', received []
- `ts-plugin-bug` hidden handlers run in subscription order: expected "'a start' 'a end' 'b start' 'b end' 'c'", received "'a start' 'b start' 'c' 'b end' 'a end'"
- `ts-plugin-bug` hidden emit resolves after every handler: emit resolves after every handler: emit resolved with 0 of 2 handlers finished
- `ts-plugin-bug` hidden a failing handler rejects emit: a failing handler rejects emit: 'expected emit to reject with the handler error, got undefined'
- `ts-plugin-bug` hidden a handler that unsubscribes itself does not stop the others: expected "'once' 'b' 'c' 'b' 'c'", received "'once' 'c' 'b' 'c'"
- `ts-plugin-bug` hidden the audit plugin redacts before it logs: expected "'notice: tool output is audited' 'bash: login password=[redacted] ok' 'read: password=[redacted]'", received "'notice: tool output is audited' 'bash: login password=hunter2 ok' 'read: password=swordfish'"

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 2); read the data (call 1); removed duplicate sessions (call 2); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 3)
- `bo-reconcile`: read the notes (call 1); read the invoices (call 1); read the statement (call 1); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 7)
- `cfg-source-drift`: read the readme (call 1); ran the generator (call 1)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 3)
- `ds-sql-funnel`: not seen: read the rules; not seen: looked at the schema; not seen: excluded test accounts; not seen: recorded the result
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); not seen: recorded the result
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 2); committed (call 5)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 1); ran the whole suite (call 2)
- `rs-lock-bug`: read the crate (call 1); ran the tests (call 3)
- `sec-leak-fix`: read the service (call 1); read the config (call 1); ran the tests (call 2)
- `hw-stutter-tuning`: not seen: read the frame capture; not seen: read the sensor log; not seen: read the settings; not seen: read the owner notes; not seen: recorded the result
- `ts-plugin-bug`: not seen: read the bus; not seen: ran the tests
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 4); looked at it in a browser (call 2)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 5); recorded the result (call 4)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: opened a source; recorded the result (call 2); wrote the dossier (call 2)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 5); wrote the page (call 7); looked at it in a browser (call 4); recorded the result (call 5)
