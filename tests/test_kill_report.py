"""Every process the runner kills is named in its output (mengine-qlora#42 / mengine-bench#264).

Agents of parallel runs still died with exit=15 (psutil kill) after the reused-pid fix, and nothing recorded who
killed what. _settle now prints pid, name and command line of each process before killing it.
"""

from __future__ import annotations

import subprocess
import sys

import psutil
import pytest

from mengine_bench.runner import containment


def test_settle_names_each_killed_process(capsys: pytest.CaptureFixture[str]) -> None:
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)  # kill-report-marker"])
    try:
        containment._settle([psutil.Process(child.pid)])
    finally:
        child.kill()
    out = capsys.readouterr().out
    assert f"pid={child.pid}" in out and "kill-report-marker" in out, f"received {out!r}; expected the killed pid named"
