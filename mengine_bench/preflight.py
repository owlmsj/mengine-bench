"""Run hygiene: block a run that could read other solutions; record personal instructions.

Earlier runs' workspaces next to this one hold other agents' solutions (gold
contamination), so a run refuses to start while any is left on disk.

Agent harnesses also load instruction files on their own: Claude Code reads
~/.claude/CLAUDE.md and every CLAUDE.md above its cwd, Codex reads
~/.codex/AGENTS.md, opencode reads ~/.config/opencode/AGENTS.md and
~/.claude/CLAUDE.md, and they read AGENTS.md above the cwd. Since #23 those
are part of the configuration under test: they are warnings, recorded by file
name only in result.json `config.personal_instructions`, never a block.
"""

from __future__ import annotations

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
    candidates = {
        "claude": [claude_home / "CLAUDE.md"],
        "codex": [codex_home / "AGENTS.md", codex_home / "AGENTS.override.md"],
        "opencode": [config_home / "opencode" / "AGENTS.md", claude_home / "CLAUDE.md"],
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
