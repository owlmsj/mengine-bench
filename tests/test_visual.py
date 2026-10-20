"""Visual tasks: deterministic content gates at run time; the headless render serves only the maintainer's judge."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from mengine_bench import visual
from mengine_bench.core import CheckResult, write
from mengine_bench.tasks import visual as visual_tasks

LANDING = next(task for task in visual_tasks.TASKS if task.id == "web-mondrian-landing")
SCENE = next(task for task in visual_tasks.TASKS if task.id == "3d-voxel-landscape")


def _solved(task: object, ws: Path) -> CheckResult:
    ws.mkdir()
    task.setup(ws)  # type: ignore[attr-defined]
    return task.check(ws, task.reference(ws))  # type: ignore[attr-defined]


def test_landing_ships_a_local_factsheet_instead_of_web_research(tmp_path: Path) -> None:
    LANDING.setup(tmp_path)
    sheet = (tmp_path / visual_tasks.FACTSHEET).read_text(encoding="utf-8")
    for fact in ("Composition with Red, Blue and Yellow", "Piet Mondrian", "1930", "De Stijl",
                 visual_tasks.FACTSHEET_SOURCE):
        assert fact in sheet
    prompt = LANDING.steps[0].prompt
    assert "FACTSHEET.md" in prompt and "web" not in prompt.lower()
    assert "web" not in LANDING.needs


def test_landing_source_gate_wants_the_factsheet_url(tmp_path: Path) -> None:
    assert _solved(LANDING, tmp_path / "ok").passed
    ws = tmp_path / "other-link"
    ws.mkdir()
    LANDING.setup(ws)
    LANDING.reference(ws)
    page = ws / visual_tasks.LANDING
    page.write_text(page.read_text(encoding="utf-8").replace(visual_tasks.FACTSHEET_SOURCE, "https://example.org/x"),
                    encoding="utf-8")
    result = LANDING.check(ws, ["done"])
    assert "links to the fact sheet's source" in result.failed() and not result.passed


def test_scene_pins_the_three_js_version(tmp_path: Path) -> None:
    assert visual_tasks.THREE_URL in SCENE.steps[0].prompt
    assert _solved(SCENE, tmp_path / "ok").passed
    ws = tmp_path / "unpinned"
    ws.mkdir()
    SCENE.reference(ws)
    page = ws / visual_tasks.SCENE
    page.write_text(page.read_text(encoding="utf-8").replace("three@0.170.0", "three"), encoding="utf-8")
    result = SCENE.check(ws, ["done"])
    assert result.failed() == ["imports three.js 0.170.0 from the CDN"]


def test_visual_checks_are_deterministic_and_never_start_a_browser(tmp_path: Path,
                                                                   monkeypatch: pytest.MonkeyPatch) -> None:
    def no_browser(*args: object, **kwargs: object) -> None:
        raise AssertionError("a visual check started a process")

    monkeypatch.setattr(subprocess, "Popen", no_browser)
    for task in visual_tasks.TASKS:
        result = _solved(task, tmp_path / task.id)
        assert type(result) is CheckResult and result.passed
        assert not any("vision" in name or "screenshot" in name for name, _ in [*result.mandatory, *result.checks])


def test_missing_page_fails_the_gate_and_scores_zero(tmp_path: Path) -> None:
    for task in visual_tasks.TASKS:
        ws = tmp_path / task.id
        ws.mkdir()
        task.setup(ws)
        result = task.check(ws, [""])
        assert not result.mandatory_ok and result.score == 0.0


def test_visual_tasks_declare_their_page_as_deliverable() -> None:
    assert LANDING.deliverables == (visual_tasks.LANDING,)
    assert SCENE.deliverables == (visual_tasks.SCENE,)


def test_render_module_has_no_run_time_grading() -> None:
    for removed in ("grade", "JUDGE", "RENDER", "enforce_rendered_profile", "PendingVision", "VisualCheckResult",
                    "PASS_RATIO", "PROFILE_UNRENDERED", "judge_screenshot"):
        assert not hasattr(visual, removed), removed


def test_find_browser_uses_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MENGINE_BENCH_BROWSER", raising=False)
    monkeypatch.setattr(visual, "browser_install_candidates", lambda: [])
    monkeypatch.setattr(visual.shutil, "which", lambda name: f"/bin/{name}" if name == "chromium" else None)
    assert visual.find_browser() == "/bin/chromium"
    monkeypatch.setattr(visual.shutil, "which", lambda name: None)
    assert visual.find_browser() is None


def test_missing_browser_reports_no_browser(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(visual, "find_browser", lambda: None)
    html = write(tmp_path, "page.html", "<html></html>")
    assert visual.render_headless(html, tmp_path / "shot.png") == visual.NO_BROWSER


def test_screenshot_has_content(tmp_path: Path) -> None:
    png = tmp_path / "a.png"
    assert not visual.screenshot_has_content(png, 10)
    png.write_bytes(b"0" * 10)
    assert visual.screenshot_has_content(png, 10)


@pytest.mark.skipif(visual.find_browser() is None, reason="no Chromium-family browser on PATH")
def test_reference_landing_renders_with_content(tmp_path: Path) -> None:
    html = write(tmp_path, visual_tasks.LANDING, visual_tasks.LANDING_REFERENCE)
    png = tmp_path / "_render" / "shot.png"
    assert visual.render_headless(html, png) == visual.RENDERED
    assert visual.screenshot_has_content(png, 10_000)


def test_find_browser_env_override_and_standard_locations(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(visual.shutil, "which", lambda name: None)
    custom = tmp_path / "my browser.exe"
    custom.write_bytes(b"")
    monkeypatch.setenv("MENGINE_BENCH_BROWSER", str(custom))
    assert visual.find_browser() == str(custom)
    monkeypatch.delenv("MENGINE_BENCH_BROWSER")
    edge = tmp_path / "x86" / "Microsoft" / "Edge" / "Application" / "msedge.exe"
    edge.parent.mkdir(parents=True)
    edge.write_bytes(b"")
    monkeypatch.setattr(visual, "browser_install_candidates", lambda: [tmp_path / "missing.exe", edge])
    assert visual.find_browser() == str(edge)


def test_browser_install_candidates_cover_each_os() -> None:
    windows = [str(p) for p in visual.browser_install_candidates(
        "Windows", {"ProgramFiles": "C:/PF", "ProgramFiles(x86)": "C:/PF86", "LOCALAPPDATA": "C:/LA"})]
    assert str(Path("C:/PF86/Microsoft/Edge/Application/msedge.exe")) in windows
    assert str(Path("C:/PF/Google/Chrome/Application/chrome.exe")) in windows
    assert str(Path("C:/LA/Google/Chrome/Application/chrome.exe")) in windows
    mac = [p.as_posix() for p in visual.browser_install_candidates("Darwin", {})]
    assert "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" in mac
    assert "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" in mac
    linux = [p.as_posix() for p in visual.browser_install_candidates("Linux", {})]
    assert {"/opt/microsoft/msedge/msedge", "/opt/google/chrome/chrome", "/snap/bin/chromium"} <= set(linux)


# Headless Chrome on Ubuntu could not screenshot without the container flags,
# and the failure said only "render failed".
LINUX_ONLY = ("--disable-dev-shm-usage", "--disable-gpu")
COMMON = ("--headless=new", "--hide-scrollbars", "--window-size=1440,900")


def test_headless_flags_linux_sandbox_only_for_root() -> None:
    desktop = visual.headless_browser_flags("Linux", is_root=False)
    assert "--no-sandbox" not in desktop and set(LINUX_ONLY + COMMON) <= set(desktop)
    assert "--no-sandbox" in visual.headless_browser_flags("Linux", is_root=True)


@pytest.mark.parametrize("system", ["Windows", "Darwin"])
def test_headless_flags_windows_and_mac_unchanged(system: str) -> None:
    flags = visual.headless_browser_flags(system, is_root=True)
    assert flags == ["--headless=new", "--no-first-run", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
                     "--hide-scrollbars", "--window-size=1440,900", "--virtual-time-budget=8000"]


FAILING_BROWSER = r"""
import sys
sys.stderr.write("[0101/000000.0:FATAL:zygote_host_impl_linux.cc] No usable sandbox!\n")
sys.stderr.write("token " + sys.argv[1] + "\n")
for n in range(50):
    sys.stderr.write(f"noise line {n}\n")
sys.exit(1)
"""


def test_render_failure_reason_carries_redacted_browser_stderr(tmp_path: Path) -> None:
    from fakes import fake_secret

    script = tmp_path / "fakes" / "bad_browser.py"
    script.parent.mkdir()
    script.write_text(FAILING_BROWSER, encoding="utf-8")
    html = write(tmp_path, "page.html", "<html></html>")
    secret = fake_secret("github")
    status = visual.render_headless(html, tmp_path / "shot.png",
                                    browser_argv=[sys.executable, "-I", str(script), secret])
    assert status.startswith(visual.RENDER_FAILED + ":")
    assert "No usable sandbox" in status and "exit code 1" in status
    assert secret not in status
    assert "noise line 49" not in status, "only the first stderr lines"
    assert visual.is_render_failure(status) and not visual.is_render_failure(visual.RENDERED)
