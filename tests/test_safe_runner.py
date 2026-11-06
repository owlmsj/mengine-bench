"""Renamed Windows runner: no real process launch or process termination (#116)."""
from pathlib import Path
import subprocess
import sys

import pytest

from mengine_bench import safe_runner


def test_runner_command_copies_refreshes_and_preserves_arguments(tmp_path: Path) -> None:
    base = tmp_path / 'python.exe'
    base.write_bytes(b'python-v1')
    argv = ['run', '--model', 'model with spaces', '--agent', 'cmd']
    command = safe_runner.runner_command(argv, str(base))
    renamed = tmp_path / 'mengine-bench-runner.exe'
    assert command == [str(renamed), '-c', safe_runner.RUN_CODE, *argv]
    assert renamed.read_bytes() == b'python-v1'
    timestamp = renamed.stat().st_mtime_ns
    safe_runner.runner_command(argv, str(base))
    assert renamed.stat().st_mtime_ns == timestamp
    # #168: same size and the same mtime as v1, as two writes inside the clock's granularity give; filecmp's
    # (size, mtime) cache then called the files equal and the runner kept the old interpreter.
    stamp = base.stat().st_mtime_ns
    base.write_bytes(b'python-v2')
    import os
    os.utime(base, ns=(stamp, stamp))
    safe_runner.runner_command(argv, str(base))
    assert renamed.read_bytes() == b'python-v2'


# #205: redo runs agents like run, so it gets the same shield.
@pytest.mark.parametrize('command', ['run', 'redo'])
def test_relaunch_returns_child_exit_and_absolute_pythonpath(command: str, tmp_path: Path,
                                                             monkeypatch: pytest.MonkeyPatch) -> None:
    base = tmp_path / 'python.exe'
    base.write_bytes(b'python')
    monkeypatch.setattr(sys, 'platform', 'win32')
    monkeypatch.setattr(sys, 'executable', str(base))
    monkeypatch.setattr(sys, '_base_executable', str(base))
    monkeypatch.setattr(sys, 'path', ['', 'relative', str(tmp_path)])
    monkeypatch.setenv('PYTHONPATH', 'obsolete')
    calls = []
    def child(command: list[str], *, env: dict[str, str]) -> int:
        calls.append(command)
        assert env['PYTHONPATH'].split(';') == [str(Path.cwd()), str(Path('relative').resolve()), str(tmp_path)]
        return 23
    monkeypatch.setattr(subprocess, 'call', child)
    assert safe_runner.relaunch_run([command, '--model', 'm']) == 23
    assert len(calls) == 1


@pytest.mark.parametrize(('platform', 'executable', 'argv'), [
    ('linux', '/bin/python.exe', ['run']),
    ('win32', 'mengine-bench-runner.exe', ['run']),
    ('win32', 'python.exe', ['list']),
])
def test_other_commands_and_interpreters_do_not_relaunch(platform: str, executable: str, argv: list[str],
                                                         monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, 'platform', platform)
    monkeypatch.setattr(sys, 'executable', executable)
    assert safe_runner.relaunch_run(argv) is None


def test_copy_failure_warns_and_keeps_current_process(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                                      capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, 'platform', 'win32')
    monkeypatch.setattr(sys, 'executable', 'python.exe')
    monkeypatch.setattr(sys, '_base_executable', str(tmp_path / 'missing.exe'))
    assert safe_runner.relaunch_run(['run']) is None
    assert 'warning:' in capsys.readouterr().err
