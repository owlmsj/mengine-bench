"""What a task left running after it ended, found by parent links recorded during the task (#161).

The step's Job or session already ends what stayed inside it (`containment`). This catches what got out:
a process born during the task window whose recorded ancestry reaches this runner. A process that existed
before the task, or was born from one (the owner's browser opening a tab renderer, another session's build),
is never touched. A process whose parent died before it was observed has no known ancestry and is spared:
killing must never guess.
"""

from __future__ import annotations

import os
import threading
from dataclasses import dataclass

import psutil

OBSERVE_EVERY_S = 0.25
KILL_WAIT_S = 10
MAX_DEPTH = 64


@dataclass(frozen=True)
class LeftProcess:
    name: str
    pid: int

    def record(self) -> dict[str, object]:
        return {"name": self.name, "pid": self.pid}


def _started() -> dict[int, float]:
    known: dict[int, float] = {}
    for proc in psutil.process_iter(["create_time"]):
        created = proc.info["create_time"]
        if created is not None:
            known[proc.pid] = created
    return known


class TaskWindow:
    """Start before the task, `sweep` after its grading: kills and returns what the task left running."""

    def __init__(self, root_pid: int | None = None, every_s: float = OBSERVE_EVERY_S) -> None:
        self._root = os.getpid() if root_pid is None else root_pid
        self._before = _started()
        # pid -> (creation time, parent pid), recorded while the parent link still exists.
        self._born: dict[int, tuple[float, int]] = {}
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
        with self._lock:
            for pid, parent in rows.items():
                if pid in self._born or pid in self._before:
                    continue
                try:
                    created = psutil.Process(pid).create_time()
                except psutil.Error:
                    continue
                self._born[pid] = (created, parent)

    def _ours(self, pid: int, created: float) -> bool:
        """True when the recorded ancestry of `pid` reaches the runner through processes born in the window."""
        current, current_created = pid, created
        for _ in range(MAX_DEPTH):
            entry = self._born.get(current)
            if entry is None or entry[0] != current_created:
                return False
            parent = entry[1]
            if parent == self._root:
                return True
            if parent in self._before:
                return False
            parent_entry = self._born.get(parent)
            if parent_entry is None or parent_entry[0] > current_created:
                return False
            current, current_created = parent, parent_entry[0]
        return False

    def sweep(self) -> list[LeftProcess]:
        self._stop.set()
        self._thread.join()
        self._observe()
        left: list[psutil.Process] = []
        for proc in psutil.process_iter(["create_time"]):
            created = proc.info["create_time"]
            if proc.pid == self._root or created is None or self._before.get(proc.pid) == created:
                continue
            with self._lock:
                ours = self._ours(proc.pid, created)
            if ours:
                left.append(proc)
        found = []
        for proc in left:
            try:
                found.append(LeftProcess(proc.name(), proc.pid))
                proc.kill()
            except psutil.Error:
                continue
        psutil.wait_procs(left, timeout=KILL_WAIT_S)
        return found
