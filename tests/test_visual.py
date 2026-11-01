"""Visual tasks: deterministic content gates at run time; the headless render serves only the maintainer's judge."""

from __future__ import annotations

import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

from mengine_bench import catalog, visual
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


@pytest.mark.skipif(visual.find_browser() is None, reason="no Chromium-family browser on PATH")
def test_reference_landing_renders_with_content(tmp_path: Path) -> None:
    html = write(tmp_path, visual_tasks.LANDING, visual_tasks.LANDING_REFERENCE)
    png = tmp_path / "_render" / "shot.png"
    assert visual.render_headless(html, png) == visual.RENDERED
    assert png.stat().st_size >= 10_000


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
                     "--hide-scrollbars", "--window-size=1440,900", "--virtual-time-budget=8000",
                     visual.RENDER_HOST_RULES]


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


@pytest.mark.parametrize("system", ["Windows", "Linux", "Darwin"])
def test_the_judge_render_reaches_only_the_pinned_cdn_and_fonts(system: str) -> None:
    # A contributor's page runs on the maintainer's machine (#23 review): every
    # host but the three.js CDN and Google Fonts fails to resolve.
    [rules] = [flag for flag in visual.headless_browser_flags(system, is_root=False)
               if flag.startswith("--host-resolver-rules=")]
    assert rules.startswith("--host-resolver-rules=MAP * ~NOTFOUND")
    for host in ("cdn.jsdelivr.net", "fonts.googleapis.com", "fonts.gstatic.com"):
        assert f"EXCLUDE {host}" in rules


@pytest.mark.parametrize("task_id", ["web-mondrian-landing", "3d-voxel-landscape"])
def test_a_commented_out_page_earns_no_checks(task_id: str, tmp_path: Path) -> None:
    # Content inside <!-- --> never renders, so it must not pass content gates (#23 review).
    task = next(t for t in catalog.all_tasks() if t.id == task_id)
    task.setup(tmp_path)
    task.reference(tmp_path)
    page = tmp_path / str(task.render_target)
    page.write_text("<!doctype html><html><body><!--\n" + page.read_text(encoding="utf-8").replace("-->", "")
                    + "\n--></body></html>" + " " * 2500, encoding="utf-8")
    result = task.check(tmp_path, [""])
    assert result.score == 0.0 and not result.passed


def test_source_link_may_space_around_the_equals_sign(tmp_path: Path) -> None:
    task = next(t for t in catalog.all_tasks() if t.id == "web-mondrian-landing")
    task.setup(tmp_path)
    answers = task.reference(tmp_path)
    page = tmp_path / "landing" / "index.html"
    page.write_text(page.read_text(encoding="utf-8").replace("href=", "href = "), encoding="utf-8")
    assert task.check(tmp_path, answers).passed


# #28 B4: a compact but complete page (794 visible chars) earns every check.
COMPACT_LANDING = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Mondrian 1930</title>
<style>body{margin:0;font-family:sans-serif;background:#111}main{display:grid;grid-template-columns:2fr 1fr;gap:10px;padding:10px}
section{background:#fff;padding:20px}.r{background:#d40920}.b{background:#1356a2;color:#fff}.y{background:#f7d842}</style></head>
<body><main><section class="r"><h1>Composition with Red, Blue and Yellow</h1><p>Painted by Piet Mondrian in 1930.</p></section>
<section class="y"><h2>De Stijl</h2><p>A Dutch movement of straight lines and primary colours, founded in 1917.</p></section>
<section class="b"><h2>Why it matters</h2><p>Its asymmetric balance shaped modern design.</p>
<button>See it</button> <a href="https://en.wikipedia.org/wiki/Composition_with_Red,_Blue_and_Yellow">Source</a></section>
</main></body></html>
"""
NAME = "Composition with Red, Blue and Yellow"


@pytest.mark.parametrize("edit,failed", [
    (lambda page: page.replace(f"<h1>{NAME}</h1>",
                               "<h1>Composition with <span>Red</span>, <span>Blue</span> and <span>Yellow</span></h1>")
     .replace(f"<title>{NAME}</title>", "<title>Mondrian 1930</title>"), []),
    (lambda page: page.replace("Piet Mondrian", "Piet <em>Mondrian</em>"), []),
    (lambda page: page.replace('<a class="cta"', "<a class='cta'"), []),
    (lambda page: page.replace('_Blue_and_Yellow">Read', "_Blue_and_Yellow/\">Read"), []),
    (lambda page: page.replace('_Blue_and_Yellow">Read', "_Blue_and_Yellow?lang=en'>Read")
     .replace('href="https://en.wikipedia.org/wiki/Composition', "href='https://en.wikipedia.org/wiki/Composition"),
     []),
    (lambda page: COMPACT_LANDING, []),
    # Wrong pages stay wrong.
    (lambda page: page.replace('_Blue_and_Yellow">Read', '_Blue_and_Yellow_II">Read'),
     ["links to the fact sheet's source"]),
    (lambda page: re.sub(r"<style>.*?</style>", "<style>body{font-family:sans-serif;color:#555;background:#eee}"
                                                "</style>", page, flags=re.S),
     ["CSS with the Mondrian palette (red, blue, yellow, black)"]),
])
def test_landing_accepts_legitimate_markup_but_not_missing_facts(
        tmp_path: Path, edit: Callable[[str], str], failed: list[str]) -> None:
    LANDING.setup(tmp_path)
    answers = LANDING.reference(tmp_path)
    page = tmp_path / visual_tasks.LANDING
    page.write_text(edit(page.read_text(encoding="utf-8")), encoding="utf-8")
    result = LANDING.check(tmp_path, answers)
    assert result.mandatory_ok and result.failed() == failed


IMPORT_CHECK = "imports three.js 0.170.0 from the CDN"
ASSET_CHECK = "no external models or textures"
SCENE_END = "</script></body></html>"


def _low_poly_as(geometry: str) -> Callable[[str], str]:
    return lambda page: page.replace("BoxGeometry", geometry).replace(", flatShading: true", "")


@pytest.mark.parametrize("edit,failed", [
    # #28 B5: other low poly primitives and a download link are legitimate.
    *((_low_poly_as(f"{shape}Geometry"), []) for shape in ("Cone", "Cylinder", "Icosahedron", "Dodecahedron",
                                                            "Tetrahedron")),
    (lambda page: page.replace(SCENE_END, '</script><a download="fuji.png" href="fuji.png">Save</a></body></html>'),
     []),
    (lambda page: page.replace("renderer.setAnimationLoop", 'const shot = "fuji.png";\nrenderer.setAnimationLoop'),
     []),
    # The judge render resolves only jsDelivr, so unpkg would check but render blank.
    # The judge render resolves Google Fonts too (#28 review).
    (lambda page: page.replace("overflow:hidden;", "overflow:hidden;}@import url(https://fonts.googleapis.com/css2"
                               "?family=Inter);x{"), []),
    (lambda page: page.replace("cdn.jsdelivr.net/npm/three@", "unpkg.com/three@"), [IMPORT_CHECK]),
    (lambda page: page.replace("renderer.setAnimationLoop", 'new THREE.TextureLoader().load("https://example.org/sky.webp");'
                               "\nrenderer.setAnimationLoop"), [ASSET_CHECK]),
    (lambda page: page.replace("renderer.setAnimationLoop", "loader.load('models/fuji.glb', g => scene.add(g.scene));"
                               "\nrenderer.setAnimationLoop"), [ASSET_CHECK]),
    (lambda page: page.replace("<body>", '<body><img src="sky.jpg" alt="">'), [ASSET_CHECK]),
    (lambda page: page.replace("overflow:hidden;", "overflow:hidden;background-image:url(https://example.org/sky);"),
     [ASSET_CHECK]),
])
def test_scene_accepts_low_poly_forms_but_not_external_assets(
        tmp_path: Path, edit: Callable[[str], str], failed: list[str]) -> None:
    answers = SCENE.reference(tmp_path)
    page = tmp_path / visual_tasks.SCENE
    page.write_text(edit(page.read_text(encoding="utf-8")), encoding="utf-8")
    result = SCENE.check(tmp_path, answers)
    assert result.mandatory_ok and result.failed() == failed
