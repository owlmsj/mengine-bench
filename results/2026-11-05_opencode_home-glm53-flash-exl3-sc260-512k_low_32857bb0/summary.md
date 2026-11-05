# mengine-bench 2.6.0: opencode opencode v2.2.5 / home/glm53-flash-exl3-sc260-512k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **94.4** | 100.0 | 7/7 | 82.6 | 94.8 | 6 min 18 s | $0.00 (price) | 0.58M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4; model=GLM-5.3-Flash; runtime=exllamav3 0c325eff + TabbyAPI 8f92fac5; quant=turboderp-sc_2.60bpw; ctx=512k; cache=Q8, 60 experts on CPU; drafter=MTP n5 dynamic; role=advisor; disk=USB SSD 20 Gbps; tier=2; temperature=1.0; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-05, started 2026-11-05T17:11:57Z; bench at f343274bbb4f; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 5/5 | 79 | 56.0 s | 0.0000 | 7 | 7 | 0.3 | 1.1k | 0.0k | 26 s |
| bo-reconcile | ok | 100% | 5/5 | 84 | 42.2 s | 0.0000 | 6 | 5 | 0.3 | 1.3k | 0.0k | 21 s |
| cmp-handoff | ok | 100% | 12/12 | 80 | 1 min 10 s | 0.0000 | 17 | 15 | 0.0 | 2.0k | 0.0k | 20 s |
| git-merge-conflict | ok | 100% | 7/7 | 88 | 51.2 s | 0.0000 | 10 | 9 | 0.3 | 1.2k | 0.0k | 28 s |
| infra-gpu-fit | ok | 100% | 7/7 | 64 | 27.4 s | 0.0000 | 3 | 4 | 0.0 | 0.9k | 0.0k | 12 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 85 | 1 min 21 s | 0.0000 | 11 | 10 | 0.3 | 2.2k | 0.0k | 64 s |
| ts-plugin-bug | ok | 100% | 8/8 | 98 | 50.3 s | 0.0000 | 8 | 10 | 0.0 | 1.3k | 0.0k | 19 s |

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 4)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 4); recorded the result (call 15)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 8); committed (call 8)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 2); read the policy (call 1); recorded the result (call 4)
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 4); read the settings (call 4); read the owner notes (call 3); recorded the result (call 9)
- `ts-plugin-bug`: read the bus (call 3); ran the tests (call 8)
