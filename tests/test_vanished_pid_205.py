"""A process that exits between two psutil calls must not crash the task (#205).

web-word-universe crashed with "post-processing failed: NoSuchProcess: process PID
not found (pid=2592)": DescendantWatch saw the pid alive, then psutil.Process(pid)
found it gone. These tests make that race deterministic with monkeypatch.
"""

from __future__ import annotations

import threading
from pathlib import Path

import psutil
import pytest

from mengine_bench.runner import containment
from mengine_bench.runner.containment import DescendantWatch, PosixSession, sweep_workspace

VANISHED = 2592


def _vanished_process(pid: int | None = None) -> psutil.Process:
    raise psutil.NoSuchProcess(VANISHED if pid is None else pid)


def test_kill_all_tolerates_a_pid_that_exits_after_it_was_seen(monkeypatch: pytest.MonkeyPatch) -> None:
    watch = DescendantWatch.__new__(DescendantWatch)
    watch._lock, watch._stop, watch._born = threading.Lock(), threading.Event(), {VANISHED: 1.0}
    monkeypatch.setattr(DescendantWatch, "_observe", lambda self: None)
    # Alive at the check, gone when the Process is built: the #205 window.
    monkeypatch.setattr(DescendantWatch, "_created", staticmethod(lambda pid: 1.0))
    monkeypatch.setattr(containment.psutil, "Process", _vanished_process)
    assert watch.kill_all() == 0


class _OrphanedRunner:
    """This runner, whose parent chain loses a member while it is walked."""

    pid = 4242

    def parent(self) -> psutil.Process:
        raise psutil.NoSuchProcess(VANISHED)

    def parents(self) -> list[psutil.Process]:
        raise psutil.NoSuchProcess(VANISHED)


def test_sweep_tolerates_an_ancestor_that_exits_during_the_walk(tmp_path: Path,
                                                               monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(containment.psutil, "Process", lambda pid=None: _OrphanedRunner())
    monkeypatch.setattr(containment.psutil, "process_iter", lambda attrs=None: iter(()))
    assert sweep_workspace(tmp_path / "ws") == 0


class _ExitingMember:
    pid = VANISHED

    def status(self) -> str:
        raise psutil.NoSuchProcess(VANISHED)


def test_posix_session_tolerates_a_member_that_exits_before_its_status(monkeypatch: pytest.MonkeyPatch) -> None:
    session = PosixSession()
    session._sid = 7
    monkeypatch.setattr(containment.psutil, "process_iter", lambda: iter([_ExitingMember()]))
    monkeypatch.setattr(containment.os, "getsid", lambda pid: 7, raising=False)
    assert session.kill_all(root_pid=1) == 0
