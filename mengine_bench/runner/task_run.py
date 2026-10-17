"""Run one task through an agent: fixture, steps, per-step timeout, then gold.

Step semantics (core.Step), ported from the private suite's runner:
- the first step runs in `step-0/` after `setup`;
- `fresh_session` starts a new agent process with no chat history in a NEW
  workspace that holds only the step's `carry` files (release review R19).
  That workspace lives under its own system-temp root, so no earlier step is
  a parent or sibling of it; once the task ends it moves to `step-<i>/` under
  the run root for grading and bundling. Files are reachable only by an
  absolute path outside the workspace, which AGENTS.md forbids;
- a task's final check is wrapped in the visual grading profile
  (visual.enforce_rendered_profile): an unrendered visual task is not solved;
- otherwise the step continues the previous session through the adapter's
  resume feature; an adapter without one makes the task "unsupported";
- `compact_before` asks the harness to compact the resumed session first
  (Claude Code `/compact`); adapters that cannot do it make it "unsupported";
- `hide` moves paths out of the workspace before the turn; `inline` pastes
  files into the prompt; `attach` names images (and passes them natively when
  the CLI supports attachments).
The gold check runs once, after the last step, on the final workspace.
"""

from __future__ import annotations

import shutil
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

from mengine_bench import visual
from mengine_bench.bundle import BROWSER_PROFILE_DIRS
from mengine_bench.core import CheckResult, EvalTask
from mengine_bench.runner import process
from mengine_bench.runner.agents import Agent, AgentError

WORKSPACE_RULES = "Work only in this directory. Do not use credentials or billable resources.\n"
COPY_IGNORE = shutil.ignore_patterns(".git", "tmp", "__pycache__", "_render")


@dataclass(frozen=True)
class StepRecord:
    index: int
    wall_s: float
    exit_code: int | None
    status: str
    error: str | None = None


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
    """Readable workspace files; unreadable (locked) ones and browser profiles are skipped."""
    files: dict[str, bytes] = {}
    for path in sorted(workspace.rglob("*")):
        rel = path.relative_to(workspace)
        if any(part in BROWSER_PROFILE_DIRS for part in rel.parts) or not path.is_file():
            continue
        try:
            files[rel.as_posix()] = path.read_bytes()
        except OSError:
            continue
    return files


def run_task(task: EvalTask, agent: Agent, root: Path, fresh_root: Path | None = None) -> TaskRunRecord:
    """`fresh_root` hosts fresh-session workspaces (default: system temp)."""
    root.mkdir(parents=True, exist_ok=False)
    workspace = root / "step-0"
    workspace.mkdir()
    task.setup(workspace)
    record = TaskRunRecord(task_id=task.id, initial_files=snapshot(workspace))
    session: str | None = None
    workspace_index = 0
    for index, step in enumerate(task.steps):
        try:
            if index and step.fresh_session:
                fresh = fresh_workspace(workspace, step.carry, fresh_root)
                settle_workspace(workspace, root, workspace_index)
                workspace, session, workspace_index = fresh, None, index
            elif index:
                _require_continuation(agent, session, task.id)
                if step.compact_before:
                    _compact(agent, task, workspace, root, index, session, record)
            prompt = render_prompt(task, index, workspace, root / "hidden" / str(index))
            (workspace / "AGENTS.md").write_text(WORKSPACE_RULES, encoding="utf-8")
            session = _run_step(agent, task, workspace, root, index, prompt, session, record)
        except StepFailed as failure:
            record.status, record.error = failure.status, str(failure)
            break
        except (ValueError, OSError) as error:
            record.status, record.error = "crash", str(error)
            break
    record.workspace = settle_workspace(workspace, root, workspace_index)
    _grade(task, record)
    return record


def fresh_workspace(previous: Path, carry: tuple[str, ...], fresh_root: Path | None) -> Path:
    """New workspace holding only `carry` from `previous`, under its own temp root.

    A carried path the agent never wrote is skipped: the next step then fails
    on its own merits instead of the runner crashing.
    """
    base = Path(tempfile.mkdtemp(prefix="mengine-bench-fresh-", dir=fresh_root))
    target = base / "workspace"
    target.mkdir()
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


def _require_continuation(agent: Agent, session: str | None, task_id: str) -> None:
    if not agent.supports_resume:
        raise StepFailed("unsupported", f"task {task_id!r} continues a session; agent {agent.name!r} cannot resume")
    if session is None:
        raise StepFailed("crash", f"task {task_id!r} continues a session; agent {agent.name!r} reported no session id")


def _compact(agent: Agent, task: EvalTask, workspace: Path, root: Path, index: int, session: str | None,
             record: TaskRunRecord) -> None:
    if not agent.supports_compact:
        raise StepFailed("unsupported", f"task {task.id!r} needs compaction; agent {agent.name!r} cannot compact")
    # Compaction time is agent time; its reply is not an answer to the task.
    _invoke(agent, task, workspace, root, f"{index}-compact", agent.compact_prompt, session, record, (), index)


def _run_step(agent: Agent, task: EvalTask, workspace: Path, root: Path, index: int, prompt: str,
              session: str | None, record: TaskRunRecord) -> str | None:
    step = task.steps[index]
    answer, new_session = _invoke(agent, task, workspace, root, str(index), prompt, session, record,
                                  step.attach, index)
    record.answers.append(answer)
    return new_session or session


def _invoke(agent: Agent, task: EvalTask, workspace: Path, root: Path, label: str, prompt: str,
            session: str | None, record: TaskRunRecord, attachments: tuple[str, ...],
            index: int) -> tuple[str, str | None]:
    prompts = root / "prompts"
    transcripts = root / "transcripts"
    prompts.mkdir(exist_ok=True)
    transcripts.mkdir(exist_ok=True)
    prompt_file = prompts / f"step-{label}.md"
    prompt_file.write_text(prompt, encoding="utf-8")
    call = agent.invocation(prompt, prompt_file.resolve(), workspace.resolve(), session, attachments)
    try:
        result = process.run_process(call.argv, workspace, task.timeout_s, stdin_text=call.stdin_text)
    except OSError as error:
        record.steps.append(StepRecord(index, 0.0, None, "crash", str(error)))
        raise StepFailed("crash", f"could not start agent {call.argv[0]!r}: {error}") from error
    (transcripts / f"step-{label}.stdout.txt").write_text(result.stdout, encoding="utf-8")
    (transcripts / f"step-{label}.stderr.txt").write_text(result.stderr, encoding="utf-8")
    if result.timed_out:
        message = f"step {label} exceeded the {task.timeout_s}s timeout"
        record.steps.append(StepRecord(index, result.wall_s, None, "timeout", message))
        raise StepFailed("timeout", message)
    try:
        parsed = agent.parse(result.stdout, result.exit_code or 0)
    except AgentError as error:
        record.steps.append(StepRecord(index, result.wall_s, result.exit_code, "crash", str(error)))
        raise StepFailed("crash", f"step {label}: {error}") from error
    record.steps.append(StepRecord(index, result.wall_s, result.exit_code, "ok"))
    return parsed.answer, parsed.session_id


def _grade(task: EvalTask, record: TaskRunRecord) -> None:
    assert record.workspace is not None
    started = time.monotonic()
    answers = record.answers + [""] * (len(task.steps) - len(record.answers))
    try:
        record.check = task.check(record.workspace, answers)
        visual.enforce_rendered_profile(record.check)
    except (ValueError, RuntimeError, OSError) as error:
        record.error = f"{record.error or ''} grading failed: {error}".strip()
        record.status = "crash"
    record.grading_s = time.monotonic() - started
