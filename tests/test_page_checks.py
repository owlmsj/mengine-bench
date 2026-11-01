"""Visual tasks run their page at grading (#82): a page that throws on load no longer reaches c=1."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from mengine_bench import catalog, visual
from mengine_bench.core import CheckResult
from mengine_bench.run_command import _detail
from mengine_bench.runner import task_run

SCRIPT_ERROR = visual.SCRIPT_ERROR_CHECK
DRAWS = visual.DRAWS_CHECK


def _probe(status: str = visual.RENDERED, errors: tuple[str, ...] = (), png_bytes: int = 50_000):
    return lambda html: visual.PageProbe(status, errors, png_bytes)


def _page(tmp_path: Path) -> Path:
    page = tmp_path / "index.html"
    page.write_text("<!doctype html><title>x</title>", encoding="utf-8")
    return page


def test_a_page_that_runs_and_draws_passes_both(tmp_path: Path) -> None:
    result = CheckResult()
    visual.add_page_checks(result, _page(tmp_path), _probe())
    assert result.checks == [(SCRIPT_ERROR, True), (DRAWS, True)] and not result.notes


def test_a_script_error_fails_and_says_which(tmp_path: Path) -> None:
    result = CheckResult()
    visual.add_page_checks(result, _page(tmp_path), _probe(errors=("Uncaught TypeError: x is null",)))
    assert result.failed() == [SCRIPT_ERROR] and result.details[SCRIPT_ERROR] == "Uncaught TypeError: x is null"


def test_a_blank_page_fails_and_gives_the_size(tmp_path: Path) -> None:
    result = CheckResult()
    visual.add_page_checks(result, _page(tmp_path), _probe(png_bytes=5_854), cdn_reachable=lambda: True)
    assert result.failed() == [DRAWS] and "5854 bytes" in result.details[DRAWS]


@pytest.mark.parametrize(("probe", "reachable", "note"), [
    (_probe(status=visual.NO_BROWSER, png_bytes=0), True, "no browser"),
    (_probe(status=f"{visual.RENDER_FAILED}: timeout after 120s", png_bytes=0), True, "timeout after 120s"),
    (_probe(png_bytes=5_854), False, "CDN"),
], ids=["no browser", "render failed", "offline"])
def test_a_machine_problem_excludes_the_checks_and_never_costs_points(tmp_path: Path, probe, reachable: bool,
                                                                      note: str) -> None:
    result = CheckResult()
    result.add("page content", True)
    visual.add_page_checks(result, _page(tmp_path), probe, cdn_reachable=lambda: reachable)
    assert result.score == 1.0 and len(result.checks) == 1 and note in result.notes[0]


def test_a_browser_that_raises_is_a_note_and_never_a_crash(tmp_path: Path) -> None:
    def raises(html: Path) -> visual.PageProbe:
        raise PermissionError("locked profile")

    result = CheckResult()
    visual.add_page_checks(result, _page(tmp_path), raises)
    assert result.checks == [] and result.notes == ["page not run: PermissionError"]


def test_no_page_runs_no_browser(tmp_path: Path) -> None:
    def refuses(html: Path) -> visual.PageProbe:
        raise AssertionError("probed a missing page")

    result = CheckResult()
    visual.add_page_checks(result, tmp_path / "missing.html", refuses)
    assert result.checks == [] and result.notes == []


def test_only_the_pages_own_uncaught_errors_count() -> None:
    log = ['[1:2:INFO:CONSOLE:1] "Uncaught TypeError: boom", source: file:///C:/work/index.html (1)',
           '[1:2:INFO:CONSOLE(1)] "Uncaught (in promise) Error: late", source: file:///C:/work/index.html (9)',
           '[1:2:INFO:CONSOLE:6] "Uncaught Error: from an extension", source: chrome-extension://abc/bg.js (6)',
           '[1:2:INFO:CONSOLE:7] "just a log line", source: file:///C:/work/index.html (7)']
    assert visual.page_errors(log) == ["Uncaught TypeError: boom", "Uncaught (in promise) Error: late"]


def _fake_browser(tmp_path: Path, stderr_line: str, png_size: int) -> list[str]:
    script = tmp_path / "browser.py"
    script.write_text(
        "import sys\n"
        "shot = next(arg.split('=', 1)[1] for arg in sys.argv if arg.startswith('--screenshot='))\n"
        f"open(shot, 'wb').write(b'x' * {png_size})\n"
        f"print({stderr_line!r}, file=sys.stderr)\n", encoding="utf-8")
    return [sys.executable, "-I", str(script)]


def test_the_probe_reads_the_browser_log_and_the_screenshot_size(tmp_path: Path) -> None:
    argv = _fake_browser(tmp_path, '[1:2:INFO:CONSOLE:1] "Uncaught Error: boom", source: file:///x/index.html (1)', 777)
    found = visual.probe_page(_page(tmp_path), argv)
    assert found == visual.PageProbe(visual.RENDERED, ("Uncaught Error: boom",), 777)


def _graded(task_id: str, tmp_path: Path) -> tuple[object, task_run.TaskRunRecord]:
    task = next(item for item in catalog.all_tasks() if item.id == task_id)
    workspace = tmp_path / "ws"
    workspace.mkdir()
    task.setup(workspace)
    record = task_run.TaskRunRecord(task_id=task.id, answers=task.reference(workspace), workspace=workspace)
    task_run._grade(task, record)
    return task, record


def test_grading_records_a_failure_with_its_reason(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(task_run, "add_page_checks", lambda result, html: result.add(SCRIPT_ERROR, False, "Uncaught Error: boom"))
    task, record = _graded("web-mondrian-landing", tmp_path)
    assert record.check is not None and not record.check.passed
    failed = [check for check in _detail(task, record)["checks"] if not check["ok"]]
    assert failed == [{"name": SCRIPT_ERROR, "ok": False, "mandatory": False, "detail": "Uncaught Error: boom"}]


def test_a_note_about_the_machine_reaches_the_flags(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(task_run, "add_page_checks", lambda result, html: result.notes.append("page not run: no browser"))
    task, record = _graded("3d-voxel-landscape", tmp_path)
    assert record.check is not None and record.check.passed
    assert _detail(task, record)["flags"] == ["page not run: no browser"]


def test_a_task_without_a_page_runs_no_browser(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def refuses(result: CheckResult, html: Path) -> None:
        raise AssertionError("a task without a page started a browser")

    monkeypatch.setattr(task_run, "add_page_checks", refuses)
    _, record = _graded("vis-chart", tmp_path)
    assert record.check is not None and record.check.passed
