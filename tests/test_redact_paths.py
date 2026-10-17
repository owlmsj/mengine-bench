"""Local path and identity redaction: user names must not reach a bundle.

Every name here is built at runtime; no real account or host name is a literal.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

from mengine_bench.redact import LocalNames, PathScope, find_path_leaks, redact_paths


def fake_name(prefix: str) -> str:
    return prefix + uuid.uuid4().hex[:8]


def test_home_path_in_every_escaping_form_is_redacted() -> None:
    name = fake_name("u")
    raw = f"C:\\Users\\{name}\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe"
    once = json.dumps({"shell": raw})
    twice = json.dumps({"line": once})
    line = " | ".join([raw, once, twice, f"d:/users/{name}/x", f"/home/{name}/repo", f"/Users/{name}/repo",
                       f"\\/home\\/{name}\\/repo"])
    assert sum(find_path_leaks(line).values()) >= 7
    cleaned = redact_paths(line, PathScope())
    assert name not in cleaned
    assert cleaned.count("<HOME>") == 7
    assert "<HOME>\\AppData\\Local" in cleaned and "<HOME>\\\\\\\\AppData" in cleaned
    assert find_path_leaks(cleaned) == {}
    inner = json.loads(json.loads(redact_paths(twice, PathScope()))["line"])
    assert inner["shell"] == "<HOME>\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe"


def test_run_dirs_become_workspace_and_workdir_labels(tmp_path: Path) -> None:
    work = tmp_path / "runs" / "stamp"
    workspace = work / "some-task" / "step-0"
    text = json.dumps({"cwd": str(workspace / "src"), "log": str(work / "some-task" / "transcripts")})
    text += "\n" + str(workspace).replace("\\", "/") + "\n" + str(workspace).upper()
    cleaned = redact_paths(text, PathScope(workspaces=(workspace,), workdirs=(work,)))
    assert str(tmp_path) not in cleaned and tmp_path.name not in cleaned
    assert cleaned.count("<WORKSPACE>") == 3
    assert "<WORKDIR>" in cleaned and "some-task" in cleaned


def test_user_and_host_are_redacted_as_whole_tokens_only() -> None:
    user, host = fake_name("usr"), fake_name("box")
    names = LocalNames(user=user, host=host)
    text = f"logged in as {user} on {host}.local; pre{user} {user}x {user.upper()}"
    cleaned = redact_paths(text, PathScope(names=names))
    assert cleaned == f"logged in as <USER> on <HOST>.local; pre{user} {user}x <USER>"
    assert find_path_leaks(text, names) == {"user": 2, "host": 1}
    assert find_path_leaks(cleaned, names) == {}


def test_short_or_generic_names_are_not_tokens() -> None:
    names = LocalNames(user="ab", host="localhost")
    text = "ab test on localhost"
    assert redact_paths(text, PathScope(names=names)) == text


def test_ordinary_text_is_untouched() -> None:
    text = "see https://example.com/home/page and /usr/bin/env, C:\\Program Files\\x, ~/notes, <HOME>/a"
    assert redact_paths(text, PathScope()) == text
    assert find_path_leaks(text) == {}
