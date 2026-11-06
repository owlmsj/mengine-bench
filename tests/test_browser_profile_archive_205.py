"""A browser user-data dir the agent left in its workspace never reaches the bundle (#205).

web-mondrian-landing left a Chromium profile named `tmp/edgeprofile`; its History, Sessions
and Favicons hold the home path, so the archived workspace failed the privacy check.
"""

from __future__ import annotations

import tarfile
from pathlib import Path

from mengine_bench.bundle import _write_workspace


def _chromium_profile(root: Path) -> None:
    (root / "Default").mkdir(parents=True)
    (root / "Local State").write_text('{"profile": {}}', encoding="utf-8")
    (root / "Default" / "History").write_bytes(b"SQLite format 3\x00 C:\\Users\\someone\\page.html")


def test_a_profile_found_by_its_local_state_marker_is_left_out(tmp_path: Path) -> None:
    ws = tmp_path / "workspace"
    (ws / "tmp").mkdir(parents=True)
    (ws / "index.html").write_text("<h1>page</h1>", encoding="utf-8")
    (ws / "tmp" / "notes.txt").write_text("kept", encoding="utf-8")
    _chromium_profile(ws / "tmp" / "edgeprofile")
    target = tmp_path / "archive.tar.gz"
    assert _write_workspace(target, ws) == []
    with tarfile.open(target) as archive:
        assert set(archive.getnames()) == {"index.html", "tmp/notes.txt"}


def test_a_profile_named_in_browser_profile_dirs_is_left_out_without_its_marker(tmp_path: Path) -> None:
    ws = tmp_path / "workspace"
    (ws / "chrome-profile" / "Default").mkdir(parents=True)
    (ws / "chrome-profile" / "Default" / "Cookies").write_bytes(b"cookie")
    (ws / "index.html").write_text("<h1>page</h1>", encoding="utf-8")
    target = tmp_path / "archive.tar.gz"
    assert _write_workspace(target, ws) == []
    with tarfile.open(target) as archive:
        assert archive.getnames() == ["index.html"]


def test_repack_drops_a_profile_from_an_archive_written_before_the_fix(tmp_path: Path) -> None:
    from mengine_bench.bundle import repack_workspace

    ws = tmp_path / "workspace"
    (ws / "tmp").mkdir(parents=True)
    (ws / "index.html").write_text("<h1>page</h1>", encoding="utf-8")
    _chromium_profile(ws / "tmp" / "edgeprofile")
    archive_path = tmp_path / "web-mondrian-landing.tar.gz"
    with tarfile.open(archive_path, "w:gz") as archive:
        for name in ("index.html", "tmp/edgeprofile/Local State", "tmp/edgeprofile/Default/History"):
            archive.add(ws / name, arcname=name)
    assert repack_workspace(archive_path) == ["tmp/edgeprofile"]
    with tarfile.open(archive_path) as archive:
        assert archive.getnames() == ["index.html"]
        assert archive.extractfile("index.html").read() == b"<h1>page</h1>"
    assert repack_workspace(archive_path) == [], "a clean archive is left as it is"
