"""Run hygiene: personal instructions, a git checkout or earlier runs block a run."""

from __future__ import annotations

from pathlib import Path

import pytest

from mengine_bench import preflight


def _touch(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x", encoding="utf-8")
    return path


@pytest.mark.parametrize(("agent", "relative"), [
    ("claude", ".claude/CLAUDE.md"),
    ("codex", ".codex/AGENTS.md"),
    ("opencode", ".config/opencode/AGENTS.md"),
    ("opencode", ".claude/CLAUDE.md"),
])
def test_global_instructions_of_the_harness_are_found(tmp_path: Path, agent: str, relative: str) -> None:
    found = _touch(tmp_path / "home" / relative)
    assert preflight.global_instruction_files(agent, tmp_path / "home", {}) == [found]


def test_global_instructions_follow_config_env_and_ignore_other_harnesses(tmp_path: Path) -> None:
    _touch(tmp_path / "home" / ".claude" / "CLAUDE.md")
    found = _touch(tmp_path / "codex-home" / "AGENTS.md")
    env = {"CODEX_HOME": str(tmp_path / "codex-home")}
    assert preflight.global_instruction_files("codex", tmp_path / "home", env) == [found]
    assert preflight.global_instruction_files("cmd", tmp_path / "home", env) == []


def test_instruction_files_and_git_above_the_workspaces_are_found(tmp_path: Path) -> None:
    _touch(tmp_path / "AGENTS.md")
    (tmp_path / "repo" / ".git").mkdir(parents=True)
    problems = preflight.ancestor_problems(tmp_path / "repo" / "runs" / "now")
    assert any("instruction file" in problem and "AGENTS.md" in problem for problem in problems)
    assert any("git checkout" in problem for problem in problems)


def test_earlier_runs_are_found_but_not_this_one(tmp_path: Path) -> None:
    scratch, temp = tmp_path / "scratch", tmp_path / "temp"
    old = scratch / "runs" / "20261019T000000Z"
    old.mkdir(parents=True)
    work = scratch / "runs" / "20261020T000000Z"
    work.mkdir()
    fresh = temp / f"{preflight.FRESH_PREFIX}abc"
    fresh.mkdir(parents=True)
    assert preflight.leftover_runs(scratch, work, temp) == [old, fresh]


def test_contamination_names_each_finding(tmp_path: Path) -> None:
    # Ancestors and the system temp dir are this machine's; only the faked parts are asserted.
    scratch, home = tmp_path / "scratch", tmp_path / "home"
    assert [p for p in preflight.contamination("claude", scratch / "runs" / "now", scratch, home=home, env={})
            if "global instructions" in p] == []
    _touch(home / ".claude" / "CLAUDE.md")
    (scratch / "runs" / "old").mkdir(parents=True)
    problems = preflight.contamination("claude", scratch / "runs" / "now", scratch, home=home, env={})
    assert f"claude global instructions: {home / '.claude' / 'CLAUDE.md'}" in problems
    assert f"earlier run left on disk: {scratch / 'runs' / 'old'}" in problems
