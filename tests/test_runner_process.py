"""Timeouts kill the whole agent process tree, grandchildren included."""

from __future__ import annotations

import sys
import time
from pathlib import Path

import psutil

from conftest import FakeAgent
from mengine_bench.runner.agents import CmdAgent
from mengine_bench.runner.process import run_process

SPAWNER = """
import subprocess, sys, time
from pathlib import Path
child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
Path(sys.argv[1], "grandchild.pid").write_text(str(child.pid))
time.sleep(120)
"""


def test_timeout_kills_child_and_grandchild(fake_agent: FakeAgent, tmp_path: Path) -> None:
    agent = CmdAgent(template=fake_agent("spawner", SPAWNER), model="m", effort=None)
    ws = tmp_path / "ws"
    ws.mkdir()
    call = agent.invocation("p", tmp_path / "p.md", ws, None, ())
    started = time.monotonic()
    result = run_process(call.argv, ws, timeout_s=3, stdin_text=call.stdin_text)
    assert result.timed_out and time.monotonic() - started < 30
    pid_file = ws / "grandchild.pid"
    assert pid_file.is_file(), "fake agent never spawned its grandchild"
    grandchild = int(pid_file.read_text())
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline and _alive(grandchild):
        time.sleep(0.1)
    assert not _alive(grandchild), "grandchild survived the timeout"


def test_completed_process_captures_output_and_exit(tmp_path: Path) -> None:
    # Agents speak UTF-8 on both pipes regardless of the host code page.
    code = ("import sys; data = sys.stdin.buffer.read().decode('utf-8'); "
            "sys.stdout.buffer.write(data.upper().encode('utf-8')); sys.stderr.write('warn'); sys.exit(3)")
    result = run_process([sys.executable, "-c", code], tmp_path, timeout_s=30, stdin_text="héllo")
    assert (result.stdout.strip(), result.stderr, result.exit_code, result.timed_out) == ("HÉLLO", "warn", 3, False)
    assert result.wall_s > 0


def _alive(pid: int) -> bool:
    try:
        return psutil.Process(pid).status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False
