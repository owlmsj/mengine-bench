"""Fetch provenance regressions from #164, with no network or local paths."""

import json

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
