# mengine-bench 2.0.0: opencode opencode v2.2.5 / zai/glm-5.3-flash (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **72.1** | 94.7 | 17/20 | 72.3 | 18.9 | 25 min 17 s | >= $0.09 (harness) | 1.53M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=opencode; tier=1; role=default; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T19:59:01Z; bench at fa60fc805d87; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 83 | 50.9 s | 0.0129 | 7 | 7 | 1.6k | 0.1k | 24 s |
| bo-pnl-runway | ok | 40% | 2/5 | 41 | 54.5 s | 0.0029 | 6 | 5 | 1.8k | 0.1k | 34 s |
| bo-reconcile | ok | 100% | 4/4 | 78 | 53.9 s | 0.0029 | 6 | 7 | 1.7k | 0.5k | 34 s |
| cmp-handoff | ok | 100% | 11/11 | 86 | 1 min 01 s | 0.0036 | 9 | 7 | 1.5k | 0.1k | 20 s |
| cfg-source-drift | ok | 100% | 3/3 | 87 | 32.6 s | 0.0018 | 6 | 7 | 0.5k | 0.0k | 10 s |
| doc-lab-pdf | ok | 100% | 6/6 | 67 | 39.0 s | 0.0022 | 4 | 4 | 1.2k | 0.2k | 18 s |
| ds-sql-funnel | ok | 100% | 3/3 | 74 | 52.2 s | 0.0025 | 8 | 8 | 1.2k | 0.2k | 27 s |
| ue-packaged-bug | ok | 100% | 5/5 | 75 | 54.4 s | 0.0029 | 6 | 9 | 1.8k | 0.6k | 32 s |
| git-merge-conflict | ok | 100% | 6/6 | 92 | 1 min 00 s | 0.0029 | 9 | 9 | 1.2k | 0.2k | 31 s |
| infra-gpu-fit | ok | 100% | 6/6 | 69 | 24.5 s | 0.0012 | 3 | 4 | 0.8k | 0.2k | 10 s |
| ir-server-logs | ok | 100% | 6/6 | 71 | 33.7 s | 0.0018 | 5 | 5 | 0.8k | 0.2k | 17 s |
| gd-integration-repo | ok | 100% | 8/8 | 90 | 53.0 s | 0.0046 | 8 | 17 | 1.2k | 0.3k | 32 s |
| rs-lock-bug | ok | 100% | 6/6 | 79 | 1 min 37 s | 0.0054 | 13 | 13 | 2.9k | 0.6k | 22 s |
| sec-leak-fix | ok | 100% | 8/8 | 86 | 33.6 s | 0.0027 | 5 | 6 | 1.1k | 0.2k | 17 s |
| hw-stutter-tuning | ok | 67% | 4/6 | 33 | 48.5 s | 0.0033 | 7 | 8 | 1.3k | 0.2k | 37 s |
| ts-plugin-bug | ok | 100% | 7/7 | 100 | 41.9 s | 0.0026 | 7 | 9 | 1.2k | 0.1k | 6 s |
| web-mondrian-landing | ok | 100% | 10/10 | 75 | 1 min 31 s | 0.0073 | 12 | 11 | 3.5k | 0.2k | 33 s |
| 3d-print-homage | ok | 100% | 11/11 | 59 | 2 min 45 s | 0.0100 | 10 | 12 | 6.8k | 0.7k | 54 s |
| web-plan-ranking | ok | 100% | 8/8 | 56 | 1 min 49 s | 0.0134 | 9 | 9 | 5.8k | 2.5k | 95 s |
| web-word-universe | timeout (timeout) | 88% | 7/8 | 46 | 6 min 00 s | - | 46 | 45 | 13.6k | 2.7k | 23 s |

## Failed checks

- `bo-pnl-runway` ebitda per month: 2026-01: expected -210278.96, received -203812.19
- `bo-pnl-runway` 3-month average burn: expected 197288.23, received 190820.54
- `bo-pnl-runway` runway in months: expected 9.363713182484327, received 9.68
- `hw-stutter-tuning` cause named: expected "the GPU link's power-saving state (ASPM L1 on its root port)", received 'Defender real-time scanning (MsMpEng.exe) bursts on the game files every few seconds. Sensor seconds 43-45 show the top process switch to MsMpEng.exe with disk_active_pct 94/83/80 and DPC latency spiking to 420-455 us
- `hw-stutter-tuning` ASPM off on the GPU root port: expected 'pcie_aspm_rp1_gpu -> disabled', received [('defender_exclusions', 'add Arena.exe and the game install folder (real-time protection stays on; no BIOS/power changes)')]
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 2); read the data (call 1); removed duplicate sessions (call 2); tested significance (call 4); recorded the result (call 7)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 5)
- `bo-reconcile`: read the notes (call 1); read the invoices (call 1); read the statement (call 1); recorded the result (call 7)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 4); recorded the result (call 7)
- `cfg-source-drift`: read the readme (call 1); ran the generator (call 1)
- `doc-lab-pdf`: opened the exams (call 1); not seen: extracted the text; recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 3); recorded the result (call 7)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 6); ran the tests (call 5); committed (call 9)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 2); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 1); read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 1); ran the whole suite (call 2)
- `rs-lock-bug`: read the crate (call 1); ran the tests (call 6)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 1)
- `hw-stutter-tuning`: read the frame capture (call 1); read the sensor log (call 1); read the settings (call 1); read the owner notes (call 1); recorded the result (call 8)
- `ts-plugin-bug`: read the bus (call 1); ran the tests (call 1)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 5); opened a source (call 2); recorded the result (call 8); wrote the dossier (call 9)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 9); wrote the page (call 11); looked at it in a browser (call 16); recorded the result (call 9)
