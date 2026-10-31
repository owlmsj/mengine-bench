"""No process outlives a run, on any exit path (owlmsj/mengine#785, mengine-bench#31)."""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

import psutil
import pytest

from mengine_bench.runner.process import run_process

SLEEP = "import time; time.sleep(120)"
# A detached process has no live parent link: only containment can find it.
DETACHED = """
import subprocess, sys
from pathlib import Path
flags = {"creationflags": 0x00000008 | 0x00000200} if sys.platform == "win32" else {"start_new_session": True}
child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"], stdin=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **flags)
Path(sys.argv[1], "detached.pid").write_text(str(child.pid))
"""
LAUNCHER_THEN_WAIT = """
import subprocess, sys, time
subprocess.run([sys.executable, sys.argv[2], sys.argv[1]], check=True)
time.sleep(120)
"""


def _alive(pid: int) -> bool:
    try:
        return psutil.Process(pid).status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False


def _gone(pid: int) -> bool:
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline and _alive(pid):
        time.sleep(0.1)
    return not _alive(pid)


def _kill_leftover(pid: int) -> None:
    # A failing assertion must not leave the sleeper behind for two minutes.
    try:
        psutil.Process(pid).kill()
    except psutil.NoSuchProcess:
        pass


@pytest.fixture
def ws(tmp_path: Path) -> Path:
    path = tmp_path / "ws"
    path.mkdir()
    return path


@pytest.fixture
def detached_script(tmp_path: Path) -> Path:
    script = tmp_path / "detached.py"
    script.write_text(DETACHED, encoding="utf-8")
    return script


def test_detached_process_dies_after_a_normal_exit(ws: Path, detached_script: Path) -> None:
    result = run_process([sys.executable, str(detached_script), str(ws)], ws, timeout_s=30)
    pid = int((ws / "detached.pid").read_text())
    try:
        assert result.exit_code == 0 and not result.timed_out
        assert _gone(pid), f"detached process {pid} outlived a normal exit"
        assert result.reaped >= 1
    finally:
        _kill_leftover(pid)


def test_detached_process_with_a_dead_parent_dies_on_timeout(ws: Path, detached_script: Path, tmp_path: Path) -> None:
    agent = tmp_path / "agent.py"
    agent.write_text(LAUNCHER_THEN_WAIT, encoding="utf-8")
    result = run_process([sys.executable, str(agent), str(ws), str(detached_script)], ws, timeout_s=5)
    pid = int((ws / "detached.pid").read_text())
    try:
        assert result.timed_out
        assert _gone(pid), f"detached process {pid} outlived the timeout"
    finally:
        _kill_leftover(pid)


@pytest.mark.skipif(sys.platform != "win32", reason="Start-Process is the Windows incident (owlmsj/mengine#785)")
def test_start_process_is_contained_and_the_workspace_can_be_removed(ws: Path) -> None:
    command = (f"$p = Start-Process -FilePath '{sys.executable}' -ArgumentList '-c','\"{SLEEP}\"' -PassThru "
               f"-WorkingDirectory '{ws}'; Set-Content -Path detached.pid -Value $p.Id")
    result = run_process(["powershell", "-NoProfile", "-NonInteractive", "-Command", command], ws, timeout_s=60)
    pid = int((ws / "detached.pid").read_text().strip())
    try:
        assert result.exit_code == 0, result.stderr
        assert _gone(pid), f"Start-Process child {pid} outlived the run"
        shutil.rmtree(ws)
        assert not ws.exists()
    finally:
        _kill_leftover(pid)


@pytest.mark.skipif(sys.platform != "win32", reason="Start-Process is the Windows incident (owlmsj/mengine#785)")
@pytest.mark.parametrize("shell", ["powershell", "pwsh"])
def test_start_process_is_reaped_with_nothing_tying_it_to_the_workspace(shell: str, ws: Path, tmp_path: Path) -> None:
    # Packaged pwsh creates every child outside the Job, and here neither cwd nor argv
    # names the workspace, so the sweep cannot help: only the parent link finds it.
    if not shutil.which(shell):
        pytest.skip(f"{shell} is not installed")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    sleeper = elsewhere / "sleeper.py"
    sleeper.write_text(SLEEP, encoding="utf-8")
    command = (f"$p = Start-Process -FilePath '{sys.executable}' -ArgumentList '{sleeper}' -PassThru -WindowStyle Hidden "
               f"-WorkingDirectory '{elsewhere}'; Set-Content -Encoding ascii -Path detached.pid -Value $p.Id")
    result = run_process([shell, "-NoProfile", "-NonInteractive", "-Command", command], ws, timeout_s=60)
    pid = int((ws / "detached.pid").read_text().strip())
    try:
        assert result.exit_code == 0, result.stderr
        assert _gone(pid), f"Start-Process child {pid} outlived the run"
    finally:
        _kill_leftover(pid)


def test_a_process_outside_the_run_holding_the_workspace_is_swept(ws: Path, tmp_path: Path) -> None:
    # What escapes containment (a daemon that left the session) is found by what it holds.
    by_cwd = subprocess.Popen([sys.executable, "-c", SLEEP], cwd=ws)
    by_argv = subprocess.Popen([sys.executable, "-c", SLEEP, f"--user-data-dir={ws / 'profile'}"], cwd=tmp_path)
    try:
        result = run_process([sys.executable, "-c", "pass"], ws, timeout_s=30)
        assert _gone(by_cwd.pid) and _gone(by_argv.pid)
        assert result.reaped >= 2
    finally:
        for proc in (by_cwd, by_argv):
            proc.kill()
            proc.wait()


def test_a_process_unrelated_to_the_workspace_survives(ws: Path, tmp_path: Path) -> None:
    other = tmp_path / "other"
    other.mkdir()
    bystander = subprocess.Popen([sys.executable, "-c", SLEEP], cwd=other)
    try:
        run_process([sys.executable, "-c", "pass"], ws, timeout_s=30)
        time.sleep(1)
        assert _alive(bystander.pid), "the run killed a process it does not own"
    finally:
        bystander.kill()
        bystander.wait()


def test_the_sweep_refuses_a_root_that_holds_this_process(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # A run started from a broad directory must not sweep everything under it.
    bystander = subprocess.Popen([sys.executable, "-c", SLEEP], cwd=tmp_path)
    monkeypatch.chdir(tmp_path)
    try:
        run_process([sys.executable, "-c", "pass"], tmp_path, timeout_s=30)
        time.sleep(1)
        assert _alive(bystander.pid), "the sweep treated a directory holding the runner as a workspace"
    finally:
        bystander.kill()
        bystander.wait()
