# mengine-bench 1.1.0: opencode opencode v2.2.2 / deepseek/deepseek-flash (none)

| Score | Correct % | Solved | Judge | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| **87.3** | 93.6 | 11/14 | 72.7 | 29 min 35 s | n/a | 48.51M |

- Judge: claude-opus-5-5@xhigh, rubric 2.1
- Config: provider=deepseek-api; model=DeepSeek V4.1 Flash; quant=full-weights-api; ctx=1M; thinking=off; opencode_variant={"reasoningEffort":"none"}; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T12:32:51Z; bench at a0ad088f706f; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 81 | 21.7 s | - | 7 | 7 | 2.3k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 81 | 27.0 s | - | 10 | 9 | 1.9k | 0.0k | 8 s |
| bo-reconcile | ok | 100% | 4/4 | 89 | 14.7 s | - | 5 | 5 | 1.3k | 0.0k | 4 s |
| cmp-handoff | ok | 100% | 10/10 | 81 | 14.4 s | - | 6 | 4 | 0.6k | 0.0k | 3 s |
| lc-changelog | ok | 60% | 3/5 | 38 | 4.2 s | - | 1 | 0 | - | - | - |
| vis-chart | ok | 100% | 4/4 | 72 | 2.8 s | - | 1 | 0 | - | - | - |
| ds-sql-funnel | ok | 67% | 2/3 | 50 | 25.7 s | - | 11 | 10 | 2.1k | 0.0k | 5 s |
| gd-astar-doors | ok | 100% | 1/1 | 70 | 16.1 s | - | 6 | 7 | 1.2k | 0.0k | 7 s |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 88 | 11.1 s | - | 5 | 5 | 0.4k | 0.0k | 5 s |
| ir-studio-wiki | ok | 100% | 6/6 | 91 | 14.3 s | - | 6 | 10 | 0.7k | 0.0k | 6 s |
| ir-server-logs | ok | 83% | 5/6 | 66 | 22.2 s | - | 9 | 9 | 1.5k | 0.0k | 16 s |
| gd-integration-repo | ok | 100% | 7/7 | 72 | 1 min 19 s | - | 30 | 29 | 5.4k | 0.0k | 46 s |
| web-mondrian-landing | ok | 100% | 9/9 | 82 | 3 min 14 s | - | 67 | 74 | 15.8k | 0.0k | 34 s |
| 3d-voxel-landscape | ok | 100% | 6/6 | 57 | 22 min 08 s | - | 344 | 343 | 130.0k | 0.0k | 16 s |
