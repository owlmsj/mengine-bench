# mengine-bench 1.3.4: opencode opencode v2.2.2 / zai/glm-5.3-flash (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **87.4** | 93.8 | 12/14 | 81.4 | 76.6 | 10 min 50 s | n/a | 0.73M |

- Judge: claude-opus-5-5@xhigh, rubric 2.4
- Config: provider=zai-api; model=GLM 5.3 Flash; quant=full-weights-api; ctx=1M; tier=1; role=default; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-11-01T02:38:23Z; bench at 20e01db73fef; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 86 | 28.9 s | - | 4 | 4 | 0.4k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 77 | 50.6 s | - | 6 | 7 | 1.4k | 0.1k | 27 s |
| bo-reconcile | ok | 100% | 4/4 | 59 | 23.4 s | - | 3 | 3 | 0.5k | 0.3k | 13 s |
| cmp-handoff | ok | 100% | 11/11 | 85 | 38.1 s | - | 6 | 4 | 0.4k | 0.0k | 10 s |
| lc-changelog | ok | 80% | 4/5 | 86 | 8.5 s | - | 1 | 0 | - | - | - |
| vis-chart | ok | 100% | 4/4 | 100 | 7.8 s | - | 1 | 0 | - | - | - |
| ds-sql-funnel | ok | 33% | 1/3 | 57 | 32.4 s | - | 5 | 4 | 0.9k | 0.0k | 21 s |
| gd-astar-doors | ok | 100% | 1/1 | 91 | 27.5 s | - | 4 | 3 | 0.6k | 0.0k | 11 s |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 98 | 46.6 s | - | 9 | 10 | 0.5k | 0.0k | 29 s |
| ir-studio-wiki | ok | 100% | 6/6 | 86 | 27.1 s | - | 5 | 7 | 0.2k | 0.0k | 16 s |
| ir-server-logs | ok | 100% | 6/6 | 67 | 41.1 s | - | 7 | 7 | 0.4k | 0.2k | 27 s |
| gd-integration-repo | ok | 100% | 8/8 | 95 | 1 min 18 s | - | 10 | 11 | 1.7k | 1.0k | 57 s |
| web-mondrian-landing | ok | 100% | 9/9 | 81 | 1 min 13 s | - | 3 | 2 | 3.7k | 0.0k | 59 s |
| 3d-voxel-landscape | ok | 100% | 6/6 | 72 | 2 min 47 s | - | 8 | 13 | 6.4k | 1.1k | 57 s |
