"""Run one task through an agent: fixture, steps, per-step timeout, then gold.

Step semantics (core.Step), ported from the private suite's runner:
- the first step runs in `step-0/` after `setup`;
- `fresh_session` starts a new agent process with no chat history in a NEW
  workspace that holds only the step's `carry` files (release review R19).
  That workspace lives under its own system-temp root, so no earlier step is
  a parent or sibling of it; once the task ends it moves to `step-<i>/` under
  the run root for grading and bundling. Files are reachable only by an
  absolute path outside the workspace, which AGENTS.md forbids;
- no step resumes a session (core.EvalTask rejects it, #23), so every
  adapter, `cmd` included, runs every task;
- `hide` moves paths out of the workspace before the turn; `inline` pastes
  files into the prompt; `attach` names images (and passes them natively when
  the CLI supports attachments).
The gold check runs once, after the last step, on the final workspace.
"""

from __future__ import annotations

import os
import shutil
import tempfile
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from mengine_bench.core import CheckResult, EvalTask
from mengine_bench.runner import process
from mengine_bench.runner.agents import Agent, AgentError, Usage, sum_usage, partial_answer
from mengine_bench.runner.stats import RunStats, merge_stats, stream_stats
from mengine_bench.visual import add_page_checks

# Browser user-data dirs an agent left in the workspace; their cache files can
# stay locked by a live browser, and they are never part of the solution.
BROWSER_PROFILE_DIRS = frozenset({"_browser-profile", ".browser-profile", "browser-profile", ".verify-profile",
                                  "verify-profile", ".chrome-profile", "chrome-profile", ".edge-profile",
                                  "edge-profile", "user-data-dir", ".user-data-dir"})

# The agent under test is harness + model as configured: every tool, MCP
# server, skill or subagent it has is fair game. Local files outside the
# workspace are not: earlier steps and runs live next to it, and the
# transcripts are published.
WORKSPACE_RULES = ("Use any skill, tool or MCP server you have. Read and write local files only inside this directory.\n"
                   "Do not print credentials, environment variables or personal data: this session is published.\n")
# #41: without this a model can plan until the limit and leave nothing to grade.
TIME_LIMIT_NOTE = ("\n\nYou have {minutes} min for this step. The folder and your reply so far are graded as they stand "
                   "when time runs out, so deliver a first complete version early. Time counts in your grade: finish as soon as the work "
                   "is right, with at most 2 rounds of revision after that first version.")
# #85: in every prompt too, for an agent that does not load AGENTS.md (AGY --print).
ANY_TOOL_NOTE = ("\n\nYou may use any skill, tool or MCP server available to you whenever it makes your work smarter, "
                 "more correct or faster.")
# #98: the route is open, so nothing here says how. Asking how they know it is right is the brief's last question.
BRIEF_NOTE = ("\n\nThis is the whole brief: there is no second turn and nobody can answer questions. Choose your own "
              "approach, decide what the brief leaves open and state your assumptions. End by saying what you found "
              "and how you know it is right.")
COPY_IGNORE = shutil.ignore_patterns(".git", "tmp", "__pycache__", "_render")


@dataclass(frozen=True)
class StepRecord:
    index: int
    wall_s: float
    exit_code: int | None
    status: str
    error: str | None = None
    # Failed steps remain unmeasured because incomplete streams cannot establish usage (#23).
    usage: Usage | None = None
    # From the stream, so a step stopped at its limit still has them (#39).
    stats: RunStats = field(default_factory=RunStats)


@dataclass
class TaskRunRecord:
    task_id: str
    status: str = "ok"
    steps: list[StepRecord] = field(default_factory=list)
    answers: list[str] = field(default_factory=list)
    error: str | None = None
    check: CheckResult | None = None
    grading_s: float = 0.0
    workspace: Path | None = None
    initial_files: dict[str, bytes] = field(default_factory=dict)
    # Published next to the status: what the runner had to do, never a grade.
    notes: list[str] = field(default_factory=list)
    # Raw stdout of each step, for the checkpoints. Not published from here: the transcripts are, after redaction.
    streams: list[str] = field(default_factory=list)

    @property
    def usage(self) -> Usage | None:
        return sum_usage([step.usage for step in self.steps if step.usage is not None])

    @property
    def stats(self) -> RunStats:
        return merge_stats(step.stats for step in self.steps)

    @property
    def agent_s(self) -> float:
        return sum(step.wall_s for step in self.steps)


class StepFailed(Exception):
    def __init__(self, status: str, message: str) -> None:
        super().__init__(message)
        self.status = status


def render_prompt(task: EvalTask, index: int, workspace: Path, hidden: Path) -> str:
    step = task.steps[index]
    text = step.prompt.replace("{WS}", ".")
    for relative in step.inline:
        body = (workspace / relative).read_text(encoding="utf-8")
        text += f'\n<document name="{Path(relative).name}">\n{body}\n</document>\n'
    for relative in step.hide:
        source = workspace / relative
        if source.exists():
            target = hidden / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), target)
    for relative in step.attach:
        if not (workspace / relative).is_file():
            raise ValueError(f"task {task.id!r} received absent attachment {relative!r}; expected a fixture file")
        text += f"\nInspect the image visually with your image reader: ./{relative}\n"
    return text


def snapshot(workspace: Path) -> dict[str, bytes]:
    """Readable workspace files; unreadable (locked) ones, browser profiles and cargo output are skipped."""
    files: dict[str, bytes] = {}
    for path in sorted(workspace.rglob("*")):
        rel = path.relative_to(workspace)
        if any(part in BROWSER_PROFILE_DIRS or part in ("__pycache__", "target") for part in rel.parts) or not path.is_file():
            continue
        try:
            files[rel.as_posix()] = path.read_bytes()
        except OSError:
            continue
    return files


def run_task(task: EvalTask, agent: Agent, root: Path, fresh_root: Path | None = None) -> TaskRunRecord:
    """`fresh_root` hosts fresh-session workspaces (default: system temp)."""
    root.mkdir(parents=True, exist_ok=False)
    # #59: alone in a temp root. Next to prompts and transcripts, in a folder named step-0 under the task id, three
    # runs delivered to `../` and the document an answer-only task hides stayed one `..` away.
    workspace = _isolated_workspace(fresh_root)
    task.setup(workspace)
    initial_files = {**snapshot(workspace), "AGENTS.md": WORKSPACE_RULES.encode("utf-8")}
    record = TaskRunRecord(task_id=task.id, initial_files=initial_files)
    workspace_index = 0
    for index, step in enumerate(task.steps):
        try:
            if index:
                fresh = fresh_workspace(workspace, step.carry, fresh_root)
                settle_workspace(workspace, root, workspace_index)
                workspace, workspace_index = fresh, index
            prompt = render_prompt(task, index, workspace, root / "hidden" / str(index))
            prompt += BRIEF_NOTE + ANY_TOOL_NOTE + TIME_LIMIT_NOTE.format(minutes=f"{task.timeout_s / 60:g}")
            (workspace / "AGENTS.md").write_text(WORKSPACE_RULES, encoding="utf-8", newline="")
            _run_step(agent, task, workspace, root, index, prompt, record)
        except StepFailed as failure:
            record.status, record.error = failure.status, str(failure)
            break
        except (ValueError, OSError) as error:
            record.status, record.error = "crash", str(error)
            break
    record.workspace = settle_workspace(workspace, root, workspace_index)
    _grade(task, record)
    return record


def _isolated_workspace(fresh_root: Path | None) -> Path:
    workspace = Path(tempfile.mkdtemp(prefix="mengine-bench-fresh-", dir=fresh_root)) / "workspace"
    workspace.mkdir()
    return workspace


def fresh_workspace(previous: Path, carry: tuple[str, ...], fresh_root: Path | None) -> Path:
    """New workspace holding only `carry` from `previous`, under its own temp root.

    A carried path the agent never wrote is skipped: the next step then fails
    on its own merits instead of the runner crashing.
    """
    target = _isolated_workspace(fresh_root)
    for relative in carry:
        source = previous / relative
        dest = target / relative
        if source.is_dir():
            shutil.copytree(source, dest, ignore=COPY_IGNORE)
        elif source.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
    return target


def settle_workspace(workspace: Path, root: Path, index: int) -> Path:
    """Move an isolated fresh workspace back under the run root as `step-<index>`."""
    if workspace.resolve().is_relative_to(root.resolve()):
        return workspace
    dest = root / f"step-{index}"
    shutil.move(str(workspace), str(dest))
    shutil.rmtree(workspace.parent, ignore_errors=True)
    return dest


def _run_step(agent: Agent, task: EvalTask, workspace: Path, root: Path, index: int, prompt: str,
              record: TaskRunRecord) -> None:
    step = task.steps[index]
    record.answers.append(_invoke(agent, task, workspace, root, index, prompt, record, step.attach))


def _step_env(workspace: Path, extra: Mapping[str, str] | None) -> dict[str, str]:
    """Caller env plus PWD=<workspace>: opencode 2.0.29 trusts PWD over the process cwd
    (cli/src/run/run.ts:73), and Popen(cwd=...) does not update PWD."""
    # #59: bytecode took 16,463 of the 19,198 characters a judge saw, and the suites the prompts ask for write it.
    env = {**os.environ, "PWD": str(workspace.resolve()), "PYTHONDONTWRITEBYTECODE": "1", **(extra or {})}
    # #95: a benchmark step must not inherit the launching Claude session.
    for key in (
        "CLAUDECODE", "CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_SESSION_ID", "CLAUDE_PID",
        "CLAUDE_EFFORT", "CLAUDE_CODE_MESSAGING_SOCKET", "CLAUDE_CODE_BRIDGE_SESSION_ID",
        "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_EXECPATH",
        "CLAUDE_CODE_MESSAGING_TOKEN",
    ):
        env.pop(key, None)
    return env


def _invoke(agent: Agent, task: EvalTask, workspace: Path, root: Path, index: int, prompt: str,
            record: TaskRunRecord, attachments: tuple[str, ...]) -> str:
    label = str(index)
    prompts = root / "prompts"
    transcripts = root / "transcripts"
    prompts.mkdir(exist_ok=True)
    transcripts.mkdir(exist_ok=True)
    prompt_file = prompts / f"step-{label}.md"
    prompt_file.write_text(prompt, encoding="utf-8")
    call = agent.invocation(prompt, prompt_file.resolve(), workspace.resolve(), attachments)
    try:
        result = process.run_process(call.argv, workspace, task.timeout_s, stdin_text=call.stdin_text,
                                     env=_step_env(workspace, call.env), final_event=call.final_event)
    except OSError as error:
        record.steps.append(StepRecord(index, 0.0, None, "crash", str(error)))
        raise StepFailed("crash", f"could not start agent {call.argv[0]!r}: {error}") from error
    if result.reaped:
        print(f"[{task.id}] step {label}: killed {result.reaped} process(es) the agent left running", flush=True)
    if result.stopped_after_final:
        print(f"[{task.id}] step {label}: the agent reported its final event but did not exit; stopped it", flush=True)
        record.notes.append("stopped after its final event")
    (transcripts / f"step-{label}.stdout.txt").write_text(result.stdout, encoding="utf-8")
    (transcripts / f"step-{label}.stderr.txt").write_text(result.stderr, encoding="utf-8")
    stats = stream_stats(result.stdout)
    record.streams.append(result.stdout)
    if result.timed_out:
        message = f"step {label} exceeded the {task.timeout_s}s timeout"
        # #59: a reply already given counts, or an answer-only task would zero at the limit.
        reply = partial_answer(result.stdout)
        if reply:
            record.answers.append(reply)
        record.steps.append(StepRecord(index, result.wall_s, None, "timeout", message, stats=stats))
        raise StepFailed("timeout", message)
    try:
        parsed = agent.parse(result.stdout, result.exit_code or 0)
    except AgentError as error:
        # #70: as at a timeout, a reply already given counts.
        reply = partial_answer(result.stdout)
        if reply:
            record.answers.append(reply)
        record.steps.append(StepRecord(index, result.wall_s, result.exit_code, "crash", str(error), stats=stats))
        raise StepFailed("crash", f"step {label}: {error}") from error
    record.steps.append(StepRecord(index, result.wall_s, result.exit_code, "ok", usage=parsed.usage, stats=stats))
    return parsed.answer


def _grade(task: EvalTask, record: TaskRunRecord) -> None:
    assert record.workspace is not None
    started = time.monotonic()
    answers = record.answers + [""] * (len(task.steps) - len(record.answers))
    try:
        record.check = task.check(record.workspace, answers)
        if task.render_target is not None:
            add_page_checks(record.check, record.workspace / task.render_target)
    except (ValueError, RuntimeError, OSError) as error:
        record.error = f"{record.error or ''} grading failed: {error}".strip()
        record.status = "crash"
    record.grading_s = time.monotonic() - started
