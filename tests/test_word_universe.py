"""#99: the word universe eval. Any valid view and data shape passes; each of the site's traps costs the check it touches."""

from __future__ import annotations

import sys
from pathlib import Path

from mengine_bench import visual


def _fake_browser(tmp_path: Path, stdout: str, exit_code: int = 0) -> list[str]:
    script = tmp_path / "browser.py"
    script.write_text(f"import sys\nsys.stdout.write({stdout!r} + sys.argv[-1])\nsys.exit({exit_code})\n", encoding="utf-8")
    return [sys.executable, "-I", str(script)]


def test_the_dump_reads_the_dom_of_the_page_with_its_query(tmp_path: Path) -> None:
    page = tmp_path / "index.html"
    page.write_text("x", encoding="utf-8")
    status, dom = visual.dump_page_dom(page, "word=pa%C3%ADs", _fake_browser(tmp_path, "<p>dom</p>"))
    assert status == visual.RENDERED and dom.startswith("<p>dom</p>file:") and dom.endswith("index.html?word=pa%C3%ADs")


def test_a_browser_that_fails_is_a_status_and_never_a_crash(tmp_path: Path) -> None:
    page = tmp_path / "index.html"
    page.write_text("x", encoding="utf-8")
    assert visual.is_render_failure(visual.dump_page_dom(page, "word=a", _fake_browser(tmp_path, "", 3))[0])
    assert visual.is_render_failure(visual.dump_page_dom(page, "word=a", [str(tmp_path / "missing.exe")])[0])


def test_no_browser_is_reported_as_such(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(visual, "find_browser", lambda: None)
    assert visual.dump_page_dom(tmp_path / "index.html", "word=a") == (visual.NO_BROWSER, "")
