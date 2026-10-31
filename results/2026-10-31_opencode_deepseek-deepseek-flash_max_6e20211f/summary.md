# mengine-bench 1.0.0: opencode opencode v2.2.2 / deepseek/deepseek-flash (max)

| Score | Correct % | Solved | Judge | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| **84.4** | 85.7 | 12/14 | 81.4 | 38 min 18 s | n/a | 2.66M |

- Judge: claude-opus-5-5@xhigh, rubric 2.0
- Config: provider=deepseek-api; model=DeepSeek V4.1 Flash; quant=full-weights-api; ctx=1M; tier=1; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T09:59:59Z; bench at 8e57786022eb; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) |
| --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 90 | 35.5 s | - |
| bo-pnl-runway | ok | 100% | 11/11 | 89 | 44.0 s | - |
| bo-reconcile | ok | 100% | 4/4 | 87 | 31.9 s | - |
| cmp-handoff | ok | 100% | 10/10 | 85 | 29.4 s | - |
| lc-changelog | ok | 100% | 5/5 | 70 | 4.5 s | - |
| vis-chart | ok | 100% | 4/4 | 70 | 4.6 s | - |
| ds-sql-funnel | ok | 100% | 3/3 | 71 | 1 min 06 s | - |
| gd-astar-doors | ok | 100% | 1/1 | 76 | 56.9 s | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 81 | 16.0 s | - |
| ir-studio-wiki | ok | 100% | 6/6 | 91 | 24.7 s | - |
| ir-server-logs | ok | 100% | 6/6 | 94 | 32.3 s | - |
| gd-integration-repo | ok | 100% | 7/7 | 87 | 2 min 33 s | - |
| web-mondrian-landing | timeout (timeout) | 0% | 9/9 | 77 | 15 min 00 s | - |
| 3d-voxel-landscape | timeout (timeout) | 0% | 6/6 | 72 | 15 min 00 s | - |
