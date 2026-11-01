"""`mengine-bench judge <bundle>`: the maintainer judges a result bundle, then rescores it.

The only judge path (#23). A run stores the judge's evidence in its bundle:
judge/<task>.json (prompts, answers, workspace diff, transcript tail, checks,
all redacted) and each declared deliverable verbatim (redacted) under
judge/<task>/<file>. The maintainer runs this while reviewing the result pull
request, so contributors need no judge and every ranked run is judged the
same way: one rubric 2.5 vote per task. For a task whose deliverable is an
HTML page, the stored page is rendered headless in a temp dir at three moments
and the judge sees the frames, kept for audit as judge/<task>-1s.png,
judge/<task>-4s.png and judge/<task>.png (the last). A frame that keeps failing
is noted and the judge votes on the others, or without an image when none
rendered: a flaky browser is no grade. Nothing is written unless every task ends with a vote, and with no browser
at all nothing is judged. `--again` replaces the votes of a judged bundle, which is
how a change to the judging reaches the ranked runs without running them again.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
from collections.abc import Callable, MutableMapping
from dataclasses import dataclass, replace
from pathlib import Path

from mengine_bench import __version__, catalog
from mengine_bench.bundle import JUDGE_DIR, RESULT_NAME, SUMMARY_NAME, public_json, public_text
from mengine_bench.core import EvalTask
from mengine_bench.judge import JUDGE_SYSTEM_PROMPT, RUBRIC_VERSION, SCREENSHOT_NAME, JudgeContext, RubricJudge, TaskVerdict
from mengine_bench.judge_view import NO_CALLS, tool_log, transcript_streams
from mengine_bench.redact import PathScope, local_names
from mengine_bench.report import render_summary
from mengine_bench.runner.agents import Agent
from mengine_bench.scoring import combined_score, judge_mean, speed_points
from mengine_bench.visual import NO_BROWSER, RENDERED, is_render_failure, render_headless

TaskEntry = MutableMapping[str, object]
Renderer = Callable[[Path, Path, int], str]
RENDER_ATTEMPTS = 3
# (virtual time, suffix of the file kept in the bundle, name attached to the vote). Each frame is its own page load:
# the Chromium command line cannot capture a running page twice, and a new dependency is out (#93).
JUDGE_FRAMES = ((1000, "-1s", "frame-1s.png"), (4000, "-4s", "frame-4s.png"), (8000, "", SCREENSHOT_NAME))
# One fixed page per task, made by Opus 5.5 xhigh to set the bar (#93), so a grade does not move when a new run comes out.
REFERENCES_DIR = Path(__file__).resolve().parent / "assets" / "references"


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
    context = JudgeContext.from_record(record)
    log = tool_log(transcript_streams(bundle / "transcripts" / f"{task_id}.jsonl.gz"))
    if log == NO_CALLS and context.stats.get("tool_calls"):
        raise ValueError(f"received {context.stats['tool_calls']} tool_calls in {task_id} and none in its log; "
                         f"expected the judge's tool log to show them")
    context = replace(context, task_id=task.id, prompts=tuple(step.prompt for step in task.steps),
                      diff=_agent_diff(context.diff, task), tool_log=log, deliverables=_stored_deliverables(bundle, task))
    return JudgePacket(context=context, render=task.render_target)


def _stored_deliverables(bundle: Path, task: EvalTask) -> tuple[tuple[str, str], ...]:
    """Each declared file whole; a link a PR committed never reaches the prompt (#23 review)."""
    stored = [(rel, bundle / JUDGE_DIR / task.id / rel) for rel in task.deliverables]
    return tuple((rel, path.read_text(encoding="utf-8", errors="replace")) for rel, path in stored
                 if path.is_file() and not path.is_symlink())


def _agent_diff(diff: str, task: EvalTask) -> str:
    """The agent's own changes: not what the bench moved away, not a file already shown whole (#70)."""
    moved = [rel for step in task.steps for rel in (*step.hide, *step.inline)]
    head, _, bodies = diff.partition("\n\n--- ")
    lines = [line for line in head.split("\n") if not (line.startswith("D ") and any(
        line[2:] == rel or line[2:].startswith(f"{rel}/") for rel in moved))]
    kept = [body for body in re.split(r"\n\n--- ", bodies) if body and body.split(" ---", 1)[0] not in task.deliverables]
    return "\n\n--- ".join(["\n".join(lines), *kept]).strip("\n")


def _render_verdict(bundle: Path, task_id: str, packet: JudgePacket, judge: RubricJudge, workdir: Path,
                    render: Renderer) -> TaskVerdict:
    """Render the stored page outside the bundle; the judge sees the screenshot, or a note when it keeps failing."""
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
    images: dict[str, Path] = {}
    failures: list[str] = []
    for budget_ms, suffix, name in JUDGE_FRAMES:
        png = _frame_path(workdir, suffix)
        status = _render_frame(site / page, png, budget_ms, render)
        if status == NO_BROWSER:
            raise ValueError(f"received {status!r} rendering {page}; expected a browser: nothing was judged")
        if status == RENDERED:
            images[name] = png
        else:
            failures.append(f"{name}: {status}")
    # #70: the same page rendered in 4 of 5 more tries after a timeout that had scored it 0.
    note = f"Not attached, the render failed, no defect of the page: {'; '.join(failures)}." if failures else ""
    attached = {**images, **_reference_images(task_id)} if images else {}
    verdict = judge.grade(packet.context, workdir / "judge", attached, note)
    return replace(verdict, errors=(*verdict.errors, *failures))


def _reference_images(task_id: str) -> dict[str, Path]:
    return {"reference.png": REFERENCES_DIR / f"{task_id}.png"}


def _frame_path(workdir: Path, suffix: str) -> Path:
    return workdir / "render" / f"shot{suffix}.png"


def _render_frame(html: Path, png: Path, budget_ms: int, render: Renderer) -> str:
    """#68: a browser timeout is not the page's fault until it repeats."""
    for _ in range(RENDER_ATTEMPTS):
        status = render(html, png, budget_ms)
        if not is_render_failure(status):
            return status
    # The bundle keeps what the vote saw, not an image left by a browser that then failed.
    png.unlink(missing_ok=True)
    return status


def judge_bundle(bundle: Path, judge_agent: Agent, render: Renderer | None = None, again: bool = False) -> dict[str, object]:
    """Judge every task, rescore, and rewrite result.json and summary.md; raises ValueError, writing nothing,
    when the bundle is already judged (unless `again`), lacks evidence, or a task ends without a vote."""
    result = json.loads((bundle / RESULT_NAME).read_text(encoding="utf-8"))
    if isinstance(result.get("judge"), dict) and not again:
        raise ValueError(f"received {bundle.name} already judged by {result['judge'].get('model')}; expected a "
                         f"bundle without a judge")
    tasks = result["tasks"]
    packets = {str(task["id"]): read_packet(bundle, str(task["id"])) for task in tasks}
    judge = RubricJudge(judge_agent)
    verdicts: dict[str, TaskVerdict] = {}
    frames: dict[str, bytes | None] = {}
    with tempfile.TemporaryDirectory(prefix="mengine-bench-judge-") as tmp:
        for task_id, packet in packets.items():
            print(f"[{task_id}] judging", flush=True)
            workdir = Path(tmp) / task_id
            if packet.render is None:
                verdicts[task_id] = judge.grade(packet.context, workdir / "judge")
                continue
            verdicts[task_id] = _render_verdict(bundle, task_id, packet, judge, workdir,
                                                render or render_headless)
            for _, suffix, _ in JUDGE_FRAMES:
                shot = _frame_path(workdir, suffix)
                frames[f"{task_id}{suffix}.png"] = shot.read_bytes() if shot.is_file() else None
    missing = {task_id: verdict.errors[-1:] for task_id, verdict in verdicts.items() if verdict.score is None}
    if missing:
        raise ValueError(f"received no judge vote for {sorted(missing)} ({missing}); expected one vote per task, "
                         f"so nothing was written")
    for name, png in frames.items():
        # Unlinked first: --again must not leave the previous vote's frame, nor write through a link a PR committed.
        (bundle / JUDGE_DIR / name).unlink(missing_ok=True)
        if png is not None:
            (bundle / JUDGE_DIR / name).write_bytes(png)
    for task in tasks:
        verdict = verdicts[str(task["id"])]
        task.update(judge=verdict.score, judge_rationale=verdict.rationale, judge_errors=list(verdict.errors),
                    judge_parts=dict(verdict.parts))
    # The judge changes Judge and Score only: checks, Correct %, Time and Cost stay as the run published them.
    totals = result["totals"]
    totals["judge"] = judge_mean([verdicts[str(task["id"])].score for task in tasks])
    totals["speed"] = speed_points(float(totals["time_s"]))
    totals["score"] = combined_score(float(totals["correct"]), totals["judge"], totals["speed"])
    result["judge"] = {"agent": judge_agent.name, "model": judge_agent.model, "effort": judge_agent.effort,
                       "rubric": RUBRIC_VERSION, "bench": __version__,
                       "system_prompt_sha256": hashlib.sha256(JUDGE_SYSTEM_PROMPT.encode("utf-8")).hexdigest()}
    # Rationales and errors come from the maintainer's machine: redact them like the run's own text.
    scope = PathScope(names=local_names().allowing(result.get("submitter")))
    public = public_json(result, scope)
    assert isinstance(public, dict)
    result = public
    (bundle / RESULT_NAME).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
                                      newline="\n")
    (bundle / SUMMARY_NAME).write_text(public_text(render_summary(result), scope), encoding="utf-8", newline="\n")
    return result
