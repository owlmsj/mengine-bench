"""What a task left running after it ended, found by parent links recorded during the task (#161).

The step's Job or session already ends what stayed inside it (`containment`). This catches what got out:
a process born during the task window whose recorded ancestry reaches this runner. A process that existed
before the task, or was born from one (the owner's browser opening a tab renderer, another session's build),
is never touched. A process whose parent died before it was observed has no known ancestry and is spared:
killing must never guess.

#177: the harness itself (Claude Code, its Git Bash wrapper) also starts helpers under the runner, such as a
`sleep.exe` the agent never asked for. Everything found is killed, but only a process the agent named in one of its
shell commands (`attribute`) counts against it; the rest is a note.
"""

from __future__ import annotations

import os
import re
import threading
from collections.abc import Sequence
from dataclasses import dataclass

import psutil

OBSERVE_EVERY_S = 0.25
KILL_WAIT_S = 10


@dataclass(frozen=True)
class LeftProcess:
    name: str
    pid: int
    # Joined psutil cmdline, "" when access is denied; kept in memory only, since a command line can hold secrets.
    cmdline: str = ""
    # True until run_task resolves it with `attribute`: an unresolved leftover keeps the 2.4 rule and counts.
    attributed: bool = True

    def record(self) -> dict[str, object]:
        return {"name": self.name, "pid": self.pid}


def attribute(left: LeftProcess, agent_commands: Sequence[str]) -> bool:
    """#177: True when the executable's base name (no `.exe`, any case) is a word in one of the agent's commands."""
    base = re.split(r"[\\/]", left.name)[-1].lower().removesuffix(".exe")
    if not base:
        return False
    word = re.compile(rf"(?<![\w.-]){re.escape(base)}(?:\.exe)?(?![\w-])", re.IGNORECASE)
    return any(word.search(command) for command in agent_commands)


def _started() -> dict[int, float]:
    known: dict[int, float] = {}
    for proc in psutil.process_iter(["create_time"]):
        created = proc.info["create_time"]
        if created is not None:
            known[proc.pid] = created
    return known


def _create_time(pid: int) -> float | None:
    try:
        return psutil.Process(pid).create_time()
    except psutil.Error:
        return None


class TaskWindow:
    """Start before the task, `sweep` after its grading: kills and returns what the task left running."""

    def __init__(self, root_pid: int | None = None, every_s: float = OBSERVE_EVERY_S) -> None:
        self._root = os.getpid() if root_pid is None else root_pid
        before = _started()
        self._before: set[tuple[int, float]] = set(before.items())
        # Live processes known to be ours (root included), revalidated by create_time every tick (#313).
        self._active: dict[int, float] = {self._root: before[self._root]} if self._root in before else {}
        # (pid, create_time) pairs decided as ours at observation time; never dropped, so a leftover stays ours
        # even after its parent exits and its pid is reused (#313, advisor review).
        self._owned: set[tuple[int, float]] = set()
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._every_s = every_s
        self._thread = threading.Thread(target=self._watch, name="bench-task-window", daemon=True)
        self._thread.start()

    def _watch(self) -> None:
        while not self._stop.wait(self._every_s):
            self._observe()

    def _observe(self) -> None:
        # One snapshot for all rows; Process.ppid() would take one per process on Windows.
        rows = psutil._ppid_map()
        kids: dict[int, list[int]] = {}
        for pid, parent in rows.items():
            kids.setdefault(parent, []).append(pid)
        with self._lock:
            nxt: dict[int, float] = {}
            queue: list[tuple[int, float, float | None]] = []
            for pid, created in self._active.items():
                current = _create_time(pid) if pid in rows else None
                if current == created:
                    nxt[pid] = created
                # A dead parent (current is None) may still have children born in this tick; a reused parent
                # (current != created) only accepts children born before the reuse timestamp.
                queue.append((pid, created, None if current == created else current))
            while queue:
                ppid, p_created, replaced_at = queue.pop()
                for child in kids.get(ppid, ()):
                    if child in nxt:
                        continue
                    c_created = _create_time(child)
                    if c_created is None or (child, c_created) in self._before or c_created < p_created:
                        continue
                    if replaced_at is not None and c_created >= replaced_at:
                        continue
                    self._owned.add((child, c_created))
                    nxt[child] = c_created
                    queue.append((child, c_created, None))
            self._active = nxt

    def _ours(self, pid: int, created: float) -> bool:
        """True when `(pid, created)` was decided as ours while its parent was still active."""
        return (pid, created) in self._owned

    def sweep(self) -> list[LeftProcess]:
        self._stop.set()
        self._thread.join()
        self._observe()
        left: list[psutil.Process] = []
        for proc in psutil.process_iter(["create_time"]):
            created = proc.info["create_time"]
            if proc.pid == self._root or created is None or (proc.pid, created) in self._before:
                continue
            with self._lock:
                ours = self._ours(proc.pid, created)
            if ours:
                left.append(proc)
        found = []
        for proc in left:
            try:
                found.append(LeftProcess(proc.name(), proc.pid, _cmdline(proc)))
                proc.kill()
            except psutil.Error:
                continue
        psutil.wait_procs(left, timeout=KILL_WAIT_S)
        return found


def _cmdline(proc: psutil.Process) -> str:
    try:
        return " ".join(proc.cmdline())
    except psutil.Error:
        return ""
