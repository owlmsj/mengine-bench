# mengine-bench 1.5.0: claude 2.1.316 (Claude Code) / claude-opus-5-5 (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **94.9** | 100.0 | 14/14 | 91.9 | 79.5 | 10 min 08 s | $4.94 (harness) | 2.40M |

- Judge: claude-opus-5-5@xhigh, rubric 2.4
- Config: harness=claude-code; tier=0; role=default; fast_mode=off; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-01, started 2026-11-01T15:05:23Z; bench at 71c53d6a44bf; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 84 | 20.6 s | 0.2312 | 4 | 6 | 2.3k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 85 | 21.6 s | 0.2542 | 4 | 3 | 2.3k | 0.3k | - |
| bo-reconcile | ok | 100% | 4/4 | 90 | 16.0 s | 0.2236 | 3 | 6 | 1.9k | 0.2k | - |
| cmp-handoff | ok | 100% | 11/11 | 91 | 20.2 s | 0.3908 | 6 | 6 | 1.9k | 0.3k | - |
| lc-changelog | ok | 100% | 5/5 | 100 | 2.6 s | 0.4327 | 1 | 0 | 0.1k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 100 | 3.3 s | 0.1520 | 2 | 1 | 0.1k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 82 | 14.7 s | 0.1987 | 3 | 2 | 1.5k | 0.1k | - |
| gd-astar-doors | ok | 100% | 5/5 | 96 | 23.5 s | 0.2498 | 5 | 8 | 2.7k | 0.4k | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 100 | 13.5 s | 0.2233 | 5 | 10 | 1.4k | 0.0k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 95 | 18.4 s | 0.2461 | 4 | 12 | 2.3k | 0.1k | - |
| ir-server-logs | ok | 100% | 6/6 | 94 | 21.6 s | 0.2352 | 4 | 3 | 2.0k | 0.3k | - |
| gd-integration-repo | ok | 100% | 8/8 | 96 | 36.9 s | 0.3355 | 5 | 4 | 4.1k | 0.8k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 89 | 1 min 47 s | 0.6164 | 6 | 22 | 11.6k | 1.9k | - |
| 3d-voxel-landscape | ok | 100% | 8/8 | 84 | 4 min 48 s | 1.1537 | 7 | 15 | 31.2k | 10.7k | - |
