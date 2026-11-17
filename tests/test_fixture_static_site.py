"""The read-only fixture site serves recorded pages and JSON one file per path, 404 otherwise (mengine-qlora #22)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

from mengine_bench.runner.site import serve_site

FIXTURE_SITE = "mengine_bench.sites.fixture_static"


def _fetch(url: str, method: str = "GET") -> tuple[int, str, bytes]:
    request = urllib.request.Request(url, data=b"" if method == "POST" else None, method=method)
    try:
        with urllib.request.urlopen(request, timeout=10) as reply:
            return reply.status, reply.headers.get("Content-Type", ""), reply.read()
    except urllib.error.HTTPError as error:
        return error.code, error.headers.get("Content-Type", ""), error.read()


def test_fixture_site_serves_pages_and_json_and_404s_the_rest(tmp_path: Path) -> None:
    ws = tmp_path / "ws"
    (ws / "site" / "t" / "canal").mkdir(parents=True)
    (ws / "site" / "api").mkdir()
    (ws / "site" / "index.html").write_text("<html><body>espelho</body></html>", encoding="utf-8")
    (ws / "site" / "t" / "canal" / "page-2.html").write_text("<html><body>página 2</body></html>", encoding="utf-8")
    (ws / "site" / "api" / "p1.json").write_text('{"preco": 2899.9}', encoding="utf-8")
    (ws / "secret.txt").write_text("not served", encoding="utf-8")
    with serve_site(FIXTURE_SITE, ws) as site:
        assert site is not None
        status, kind, body = _fetch(site.url + "/t/canal/page-2.html")
        assert (status, kind) == (200, "text/html; charset=utf-8")
        assert "página 2" in body.decode("utf-8") and b"/__bench/heartbeat" in body
        status, kind, body = _fetch(site.url + "/api/p1.json")
        assert (status, kind, json.loads(body)) == (200, "application/json; charset=utf-8", {"preco": 2899.9})
        assert b"espelho" in _fetch(site.url + "/")[2], "a directory serves its index.html"
        assert _fetch(site.url + "/t/canal/page-3.html")[0] == 404, "no index fallback on a multi-page site"
        assert _fetch(site.url + "/../secret.txt")[0] == 404
        assert _fetch(site.url + "/api/p1.json", "POST")[0] == 405
