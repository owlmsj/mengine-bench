"""`mengine-bench judge <bundle>`: the maintainer judges a result bundle, then rescores it.

The only judge path (#23). A run stores the judge's evidence in its bundle:
judge/<task>.json (prompts, answers, workspace diff, transcript tail, checks,
all redacted) and each declared deliverable verbatim (redacted) under
judge/<task>/<file>. The maintainer runs this while reviewing the result pull
request, so contributors need no judge and every ranked run is judged the
same way: one rubric 2.0 vote per task. For a task whose deliverable is an
HTML page, the stored page is rendered headless in a temp dir and the judge
sees the screenshot; a blank or failed render scores that task's judge 0.
Nothing is written unless every task ends with a vote.
"""

from __future__ import annotations

import json
import shutil
import tempfile
from collections.abc import Callable, MutableMapping
from dataclasses import dataclass
from pathlib import Path

from mengine_bench.bundle import JUDGE_DIR, RESULT_NAME, SUMMARY_NAME, public_text
from mengine_bench.judge import RUBRIC_VERSION, JudgeContext, RubricJudge, TaskVerdict
from mengine_bench.redact import PathScope, local_names
from mengine_bench.report import render_summary
from mengine_bench.runner.agents import Agent
from mengine_bench.scoring import combined_score, judge_mean
from mengine_bench.visual import RENDERED, render_headless, screenshot_has_content

TaskEntry = MutableMapping[str, object]
Renderer = Callable[[Path, Path], str]
# A blank or black 1440x900 page compresses far below this; a real layout does not.
BLANK_PNG_BYTES = 10_000


@dataclass(frozen=True)
class JudgePacket:
    context: JudgeContext
    # Workspace-relative HTML deliverable to render, stored under judge/<task>/.
    render: str | None


def read_packet(bundle: Path, task_id: str) -> JudgePacket:
    packet_file = bundle / JUDGE_DIR / f"{task_id}.json"
    if not packet_file.is_file():
        raise ValueError(f"received {bundle.name} without {JUDGE_DIR}/{task_id}.json; expected judge evidence "
                         f"for every task (a bundle written by bench 1.0 or later)")
    record = json.loads(packet_file.read_text(encoding="utf-8"))
    render = record.get("render")
    return JudgePacket(context=JudgeContext.from_record(record), render=render if isinstance(render, str) else None)


def _render_verdict(bundle: Path, task_id: str, packet: JudgePacket, judge: RubricJudge, workdir: Path,
                    render: Renderer) -> TaskVerdict:
    """Render the stored page outside the bundle; the judge sees the screenshot, a failed render scores 0."""
    stored = bundle / JUDGE_DIR / task_id
    site = workdir / "site"
    if stored.is_dir():
        shutil.copytree(stored, site)
    page = str(packet.render)
    png = workdir / "render" / "shot.png"
    status = render(site / page, png)
    if status != RENDERED or not screenshot_has_content(png, BLANK_PNG_BYTES):
        reason = status if status != RENDERED else f"blank screenshot (< {BLANK_PNG_BYTES} bytes)"
        return TaskVerdict(score=0, rationale=f"render of {page} failed: {reason}; judge 0 for this task")
    return judge.grade(packet.context, workdir / "judge", png)


def judge_bundle(bundle: Path, judge_agent: Agent, render: Renderer | None = None) -> dict[str, object]:
    """Judge every task, rescore, and rewrite result.json and summary.md; raises ValueError, writing nothing,
    when the bundle is already judged, lacks evidence, or a task ends without a vote."""
    result = json.loads((bundle / RESULT_NAME).read_text(encoding="utf-8"))
    if isinstance(result.get("judge"), dict):
        raise ValueError(f"received {bundle.name} already judged by {result['judge'].get('model')}; expected a "
                         f"bundle without a judge")
    tasks = result["tasks"]
    packets = {str(task["id"]): read_packet(bundle, str(task["id"])) for task in tasks}
    judge = RubricJudge(judge_agent)
    verdicts: dict[str, TaskVerdict] = {}
    with tempfile.TemporaryDirectory(prefix="mengine-bench-judge-") as tmp:
        for task_id, packet in packets.items():
            print(f"[{task_id}] judging", flush=True)
            workdir = Path(tmp) / task_id
            if packet.render is None:
                verdicts[task_id] = judge.grade(packet.context, workdir / "judge")
                continue
            verdicts[task_id] = _render_verdict(bundle, task_id, packet, judge, workdir,
                                                render or render_headless)
    missing = {task_id: verdict.errors[-1:] for task_id, verdict in verdicts.items() if verdict.score is None}
    if missing:
        raise ValueError(f"received no judge vote for {sorted(missing)} ({missing}); expected one vote per task, "
                         f"so nothing was written")
    for task in tasks:
        verdict = verdicts[str(task["id"])]
        task.update(judge=verdict.score, judge_rationale=verdict.rationale, judge_errors=list(verdict.errors))
    # The judge changes Judge and Score only: checks, Correct %, Time and Cost stay as the run published them.
    totals = result["totals"]
    totals["judge"] = judge_mean([verdicts[str(task["id"])].score for task in tasks])
    totals["score"] = combined_score(float(totals["correct"]), totals["judge"])
    result["judge"] = {"agent": judge_agent.name, "model": judge_agent.model, "effort": judge_agent.effort,
                       "rubric": RUBRIC_VERSION}
    (bundle / RESULT_NAME).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
                                      newline="\n")
    scope = PathScope(names=local_names().allowing(result.get("submitter")))
    (bundle / SUMMARY_NAME).write_text(public_text(render_summary(result), scope), encoding="utf-8", newline="\n")
    return result
