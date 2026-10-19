"""Run hygiene: refuse to start a run that could be contaminated.

Agent harnesses load instruction files on their own: Claude Code reads
~/.claude/CLAUDE.md and every CLAUDE.md above its cwd, Codex reads
~/.codex/AGENTS.md, opencode reads ~/.config/opencode/AGENTS.md and
~/.claude/CLAUDE.md, and both read AGENTS.md above the cwd. Personal
instructions there would steer the run and leak into its transcripts. Earlier
runs' workspaces next to this one hold other agents' solutions. A run starts
only when none of these exist, or with --allow-unclean, which records them in
result.json so the run is listed apart.
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


def ancestor_problems(work: Path) -> list[str]:
    """Instruction files or a git checkout in `work` or any directory above it."""
    problems: list[str] = []
    for folder in (work, *work.parents):
        problems += [f"instruction file above the workspaces: {folder / name}"
                     for name in INSTRUCTION_FILES if (folder / name).is_file()]
        if (folder / ".git").exists():
            problems.append(f"workspaces inside a git checkout: {folder}")
    return problems


def leftover_runs(scratch: Path, work: Path, temp: Path) -> list[Path]:
    """Earlier runs' dirs an agent could read: bench scratch runs and fresh-session workspaces."""
    runs = scratch / "runs"
    found = [path for path in runs.iterdir() if path.resolve() != work.resolve()] if runs.is_dir() else []
    return found + sorted(temp.glob(FRESH_PREFIX + "*"))


def contamination(agent: str, work: Path, scratch: Path, home: Path | None = None,
                  env: Mapping[str, str] | None = None) -> list[str]:
    """Every reason this run would not start clean; empty when clean."""
    env = {} if env is None else env
    home = Path.home() if home is None else home
    problems = [f"{agent} global instructions: {path}" for path in global_instruction_files(agent, home, env)]
    problems += ancestor_problems(work.resolve())
    problems += [f"earlier run left on disk: {path}"
                 for path in leftover_runs(scratch, work, Path(tempfile.gettempdir()))]
    return problems
