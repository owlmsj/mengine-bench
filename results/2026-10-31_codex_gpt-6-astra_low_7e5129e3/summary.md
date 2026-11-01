# mengine-bench 1.3.1: codex codex-cli 0.165.0 / gpt-6-astra (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **97.0** | 100.0 | 14/14 | 89.4 | 97.5 | 5 min 37 s | n/a | 1.70M |

- Judge: claude-opus-5-5@xhigh, rubric 2.4
- Config: harness=codex; role=default; service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T22:53:29Z; bench at d3eb3b95cbd3; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 90 | 14.5 s | - | 1 | 2 | 0.9k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 88 | 15.3 s | - | 1 | 2 | 1.2k | 0.0k | - |
| bo-reconcile | ok | 100% | 4/4 | 81 | 11.4 s | - | 1 | 2 | 0.6k | 0.0k | - |
| cmp-handoff | ok | 100% | 11/11 | 95 | 18.4 s | - | 2 | 3 | 0.6k | 0.0k | - |
| lc-changelog | ok | 100% | 5/5 | 100 | 5.7 s | - | 1 | 0 | 0.1k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 100 | 8.7 s | - | 1 | 0 | 0.1k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 94 | 15.4 s | - | 1 | 3 | 1.0k | 0.0k | - |
| gd-astar-doors | ok | 100% | 1/1 | 91 | 18.8 s | - | 1 | 6 | 1.0k | 0.0k | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 98 | 18.6 s | - | 1 | 5 | 0.5k | 0.0k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 85 | 14.4 s | - | 1 | 4 | 0.5k | 0.0k | - |
| ir-server-logs | ok | 100% | 6/6 | 82 | 17.2 s | - | 1 | 4 | 0.6k | 0.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 94 | 40.0 s | - | 1 | 9 | 2.7k | 0.1k | - |
| web-mondrian-landing | ok | 100% | 9/9 | 79 | 48.3 s | - | 1 | 3 | 4.5k | 0.1k | - |
| 3d-voxel-landscape | ok | 100% | 6/6 | 75 | 1 min 30 s | - | 1 | 10 | 7.0k | 0.4k | - |
