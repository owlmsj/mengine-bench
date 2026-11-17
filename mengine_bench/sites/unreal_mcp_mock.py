"""A mock of the owner's live `unreal-mcp` server (UE 5.8 editor + Epic toolsets + VibeUE) for track U of mengine-qlora #22.

Transport: MCP streamable HTTP as the live editor speaks it on :8000 - POST `/mcp` with one JSON-RPC message,
a plain `application/json` reply, `Mcp-Session-Id` set on `initialize`; GET `/mcp` answers 405 (the live
readiness probe). Any query string is ignored (an OpenCode remote server may get `?codemode=false`).

Surface, copied from a live dump on 2026-11-17 (`unreal_mcp_data/`): `initialize`, the 11 root tools of
`tools/list` with their exact input schemas, `list_toolsets` (the real markdown of 88 toolsets) and
`describe_toolset` (the real reply per toolset, and the real not-found text). `call_tool` validates required
arguments against the real schema with the live error text, then runs the typed tools of
`unreal_mcp_tools` over the task's fake world; any other tool of a real toolset answers the live error for a
bad call (a parameter error for a reference the world lacks, else "Unknown tool"). The Python root tools
refuse: `execute_python_code` is disabled here, so a trajectory learns the typed path.

World: the task's `setup` writes `site-data/ue-world.json`; the server reads it once as the signed seed and
removes it. Every `tools/call` is one signed journal event, so the grader sees the final world and every call
made, refused ones included (see `mengine_bench.sites.signed_store`).

Stdlib only; run with `python -m mengine_bench.sites.unreal_mcp_mock`.
"""

from __future__ import annotations

import copy
import gzip
import json
import threading
import uuid
from functools import cache
from pathlib import Path
from urllib.parse import urlsplit

from mengine_bench.sites.server_base import SiteHandler, serve
from mengine_bench.sites.signed_store import DATA_DIR, SiteEvent, SiteState
from mengine_bench.sites.unreal_mcp_tools import UE_TOOLS, UeToolError, ue_empty_world, ue_run_tool

UE_MCP_PATH = "/mcp"
UE_SEED_FILE = "ue-world.json"
UE_DATA_DIR = Path(__file__).resolve().parent / "unreal_mcp_data"
UE_SESSION_HEADER = "Mcp-Session-Id"
UE_PYTHON_REFUSAL = ("{tool} is disabled in this environment. Use the typed editor tools instead: list_toolsets, "
                     "describe_toolset, then call_tool.")
UE_ROOT_REFUSALS = {
    "execute_python_code": UE_PYTHON_REFUSAL, "discover_python_module": UE_PYTHON_REFUSAL,
    "discover_python_class": UE_PYTHON_REFUSAL, "discover_python_function": UE_PYTHON_REFUSAL,
    "list_python_subsystems": UE_PYTHON_REFUSAL,
    "capture_image": "capture_image is unavailable in this environment: the editor has no visible viewport.",
    "deep_research": "deep_research is unavailable in this environment: there is no web access.",
    "terrain_data": "terrain_data is unavailable in this environment: there is no VibeUE API key.",
}
UE_LOCK = threading.Lock()


@cache
def ue_root() -> dict[str, object]:
    """{"initialize": result, "tools": [the 11 root tools]} as the live server answered them."""
    return json.loads((UE_DATA_DIR / "root_tools.json").read_text(encoding="utf-8"))


@cache
def ue_toolset_listing() -> str:
    return (UE_DATA_DIR / "list_toolsets.md").read_text(encoding="utf-8")


@cache
def ue_toolsets() -> dict[str, str]:
    """Toolset name -> the live describe_toolset text, in the live server's order."""
    return json.loads(gzip.decompress((UE_DATA_DIR / "describe_toolset.json.gz").read_bytes()))


@cache
def ue_tool_schemas(toolset: str) -> dict[str, dict]:
    """Short tool name -> input schema, key order as the live server prints it in its errors."""
    described = json.loads(ue_toolsets()[toolset])
    return {tool["name"].rsplit(".", 1)[-1]: tool["inputSchema"] for tool in described["tools"]}


def _compact(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def ue_missing_arguments(name: str, schema: dict, args: dict) -> str | None:
    """The live validator's text for absent required arguments (2026-11-17 samples), or None."""
    required = [key for key in schema.get("required", []) if key not in args]
    if not required:
        return None
    if not args:
        return (f'Function "{name}", input params are required by the function input schema Json, but incoming '
                f"function input params Json is empty.\nFunction schema Json -\n{_compact(schema)}")
    return (f'Function "{name}", input param "{required[0]}" is required by the function input schema Json, but is '
            f"missing from the incoming function input params Json.\nFunction schema Json -\n{_compact(schema)}\n"
            f"Function input params Json -\n{_compact(args)}")


def ue_unimplemented(world: SiteState, name: str, schema: dict, args: dict) -> str:
    """A real tool this mock does not run: the live text for a missing referenced object, else for a bad name."""
    for prop, spec in schema.get("properties", {}).items():
        title = str(spec.get("title", ""))
        if prop in args and title.startswith("/Script/") and "refPath" in spec.get("properties", {}):
            ref = args[prop].get("refPath", "") if isinstance(args[prop], dict) else args[prop]
            return f"Parameter error: {ref} is not valid {title.rsplit('.', 1)[-1]} for property '{prop}'."
    return f"Unknown tool {name}"


def _reply(value: object) -> str:
    return _compact({"returnValue": value})


def ue_inner_arguments(args: dict) -> object:
    """call_tool's `arguments`: an object, or JSON text of one (not sampled live: a model that sends the object as
    text still gets through); text that is not JSON comes back unchanged."""
    arguments = args.get("arguments") or {}
    if isinstance(arguments, str):
        try:
            return json.loads(arguments)
        except ValueError:
            return arguments
    return arguments


def ue_call_tool(world: SiteState, args: dict) -> tuple[SiteState, str, bool]:
    """(world after, reply text, is error) for one call_tool."""
    toolset, name = str(args.get("toolset_name") or ""), str(args.get("tool_name") or "")
    arguments = ue_inner_arguments(args)
    if isinstance(arguments, str):
        return world, f"arguments is not valid JSON: {arguments[:200]}", True
    if not isinstance(arguments, dict):
        return world, f"arguments must be a JSON object, got {type(arguments).__name__}", True
    if not toolset:
        if name in {tool["name"] for tool in ue_root()["tools"]} and name != "call_tool":  # type: ignore[union-attr]
            return ue_root_tool(world, name, arguments)
        return world, f"Tool '{name}' not found", True  # live 2026-11-17, dotted and bare names alike
    if toolset not in ue_toolsets():
        return world, f"Toolset '{toolset}' not found", True
    schema = ue_tool_schemas(toolset).get(name)
    if schema is None:
        return world, f"Unknown tool {name}", True
    missing = ue_missing_arguments(name, schema, arguments)
    if missing:
        return world, missing, True
    if (toolset, name) not in UE_TOOLS:
        return world, ue_unimplemented(world, name, schema, arguments), True
    try:
        after, value = ue_run_tool(world, toolset, name, arguments)
    except UeToolError as error:
        return world, str(error), True
    return after, _reply(value), False


def ue_root_tool(world: SiteState, name: str, args: dict) -> tuple[SiteState, str, bool]:
    if name == "call_tool":
        return ue_call_tool(world, args)
    if name == "list_toolsets":
        return world, ue_toolset_listing(), False
    if name == "describe_toolset":
        wanted = str(args.get("toolset_name") or "")
        if wanted in ue_toolsets():
            return world, ue_toolsets()[wanted], False
        return world, f"Toolset '{wanted}' not found. Available toolsets: {', '.join(ue_toolsets())}", True
    return world, UE_ROOT_REFUSALS[name].format(tool=name), True


def apply_unreal_mcp(state: SiteState, event: SiteEvent) -> SiteState:
    """Replay one call: a successful typed mutation changes the world, anything else leaves it as it was."""
    if event.get("type") != "call" or not event.get("ok") or event.get("tool") != "call_tool":
        return state
    key = (str(event.get("toolset")), str(event.get("name")))
    if key not in UE_TOOLS or not UE_TOOLS[key].mutates:
        return state
    return ue_run_tool(state, key[0], key[1], dict(event.get("arguments") or {}))[0]  # type: ignore[call-overload]


def ue_seed(workspace: Path) -> SiteState:
    """The task's world from `site-data/ue-world.json`, read once and removed; an empty world without one."""
    seed_file = workspace / DATA_DIR / UE_SEED_FILE
    world = ue_empty_world()
    if seed_file.is_file():
        world.update(json.loads(seed_file.read_text(encoding="utf-8")))
        seed_file.unlink()
    return world


class UnrealMcpHandler(SiteHandler):
    """POST /mcp JSON-RPC; GET /mcp 405 like the live editor; everything else 404."""

    def _mcp_path(self) -> bool:
        return urlsplit(self.path).path.rstrip("/") == UE_MCP_PATH

    def send_rpc(self, status: int, payload: object | None, session: str | None = None) -> None:
        body = b"" if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        if payload is not None:
            self.send_header("Content-Type", "application/json")
        if session:
            self.send_header(UE_SESSION_HEADER, session)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler's name
        if self._mcp_path():
            self.send_response(405)
            self.send_header("Allow", "POST")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        self.send_json(404, {"error": "not_found", "message": f"received GET {urlsplit(self.path).path}; expected POST /mcp"})

    def do_DELETE(self) -> None:  # noqa: N802 - a client closing its session
        self.send_rpc(200 if self._mcp_path() else 404, None)

    def do_POST(self) -> None:  # noqa: N802
        if not self._mcp_path():
            self.send_json(404, {"error": "not_found", "message": f"received POST {urlsplit(self.path).path}; expected /mcp"})
            return
        try:
            message = json.loads(self.read_body() or b"null")
        except ValueError as error:
            self.send_rpc(400, {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Parse error: {error}"}})
            return
        if not isinstance(message, dict) or not isinstance(message.get("method"), str):
            self.send_rpc(400, {"jsonrpc": "2.0", "id": None,
                                "error": {"code": -32600, "message": f"Invalid Request: received {str(message)[:120]}; "
                                                                    "expected one JSON-RPC object with a method"}})
            return
        self.answer(message)

    def answer(self, message: dict) -> None:
        method, ident = message["method"], message.get("id")
        params = message.get("params") if isinstance(message.get("params"), dict) else {}
        if "id" not in message:  # a notification (notifications/initialized, cancelled, ...)
            self.send_rpc(202, None)
            return
        if method == "initialize":
            self.send_rpc(200, {"jsonrpc": "2.0", "id": ident, "result": ue_root()["initialize"]}, uuid.uuid4().hex)
            return
        results = {"ping": {}, "tools/list": {"tools": ue_root()["tools"]}, "resources/list": {"resources": []},
                   "resources/templates/list": {"resourceTemplates": []}}
        if method in results:
            self.send_rpc(200, {"jsonrpc": "2.0", "id": ident, "result": results[method]})
            return
        if method != "tools/call":
            self.send_rpc(200, {"jsonrpc": "2.0", "id": ident, "error": {"code": -32601, "message": f"Method not found: {method}"}})
            return
        name, args = str(params.get("name") or ""), params.get("arguments") or {}
        if name not in {tool["name"] for tool in ue_root()["tools"]}:  # type: ignore[union-attr]
            # Live 2026-11-17: HTTP 400 with {"code": -32602, "message": "Unknown tool: not_a_root_tool"}.
            self.send_rpc(400, {"jsonrpc": "2.0", "id": ident, "error": {"code": -32602, "message": f"Unknown tool: {name}"}})
            return
        self.send_rpc(200, {"jsonrpc": "2.0", "id": ident, "result": self.call(name, args if isinstance(args, dict) else {})})

    def call(self, name: str, args: dict) -> dict[str, object]:
        with UE_LOCK:
            world = copy.deepcopy(self.store.state)
            _, text, failed = ue_root_tool(world, name, args)
            event: SiteEvent = {"type": "call", "tool": name, "arguments": args, "ok": not failed}
            if name == "call_tool":
                event.update(toolset=args.get("toolset_name") or None, name=args.get("tool_name"),
                             arguments=ue_inner_arguments(args))
            self.store.record(event)
        result: dict[str, object] = {"content": [{"type": "text", "text": text}]}
        if failed:
            result["isError"] = True
        return result


if __name__ == "__main__":
    serve(UnrealMcpHandler, apply_unreal_mcp, ue_seed)
