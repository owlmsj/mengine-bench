"""`mengine-bench judge <bundle>`: the maintainer judges a result bundle, then rescores it.

The only judge path (#23). A run stores the judge's evidence in its bundle:
judge/<task>.json (prompts, answers, workspace diff, transcript tail, checks,
all redacted) and each declared deliverable verbatim (redacted) under
judge/<task>/<file>. The maintainer runs this while reviewing the result pull
request, so contributors need no judge and every ranked run is judged the
same way: one rubric 2.3 vote per task. For a task whose deliverable is an
HTML page, the stored page is rendered headless in a temp dir and the judge
sees the screenshot, kept as judge/<task>.png for audit; a blank or failed
render scores that task's judge 0, unless the run was stopped at its limit:
then the judge votes on what exists. Nothing is written unless every task ends
with a vote.
"""

from __future__ import annotations

import json
import shutil
import tempfile
from collections.abc import Callable, MutableMapping
from dataclasses import dataclass, replace
from pathlib import Path

from mengine_bench import catalog
from mengine_bench.bundle import JUDGE_DIR, RESULT_NAME, SUMMARY_NAME, public_json, public_text
from mengine_bench.judge import RUBRIC_VERSION, JudgeContext, RubricJudge, TaskVerdict
from mengine_bench.redact import PathScope, local_names
from mengine_bench.report import render_summary
from mengine_bench.runner.agents import Agent
from mengine_bench.scoring import combined_score, judge_mean, speed_points
from mengine_bench.visual import RENDERED, is_render_failure, render_headless, screenshot_has_content

TaskEntry = MutableMapping[str, object]
Renderer = Callable[[Path, Path], str]
# A blank or black 1440x900 page compresses far below this; a real layout does not.
BLANK_PNG_BYTES = 10_000
RENDER_ATTEMPTS = 3


@dataclass(frozen=True)
class JudgePacket:
    context: JudgeContext
    # Workspace-relative HTML deliverable to render, stored under judge/<task>/.
    render: str | None


def read_packet(bundle: Path, task_id: str) -> JudgePacket:
    """The evidence of one task. The bundle comes from a contributor's pull request, so the task's prompts
    and the page to render come from the catalog, never from the packet (#23 review)."""
    task = next((task for task in catalog.all_tasks() if task.id == task_id), None)
    if task is None:
        raise ValueError(f"received task {task_id!r} in {bundle.name}; expected a catalog task id")
    packet_file = bundle / JUDGE_DIR / f"{task_id}.json"
    if not packet_file.is_file():
        raise ValueError(f"received {bundle.name} without {JUDGE_DIR}/{task_id}.json; expected judge evidence "
                         f"for every task (a bundle written by bench 1.0 or later)")
    record = json.loads(packet_file.read_text(encoding="utf-8"))
    context = replace(JudgeContext.from_record(record), task_id=task.id,
                      prompts=tuple(step.prompt for step in task.steps))
    return JudgePacket(context=context, render=task.render_target)


def _render_verdict(bundle: Path, task_id: str, packet: JudgePacket, judge: RubricJudge, workdir: Path,
                    render: Renderer) -> TaskVerdict:
    """Render the stored page outside the bundle; the judge sees the screenshot, a failed render scores 0."""
    stored = bundle / JUDGE_DIR / task_id
    site = workdir / "site"
    page = str(packet.render)
    # copytree would follow a link a PR committed next to the page into a maintainer file (#23 review).
    links = [path for path in stored.rglob("*") if path.is_symlink()] if stored.is_dir() else []
    if links:
        return TaskVerdict(score=0, rationale=f"render of {page} refused: symlink in the stored deliverables "
                                              f"({links[0].name}); judge 0 for this task")
    if stored.is_dir():
        shutil.copytree(stored, site)
    png = workdir / "render" / "shot.png"
    # #68: a browser timeout is not the page's fault until it repeats.
    for _ in range(RENDER_ATTEMPTS):
        status = render(site / page, png)
        if not is_render_failure(status):
            break
    if status != RENDERED or not screenshot_has_content(png, BLANK_PNG_BYTES):
        if packet.context.status == "timeout":
            # #41: a run stopped at its limit is graded on what exists, never zeroed for a missing page.
            return judge.grade(packet.context, workdir / "judge")
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
    screenshots: dict[str, bytes] = {}
    with tempfile.TemporaryDirectory(prefix="mengine-bench-judge-") as tmp:
        for task_id, packet in packets.items():
            print(f"[{task_id}] judging", flush=True)
            workdir = Path(tmp) / task_id
            if packet.render is None:
                verdicts[task_id] = judge.grade(packet.context, workdir / "judge")
                continue
            verdicts[task_id] = _render_verdict(bundle, task_id, packet, judge, workdir,
                                                render or render_headless)
            shot = workdir / "render" / "shot.png"
            if shot.is_file():
                screenshots[task_id] = shot.read_bytes()
    missing = {task_id: verdict.errors[-1:] for task_id, verdict in verdicts.items() if verdict.score is None}
    if missing:
        raise ValueError(f"received no judge vote for {sorted(missing)} ({missing}); expected one vote per task, "
                         f"so nothing was written")
    for task_id, png in screenshots.items():
        (bundle / JUDGE_DIR / f"{task_id}.png").write_bytes(png)
    for task in tasks:
        verdict = verdicts[str(task["id"])]
        task.update(judge=verdict.score, judge_rationale=verdict.rationale, judge_errors=list(verdict.errors))
    # The judge changes Judge and Score only: checks, Correct %, Time and Cost stay as the run published them.
    totals = result["totals"]
    totals["judge"] = judge_mean([verdicts[str(task["id"])].score for task in tasks])
    totals["speed"] = speed_points(float(totals["time_s"]))
    totals["score"] = combined_score(float(totals["correct"]), totals["judge"], totals["speed"])
    result["judge"] = {"agent": judge_agent.name, "model": judge_agent.model, "effort": judge_agent.effort,
                       "rubric": RUBRIC_VERSION}
    # Rationales and errors come from the maintainer's machine: redact them like the run's own text.
    scope = PathScope(names=local_names().allowing(result.get("submitter")))
    public = public_json(result, scope)
    assert isinstance(public, dict)
    result = public
    (bundle / RESULT_NAME).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
                                      newline="\n")
    (bundle / SUMMARY_NAME).write_text(public_text(render_summary(result), scope), encoding="utf-8", newline="\n")
    return result
