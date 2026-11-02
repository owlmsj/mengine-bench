"""#124: cfg-source-drift passes a fix in the source, however out/ is rebuilt, and fails a patched copy."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.core import read, write
from mengine_bench.tasks import configgen
from mengine_bench.tasks.configgen import CFG_GEN, CFG_SOURCE, _cfg_check, _cfg_reference, _cfg_setup

OLD_FAST = '"name": "fast-coder", "context_window": 131072'
NEW_FAST = '"name": "fast-coder", "context_window": 262144'
REGENERATED = "regenerating gives fast-coder 262144 in all three configs"
DELIVERED = "the delivered configs equal what the source generates"
UNCHANGED = "the other models and fields are unchanged"


def _task() -> configgen.EvalTask:
    return next(task for task in catalog.all_tasks() if task.id == "cfg-source-drift")


def _fresh(tmp_path: Path) -> Path:
    _cfg_setup(tmp_path)
    return tmp_path


def _regenerate(ws: Path, source: str) -> None:
    write(ws, "models.json", source)
    for rel, text in configgen._cfg_generate(source).items():
        write(ws, rel, text)


def test_the_fixture_has_the_drift(tmp_path: Path) -> None:
    ws = _fresh(tmp_path)
    contexts = configgen._cfg_fast_coder_contexts({rel: read(ws, rel) or "" for rel in configgen.CFG_OUTPUTS})
    assert contexts == {"opencode": 262144, "codex": 131072, "claude": 131072}
    assert "generated" in (read(ws, "README.md") or "")


def test_the_reference_passes_and_the_untouched_folder_fails(tmp_path: Path) -> None:
    (tmp_path / "bare").mkdir()
    (tmp_path / "solved").mkdir()
    task = _task()
    task.setup(tmp_path / "bare")
    assert not task.check(tmp_path / "bare", [""]).passed
    task.setup(tmp_path / "solved")
    result = task.check(tmp_path / "solved", task.reference(tmp_path / "solved"))
    assert result.passed, (result.failed(), result.details)


def test_the_source_fixed_and_the_copies_patched_by_hand_passes(tmp_path: Path) -> None:
    ws = _fresh(tmp_path)
    write(ws, "models.json", CFG_SOURCE.replace(OLD_FAST, NEW_FAST))
    codex = (read(ws, "out/codex.toml") or "").replace("context_window = 131072", "context_window = 262144", 1)
    write(ws, "out/codex.toml", codex)
    claude = json.loads(read(ws, "out/claude.json") or "")
    claude["models"][0]["contextWindow"] = 262144
    # A different layout is still the same config.
    (ws / "out/claude.json").write_text(json.dumps(claude), encoding="utf-8", newline="\r\n")
    result = _cfg_check(ws, [""])
    assert result.passed, (result.failed(), result.details)


def test_a_source_reformatted_with_other_spacing_passes(tmp_path: Path) -> None:
    ws = _fresh(tmp_path)
    models = json.loads(CFG_SOURCE)
    models["models"][0]["context_window"] = 262144
    _regenerate(ws, json.dumps(models, indent=4))
    assert _cfg_check(ws, [""]).passed


def test_patching_only_the_copies_fails_the_regeneration(tmp_path: Path) -> None:
    ws = _fresh(tmp_path)
    for rel, old, new in (("out/codex.toml", "context_window = 131072", "context_window = 262144"),
                          ("out/claude.json", '"contextWindow": 131072', '"contextWindow": 262144')):
        write(ws, rel, (read(ws, rel) or "").replace(old, new, 1))
    failed = _cfg_check(ws, [""]).failed()
    assert REGENERATED in failed and UNCHANGED not in failed


def test_a_fixed_source_left_unregenerated_fails_the_delivery(tmp_path: Path) -> None:
    ws = _fresh(tmp_path)
    write(ws, "models.json", CFG_SOURCE.replace(OLD_FAST, NEW_FAST))
    failed = _cfg_check(ws, [""]).failed()
    assert failed == [DELIVERED]


@pytest.mark.parametrize(("source", "check"), [
    (CFG_SOURCE.replace(OLD_FAST, '"name": "fast-coder", "context_window": 200000'), REGENERATED),
    (CFG_SOURCE.replace(OLD_FAST, NEW_FAST).replace('"context_window": 32768', '"context_window": 65536'), UNCHANGED),
    (CFG_SOURCE.replace(OLD_FAST, NEW_FAST).replace('"max_output": 16384', '"max_output": 32768'), UNCHANGED),
    (CFG_SOURCE.replace(OLD_FAST, NEW_FAST).replace(
        '    {"name": "tiny-chat", "context_window": 32768, "max_output": 4096, "tool_calling": false}\n', "").replace(
        '"tool_calling": true},\n  ]', '"tool_calling": true}\n  ]'), UNCHANGED),
])
def test_each_check_fails_its_own_wrong_answer(tmp_path: Path, source: str, check: str) -> None:
    ws = _fresh(tmp_path)
    _regenerate(ws, source)
    assert check in _cfg_check(ws, [""]).failed()


def test_editing_the_generator_fails_the_gate(tmp_path: Path) -> None:
    ws = _fresh(tmp_path)
    _cfg_reference(ws)
    write(ws, "gen.py", CFG_GEN.replace('"context": model["context_window"]', '"context": 262144'))
    result = _cfg_check(ws, [""])
    assert not result.mandatory_ok and result.score == 0.0


def test_the_brief_does_not_hand_over_the_cause() -> None:
    prompt = _task().steps[0].prompt.lower()
    for word in ("models.json", "gen.py", "generat", "source of truth", "out/", "hand-edit", "hand edit"):
        assert word not in prompt, word


def test_a_correct_answer_in_the_chat_alone_earns_nothing(tmp_path: Path) -> None:
    ws = _fresh(tmp_path)
    assert not _cfg_check(ws, ["I set fast-coder to 262144 in models.json and ran gen.py"]).passed
