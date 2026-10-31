"""Secret and image-blob redaction for published transcripts."""

from __future__ import annotations

import base64
import hashlib
import json

import pytest

from fakes import KINDS, MARKER, fake_secret
from mengine_bench.redact import (
    LocalNames, PathScope, find_leaks, find_secrets, redact_paths, redact_text, secret_env_values,
)


@pytest.mark.parametrize("kind", KINDS)
def test_planted_secret_is_found_and_redacted(kind: str) -> None:
    secret = fake_secret(kind)
    assert MARKER in secret
    text = f"line before\nagent saw {secret} in the env\nline after"
    assert find_secrets(text), f"{kind} fake not detected"
    cleaned = redact_text(text)
    assert MARKER not in cleaned
    assert "[REDACTED:" in cleaned
    assert find_secrets(cleaned) == [], "redacted text must scan clean"
    assert cleaned.startswith("line before\n") and cleaned.endswith("\nline after")


def test_secret_inside_json_string_is_redacted() -> None:
    line = json.dumps({"type": "tool_result", "content": "export " + fake_secret("env")})
    cleaned = redact_text(line)
    assert MARKER not in cleaned
    assert json.loads(cleaned)["content"].startswith("export MY_SERVICE_API_TOKEN=")


def test_plain_text_is_untouched() -> None:
    text = "skill-based task-sk: tokens=12 KEY_COUNT=3 bearer of news; ask-me AKIAxyz"
    assert redact_text(text) == text
    assert find_secrets(text) == []


def test_base64_images_become_hash_placeholders() -> None:
    blob = bytes(range(256)) * 8
    encoded = base64.b64encode(blob).decode("ascii")
    digest = hashlib.sha256(blob).hexdigest()
    uri = f'<img src="data:image/png;base64,{encoded}">'
    stream = json.dumps({"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": encoded}})
    for text in (uri, stream):
        cleaned = redact_text(text)
        assert encoded not in cleaned
        assert f"sha256={digest}" in cleaned and f"bytes={len(blob)}" in cleaned
    json.loads(redact_text(stream))


# An agent that reads a public web page echoes the page's contact address into
# its transcript (2026-10-19 FULL run, web-mondrian-landing); published text
# keeps no third-party email. Placeholder domains and GitHub noreply stay.
def test_redact_text_hides_third_party_emails_only() -> None:
    third_party = "sammlungonline" + "@" + "kunsthaus.ch"
    text = f"mail {third_party} or dev@example.com or 1+me@users.noreply.github.com"
    out = redact_text(text)
    assert third_party not in out and "[REDACTED:email]" in out
    assert "dev@example.com" in out and "1+me@users.noreply.github.com" in out


def test_secret_env_values_are_picked_by_name_segment() -> None:
    env = {"DEEPSEEK_API_KEY": "ds-0123456789abcdef", "GH_TOKEN": "tok0123456789", "PATH": "C:/bin;C:/tools",
           "PWD": "/home/project", "MY_AUTH": "short", "SESSIONNAME": "Console0123", "KEYBOARD": "us-international"}
    assert set(secret_env_values(env)) == {"ds-0123456789abcdef", "tok0123456789"}


def test_secret_env_value_is_redacted_raw_and_json_escaped() -> None:
    # A value no pattern knows: only the exact-value rule catches it.
    value = "pw" + "\\" + "q9Zx7Lk2Vm"
    names = LocalNames(secret_values=(value,))
    text = f"plain {value} and json {json.dumps(value)}"
    assert find_leaks(text, names) == {"env secret": 2}
    cleaned = redact_paths(text, PathScope(names=names))
    assert value not in cleaned and json.dumps(value)[1:-1] not in cleaned
    assert cleaned.count("[REDACTED:env]") == 2


def test_the_chosen_public_credit_is_not_scrubbed() -> None:
    # --submitter is published on purpose; it often equals the git name or account.
    names = LocalNames(user="dquill", host="box-17", person="dquill").allowing("DQuill")
    assert names == LocalNames(user=None, host="box-17", person=None)
    assert LocalNames(user="dquill").allowing(None) == LocalNames(user="dquill")


def test_git_author_name_is_redacted_as_a_whole_token() -> None:
    names = LocalNames(person="Dana Quill")
    text = "Author: Dana Quill <x@y.z>; Dana Quillfeather stays"
    assert redact_paths(text, PathScope(names=names)) == "Author: <NAME> <x@y.z>; Dana Quillfeather stays"


def test_connector_names_of_the_account_are_redacted() -> None:
    # Claude Code lists them when a session starts: they tell which services the submitter connected.
    line = ('{"tools":["Read","mcp__claude_ai_Gmail__create_draft","mcp__mengine-cu__browser"],'
            '"mcp_servers":[{"name":"claude.ai Google Drive","status":"connected"},{"name":"mengine-cu"}]}')
    assert find_leaks(line) == {"connector": 2}
    cleaned = redact_text(line)
    assert find_leaks(cleaned) == {}
    for private in ("Gmail", "Google Drive"):
        assert private not in cleaned
    assert "mcp__mengine-cu__browser" in cleaned and '"Read"' in cleaned


def test_a_mention_of_the_site_is_not_a_connector() -> None:
    assert find_leaks("See claude.ai for details, or Claude Docs.") == {}
