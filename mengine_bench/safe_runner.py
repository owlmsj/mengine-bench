"""Keep the Windows runner out of agents' broad python.exe kills (#116)."""

from __future__ import annotations

import filecmp
import os
import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

RUN_CODE = "import sys; from mengine_bench.cli import main; sys.exit(main(sys.argv[1:]))"


def runner_command(argv: Sequence[str], base_executable: str) -> list[str]:
    base = Path(base_executable).resolve()
    runner = base.with_name("mengine-bench-runner.exe")
    if not runner.is_file() or not filecmp.cmp(base, runner, shallow=False):
        shutil.copyfile(base, runner)
    return [str(runner), "-c", RUN_CODE, *argv]


def relaunch_run(argv: Sequence[str]) -> int | None:
    if sys.platform != "win32" or Path(sys.executable).name.lower() != "python.exe":
        return None
    if not argv or argv[0] != "run":
        return None
    try:
        command = runner_command(argv, sys._base_executable)
    except OSError as error:
        print(f"warning: could not copy the runner executable: {error}; continuing in the current process", file=sys.stderr)
        return None
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(str(Path(entry).resolve()) for entry in sys.path)
    return subprocess.call(command, env=env)
