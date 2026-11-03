"""What every task site server shares (#153): launch handshake, static files, JSON replies.

Handshake: the runner writes one JSON line on stdin, {"workspace": ..., "key": <hex>}, then closes it;
the server binds 127.0.0.1 on a free port, writes `site-data/server.json` and prints {"port": N} as its
only stdout line. The workspace never appears on the command line or as the current directory, so the
runner's workspace sweep after a step leaves the server alone and the runner stops it when the task ends.

Only `site/` is served, the app like the real site's web root. The grader's files in `site-data/` stay off
HTTP, as a real site's database does; the agent may still read them on disk, which reveals nothing it could
not get from the API, and it cannot sign a change to them.

Presence (#161): every app page carries a heartbeat to `/__bench/heartbeat`. When the agent is done the
runner, with the run key, ends the task (`/__bench/end`), waits a few beats and asks how many pages still beat
(`/__bench/open-tabs`): those are tabs the agent left open. A page told the task is over leaves for a static
"task has ended" page with no script. Heartbeats live in memory only, never in the signed journal.

Stdlib only.
"""

from __future__ import annotations

import hmac
import json
import mimetypes
import os
import re
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

from mengine_bench.sites.signed_store import DATA_DIR, SERVED_DIR, SERVER_FILE, ApplyEvent, SignedStore, SiteState

MAX_BODY_BYTES = 5_000_000
PRESENCE_PREFIX = "/__bench/"
KEY_HEADER = "X-Bench-Key"
PAGE_ID = re.compile(r"[A-Za-z0-9]{8,64}")
MAX_PAGES = 1000
ENDED_PAGE = (b"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>Task ended</title></head>"
              b"<body><p>This task has ended. You can close this tab.</p></body></html>")
# Every 2 s; the runner waits PRESENCE_WAIT_S after the end, so an open tab beats at least twice in it.
PRESENCE_SCRIPT = (b"<script>(function(){var id=Math.random().toString(36).slice(2)+Date.now().toString(36);"
                   b"function beat(){fetch('/__bench/heartbeat?page='+id,{cache:'no-store'})"
                   b".then(function(r){return r.json();}).then(function(j){if(j.over){clearInterval(t);"
                   b"location.replace('/__bench/ended');}}).catch(function(){});}"
                   b"var t=setInterval(beat,2000);beat();})();</script>")


class Presence:
    """Which app pages beat, and since when the task is over; shared by every handler thread."""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.seen: dict[str, float] = {}
        self.over_at: float | None = None

    def beat(self, page: str) -> bool:
        with self.lock:
            if page in self.seen or len(self.seen) < MAX_PAGES:
                self.seen[page] = time.monotonic()
            return self.over_at is not None

    def end(self) -> None:
        with self.lock:
            if self.over_at is None:
                self.over_at = time.monotonic()

    def open_pages(self) -> int:
        with self.lock:
            if self.over_at is None:
                return 0
            return sum(seen >= self.over_at for seen in self.seen.values())


def with_presence(page: bytes) -> bytes:
    """The app page with its heartbeat, before </body> (or at the end)."""
    if b"</body>" in page:
        return page.replace(b"</body>", PRESENCE_SCRIPT + b"\n</body>", 1)
    return page + PRESENCE_SCRIPT


class SiteHandler(BaseHTTPRequestHandler):
    """Static files from `site/`, with index.html for every unknown path (a client-routed app)."""

    store: SignedStore
    workspace: Path
    run_key: str = ""
    presence: Presence = Presence()
    server_version = "site/1.0"

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002 - BaseHTTPRequestHandler's name
        return

    def send_json(self, status: int, payload: object) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_bytes(self, body: bytes, content_type: str, headers: tuple[tuple[str, str], ...] = ()) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        for name, value in headers:
            self.send_header(name, value)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length") or 0)
        if length < 0 or length > MAX_BODY_BYTES:
            raise ValueError(f"received Content-Length {length}; expected 0..{MAX_BODY_BYTES}")
        return self.rfile.read(length)

    def serve_static(self) -> None:
        root = (self.workspace / SERVED_DIR).resolve()
        relative = unquote(urlsplit(self.path).path).lstrip("/")
        target = (root / relative).resolve() if relative else root / "index.html"
        if not target.is_relative_to(root) or not target.is_file():
            target = root / "index.html"
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type.endswith("javascript"):
            content_type += "; charset=utf-8"
        if target.name == "index.html":
            body, headers = self.render_page(target.read_bytes())
            self.send_bytes(with_presence(body), content_type, headers)
            return
        self.send_bytes(target.read_bytes(), content_type)

    def presence_route(self) -> bool:
        """Serve a `/__bench/` path; False for any other path, which the site handles."""
        parts = urlsplit(self.path)
        if not parts.path.startswith(PRESENCE_PREFIX):
            return False
        name = parts.path.removeprefix(PRESENCE_PREFIX)
        if name == "heartbeat":
            page = parse_qs(parts.query).get("page", [""])[-1]
            if not PAGE_ID.fullmatch(page):
                self.send_json(400, {"error": "invalid", "message": f"received page id {page[:70]!r}; expected 8-64 letters or digits"})
                return True
            self.send_json(200, {"over": self.presence.beat(page)})
        elif name == "ended":
            self.send_bytes(ENDED_PAGE, "text/html; charset=utf-8")
        elif not hmac.compare_digest(self.headers.get(KEY_HEADER) or "", self.run_key):
            self.send_json(403, {"error": "forbidden", "message": f"{PRESENCE_PREFIX}{name} is the runner's"})
        elif name == "end":
            self.presence.end()
            self.send_json(200, {"over": True})
        elif name == "open-tabs":
            self.send_json(200, {"open_tabs": self.presence.open_pages()})
        else:
            self.send_json(404, {"error": "not_found", "message": f"no route at {parts.path}"})
        return True

    def render_page(self, body: bytes) -> tuple[bytes, tuple[tuple[str, str], ...]]:
        """The app page as served, with any extra headers: a site injects a per-load value or sets a cookie here."""
        return body, ()


def _with_presence_routes(handler: type[SiteHandler]) -> type[SiteHandler]:
    """The site's handler with `/__bench/` answered first, so no site can shadow it."""

    class PresenceHandler(handler):  # type: ignore[valid-type,misc]
        def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler's name
            if not self.presence_route():
                super().do_GET()

        def do_POST(self) -> None:  # noqa: N802
            if not self.presence_route():
                super().do_POST()

    return PresenceHandler


def serve(handler: type[SiteHandler], apply: ApplyEvent, seed: SiteState) -> None:
    config = json.loads(sys.stdin.readline())
    workspace, key = Path(config["workspace"]), bytes.fromhex(config["key"])
    handler = _with_presence_routes(handler)
    handler.workspace = workspace
    handler.run_key = config["key"]
    handler.store = SignedStore(workspace / DATA_DIR, key, apply, seed)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server.daemon_threads = True
    port = server.server_address[1]
    found = {"url": f"http://127.0.0.1:{port}", "pid": os.getpid()}
    (workspace / DATA_DIR / SERVER_FILE).write_text(json.dumps(found), encoding="utf-8")
    sys.stdout.write(json.dumps({"port": port}) + "\n")
    sys.stdout.flush()
    server.serve_forever()
