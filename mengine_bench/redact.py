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
import json
import os
import re
import shutil
import socket
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
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

# Claude Code lists the account's connectors when a session starts (#57).
_CONNECTOR = re.compile(r"mcp__claude_ai_\w+|claude\.ai [A-Z][\w ]*\w(?=\\*\")")


def redact_text(text: str) -> str:
    # Images first: a long base64 run could otherwise be read as a token.
    # Emails are text-only: a workspace file keeping one is not dropped (re-grading needs it).
    text = _CONNECTOR.sub(REDACTED.format(kind="connector"), redact_secrets(redact_images(text)))
    return _EMAIL.sub(REDACTED.format(kind="email"), text)


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

HOME, WORKSPACE, WORKDIR, USER, HOST, PERSON = "<HOME>", "<WORKSPACE>", "<WORKDIR>", "<USER>", "<HOST>", "<NAME>"
_SEP = r"(?:\\+|/+)"
_NAME = r"[^\\/\s\"'<>:|*?]+"
_SEGMENT_END = r"(?![^\\/\s\"'<>:|*?])"
_WINDOWS_HOME = re.compile(r"\b[A-Za-z]:" + _SEP + r"Users" + _SEP + _NAME, re.IGNORECASE)
# Not after a word char: a URL path segment named home is not a home dir.
_UNIX_HOME = re.compile(r"(?<![\w.~\-])\\*/(?:home|Users)\\*/" + _NAME)
# Claude Code project dirs flatten the cwd, every separator becoming "-"
# (C--Users-<name>-AppData-..., -home-<name>-repo); #23 QA leaked a name this way.
_SLUG_HOME = re.compile(r"(?<![A-Za-z0-9])((?:[A-Za-z]-)?-(?:Users|home)-)[A-Za-z0-9_.]+(?=-)", re.IGNORECASE)
_TOKEN_BEFORE, _TOKEN_AFTER = r"(?<![A-Za-z0-9_.\-])", r"(?![A-Za-z0-9_\-])"
# Too short or too generic to be identifying; redacting them would mangle text.
_GENERIC_NAMES = frozenset({"localhost", "root", "user", "admin"})


# Env var name segments that mark a secret (OPENAI_API_KEY, GH_TOKEN, ...).
_SECRET_ENV_SEGMENTS = frozenset({"KEY", "KEYS", "APIKEY", "TOKEN", "TOKENS", "SECRET", "SECRETS", "PASSWORD",
                                  "PASSWD", "CREDENTIAL", "CREDENTIALS", "AUTH"})
_SECRET_VALUE_MIN = 8


@dataclass(frozen=True)
class LocalNames:
    """This machine's identity and secrets: account, host and git author names
    are scrubbed as whole tokens, secret env values wherever they appear."""

    user: str | None = None
    host: str | None = None
    person: str | None = None
    secret_values: tuple[str, ...] = ()

    def allowing(self, public: str | None) -> LocalNames:
        """These names minus `public` (the --submitter credit, published on purpose)."""
        if not public:
            return self
        def kept(name: str | None) -> str | None:
            return None if name is not None and name.lower() == public.lower() else name
        return replace(self, user=kept(self.user), host=kept(self.host), person=kept(self.person))

    def patterns(self) -> list[tuple[str, str, re.Pattern[str]]]:
        # Secret values first: a value may contain a name token.
        found = [("env secret", REDACTED.format(kind="env"),
                  re.compile("|".join(re.escape(form) for form in (value, json.dumps(value)[1:-1]))))
                 for value in sorted(set(self.secret_values), key=len, reverse=True)]
        for kind, label, name in (("user", USER, self.user), ("host", HOST, self.host),
                                  ("person", PERSON, self.person)):
            if name and len(name) >= 3 and name.lower() not in _GENERIC_NAMES:
                found.append((kind, label, re.compile(_TOKEN_BEFORE + re.escape(name) + _TOKEN_AFTER,
                                                      re.IGNORECASE)))
        return found


def secret_env_values(env: Mapping[str, str]) -> tuple[str, ...]:
    """Values of env vars whose name has a secret-like segment; agents print `env` and config files."""
    return tuple(value for name, value in env.items()
                 if _SECRET_ENV_SEGMENTS & set(name.upper().split("_"))
                 and len(value) >= _SECRET_VALUE_MIN and not any(char.isspace() for char in value))


def _git_user_name() -> str | None:
    git = shutil.which("git")
    if git is None:
        return None
    try:
        done = subprocess.run([git, "config", "--get", "user.name"], capture_output=True, text=True, timeout=10,
                              check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return done.stdout.strip() or None


def local_names() -> LocalNames:
    """This machine's account, host and git author names and secret env values."""
    try:
        user: str | None = getpass.getuser()
    except (OSError, KeyError):
        user = None
    return LocalNames(user=user, host=socket.gethostname() or None, person=_git_user_name(),
                      secret_values=secret_env_values(os.environ))


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


# Every step runs in a temp workspace of its own (#59), named the same way on every machine.
_TEMP_WORKSPACE = re.compile(r"[^\s\"'`<>|,;=()]*mengine-bench-fresh-[\w-]+" + _SEP + r"workspace", re.IGNORECASE)


def redact_paths(text: str, scope: PathScope) -> str:
    text = _TEMP_WORKSPACE.sub(WORKSPACE, text)
    for label, paths in ((WORKSPACE, scope.workspaces), (WORKDIR, scope.workdirs)):
        for pattern in _dir_patterns(paths):
            text = pattern.sub(label, text)
    text = _UNIX_HOME.sub(HOME, _WINDOWS_HOME.sub(HOME, text))
    text = _SLUG_HOME.sub(lambda match: match.group(1) + USER, text)
    for _, label, pattern in scope.names.patterns():
        text = pattern.sub(label, text)
    return text


def find_leaks(text: str, names: LocalNames | None = None) -> dict[str, int]:
    """Count per kind of what redaction should have removed: secret patterns,
    e-mail addresses, connector names, home paths, local names and secret env values (empty when clean)."""
    counts = {kind: len(pattern.findall(text)) for kind, pattern in SECRET_PATTERNS}
    counts["email"] = len(_EMAIL.findall(text))
    counts["connector"] = len(_CONNECTOR.findall(text))
    counts["home path"] = sum(len(pattern.findall(text)) for pattern in (_WINDOWS_HOME, _UNIX_HOME, _SLUG_HOME))
    for kind, _, pattern in (names or LocalNames()).patterns():
        counts[kind] = counts.get(kind, 0) + len(pattern.findall(text))
    return {kind: count for kind, count in counts.items() if count}
