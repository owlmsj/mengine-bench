"""Visual tasks run their page at grading (#82): a page that throws on load no longer reaches c=1."""

from __future__ import annotations

import io
import sys
from pathlib import Path

import pytest
from PIL import Image

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
    assert found.png == b"x" * 777, "the screenshot reaches the composition check (#164)"


def _graded(task_id: str, tmp_path: Path) -> tuple[object, task_run.TaskRunRecord]:
    task = next(item for item in catalog.all_tasks() if item.id == task_id)
    workspace = tmp_path / "ws"
    workspace.mkdir()
    task.setup(workspace)
    record = task_run.TaskRunRecord(task_id=task.id, answers=task.reference(workspace), workspace=workspace)
    task_run._grade(task, record)
    return task, record


def test_grading_records_a_failure_with_its_reason(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(task_run, "add_page_checks", lambda result, html, **kwargs: result.add(SCRIPT_ERROR, False, "Uncaught Error: boom"))
    task, record = _graded("web-mondrian-landing", tmp_path)
    assert record.check is not None and not record.check.passed
    failed = [check for check in _detail(task, record)["checks"] if not check["ok"]]
    assert failed == [{"name": SCRIPT_ERROR, "ok": False, "mandatory": False, "detail": "Uncaught Error: boom"}]


def test_a_note_about_the_machine_reaches_the_flags(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(task_run, "add_page_checks", lambda result, html, **kwargs: result.notes.append("page not run: no browser"))
    task, record = _graded("3d-print-homage", tmp_path)
    assert record.check is not None and record.check.passed
    assert _detail(task, record)["flags"] == ["page not run: no browser"]


def test_a_task_without_a_page_runs_no_browser(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def refuses(result: CheckResult, html: Path) -> None:
        raise AssertionError("a task without a page started a browser")

    monkeypatch.setattr(task_run, "add_page_checks", refuses)
    _, record = _graded("infra-gpu-fit", tmp_path)
    assert record.check is not None and record.check.passed


# ------------------------------------------------- 3d-print-homage composition (#164) --

PRINT = visual.COMPOSITION_PRINTS["3d-print-homage"]
FIXTURES = Path(__file__).parent / "fixtures" / "print-homage"
JUDGE_REFERENCE = Path(visual.__file__).parent / "assets" / "references" / "3d-print-homage.png"


@pytest.mark.parametrize("caller", ["runner", "selftest"])
@pytest.mark.parametrize("render", ["reference", "audited-opus-spire.png", "audited-sonnet-pillar.png"])
def test_production_grading_includes_composition(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                                caller: str, render: str) -> None:
    from mengine_bench import cli
    from mengine_bench.runner import task_run

    task = next(item for item in catalog.all_tasks() if item.id == "3d-print-homage")
    png = (JUDGE_REFERENCE if render == "reference" else FIXTURES / render).read_bytes()
    results: list[CheckResult] = []

    def page_checks(result: CheckResult, html: Path, *, composition: Path | None = None) -> None:
        visual.add_page_checks(result, html, lambda path: visual.PageProbe(visual.RENDERED, (), len(png), png),
                               composition=composition)
        results.append(result)

    monkeypatch.setattr(task_run if caller == "runner" else cli, "add_page_checks", page_checks)
    if caller == "runner":
        task.setup(tmp_path)
        record = task_run.TaskRunRecord(task.id, workspace=tmp_path, answers=task.reference(tmp_path))
        task_run._grade(task, record)
    else:
        cli._gold_problem(task, tmp_path)
    # #185: the similarity is a note for humans, never a scored check.
    assert visual.COMPOSITION_CHECK not in dict(results[0].checks)
    assert any(note.startswith(visual.COMPOSITION_CHECK) for note in results[0].notes)


def _flat_png(color: tuple[int, int, int]) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (1440, 900), color).save(buffer, "PNG")
    return buffer.getvalue()


@pytest.mark.parametrize(("png", "passes"), [
    (JUDGE_REFERENCE.read_bytes(), True),
    # #164: both scored 100% on tokens and palette; the judge saw a spire with arrow boats and a centre pillar.
    ((FIXTURES / "audited-opus-spire.png").read_bytes(), False),
    ((FIXTURES / "audited-sonnet-pillar.png").read_bytes(), False),
    (_flat_png((239, 227, 198)), False),
    (_flat_png((31, 58, 107)), False),
], ids=["judge reference", "audited opus spire", "audited sonnet pillar", "blank cream", "flat blue"])
def test_the_homage_render_similarity_is_a_note_never_a_point(tmp_path: Path, png: bytes, passes: bool) -> None:
    # #185 (2.6): on 18 published renders no cutoff separated the judge's votes, so the number is reported, not scored.
    result = CheckResult()
    probe = lambda html: visual.PageProbe(visual.RENDERED, (), len(png), png)  # noqa: E731
    visual.add_page_checks(result, _page(tmp_path), probe, composition=PRINT)
    assert visual.COMPOSITION_CHECK not in dict(result.checks)
    note = next(note for note in result.notes if note.startswith(visual.COMPOSITION_CHECK))
    similarity = float(note.split(": ")[1].split(" ")[0])
    assert (similarity >= visual.COMPOSITION_MIN) == passes


def test_the_composition_margins_hold() -> None:
    # #164 calibration: the reference clears the bar by more than 0.15, the audited renders miss it by more than 0.07.
    similarity = lambda path: visual.composition_similarity(path.read_bytes(), PRINT)  # noqa: E731
    assert similarity(JUDGE_REFERENCE) - visual.COMPOSITION_MIN > 0.15
    for name in ("audited-opus-spire.png", "audited-sonnet-pillar.png"):
        assert visual.COMPOSITION_MIN - similarity(FIXTURES / name) > 0.07


def test_a_page_without_a_print_gets_no_composition_check(tmp_path: Path) -> None:
    result = CheckResult()
    png = (FIXTURES / "audited-opus-spire.png").read_bytes()
    visual.add_page_checks(result, _page(tmp_path), lambda html: visual.PageProbe(visual.RENDERED, (), len(png), png))
    assert [name for name, _ok in result.checks] == [SCRIPT_ERROR, DRAWS]


@pytest.mark.skipif(visual.find_browser() is None, reason="no Chromium-family browser on PATH")
def test_the_gold_scene_renders_with_the_print_composition(tmp_path: Path) -> None:
    if not visual.three_cdn_reachable():
        pytest.skip(f"the {visual.THREE_CDN_HOST} CDN is out of reach")
    task = next(item for item in catalog.all_tasks() if item.id == "3d-print-homage")
    task.setup(tmp_path)
    task.reference(tmp_path)
    result = CheckResult()
    visual.add_page_checks(result, tmp_path / task.render_target, composition=PRINT)
    assert result.checks == [(SCRIPT_ERROR, True), (DRAWS, True)], result.details
    assert any(note.startswith(visual.COMPOSITION_CHECK) for note in result.notes)
