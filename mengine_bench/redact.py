"""Redaction for published bundles: secrets out, base64 images shrunk to a hash.

Transcripts are raw agent output, and agents echo env dumps, config files and
tool results. Everything a bundle publishes goes through `redact_text`.

Patterns are spelled with quantifiers (`-{5}`, `{16}`) instead of literal
key prefixes plus filler, so this file never looks like a leaked key itself.
"""

from __future__ import annotations

import base64
import binascii
import getpass
import hashlib
import re
import socket
from dataclasses import dataclass, field
from pathlib import Path

REDACTED = "[REDACTED:{kind}]"
_NOT_REDACTED = r"(?!\[REDACTED)"

# (kind, pattern); the whole match is replaced unless the pattern has a
# `keep` group, which survives so the reader still sees which variable leaked.
SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("private-key", re.compile(r"-{5}BEGIN[A-Z ]{0,40}PRIVATE KEY-{5}.*?-{5}END[A-Z ]{0,40}PRIVATE KEY-{5}",
                               re.DOTALL)),
    ("openai", re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}")),
    ("github", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")),
    ("slack", re.compile(r"\bxox[abposr]-[A-Za-z0-9\-]{10,}")),
    ("aws", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("google", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}")),
    ("bearer", re.compile(r"(?P<keep>\b[Bb]earer\s+)" + _NOT_REDACTED + r"[A-Za-z0-9._~+/\-]{16,}=*")),
    ("env", re.compile(r"(?P<keep>\b[A-Z][A-Z0-9_]*(?:_KEY|TOKEN|SECRET|PASSWORD|PASSWD)S?[\"']?\s*[=:]\s*[\"']?)"
                       + _NOT_REDACTED + r"[^\s\"',;}\\]{8,}")),
)

# Data URIs, and the `"data": "<base64>"` fields of stream-json image blocks.
_DATA_URI = re.compile(r"data:image/[a-z0-9.+\-]+;base64,(?P<b64>[A-Za-z0-9+/]{64,}={0,2})")
_JSON_BLOB = re.compile(r"(?P<keep>\"data\"\s*:\s*\")(?P<b64>[A-Za-z0-9+/]{256,}={0,2})(?=\")")


def _image_placeholder(encoded: str) -> str | None:
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError):
        return None
    return f"[image sha256={hashlib.sha256(raw).hexdigest()} bytes={len(raw)}]"


def _replace_image(match: re.Match[str]) -> str:
    placeholder = _image_placeholder(match.group("b64"))
    if placeholder is None:
        return match.group(0)
    keep = match.groupdict().get("keep") or ""
    return keep + placeholder


def redact_images(text: str) -> str:
    return _JSON_BLOB.sub(_replace_image, _DATA_URI.sub(_replace_image, text))


def redact_secrets(text: str) -> str:
    for kind, pattern in SECRET_PATTERNS:
        marker = REDACTED.format(kind=kind)
        text = pattern.sub(lambda m, marker=marker: (m.groupdict().get("keep") or "") + marker, text)
    return text


# Third-party addresses only; placeholders and GitHub noreply addresses stay readable.
_EMAIL = re.compile(r"(?<![\w.%+\-])[A-Za-z0-9._%+\-]+@(?!(?:users\.noreply\.github\.com|example\.(?:com|org|net))\b)"
                    r"[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}\b")


def redact_text(text: str) -> str:
    # Images first: a long base64 run could otherwise be read as a token.
    # Emails are text-only: a workspace file keeping one is not dropped (re-grading needs it).
    return _EMAIL.sub(REDACTED.format(kind="email"), redact_secrets(redact_images(text)))


def find_secrets(text: str) -> list[str]:
    """Kinds of unredacted secrets in `text` (empty when clean)."""
    return [kind for kind, pattern in SECRET_PATTERNS if pattern.search(text)]


def redact_value(value: object) -> object:
    """Redact every string inside a JSON-like value."""
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, dict):
        return {key: redact_value(item) for key, item in value.items()}
    return value


# --- Local paths and identity -------------------------------------------
# Agents echo absolute paths (cwd, shell, tool results), often JSON-escaped
# once or twice, so a separator is any run of backslashes or slashes. The
# first public baseline leaked the Windows account name through the Codex
# shell path; every submitter would leak theirs the same way.

HOME, WORKSPACE, WORKDIR, USER, HOST = "<HOME>", "<WORKSPACE>", "<WORKDIR>", "<USER>", "<HOST>"
_SEP = r"(?:\\+|/+)"
_NAME = r"[^\\/\s\"'<>:|*?]+"
_SEGMENT_END = r"(?![^\\/\s\"'<>:|*?])"
_WINDOWS_HOME = re.compile(r"\b[A-Za-z]:" + _SEP + r"Users" + _SEP + _NAME, re.IGNORECASE)
# Not after a word char: a URL path segment named home is not a home dir.
_UNIX_HOME = re.compile(r"(?<![\w.~\-])\\*/(?:home|Users)\\*/" + _NAME)
_TOKEN_BEFORE, _TOKEN_AFTER = r"(?<![A-Za-z0-9_.\-])", r"(?![A-Za-z0-9_\-])"
# Too short or too generic to be identifying; redacting them would mangle text.
_GENERIC_NAMES = frozenset({"localhost", "root", "user", "admin"})


@dataclass(frozen=True)
class LocalNames:
    """Account and machine names to scrub as whole tokens."""

    user: str | None = None
    host: str | None = None

    def patterns(self) -> list[tuple[str, str, re.Pattern[str]]]:
        found = []
        for kind, label, name in (("user", USER, self.user), ("host", HOST, self.host)):
            if name and len(name) >= 3 and name.lower() not in _GENERIC_NAMES:
                found.append((kind, label, re.compile(_TOKEN_BEFORE + re.escape(name) + _TOKEN_AFTER,
                                                      re.IGNORECASE)))
        return found


def local_names() -> LocalNames:
    """This machine's account and host names."""
    try:
        user: str | None = getpass.getuser()
    except (OSError, KeyError):
        user = None
    return LocalNames(user=user, host=socket.gethostname() or None)


@dataclass(frozen=True)
class PathScope:
    """What one run must scrub: its own dirs first (most specific), then homes and names."""

    workspaces: tuple[Path, ...] = ()
    workdirs: tuple[Path, ...] = ()
    names: LocalNames = field(default_factory=LocalNames)


def _dir_pattern(path: Path) -> re.Pattern[str]:
    parts = [part for part in re.split(r"[\\/]+", str(path)) if part]
    lead = "" if re.match(r"^[A-Za-z]:", str(path)) else r"\\*/"
    return re.compile(lead + _SEP.join(map(re.escape, parts)) + _SEGMENT_END, re.IGNORECASE)


def _dir_patterns(paths: tuple[Path, ...]) -> list[re.Pattern[str]]:
    forms = {str(form) for path in paths for form in (path, path.resolve())}
    # Longest first, so a nested dir wins over its parent.
    return [_dir_pattern(Path(form)) for form in sorted(forms, key=lambda form: (-len(form), form))]


def redact_paths(text: str, scope: PathScope) -> str:
    for label, paths in ((WORKSPACE, scope.workspaces), (WORKDIR, scope.workdirs)):
        for pattern in _dir_patterns(paths):
            text = pattern.sub(label, text)
    text = _UNIX_HOME.sub(HOME, _WINDOWS_HOME.sub(HOME, text))
    for _, label, pattern in scope.names.patterns():
        text = pattern.sub(label, text)
    return text


def find_path_leaks(text: str, names: LocalNames | None = None) -> dict[str, int]:
    """Count of unredacted home paths and local name tokens per kind (empty when clean)."""
    counts = {"home path": len(_WINDOWS_HOME.findall(text)) + len(_UNIX_HOME.findall(text))}
    for kind, _, pattern in (names or LocalNames()).patterns():
        counts[kind] = len(pattern.findall(text))
    return {kind: count for kind, count in counts.items() if count}
