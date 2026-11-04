"""Tool inputs and source-fetch evidence, shared by checks and checkpoints (#164)."""

from __future__ import annotations

import ast
import json
import re
import shlex
from collections.abc import Mapping, Sequence
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

from mengine_bench.core import ToolCall
from mengine_bench.runner.agents import split_jsonl


def _mapping(value: object) -> Mapping[str, object]:
    return value if isinstance(value, dict) else {}


def _blocks(event: Mapping[str, object]) -> list[Mapping[str, object]]:
    content = _mapping(event.get("message")).get("content")
    return [block for block in content if isinstance(block, dict)] if isinstance(content, list) else []


def _call(name: object, inputs: object, *, failed: bool = False) -> ToolCall:
    if isinstance(inputs, str):
        try:
            inputs = json.loads(inputs)
        except ValueError:
            inputs = {"command": inputs}
    return ToolCall(str(name or ""), dict(_mapping(inputs)), failed)


def _event_calls(event: Mapping[str, object], failures: set[str]) -> list[ToolCall]:
    kind = event.get("type")
    if kind == "assistant":
        return [_call(block.get("name"), block.get("input"), failed=str(block.get("id")) in failures)
                for block in _blocks(event) if block.get("type") == "tool_use"]
    if kind == "tool_use":
        part = _mapping(event.get("part"))
        state = _mapping(part.get("state"))
        return [_call(part.get("tool"), state.get("input"), failed=state.get("status") == "error")]
    if kind == "item.completed":
        item = _mapping(event.get("item"))
        subtype = item.get("type")
        failed = item.get("status") == "failed" or item.get("exit_code") not in (None, 0)
        if subtype == "command_execution":
            return [_call("shell", {"command": item.get("command")}, failed=failed)]
        if subtype == "file_change":
            return [_call("apply_patch", {"changes": item.get("changes")}, failed=failed)]
        if subtype == "mcp_tool_call":
            return [_call(item.get("tool"), item.get("arguments"), failed=failed)]
        if subtype == "web_search":
            return [_call("web", _mapping(item.get("action")))]
    step = _mapping(event.get("step_update"))
    if step.get("step_type") == "tool" and step.get("state") != "ACTIVE":
        return [_call(step.get("tool_name"), _mapping(step.get("tool_info")).get("parameters"), failed=step.get("state") != "DONE")]
    return []


def tool_trace(streams: Sequence[str], workspace: Path | None = None,
               original_workspace: Path | None = None) -> tuple[ToolCall, ...]:
    """One input per completed/reportable call, using the same harness shapes as stats."""
    calls: list[ToolCall] = []
    for stream in streams:
        events = split_jsonl(stream)
        failures = {str(block.get("tool_use_id")) for event in events if event.get("type") == "user"
                    for block in _blocks(event) if block.get("type") == "tool_result" and block.get("is_error")}
        calls.extend(call for event in events for call in _event_calls(event, failures))
    return tuple(calls)


def url_key(url: object) -> str:
    """Distinct fetched URL identity; query values remain distinct sources (#164)."""
    try:
        parsed = urlsplit(str(url or "").strip())
        host = (parsed.hostname or "").lower().removeprefix("www.")
        if parsed.scheme not in ("http", "https") or not host:
            return ""
        return host + (f":{parsed.port}" if parsed.port else "") + (parsed.path.rstrip("/") or "/") + (f"?{parsed.query}" if parsed.query else "")
    except ValueError:
        return ""


def host_key(url: object) -> str:
    if not url_key(url):
        return ""
    return (urlsplit(str(url).strip()).hostname or "").lower().removeprefix("www.")


def fetched_hosts(trace: Sequence[ToolCall]) -> set[str]:
    return {host_key(url) for action in fetch_actions(trace) for url in action if host_key(url)}


def _literal_strings(node: ast.AST, bindings: Mapping[str, set[str]]) -> set[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return {node.value}
    if isinstance(node, ast.Name):
        return bindings.get(node.id, set())
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return set().union(*(_literal_strings(item, bindings) for item in node.elts))
    if isinstance(node, ast.Call) and ast.unparse(node.func).split(".")[-1] == "Request" and node.args:
        return _literal_strings(node.args[0], bindings)
    return set()


def _python_urls(source: str) -> set[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    bindings: dict[str, set[str]] = {}
    aliases: dict[str, str] = {}
    found: set[str] = set()
    # Only download-call arguments count; a result.json literal in the same script is not evidence (#164).
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            aliases.update({item.asname: item.name for item in node.names if item.asname})
        if isinstance(node, ast.ImportFrom):
            aliases.update({item.asname or item.name: f"{node.module}.{item.name}" for item in node.names})
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    bindings[target.id] = _literal_strings(node.value, bindings)
                    if isinstance(node.value, ast.Call):
                        constructor = ast.unparse(node.value.func)
                        prefix, dot, suffix = constructor.partition(".")
                        constructor = aliases.get(prefix, prefix) + dot + suffix
                        if constructor in {"requests.Session", "httpx.Client"}:
                            aliases[target.id] = constructor.split(".")[0]
        if isinstance(node, ast.For) and isinstance(node.target, ast.Name):
            bindings[node.target.id] = _literal_strings(node.iter, bindings)
        if not isinstance(node, ast.Call):
            continue
        name = ast.unparse(node.func)
        prefix, dot, suffix = name.partition(".")
        name = aliases.get(prefix, prefix) + dot + suffix
        if not re.fullmatch(r"(?:requests|httpx|session|client)\.(?:get|request)|(?:urllib\.request\.)?(?:urlopen|urlretrieve)|.+\.goto", name):
            continue
        offset = 1 if name.endswith(".request") else 0
        args = list(node.args[offset:offset + 1]) + [kw.value for kw in node.keywords if kw.arg in ("url", "uri")]
        found.update(value for arg in args for value in _literal_strings(arg, bindings) if url_key(value))
    return found


_HEREDOC = re.compile(r"(?m)^(?P<head>[^\n]*?)<<-?\s*['\"]?(?P<tag>\w+)['\"]?[^\n]*\n(?P<body>.*?)\n(?P=tag)\b", re.DOTALL)
_HERESTRING = re.compile(r"@(?P<quote>['\"])\r?\n(?P<body>.*?)\r?\n(?P=quote)@(?P<tail>[^\n;]*)", re.DOTALL)
_SHELLS = {"bash", "shell", "run_command", "exec_command", "powershell", "terminal"}
_DOWNLOADS = {"curl", "curl.exe", "wget", "wget.exe", "invoke-webrequest", "invoke-restmethod", "iwr", "irm"}


def _shell_urls(command: str) -> set[str]:
    found: set[str] = set()
    # #164: written files and heredoc bodies cannot establish input-only fetch evidence.
    command = _HEREDOC.sub("", command)
    command = _HERESTRING.sub("", command)
    command = re.sub(r"[A-Za-z]:\\[^\s'\"]+", lambda match: match[0].replace("\\", "/"), command)
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
    bindings: dict[str, str] = {}
    for words in segments:
        assignment = re.fullmatch(r"\$?(\w+)\s*=\s*(.*)", " ".join(words))
        if assignment:
            bindings[assignment[1]] = assignment[2]
            # #164: PowerShell assignment captures a command's output; it still executes the fetch.
            equal = next(index for index, word in enumerate(words) if "=" in word)
            suffix = words[equal].split("=", 1)[1]
            words = ([suffix] if suffix else []) + words[equal + 1:]
        expanded = [bindings.get(word.removeprefix("$").strip("{}"), word) if word.startswith("$") else word for word in words]
        found.update(_command_urls(expanded))
    return found


def _command_urls(words: list[str]) -> set[str]:
    if not words:
        return set()
    name = PurePosixPath(words[0].replace("\\", "/")).name.lower()
    if name in _DOWNLOADS:
        ignored_values = {"-h", "--header", "-o", "--output", "-outfile", "--referer", "-e", "--data", "-d", "--data-raw"}
        return {word.removeprefix("--url=") for index, word in enumerate(words[1:], 1)
                if words[index - 1].lower() not in ignored_values and re.match(r"^(?:--url=)?https?://\S+$", word)}
    if name in {"bash", "sh", "pwsh", "powershell", "pwsh.exe", "powershell.exe"}:
        flag = next((index for index, word in enumerate(words) if word.lower() in {"-c", "-lc", "-command"}), None)
        if flag is not None and flag + 1 < len(words):
            return _shell_urls(" ".join(words[flag + 1:]))
    if name == "uv" and words[1:2] == ["run"]:
        return _command_urls(words[2:])
    if re.fullmatch(r"python[\d.]*|python.exe", name):
        if "-c" in words and words.index("-c") + 1 < len(words):
            return _python_urls(words[words.index("-c") + 1])
    if name in {"node", "node.exe"}:
        source = words[words.index("-e") + 1] if "-e" in words and words.index("-e") + 1 < len(words) else ""
        return _javascript_urls(source)
    return set()


def _javascript_urls(source: str) -> set[str]:
    strings: dict[str, str] = {}

    def mask(match: re.Match[str]) -> str:
        token = match[0]
        if token.startswith(("//", "/*")):
            return " "
        key = f"__trace_string_{len(strings)}__"
        strings[key] = token[1:-1].replace("\\/", "/")
        return key

    # #164: mask entire literals first, so source code written as text cannot impersonate a call.
    masked = re.sub(r'''//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`''', mask, source, flags=re.DOTALL)
    for name, literal in re.findall(r"\b(?:const|let|var)\s+(\w+)\s*=\s*(__trace_string_\d+__)", masked):
        strings[name] = strings[literal]
    found: set[str] = set()
    pattern = r"(?P<call>\bfetch|\b(?:axios|https?|driver)\.get|\.goto|\.navigate|\.createBrowserTab)\(\s*(?P<args>[^)]*)\)"
    for match in re.finditer(pattern, masked):
        args = match["args"].split(",")
        index = 1 if match["call"] == ".createBrowserTab" else 0
        value = strings.get(args[index].strip(), "") if len(args) > index else ""
        if url_key(value):
            found.add(value)
    return found


def fetch_actions(trace: Sequence[ToolCall]) -> list[set[str]]:
    """Fetch inputs only; output labels and reconstructed scripts are not evidence (#164)."""
    actions: list[set[str]] = []
    for call in trace:
        name = call.name.lower()
        # A shell's exit code belongs to the whole script, not each fetch inside it (#164).
        if call.failed and name not in _SHELLS:
            actions.append(set())
            continue
        inputs = call.inputs
        found: set[str] = set()
        if name in _SHELLS:
            found = _shell_urls(str(inputs.get("command", inputs.get("cmd", inputs.get("CommandLine", "")))))
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
            if "click" in name:
                found.update(str(value) for key, value in inputs.items() if key in {"url", "page_url"} and url_key(value))
        actions.append(found)
    return actions


def fetched_urls(trace: Sequence[ToolCall]) -> set[str]:
    return {url_key(url) for action in fetch_actions(trace) for url in action if url_key(url)}
