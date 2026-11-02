"""#124: the TypeScript hook bus eval fails wrong fixes, accepts every valid design and reads only the delivered files."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.core import write
from mengine_bench.tasks import typescript
from mengine_bench.tasks.typescript import BUS, FIXED_EMIT, PACKAGE_JSON, PLANTED_EMIT

SET_BUS = """export type Handler<T> = (payload: T) => void | Promise<void>;

export class HookBus {
  private handlers: Map<string, Set<Handler<unknown>>> = new Map();

  on<T>(event: string, handler: Handler<T>): () => void {
    const set = this.handlers.get(event) ?? new Set<Handler<unknown>>();
    set.add(handler as Handler<unknown>);
    this.handlers.set(event, set);
    return () => { set.delete(handler as Handler<unknown>); };
  }

  async emit<T>(event: string, payload: T): Promise<void> {
    for (const handler of Array.from(this.handlers.get(event) ?? [])) {
      await handler(payload);
    }
  }

  count(event: string): number {
    return this.handlers.get(event)?.size ?? 0;
  }
}
"""

REDUCE_EMIT = """  async emit<T>(event: string, payload: T): Promise<void> {
    const list = (this.handlers.get(event) ?? []).slice();
    await list.reduce<Promise<void>>((chain, handler) => chain.then(() => handler(payload)), Promise.resolve());
  }
"""


def _task() -> object:
    return next(task for task in catalog.all_tasks() if task.id == "ts-plugin-bug")


def _with_emit(ws: Path, emit: str) -> Path:
    typescript._ts_setup(ws)
    write(ws, "src/bus.ts", BUS.replace(PLANTED_EMIT, emit))
    return ws


def test_the_reference_passes_and_the_untouched_folder_fails(tmp_path: Path) -> None:
    task = _task()
    (tmp_path / "bare").mkdir()
    (tmp_path / "solved").mkdir()
    task.setup(tmp_path / "bare")
    assert not task.check(tmp_path / "bare", [""]).passed
    task.setup(tmp_path / "solved")
    result = task.check(tmp_path / "solved", task.reference(tmp_path / "solved"))
    assert result.passed, (result.failed(), result.details)


@pytest.mark.parametrize("variant", ["set", "reduce"])
def test_other_valid_designs_pass(tmp_path: Path, variant: str) -> None:
    typescript._ts_setup(tmp_path)
    if variant == "set":
        write(tmp_path, "src/bus.ts", SET_BUS)
    else:
        _with_emit(tmp_path, REDUCE_EMIT)
    result = typescript._ts_check(tmp_path, [""])
    assert result.passed, (result.failed(), result.details)


@pytest.mark.parametrize(("emit", "check"), [
    ("""  async emit<T>(event: string, payload: T): Promise<void> {
    await Promise.all([...(this.handlers.get(event) ?? [])].map((handler) => handler(payload)));
  }
""", "hidden handlers run in subscription order"),
    ("""  async emit<T>(event: string, payload: T): Promise<void> {
    let chain: Promise<void> = Promise.resolve();
    for (const handler of [...(this.handlers.get(event) ?? [])]) {
      chain = chain.then(() => handler(payload));
    }
    chain.catch(() => {});
  }
""", "hidden emit resolves after every handler"),
    ("""  async emit<T>(event: string, payload: T): Promise<void> {
    for (const handler of [...(this.handlers.get(event) ?? [])]) {
      try { await handler(payload); } catch { /* keep going */ }
    }
  }
""", "hidden a failing handler rejects emit"),
    ("""  async emit<T>(event: string, payload: T): Promise<void> {
    const list = this.handlers.get(event) ?? [];
    for (let index = 0; index < list.length; index++) {
      await list[index](payload);
    }
  }
""", "hidden a handler that unsubscribes itself does not stop the others"),
])
def test_each_wrong_fix_fails_its_own_check(tmp_path: Path, emit: str, check: str) -> None:
    result = typescript._ts_check(_with_emit(tmp_path, emit), [""])
    assert check in result.failed()
    assert result.details[check]


def test_a_failing_case_reports_actual_and_expected(tmp_path: Path) -> None:
    typescript._ts_setup(tmp_path)
    details = typescript._ts_check(tmp_path, [""]).details
    assert "'a start' 'a end' 'b start'" in details["hidden handlers run in subscription order"]


def test_editing_the_visible_tests_earns_nothing(tmp_path: Path) -> None:
    ws = _with_emit(tmp_path, FIXED_EMIT)
    write(ws, "test/bus.test.ts", "")
    result = typescript._ts_check(ws, [""])
    assert not result.mandatory_ok and result.score == 0


def test_a_new_dependency_earns_nothing(tmp_path: Path) -> None:
    ws = _with_emit(tmp_path, FIXED_EMIT)
    manifest = json.loads(PACKAGE_JSON)
    write(ws, "package.json", json.dumps({**manifest, "dependencies": {"p-series": "^3.0.0"}}))
    assert not typescript._ts_check(ws, [""]).mandatory_ok


def test_without_node_every_case_fails_and_says_so(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ws = _with_emit(tmp_path, FIXED_EMIT)
    monkeypatch.setattr(typescript.shutil, "which", lambda name: None)
    result = typescript._ts_check(ws, [""])
    assert result.score == 0
    assert all("node not found" in result.details[f"hidden {name}"] for name in typescript.HIDDEN_CASES)


def test_the_brief_does_not_hand_over_the_cause() -> None:
    prompt = _task().steps[0].prompt.lower()
    for word in ("foreach", "concurren", "parallel", "splice", "await", "copy", "promise", "sequential"):
        assert word not in prompt, word


def test_a_fix_only_in_the_chat_earns_nothing(tmp_path: Path) -> None:
    typescript._ts_setup(tmp_path)
    assert typescript._ts_check(tmp_path, [BUS.replace(PLANTED_EMIT, FIXED_EMIT)]).score == 0
