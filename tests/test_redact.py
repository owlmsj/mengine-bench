"""Secret and image-blob redaction for published transcripts."""

from __future__ import annotations

import base64
import hashlib
import json

import pytest

from fakes import KINDS, MARKER, fake_secret
from mengine_bench.redact import find_secrets, redact_text


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
