"""Browser profile and post-processing robustness.

The FULL codex baseline crashed on its last task: the headless browser kept
cache files locked inside the task workspace and the archive step raised
PermissionError, aborting the suite before the bundle was written.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pytest

from conftest import FakeAgent
from mengine_bench import cli, run_command, visual
from mengine_bench.runner import task_run

# Mimics Edge: the launcher writes the screenshot and exits while a helper
# process keeps a cache file in the profile open.
FAKE_BROWSER = r"""
import subprocess, sys
from pathlib import Path
args = dict(a.split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
profile = Path(args["--user-data-dir"])
(Path(__file__).parent / "profile.txt").write_text(str(profile), encoding="utf-8")
cache = profile / "Default" / "Cache" / "Cache_Data"
cache.mkdir(parents=True, exist_ok=True)
HOLD = "import sys, time; f = open(sys.argv[1], 'wb'); f.write(b'x'); f.flush(); time.sleep(60)"
subprocess.Popen([sys.executable, "-c", HOLD, str(cache / "data_0"), str(profile)])
while not (cache / "data_0").exists():
    pass
Path(args["--screenshot"]).write_bytes(b"P" * 20_000)
"""


def test_render_keeps_the_browser_profile_outside_the_workspace(tmp_path: Path,
                                                                monkeypatch: pytest.MonkeyPatch) -> None:
    script = tmp_path / "fakes" / "browser.py"
    script.parent.mkdir()
    script.write_text(FAKE_BROWSER, encoding="utf-8")
    monkeypatch.setattr(visual, "BROWSER_EXIT_WAIT_S", 1.0)
    ws = tmp_path / "ws"
    (ws / "scene").mkdir(parents=True)
    html = ws / "scene" / "index.html"
    html.write_text("<html><body>scene</body></html>", encoding="utf-8")
    started = time.monotonic()
    status = visual.render_headless(html, ws / "_render" / "shot.png",
                                    browser_argv=[sys.executable, "-I", str(script)])
    assert status == visual.RENDERED
    assert time.monotonic() - started < 30, "a lingering browser helper must be killed, not waited for"
    profile = Path((script.parent / "profile.txt").read_text(encoding="utf-8"))
    assert not profile.resolve().is_relative_to(ws.resolve()), f"profile {profile} must live outside the workspace"
    assert not profile.exists(), "the temp profile is removed once the browser tree is gone"


def test_snapshot_skips_unreadable_files_and_browser_profiles(tmp_path: Path,
                                                             monkeypatch: pytest.MonkeyPatch) -> None:
    ws = tmp_path / "ws"
    (ws / "scene" / ".verify-profile" / "Default").mkdir(parents=True)
    (ws / "scene" / ".verify-profile" / "Default" / "data_0").write_bytes(b"cache")
    (ws / "scene" / "index.html").write_text("<html></html>", encoding="utf-8")
    (ws / "locked.bin").write_bytes(b"locked")
    real_read = Path.read_bytes

    def read_bytes(self: Path) -> bytes:
        if self.name == "locked.bin":
            raise PermissionError(13, "Permission denied", str(self))
        return real_read(self)

    monkeypatch.setattr(Path, "read_bytes", read_bytes)
    assert task_run.snapshot(ws) == {"scene/index.html": b"<html></html>"}


IDLE_AGENT = "print('done')\n"


def test_post_processing_crash_marks_the_task_crash_and_the_suite_continues(
        fake_agent: FakeAgent, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    real_judge_packet = run_command._judge_packet
    calls: list[int] = []

    def flaky_judge_packet(*args: object) -> object:
        calls.append(1)
        if len(calls) == 1:
            raise PermissionError(13, "Permission denied", "data_0")
        return real_judge_packet(*args)  # type: ignore[arg-type]

    monkeypatch.setattr(run_command, "_judge_packet", flaky_judge_packet)
    out = tmp_path / "results"
    code = cli.main(["run", "--agent", "cmd", "--cmd", fake_agent("idle", IDLE_AGENT),
                     "--model", "fake/idle", "--tasks", "ds-ab-playtest,bo-pnl-runway", "--out", str(out),
                     "--work", str(tmp_path / "work")])
    assert code == 0
    [result_file] = out.glob("*/result.json")
    tasks = {task["id"]: task for task in json.loads(result_file.read_text(encoding="utf-8"))["tasks"]}
    assert tasks["ds-ab-playtest"]["status"] == "crash"
    assert "PermissionError" in tasks["ds-ab-playtest"]["error"]
    assert tasks["bo-pnl-runway"]["status"] == "ok"
