"""The unreal-mcp mock speaks the live editor's MCP and signs every call (mengine-qlora #22 track U)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

from mengine_bench.runner.site import serve_site
from mengine_bench.sites.signed_store import DATA_DIR, KEY_FILE, verify
from mengine_bench.sites.unreal_mcp_mock import UE_DATA_DIR, UE_SEED_FILE, apply_unreal_mcp
from mengine_bench.sites.unreal_mcp_tools import UE_ST

UE_MOCK = "mengine_bench.sites.unreal_mcp_mock"
ST_HUD = "/Game/UI/ST_Hud.ST_Hud"
LIVE_ROOT_TOOLS = ["capture_image", "deep_research", "execute_python_code", "discover_python_module",
                   "discover_python_class", "discover_python_function", "list_python_subsystems", "terrain_data",
                   "list_toolsets", "describe_toolset", "call_tool"]


class McpClient:
    def __init__(self, url: str) -> None:
        self.url, self.session, self.next_id = url, "", 0

    def post(self, body: dict) -> tuple[int, dict[str, str], dict | None]:
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        request = urllib.request.Request(self.url, data=json.dumps(body).encode(), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=10) as reply:
                status, head, raw = reply.status, dict(reply.headers), reply.read()
        except urllib.error.HTTPError as error:
            status, head, raw = error.code, dict(error.headers), error.read()
        return status, head, json.loads(raw) if raw else None

    def rpc(self, method: str, params: dict | None = None) -> dict:
        self.next_id += 1
        status, _, reply = self.post({"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params or {}})
        assert status == 200 and reply is not None and reply["id"] == self.next_id, (status, reply)
        return reply["result"]

    def tool(self, toolset: str, name: str, arguments: dict) -> dict:
        return self.rpc("tools/call", {"name": "call_tool", "arguments": {"toolset_name": toolset, "tool_name": name,
                                                                         "arguments": arguments}})


def _seed(ws: Path) -> None:
    (ws / DATA_DIR).mkdir(parents=True)
    world = {"string_tables": {ST_HUD: {"namespace": "Hud", "entries": {"Paused": "FLOW PAUSED.", "Resume": "RESUME"}}}}
    (ws / DATA_DIR / UE_SEED_FILE).write_text(json.dumps(world), encoding="utf-8")


def test_mock_round_trip_serves_the_live_surface_and_signs_a_mutation(tmp_path: Path) -> None:
    ws = tmp_path / "ws"
    _seed(ws)
    with serve_site(UE_MOCK, ws) as site:
        assert site is not None
        # OpenCode may add ?codemode=false to a remote MCP URL; the mock ignores the query.
        client = McpClient(site.url + "/mcp?codemode=false")
        client.next_id += 1
        status, head, reply = client.post({"jsonrpc": "2.0", "id": client.next_id, "method": "initialize",
                                           "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                                                      "clientInfo": {"name": "test", "version": "1"}}})
        assert status == 200 and reply["result"]["protocolVersion"] == "2025-06-18"
        client.session = head["Mcp-Session-Id"]
        assert client.post({"jsonrpc": "2.0", "method": "notifications/initialized"})[0] == 202
        assert [tool["name"] for tool in client.rpc("tools/list")["tools"]] == LIVE_ROOT_TOOLS
        listing = client.rpc("tools/call", {"name": "list_toolsets", "arguments": {}})["content"][0]["text"]
        assert listing == (UE_DATA_DIR / "list_toolsets.md").read_text(encoding="utf-8")
        described = client.rpc("tools/call", {"name": "describe_toolset", "arguments": {"toolset_name": UE_ST}})
        assert json.loads(described["content"][0]["text"])["name"] == UE_ST and "isError" not in described
        unknown = client.rpc("tools/call", {"name": "describe_toolset", "arguments": {"toolset_name": "StringTableTools"}})
        assert unknown["isError"] and "Available toolsets: ToolsetRegistry.AgentSkillToolset" in unknown["content"][0]["text"]

        table = {"refPath": ST_HUD}
        changed = client.tool(UE_ST, "set_entry", {"string_table": table, "key": "Paused", "value": "CANVAS PAUSED."})
        assert changed == {"content": [{"type": "text", "text": '{"returnValue":null}'}]}
        read = client.tool(UE_ST, "get_entry", {"string_table": {"refPath": "/Game/UI/ST_Hud"}, "key": "Paused"})
        assert read["content"][0]["text"] == '{"returnValue":"CANVAS PAUSED."}'
        missing = client.tool(UE_ST, "list_keys", {})
        assert missing["isError"] and missing["content"][0]["text"].startswith(
            'Function "list_keys", input params are required by the function input schema Json')
        python = client.rpc("tools/call", {"name": "execute_python_code", "arguments": {"code": "import unreal"}})
        assert python["isError"] and "disabled in this environment" in python["content"][0]["text"]
        status, _, error = client.post({"jsonrpc": "2.0", "id": 99, "method": "tools/call",
                                        "params": {"name": "not_a_root_tool", "arguments": {}}})
        assert (status, error["error"]) == (400, {"code": -32602, "message": "Unknown tool: not_a_root_tool"})
        get_status = urllib.request.Request(site.url + "/mcp", method="GET")
        try:
            urllib.request.urlopen(get_status, timeout=10)
            raise AssertionError("GET /mcp answered 2xx; expected 405 like the live editor")
        except urllib.error.HTTPError as http:
            assert http.code == 405
    assert not (ws / DATA_DIR / UE_SEED_FILE).exists(), "the server reads the seed once and removes it"
    key = bytes.fromhex((ws / DATA_DIR / KEY_FILE).read_text(encoding="ascii"))
    state, events = verify(ws / DATA_DIR, key, apply_unreal_mcp)
    assert state["string_tables"][ST_HUD]["entries"] == {"Paused": "CANVAS PAUSED.", "Resume": "RESUME"}
    assert state["dirty"] == ["/Game/UI/ST_Hud"]
    calls = [(e["tool"], e.get("name"), e["ok"]) for e in events if e["type"] == "call"]
    assert calls == [("list_toolsets", None, True), ("describe_toolset", None, True), ("describe_toolset", None, False),
                     ("call_tool", "set_entry", True), ("call_tool", "get_entry", True),
                     ("call_tool", "list_keys", False), ("execute_python_code", None, False)]
