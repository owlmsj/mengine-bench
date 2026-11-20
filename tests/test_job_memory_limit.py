"""A runaway agent process must not take the host's memory (mengine-qlora#42, 2026-11-20).

During collection one python started by a scale800 task grew to 18 GB of private memory on a 31 GB laptop; the
harness reaped every background job. MENGINE_BENCH_JOB_MEMORY_MB caps the whole Job, so the task's own allocation
fails instead.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from mengine_bench.runner.process import run_process

GRAB = "b = bytearray(1536 * 1024 * 1024); print('allocated', len(b))"


@pytest.mark.skipif(sys.platform != "win32", reason="Windows Job limit")
def test_the_job_memory_cap_stops_a_runaway_allocation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MENGINE_BENCH_JOB_MEMORY_MB", "512")
    result = run_process([sys.executable, "-c", GRAB], tmp_path, 60)
    assert result.exit_code != 0 and "allocated" not in result.stdout, (
        f"received exit {result.exit_code} and stdout {result.stdout!r}; expected the 1.5 GB allocation refused")


@pytest.mark.skipif(sys.platform != "win32", reason="Windows Job limit")
def test_without_the_cap_the_allocation_runs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MENGINE_BENCH_JOB_MEMORY_MB", raising=False)
    result = run_process([sys.executable, "-c", GRAB], tmp_path, 60)
    assert result.exit_code == 0 and "allocated" in result.stdout, f"received {result.exit_code} {result.stdout!r}"
