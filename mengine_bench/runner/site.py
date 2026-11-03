"""Start and stop a task's local site server (#153).

The server runs the task's stdlib module with this interpreter, contained like an agent (a Windows Job
that dies with the runner, or a POSIX session), with no window. It gets the workspace and a per-run key
on stdin, prints its port, and is killed with everything it started when the task ends; only then does
the key reach the workspace, for the grader (see `mengine_bench.sites.signed_store`).
"""

from __future__ import annotations

import json
import os
import secrets
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import IO

import mengine_bench
from mengine_bench.runner.containment import PosixSession, WindowsJob, new_scope, stop_session_group
from mengine_bench.runner.process import kill_tree
from mengine_bench.sites.server_base import KEY_HEADER, PRESENCE_PREFIX
from mengine_bench.sites.signed_store import DATA_DIR, KEY_FILE

START_TIMEOUT_S = 20
CREATE_NO_WINDOW = 0x08000000
SITE_PLACEHOLDER = "{SITE}"
# #161: a page beats every 2 s; an open tab beats at least twice in this wait, and is told the task is over.
PRESENCE_WAIT_S = 5.0
PRESENCE_TIMEOUT_S = 5


class SiteFailed(RuntimeError):
    """The site server did not start."""


@dataclass
class SiteServer:
    module: str
    workspace: Path
    key: str
    port: int
    proc: subprocess.Popen[bytes]
    scope: PosixSession | WindowsJob
    log: IO[bytes]

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}"


def _popen_kwargs(scope: PosixSession | WindowsJob) -> dict[str, object]:
    kwargs = dict(scope.popen_kwargs)
    if sys.platform == "win32":
        kwargs["creationflags"] = int(kwargs.get("creationflags", 0)) | CREATE_NO_WINDOW  # type: ignore[call-overload]
    return kwargs


def _read_port(proc: subprocess.Popen[bytes]) -> int | None:
    line: list[bytes] = []
    reader = threading.Thread(target=lambda: line.append(proc.stdout.readline() if proc.stdout else b""), daemon=True)
    reader.start()
    reader.join(START_TIMEOUT_S)
    try:
        port = json.loads(line[0])["port"] if line else None
    except (ValueError, KeyError, TypeError):
        return None
    return port if isinstance(port, int) and 0 < port < 65536 else None


def start_site(module: str, workspace: Path) -> SiteServer:
    key = secrets.token_hex(32)
    scope = new_scope()
    # This interpreter's own path: the relaunched Windows runner has no venv, and -I would drop PYTHONPATH.
    env = {**os.environ, "PYTHONPATH": os.pathsep.join(str(Path(entry).resolve()) for entry in sys.path if entry),
           "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUNBUFFERED": "1"}
    log = tempfile.TemporaryFile()
    # The package folder as cwd: never the workspace, which the step sweep would treat as the agent's.
    cwd = Path(mengine_bench.__file__).resolve().parent
    proc = subprocess.Popen([sys.executable, "-m", module], cwd=cwd, env=env, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=log, **_popen_kwargs(scope))
    scope.adopt(proc)
    server = SiteServer(module, workspace, key, 0, proc, scope, log)
    assert proc.stdin is not None
    proc.stdin.write((json.dumps({"workspace": str(workspace.resolve()), "key": key}) + "\n").encode("utf-8"))
    proc.stdin.close()
    port = _read_port(proc)
    if port is None:
        stop_site(server, write_key=False)
        log.seek(0)
        tail = log.read()[-600:].decode("utf-8", errors="replace")
        raise SiteFailed(f"site {module!r} printed no port within {START_TIMEOUT_S}s; expected {{\"port\": N}}. "
                         f"stderr: {tail}")
    server.port = port
    return server


def _presence_call(server: SiteServer, name: str, method: str) -> dict[str, object]:
    request = urllib.request.Request(server.url + PRESENCE_PREFIX + name, data=b"" if method == "POST" else None,
                                     method=method, headers={KEY_HEADER: server.key})
    with urllib.request.urlopen(request, timeout=PRESENCE_TIMEOUT_S) as reply:
        payload = json.loads(reply.read())
    if not isinstance(payload, dict):
        raise ValueError(f"received {payload!r:.80} from {name}; expected a JSON object")
    return payload


def end_pages(server: SiteServer, wait_s: float | None = None) -> int | None:
    """Tell every app page the task is over and count those still open (#161); None when the server did not answer."""
    try:
        _presence_call(server, "end", "POST")
        time.sleep(PRESENCE_WAIT_S if wait_s is None else wait_s)
        count = _presence_call(server, "open-tabs", "GET").get("open_tabs")
    except (OSError, ValueError, urllib.error.URLError):
        return None
    return count if isinstance(count, int) else None


def stop_site(server: SiteServer, write_key: bool = True) -> None:
    """Kill the server and all it started, then hand the key to the grader."""
    kill_tree(server.proc.pid)
    server.proc.wait()
    stop_session_group(server.proc.pid)
    try:
        server.scope.kill_all(server.proc.pid)
    finally:
        server.scope.close()
        if server.proc.stdout is not None:
            server.proc.stdout.close()
        server.log.close()
    if write_key:
        # Written after the server is gone, over anything the agent left there.
        data = server.workspace / DATA_DIR
        data.mkdir(parents=True, exist_ok=True)
        (data / KEY_FILE).write_text(server.key, encoding="ascii")


@contextmanager
def serve_site(module: str | None, workspace: Path) -> Iterator[SiteServer | None]:
    """The site for one task while the block runs; nothing when the task has none."""
    if module is None:
        yield None
        return
    server = start_site(module, workspace)
    try:
        yield server
    finally:
        stop_site(server)
