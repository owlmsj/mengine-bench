"""Visual grading: browser discovery, gates, judge hook and 0.7 vote ratio."""

from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

import pytest

from mengine_bench import visual
from mengine_bench.core import write
from mengine_bench.tasks import visual as visual_tasks

CHECKLIST = ("style ok", "palette ok", "no overlap", "cta visible", "grid ok")
MANDATORY = frozenset({"no overlap", "cta visible"})
DETERMINISTIC = [("file exists", True)]


def fake_render(html: Path, png: Path) -> str:
    png.parent.mkdir(parents=True, exist_ok=True)
    png.write_bytes(b"\x89PNG" + b"0" * 20_000)
    return visual.RENDERED


def judge_failing(*items: str) -> visual.VisionJudge:
    def judge(png: Path, checklist: Sequence[str]) -> dict[str, bool]:
        return {item: item not in items for item in checklist}
    return judge


def grade(tmp_path: Path, judge: visual.VisionJudge, deterministic: list[tuple[str, bool]] = DETERMINISTIC):
    write(tmp_path, "page.html", "<html></html>")
    return visual.grade(tmp_path, "page.html", deterministic, CHECKLIST, MANDATORY, 10_000,
                        render=fake_render, judge=judge)


def test_all_items_pass(tmp_path: Path) -> None:
    result = grade(tmp_path, judge_failing())
    assert result.passed and result.flags == []


def test_mandatory_visual_item_cannot_be_outvoted(tmp_path: Path) -> None:
    result = grade(tmp_path, judge_failing("cta visible"))
    assert not result.passed and "vision: cta visible" in result.failed()


def test_failed_deterministic_gate_blocks(tmp_path: Path) -> None:
    assert not grade(tmp_path, judge_failing(), [("file exists", False)]).passed


def test_blank_screenshot_gates(tmp_path: Path) -> None:
    def tiny_render(html: Path, png: Path) -> str:
        png.parent.mkdir(parents=True, exist_ok=True)
        png.write_bytes(b"\x89PNG")
        return visual.RENDERED

    write(tmp_path, "page.html", "<html></html>")
    result = visual.grade(tmp_path, "page.html", DETERMINISTIC, CHECKLIST, MANDATORY, 10_000,
                          render=tiny_render, judge=judge_failing())
    assert not result.passed


def test_no_browser_grades_deterministic_only_and_flags(tmp_path: Path) -> None:
    write(tmp_path, "page.html", "<html></html>")
    result = visual.grade(tmp_path, "page.html", DETERMINISTIC, CHECKLIST, MANDATORY, 10_000,
                          render=lambda html, png: visual.NO_BROWSER, judge=judge_failing())
    assert result.passed and result.flags == ["no browser"]


def test_unavailable_judge_flags_and_keeps_screenshot_gate(tmp_path: Path) -> None:
    result = grade(tmp_path, visual.unavailable_judge)
    assert result.passed and result.flags == ["no judge"]
    assert ("screenshot rendered with content", True) in result.mandatory


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


# R10 (release review): without a browser or a vision judge the textual gates
# alone scored 100. The run's grading profile is now explicit and an
# unrendered visual task can never count as solved.
@pytest.mark.parametrize("render, judge, flag", [
    (lambda html, png: visual.NO_BROWSER, judge_failing(), "no browser"),
    (fake_render, visual.unavailable_judge, "no judge"),
])
def test_unrendered_profile_caps_visual_tasks(tmp_path: Path, render: visual.Renderer,
                                              judge: visual.VisionJudge, flag: str) -> None:
    write(tmp_path, "page.html", "<html></html>")
    result = visual.grade(tmp_path, "page.html", DETERMINISTIC, CHECKLIST, MANDATORY, 10_000,
                          render=render, judge=judge)
    assert visual.enforce_rendered_profile(result) == visual.PROFILE_UNRENDERED
    assert not result.passed and (visual.PROFILE_CHECK, False) in result.mandatory
    assert result.flags == [flag, visual.PROFILE_UNRENDERED]
    assert visual.enforce_rendered_profile(result) == visual.PROFILE_UNRENDERED
    assert result.mandatory.count((visual.PROFILE_CHECK, False)) == 1, "idempotent"


def test_rendered_profile_leaves_judged_tasks_alone(tmp_path: Path) -> None:
    result = grade(tmp_path, judge_failing())
    assert visual.enforce_rendered_profile(result) == visual.PROFILE_RENDERED
    assert result.passed and result.flags == []
    from mengine_bench.core import CheckResult
    assert visual.enforce_rendered_profile(CheckResult()) is None, "non-visual tasks have no profile"


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


VISUAL_REFERENCE_AGENT = """
import sys
from pathlib import Path
from mengine_bench import catalog
task = next(t for t in catalog.all_tasks() if t.id == "web-mondrian-landing")
sys.stdout.write(task.reference(Path(sys.argv[1]))[-1] or "done")
"""


def test_no_browser_run_is_recorded_unrendered(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import json
    import sys

    from mengine_bench import cli

    script = tmp_path / "fakes" / "visual_ref.py"
    script.parent.mkdir(parents=True)
    script.write_text(VISUAL_REFERENCE_AGENT, encoding="utf-8")
    monkeypatch.setattr(visual, "RENDER", lambda html, png: visual.NO_BROWSER)
    out = tmp_path / "r"
    template = json.dumps([sys.executable, str(script), "{workspace}", "{prompt_file}"])
    assert cli.main(["run", "--agent", "cmd", "--cmd", template, "--model", "fake/ref",
                     "--tasks", "web-mondrian-landing", "--out", str(out), "--work", str(tmp_path / "w")]) == 0
    [bundle] = out.glob("*")
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    assert result["grading"] == {"visual": "unrendered"}
    [task] = result["tasks"]
    assert task["passed"] is False and task["c"] == 0.0
    assert "unrendered" in task["flags"]
    assert result["totals"]["solved"] == 0
    assert "visual grading: unrendered" in (bundle / "summary.md").read_text(encoding="utf-8")


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
