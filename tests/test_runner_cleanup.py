"""#161: a task leaves no app running and no site tab open; the owner's processes stay untouched."""

from __future__ import annotations

import json
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

import psutil
import pytest

from conftest import FakeAgent
from mengine_bench.core import CheckResult, EvalTask, Step
from mengine_bench.runner import site as site_module
from mengine_bench.runner.agents import CmdAgent
from mengine_bench.runner.site import end_pages, serve_site
from mengine_bench.runner.task_run import CLEANUP_CHECK, CLOSE_NOTE, run_task

SITE = "site_counter"
DETACHED = (subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP) if sys.platform == "win32" else 0
# Writes its pid, then sleeps: the stand-in for an app or server left running.
SLEEPER = "import os, sys, time; open(sys.argv[1], 'w').write(str(os.getpid())); time.sleep(120)"
# Starts a detached sleeper, stays long enough to be seen as its parent, then exits: the sleeper is orphaned.
LAUNCHER = ("import subprocess, sys, time; subprocess.Popen([sys.executable, '-c', sys.argv[1], sys.argv[2]], "
            "creationflags=int(sys.argv[3]), start_new_session=sys.platform != 'win32', "
            "stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.5)")
# A process that existed before the task and starts a child during it, as the owner's browser opens a renderer.
OWNER_APP = ("import subprocess, sys, time; time.sleep(float(sys.argv[3])); "
             "child = subprocess.Popen([sys.executable, '-c', sys.argv[1], sys.argv[2]]); time.sleep(120)")


def _pid_from(path: Path, wait_s: float = 15) -> int:
    deadline = time.monotonic() + wait_s
    while time.monotonic() < deadline:
        if path.is_file() and path.read_text().strip():
            return int(path.read_text())
        time.sleep(0.05)
    raise AssertionError(f"received no pid in {path} after {wait_s}s; expected the sleeper to write one")


def _alive(pid: int) -> bool:
    try:
        return psutil.Process(pid).status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False


def _kill(*procs: subprocess.Popen[bytes]) -> None:
    for proc in procs:
        for member in [*psutil.Process(proc.pid).children(recursive=True), psutil.Process(proc.pid)] if _alive(proc.pid) else []:
            try:
                member.kill()
            except psutil.NoSuchProcess:
                continue
        proc.wait(10)


def _plain_task(setup: object) -> EvalTask:
    return EvalTask(id="leaves-app", category="test", provenance="test", summary="t", setup=setup,  # type: ignore[arg-type]
                    steps=(Step("Say done."),), check=lambda ws, answers: _one_check(), reference=lambda ws: [""])


def _one_check() -> CheckResult:
    result = CheckResult()
    result.add("ran", True)
    return result


def test_runner_kills_what_the_task_left_and_spares_the_owners(fake_agent: FakeAgent, tmp_path: Path) -> None:
    owner_pid_file, owner_child_file, left_pid_file = tmp_path / "owner.pid", tmp_path / "owner-child.pid", tmp_path / "left.pid"
    owner = subprocess.Popen([sys.executable, "-c", SLEEPER, str(owner_pid_file)])
    # Starts its child 2 s in, inside the task window, from a process that is not the task's.
    owner_app = subprocess.Popen([sys.executable, "-c", OWNER_APP, SLEEPER, str(owner_child_file), "2"])
    _pid_from(owner_pid_file)

    def leave_an_app(ws: Path) -> None:
        (ws / "README.md").write_text("x", encoding="utf-8")
        subprocess.run([sys.executable, "-c", LAUNCHER, SLEEPER, str(left_pid_file), str(DETACHED)], check=True)

    template = fake_agent("done", "import time; time.sleep(1); print('done')")
    try:
        record = run_task(_plain_task(leave_an_app), CmdAgent(template=template, model="m", effort=None), tmp_path / "run")
        left_pid, owner_child_pid = _pid_from(left_pid_file), _pid_from(owner_child_file)
        # A Windows venv python is a launcher plus the interpreter (and a detached console host): all are the task's.
        assert left_pid in {left.pid for left in record.left_running}, record.left_running
        assert not any(_alive(left.pid) for left in record.left_running), "the app the task left running survived"
        assert _alive(owner.pid) and _alive(owner_app.pid), "a process from before the task was killed"
        assert _alive(owner_child_pid), "a child of the owner's app, born during the task, was killed"
        assert record.left_open_tabs is None and record.check is not None
        assert CLEANUP_CHECK not in dict(record.check.checks), "only site tasks score closing"
    finally:
        _kill(owner, owner_app)


def _workspace(tmp_path: Path) -> Path:
    ws = tmp_path / "ws"
    (ws / "site").mkdir(parents=True)
    (ws / "site" / "index.html").write_text("<html><body><p>counter app</p></body></html>", encoding="utf-8")
    return ws


def _site_setup(ws: Path) -> None:
    (ws / "site").mkdir()
    (ws / "site" / "index.html").write_text("<html><body><p>counter app</p></body></html>", encoding="utf-8")


def _get(url: str, headers: dict[str, str] | None = None) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=10) as reply:
        return reply.read()


class FakePage(threading.Thread):
    """A browser tab: beats until told the task is over, then loads the ended page (#161)."""

    def __init__(self, url: str, every_s: float = 0.1) -> None:
        super().__init__(daemon=True)
        self.url, self.every_s = url, every_s
        self.closed = threading.Event()
        self.ended_page = b""

    def run(self) -> None:
        while not self.closed.is_set():
            over = json.loads(_get(self.url + "/__bench/heartbeat?page=fakepage0001"))["over"]
            if over:
                self.ended_page = _get(self.url + "/__bench/ended")
                return
            self.closed.wait(self.every_s)


def test_an_open_page_is_counted_then_told_to_blank(tmp_path: Path) -> None:
    with serve_site(SITE, _workspace(tmp_path)) as site:
        assert site is not None
        assert b"/__bench/heartbeat" in _get(site.url + "/"), "the app page carries the heartbeat"
        page = FakePage(site.url)
        page.start()
        time.sleep(0.3)
        assert end_pages(site, wait_s=1.0) == 1
        page.join(5)
        assert not page.is_alive(), "the page kept beating after the task ended"
        assert b"This task has ended" in page.ended_page and b"<script" not in page.ended_page


def test_a_page_closed_before_the_end_is_not_counted(tmp_path: Path) -> None:
    with serve_site(SITE, _workspace(tmp_path)) as site:
        assert site is not None
        page = FakePage(site.url)
        page.start()
        time.sleep(0.3)
        page.closed.set()
        page.join(5)
        assert end_pages(site, wait_s=1.0) == 0


def test_only_the_runner_can_end_the_task(tmp_path: Path) -> None:
    with serve_site(SITE, _workspace(tmp_path)) as site:
        assert site is not None
        for name in ("end", "open-tabs"):
            with pytest.raises(urllib.error.HTTPError) as refused:
                _get(site.url + f"/__bench/{name}", headers={"X-Bench-Key": "0" * 64})
            assert refused.value.code == 403


# Opens the page (one beat), then closes it, or leaves it open by handing the URL to the test's tab.
SITE_AGENT = """
import re, sys, urllib.request
from pathlib import Path
prompt = Path(sys.argv[2]).read_text(encoding="utf-8")
url = re.search(r"http://127\\.0\\.0\\.1:\\d+", prompt).group()
urllib.request.urlopen(url + "/__bench/heartbeat?page=agentpage01", timeout=10).read()
Path(sys.argv[3]).write_text(url, encoding="utf-8")
print("visited " + url)
"""


@pytest.mark.parametrize("leave_open", [False, True])
def test_a_site_task_scores_closing_its_tabs(leave_open: bool, fake_agent: FakeAgent, tmp_path: Path,
                                             monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(site_module, "PRESENCE_WAIT_S", 1.5)
    url_file = tmp_path / "url.txt"
    template = json.loads(fake_agent("site", SITE_AGENT)) + [str(url_file)]
    task = EvalTask(id="site-tab", category="test", provenance="test", summary="visit the site",
                    setup=_site_setup,
                    steps=(Step("Visit {SITE}."),), check=lambda ws, answers: _one_check(), reference=lambda ws: [""],
                    site=SITE)
    pages: list[FakePage] = []

    def open_tab_once_the_agent_is_done() -> None:
        while not url_file.is_file():
            time.sleep(0.05)
        pages.append(FakePage(url_file.read_text(encoding="utf-8")))
        pages[0].start()

    if leave_open:
        threading.Thread(target=open_tab_once_the_agent_is_done, daemon=True).start()
    record = run_task(task, CmdAgent(template=json.dumps(template), model="m", effort=None), tmp_path / "run")
    assert record.status == "ok", record.error
    assert record.left_open_tabs == (1 if leave_open else 0)
    assert record.check is not None and dict(record.check.checks)[CLEANUP_CHECK] is (not leave_open)
    assert record.check.score == (0.5 if leave_open else 1.0)
    prompt = (tmp_path / "run" / "prompts" / "step-0.md").read_text(encoding="utf-8")
    assert CLOSE_NOTE.strip() in prompt


def _summary_of(**left: object) -> str:
    from mengine_bench.report import render_summary
    return render_summary({"bench_version": "2.4.0", "date": "d", "agent": {"name": "a", "model": "m"},
                           "totals": {"score": 1.0, "correct": 1.0, "solved": 1, "total": 1, "judge": 1.0, "time_s": 1.0},
                           "tasks": [{"id": "cu-x", "status": "ok", "flags": [], "c": 1.0, "agent_s": 1.0,
                                      "checks": [{"name": "ran", "ok": True}], **left}]})


def test_the_summary_shows_what_a_task_left_open_only_when_it_did() -> None:
    summary = _summary_of(left_open_tabs=2, left_running=[{"name": "node.exe", "pid": 42}])
    assert "## Left open" in summary and "- `cu-x`: 2 tab(s) open; still running: node.exe (42)" in summary
    assert "Left open" not in _summary_of(left_open_tabs=0, left_running=[])
    assert "Left open" not in _summary_of()
