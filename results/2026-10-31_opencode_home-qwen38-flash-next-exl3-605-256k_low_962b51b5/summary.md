# mengine-bench 1.0.0: opencode opencode v2.2.2 / home/qwen38-flash-next-exl3-605-256k (low)

| Score | Correct % | Solved | Judge | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| **94.6** | 100.0 | 14/14 | 82.1 | 9 min 41 s | >= $0.00 (price) | 2.36M |

- Judge: claude-opus-5-5@xhigh, rubric 2.0
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4-3600; model=Qwen3.8-Flash-Next; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-6.05bpw; ctx=256k; drafter=MTP n6 dynamic; role=dev; disk=Linux SSD; temperature=0.5; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T04:33:11Z; bench at 8dc14ff9c1be; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) |
| --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 86 | 40.1 s | 0.0000 |
| bo-pnl-runway | ok | 100% | 11/11 | 81 | 36.5 s | 0.0000 |
| bo-reconcile | ok | 100% | 4/4 | 72 | 21.0 s | 0.0000 |
| cmp-handoff | ok | 100% | 10/10 | 89 | 29.6 s | 0.0000 |
| lc-changelog | ok | 100% | 5/5 | 77 | 12.5 s | 0.0000 |
| vis-chart | ok | 100% | 4/4 | 72 | 4.0 s | 0.0000 |
| ds-sql-funnel | ok | 100% | 3/3 | 87 | 34.9 s | 0.0000 |
| gd-astar-doors | ok | 100% | 1/1 | 87 | 21.7 s | 0.0000 |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 80 | 12.6 s | 0.0000 |
| ir-studio-wiki | ok | 100% | 6/6 | 87 | 18.8 s | 0.0000 |
| ir-server-logs | ok | 100% | 6/6 | 89 | 45.9 s | 0.0000 |
| gd-integration-repo | ok | 100% | 7/7 | 86 | 37.8 s | 0.0000 |
| web-mondrian-landing | ok | 100% | 9/9 | 90 | 56.5 s | 0.0000 |
| 3d-voxel-landscape | ok | 100% | 6/6 | 67 | 3 min 29 s | 0.0000 |
