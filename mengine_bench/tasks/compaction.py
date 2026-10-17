"""Compaction tasks, AMA-Bench style: compact, then answer from the
compaction ALONE in a fresh session (the source is moved out of reach).

The source holds superseded values on purpose (a spilled VRAM reading, a
price that was debated then changed): a summary that keeps the first number
instead of the final one fails, exactly like a bad handoff in real life.
"""

from __future__ import annotations

import json
import random
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import (
    FAST,
    FULL,
    CheckResult,
    EvalTask,
    Step,
    answer_json,
    has,
    read,
    write,
)

FILLER = [
    "Ran `git status` again; nothing new beyond what was already listed.",
    "Read the whole llama-server log; most of it is tensor-loading noise.",
    "Checked the flag documentation in --help; the text did not help much.",
    "Waiting for the download to finish before measuring, so the number is not contaminated.",
    "Reviewed the diff: formatting only, no behavior change.",
    "Opened the GPU panel; the graphs say nothing the counter does not already say.",
    "Tried to reproduce with the short prompt; prefill is irrelevant at that size.",
    "Noted for later: review the names of the scratchpad temp files.",
]

# Fictional speakers: Alice chairs, Bruno and Carla debate.
MEETING_FILLER = [
    "[Bruno] Quick aside: the air conditioner in room 2 is dripping again.",
    "[Carla] Did anyone see the accountant's email about the monthly tax slip? I think it was paid.",
    "[Alice] Noted, moving on. No need to decide that today.",
    "[Bruno] The funnel dashboard is slow again, but it is the browser cache.",
    "[Carla] Reminder: end-of-semester party, vote in the #general channel.",
    "[Alice] Let's keep to the agenda, please.",
    "[Bruno] I have last quarter's numbers, but they do not change the discussion.",
    "[Carla] I partly agree; I will send it in writing later.",
]


def _transcript(seed: int, key_turns: list[str], filler_turns: int, filler: Sequence[str] = FILLER) -> str:
    rng = random.Random(seed)
    turns: list[str] = []
    slots = sorted(rng.sample(range(filler_turns + len(key_turns)), len(key_turns)))
    key_iter = iter(key_turns)
    for i in range(filler_turns + len(key_turns)):
        if i in slots:
            turns.append(next(key_iter))
        else:
            line = rng.choice(filler)
            if filler is FILLER:
                line = f"[agent] {line} (step {i})\n[tool] ok, {rng.randint(40, 900)} lines of output omitted"
            turns.append(line)
    return "\n\n".join(turns) + "\n"


def _summary_check(result: CheckResult, text: str | None, limit: int, must: Sequence[str]) -> None:
    result.add(f"summary exists and fits in {limit} characters", text is not None and 0 < len(text) <= limit)
    for literal in must:
        result.add(f"summary keeps `{literal}`", bool(text) and literal in (text or ""))


# ------------------------------------------------------------ cmp-handoff --

HANDOFF_KEYS = [
    "[user] The local model needs 128k. Measure local-9b Q5 at that context.",
    "[agent] Measured with `pwsh -File scripts/measure_decode.ps1 -Ctx 131072 -NPredict 1024`: decode 37.8 t/s, VRAM 7881 MiB.",
    "[agent] WARNING: 7881 MiB is the WDDM ceiling; the Shared Usage counter shows 1494 MiB spilled. That number does not count.",
    "[agent] With `--no-mmproj-offload` and `-ub 512` the spill is gone: final VRAM 7697 MiB, final decode 38.0 t/s (median of 3).",
    "[agent] Q6_K (7.03 GiB) does not fit at 128k; discarded. Q4_K_M fits with 7305 MiB and 40.4 t/s, kept only as fallback.",
    "[agent] Applied the recipe in scripts/start_server.ps1:165 (local9 block) and in the profile profiles/local/local-9b.json.",
    "[user] Great. What is left?",
    "[agent] Pending: update the evals README, which still cites check_vision.ps1 (the file no longer exists).",
]
HANDOFF_GOLD = {
    "file_line": r"start_server\.ps1:165",
    "final_decode": r"38[.,]0",
    "final_vram_mib": r"7697",
    "discarded_quant": r"Q6",
    "pending": r"README|check_vision",
    "measure_command": r"measure_decode\.ps1",
}


def _handoff_setup(ws: Path) -> None:
    write(ws, "session/transcript.md", _transcript(6329, HANDOFF_KEYS, 70))


def _handoff_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    _summary_check(result, read(ws, "HANDOFF.md"), 1500, ["--no-mmproj-offload", "7697"])
    got = answer_json(answers)
    for key, pattern in HANDOFF_GOLD.items():
        result.add(f"answer {key}", has(str(got.get(key, "")), pattern))
    result.add("does not repeat the spilled VRAM as final", "7881" not in str(got.get("final_vram_mib", "")))
    return result


def _handoff_reference(ws: Path) -> list[str]:
    write(ws, "HANDOFF.md", "local-9b Q5 128k: `--no-mmproj-offload` + `-ub 512` in scripts/start_server.ps1:165; "
          "decode 38.0 t/s, VRAM 7697 MiB (7881 was spill). Q6_K does not fit. Measure: "
          "`pwsh -File scripts/measure_decode.ps1 -Ctx 131072 -NPredict 1024`. Pending: evals README "
          "(check_vision.ps1 is gone).\n")
    return ["ok", json.dumps({"file_line": "scripts/start_server.ps1:165", "final_decode": "38.0",
                              "final_vram_mib": 7697, "discarded_quant": "Q6_K", "pending": "evals README",
                              "measure_command": "pwsh -File scripts/measure_decode.ps1 -Ctx 131072 -NPredict 1024"})]


# ------------------------------------------------------ cmp-meeting-decisions --

MEETING_KEYS = [
    "[Alice] Item 1: Pro plan price. Today BRL 49/month, low churn, CAC rising.",
    "[Bruno] I propose BRL 59. Competitor benchmark is between 55 and 69.",
    "[Carla] 59 scares the base of small studios. I suggest 55 with 6 months of grandfathering for current payers.",
    "[Alice] Decided: Pro goes to BRL 55/month starting August 1st, current base keeps BRL 49 until January 31st, 2027.",
    "[Bruno] Item 2: hiring. Proposal of 3 roles: SRE, backend dev, designer.",
    "[Alice] Decided: hiring freeze, except 1 SRE role. Role owner: Alice. Open it by July 15th.",
    "[Carla] Item 3: cloud. We spent BRL 71k in June, driven by a test GPU left running.",
    "[Alice] Decided: cloud cap of BRL 60k/month; billing alert at 80% of the cap. Owner: Bruno.",
    "[Bruno] Item 4: billing. I will migrate invoicing from manual bank slips to Stripe.",
    "[Alice] Decided: Bruno migrates billing to Stripe by July 31st; Carla validates the first month's reconciliation.",
    "[Carla] Oh, and the designer? Deferred to Q4 if revenue goes above BRL 300k/month.",
]
MEETING_GOLD = {
    "new_pro_price": r"\b55\b",
    "new_price_start": r"2026-08-01|01/08|08/01|\baug",
    "approved_role": r"SRE",
    "role_owner": r"Alice",
    "monthly_cloud_cap": r"60",
    "stripe_deadline": r"2026-07-31|31/07|07/31|jul(y)?\.? 31|31(st)? (of )?jul",
    "designer_trigger": r"300",
}


def _meeting_setup(ws: Path) -> None:
    write(ws, "meetings/2026-06-30-ops.md", "# Weekly operations meeting - 2026-06-30\n\n" + _transcript(6330, MEETING_KEYS, 220, MEETING_FILLER))


def _meeting_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    _summary_check(result, read(ws, "DECISIONS.md"), 2000, ["55", "SRE", "Stripe"])
    got = answer_json(answers)
    for key, pattern in MEETING_GOLD.items():
        result.add(f"answer {key}", has(str(got.get(key, "")), pattern))
    result.add("final price is not the proposed one (59)", "59" not in str(got.get("new_pro_price", "")))
    return result


def _meeting_reference(ws: Path) -> list[str]:
    write(ws, "DECISIONS.md", "- Pro BRL 55/month from 2026-08-01; current base BRL 49 until 2027-01-31 (59 rejected).\n"
          "- Hiring freeze; exception 1 SRE, owner Alice, open by 07-15. Designer only in Q4 if revenue > BRL 300k/month.\n"
          "- Cloud cap BRL 60k/month, alert at 80%, owner Bruno.\n- Bruno migrates billing to Stripe by 2026-07-31; Carla reconciles.\n")
    return ["ok", json.dumps({"new_pro_price": 55, "new_price_start": "2026-08-01", "approved_role": "SRE",
                              "role_owner": "Alice", "monthly_cloud_cap": 60000, "stripe_deadline": "2026-07-31",
                              "designer_trigger": "revenue above BRL 300k/month"})]


# ------------------------------------------------------ cmp-agent-trajectory --


def _trajectory() -> str:
    rng = random.Random(6331)
    events: list[dict[str, object]] = []
    files = ["server/net/replication.cpp", "server/net/serializer.cpp", "server/sim/tick.cpp", "tests/net_test.cpp"]
    p99_series = [14.2, 13.6, 12.9]
    for i in range(160):
        kind = rng.choice(["read", "grep", "bash", "edit"])
        entry: dict[str, object] = {"step": i, "tool": kind}
        if kind == "edit":
            entry["file"] = rng.choice(files[1:])
        elif kind == "bash":
            entry["cmd"] = "ctest -R Net --output-on-failure"
            entry["result"] = "12 passed"
        else:
            entry["file"] = rng.choice(files)
        events.append(entry)
    plan: dict[int, dict[str, object]] = {
        30: {"tool": "bash", "cmd": "tools/bench_tick.sh", "result": f"tick p99 = {p99_series[0]} ms"},
        55: {"tool": "note", "text": "Trying a SIMD (AVX2) serializer for delta compression."},
        78: {"tool": "bash", "cmd": "tools/bench_tick.sh", "result": f"tick p99 = {p99_series[1]} ms"},
        96: {"tool": "note", "text": "Abandoning the SIMD serializer: crash on the ARM64 dedicated server build; reverted."},
        120: {"tool": "bash", "cmd": "tools/bench_tick.sh", "result": f"tick p99 = {p99_series[2]} ms"},
        150: {"tool": "bash", "cmd": "tools/bench_tick.sh", "result": "tick p99 = 11.8 ms"},
        157: {"tool": "edit", "file": "server/net/replication.cpp"},
        158: {"tool": "read", "file": "tests/net_test.cpp"},
        159: {"tool": "bash", "cmd": "ctest -R Net --output-on-failure", "result": "1 failed: ReplicationTest.DeltaCompression"},
    }
    for step, entry in plan.items():
        events[step] = {"step": step, **entry}
    return "\n".join(json.dumps(e, ensure_ascii=False) for e in events) + "\n"


TRAJ_GOLD = {
    "last_edited_file": r"replication\.cpp",
    "failing_test": r"ReplicationTest\.DeltaCompression",
    "last_measured_p99_ms": r"11[.,]8",
    "abandoned_approach": r"SIMD|AVX",
    "abandon_reason": r"ARM|crash",
}


def _traj_setup(ws: Path) -> None:
    write(ws, "agent/trajectory.jsonl", _trajectory())


def _traj_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    _summary_check(result, read(ws, "STATE.md"), 1800, ["11.8", "DeltaCompression"])
    got = answer_json(answers)
    for key, pattern in TRAJ_GOLD.items():
        result.add(f"answer {key}", has(str(got.get(key, "")), pattern))
    result.add("last p99 is not an intermediate one", not any(v in str(got.get("last_measured_p99_ms", "")) for v in ("14.2", "13.6", "12.9")))
    return result


def _traj_reference(ws: Path) -> list[str]:
    write(ws, "STATE.md", "p99 14.2 -> 11.8 ms. SIMD/AVX2 serializer abandoned (ARM64 crash). Last edit: "
          "server/net/replication.cpp. Failing: ReplicationTest.DeltaCompression.\n")
    return ["ok", json.dumps({"last_edited_file": "server/net/replication.cpp",
                              "failing_test": "ReplicationTest.DeltaCompression", "last_measured_p99_ms": "11.8",
                              "abandoned_approach": "SIMD AVX2 serializer", "abandon_reason": "crash on ARM64"})]


def _two_steps(source: str, summary: str, limit: int, ask: str) -> tuple[Step, ...]:
    return (
        Step(f"Read {{WS}}/{source} and write {{WS}}/{summary} with at most {limit} characters: the final state for "
             "someone else to continue without the original. Keep exact commands, file:line, FINAL measured numbers, "
             "decisions, owners, deadlines and pending items; drop noise and superseded values. Work only inside {WS}."),
        Step(f"You just took over this work. The only context is {{WS}}/{summary} (read it). {ask} "
             "Reply ONLY with a JSON object.", fresh_session=True, hide=(source,), carry=(summary,)),
    )


# par_s: DeepSeek V4.1 Flash wall times from the maintainers' v1 FAST run
# (2026-09-23), rounded up. cmp-meeting-decisions and cmp-agent-trajectory
# were not in that run: 2x cmp-handoff (19.6 s), the closest compaction task.
TASKS = [
    EvalTask(
        id="cmp-handoff", category="compaction", suites=frozenset({FAST, FULL}),
        provenance="Agent debugging-session handoff on a local LLM server; native retention rules",
        summary="Compact a debugging session into HANDOFF.md <=1500 chars and answer 6 questions from it alone",
        setup=_handoff_setup, check=_handoff_check, reference=_handoff_reference, timeout_s=360, par_s=20,
        steps=_two_steps("session/transcript.md", "HANDOFF.md", 1500,
                         "Keys: file_line (where the recipe was applied), final_decode, final_vram_mib, "
                         "discarded_quant, pending, measure_command."),
    ),
    EvalTask(
        id="cmp-meeting-decisions", category="compaction", suites=frozenset({FULL}),
        provenance="Startup weekly ops meeting: decisions, owners, deadlines, with a debated-then-changed price",
        summary="Compact a long operations meeting into DECISIONS.md and answer 7 questions from it alone",
        setup=_meeting_setup, check=_meeting_check, reference=_meeting_reference, timeout_s=420, par_s=40,
        steps=_two_steps("meetings/2026-06-30-ops.md", "DECISIONS.md", 2000,
                         "Keys: new_pro_price, new_price_start, approved_role, role_owner, monthly_cloud_cap, "
                         "stripe_deadline, designer_trigger."),
    ),
    EvalTask(
        id="cmp-agent-trajectory", category="compaction", suites=frozenset({FULL}),
        provenance="AMA-Bench style: compact a 160-step agent trajectory (JSONL) and answer from the state only",
        summary="Compact an agent trajectory (160 steps) into STATE.md and answer 5 questions from it alone",
        setup=_traj_setup, check=_traj_check, reference=_traj_reference, timeout_s=420, par_s=40,
        steps=_two_steps("agent/trajectory.jsonl", "STATE.md", 1800,
                         "Keys: last_edited_file, failing_test, last_measured_p99_ms (last tools/bench_tick.sh), "
                         "abandoned_approach, abandon_reason."),
    ),
]
