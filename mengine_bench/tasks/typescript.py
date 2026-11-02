"""TypeScript: the hook bus of a harness plugin runs tool.after hooks out of order and loses some (#124).

The agent edits a small OpenCode-style hook bus. Node 24 strips erasable TypeScript natively, so the gold copies the
sources next to hidden `node --test` files the agent never saw, one file per case: an unhandled rejection in one case
cannot fail another. Any sequential design that keeps the public API passes.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import CheckResult, EvalTask, Step, checkpoints, read, saw, scratch_root, write

PACKAGE_JSON = """{
  "name": "harness-hooks",
  "version": "0.3.0",
  "private": true,
  "type": "module",
  "scripts": {
    "test": "node --test"
  }
}
"""

README = """# harness-hooks

The hook bus our harness plugins use (OpenCode-style hooks such as `tool.before` and `tool.after`).
Plain TypeScript run by Node 24 directly (`npm test` runs `node --test`); no dependencies.

## How the bus behaves

- `bus.on(event, handler)` subscribes a handler and returns a function that unsubscribes it.
- `await bus.emit(event, payload)` runs the handlers of that event one after another, in the order they
  subscribed: each handler finishes (its promise settles) before the next one starts.
- `emit` resolves only after every handler has finished.
- When a handler throws or rejects, `emit` rejects with that same error and the handlers after it do not run.
- `emit` runs the handlers that were subscribed when it started. A handler that unsubscribes itself (or another
  handler) during an emit does not stop the others in that emit; the change counts from the next emit on.

## Plugins

`src/plugin.ts` is the audit plugin: on `tool.after` it shows a one-time notice, redacts passwords from the tool
output, then appends the result to the audit log.
"""

BUS = """/**
 * Hook bus for harness plugins (OpenCode-style hooks). The README states the contract:
 * handlers run one after another in subscription order, emit resolves after all of them,
 * a handler error rejects emit, and unsubscribing during an emit does not stop the others.
 */

export type Handler<T> = (payload: T) => void | Promise<void>;

export class HookBus {
  private handlers: Map<string, Handler<unknown>[]> = new Map();

  /** Subscribes a handler to an event; returns the function that unsubscribes it. */
  on<T>(event: string, handler: Handler<T>): () => void {
    const list = this.handlers.get(event) ?? [];
    list.push(handler as Handler<unknown>);
    this.handlers.set(event, list);
    return () => {
      const index = list.indexOf(handler as Handler<unknown>);
      if (index >= 0) {
        list.splice(index, 1);
      }
    };
  }

  /** Runs the handlers of an event with the payload. */
  async emit<T>(event: string, payload: T): Promise<void> {
    const list = this.handlers.get(event) ?? [];
    list.forEach(async (handler) => {
      await handler(payload);
    });
  }

  /** How many handlers an event has. */
  count(event: string): number {
    return (this.handlers.get(event) ?? []).length;
  }
}
"""

PLUGIN = """import type { HookBus } from "./bus.ts";

export type ToolResult = { tool: string; output: string };

const PASSWORD = /password=\\S+/g;

/** The redaction rules load asynchronously in production (from the workspace settings). */
async function loadRules(): Promise<RegExp> {
  await new Promise((resolve) => setTimeout(resolve, 5));
  return PASSWORD;
}

/** Audit plugin: a one-time notice, then redaction, then the audit log, in that order on every tool.after. */
export function registerAuditPlugin(bus: HookBus, audit: string[]): void {
  const stopNotice = bus.on<ToolResult>("tool.after", () => {
    stopNotice();
    audit.push("notice: tool output is audited");
  });
  bus.on<ToolResult>("tool.after", async (result) => {
    const rule = await loadRules();
    result.output = result.output.replace(rule, "password=[redacted]");
  });
  bus.on<ToolResult>("tool.after", (result) => {
    audit.push(`${result.tool}: ${result.output}`);
  });
}
"""

VISIBLE = """import { test } from "node:test";
import assert from "node:assert/strict";
import { HookBus } from "../src/bus.ts";

test("emit calls a subscribed handler with the payload", async () => {
  const bus = new HookBus();
  const seen: string[] = [];
  bus.on<string>("tool.after", (payload) => {
    seen.push(payload);
  });
  await bus.emit("tool.after", "read");
  assert.deepEqual(seen, ["read"]);
});

test("unsubscribe removes the handler", async () => {
  const bus = new HookBus();
  const off = bus.on("tool.after", () => {});
  assert.equal(bus.count("tool.after"), 1);
  off();
  assert.equal(bus.count("tool.after"), 0);
});
"""

HIDDEN_HEADER = """import { test } from "node:test";
import assert from "node:assert/strict";
import { HookBus } from "../src/bus.ts";

const pause = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
"""

# Case name -> body of its own hidden file. Each runs alone so one case's stray rejection cannot fail another (#124).
HIDDEN_CASES: dict[str, str] = {
    "handlers run in subscription order": """
test("handlers run in subscription order", { timeout: 5000 }, async () => {
  const bus = new HookBus();
  const seen: string[] = [];
  bus.on("tool.after", async () => { seen.push("a start"); await pause(30); seen.push("a end"); });
  bus.on("tool.after", async () => { seen.push("b start"); await pause(1); seen.push("b end"); });
  bus.on("tool.after", () => { seen.push("c"); });
  await bus.emit("tool.after", {});
  await pause(50);
  assert.deepEqual(seen, ["a start", "a end", "b start", "b end", "c"]);
});
""",
    "emit resolves after every handler": """
test("emit resolves after every handler", { timeout: 5000 }, async () => {
  const bus = new HookBus();
  const done: number[] = [];
  bus.on("tool.after", async () => { await pause(20); done.push(1); });
  bus.on("tool.after", async () => { await pause(10); done.push(2); });
  await bus.emit("tool.after", {});
  assert.equal(done.length, 2, `emit resolved with ${done.length} of 2 handlers finished`);
});
""",
    "a failing handler rejects emit": """
test("a failing handler rejects emit", { timeout: 5000 }, async () => {
  const bus = new HookBus();
  const boom = new Error("boom");
  bus.on("tool.after", async () => { await pause(5); throw boom; });
  let caught: unknown = undefined;
  try {
    await bus.emit("tool.after", {});
  } catch (error) {
    caught = error;
  }
  const wrapped = caught as { cause?: unknown; errors?: unknown[] } | undefined;
  assert.ok(caught === boom || wrapped?.cause === boom || (wrapped?.errors ?? []).includes(boom),
            `expected emit to reject with the handler error, got ${String(caught)}`);
});
""",
    "a handler that unsubscribes itself does not stop the others": """
test("a handler that unsubscribes itself does not stop the others", { timeout: 5000 }, async () => {
  const bus = new HookBus();
  const seen: string[] = [];
  const off = bus.on("tool.after", () => { off(); seen.push("once"); });
  bus.on("tool.after", () => { seen.push("b"); });
  bus.on("tool.after", () => { seen.push("c"); });
  await bus.emit("tool.after", {});
  await bus.emit("tool.after", {});
  assert.deepEqual(seen, ["once", "b", "c", "b", "c"]);
});
""",
    "the audit plugin redacts before it logs": """
import { registerAuditPlugin } from "../src/plugin.ts";

test("the audit plugin redacts before it logs", { timeout: 5000 }, async () => {
  const bus = new HookBus();
  const audit: string[] = [];
  registerAuditPlugin(bus, audit);
  await bus.emit("tool.after", { tool: "bash", output: "login password=hunter2 ok" });
  await bus.emit("tool.after", { tool: "read", output: "password=swordfish" });
  assert.deepEqual(audit, ["notice: tool output is audited", "bash: login password=[redacted] ok",
                           "read: password=[redacted]"]);
});
""",
}

TS_FILES = {"package.json": PACKAGE_JSON, "README.md": README, "src/bus.ts": BUS, "src/plugin.ts": PLUGIN,
            "test/bus.test.ts": VISIBLE}
NODE_LIMIT_S = 120
DEPENDENCY_KEYS = ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies", "bundledDependencies",
                   "bundleDependencies")


def _sha(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def _hidden_file(name: str) -> str:
    return "hidden_" + re.sub(r"\W+", "_", name).strip("_") + ".test.ts"


def _ts_setup(ws: Path) -> None:
    for rel, text in TS_FILES.items():
        write(ws, rel, text)


def run_node_hidden(ws: Path) -> tuple[dict[str, bool], dict[str, str], str]:
    """Each hidden case's result in a copy of src/, and why the run failed when it did.

    Only src/ is copied, with the gold's own package.json: the agent's tests and settings do not count. A case passes
    when its test is `ok` and its file did not fail afterwards (an unhandled rejection fails the file, not the test).
    """
    node = shutil.which("node")
    if node is None:
        return {}, {}, "node not found; expected Node.js 24 (or 22.18+) on PATH"
    with tempfile.TemporaryDirectory(prefix="bench-node-", dir=scratch_root(), ignore_cleanup_errors=True) as tmp:
        root = Path(tmp)
        shutil.copytree(ws / "src", root / "src")
        write(root, "package.json", '{"type": "module"}\n')
        files = []
        for name, body in HIDDEN_CASES.items():
            files.append(f"test/{_hidden_file(name)}")
            write(root, files[-1], HIDDEN_HEADER + body)
        try:
            done = subprocess.run([node, "--test", "--test-reporter=tap", *files], cwd=root, capture_output=True,
                                  text=True, encoding="utf-8", errors="replace", timeout=NODE_LIMIT_S, check=False)
        except subprocess.TimeoutExpired:
            return {}, {}, f"node --test exceeded {NODE_LIMIT_S}s"
    points = re.findall(r"^\s*(ok|not ok) \d+ - (.+?)\s*(?:#.*)?$", done.stdout, re.MULTILINE)
    failed_files = {label.replace("\\\\", "/").replace("\\", "/").rsplit("/", 1)[-1] for verdict, label in points
                    if verdict == "not ok" and label.endswith(".test.ts")}
    passed = {name: (verdict == "ok" and _hidden_file(name) not in failed_files) for verdict, name in points
              if name in HIDDEN_CASES}
    why = {name: _tap_failure(done.stdout, name) for name in HIDDEN_CASES if not passed.get(name)}
    errors = [line.strip("# ").strip() for line in done.stdout.splitlines() if re.search(r"Error\b", line)]
    return passed, why, " | ".join(errors[:3]) or (done.stdout + done.stderr)[-200:]


def _tap_failure(tap: str, name: str) -> str:
    """The assertion a failed hidden case reports, as actual vs expected when TAP gives both (#82)."""
    found = re.search(r"^not ok \d+ - " + re.escape(name) + r"\n(.*?)^  \.\.\.$", tap, re.MULTILINE | re.DOTALL)
    if found is None:
        return f"{name}: its file failed after the test (a stray rejection) or never loaded; expected `ok - {name}`"
    block = found.group(1)
    sides = {key: re.findall(r"^    \d+: (.*)$", part, re.MULTILINE)
             for key, part in re.findall(r"^  (actual|expected):\n((?:    .*\n?)*)", block, re.MULTILINE)}
    if sides.get("actual") is not None and sides.get("expected") is not None:
        return saw(" ".join(sides["actual"]), " ".join(sides["expected"]))
    message = re.search(r"^  error: (?:\|-\n)?\s*(.+)$", block, re.MULTILINE)
    return f"{name}: {message.group(1).strip() if message else 'failed'}"


def _no_new_dependencies(ws: Path) -> bool:
    text = read(ws, "package.json")
    if text is None:
        return True
    try:
        manifest = json.loads(text)
    except json.JSONDecodeError:
        return False
    return isinstance(manifest, dict) and not any(manifest.get(key) for key in DEPENDENCY_KEYS)


def _ts_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    untouched = _sha(read(ws, "test/bus.test.ts") or "") == _sha(VISIBLE)
    result.mandatory.append(("visible tests left untouched", untouched))
    result.mandatory.append(("package.json takes no dependencies", _no_new_dependencies(ws)))
    passed, why, run_error = run_node_hidden(ws) if (ws / "src").is_dir() else ({}, {}, "src/ is gone")
    for name in HIDDEN_CASES:
        result.add(f"hidden {name}", passed.get(name, False), why.get(name, "") if passed else run_error)
    return result


FIXED_EMIT = """  async emit<T>(event: string, payload: T): Promise<void> {
    // A copy, so a handler that unsubscribes during the emit cannot shift the ones after it.
    const list = [...(this.handlers.get(event) ?? [])];
    for (const handler of list) {
      await handler(payload);
    }
  }
"""
PLANTED_EMIT = """  async emit<T>(event: string, payload: T): Promise<void> {
    const list = this.handlers.get(event) ?? [];
    list.forEach(async (handler) => {
      await handler(payload);
    });
  }
"""


def _ts_reference(ws: Path) -> list[str]:
    write(ws, "src/bus.ts", BUS.replace(PLANTED_EMIT, FIXED_EMIT))
    return ["emit now awaits each handler in order over a copy of the list"]


TASKS = [
    EvalTask(
        id="ts-plugin-bug", category="engineering",
        provenance="Real TypeScript harness plugin work: an OpenCode-style hook bus; hidden node --test cases, any "
                   "sequential design passes",
        summary="Fix a TypeScript plugin hook bus that runs hooks out of order, skips some and hides failures.",
        setup=_ts_setup, check=_ts_check, reference=_ts_reference, timeout_s=180,
        checkpoints=checkpoints(("read the bus", r"bus\.ts"), ("ran the tests", r"node\s+(--\S+\s+)*--test|npm\s+(run\s+)?test")),
        steps=(Step("Users of our harness plugins report that tool.after hooks run out of order, that sometimes a hook "
                    "never runs, and that a failing hook is silently ignored. The hook bus and the plugin are in {WS}; "
                    "the README there says how the bus must behave. Fix the bus. Its public API stays as it is, the "
                    "tests in {WS}/test stay as they are, and package.json takes no dependencies."),),
    ),
]
