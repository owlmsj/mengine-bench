"""Run one agent process with a hard timeout, and leave nothing of it behind.

Agent CLIs spawn shells, language servers, test runners and browsers; any of
them can outlive the agent (and hold files in the workspace), so every exit path
kills all that the run started: see `containment`.
Output goes to temp files, not pipes: a surviving grandchild holding an
inherited pipe would otherwise block the read forever.
"""

from __future__ import annotations

import subprocess
import tempfile
import threading
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

import psutil

from mengine_bench.runner.containment import new_scope, stop_session_group, sweep_workspace

KILL_WAIT_S = 10
WATCH_EVERY_S = 0.2
# Long enough for a normal exit (1 to 3 s measured for `codex exec`), short enough to cost nothing: the clock has stopped.
FINAL_EVENT_GRACE_S = 5


@dataclass(frozen=True)
class ProcessResult:
    stdout: str
    stderr: str
    exit_code: int | None
    timed_out: bool
    wall_s: float
    # Processes the agent left behind and the runner killed.
    reaped: int = 0
    # The agent reported its final event, then did not exit, and the runner ended it (#85).
    stopped_after_final: bool = False


def kill_tree(pid: int) -> None:
    try:
        root = psutil.Process(pid)
        family = [*root.children(recursive=True), root]
    except psutil.NoSuchProcess:
        return
    for member in family:
        try:
            member.kill()
        except psutil.NoSuchProcess:
            continue
    psutil.wait_procs(family, timeout=KILL_WAIT_S)


class _FinalEventWatch(threading.Thread):
    """Ends the step when the agent says it is done (#85).

    `codex exec` gave its final reply at 128 s and was still alive when the 480 s limit killed it,
    so finished work counted as a timeout. A line must start with the event: inside a message its
    quotes are escaped and the newline before it is not a newline.
    """

    def __init__(self, proc: subprocess.Popen[bytes], output: Path, final_event: str | None) -> None:
        super().__init__(daemon=True)
        self._proc, self._output, self._final_event = proc, output, final_event
        self._closed = threading.Event()
        self.finished_at: float | None = None
        self.stopped = False

    def run(self) -> None:
        if self._final_event is None or not self._saw_final_event(self._final_event):
            return
        self.finished_at = time.monotonic()
        if not self._closed.wait(FINAL_EVENT_GRACE_S):
            self.stopped = True
            kill_tree(self._proc.pid)

    def _saw_final_event(self, final_event: str) -> bool:
        needle = b"\n" + final_event.encode("utf-8")
        seen = b"\n"
        with self._output.open("rb") as reader:
            while not self._closed.wait(WATCH_EVERY_S):
                seen = seen[-len(needle):] + reader.read()
                if needle in seen:
                    return True
        return False

    def close(self) -> None:
        self._closed.set()
        self.join()


def run_process(argv: Sequence[str], cwd: Path, timeout_s: float, stdin_text: str | None = None,
                env: Mapping[str, str] | None = None, final_event: str | None = None) -> ProcessResult:
    if not argv:
        raise ValueError(f"received argv={list(argv)!r}; expected a non-empty argument list")
    payload = stdin_text.encode("utf-8") if stdin_text is not None else None
    scope = new_scope()
    reaped = 0
    # Named files, so the watch reads with its own position: an inherited handle shares the agent's.
    with tempfile.TemporaryDirectory(prefix="mengine-bench-output-", ignore_cleanup_errors=True) as output_dir:
        out_path, err_path = Path(output_dir) / "stdout", Path(output_dir) / "stderr"
        with out_path.open("wb") as out, err_path.open("wb") as err:
            started = time.monotonic()
            try:
                proc = subprocess.Popen(list(argv), cwd=cwd, env=dict(env) if env is not None else None,
                                        stdin=subprocess.PIPE if payload is not None else subprocess.DEVNULL,
                                        stdout=out, stderr=err, **scope.popen_kwargs)
                scope.adopt(proc)
                watch = _FinalEventWatch(proc, out_path, final_event)
                watch.start()
                timed_out = False
                try:
                    proc.communicate(input=payload, timeout=timeout_s)
                except subprocess.TimeoutExpired:
                    timed_out = True
                    kill_tree(proc.pid)
                    proc.wait()
                ended = time.monotonic()
                watch.close()
                stop_session_group(proc.pid)
                reaped += scope.kill_all(proc.pid)
            finally:
                scope.close()
            reaped += sweep_workspace(cwd)
        stdout = out_path.read_bytes().decode("utf-8", errors="replace")
        stderr = err_path.read_bytes().decode("utf-8", errors="replace")
    finished = watch.finished_at is not None
    stopped = watch.stopped or (timed_out and finished)
    timed_out = timed_out and not finished
    # The clock stops at the final event: shutting down is not work, and the time to exit varies by configuration.
    wall_s = (watch.finished_at if watch.finished_at is not None else ended) - started
    exit_code = None if timed_out else 0 if stopped else proc.returncode
    return ProcessResult(stdout=stdout, stderr=stderr, exit_code=exit_code, timed_out=timed_out, wall_s=wall_s,
                         reaped=reaped, stopped_after_final=stopped)
