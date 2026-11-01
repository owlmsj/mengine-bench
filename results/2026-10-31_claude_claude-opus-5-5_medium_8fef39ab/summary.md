# mengine-bench 1.3.4: claude 2.1.316 (Claude Code) / claude-opus-5-5 (medium)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **92.3** | 100.0 | 14/14 | 92.6 | 61.0 | 14 min 45 s | $5.85 (harness) | 2.98M |

- Judge: claude-opus-5-5@xhigh, rubric 2.4
- Config: harness=claude-code; tier=0; role=default; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-11-01T02:10:00Z; bench at 20e01db73fef; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 88 | 20.5 s | 0.2262 | 4 | 3 | 2.2k | 0.4k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 90 | 34.1 s | 0.3133 | 5 | 6 | 3.9k | 1.0k | - |
| bo-reconcile | ok | 100% | 4/4 | 88 | 14.9 s | 0.2145 | 3 | 3 | 1.6k | 0.2k | - |
| cmp-handoff | ok | 100% | 11/11 | 88 | 27.2 s | 0.4171 | 7 | 7 | 2.6k | 0.8k | - |
| lc-changelog | ok | 100% | 5/5 | 100 | 2.5 s | 0.4325 | 1 | 0 | 0.1k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 100 | 3.2 s | 0.1517 | 2 | 1 | 0.1k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 94 | 19.5 s | 0.2276 | 4 | 3 | 2.2k | 0.2k | - |
| gd-astar-doors | ok | 100% | 1/1 | 91 | 24.6 s | 0.2426 | 4 | 6 | 2.9k | 0.8k | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 100 | 11.5 s | 0.1958 | 4 | 3 | 0.9k | 0.0k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 95 | 14.4 s | 0.2453 | 4 | 5 | 1.5k | 0.1k | - |
| ir-server-logs | ok | 100% | 6/6 | 94 | 23.5 s | 0.2534 | 4 | 5 | 2.4k | 0.4k | - |
| gd-integration-repo | ok | 100% | 8/8 | 95 | 56.5 s | 0.4026 | 6 | 5 | 6.3k | 1.7k | - |
| web-mondrian-landing | ok | 100% | 9/9 | 90 | 3 min 30 s | 0.8853 | 9 | 14 | 22.1k | 7.8k | - |
| 3d-voxel-landscape | ok | 100% | 6/6 | 83 | 7 min 03 s | 1.6373 | 10 | 16 | 44.9k | 19.2k | - |
