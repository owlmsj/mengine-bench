"""Tool inputs and source-fetch evidence, shared by checks and checkpoints (#164)."""

from __future__ import annotations

import ast
import json
import posixpath
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


def _call(name: object, inputs: object, *, failed: bool = False, output: object = None) -> ToolCall:
    if isinstance(inputs, str):
        try:
            inputs = json.loads(inputs)
        except ValueError:
            inputs = {"command": inputs}
    parameters = dict(_mapping(inputs))
    # #164: retain only explicit destination metadata, never URLs in page prose or snippets.
    destinations = _result_destinations(output, str(parameters.get("command", parameters.get("cmd", ""))))
    if destinations:
        parameters["_trace_destinations"] = sorted(destinations)
    return ToolCall(str(name or ""), parameters, failed)


def _result_destinations(output: object, command: str = "") -> set[str]:
    if isinstance(output, dict):
        found = {str(value) for key, value in output.items()
                 if key.lower() in {"final_url", "effective_url", "url_effective", "responseuri"} and url_key(value)}
        return found | set().union(*(_result_destinations(value, command) for key, value in output.items()
                                     if key in {"content", "text", "output"}))
    if isinstance(output, list):
        return set().union(*(_result_destinations(value, command) for value in output))
    if not isinstance(output, str):
        return set()
    found = set(re.findall(r"(?im)^\s*(?:- )?(?:Page URL|Final URL|effective_url|url_effective|ResponseUri):\s*(https?://\S+)", output))
    if "url_effective" in command:
        found.update(re.findall(r"(?m)^\s*(https?://\S+)\s*$", output))
    if re.search(r"\bwget(?:\.exe)?\b", command):
        hops = re.findall(r"(?m)^--[^\n]+?--\s+(https?://\S+)", output)
        found.update(hops[-1:])
    return found


def _event_calls(event: Mapping[str, object], failures: set[str], outputs: Mapping[str, object]) -> list[ToolCall]:
    kind = event.get("type")
    if kind == "assistant":
        return [_call(block.get("name"), block.get("input"), failed=str(block.get("id")) in failures,
                      output=outputs.get(str(block.get("id"))))
                for block in _blocks(event) if block.get("type") == "tool_use"]
    if kind == "tool_use":
        part = _mapping(event.get("part"))
        state = _mapping(part.get("state"))
        return [_call(part.get("tool"), state.get("input"), failed=state.get("status") == "error", output=state.get("output"))]
    if kind == "item.completed":
        item = _mapping(event.get("item"))
        subtype = item.get("type")
        failed = item.get("status") == "failed" or item.get("exit_code") not in (None, 0)
        if subtype == "command_execution":
            return [_call("shell", {"command": item.get("command")}, failed=failed, output=item.get("aggregated_output"))]
        if subtype == "file_change":
            return [_call("apply_patch", {"changes": item.get("changes")}, failed=failed)]
        if subtype == "mcp_tool_call":
            return [_call(item.get("tool"), item.get("arguments"), failed=failed, output=item.get("result"))]
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
        outputs = {str(block.get("tool_use_id")): block.get("content") for event in events if event.get("type") == "user"
                   for block in _blocks(event) if block.get("type") == "tool_result"}
        calls.extend(call for event in events for call in _event_calls(event, failures, outputs))
    if workspace is not None:
        calls = _recover_final_scripts(calls, workspace, original_workspace)
    return tuple(calls)


def url_key(url: object) -> str:
    """Distinct fetched URL identity; query values remain distinct sources (#164)."""
    try:
        parsed = urlsplit(str(url or "").strip())
        host = (parsed.hostname or "").lower().removeprefix("www.").rstrip(".")
        if parsed.scheme not in ("http", "https") or not host:
            return ""
        return host + (f":{parsed.port}" if parsed.port else "") + (parsed.path.rstrip("/") or "/") + (f"?{parsed.query}" if parsed.query else "")
    except ValueError:
        return ""


def host_key(url: object) -> str:
    if not url_key(url):
        return ""
    return (urlsplit(str(url).strip()).hostname or "").lower().removeprefix("www.").rstrip(".")


def fetched_hosts(trace: Sequence[ToolCall]) -> set[str]:
    return {host_key(url) for action in fetch_actions(trace) for url in action if host_key(url)}


def _literal_strings(node: ast.AST, bindings: Mapping[str, set[str]]) -> set[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return {node.value}
    if isinstance(node, ast.Name):
        return bindings.get(node.id, set())
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return set().union(*(_literal_strings(item, bindings) for item in node.elts))
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return {left + right for left in _literal_strings(node.left, bindings) for right in _literal_strings(node.right, bindings)}
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


def _script_key(path: str) -> str:
    return posixpath.normpath(path.replace("\\", "/"))


def _script_lookup(path: str, scripts: Mapping[str, str]) -> str | None:
    key = _script_key(path)
    if key in scripts:
        return key
    matches = [candidate for candidate in scripts if candidate.endswith("/" + key) or key.endswith("/" + candidate)]
    return matches[0] if len(matches) == 1 else None


def _patch_scripts(patch: str, scripts: dict[str, str]) -> None:
    sections = re.split(r"(?m)^\*\*\* (Add|Update|Delete) File: (.+)\n", patch)
    for index in range(1, len(sections), 3):
        operation, path, body = sections[index:index + 3]
        key = _script_lookup(path, scripts) or _script_key(path)
        if operation == "Delete":
            scripts.pop(key, None)
            continue
        if operation == "Add":
            scripts[key] = "\n".join(line[1:] for line in body.splitlines() if line.startswith("+")) + "\n"
            continue
        scripts[key] = _patched_source(scripts.get(key, ""), body)


def _patched_source(source: str, diff: str) -> str:
    for chunk in re.split(r"(?m)^@@[^\n]*\n", diff):
        lines = [line for line in chunk.splitlines() if line[:1] in {" ", "+", "-"}
                 and not line.startswith(("+++", "---"))]
        if not lines:
            continue
        old = "\n".join(line[1:] for line in lines if line[0] != "+")
        new = "\n".join(line[1:] for line in lines if line[0] != "-")
        if old and old in source:
            source = source.replace(old, new, 1)
        elif not source and not old:
            source = new + "\n"
    return source


def _remember_script(call: ToolCall, scripts: dict[str, str]) -> None:
    inputs, name = call.inputs, call.name.lower()
    path = inputs.get("file_path", inputs.get("path", inputs.get("filePath", inputs.get("TargetFile"))))
    body = inputs.get("content", inputs.get("CodeContent"))
    key = (_script_lookup(path, scripts) or _script_key(path)) if isinstance(path, str) else None
    if key and name in {"write", "write_file", "write_to_file"} and isinstance(body, str):
        scripts[key] = body
    if key and name in {"edit", "edit_file"}:
        old, new = inputs.get("old_string", inputs.get("oldString")), inputs.get("new_string", inputs.get("newString"))
        if isinstance(old, str) and isinstance(new, str) and old:
            scripts[key] = scripts.get(key, "").replace(old, new, -1 if inputs.get("replace_all", inputs.get("replaceAll")) else 1)
    if "apply_patch" not in name:
        return
    patch = inputs.get("patch", inputs.get("patchText", inputs.get("input", inputs.get("command"))))
    if isinstance(patch, str):
        _patch_scripts(patch, scripts)
    changes = inputs.get("changes", [])
    for change in changes if isinstance(changes, list) else []:
        if not isinstance(change, dict) or not isinstance(change.get("path"), str):
            continue
        key = _script_lookup(change["path"], scripts) or _script_key(change["path"])
        if change.get("kind") == "delete":
            scripts.pop(key, None)
        elif isinstance(change.get("content"), str):
            scripts[key] = change["content"]
        elif isinstance(change.get("diff"), str):
            scripts[key] = _patched_source(scripts.get(key, ""), change["diff"])
        else:
            scripts.pop(key, None)


def _recover_final_scripts(calls: list[ToolCall], workspace: Path, original_workspace: Path | None) -> list[ToolCall]:
    # #164: Codex JSONL omits patch contents. Recover only the last mutation, never use future bytes at an earlier edit.
    seen: set[str] = set()
    recovered: list[ToolCall] = []
    for call in reversed(calls):
        inputs = dict(call.inputs)
        touched: dict[str, str] = {}
        if not call.failed:
            _remember_script(call, touched)
        if call.name.lower() in _SHELLS:
            _shell_urls(str(inputs.get("command", inputs.get("cmd", ""))), touched)
        seen.update(touched)
        changes = inputs.get("changes")
        if not call.failed and isinstance(changes, list):
            copied = [dict(change) for change in changes if isinstance(change, dict)]
            for change in copied:
                path = str(change.get("path", ""))
                key = _script_key(path)
                source = Path(path)
                if original_workspace is not None and source.is_absolute() and source.is_relative_to(original_workspace):
                    source = source.relative_to(original_workspace)
                candidate = (workspace / source).resolve()
                already_seen = _script_lookup(key, {item: "" for item in seen}) is not None
                seen.add(key)
                if already_seen or candidate.suffix not in {".py", ".js"} or not candidate.is_relative_to(workspace.resolve()):
                    continue
                try:
                    change["content"] = candidate.read_text(encoding="utf-8")
                except (OSError, UnicodeError):
                    pass
            inputs["changes"] = copied
        recovered.append(ToolCall(call.name, inputs, call.failed))
    return list(reversed(recovered))


def _shell_urls(command: str, scripts: dict[str, str]) -> set[str]:
    found: set[str] = set()

    def heredoc(match: re.Match[str]) -> str:
        head, body = match["head"].strip(), match["body"]
        if re.match(r"(?:python[\d.]*|uv run python)\b", head):
            found.update(_python_urls(body))
        dest = re.search(r">\s*['\"]?([\w./-]+)", head)
        if dest and re.match(r"cat\b", head):
            scripts[_script_key(dest[1])] = body
        if re.match(r"apply_patch\b", head):
            _patch_scripts(body, scripts)
        return ""

    def here_string(match: re.Match[str]) -> str:
        destination = re.search(r"(?:\|\s*(?:Set-Content|Out-File)\s+(?:(?:-Path|-FilePath)\s+)?|>)['\"]?([^\s'\"]+)", match["tail"], re.IGNORECASE)
        if destination:
            scripts[_script_key(destination[1])] = match["body"]
        return ""

    command = _HEREDOC.sub(heredoc, command)
    command = _HERESTRING.sub(here_string, command)
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
        found.update(_command_urls(expanded, scripts))
    return found


def _command_urls(words: list[str], scripts: dict[str, str]) -> set[str]:
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
            return _shell_urls(" ".join(words[flag + 1:]), scripts)
    if name == "uv" and words[1:2] == ["run"]:
        return _command_urls(words[2:], scripts)
    if re.fullmatch(r"python[\d.]*|python.exe", name):
        if "-c" in words and words.index("-c") + 1 < len(words):
            return _python_urls(words[words.index("-c") + 1])
        script = next((key for word in words[1:] if (key := _script_lookup(word, scripts)) is not None), None)
        return _python_urls(scripts[script]) if script else set()
    if name in {"node", "node.exe"}:
        source = words[words.index("-e") + 1] if "-e" in words and words.index("-e") + 1 < len(words) else scripts.get(words[-1], "")
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
    """Fetch inputs and explicit destination metadata; never search snippets or written prose."""
    scripts: dict[str, str] = {}
    actions: list[set[str]] = []
    for call in trace:
        name = call.name.lower()
        # A shell's exit code belongs to the whole script, not each fetch inside it (#164).
        if call.failed and name not in _SHELLS:
            actions.append(set())
            continue
        inputs = call.inputs
        found: set[str] = set()
        _remember_script(call, scripts)
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
            if "click" in name:
                found.update(str(value) for key, value in inputs.items() if key in {"url", "page_url"} and url_key(value))
        if found or (("browser" in name or "cua" in name) and "click" in name):
            found.update(str(value) for value in inputs.get("_trace_destinations", []) if url_key(value))
        actions.append(found)
    return actions


def fetched_urls(trace: Sequence[ToolCall]) -> set[str]:
    return {url_key(url) for action in fetch_actions(trace) for url in action if url_key(url)}
