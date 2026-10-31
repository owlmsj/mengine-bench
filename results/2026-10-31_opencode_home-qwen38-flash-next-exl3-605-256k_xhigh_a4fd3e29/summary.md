# mengine-bench 1.1.0: opencode opencode v2.2.2 / home/qwen38-flash-next-exl3-605-256k (xhigh)

| Score | Correct % | Solved | Judge | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| **95.4** | 100.0 | 14/14 | 84.8 | 8 min 29 s | >= $0.00 (price) | 1.62M |

- Judge: claude-opus-5-5@xhigh, rubric 2.1
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4-3600; model=Qwen3.8-Flash-Next; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-6.05bpw; ctx=256k; drafter=MTP n6 dynamic; role=default; disk=Linux SSD; temperature=0.5; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T16:00:21Z; bench at 645d259d6703; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 87 | 20.9 s | 0.0000 | 5 | 6 | 2.0k | 0.0k | 8 s |
| bo-pnl-runway | ok | 100% | 11/11 | 85 | 36.9 s | 0.0000 | 12 | 12 | 3.5k | 0.0k | 13 s |
| bo-reconcile | ok | 100% | 4/4 | 90 | 27.6 s | 0.0000 | 5 | 6 | 3.2k | 0.0k | 17 s |
| cmp-handoff | ok | 100% | 10/10 | 88 | 29.9 s | 0.0000 | 10 | 8 | 2.5k | 0.0k | 9 s |
| lc-changelog | ok | 100% | 5/5 | 80 | 21.8 s | 0.0000 | 2 | 1 | 1.4k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 80 | 4.5 s | 0.0000 | 2 | 1 | 0.2k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 79 | 26.5 s | 0.0000 | 8 | 7 | 3.0k | 0.0k | 5 s |
| gd-astar-doors | ok | 100% | 1/1 | 86 | 37.7 s | 0.0000 | 8 | 8 | 4.5k | 0.0k | 9 s |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 86 | 12.6 s | 0.0000 | 6 | 11 | 0.9k | 0.0k | 7 s |
| ir-studio-wiki | ok | 100% | 6/6 | 91 | 15.8 s | 0.0000 | 5 | 4 | 1.2k | 0.0k | 8 s |
| ir-server-logs | ok | 100% | 6/6 | 90 | 35.5 s | 0.0000 | 7 | 8 | 1.9k | 0.0k | 28 s |
| gd-integration-repo | ok | 100% | 7/7 | 90 | 1 min 13 s | 0.0000 | 12 | 25 | 7.7k | 0.0k | 56 s |
| web-mondrian-landing | ok | 100% | 9/9 | 85 | 58.3 s | 0.0000 | 18 | 17 | 7.4k | 0.0k | 26 s |
| 3d-voxel-landscape | ok | 100% | 6/6 | 70 | 1 min 48 s | 0.0000 | 6 | 11 | 13.6k | 0.0k | 75 s |
