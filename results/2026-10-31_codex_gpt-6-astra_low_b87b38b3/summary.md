# mengine-bench 1.1.0: codex codex-cli 0.165.0 / gpt-6-astra (low)

| Score | Correct % | Solved | Judge | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| **95.1** | 100.0 | 14/14 | 83.6 | 6 min 00 s | n/a | 1.59M |

- Judge: claude-opus-5-5@xhigh, rubric 2.1
- Config: harness=codex; tier=0; role=default; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T16:12:09Z; bench at d6da6b277d52; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 90 | 16.0 s | - | 1 | 2 | 0.9k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 85 | 18.4 s | - | 1 | 2 | 1.1k | 0.0k | - |
| bo-reconcile | ok | 100% | 4/4 | 80 | 18.5 s | - | 1 | 3 | 1.4k | 0.0k | - |
| cmp-handoff | ok | 100% | 10/10 | 86 | 20.6 s | - | 2 | 3 | 0.6k | 0.0k | - |
| lc-changelog | ok | 100% | 5/5 | 77 | 4.9 s | - | 1 | 0 | 0.1k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 74 | 7.7 s | - | 1 | 0 | 0.1k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 93 | 18.9 s | - | 1 | 4 | 1.2k | 0.0k | - |
| gd-astar-doors | ok | 100% | 1/1 | 81 | 24.5 s | - | 1 | 6 | 1.1k | 0.0k | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 91 | 15.7 s | - | 1 | 5 | 0.6k | 0.0k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 88 | 17.1 s | - | 1 | 3 | 0.4k | 0.0k | - |
| ir-server-logs | ok | 100% | 6/6 | 85 | 17.6 s | - | 1 | 5 | 0.8k | 0.0k | - |
| gd-integration-repo | ok | 100% | 7/7 | 84 | 41.7 s | - | 1 | 11 | 3.0k | 0.2k | - |
| web-mondrian-landing | ok | 100% | 9/9 | 82 | 41.1 s | - | 1 | 2 | 3.4k | 0.0k | - |
| 3d-voxel-landscape | ok | 100% | 6/6 | 74 | 1 min 37 s | - | 1 | 7 | 8.1k | 0.4k | - |
