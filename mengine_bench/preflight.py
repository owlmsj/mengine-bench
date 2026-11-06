"""Run hygiene: block a run that could read other solutions; record personal instructions.

Earlier runs' workspaces next to this one hold other agents' solutions (gold
contamination), so a run refuses to start while any is left on disk.

Agent harnesses also load instruction files on their own: Claude Code reads
~/.claude/CLAUDE.md and every CLAUDE.md above its cwd, Codex reads
~/.codex/AGENTS.md, opencode reads ~/.config/opencode/AGENTS.md, pi reads
~/.pi/agent/AGENTS.md, and they read the project's AGENTS.md. Since #23 those
are part of the configuration under test: they are warnings, recorded by file
name only in result.json `config.personal_instructions`, never a block.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from collections.abc import Mapping
from pathlib import Path

INSTRUCTION_FILES = ("CLAUDE.md", "CLAUDE.local.md", "AGENTS.md", "AGENTS.override.md")
FRESH_PREFIX = "mengine-bench-fresh-"


def global_instruction_files(agent: str, home: Path, env: Mapping[str, str]) -> list[Path]:
    """The harness's user-level instruction files that exist on this machine."""
    claude_home = Path(env.get("CLAUDE_CONFIG_DIR") or home / ".claude")
    codex_home = Path(env.get("CODEX_HOME") or home / ".codex")
    config_home = Path(env.get("XDG_CONFIG_HOME") or home / ".config")
    pi_home = Path(env.get("PI_CODING_AGENT_DIR") or home / ".pi" / "agent")
    candidates = {
        "claude": [claude_home / "CLAUDE.md"],
        "codex": [codex_home / "AGENTS.md", codex_home / "AGENTS.override.md"],
        "opencode": [config_home / "opencode" / "AGENTS.md"],
        "agy": [home / ".gemini" / "GEMINI.md"],
        # pi 1.5.0 docs/configuration.md:18-20; AGENTS.MD and CLAUDE.MD name the same files on Windows.
        "pi": [pi_home / name for name in ("AGENTS.override.md", "AGENTS.md", "CLAUDE.md", "SYSTEM.md",
                                           "APPEND_SYSTEM.md")],
    }.get(agent, [])
    return [path for path in candidates if path.is_file()]


def _public_name(path: Path, home: Path) -> str:
    # Published in result.json: a home-relative name, never the user's full path.
    try:
        return "~/" + path.resolve().relative_to(home.resolve()).as_posix()
    except ValueError:
        return path.name


def ancestor_instructions(work: Path) -> list[str]:
    """Instruction files or a git checkout in `work` or any directory above it, by name only."""
    found: list[str] = []
    for folder in (work, *work.parents):
        found += [f"{name} above the workspaces" for name in INSTRUCTION_FILES if (folder / name).is_file()]
        if (folder / ".git").exists():
            found.append("git checkout around the workspaces")
    return found


def personal_instructions(agent: str, work: Path, home: Path | None = None,
                          env: Mapping[str, str] | None = None) -> list[str]:
    """Warnings for result.json `config.personal_instructions`; empty when none apply."""
    env = {} if env is None else env
    home = Path.home() if home is None else home
    found = [_public_name(path, home) for path in global_instruction_files(agent, home, env)]
    return found + ancestor_instructions(work.resolve())


def leftover_runs(scratch: Path, work: Path, temp: Path) -> list[Path]:
    """Earlier runs' dirs an agent could read: bench scratch runs and fresh-session workspaces."""
    runs = scratch / "runs"
    found = [path for path in runs.iterdir() if path.resolve() != work.resolve()] if runs.is_dir() else []
    return found + sorted(temp.glob(FRESH_PREFIX + "*"))


def blocking_problems(scratch: Path, work: Path, temp: Path | None = None) -> list[str]:
    """Every reason this run must not start; empty when it may."""
    temp = Path(tempfile.gettempdir()) if temp is None else temp
    return [f"earlier run left on disk: {path}" for path in leftover_runs(scratch, work, temp)]


def toolchain_problems() -> list[str]:
    """#185: missing build tools block a run before any agent starts."""
    problems = [f"{name} missing" for name in ("cargo", "node", "git") if shutil.which(name) is None]
    node = shutil.which("node")
    if node is None:
        return problems
    try:
        result = subprocess.run([node, "--version"], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as error:
        return [*problems, f"node version unavailable: {error}; expected >= 22.18"]
    version = result.stdout.strip()
    match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", version)
    if result.returncode or match is None or tuple(map(int, match.groups())) < (22, 18, 0):
        problems.append(f"node version {version!r}; expected >= 22.18")
    return problems


TMP_WARNING = "could not find /tmp"


def git_bash() -> Path | None:
    """The Git Bash the Windows harnesses run tools with: CLAUDE_CODE_GIT_BASH_PATH, else bin/bash.exe beside git."""
    named = os.environ.get("CLAUDE_CODE_GIT_BASH_PATH")
    if named:
        return Path(named)
    git = shutil.which("git")
    if git is None:
        return None
    # git may be Git/cmd/git.exe or Git/mingw64/bin/git.exe; the bash lives in Git/bin either way.
    for folder in Path(git).resolve().parents:
        if (folder / "bin" / "bash.exe").is_file():
            return folder / "bin" / "bash.exe"
    return None


def shell_problems(bash: Path | None = None) -> list[str]:
    """#189: Git Bash without a usable /tmp blocks a run.

    A long-lived MSYS process keeps the shared mount table alive; when it started while TEMP pointed at a directory
    since deleted, every new bash warns "could not find /tmp" and the agent under test has no /tmp (156 warnings and
    a hung task in one Opus run). The owner fixes the host: end the stale process or recreate the directory.
    """
    bash = git_bash() if bash is None else bash
    if bash is None:
        return []
    try:
        result = subprocess.run([str(bash), "-c", "mount | grep ' /tmp '; test -d /tmp"], capture_output=True,
                                text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired) as error:
        return [f"Git Bash check failed: {error}; expected `bash -c 'test -d /tmp'` to run"]
    if result.returncode == 0 and TMP_WARNING not in result.stderr:
        return []
    mounted = result.stdout.strip().split(" on /tmp")[0] or "no /tmp mount"
    return [f"Git Bash has no usable /tmp (mounted from {mounted!r}); expected an existing directory: end the stale "
            "MSYS processes (bash, ssh) that pin the mount table, or create that directory, then run again"]
