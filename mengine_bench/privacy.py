"""Privacy scan of the public repo: generic leak shapes, plus optional private terms.

The public checks need no secret list: home paths, e-mail addresses, private
and tailnet addresses, default Windows host names and token shapes are
recognizable by form alone. Names worth protecting are not, but publishing
them (even as unsalted hashes of short words, which a dictionary reverses)
tells readers exactly what is protected. So the maintainer keeps them in a
file outside git and points `MENGINE_BENCH_PRIVATE_TERMS` at it before a
release (CONTRIBUTING.md).

Hits carry file, line and kind only, never the matched text: the CLI output
lands in CI logs, which are public too.
"""

from __future__ import annotations

import gzip
import io
import os
import re
import subprocess
import tarfile
import unicodedata
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from mengine_bench.redact import SECRET_PATTERNS
from mengine_bench.unpack_budget import UnpackBudget, UnpackBudgetExceeded, iter_tar_bounded, read_gzip_bounded

PRIVATE_TERMS_ENV = "MENGINE_BENCH_PRIVATE_TERMS"
PRIVATE_TERMS_FILENAME = "private-terms.txt"
PRIVATE_TERM = "private-term"

# The only lines allowed to name the owner: the README "about" line and the
# LICENSE copyright. They waive private-term hits only; a path or address on
# them still fails.
ALLOWED_LINES: tuple[tuple[str, str], ...] = (
    ("README.md", "mengine-bench is the coding-agent benchmark of "),
    ("LICENSE", "Copyright (c) "),
)

_SEP = r"(?:\\+|/+)"
# A real account name starts with a word char; `{name}` and `<name>` are templates.
_ACCOUNT = r"[A-Za-z0-9_][\w.\-]*"
_OCTET = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
_TAIL = r"\." + _OCTET + r"\." + _OCTET
# Not inside a longer dotted run, so version strings like 1.10.2.3.4 stay clean.
_IP_BEFORE, _IP_AFTER = r"(?<![\d.])", r"(?!\d|\.\d)"
GENERIC_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("home-path", re.compile(r"\b[A-Za-z]:" + _SEP + r"Users" + _SEP + _ACCOUNT, re.IGNORECASE)),
    ("home-path", re.compile(r"(?<![\w.~\-])\\*/+(?:home|Users)\\*/+" + _ACCOUNT)),
    ("private-ip", re.compile(_IP_BEFORE + r"(?:10\." + _OCTET + r"|172\.(?:1[6-9]|2\d|3[01])|192\.168"
                              + r"|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7]))" + _TAIL + _IP_AFTER)),
    ("tailnet-host", re.compile(r"\b[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.ts\.net\b", re.IGNORECASE)),
    ("windows-host", re.compile(r"\bDESKTOP-[A-Z0-9]{7}\b")),
)
_EMAIL = re.compile(r"(?<![\w.%+\-])[A-Za-z0-9._%+\-]+@(?P<domain>[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*"
                    r"\.[A-Za-z]{2,})\b")
_PUBLIC_MAIL_DOMAINS = frozenset({"users.noreply.github.com", "example.com", "example.org", "example.net"})
_WORD = re.compile(r"[a-z0-9]+")
# Fallback walk only (no git): caches anywhere, scratch at the top. Bundles keep
# their own workspaces/ dirs, so that name is skipped only at the root.
_SKIP_ANYWHERE = frozenset({".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"})
_SKIP_TOP = frozenset({"workspaces", "tmp", "dist", "build"})

PrivateTerms = tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class PrivacyHit:
    path: str
    line: int
    kind: str


def ascii_fold(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").lower()


def load_private_terms(path: Path) -> PrivateTerms:
    """One term per line (a word or a word sequence); blank lines and `#` comments skipped."""
    if not path.is_file():
        raise FileNotFoundError(f"received private terms path {path.name!r}; expected a file, one term per line")
    terms = {tuple(_WORD.findall(ascii_fold(line))) for line in path.read_text(encoding="utf-8").splitlines()
             if line.strip() and not line.lstrip().startswith("#")}
    return tuple(sorted(term for term in terms if term))


def private_terms_from_env() -> PrivateTerms | None:
    value = os.environ.get(PRIVATE_TERMS_ENV)
    return load_private_terms(Path(value)) if value else None


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _generic_hits(text: str) -> Iterator[tuple[int, str]]:
    for kind, pattern in GENERIC_PATTERNS:
        yield from ((_line_of(text, m.start()), kind) for m in pattern.finditer(text))
    for m in _EMAIL.finditer(text):
        if m.group("domain").lower() not in _PUBLIC_MAIL_DOMAINS:
            yield _line_of(text, m.start()), "email"
    for _, pattern in SECRET_PATTERNS:
        yield from ((_line_of(text, m.start()), "token") for m in pattern.finditer(text))


def _private_hits(text: str, terms: PrivateTerms) -> Iterator[int]:
    # Per line, so a hit keeps its line; one word stream, so a pair split by a wrap still matches.
    words = [(word, number) for number, line in enumerate(text.split("\n"), 1)
             for word in _WORD.findall(ascii_fold(line))]
    for size in sorted({len(term) for term in terms}):
        wanted = {term for term in terms if len(term) == size}
        for start in range(len(words) - size + 1):
            if tuple(word for word, _ in words[start:start + size]) in wanted:
                yield words[start][1]


def _allowed(rel: str, text: str, line: int) -> bool:
    lines = text.split("\n")
    return any(rel == path and line <= len(lines) and lines[line - 1].startswith(prefix)
               for path, prefix in ALLOWED_LINES)


def scan_text(text: str, rel: str, private_terms: PrivateTerms | None = None) -> list[PrivacyHit]:
    found = [PrivacyHit(rel, line, kind) for line, kind in _generic_hits(text)]
    found += [PrivacyHit(rel, line, PRIVATE_TERM) for line in _private_hits(text, private_terms or ())
              if not _allowed(rel, text, line)]
    return sorted(found, key=lambda hit: (hit.line, hit.kind))


def _as_text(raw: bytes) -> str | None:
    if b"\0" in raw[:8192]:
        return None
    return raw.decode("utf-8", errors="replace")


def _tar_texts(rel: str, raw: bytes, terms: PrivateTerms | None,
               budget: UnpackBudget) -> Iterator[tuple[str, str]]:
    for index, (member, body) in enumerate(iter_tar_bounded(io.BytesIO(raw), budget, rel)):
        label = f"{rel}!{member.name}"
        if scan_text(member.name, label, terms):
            # A leak in the member name must not reach the report through the label.
            label = f"{rel}!member#{index}"
            yield label, member.name
        text = _as_text(body) if body is not None else None
        if text is not None:
            yield label, text


def _file_texts(root: Path, path: Path, terms: PrivateTerms | None,
                budget: UnpackBudget) -> Iterator[tuple[str, str]]:
    rel = path.relative_to(root).as_posix()
    raw = path.read_bytes()
    if rel.endswith((".tar.gz", ".tgz")):
        yield from _tar_texts(rel, raw, terms, budget)
        return
    if rel.endswith(".gz"):
        raw = read_gzip_bounded(io.BytesIO(raw), budget, rel)
    text = _as_text(raw)
    if text is not None:
        yield rel, text


def _skipped(dirs: tuple[str, ...]) -> bool:
    return bool(_SKIP_ANYWHERE.intersection(dirs)) or bool(dirs and dirs[0] in _SKIP_TOP)


def repo_files(root: Path) -> list[Path]:
    """Tracked plus untracked-not-ignored files under a git root; a plain walk elsewhere."""
    root = root.resolve()
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=root, capture_output=True, text=True,
                             check=True).stdout.strip()
        listed = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=root,
                                capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        top, listed = "", b""
    if top and Path(top).resolve() == root:
        files = [root / name for name in listed.decode("utf-8").split("\0") if name]
    else:
        files = [path for path in root.rglob("*") if not _skipped(path.relative_to(root).parts[:-1])]
    return sorted(path for path in files if path.is_file() and path.name != PRIVATE_TERMS_FILENAME)


def _budget_key(root: Path, path: Path) -> Path:
    """Result bundles share one unpack budget (review R09); any other file gets its own."""
    parts = path.relative_to(root).parts
    for index, part in enumerate(parts[:-1]):
        if part in ("workspaces", "transcripts") and index > 0:
            return root.joinpath(*parts[:index])
    return path


def scan_repo(root: Path, private_terms: PrivateTerms | None = None) -> list[PrivacyHit]:
    root = root.resolve()
    found: list[PrivacyHit] = []
    budgets: dict[Path, UnpackBudget] = {}
    exhausted: set[Path] = set()
    for path in repo_files(root):
        key = _budget_key(root, path)
        if key in exhausted:
            continue  # stop on the first violation: the rest of that bundle is never inflated
        try:
            texts = list(_file_texts(root, path, private_terms, budgets.setdefault(key, UnpackBudget())))
        except UnpackBudgetExceeded:
            exhausted.add(key)
            found.append(PrivacyHit(path.relative_to(root).as_posix(), 0, "unpack-budget"))
            continue
        except (OSError, EOFError, gzip.BadGzipFile, tarfile.TarError) as error:
            # Fail closed: an archive we cannot read is one we cannot vouch for.
            found.append(PrivacyHit(path.relative_to(root).as_posix(), 0, f"unreadable:{type(error).__name__}"))
            continue
        for label, text in texts:
            found += scan_text(text, label, private_terms)
    return found
