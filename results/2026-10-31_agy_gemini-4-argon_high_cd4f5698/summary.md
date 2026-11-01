# mengine-bench 1.3.4: agy 1.4.12 / gemini-4-argon (high)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **83.3** | 100.0 | 13/14 | 88.6 | 7.5 | 28 min 08 s | n/a | 1.75M |

- Judge: claude-opus-5-5@xhigh, rubric 2.4
- Config: provider=agy-subscription; model=Gemini 4 Argon; tier=none; role=default; personal_instructions=~/.gemini/GEMINI.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-11-01T01:06:19Z; bench at e860bb520526; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 95 | 42.1 s | - | 4 | 4 | 2.4k | 0.4k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 86 | 1 min 04 s | - | 5 | 8 | 4.2k | 1.3k | - |
| bo-reconcile | ok | 100% | 4/4 | 75 | 1 min 09 s | - | 4 | 4 | 6.5k | 4.8k | - |
| cmp-handoff | ok | 100% | 11/11 | 95 | 1 min 38 s | - | 6 | 4 | 5.0k | 3.6k | - |
| lc-changelog | ok | 100% | 5/5 | 100 | 20.1 s | - | 1 | 0 | 1.6k | 1.5k | - |
| vis-chart | ok | 100% | 4/4 | 100 | 20.2 s | - | 2 | 1 | 1.2k | 1.1k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 87 | 1 min 54 s | - | 7 | 6 | 7.5k | 5.4k | - |
| gd-astar-doors | ok | 100% | 1/1 | 88 | 1 min 39 s | - | 8 | 8 | 5.5k | 3.1k | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 100 | 52.8 s | - | 6 | 11 | 2.2k | 1.1k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 95 | 1 min 02 s | - | 6 | 13 | 3.5k | 1.2k | - |
| ir-server-logs | ok | 100% | 6/6 | 78 | 1 min 18 s | - | 8 | 8 | 3.8k | 1.8k | - |
| gd-integration-repo | ok | 100% | 8/8 | 91 | 4 min 15 s | - | 20 | 34 | 15.1k | 9.8k | - |
| web-mondrian-landing | ok | 100% | 9/9 | 73 | 3 min 53 s | - | 9 | 8 | 21.3k | 3.9k | - |
| 3d-voxel-landscape | timeout (timeout) | 100% | 6/6 | 78 | 8 min 00 s | - | 7 | 7 | 39.3k | 3.4k | - |
