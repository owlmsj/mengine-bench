"""What every task site server shares (#153): launch handshake, static files, JSON replies.

Handshake: the runner writes one JSON line on stdin, {"workspace": ..., "key": <hex>}, then closes it;
the server binds 127.0.0.1 on a free port, writes `site-data/server.json` and prints {"port": N} as its
only stdout line. The workspace never appears on the command line or as the current directory, so the
runner's workspace sweep after a step leaves the server alone and the runner stops it when the task ends.

Only `site/` is served, the app like the real site's web root. The grader's files in `site-data/` stay off
HTTP, as a real site's database does; the agent may still read them on disk, which reveals nothing it could
not get from the API, and it cannot sign a change to them.

Stdlib only.
"""

from __future__ import annotations

import json
import mimetypes
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from mengine_bench.sites.signed_store import DATA_DIR, SERVED_DIR, SERVER_FILE, ApplyEvent, SignedStore, SiteState

MAX_BODY_BYTES = 5_000_000


class SiteHandler(BaseHTTPRequestHandler):
    """Static files from `site/`, with index.html for every unknown path (a client-routed app)."""

    store: SignedStore
    workspace: Path
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

    def send_bytes(self, body: bytes, content_type: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
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
        self.send_bytes(target.read_bytes(), content_type)


def serve(handler: type[SiteHandler], apply: ApplyEvent, seed: SiteState) -> None:
    config = json.loads(sys.stdin.readline())
    workspace, key = Path(config["workspace"]), bytes.fromhex(config["key"])
    handler.workspace = workspace
    handler.store = SignedStore(workspace / DATA_DIR, key, apply, seed)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server.daemon_threads = True
    port = server.server_address[1]
    found = {"url": f"http://127.0.0.1:{port}", "pid": os.getpid()}
    (workspace / DATA_DIR / SERVER_FILE).write_text(json.dumps(found), encoding="utf-8")
    sys.stdout.write(json.dumps({"port": port}) + "\n")
    sys.stdout.flush()
    server.serve_forever()
