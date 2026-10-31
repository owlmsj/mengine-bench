# mengine-bench 1.1.0: codex codex-cli 0.165.0 / gpt-6.1-sol (low)

| Score | Correct % | Solved | Judge | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| **94.8** | 100.0 | 14/14 | 82.8 | 5 min 04 s | n/a | 1.38M |

- Judge: claude-opus-5-5@xhigh, rubric 2.1
- Config: harness=codex; tier=0; role=default; service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T17:00:54Z; bench at 8101e454ae49; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 86 | 16.0 s | - | 1 | 2 | 0.9k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 83 | 15.3 s | - | 1 | 2 | 1.2k | 0.0k | - |
| bo-reconcile | ok | 100% | 4/4 | 80 | 14.0 s | - | 1 | 2 | 0.9k | 0.0k | - |
| cmp-handoff | ok | 100% | 10/10 | 84 | 21.1 s | - | 2 | 3 | 0.6k | 0.0k | - |
| lc-changelog | ok | 100% | 5/5 | 73 | 5.5 s | - | 1 | 0 | 0.1k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 73 | 4.1 s | - | 1 | 0 | 0.1k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 91 | 18.2 s | - | 1 | 3 | 1.2k | 0.0k | - |
| gd-astar-doors | ok | 100% | 1/1 | 86 | 22.6 s | - | 1 | 6 | 1.1k | 0.1k | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 91 | 13.5 s | - | 1 | 3 | 0.5k | 0.0k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 90 | 13.4 s | - | 1 | 3 | 0.5k | 0.0k | - |
| ir-server-logs | ok | 100% | 6/6 | 86 | 20.7 s | - | 1 | 6 | 0.8k | 0.0k | - |
| gd-integration-repo | ok | 100% | 7/7 | 87 | 36.6 s | - | 1 | 8 | 2.0k | 0.2k | - |
| web-mondrian-landing | ok | 100% | 9/9 | 84 | 43.4 s | - | 1 | 4 | 4.0k | 0.1k | - |
| 3d-voxel-landscape | ok | 100% | 6/6 | 65 | 59.5 s | - | 1 | 3 | 4.7k | 0.1k | - |
