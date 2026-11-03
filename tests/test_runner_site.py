"""Per-task local site: starts on a free port, serves the workspace app, signs its state, leaves nothing (#153)."""

from __future__ import annotations

import json
import socket
import time
import urllib.request
from pathlib import Path

import psutil
import pytest

from conftest import FakeAgent
from mengine_bench.core import CheckResult, EvalTask, Step
from mengine_bench.runner.agents import CmdAgent
from mengine_bench.runner.containment import sweep_workspace
from mengine_bench.runner.site import serve_site
from mengine_bench.runner.task_run import run_task
from mengine_bench.sites.signed_store import DATA_DIR, JOURNAL_FILE, KEY_FILE, SERVER_FILE, STATE_FILE, verify
from site_counter import apply_counter

SITE = "site_counter"


def _workspace(tmp_path: Path) -> Path:
    ws = tmp_path / "ws"
    (ws / "site").mkdir(parents=True)
    (ws / "site" / "index.html").write_text("<title>counter app</title>", encoding="utf-8")
    return ws


def _get(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=10) as reply:
        return reply.read()


def _post(url: str) -> object:
    request = urllib.request.Request(url, data=b"", method="POST")
    with urllib.request.urlopen(request, timeout=10) as reply:
        return json.loads(reply.read())


def _port_open(port: int) -> bool:
    with socket.socket() as probe:
        probe.settimeout(1)
        return probe.connect_ex(("127.0.0.1", port)) == 0


def _gone(pid: int, wait_s: float = 10) -> bool:
    deadline = time.monotonic() + wait_s
    while time.monotonic() < deadline:
        if not psutil.pid_exists(pid) or psutil.Process(pid).status() == psutil.STATUS_ZOMBIE:
            return True
        time.sleep(0.1)
    return False


def test_site_serves_the_app_signs_state_and_leaves_nothing(tmp_path: Path) -> None:
    ws = _workspace(tmp_path)
    with serve_site(SITE, ws) as site:
        assert site is not None
        assert b"counter app" in _get(site.url + "/")
        assert b"counter app" in _get(site.url + "/profile/anyone/post/1"), "client routes fall back to index.html"
        assert b"counter app" in _get(site.url + "/../site-data/state.json"), "the grader's files stay off HTTP"
        assert _post(site.url + "/hit") == {"hits": 1}
        # The serving pid, which a Windows venv launcher runs as its child.
        pid, port = json.loads((ws / DATA_DIR / SERVER_FILE).read_text())["pid"], site.port
        assert pid == site.proc.pid or pid in {child.pid for child in psutil.Process(site.proc.pid).children(True)}
        assert not (ws / DATA_DIR / KEY_FILE).exists(), "the key must not reach the workspace while the agent runs"
    assert _gone(pid), "server process survived the task"
    assert not _port_open(port), "server port still accepts connections"
    key = bytes.fromhex((ws / DATA_DIR / KEY_FILE).read_text())
    state, events = verify(ws / DATA_DIR, key, apply_counter)
    assert state == {"hits": 1} and [event["type"] for event in events] == ["seed", "hit"]


def test_server_is_not_the_agents_so_the_step_sweep_spares_it(tmp_path: Path) -> None:
    ws = _workspace(tmp_path)
    with serve_site(SITE, ws) as site:
        assert site is not None
        assert sweep_workspace(ws) == 0
        assert _post(site.url + "/hit") == {"hits": 1}


@pytest.mark.parametrize("tamper", ["state", "journal", "drop_line", "other_key"])
def test_any_edit_but_the_servers_fails_verification(tmp_path: Path, tamper: str) -> None:
    ws = _workspace(tmp_path)
    with serve_site(SITE, ws) as site:
        assert site is not None
        _post(site.url + "/hit")
        _post(site.url + "/hit")
    data = ws / DATA_DIR
    key = bytes.fromhex((data / KEY_FILE).read_text())
    if tamper == "state":
        stored = json.loads((data / STATE_FILE).read_text(encoding="utf-8"))
        stored["state"]["hits"] = 5
        (data / STATE_FILE).write_text(json.dumps(stored), encoding="utf-8")
    elif tamper == "journal":
        text = (data / JOURNAL_FILE).read_text(encoding="utf-8")
        (data / JOURNAL_FILE).write_text(text.replace('"hit"', '"hit "', 1), encoding="utf-8")
    elif tamper == "drop_line":
        lines = (data / JOURNAL_FILE).read_text(encoding="utf-8").splitlines(keepends=True)
        (data / JOURNAL_FILE).write_text("".join(lines[:-1]), encoding="utf-8")
    else:
        key = bytes(32)
    with pytest.raises(ValueError, match="not signed|differs"):
        verify(data, key, apply_counter)


SITE_AGENT = """
import json, re, sys, urllib.request
from pathlib import Path
prompt = Path(sys.argv[2]).read_text(encoding="utf-8")
url = re.search(r"http://127\\.0\\.0\\.1:\\d+", prompt).group()
urllib.request.urlopen(urllib.request.Request(url + "/hit", data=b"", method="POST"), timeout=10).read()
print("hit " + url)
"""


def _counter_check(ws: Path, answers: list[str]) -> CheckResult:
    result = CheckResult()
    key = bytes.fromhex((ws / DATA_DIR / KEY_FILE).read_text())
    state, _ = verify(ws / DATA_DIR, key, apply_counter)
    result.add("one hit", state == {"hits": 1})
    return result


def test_run_task_puts_the_url_in_the_prompt_and_stops_the_server(fake_agent: FakeAgent, tmp_path: Path) -> None:
    template = json.loads(fake_agent("site", SITE_AGENT))
    task = EvalTask(id="site-counter", category="test", provenance="test", summary="hit the site once",
                    setup=_workspace_setup, steps=(Step("Hit the counter at {SITE} once."),), check=_counter_check,
                    reference=lambda ws: [""], site=SITE)
    record = run_task(task, CmdAgent(template=json.dumps(template), model="m", effort=None), tmp_path / "run")
    assert record.status == "ok", record.error
    assert record.check is not None and record.check.passed
    prompt = (tmp_path / "run" / "prompts" / "step-0.md").read_text(encoding="utf-8")
    assert "{SITE}" not in prompt and "http://127.0.0.1:" in prompt
    assert record.workspace is not None
    server = json.loads((record.workspace / DATA_DIR / SERVER_FILE).read_text())
    assert _gone(server["pid"])
    assert not _port_open(int(server["url"].rsplit(":", 1)[1]))


def _workspace_setup(ws: Path) -> None:
    (ws / "site").mkdir()
    (ws / "site" / "index.html").write_text("<title>counter app</title>", encoding="utf-8")


def test_a_site_task_must_have_one_step() -> None:
    with pytest.raises(ValueError, match="one step"):
        EvalTask(id="x", category="t", provenance="t", summary="t", setup=_workspace_setup,
                 steps=(Step("a {SITE}"), Step("b", fresh_session=True)), check=_counter_check,
                 reference=lambda ws: [""], site=SITE)
