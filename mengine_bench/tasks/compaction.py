"""Compaction tasks, AMA-Bench style: compact, then answer from the
compaction ALONE in a fresh session (the source is moved out of reach).

The source holds superseded values on purpose (a spilled VRAM reading, a
quantization that was later discarded): a summary that keeps the first number
instead of the final one fails, exactly like a bad handoff in real life.
"""

from __future__ import annotations

import json
import random
import re
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import (
    CheckResult,
    EvalTask,
    Step,
    answer_json,
    close,
    has,
    read,
    saw,
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
    result.add(f"summary exists and fits in {limit} characters", text is not None and 0 < len(text) <= limit,
               "no summary file" if text is None else f"{len(text)} characters")
    for literal in must:
        result.add(f"summary keeps `{literal}`", bool(text) and literal in (text or ""), f"`{literal}` is not in the summary")


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
    "file_line": r"\bstart_server\.ps1\b.{0,40}?\b165\b",
    # #59: the value with a unit glued to it counts; the superseded 37.8 next to it does not.
    "final_decode": r"^(?!.*37[.,]8)(?=.*(?<![\w.,+-])38(?:[.,]0+)?(?!\d|[.,]\d))",
    "final_vram_mib": r"(?<![\w.,+-])7697(?:[.,]0+)?(?!\w|[.,]\d)",
    "discarded_quant": r"\bQ6(?:_?K)?\b",
    # #28, #59: the README with what is wrong in it, in any wording, and not another README.
    "pending": r"^(?!.*\broot\b)(?=.*\bREADME\b)"
               r"(?=.*\b(?:update|fix|remove|edit|replace|check_vision|evals|stale|out of date))",
    # #59: both numbers, and not swapped between the flags.
    "measure_command": r"^(?!.*-Ctx[\s:=]+1024\b)(?!.*-NPredict[\s:=]+131072\b)"
                       r"(?=.*\bmeasure_decode\.ps1\b)(?=.*\b131072\b)(?=.*\b1024\b)",
}


HANDOFF_LIMIT = 1000


def _handoff_setup(ws: Path) -> None:
    write(ws, "session/transcript.md", _transcript(6329, HANDOFF_KEYS, 70))


def _handoff_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    _summary_check(result, read(ws, "HANDOFF.md"), HANDOFF_LIMIT, ["--no-mmproj-offload", "-ub 512", "7697"])
    got = answer_json(answers)
    # #59: "7,697 MiB" and "Q5 at 7697 MiB" hold the value. The first MiB-sized number is the answer, so
    # "7697 (7881 was the spill)" passes and "7881, corrected to 7697" does not.
    numbers = re.findall(r"\d+(?:\.\d+)?", re.sub(r"(?<=\d),(?=\d{3}\b)", "", str(got.get("final_vram_mib", ""))))
    vram = next((number for number in numbers if float(number) >= 1000), None)
    got["final_vram_mib"] = vram or ""
    for key, pattern in HANDOFF_GOLD.items():
        result.add(f"answer {key}", has(str(got.get(key, "")), pattern), saw(got.get(key), f"a match for {pattern}"))
    result.add("does not repeat the spilled VRAM as final", vram is not None and not close(vram, 7881, 0), saw(vram, "not 7881"))
    return result


def _handoff_reference(ws: Path) -> list[str]:
    write(ws, "HANDOFF.md", "local-9b Q5 128k: `--no-mmproj-offload` + `-ub 512` in scripts/start_server.ps1:165; "
          "decode 38.0 t/s, VRAM 7697 MiB (7881 was spill). Q6_K does not fit. Measure: "
          "`pwsh -File scripts/measure_decode.ps1 -Ctx 131072 -NPredict 1024`. Pending: evals README "
          "(check_vision.ps1 is gone).\n")
    return ["ok", json.dumps({"file_line": "scripts/start_server.ps1:165", "final_decode": "38.0",
                              "final_vram_mib": 7697, "discarded_quant": "Q6_K", "pending": "Update evals README",
                              "measure_command": "pwsh -File scripts/measure_decode.ps1 -Ctx 131072 -NPredict 1024"})]


def _two_steps(source: str, summary: str, limit: int, ask: str) -> tuple[Step, ...]:
    return (
        Step(f"Read {{WS}}/{source} and write {{WS}}/{summary} with at most {limit} characters: the final state for "
             "someone else to continue without the original. Keep exact commands, file:line, FINAL measured numbers, "
             "decisions, owners, deadlines and pending items; drop noise and superseded values. Work only inside {WS}."),
        Step(f"You just took over this work. The only context is {{WS}}/{summary} (read it). {ask} "
             "Reply ONLY with a JSON object.", fresh_session=True, hide=(source,), carry=(summary,)),
    )


TASKS = [
    EvalTask(
        id="cmp-handoff", category="compaction",
        provenance="Agent debugging-session handoff on a local LLM server; native retention rules",
        summary="Summarize a debugging session, then answer questions using only that summary.",
        setup=_handoff_setup, check=_handoff_check, reference=_handoff_reference, timeout_s=120,
        steps=_two_steps("session/transcript.md", "HANDOFF.md", HANDOFF_LIMIT,
                         "Keys: file_line (where the recipe was applied), final_decode, final_vram_mib, "
                         "discarded_quant, pending, measure_command."),
    ),
]
