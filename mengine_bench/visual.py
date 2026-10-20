"""Headless Chromium screenshots of a task's HTML deliverable.

Only the maintainer's `mengine-bench judge` renders (#23): runs grade visual
tasks on deterministic content gates, so contributors need no browser and the
render never changes CHECKS. The judge sees the screenshot for the
rendered-look part of its rubric; a blank or failed render scores 0 there.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import tempfile
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import IO

import psutil

from mengine_bench.redact import PathScope, local_names, redact_paths, redact_text
from mengine_bench.runner.process import kill_tree

RENDERED = "rendered"
NO_BROWSER = "no browser"
RENDER_FAILED = "render failed"
# Chromium-family executables share the --headless/--screenshot flags.
BROWSER_NAMES = ("msedge", "microsoft-edge", "microsoft-edge-stable", "chrome", "google-chrome",
                 "google-chrome-stable", "chromium", "chromium-browser")
RENDER_TIMEOUT_S = 120
# Edge's launcher exits before its helpers release the profile cache.
BROWSER_EXIT_WAIT_S = 5.0
PROFILE_REMOVE_ATTEMPTS = 10
PROFILE_REMOVE_DELAY_S = 0.5
STDERR_REASON_LINES = 8
STDERR_REASON_LINE_CHARS = 300
# SwiftShader keeps WebGL scenes rendering on GPU-less hosts; the virtual
# time budget lets animation loops and fonts settle before the capture.
_HEADLESS_FLAGS = ("--headless=new", "--no-first-run", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
                   "--hide-scrollbars", "--window-size=1440,900", "--virtual-time-budget=8000")
# Containers have a tiny /dev/shm and no GPU; headless Chrome on Ubuntu
# failed to screenshot without these.
_LINUX_FLAGS = ("--disable-dev-shm-usage", "--disable-gpu")


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


def screenshot_has_content(png: Path, min_bytes: int) -> bool:
    # A blank or black page compresses to a tiny PNG; a real layout does not.
    return png.is_file() and png.stat().st_size >= min_bytes
