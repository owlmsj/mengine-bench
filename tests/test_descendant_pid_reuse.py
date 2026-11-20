"""DescendantWatch must not adopt a stranger through a parent pid that was reused (mengine-qlora#42, 2026-11-20).

Collection with several runners in parallel saw agents end with exit=15 (psutil's kill on Windows) and no error
of their own. _observe adopted any child of a pid still in `_born` and pruned dead or reused pids only afterwards,
so a stranger whose parent reused a tracked pid joined this run's descendants and was killed at kill_all.
"""

from __future__ import annotations

import threading

import pytest

from mengine_bench.runner import containment
from mengine_bench.runner.containment import DescendantWatch

ROOT, CHILD, STRANGER, ORPHAN = 100, 200, 300, 201
CREATED = {ROOT: 10.0, CHILD: 50.0, STRANGER: 60.0, ORPHAN: 30.0}  # CHILD's pid now belongs to a process born at 50


def test_a_reused_parent_pid_adopts_no_stranger(monkeypatch: pytest.MonkeyPatch) -> None:
    watch = DescendantWatch.__new__(DescendantWatch)
    # CHILD (born at 20) was ours; it died and its pid was reused by an unrelated process born at 50.
    watch._lock, watch._stop, watch._born = threading.Lock(), threading.Event(), {ROOT: 10.0, CHILD: 20.0}
    monkeypatch.setattr(containment.psutil, "_ppid_map", lambda: {ROOT: 1, CHILD: 7, STRANGER: CHILD})
    monkeypatch.setattr(DescendantWatch, "_created", staticmethod(lambda pid: CREATED.get(pid)))
    watch._observe()
    assert STRANGER not in watch._born, f"received {watch._born}; expected no stranger adopted through a reused pid"


def test_an_orphan_of_a_dead_parent_is_still_adopted(monkeypatch: pytest.MonkeyPatch) -> None:
    watch = DescendantWatch.__new__(DescendantWatch)
    watch._lock, watch._stop, watch._born = threading.Lock(), threading.Event(), {ROOT: 10.0, CHILD: 20.0}
    monkeypatch.setattr(containment.psutil, "_ppid_map", lambda: {ROOT: 1, ORPHAN: CHILD})
    # CHILD exited (no process holds its pid); its child ORPHAN, born at 30, is still ours.
    monkeypatch.setattr(DescendantWatch, "_created", staticmethod(lambda pid: None if pid == CHILD else CREATED.get(pid)))
    watch._observe()
    assert ORPHAN in watch._born, f"received {watch._born}; expected the dead parent's child adopted"
