"""Run hygiene: earlier runs on disk block a run; personal instructions are recorded warnings (#23)."""

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
    found = preflight.ancestor_instructions(tmp_path / "repo" / "runs" / "now")
    assert "AGENTS.md above the workspaces" in found and "git checkout around the workspaces" in found


def test_earlier_runs_are_found_but_not_this_one(tmp_path: Path) -> None:
    scratch, temp = tmp_path / "scratch", tmp_path / "temp"
    old = scratch / "runs" / "20261019T000000Z"
    old.mkdir(parents=True)
    work = scratch / "runs" / "20261020T000000Z"
    work.mkdir()
    fresh = temp / f"{preflight.FRESH_PREFIX}abc"
    fresh.mkdir(parents=True)
    assert preflight.leftover_runs(scratch, work, temp) == [old, fresh]


def test_personal_instructions_are_file_names_only(tmp_path: Path) -> None:
    home, work = tmp_path / "home", tmp_path / "repo" / "runs" / "now"
    _touch(home / ".claude" / "CLAUDE.md")
    _touch(tmp_path / "repo" / "AGENTS.md")
    (tmp_path / "repo" / ".git").mkdir(parents=True)
    found = preflight.personal_instructions("claude", work, home=home, env={})
    assert found[:3] == ["~/.claude/CLAUDE.md", "AGENTS.md above the workspaces", "git checkout around the workspaces"]
    assert not any(str(tmp_path) in item or "\\" in item for item in found), found


def test_only_earlier_runs_block(tmp_path: Path) -> None:
    scratch, temp = tmp_path / "scratch", tmp_path / "temp"
    temp.mkdir()
    work = scratch / "runs" / "now"
    assert preflight.blocking_problems(scratch, work, temp) == []
    (scratch / "runs" / "old").mkdir(parents=True)
    assert preflight.blocking_problems(scratch, work, temp) == [f"earlier run left on disk: {scratch / 'runs' / 'old'}"]
    assert not hasattr(preflight, "contamination")
