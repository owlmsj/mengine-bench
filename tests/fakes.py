"""Fake secrets for redaction tests, assembled at runtime.

Owner decision: no secret-shaped literal may appear in
any source file, or secret-leak hooks block the commit. Every fake is built
here from harmless fragments and carries the marker "FAKE".
"""

from __future__ import annotations

MARKER = "FAKE"
_DASHES = "-" * 5
_PEM_LABEL = " ".join(["PRIVATE", "KEY"])

KINDS = ("openai", "github", "slack", "aws", "google", "bearer", "pem", "env")


def _pem() -> str:
    header = _DASHES + "BEGIN " + _PEM_LABEL + _DASHES
    footer = _DASHES + "END " + _PEM_LABEL + _DASHES
    body = "\n".join([MARKER * 16] * 3)
    return f"{header}\n{body}\n{footer}"


def fake_secret(kind: str) -> str:
    builders = {
        "openai": lambda: "sk" + "-" + MARKER * 12,
        "github": lambda: "gh" + "p_" + MARKER * 9,
        "slack": lambda: "xo" + "xb-" + MARKER * 6,
        "aws": lambda: "AK" + "IA" + MARKER * 4,
        "google": lambda: "AI" + "za" + (MARKER * 9)[:35],
        "bearer": lambda: "Bear" + "er " + MARKER * 8,
        "pem": _pem,
        "env": lambda: "MY_SERVICE_" + "API_" + "TOKEN=" + MARKER * 5,
    }
    if kind not in builders:
        raise ValueError(f"received fake secret kind {kind!r}; expected one of {KINDS}")
    return builders[kind]()
