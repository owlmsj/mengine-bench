"""Build a site's client into one minified bundle, as a real site ships it (#153).

The source keeps readable names; the workspace gets only the bundle: comments and whitespace gone, declared
function and variable names shortened, and every `S("...")` string (API methods, header and meta names) moved
into an encoded table decoded at load. An agent can still read it, as it can read a real site's bundle; it just
costs more than reading a source file.

Works on source written for it: semicolons everywhere, no regex literals, no shorthand properties
(`{a}`), no object key that is a renamed name unless written as `key:` right after `{` or `,`.
"""

from __future__ import annotations

import base64
import hashlib
import re

KEYWORDS = frozenset("""break case catch class const continue debugger default delete do else export extends false
finally for function if import in instanceof let new null of return super switch this throw true try typeof undefined
var void while with yield async await static get set""".split())
SECRET = re.compile(r'S\("((?:[^"\\]|\\.)*)"\)')
DECLARED = re.compile(r"\b(?:function|const|let|var)\s+([A-Za-z_$][\w$]*)")
IDENT = re.compile(r"[A-Za-z_$][\w$]*")
NUMBER = re.compile(r"\d[\w.]*")
TABLE = "_$"


def _encode(text: str) -> str:
    return base64.b64encode(text[::-1].encode("utf-8")).decode("ascii")


def _short_names(taken: set[str]):  # noqa: ANN202 - a generator of names
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    size = 1
    while True:
        for number in range(len(alphabet) ** size):
            name, value = "", number
            for _ in range(size):
                name, value = alphabet[value % 26] + name, value // 26
            if name not in taken and name not in KEYWORDS:
                yield name
        size += 1


def _tokens(source: str) -> list[tuple[str, str]]:
    """(kind, text) with kind in str, ident, space, other; comments dropped."""
    out: list[tuple[str, str]] = []
    index = 0
    while index < len(source):
        char = source[index]
        if source.startswith("//", index):
            index = source.find("\n", index) if "\n" in source[index:] else len(source)
            out.append(("space", "\n"))
        elif source.startswith("/*", index):
            index = source.index("*/", index) + 2
        elif char in "\"'`":
            end = index + 1
            while source[end] != char:
                end += 2 if source[end] == "\\" else 1
            out.append(("str", source[index:end + 1]))
            index = end + 1
        elif char.isspace():
            end = index
            while end < len(source) and source[end].isspace():
                end += 1
            out.append(("space", " "))
            index = end
        elif char.isdigit():
            match = NUMBER.match(source, index)
            assert match is not None
            out.append(("num", match.group()))
            index = match.end()
        elif IDENT.match(source, index):
            match = IDENT.match(source, index)
            assert match is not None
            out.append(("ident", match.group()))
            index = match.end()
        else:
            out.append(("other", char))
            index += 1
    return out


def _is_key(tokens: list[tuple[str, str]], at: int) -> bool:
    """`name` in `{name: ...}` or `, name: ...`: an object key, not the variable."""
    before = next((text for kind, text in reversed(tokens[:at]) if kind != "space"), "")
    after = next((text for kind, text in tokens[at + 1:] if kind != "space"), "")
    return after == ":" and before in ("{", ",")


def minify(source: str) -> str:
    secrets: list[str] = []

    def stash(match: re.Match[str]) -> str:
        secrets.append(match.group(1).encode("utf-8").decode("unicode_escape"))
        return f"{TABLE}[{len(secrets) - 1}]"

    source = SECRET.sub(stash, source)
    tokens = _tokens(source)
    names = {text for kind, text in tokens if kind == "ident"}
    fresh = _short_names(names | {TABLE})
    renamed = {name: next(fresh) for name in dict.fromkeys(DECLARED.findall(source)) if len(name) > 2}
    out: list[str] = []
    previous = ""
    for at, (kind, text) in enumerate(tokens):
        if kind == "space":
            continue
        # `a.name` is a property; `...name` is a spread of the variable.
        is_property = previous == "." and "".join(out[-3:]) != "..."
        if kind == "ident" and text in renamed and not is_property and not _is_key(tokens, at):
            text = renamed[text]
        if previous and (previous[-1].isalnum() or previous[-1] in "_$") and (text[0].isalnum() or text[0] in "_$"):
            out.append(" ")
        out.append(text)
        previous = text
    table = ",".join(f'"{_encode(secret)}"' for secret in secrets)
    prelude = f'var {TABLE}=[{table}].map(function(x){{return atob(x).split("").reverse().join("")}});'
    return prelude + "".join(out)


def bundle_name(code: str) -> str:
    return f"main.{hashlib.sha256(code.encode('utf-8')).hexdigest()[:8]}.js"
