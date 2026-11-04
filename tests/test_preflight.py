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


def test_opencode_does_not_publish_claude_global_instructions(tmp_path: Path) -> None:
    home = tmp_path / 'home'
    _touch(home / '.claude' / 'CLAUDE.md')
    _touch(home / '.config' / 'opencode' / 'AGENTS.md')
    work = tmp_path / 'project'
    _touch(work / 'AGENTS.md')
    found = preflight.personal_instructions('opencode', work, home=home)
    assert '~/.config/opencode/AGENTS.md' in found
    assert 'AGENTS.md above the workspaces' in found
    assert '~/.claude/CLAUDE.md' not in found


@pytest.mark.parametrize("version,expected", [("v22.18.0", []), ("v24.0.0", []),
    ("v22.17.9", ["node version 'v22.17.9'; expected >= 22.18"]),
    ("bad", ["node version 'bad'; expected >= 22.18"])])
def test_toolchain_node_version(monkeypatch, version, expected) -> None:
    from types import SimpleNamespace
    monkeypatch.setattr(preflight.shutil, "which", lambda name: name)
    monkeypatch.setattr(preflight.subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=version, returncode=0))
    assert preflight.toolchain_problems() == expected


def test_missing_toolchains(monkeypatch) -> None:
    monkeypatch.setattr(preflight.shutil, "which", lambda name: None)
    assert preflight.toolchain_problems() == ["cargo missing", "node missing", "git missing"]


def test_cli_toolchain_block_and_waiver(monkeypatch, capsys) -> None:
    from mengine_bench import cli
    monkeypatch.setattr(cli, "toolchain_problems", lambda: ["cargo missing"])
    monkeypatch.setattr(cli, "find_browser", lambda: None)
    argv = ["run", "--agent", "codex", "--model", "fake", "--tasks", "ds-ab-playtest"]
    with pytest.raises(SystemExit, match="cargo missing"):
        cli.main(argv)
    assert "page checks will be left out" in capsys.readouterr().out
    assert cli.main([*argv, "--dry-run", "--allow-missing-toolchain"]) == 0
    import json
    plan = json.loads(capsys.readouterr().out.splitlines()[-1])
    assert plan["config"]["allow_missing_toolchain"] == ["cargo missing"]


def test_git_bash_without_tmp_blocks_with_the_mounted_path_189(monkeypatch) -> None:
    from types import SimpleNamespace
    stale = "C:/Users/o/Code/mengine-bench/tmp/zerg-1793814340766940600-17972/tmp"
    monkeypatch.setattr(preflight.subprocess, "run", lambda *a, **k: SimpleNamespace(
        stdout=f"{stale} on /tmp type ntfs (binary,noacl,posix=0,usertemp)\n",
        stderr="bash.exe: warning: could not find /tmp, please create!\n", returncode=1))
    [problem] = preflight.shell_problems(Path("bash.exe"))
    assert "Git Bash has no usable /tmp" in problem and stale in problem and "stale" in problem
    monkeypatch.setattr(preflight.subprocess, "run", lambda *a, **k: SimpleNamespace(
        stdout="C:/Users/o/AppData/Local/Temp on /tmp type ntfs (binary,noacl,posix=0,usertemp)\n", stderr="",
        returncode=0))
    assert preflight.shell_problems(Path("bash.exe")) == []


def test_cli_blocks_on_a_broken_git_bash_without_waiver_189(monkeypatch, capsys) -> None:
    import json
    from mengine_bench import cli
    monkeypatch.setattr(cli, "toolchain_problems", lambda: [])
    monkeypatch.setattr(cli, "shell_problems", lambda: ["Git Bash has no usable /tmp (mounted from 'x')"])
    argv = ["run", "--agent", "codex", "--model", "fake", "--tasks", "ds-ab-playtest"]
    with pytest.raises(SystemExit, match="no usable /tmp"):
        cli.main([*argv, "--allow-missing-toolchain"])
    assert "preflight: Git Bash has no usable /tmp" in capsys.readouterr().out
    assert cli.main([*argv, "--dry-run"]) == 0
    plan = json.loads(capsys.readouterr().out.splitlines()[-1])
    assert plan["preflight"] == "blocked by the shell"
