"""Fetch provenance regressions from #164, with no network or local paths."""

import json
from pathlib import Path

import pytest

from mengine_bench.core import Checkpoint, ToolCall
from mengine_bench.checkpoints import reached_checkpoints
from mengine_bench.runner.trace import fetched_urls, tool_trace, url_key


@pytest.mark.parametrize("call", [
    ToolCall("WebFetch", {"url": "https://sqlite.org/changes.html"}),
    ToolCall("Bash", {"command": "curl -s https://sqlite.org/changes.html"}),
    ToolCall("shell", {"command": "wget https://sqlite.org/changes.html -O source.html"}),
    ToolCall("shell", {"command": "Invoke-WebRequest -Uri 'https://sqlite.org/changes.html'"}),
    ToolCall("mcp__browser__navigate", {"url": "https://sqlite.org/changes.html"}),
    ToolCall("web.run", {"open": [{"ref_id": "https://sqlite.org/changes.html"}]}),
    ToolCall("Bash", {"command": "python -c \"import requests; requests.get('https://sqlite.org/changes.html')\""}),
])
def test_fetch_routes(call: ToolCall) -> None:
    assert url_key("https://sqlite.org/changes.html") in fetched_urls([call])


@pytest.mark.parametrize("call", [
    ToolCall("Write", {"file_path": "result.json", "content": "https://sqlite.org/changes.html"}),
    ToolCall("Bash", {"command": "cat > result.json <<'EOF'\nhttps://sqlite.org/changes.html\ncurl https://sqlite.org/changes.html\nEOF"}),
    ToolCall("WebSearch", {"query": "https://sqlite.org/changes.html"}),
    ToolCall("Bash", {"command": "echo 'curl https://sqlite.org/changes.html'"}),
])
def test_written_or_searched_urls_are_not_fetches(call: ToolCall) -> None:
    assert not fetched_urls([call])


def test_checkpoint_does_not_match_its_own_heredoc() -> None:
    stream = json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Bash", "input": {"command": "cat > result.json <<'EOF'\nsqlite.org\nEOF"}},
        {"type": "tool_use", "name": "WebFetch", "input": {"url": "https://sqlite.org/changes.html"}},
    ]}})
    mark = Checkpoint("opened a source", "https?://", fetch_only=True)
    assert reached_checkpoints([mark], [stream]) == [{"name": "opened a source", "call": 2}]
    assert len(tool_trace([stream])) == 2


@pytest.mark.parametrize("event", [
    {"type": "tool_use", "part": {"tool": "webfetch", "state": {"input": {"url": "https://example.org/source"}}}},
    {"type": "item.completed", "item": {"type": "mcp_tool_call", "tool": "browser_navigate", "arguments": {"url": "https://example.org/source"}}},
    {"type": "item.completed", "item": {"type": "web_search", "action": {"type": "open_page", "url": "https://example.org/source"}}},
    {"event": "step_update", "step_update": {"step_type": "tool", "state": "DONE", "tool_name": "read_url_content", "tool_info": {"parameters": {"Url": "https://example.org/source"}}}},
])
def test_harness_fetch_shapes(event: dict[str, object]) -> None:
    assert fetched_urls(tool_trace([json.dumps(event)])) == {"example.org/source"}


@pytest.mark.parametrize("command", [
    "python -I - <<'PY'\nimport requests\nurl = 'https://example.org/source'\nrequests.get(url)\nPY",
    "python -c \"import urllib.request as request; request.urlopen('https://example.org/source')\"",
    "python -c \"from urllib.request import Request, urlopen; req = Request('https://example.org/source'); urlopen(req)\"",
    "pwsh -NoProfile -Command \"Invoke-WebRequest -Uri 'https://example.org/source'\"",
    "$url = 'https://example.org/source'; Invoke-WebRequest -Uri $url",
    "URL=https://example.org/source; curl \"$URL\"",
    "node -e \"fetch('https://example.org/source')\"",
])
def test_downloader_scripts_and_shell_variables(command: str) -> None:
    assert fetched_urls([ToolCall("Bash", {"command": command})]) == {"example.org/source"}


def test_a_written_script_counts_only_when_executed() -> None:
    script = ToolCall("Write", {"file_path": "lookup.py", "content": "import requests\nrequests.get('https://example.org/source')"})
    assert fetched_urls([script]) == set()
    assert fetched_urls([script, ToolCall("Bash", {"command": "python lookup.py"})]) == {"example.org/source"}


def test_written_heredoc_script_counts_only_when_executed() -> None:
    command = "cat > lookup.py <<'PY'\nimport requests\nrequests.get('https://example.org/source')\nPY\npython lookup.py"
    assert fetched_urls([ToolCall("Bash", {"command": command})]) == {"example.org/source"}


def test_result_text_in_a_downloader_script_is_not_a_fetch() -> None:
    command = "python - <<'PY'\nimport requests\nrequests.get('https://example.org/opened')\nresult = {'url': 'https://example.org/unopened'}\nPY"
    assert fetched_urls([ToolCall("Bash", {"command": command})]) == {"example.org/opened"}


def test_curl_header_is_not_a_fetched_page() -> None:
    command = "curl -H 'Referer: https://example.org/not-opened' https://example.org/opened"
    assert fetched_urls([ToolCall("Bash", {"command": command})]) == {"example.org/opened"}


def test_browser_code_navigation() -> None:
    trace = [ToolCall("mcp__cua_repl__js", {"code": "await tab.goto('https://example.org/source')"})]
    assert fetched_urls(trace) == {"example.org/source"}


def test_javascript_written_fetch_text_is_not_a_fetch() -> None:
    script = "fs.writeFileSync('result.json', \"fetch('https://example.org/unopened')\"); fetch('https://example.org/opened')"
    assert fetched_urls([ToolCall("browser_execute", {"code": script})]) == {"example.org/opened"}


def test_browser_navigation_through_a_url_variable() -> None:
    script = "const url = 'https://example.org/source'; await page.goto(url)"
    assert fetched_urls([ToolCall("browser_execute", {"code": script})]) == {"example.org/source"}


def test_powershell_written_here_string_is_not_a_fetch() -> None:
    command = "@'\ncurl https://example.org/unopened\n'@ | Set-Content result.json"
    assert not fetched_urls([ToolCall("shell", {"command": command})])


def test_failed_fetch_does_not_confirm_a_source() -> None:
    events = [
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "fetch-1", "name": "WebFetch", "input": {"url": "https://example.org/source"}}]}},
        {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "fetch-1", "is_error": True, "content": "connection refused"}]}},
    ]
    assert not fetched_urls(tool_trace(["\n".join(map(json.dumps, events))]))


def test_a_later_shell_failure_does_not_erase_a_fetch_action() -> None:
    trace = [ToolCall("shell", {"command": "curl https://example.org/source; exit 1"}, failed=True)]
    assert fetched_urls(trace) == {"example.org/source"}


def test_non_tool_and_incomplete_events_are_ignored() -> None:
    events = [
        {"type": "user", "message": {"content": None}},
        {"type": "assistant", "message": {"content": "https://example.org/source"}},
        {"type": "item.started", "item": {"type": "command_execution", "command": "curl https://example.org/source"}},
        {"event": "step_update", "step_update": {"step_type": "tool", "state": "ACTIVE", "tool_name": "fetch_url"}},
    ]
    assert tool_trace(["\n".join(map(json.dumps, events))]) == ()


@pytest.mark.parametrize("downloader", ["Invoke-WebRequest", "iwr", "irm", "curl"])
@pytest.mark.parametrize("wrapper", ["", "powershell.exe", "pwsh.exe"])
def test_assigned_powershell_fetches(downloader: str, wrapper: str) -> None:
    command = f"$page = {downloader} -Uri 'https://example.org/source'"
    if wrapper:
        command = f'{wrapper} -NoProfile -Command "{command}"'
    event = {"type": "tool_use", "part": {"tool": "bash", "state": {"status": "completed", "input": {"command": command}}}}
    assert fetched_urls(tool_trace([json.dumps(event)])) == {"example.org/source"}


def test_edit_then_execute_python_script() -> None:
    events = [
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Write", "input": {
            "file_path": "scripts/lookup.py", "content": "import httpx\nurl = 'https://example.org/old'\nhttpx.get(url)\n"}}]}},
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Edit", "input": {
            "file_path": "scripts/lookup.py", "old_string": "example.org/old", "new_string": "example.org/source"}}]}},
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash", "input": {
            "command": "python ./scripts/lookup.py"}}]}},
    ]
    assert fetched_urls(tool_trace(["\n".join(map(json.dumps, events))])) == {"example.org/source"}


def test_apply_patch_then_execute_python_script() -> None:
    patch = "*** Begin Patch\n*** Add File: lookup.py\n+import urllib.request\n+urllib.request.urlopen('https://example.org/source')\n*** End Patch"
    events = [
        {"type": "tool_use", "part": {"tool": "apply_patch", "state": {"status": "completed", "input": {"patchText": patch}}}},
        {"type": "tool_use", "part": {"tool": "bash", "state": {"status": "completed", "input": {"command": "python ./lookup.py"}}}},
    ]
    assert fetched_urls(tool_trace(["\n".join(map(json.dumps, events))])) == {"example.org/source"}


def test_curl_redirect_result_confirms_final_host() -> None:
    events = [
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "download", "name": "Bash", "input": {
            "command": "curl -L -o source.html -w '%{url_effective}' https://example.org/start"}}]}},
        {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "download", "content": "https://example.net/final"}]}},
    ]
    assert fetched_urls(tool_trace(["\n".join(map(json.dumps, events))])) == {"example.org/start", "example.net/final"}


def test_browser_click_confirms_its_page_url() -> None:
    event = {"type": "item.completed", "item": {"type": "mcp_tool_call", "tool": "browser_click", "arguments": {
        "element": "Source", "ref": "e3"}, "result": {"content": [{"type": "text", "text": "- Page URL: https://example.org/source\n- Page Title: Source"}]}}}
    assert fetched_urls(tool_trace([json.dumps(event)])) == {"example.org/source"}


@pytest.mark.parametrize("wrapper", ["powershell.exe", "pwsh.exe"])
def test_absolute_powershell_wrapper(tmp_path: Path, wrapper: str) -> None:
    command = f'& "{tmp_path / "tools" / wrapper}" -Command "$page = iwr -Uri \'https://example.org/source\'"'
    event = {"type": "item.completed", "item": {"type": "command_execution", "command": command,
             "exit_code": 0, "status": "completed", "aggregated_output": ""}}
    assert fetched_urls(tool_trace([json.dumps(event)])) == {"example.org/source"}


@pytest.mark.parametrize("absolute_edit", [True, False])
def test_codex_patch_without_contents_uses_final_workspace(tmp_path: Path, absolute_edit: bool) -> None:
    source = tmp_path / "lookup.py"
    source.write_text("import requests\nrequests.get('https://example.org/source')\n")
    events = [
        {"type": "item.completed", "item": {"id": "item_1", "type": "file_change", "status": "completed", "changes": [
            {"path": str(source) if absolute_edit else "lookup.py", "kind": "add"}]}},
        {"type": "item.completed", "item": {"id": "item_2", "type": "command_execution", "status": "completed",
            "command": 'python ./lookup.py' if absolute_edit else f'python "{source}"', "exit_code": 0, "aggregated_output": ""}},
    ]
    stream = "\n".join(map(json.dumps, events))
    assert not fetched_urls(tool_trace([stream]))
    assert fetched_urls(tool_trace([stream], tmp_path)) == {"example.org/source"}


def test_final_script_cannot_prove_fetch_before_last_edit(tmp_path: Path) -> None:
    (tmp_path / "lookup.py").write_text("import requests\nrequests.get('https://example.org/source')\n")
    patch = {"type": "item.completed", "item": {"type": "file_change", "status": "completed", "changes": [{"path": "lookup.py", "kind": "update"}]}}
    execute = {"type": "item.completed", "item": {"type": "command_execution", "command": "python lookup.py", "exit_code": 0}}
    assert not fetched_urls(tool_trace(["\n".join(map(json.dumps, [patch, execute, patch]))], tmp_path))


def test_open_code_edit_shape_and_python_alias() -> None:
    rows = [
        ("write", {"path": "lookup.py", "content": "import httpx as client\nclient.get('https://example.org/old')\n"}),
        ("edit", {"path": "lookup.py", "oldString": "example.org/old", "newString": "example.org/source"}),
        ("shell", {"command": "python lookup.py", "workdir": "."}),
    ]
    events = [{"type": "tool_use", "part": {"type": "tool", "tool": name, "state": {
        "status": "completed", "input": inputs, "output": "", "title": name, "metadata": {}, "time": {"start": 1, "end": 2}}}}
        for name, inputs in rows]
    assert fetched_urls(tool_trace(["\n".join(map(json.dumps, events))])) == {"example.org/source"}


def test_patch_heredoc_and_update_remove_old_fetch() -> None:
    add = "*** Begin Patch\n*** Add File: lookup.py\n+import requests\n+requests.get('https://example.org/old')\n*** End Patch"
    update = "*** Begin Patch\n*** Update File: lookup.py\n@@\n-requests.get('https://example.org/old')\n+requests.get('https://example.org/source')\n*** End Patch"
    command = f"apply_patch <<'PATCH'\n{add}\nPATCH\napply_patch <<'PATCH'\n{update}\nPATCH\npython lookup.py"
    assert fetched_urls([ToolCall("shell", {"command": command})]) == {"example.org/source"}


def test_search_and_written_redirect_prose_are_not_fetches() -> None:
    events = [{"type": "tool_use", "part": {"tool": name, "state": {"status": "completed", "input": inputs,
               "output": "Final URL: https://example.net/final"}}} for name, inputs in [
        ("websearch", {"query": "example"}), ("write", {"path": "result.json", "content": "{}"}),
        ("shell", {"command": "echo 'Final URL: https://example.net/final'"})]]
    assert not fetched_urls(tool_trace(["\n".join(map(json.dumps, events))]))


def test_powershell_here_string_script_counts_only_when_executed() -> None:
    command = "@'\nimport requests\nrequests.get('https://example.org/source')\n'@ | Set-Content lookup.py"
    assert not fetched_urls([ToolCall("shell", {"command": command})])
    assert fetched_urls([ToolCall("shell", {"command": command + "; python ./lookup.py"})]) == {"example.org/source"}


def test_codex_patch_recovery_survives_settled_workspace(tmp_path: Path) -> None:
    original, settled = tmp_path / "original", tmp_path / "settled"
    settled.mkdir()
    (settled / "lookup.py").write_text("import requests\nrequests.get('https://example.org/source')\n")
    events = [
        {"type": "item.completed", "item": {"type": "file_change", "status": "completed", "changes": [{"path": str(original / "lookup.py"), "kind": "add"}]}},
        {"type": "item.completed", "item": {"type": "command_execution", "command": "python lookup.py", "exit_code": 0}},
    ]
    assert fetched_urls(tool_trace(["\n".join(map(json.dumps, events))], settled, original)) == {"example.org/source"}


@pytest.mark.parametrize("late_tool", ["write", "edit", "shell"])
def test_later_other_edit_route_cannot_rewrite_codex_execution(tmp_path: Path, late_tool: str) -> None:
    source = "import requests\nrequests.get('https://example.org/source')\n"
    (tmp_path / "lookup.py").write_text(source)
    inputs = {"write": {"path": "lookup.py", "content": source},
              "edit": {"path": "lookup.py", "oldString": "print(1)", "newString": source},
              "shell": {"command": f"cat > lookup.py <<'PY'\n{source}\nPY"}}[late_tool]
    events = [
        {"type": "item.completed", "item": {"type": "file_change", "status": "completed", "changes": [{"path": "lookup.py", "kind": "add"}]}},
        {"type": "item.completed", "item": {"type": "command_execution", "command": "python lookup.py", "exit_code": 0}},
        {"type": "tool_use", "part": {"tool": late_tool, "state": {"status": "completed", "input": inputs}}},
    ]
    assert not fetched_urls(tool_trace(["\n".join(map(json.dumps, events))], tmp_path))


def test_wget_final_host_and_unlabelled_page_links() -> None:
    event = {"type": "tool_use", "part": {"tool": "shell", "state": {"status": "completed", "input": {
        "command": "wget https://example.org/start"}, "output": "--2026-01-01 12:00:00--  https://example.org/start\n--2026-01-01 12:00:01--  https://example.net/final\nhttps://example.com/unopened"}}}
    assert fetched_urls(tool_trace([json.dumps(event)])) == {"example.org/start", "example.net/final"}


@pytest.mark.parametrize("assignment", ["$page=iwr", "$page =iwr", "$page= iwr"])
def test_powershell_assignment_spacing(assignment: str) -> None:
    assert fetched_urls([ToolCall("shell", {"command": assignment + " -Uri https://example.org/source"})]) == {"example.org/source"}


@pytest.mark.parametrize("constructor", ["requests.Session", "httpx.Client"])
def test_python_client_variable_names(constructor: str) -> None:
    source = f"import {constructor.split('.')[0]}\nconnection = {constructor}()\nconnection.get('https://example.org/source')\n"
    trace = [ToolCall("Write", {"path": "lookup.py", "content": source}), ToolCall("shell", {"command": "python lookup.py"})]
    assert fetched_urls(trace) == {"example.org/source"}
