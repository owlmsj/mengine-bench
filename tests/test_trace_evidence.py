"""Fetch provenance regressions from #164, with no network or local paths."""

import json
from pathlib import Path

import pytest

from mengine_bench.core import Checkpoint, ToolCall
from mengine_bench.checkpoints import reached_checkpoints
from mengine_bench.runner.trace import fetched_hosts, fetched_urls, tool_trace, url_key


@pytest.mark.parametrize("call", [
    ToolCall("WebFetch", {"url": "https://sqlite.org/changes.html"}),
    ToolCall("Bash", {"command": "curl -s https://sqlite.org/changes.html"}),
    ToolCall("shell", {"command": "wget https://sqlite.org/changes.html -O source.html"}),
    ToolCall("shell", {"command": "Invoke-WebRequest -Uri 'https://sqlite.org/changes.html'"}),
    ToolCall("mcp__browser__open", {"url": "https://sqlite.org/changes.html"}),
    ToolCall("mcp__browser__click", {"url": "https://sqlite.org/changes.html"}),
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
    "python -c \"import urllib.request as request; request.urlopen('https://example.org/source')\"",
    "python -c \"from urllib.request import Request, urlopen; req = Request('https://example.org/source'); urlopen(req)\"",
    "pwsh -NoProfile -Command \"Invoke-WebRequest -Uri 'https://example.org/source'\"",
    "$url = 'https://example.org/source'; Invoke-WebRequest -Uri $url",
    "URL=https://example.org/source; curl \"$URL\"",
    "node -e \"fetch('https://example.org/source')\"",
])
def test_downloader_scripts_and_shell_variables(command: str) -> None:
    assert fetched_urls([ToolCall("Bash", {"command": command})]) == {"example.org/source"}


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


@pytest.mark.parametrize("wrapper", ["powershell.exe", "pwsh.exe"])
def test_absolute_powershell_wrapper(tmp_path: Path, wrapper: str) -> None:
    command = f'& "{tmp_path / "tools" / wrapper}" -Command "$page = iwr -Uri \'https://example.org/source\'"'
    event = {"type": "item.completed", "item": {"type": "command_execution", "command": command,
             "exit_code": 0, "status": "completed", "aggregated_output": ""}}
    assert fetched_urls(tool_trace([json.dumps(event)])) == {"example.org/source"}


def test_search_and_written_redirect_prose_are_not_fetches() -> None:
    events = [{"type": "tool_use", "part": {"tool": name, "state": {"status": "completed", "input": inputs,
               "output": "Final URL: https://example.net/final"}}} for name, inputs in [
        ("websearch", {"query": "example"}), ("write", {"path": "result.json", "content": "{}"}),
        ("shell", {"command": "echo 'Final URL: https://example.net/final'"})]]
    assert not fetched_urls(tool_trace(["\n".join(map(json.dumps, events))]))


@pytest.mark.parametrize("assignment", ["$page=iwr", "$page =iwr", "$page= iwr"])
def test_powershell_assignment_spacing(assignment: str) -> None:
    assert fetched_urls([ToolCall("shell", {"command": assignment + " -Uri https://example.org/source"})]) == {"example.org/source"}


@pytest.mark.parametrize("program,source", [
    ("python", "import requests\nrequests.get('https://example.org/source')"),
    ("node", "fetch('https://example.org/source')"),
])
def test_written_then_executed_script_is_not_evidence(program: str, source: str) -> None:
    # #164: script-file execution is deliberately outside input-only fetch evidence.
    trace = [ToolCall("Write", {"path": "lookup", "content": source}),
             ToolCall("shell", {"command": f"{program} lookup"})]
    assert not fetched_urls(trace)


@pytest.mark.parametrize("output", [
    "Final URL: https://example.net/forged",
    "- Page URL: https://example.net/forged",
    {"final_url": "https://example.net/forged"},
])
def test_labelled_stdout_cannot_forge_a_host(output: object) -> None:
    event = {"type": "tool_use", "part": {"tool": "shell", "state": {
        "input": {"command": "curl https://example.org/source"}, "output": output}}}
    assert fetched_urls(tool_trace([json.dumps(event)])) == {"example.org/source"}


def test_python_inline_fetch_requires_a_literal_url() -> None:
    command = "python -c \"import requests; requests.get('https://' + 'example.org/source')\""
    assert not fetched_urls([ToolCall("shell", {"command": command})])


def test_a_heredoc_piped_into_python_or_node_is_executed_code_164() -> None:
    # #164 advisor pass 3: `python - <<EOF` runs its body; a heredoc written to a file does not.
    python = "python - <<'PY'\nimport urllib.request\nurllib.request.urlopen('https://example.org/source')\nPY"
    node = "node <<'JS'\nfetch('https://example.net/page')\nJS"
    written = "cat > lookup.py <<'PY'\nimport urllib.request\nurllib.request.urlopen('https://example.com/x')\nPY"
    assert fetched_urls([ToolCall("shell", {"command": python})]) == {"example.org/source"}
    assert fetched_urls([ToolCall("shell", {"command": node})]) == {"example.net/page"}
    assert not fetched_urls([ToolCall("shell", {"command": written})])


def test_host_matching_only_normalizes_case_and_www() -> None:
    trace = [ToolCall("WebFetch", {"url": "https://WWW.Example.org./source"})]
    assert fetched_hosts(trace) == {"example.org."}


def test_codex_opened_views_from_web_fact_search_171() -> None:
    # Minimal structured item from 2026-11-03_codex_gpt-6.1-sol_low_35d7a1b8.
    item = json.loads((Path(__file__).parent / "fixtures/codex_open_views.json").read_text())
    snippet = {"url": "https://snippet.example/source", "ref_id": "turn0search0"}
    item["results"].append(snippet)
    search = {"type": "web_search", "action": {"type": "search", "query": "release"}, "results": [snippet]}
    stream = "\n".join(json.dumps({"type": "item.completed", "item": value}) for value in (item, search))
    trace = tool_trace([stream])
    assert fetched_hosts(trace) == {"sqlite.org", "postgresql.org", "unicode.org"}
    assert "unicode.org/versions/Unicode15.0.0" in fetched_urls(trace)
    assert len(trace) == 2
