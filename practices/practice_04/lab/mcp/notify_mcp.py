"""Minimal stdio MCP server: tool subscribe_name for Notify Mini.

Protocol subset sufficient for OpenCode local MCP and --self-check demos.
Dependencies: Python 3.10+ standard library only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from service import subscribe, subscribers  # noqa: E402


SERVER_INFO = {"name": "notify-mcp", "version": "1.0.0"}
TOOLS = [
    {
        "name": "subscribe_name",
        "description": "Subscribe a person name in Notify Mini. Rejects empty names.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Subscriber name"}
            },
            "required": ["name"],
        },
    }
]


def tool_subscribe_name(arguments: dict) -> dict:
    if "name" not in arguments:
        return {"ok": False, "error": "missing required field: name"}
    name = arguments["name"]
    if not isinstance(name, str):
        return {"ok": False, "error": "name must be a string"}
    try:
        result = subscribe(name)
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}
    return {
        "ok": True,
        "result": result,
        "subscribers": sorted(subscribers),
    }


def handle(msg: dict) -> dict | None:
    mid = msg.get("id")
    method = msg.get("method")
    params = msg.get("params") or {}

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": mid,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            },
        }
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        if name != "subscribe_name":
            return {
                "jsonrpc": "2.0",
                "id": mid,
                "error": {"code": -32601, "message": f"Unknown tool: {name}"},
            }
        payload = tool_subscribe_name(args)
        return {
            "jsonrpc": "2.0",
            "id": mid,
            "result": {
                "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}],
                "isError": not payload.get("ok", False),
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    return {
        "jsonrpc": "2.0",
        "id": mid,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def self_check() -> int:
    subscribers.clear()
    ok = tool_subscribe_name({"name": "Ann"})
    bad = tool_subscribe_name({"name": "   "})
    missing = tool_subscribe_name({})
    print("SUCCESS:", json.dumps(ok, ensure_ascii=False))
    print("ERROR_EMPTY:", json.dumps(bad, ensure_ascii=False))
    print("ERROR_MISSING:", json.dumps(missing, ensure_ascii=False))
    assert ok["ok"] is True
    assert bad["ok"] is False and bad["error"] == "empty name"
    assert missing["ok"] is False
    print("self-check: OK")
    return 0


def serve() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        msg = json.loads(line)
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    if "--self-check" in sys.argv:
        raise SystemExit(self_check())
    serve()
