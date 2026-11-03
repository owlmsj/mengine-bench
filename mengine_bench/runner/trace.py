"""Tool inputs and source-fetch evidence, shared by checks and checkpoints (#164)."""

from __future__ import annotations

import ast
import json
import re
import shlex
from collections.abc import Mapping, Sequence
from pathlib import PurePosixPath
from urllib.parse import urlsplit

from mengine_bench.core import ToolCall
from mengine_bench.runner.agents import split_jsonl


def _mapping(value: object) -> Mapping[str, object]:
    return value if isinstance(value, dict) else {}


def _call(name: object, inputs: object) -> ToolCall:
    if isinstance(inputs, str):
        try:
            inputs = json.loads(inputs)
        except ValueError:
            inputs = {"command": inputs}
    return ToolCall(str(name or ""), _mapping(inputs))


def _event_calls(event: Mapping[str, object]) -> list[ToolCall]:
    kind = event.get("type")
    if kind == "assistant":
        blocks = _mapping(event.get("message")).get("content", [])
        return [_call(block.get("name"), block.get("input")) for block in blocks
                if isinstance(block, dict) and block.get("type") == "tool_use"] if isinstance(blocks, list) else []
    if kind == "tool_use":
        part = _mapping(event.get("part"))
        return [_call(part.get("tool"), _mapping(part.get("state")).get("input"))]
    if kind == "item.completed":
        item = _mapping(event.get("item"))
        subtype = item.get("type")
        if subtype == "command_execution":
            return [_call("shell", {"command": item.get("command")})]
        if subtype == "file_change":
            return [_call("apply_patch", {"changes": item.get("changes")})]
        if subtype == "mcp_tool_call":
            return [_call(item.get("tool"), item.get("arguments"))]
        if subtype == "web_search":
            return [_call("web", _mapping(item.get("action")))]
    step = _mapping(event.get("step_update"))
    if step.get("step_type") == "tool" and step.get("state") != "ACTIVE":
        return [_call(step.get("tool_name"), _mapping(step.get("tool_info")).get("parameters"))]
    return []


def tool_trace(streams: Sequence[str]) -> tuple[ToolCall, ...]:
    """One input per completed/reportable call, using the same harness shapes as stats."""
    return tuple(call for stream in streams for event in split_jsonl(stream) for call in _event_calls(event))


def url_key(url: object) -> str:
    """Host + path tolerates scheme, fragment and www aliases, not a different page (#164)."""
    try:
        parsed = urlsplit(str(url or "").strip())
        host = (parsed.hostname or "").lower().removeprefix("www.").rstrip(".")
        if parsed.scheme not in ("http", "https") or not host:
            return ""
        return host + (f":{parsed.port}" if parsed.port else "") + (parsed.path.rstrip("/") or "/")
    except ValueError:
        return ""


def _urls(text: str) -> set[str]:
    return set(re.findall(r"https?://[^\s\"'<>`\])}]+", text))


def _literal_strings(node: ast.AST, bindings: Mapping[str, set[str]]) -> set[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return {node.value}
    if isinstance(node, ast.Name):
        return bindings.get(node.id, set())
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return set().union(*(_literal_strings(item, bindings) for item in node.elts))
    return set()


def _python_urls(source: str) -> set[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    bindings: dict[str, set[str]] = {}
    found: set[str] = set()
    # Only download-call arguments count; a result.json literal in the same script is not evidence (#164).
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    bindings[target.id] = _literal_strings(node.value, bindings)
        if isinstance(node, ast.For) and isinstance(node.target, ast.Name):
            bindings[node.target.id] = _literal_strings(node.iter, bindings)
        if not isinstance(node, ast.Call):
            continue
        name = ast.unparse(node.func)
        if not re.fullmatch(r"(?:requests|httpx|session|client)\.(?:get|request)|(?:urllib\.request\.)?(?:urlopen|urlretrieve)|.+\.goto", name):
            continue
        args = list(node.args) + [kw.value for kw in node.keywords if kw.arg in ("url", "uri")]
        found.update(value for arg in args for value in _literal_strings(arg, bindings) if url_key(value))
    return found


_HEREDOC = re.compile(r"(?m)^(?P<head>[^\n]*?)<<-?\s*['\"]?(?P<tag>\w+)['\"]?[^\n]*\n(?P<body>.*?)\n(?P=tag)\b", re.DOTALL)
_SHELLS = {"bash", "shell", "run_command", "exec_command", "powershell", "terminal"}
_DOWNLOADS = {"curl", "curl.exe", "wget", "wget.exe", "invoke-webrequest", "invoke-restmethod", "iwr", "irm"}


def _shell_urls(command: str, scripts: dict[str, str]) -> set[str]:
    found: set[str] = set()

    def heredoc(match: re.Match[str]) -> str:
        head, body = match["head"].strip(), match["body"]
        if re.match(r"(?:python[\d.]*|uv run python)\b", head):
            found.update(_python_urls(body))
        dest = re.search(r">\s*['\"]?([\w./-]+)", head)
        if dest and re.match(r"cat\b", head):
            scripts[dest[1]] = body
        return ""

    command = _HEREDOC.sub(heredoc, command)
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|\n")
        lexer.whitespace = " \t\r"
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return found
    segments: list[list[str]] = [[]]
    for token in tokens:
        if token and all(char in ";&|\n" for char in token):
            segments.append([])
        else:
            segments[-1].append(token)
    for words in segments:
        found.update(_command_urls(words, scripts))
    return found


def _command_urls(words: list[str], scripts: dict[str, str]) -> set[str]:
    if not words:
        return set()
    name = PurePosixPath(words[0].replace("\\", "/")).name.lower()
    if name in _DOWNLOADS:
        return {url for word in words[1:] for url in _urls(word)}
    if name in {"bash", "sh", "pwsh", "powershell"} and len(words) > 2 and words[1].lower() in {"-c", "-lc", "-command"}:
        return _shell_urls(words[2], scripts)
    if name == "uv" and words[1:2] == ["run"]:
        return _command_urls(words[2:], scripts)
    if re.fullmatch(r"python[\d.]*|python.exe", name):
        if "-c" in words and words.index("-c") + 1 < len(words):
            return _python_urls(words[words.index("-c") + 1])
        script = next((word for word in words[1:] if word in scripts), None)
        return _python_urls(scripts[script]) if script else set()
    if name in {"node", "node.exe"}:
        source = words[words.index("-e") + 1] if "-e" in words and words.index("-e") + 1 < len(words) else scripts.get(words[-1], "")
        return _javascript_urls(source)
    return set()


def _javascript_urls(source: str) -> set[str]:
    return set(re.findall(r"(?:\bfetch|\.goto|\.navigate|\.get|\.createBrowserTab)\(\s*(?:['\"][^'\"]+['\"]\s*,\s*)?['\"](https?://[^'\"]+)['\"]", source))


def fetch_actions(trace: Sequence[ToolCall]) -> list[set[str]]:
    """URL inputs per action; never scan tool results, search snippets or written prose."""
    scripts: dict[str, str] = {}
    actions: list[set[str]] = []
    for call in trace:
        name = call.name.lower()
        inputs = call.inputs
        found: set[str] = set()
        if name in {"write", "write_file", "write_to_file"}:
            path = inputs.get("file_path", inputs.get("path", inputs.get("TargetFile")))
            body = inputs.get("content", inputs.get("CodeContent"))
            if isinstance(path, str) and isinstance(body, str):
                scripts[path] = body
        if name in _SHELLS:
            found = _shell_urls(str(inputs.get("command", inputs.get("cmd", inputs.get("CommandLine", "")))), scripts)
        elif re.search(r"fetch|navigate|browse|open_url|read_url", name) and "search" not in name:
            found = {str(value) for key, value in inputs.items() if key.lower() in {"url", "uri", "targeturl"} and url_key(value)}
        if name in {"web", "web.run", "web__run"} or name.endswith("web_run"):
            opened = inputs.get("open", [])
            if isinstance(opened, list):
                found.update(str(row.get("ref_id")) for row in opened if isinstance(row, dict) and url_key(row.get("ref_id")))
            if inputs.get("type") in {"open_page", "open"} and url_key(inputs.get("url")):
                found.add(str(inputs["url"]))
        if "browser" in name or "cua" in name:
            found.update(_javascript_urls(str(inputs.get("code", inputs.get("script", "")))))
        actions.append(found)
    return actions


def fetched_urls(trace: Sequence[ToolCall]) -> set[str]:
    return {url_key(url) for action in fetch_actions(trace) for url in action if url_key(url)}
