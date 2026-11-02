# mengine-bench 1.7.2: opencode opencode v2.2.2 / alibaba/qwen3.8-flash (medium)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **73.7** | 90.8 | 13/15 | 72.7 | 7.5 | 28 min 07 s | >= $0.08 (harness) | 1.04M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=opencode default clean install; personal_instructions=none
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T03:05:22Z; bench at 79c180a57574; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 77 | 42.1 s | 0.0133 | 8 | 7 | 1.0k | 0.3k | 19 s |
| bo-pnl-runway | ok | 100% | 5/5 | 78 | 1 min 41 s | 0.0059 | 9 | 8 | 4.2k | 1.1k | 47 s |
| bo-reconcile | ok | 100% | 4/4 | 81 | 1 min 02 s | 0.0039 | 7 | 8 | 2.1k | 1.1k | 21 s |
| cmp-handoff | ok | 100% | 11/11 | 78 | 2 min 11 s | 0.0096 | 18 | 17 | 5.4k | 2.8k | 32 s |
| lc-changelog | ok | 100% | 5/5 | 99 | 40.7 s | 0.0082 | 2 | 1 | 1.6k | 1.4k | 24 s |
| vis-chart | ok | 100% | 4/4 | 93 | 14.8 s | 0.0018 | 3 | 2 | 0.3k | 0.1k | 5 s |
| ds-sql-funnel | ok | 100% | 3/3 | 78 | 55.0 s | 0.0028 | 6 | 6 | 1.5k | 0.4k | 10 s |
| ue-packaged-bug | ok | 100% | 5/5 | 76 | 56.9 s | 0.0028 | 4 | 10 | 1.6k | 0.8k | 41 s |
| ir-studio-wiki | ok | 100% | 6/6 | 93 | 35.4 s | 0.0029 | 6 | 10 | 0.9k | 0.4k | 22 s |
| ir-server-logs | ok | 100% | 6/6 | 86 | 1 min 32 s | 0.0113 | 8 | 9 | 4.1k | 1.9k | 73 s |
| gd-integration-repo | ok | 100% | 8/8 | 80 | 1 min 49 s | 0.0066 | 13 | 23 | 3.5k | 1.9k | 69 s |
| rs-lock-bug | ok | 100% | 6/6 | 86 | 1 min 09 s | 0.0035 | 6 | 6 | 2.2k | 1.0k | 44 s |
| web-mondrian-landing | ok | 100% | 10/10 | 50 | 1 min 38 s | 0.0051 | 4 | 3 | 5.5k | 0.3k | 73 s |
| 3d-voxel-landscape | timeout (timeout) | 0% | 1/5 | 0 | 7 min 00 s | - | 1 | 0 | - | - | - |
| web-word-universe | timeout (timeout) | 62% | 5/8 | 35 | 6 min 00 s | - | 21 | 30 | 18.5k | 7.0k | 54 s |

## Failed checks

- `3d-voxel-landscape` index.html exists with content
- `3d-voxel-landscape` imports three.js 0.170.0 from the CDN
- `3d-voxel-landscape` creates a WebGLRenderer
- `3d-voxel-landscape` animation loop
- `web-word-universe` collected exactly the site's words: missing 52 (aflição, almoço, amanhã, angústia, açougueiro), extra 55 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: saudade: missing 1 (esperança), extra 1 (esperanca)
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 757, 'most_connected': ['tempo', 'palavra']}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 2); read the data (call 2); removed duplicate sessions (call 3); tested significance (call 5); recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 5)
- `bo-reconcile`: read the notes (call 4); read the invoices (call 1); read the statement (call 1); recorded the result (call 6)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 4); recorded the result (call 17)
- `lc-changelog`: recorded the result (call 1)
- `vis-chart`: recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 4); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); recorded the result (call 10)
- `ir-studio-wiki`: followed the bug (call 1); checked the approvals (call 1); read the postmortem (call 1); recorded the result (call 10)
- `ir-server-logs`: read the notes (call 1); read the logs (call 1); recorded the result (call 8)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 2); ran the whole suite (call 3)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 6)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); not seen: looked at it in a browser
- `3d-voxel-landscape`: not seen: wrote the scene; not seen: looked at it in a browser
- `web-word-universe`: walked the site (call 1); wrote words.json (call 7); wrote the page (call 24); looked at it in a browser (call 26); recorded the result (call 7)
