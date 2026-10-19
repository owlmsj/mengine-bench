"""Visual grading: headless screenshot, deterministic gates and a vision-judge hook.

Ported from the private suite's visual.py. The renderer and the judge are
module-level hooks so tests inject fakes and the runner slice installs the real
judge adapter; nothing here calls a model. Deterministic checks gate the task
(a broken render or missing content cannot be outvoted by style), and
the aesthetic checklist passes at PASS_RATIO of the judge's majority votes.

Grading profile (release review R10): `grade` without a browser or a judge
falls back to the deterministic gates, which is right for gold self-tests,
but a run graded that way never saw the page. The runner calls
`enforce_rendered_profile` on every real run, which marks such a task
"unrendered" with a failing mandatory check: not solved, c capped at 0.5.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import tempfile
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import IO, Protocol

import psutil

from mengine_bench.core import CheckResult
from mengine_bench.redact import PathScope, local_names, redact_paths, redact_text
from mengine_bench.runner.process import kill_tree

PASS_RATIO = 0.7
RENDERED = "rendered"
NO_BROWSER = "no browser"
RENDER_FAILED = "render failed"
NO_JUDGE = "no judge"
SCREENSHOT_CHECK = "screenshot rendered with content"
# Chromium-family executables share the --headless/--screenshot flags.
BROWSER_NAMES = ("msedge", "microsoft-edge", "microsoft-edge-stable", "chrome", "google-chrome",
                 "google-chrome-stable", "chromium", "chromium-browser")
RENDER_TIMEOUT_S = 120
# Edge's launcher exits before its helpers release the profile cache.
BROWSER_EXIT_WAIT_S = 5.0
PROFILE_REMOVE_ATTEMPTS = 10
PROFILE_REMOVE_DELAY_S = 0.5
PROFILE_RENDERED = "rendered"
PROFILE_UNRENDERED = "unrendered"
PROFILE_CHECK = "graded rendered: browser screenshot and vision judge"
_UNRENDERED_CAUSES = (NO_BROWSER, NO_JUDGE)
STDERR_REASON_LINES = 8
STDERR_REASON_LINE_CHARS = 300
# SwiftShader keeps WebGL scenes rendering on GPU-less hosts; the virtual
# time budget lets animation loops and fonts settle before the capture.
_HEADLESS_FLAGS = ("--headless=new", "--no-first-run", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
                   "--hide-scrollbars", "--window-size=1440,900", "--virtual-time-budget=8000")
# Containers have a tiny /dev/shm and no GPU; headless Chrome on Ubuntu
# failed to screenshot without these.
_LINUX_FLAGS = ("--disable-dev-shm-usage", "--disable-gpu")


class JudgeUnavailable(RuntimeError):
    """No vision judge configured: the task is graded on deterministic checks only."""


class VisionJudge(Protocol):
    def __call__(self, png: Path, checklist: Sequence[str]) -> dict[str, bool]: ...


Renderer = Callable[[Path, Path], str]


@dataclass(frozen=True)
class PendingVision:
    """A rendered screenshot no judge has seen yet: what `mengine-bench judge`
    needs to finish the visual grade later (judge/<task>.json and .png)."""

    png: Path
    checklist: tuple[str, ...]
    mandatory_items: tuple[str, ...]
    deterministic: tuple[tuple[str, bool], ...]
    screenshot_ok: bool

    def record(self) -> dict[str, object]:
        return {"checklist": list(self.checklist), "mandatory_items": list(self.mandatory_items),
                "deterministic": [[name, ok] for name, ok in self.deterministic], "screenshot_ok": self.screenshot_ok}


@dataclass
class VisualCheckResult(CheckResult):
    # Degraded grading modes ("no browser", "no judge") are reported, not hidden.
    flags: list[str] = field(default_factory=list)
    pending_vision: PendingVision | None = None


def browser_install_candidates(system: str | None = None, env: Mapping[str, str] | None = None) -> list[Path]:
    """Standard Edge/Chrome/Chromium install paths, for hosts where they are not on PATH."""
    system = system or platform.system()
    env = os.environ if env is None else env
    if system == "Windows":
        bases = [env[key] for key in ("ProgramFiles(x86)", "ProgramFiles", "LOCALAPPDATA") if env.get(key)]
        apps = (("Microsoft", "Edge", "Application", "msedge.exe"), ("Google", "Chrome", "Application", "chrome.exe"),
                ("Chromium", "Application", "chrome.exe"))
        return [Path(base, *app) for app in apps for base in bases]
    if system == "Darwin":
        return [Path(f"/Applications/{app}.app/Contents/MacOS/{app}")
                for app in ("Microsoft Edge", "Google Chrome", "Chromium")]
    return [Path(path) for path in ("/opt/microsoft/msedge/msedge", "/opt/google/chrome/chrome",
                                    "/usr/bin/chromium", "/usr/bin/chromium-browser", "/snap/bin/chromium")]


def find_browser() -> str | None:
    """MENGINE_BENCH_BROWSER, then PATH, then the standard install locations."""
    override = os.environ.get("MENGINE_BENCH_BROWSER")
    if override:
        return override
    for name in BROWSER_NAMES:
        found = shutil.which(name)
        if found:
            return found
    for candidate in browser_install_candidates():
        if candidate.is_file():
            return str(candidate)
    return None


def headless_browser_flags(system: str, is_root: bool) -> list[str]:
    """Chromium flags for one OS, without the per-call profile, screenshot and URL."""
    if system != "Linux":
        return list(_HEADLESS_FLAGS)
    flags = [*_HEADLESS_FLAGS, *_LINUX_FLAGS]
    # Chrome refuses to start as root with the sandbox; desktops keep it.
    if is_root:
        flags.append("--no-sandbox")
    return flags


def _running_as_root() -> bool:
    geteuid = getattr(os, "geteuid", None)
    return geteuid is not None and geteuid() == 0


def is_render_failure(status: str) -> bool:
    return status == RENDER_FAILED or status.startswith(RENDER_FAILED + ":")


def render_headless(html: Path, png: Path, browser_argv: Sequence[str] | None = None) -> str:
    """Screenshot `html` at 1440x900; returns RENDERED, NO_BROWSER or a RENDER_FAILED reason.

    A failure reads "render failed: <cause>" so the run log explains itself.
    `browser_argv` replaces the discovered browser executable (tests use a fake).
    """
    if not html.is_file():
        return f"{RENDER_FAILED}: no html file {html.name}"
    if browser_argv is None:
        browser = find_browser()
        if browser is None:
            return NO_BROWSER
        browser_argv = [browser]
    png.parent.mkdir(parents=True, exist_ok=True)
    # The profile lives in system temp, never in the workspace: a browser
    # helper still holding its cache made archiving the workspace fail.
    profile = Path(tempfile.mkdtemp(prefix="mengine-bench-browser-"))
    try:
        return _screenshot(list(browser_argv), profile, html, png)
    finally:
        _stop_profile_processes(profile)
        _remove_profile(profile)


def _screenshot(browser_argv: list[str], profile: Path, html: Path, png: Path) -> str:
    flags = headless_browser_flags(platform.system(), _running_as_root())
    argv = [*browser_argv, *flags, f"--user-data-dir={profile}", f"--screenshot={png.resolve()}",
            html.resolve().as_uri()]
    # stderr goes to a file, not a pipe: orphaned helpers inherit the handle
    # and a pipe would never reach EOF while they live.
    with tempfile.TemporaryFile() as stderr_log:
        try:
            proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=stderr_log)
        except OSError as exc:
            return f"{RENDER_FAILED}: cannot start browser: {type(exc).__name__}"
        try:
            returncode = proc.wait(timeout=RENDER_TIMEOUT_S)
        except subprocess.TimeoutExpired:
            kill_tree(proc.pid)
            proc.wait()
            return _failure_reason(f"timeout after {RENDER_TIMEOUT_S}s", stderr_log, profile, html)
        if returncode:
            return _failure_reason(f"exit code {returncode}", stderr_log, profile, html)
        if not png.is_file():
            return _failure_reason("exit code 0 but no screenshot", stderr_log, profile, html)
    return RENDERED


def _failure_reason(cause: str, stderr_log: IO[bytes], profile: Path, html: Path) -> str:
    stderr_log.seek(0)
    lines = stderr_log.read().decode("utf-8", errors="replace").split("\n")
    head = [line.strip()[:STDERR_REASON_LINE_CHARS] for line in lines if line.strip()][:STDERR_REASON_LINES]
    scope = PathScope(workdirs=(profile, html.parent), names=local_names())
    stderr_text = redact_paths(redact_text(" | ".join(head)), scope)
    return f"{RENDER_FAILED}: {cause}; stderr: {stderr_text or '(empty)'}"


def _profile_processes(profile: Path) -> list[psutil.Process]:
    # Helpers outlive the launcher and are orphaned, so they are found by the
    # profile path on their command line, not by walking the launcher's tree.
    marker = str(profile)
    found = []
    for candidate in psutil.process_iter(["cmdline"]):
        try:
            cmdline = candidate.info["cmdline"] or []
        except (psutil.Error, KeyError):
            continue
        if any(marker in part for part in cmdline):
            found.append(candidate)
    return found


def _stop_profile_processes(profile: Path) -> None:
    lingering = _profile_processes(profile)
    if not lingering:
        return
    _gone, alive = psutil.wait_procs(lingering, timeout=BROWSER_EXIT_WAIT_S)
    for survivor in alive:
        kill_tree(survivor.pid)


def _remove_profile(profile: Path) -> None:
    # Windows releases file handles a moment after the process dies; a profile
    # that still resists stays in temp rather than failing the task.
    for _attempt in range(PROFILE_REMOVE_ATTEMPTS):
        shutil.rmtree(profile, ignore_errors=True)
        if not profile.exists():
            return
        time.sleep(PROFILE_REMOVE_DELAY_S)


def unavailable_judge(png: Path, checklist: Sequence[str]) -> dict[str, bool]:
    raise JudgeUnavailable(f"received no vision judge for {png.name}; expected one installed in visual.JUDGE")


def screenshot_has_content(png: Path, min_bytes: int) -> bool:
    # A blank or black page compresses to a tiny PNG; a real layout does not.
    return png.is_file() and png.stat().st_size >= min_bytes


RENDER: Renderer = render_headless
JUDGE: VisionJudge = unavailable_judge


def grade(ws: Path, html_rel: str, deterministic: list[tuple[str, bool]], checklist: Sequence[str],
          mandatory_items: frozenset[str], min_png_bytes: int,
          render: Renderer | None = None, judge: VisionJudge | None = None) -> VisualCheckResult:
    result = VisualCheckResult(pass_ratio=PASS_RATIO, mandatory=list(deterministic))
    png = ws / "_render" / "shot.png"
    status = (render or RENDER)(ws / html_rel, png)
    if status == NO_BROWSER:
        return _deterministic_only(result, deterministic, NO_BROWSER)
    rendered = status == RENDERED
    screenshot_ok = rendered and screenshot_has_content(png, min_png_bytes)
    result.mandatory.append((SCREENSHOT_CHECK, screenshot_ok))
    if not rendered:
        return _deterministic_only(result, deterministic, None)
    try:
        return judge_screenshot(png, deterministic, screenshot_ok, checklist, mandatory_items, judge or JUDGE)
    except JudgeUnavailable:
        degraded = _deterministic_only(result, deterministic, NO_JUDGE)
        degraded.pending_vision = PendingVision(png=png, checklist=tuple(checklist),
                                                mandatory_items=tuple(sorted(mandatory_items)),
                                                deterministic=tuple(deterministic), screenshot_ok=screenshot_ok)
        return degraded


def judge_screenshot(png: Path, deterministic: Sequence[tuple[str, bool]], screenshot_ok: bool,
                     checklist: Sequence[str], mandatory_items: frozenset[str],
                     judge: VisionJudge) -> VisualCheckResult:
    """The visual grade from a screenshot: deterministic gates, the screenshot
    gate, then the judge's checklist. Raises JudgeUnavailable without votes."""
    verdict = judge(png, checklist)
    result = VisualCheckResult(pass_ratio=PASS_RATIO,
                               mandatory=[*deterministic, (SCREENSHOT_CHECK, screenshot_ok)])
    for item in checklist:
        target = result.mandatory if item in mandatory_items else result.checks
        target.append((f"vision: {item}", verdict.get(item) is True))
    return result


def enforce_rendered_profile(check: CheckResult | None) -> str | None:
    """Grading profile of one task's check; None for non-visual tasks.

    Idempotent.
    """
    if not isinstance(check, VisualCheckResult):
        return None
    if not any(flag in _UNRENDERED_CAUSES for flag in check.flags):
        return PROFILE_RENDERED
    if PROFILE_UNRENDERED not in check.flags:
        check.mandatory.append((PROFILE_CHECK, False))
        check.flags.append(PROFILE_UNRENDERED)
    return PROFILE_UNRENDERED


def _deterministic_only(result: VisualCheckResult, deterministic: list[tuple[str, bool]],
                        flag: str | None) -> VisualCheckResult:
    # Mirror the gates as scored checks so correctness stays the share of
    # deterministic checks instead of an empty (zero) checklist.
    result.checks.extend(deterministic)
    if flag:
        result.flags.append(flag)
    return result
