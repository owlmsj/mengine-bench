# mengine-bench 1.3.3: opencode opencode v2.2.2 / deepseek/deepseek-flash (max)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **87.3** | 98.6 | 11/14 | 87.3 | 42.9 | 19 min 17 s | n/a | 1.55M |

- Judge: claude-opus-5-5@xhigh, rubric 2.4
- Config: provider=deepseek-api; model=DeepSeek V4.1 Flash; quant=full-weights-api; ctx=1M; tier=1; role=default; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-11-01T00:38:11Z; bench at 2b320be6413e; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 89 | 18.8 s | - | 7 | 8 | 1.9k | 0.3k | 6 s |
| bo-pnl-runway | ok | 100% | 11/11 | 90 | 23.9 s | - | 6 | 7 | 3.1k | 0.8k | - |
| bo-reconcile | ok | 100% | 4/4 | 93 | 25.8 s | - | 8 | 10 | 3.0k | 1.6k | 10 s |
| cmp-handoff | ok | 100% | 11/11 | 80 | 25.8 s | - | 8 | 6 | 1.3k | 0.6k | 6 s |
| lc-changelog | ok | 80% | 4/5 | 90 | 4.6 s | - | 1 | 0 | - | - | - |
| vis-chart | ok | 100% | 4/4 | 88 | 44.7 s | - | 12 | 12 | 4.7k | 2.1k | 8 s |
| ds-sql-funnel | ok | 100% | 3/3 | 85 | 37.9 s | - | 13 | 12 | 4.5k | 1.6k | 3 s |
| gd-astar-doors | ok | 100% | 1/1 | 73 | 55.1 s | - | 11 | 13 | 8.8k | 2.4k | 11 s |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 95 | 15.3 s | - | 7 | 11 | 1.0k | 0.1k | 9 s |
| ir-studio-wiki | ok | 100% | 6/6 | 97 | 12.9 s | - | 7 | 12 | 0.9k | 0.3k | 7 s |
| ir-server-logs | ok | 100% | 6/6 | 88 | 18.9 s | - | 6 | 8 | 1.8k | 1.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 97 | 1 min 33 s | - | 15 | 29 | 12.1k | 7.7k | 37 s |
| web-mondrian-landing | timeout (timeout) | 100% | 9/9 | 82 | 5 min 00 s | - | 24 | 24 | 50.2k | 38.6k | 198 s |
| 3d-voxel-landscape | timeout (timeout) | 100% | 6/6 | 75 | 8 min 00 s | - | 24 | 38 | 80.4k | 58.0k | 286 s |
