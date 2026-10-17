"""The whole repo scans clean: generic leaks always, private terms when the maintainer sets them.

No list of protected terms lives here, plain or hashed: a public list (even
unsalted hashes of short words) tells readers exactly what it protects. The
maintainer keeps the terms outside the repo (CONTRIBUTING.md, pre-release).
"""

from __future__ import annotations

import ast
import io
import re
import tokenize
from pathlib import Path

import pytest

from mengine_bench.privacy import private_terms_from_env, repo_files, scan_repo

ROOT = Path(__file__).resolve().parents[1]


def test_repo_scans_clean() -> None:
    hits = scan_repo(ROOT, private_terms_from_env())
    assert [f"{hit.path}:{hit.line} {hit.kind}" for hit in hits] == []


def test_no_protected_term_list_remains() -> None:
    # Old variable names, assembled here so this file does not match itself.
    old_names = re.compile(r"\b" + "BAN" + "NED" + r"(?:_SHA256)?\b")
    found = [path.relative_to(ROOT).as_posix() for path in repo_files(ROOT)
             if old_names.search(path.read_bytes().decode("utf-8", errors="ignore"))]
    assert found == []


# Private tracker links mean nothing to public readers; keep the why, drop the link.
PRIVATE_TRACKER = re.compile(r"\bmengine" + r"#", re.IGNORECASE)
PRIVATE_REF = re.compile(PRIVATE_TRACKER.pattern + r"|(?<![\w#])#\d+\b", re.IGNORECASE)
PUBLIC_SOURCES = [path for base in ("mengine_bench", "tests", "docs") for path in sorted((ROOT / base).rglob("*"))
                  if path.is_file() and path.suffix in (".py", ".md")]
PUBLIC_SOURCES += [ROOT / "README.md", ROOT / "CONTRIBUTING.md"]


def provenance_text(source: str) -> str:
    # Fictional PR ids and CSS colors in fixtures are not tracker provenance.
    comments = [token.string for token in tokenize.generate_tokens(io.StringIO(source).readline)
                if token.type == tokenize.COMMENT]
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            comments.append(ast.get_docstring(node) or "")
        if isinstance(node, ast.keyword) and node.arg == "provenance" and isinstance(node.value, ast.Constant):
            comments.append(str(node.value.value))
    return "\n".join(comments)


@pytest.mark.parametrize("path", PUBLIC_SOURCES, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_no_private_issue_references(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    text = provenance_text(source) if path.suffix == ".py" else source
    hits = PRIVATE_REF.findall(text) + PRIVATE_TRACKER.findall(source)
    assert hits == [], f"{path.name}: private issue references {hits}"


@pytest.mark.parametrize("reference", ["#" + "424", "#" + "424 b6", "mengine" + "#", "mengine" + "#317"])
def test_private_reference_pattern_catches_tracker_provenance(reference: str) -> None:
    assert PRIVATE_REF.search(reference)


@pytest.mark.parametrize("text", ["128k context", "7697 MiB", "1930", "version 0.14.3", "# Par times"])
def test_private_reference_pattern_allows_task_numbers(text: str) -> None:
    assert PRIVATE_REF.search(text) is None
