# mengine-bench 1.1.0: opencode opencode v2.2.2 / home/qwen38-flash-next-exl3-605-256k (medium)

| Score | Correct % | Solved | Judge | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| **81.8** | 85.7 | 12/14 | 72.7 | 5 min 50 s | >= $0.00 (price) | 1.04M |

- Judge: claude-opus-5-5@xhigh, rubric 2.1
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4-3600; model=Qwen3.8-Flash-Next; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-6.05bpw; ctx=256k; drafter=MTP n6 dynamic; role=default; disk=Linux SSD; temperature=0.5; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T15:27:11Z; bench at d4357f3964c3; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 0% | 0/6 | 36 | 13.6 s | 0.0000 | 5 | 5 | 1.0k | 0.0k | 4 s |
| bo-pnl-runway | ok | 100% | 11/11 | 77 | 16.0 s | 0.0000 | 6 | 5 | 1.3k | 0.0k | 6 s |
| bo-reconcile | ok | 100% | 4/4 | 85 | 16.6 s | 0.0000 | 5 | 5 | 1.5k | 0.0k | 7 s |
| cmp-handoff | ok | 100% | 10/10 | 86 | 27.8 s | 0.0000 | 10 | 8 | 2.4k | 0.0k | 9 s |
| lc-changelog | ok | 100% | 5/5 | 70 | 16.2 s | 0.0000 | 3 | 2 | 0.8k | 0.0k | 3 s |
| vis-chart | ok | 100% | 4/4 | 77 | 4.6 s | 0.0000 | 2 | 1 | 0.2k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 79 | 23.7 s | 0.0000 | 10 | 9 | 2.5k | 0.0k | 6 s |
| gd-astar-doors | ok | 100% | 1/1 | 69 | 15.9 s | 0.0000 | 6 | 7 | 1.7k | 0.0k | 8 s |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 91 | 11.3 s | 0.0000 | 6 | 10 | 0.8k | 0.0k | 6 s |
| ir-studio-wiki | ok | 100% | 6/6 | 87 | 17.1 s | 0.0000 | 8 | 12 | 1.3k | 0.0k | 11 s |
| ir-server-logs | ok | 100% | 6/6 | 88 | 22.4 s | 0.0000 | 8 | 9 | 2.2k | 0.0k | 16 s |
| gd-integration-repo | ok | 100% | 7/7 | 88 | 1 min 10 s | 0.0000 | 11 | 24 | 8.8k | 0.0k | 54 s |
| web-mondrian-landing | ok | 100% | 9/9 | 85 | 46.5 s | 0.0000 | 10 | 10 | 6.1k | 0.0k | 31 s |
| 3d-voxel-landscape | crash (crash) | 0% | 1/6 | 0 | 48.2 s | 0.0000 | 1 | 0 | - | - | - |
