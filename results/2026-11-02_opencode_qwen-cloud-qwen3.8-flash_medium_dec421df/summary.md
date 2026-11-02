# mengine-bench 1.7.2: opencode opencode v2.2.2 / qwen-cloud/qwen3.8-flash (medium)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **68.9** | 80.0 | 12/15 | 68.0 | 32.2 | 21 min 58 s | >= $0.00 (harness) | 1.97M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=opencode; tier=1; role=default; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T02:38:17Z; bench at 79c180a57574; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 77 | 1 min 18 s | 0.0000 | 11 | 11 | 3.2k | 1.4k | 24 s |
| bo-pnl-runway | ok | 0% | 0/5 | 12 | 1 min 02 s | 0.0000 | 6 | 7 | 3.0k | 0.9k | 24 s |
| bo-reconcile | ok | 100% | 4/4 | 85 | 50.3 s | 0.0000 | 7 | 8 | 2.7k | 1.8k | 33 s |
| cmp-handoff | ok | 100% | 11/11 | 82 | 2 min 43 s | 0.0000 | 17 | 16 | 8.6k | 5.8k | 21 s |
| lc-changelog | ok | 100% | 5/5 | 96 | 23.8 s | 0.0000 | 2 | 1 | 0.7k | 0.5k | 10 s |
| vis-chart | ok | 100% | 4/4 | 92 | 53.8 s | 0.0000 | 5 | 4 | 2.8k | 1.7k | 44 s |
| ds-sql-funnel | ok | 100% | 3/3 | 88 | 50.3 s | 0.0000 | 7 | 7 | 1.7k | 0.6k | 7 s |
| ue-packaged-bug | ok | 100% | 5/5 | 85 | 56.2 s | 0.0000 | 6 | 12 | 2.7k | 0.8k | 33 s |
| ir-studio-wiki | ok | 100% | 6/6 | 96 | 38.2 s | 0.0000 | 6 | 10 | 1.1k | 0.5k | 21 s |
| ir-server-logs | ok | 100% | 6/6 | 79 | 1 min 07 s | 0.0000 | 9 | 10 | 2.8k | 1.6k | 49 s |
| gd-integration-repo | ok | 100% | 8/8 | 81 | 3 min 32 s | 0.0000 | 18 | 19 | 10.9k | 7.7k | 58 s |
| rs-lock-bug | ok | 100% | 6/6 | 79 | 2 min 57 s | 0.0000 | 9 | 10 | 4.4k | 2.2k | 36 s |
| web-mondrian-landing | ok | 0% | 0/8 | 2 | 37.1 s | 0.0000 | 3 | 3 | 1.7k | 0.3k | - |
| 3d-voxel-landscape | ok | 100% | 7/7 | 64 | 3 min 50 s | 0.0000 | 17 | 16 | 14.4k | 6.0k | 119 s |
| web-word-universe | ok | 0% | 0/6 | 2 | 19.5 s | 0.0000 | 2 | 1 | 0.1k | 0.0k | - |

## Failed checks

- `bo-pnl-runway` revenue per month: 2026-01: expected 200510.87, received None
- `bo-pnl-runway` gross_margin_pct per month: 2026-01: expected 70.0305923564144, received None
- `bo-pnl-runway` ebitda per month: 2026-01: expected -210278.96, received None
- `bo-pnl-runway` 3-month average burn: expected 197288.23, received None
- `bo-pnl-runway` runway in months: expected 9.363713182484327, received None
- `web-mondrian-landing` index.html exists with content
- `web-mondrian-landing` has a page title and an h1
- `web-mondrian-landing` names the painting (Composition with Red, Blue and Yellow)
- `web-mondrian-landing` names the painter (Piet Mondrian)
- `web-mondrian-landing` states the year 1930
- `web-mondrian-landing` names the De Stijl movement
- `web-mondrian-landing` links to the fact sheet's source
- `web-mondrian-landing` CSS with the Mondrian palette (red, blue, yellow, black)
- `web-word-universe` collected exactly the site's words: missing 250 (acento, advogado, afeto, aflição, aldeia), extra 0 (none)
- `web-word-universe` relations of a sample of words: saudade: missing 5 (ansiedade, carinho, dor, esperança, nostalgia), extra 0 (none)
- `web-word-universe` no relation from a sidebar or a footer: no words.json
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {}
- `web-word-universe` the page has a search field: no input, contenteditable or searchbox in universe/index.html
- `web-word-universe` opening the page with ?word= shows that word's relations: no universe/index.html

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 1); read the data (call 1); removed duplicate sessions (call 2); tested significance (call 5); recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 8)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 14)
- `lc-changelog`: recorded the result (call 1)
- `vis-chart`: recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 4); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); recorded the result (call 11)
- `ir-studio-wiki`: followed the bug (call 1); checked the approvals (call 1); read the postmortem (call 1); recorded the result (call 10)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 10)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 3); ran the whole suite (call 5)
- `rs-lock-bug`: read the crate (call 1); ran the tests (call 5)
- `web-mondrian-landing`: read the fact sheet (call 1); not seen: wrote the page; not seen: looked at it in a browser
- `3d-voxel-landscape`: wrote the scene (call 1); looked at it in a browser (call 2)
- `web-word-universe`: walked the site (call 1); not seen: wrote words.json; not seen: wrote the page; not seen: looked at it in a browser; not seen: recorded the result
