# mengine-bench 1.0.0: opencode opencode v2.2.2 / ds41/deepseek41-1017-exl3-225 (default effort)

| Score | Correct % | Solved | Judge | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| **72.3** | 72.7 | 10/14 | 71.3 | 53 min 11 s | >= $0.00 (price) | 1.60M |

- Judge: claude-opus-5-5@xhigh, rubric 2.0
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4-3600; model=DeepSeek-V4.1-Flash-1017; server=home; runtime=exllamav3 dev a0932069 + TabbyAPI b1c22539; quant=turboderp-2.25bpw; ctx=256k; drafter=DSpark n5 dynamic; disk=engram on Linux SSD, weights on USB ntfs3; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-30, started 2026-10-31T00:40:56Z; bench at 10413e1bb932 (dirty tree); submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) |
| --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 86 | 2 min 22 s | 0.0000 |
| bo-pnl-runway | ok | 18% | 2/11 | 57 | 1 min 49 s | 0.0000 |
| bo-reconcile | ok | 100% | 4/4 | 82 | 1 min 15 s | 0.0000 |
| cmp-handoff | ok | 100% | 10/10 | 81 | 1 min 29 s | 0.0000 |
| lc-changelog | ok | 100% | 5/5 | 66 | 1 min 23 s | 0.0000 |
| vis-chart | ok | 100% | 4/4 | 72 | 33.3 s | 0.0000 |
| ds-sql-funnel | ok | 100% | 3/3 | 84 | 2 min 46 s | 0.0000 |
| gd-astar-doors | ok | 100% | 1/1 | 83 | 1 min 50 s | 0.0000 |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 89 | 1 min 14 s | 0.0000 |
| ir-studio-wiki | ok | 100% | 6/6 | 90 | 1 min 04 s | 0.0000 |
| ir-server-logs | ok | 0% | 0/6 | 42 | 2 min 31 s | 0.0000 |
| gd-integration-repo | ok | 100% | 7/7 | 88 | 4 min 54 s | 0.0000 |
| web-mondrian-landing | timeout (timeout) | 0% | 9/9 | 78 | 15 min 00 s | 0.0000 |
| 3d-voxel-landscape | timeout (timeout) | 0% | 1/6 | 0 | 15 min 00 s | 0.0000 |
