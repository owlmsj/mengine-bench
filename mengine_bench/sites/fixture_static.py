"""A read-only multi-page site over the workspace's `site/` tree, for tasks whose pages are a recorded fixture.

Pool tasks loaded by path (mengine-qlora #22) cannot ship their own site module, so their `setup` writes the
recorded pages under `site/` and names this module as the task site. Each path maps to one file, as on a real
multi-page site: `/dir/` serves `dir/index.html`, `.json` files answer as a JSON API, and a missing file is a 404
(no client-route fallback to index.html, which would hand an agent page 1 again for any wrong link). Nothing the
agent sends changes state: POST answers 405 and the signed journal only holds its seed.

Stdlib only; run with `python -m mengine_bench.sites.fixture_static`.
"""

from __future__ import annotations

from urllib.parse import unquote, urlsplit

from mengine_bench.sites.server_base import SiteHandler, serve, with_presence
from mengine_bench.sites.signed_store import SERVED_DIR, SiteEvent, SiteState

# Explicit types: the Windows registry can map .js or .json to something odd, and mimetypes reads it.
FIXTURE_STATIC_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".htm": "text/html; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".csv": "text/csv; charset=utf-8",
    ".xml": "application/xml; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}
FIXTURE_STATIC_404 = ("<!doctype html><html lang=\"pt-BR\"><head><meta charset=\"utf-8\"><title>404</title></head>"
                      "<body><h1>404</h1><p>Página não encontrada.</p></body></html>").encode("utf-8")


def apply_fixture_static(state: SiteState, event: SiteEvent) -> SiteState:
    raise ValueError(f"received event {event!r}; expected none, the fixture site is read-only")


class FixtureStaticHandler(SiteHandler):
    """One file per path under `site/`; HTML pages carry the presence heartbeat like any app page."""

    def send_status_page(self, status: int, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler's name
        root = (self.workspace / SERVED_DIR).resolve()
        relative = unquote(urlsplit(self.path).path).lstrip("/")
        target = (root / relative).resolve()
        if target.is_dir():
            target = target / "index.html"
        if not target.is_relative_to(root) or not target.is_file():
            self.send_status_page(404, FIXTURE_STATIC_404)
            return
        content_type = FIXTURE_STATIC_TYPES.get(target.suffix.lower(), "application/octet-stream")
        body = target.read_bytes()
        if content_type.startswith("text/html"):
            body = with_presence(body)
        self.send_bytes(body, content_type)

    def do_POST(self) -> None:  # noqa: N802
        self.send_json(405, {"error": "read_only", "message": f"received POST {urlsplit(self.path).path}; "
                                                              "expected GET, this fixture site is read-only"})


if __name__ == "__main__":
    serve(FixtureStaticHandler, apply_fixture_static, {})
