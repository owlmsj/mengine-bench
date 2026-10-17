"""Run one agent process with a hard timeout that takes its whole tree down.

Agent CLIs spawn shells, language servers and test runners; killing only the
direct child leaves those running (and holding files in the workspace), so the
timeout walks the tree with psutil while the parent is still alive.
Output goes to temp files, not pipes: a surviving grandchild holding an
inherited pipe would otherwise block the read forever.
"""

from __future__ import annotations

import subprocess
import tempfile
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

import psutil

KILL_WAIT_S = 10


@dataclass(frozen=True)
class ProcessResult:
    stdout: str
    stderr: str
    exit_code: int | None
    timed_out: bool
    wall_s: float


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


def run_process(argv: Sequence[str], cwd: Path, timeout_s: float, stdin_text: str | None = None,
                env: Mapping[str, str] | None = None) -> ProcessResult:
    if not argv:
        raise ValueError(f"received argv={list(argv)!r}; expected a non-empty argument list")
    payload = stdin_text.encode("utf-8") if stdin_text is not None else None
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        started = time.monotonic()
        proc = subprocess.Popen(list(argv), cwd=cwd, env=dict(env) if env is not None else None,
                                stdin=subprocess.PIPE if payload is not None else subprocess.DEVNULL,
                                stdout=out, stderr=err)
        timed_out = False
        try:
            proc.communicate(input=payload, timeout=timeout_s)
        except subprocess.TimeoutExpired:
            timed_out = True
            kill_tree(proc.pid)
            proc.wait()
        wall_s = time.monotonic() - started
        out.seek(0)
        err.seek(0)
        stdout = out.read().decode("utf-8", errors="replace")
        stderr = err.read().decode("utf-8", errors="replace")
    return ProcessResult(stdout=stdout, stderr=stderr, exit_code=None if timed_out else proc.returncode,
                         timed_out=timed_out, wall_s=wall_s)
