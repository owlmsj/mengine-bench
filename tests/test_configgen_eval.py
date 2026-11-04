"""#124: cfg-source-drift passes a fix in the source, however out/ is rebuilt, and fails a patched copy."""

from __future__ import annotations

import io
import json
import os
import subprocess
import time
from pathlib import Path

import psutil
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
OWN_GENERATOR = "the delivered generator still writes those configs"


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


def test_a_generator_hardcoding_the_value_fails_the_regeneration(tmp_path: Path) -> None:
    # The source still says 131072, so the fix lives in the generator, not in the source of truth.
    ws = _fresh(tmp_path)
    hacked = CFG_GEN.replace('"context": model["context_window"]', '"context": 262144')
    write(ws, "gen.py", hacked)
    for rel, text in configgen._cfg_generate(CFG_SOURCE).items():
        write(ws, rel, text.replace("131072", "262144", 1) if rel.endswith("opencode.json") else text)
    result = _cfg_check(ws, [""])
    assert REGENERATED in result.failed() and not result.passed


def test_a_refactored_generator_with_the_same_output_passes(tmp_path: Path) -> None:
    # #124: the Opus 5.5 xhigh probe split gen.py into a RENDERERS table and added a drift test; a valid route.
    ws = _fresh(tmp_path)
    _cfg_reference(ws)
    write(ws, "gen.py", CFG_GEN + "\n# renderers listed once so a drift test can reuse them\n")
    write(ws, "test_gen.py", "import unittest\n")
    assert _cfg_check(ws, [""]).passed


@pytest.mark.parametrize("broken", [
    "raise SystemExit('gen.py broken')\n",
    CFG_GEN.replace('"contextWindow": model["context_window"]', '"contextWindow": 131072'),
    CFG_GEN.replace("    main()\n", "    pass\n"),
], ids=["crashes", "hardcodes-claude-context", "writes-nothing"])
def test_a_delivery_whose_generator_no_longer_regenerates_fails(tmp_path: Path, broken: str) -> None:
    # #164: right source and outputs with a broken gen.py passed, because only the bundled generator ran.
    ws = _fresh(tmp_path)
    _cfg_reference(ws)
    write(ws, "gen.py", broken)
    result = _cfg_check(ws, [""])
    assert result.failed() == [OWN_GENERATOR], (result.failed(), result.details)


@pytest.mark.parametrize("entrypoint", [
    "from render import main\n\nmain()\n",
    "import subprocess\nsubprocess.run(['python', 'render.py'], check=True)\n",
], ids=["sibling-import", "python-child"])
def test_a_generator_split_into_modules_passes(tmp_path: Path, entrypoint: str) -> None:
    # #164: an equivalent refactor that imports a sibling module still regenerates the same configs.
    ws = _fresh(tmp_path)
    _cfg_reference(ws)
    write(ws, "render.py", CFG_GEN)
    write(ws, "gen.py", entrypoint)
    result = _cfg_check(ws, [""])
    assert result.passed, (result.failed(), result.details)


def test_delivered_generator_receives_only_minimal_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ws = _fresh(tmp_path)
    _cfg_reference(ws)
    monkeypatch.setenv("BENCH_TEST_SENTINEL", "synthetic-do-not-inherit")
    allowed = {"PATH", "SYSTEMROOT", "TEMP", "TMP"} if os.name == "nt" else {"PATH", "LC_CTYPE"}
    write(ws, "gen.py", "import os\nassert set(os.environ) <= " + repr(allowed) + "\n" + CFG_GEN)
    assert _cfg_check(ws, [""]).passed


def test_generator_depending_on_inherited_host_values_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # #164: this delivery previously passed by reading the grader's environment.
    ws = _fresh(tmp_path)
    _cfg_reference(ws)
    monkeypatch.setenv("BENCH_TEST_SENTINEL", "synthetic-do-not-inherit")
    write(ws, "gen.py", "import os\nassert os.environ.get('BENCH_TEST_SENTINEL') == 'synthetic-do-not-inherit'\n" + CFG_GEN)
    assert _cfg_check(ws, [""]).failed() == [OWN_GENERATOR]


def test_delivered_generator_runs_in_a_private_copy(tmp_path: Path) -> None:
    ws = _fresh(tmp_path)
    _cfg_reference(ws)
    write(ws, "gen.py", "from pathlib import Path\nPath('private-marker').write_text('copy only')\n" + CFG_GEN)
    assert _cfg_check(ws, [""]).passed
    assert not (ws / "private-marker").exists()


def test_noisy_valid_generator_passes_with_bounded_capture(tmp_path: Path) -> None:
    ws = _fresh(tmp_path)
    _cfg_reference(ws)
    write(ws, "gen.py", "print('x' * (256 * 1024))\n" + CFG_GEN)
    assert _cfg_check(ws, [""]).passed
    captured = bytearray()
    configgen._cfg_drain_output(io.BytesIO(b"x" * (256 * 1024)), captured)
    assert captured == b"x" * configgen.CFG_GEN_OUTPUT_LIMIT


@pytest.mark.parametrize("parent_exits", [False, True], ids=["timeout", "parent-exits"])
def test_generator_children_do_not_survive(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, parent_exits: bool) -> None:
    monkeypatch.setattr(configgen, "CFG_GEN_LIMIT_S", 1.0)
    write(tmp_path, "gen.py", "import subprocess, sys, time\nfrom pathlib import Path\n"
          "child = subprocess.Popen([sys.executable, '-I', '-c', 'import time; time.sleep(120)'])\n"
          "Path('child.pid').write_text(str(child.pid))\n" + ("" if parent_exits else "time.sleep(120)\n"))
    started = time.monotonic()
    try:
        assert configgen._cfg_run_generator(tmp_path, "-Es") == {}
        child_pid = int((tmp_path / "child.pid").read_text())
        assert time.monotonic() - started < 5
        assert not psutil.pid_exists(child_pid) or psutil.Process(child_pid).status() == psutil.STATUS_ZOMBIE
    finally:
        pid_file = tmp_path / "child.pid"
        if pid_file.exists() and psutil.pid_exists(int(pid_file.read_text())):
            psutil.Process(int(pid_file.read_text())).kill()


@pytest.mark.parametrize("external", [False, True], ids=["internal", "escaping"])
def test_project_symlinks_stay_inside_copy(tmp_path: Path, external: bool) -> None:
    ws = tmp_path / "project"
    ws.mkdir()
    _fresh(ws)
    _cfg_reference(ws)
    target = tmp_path / "outside.py" if external else ws / "render.py"
    target.write_text(CFG_GEN, encoding="utf-8")
    (ws / "gen.py").unlink()
    try:
        (ws / "gen.py").symlink_to(os.path.relpath(target, ws))
    except OSError as exc:
        pytest.skip(f"symlink creation unavailable: {exc.winerror if hasattr(exc, 'winerror') else exc.errno}")
    result = _cfg_check(ws, [""])
    assert result.passed is (not external)
    if external:
        assert result.failed() == [OWN_GENERATOR]


def test_escaping_link_is_refused_before_copy_or_execution(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # #164: exercise the refusal even on Windows hosts without symlink creation privileges.
    ws = tmp_path / "project"
    ws.mkdir()
    write(ws, "escape.py", "raise AssertionError('must not execute')")
    original_resolve = Path.resolve

    def resolve_link(path: Path, strict: bool = False) -> Path:
        return tmp_path / "external.py" if path == ws / "escape.py" else original_resolve(path, strict=strict)

    monkeypatch.setattr(Path, "resolve", resolve_link)
    assert configgen._cfg_generate_delivered(ws) == {}


def test_copy_preserves_symlinks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ws = _fresh(tmp_path)
    _cfg_reference(ws)
    original_copytree = configgen.shutil.copytree
    seen: list[bool] = []

    def copy_project(source: Path, destination: Path, *args: object, **kwargs: object) -> Path:
        seen.append((args[0] if args else kwargs.get("symlinks")) is True)
        return original_copytree(source, destination, *args, **kwargs)

    monkeypatch.setattr(configgen.shutil, "copytree", copy_project)
    assert configgen._cfg_generate_delivered(ws)
    assert seen and all(seen)


@pytest.mark.skipif(os.name != "nt", reason="Windows directory junction regression")
def test_escaping_directory_junction_is_refused(tmp_path: Path) -> None:
    # #164: junctions can escape copytree on Windows without symlink privileges.
    ws = tmp_path / "project"
    ws.mkdir()
    _fresh(ws)
    _cfg_reference(ws)
    outside = tmp_path / "outside"
    outside.mkdir()
    done = subprocess.run(["cmd", "/c", "mklink", "/J", str(ws / "escape"), str(outside)],
                          cwd=tmp_path, capture_output=True, check=False, timeout=5)
    assert done.returncode == 0
    assert _cfg_check(ws, [""]).failed() == [OWN_GENERATOR]


def test_the_brief_does_not_hand_over_the_cause() -> None:
    prompt = _task().steps[0].prompt.lower()
    for word in ("models.json", "gen.py", "generat", "source of truth", "out/", "hand-edit", "hand edit"):
        assert word not in prompt, word


def test_a_correct_answer_in_the_chat_alone_earns_nothing(tmp_path: Path) -> None:
    ws = _fresh(tmp_path)
    assert not _cfg_check(ws, ["I set fast-coder to 262144 in models.json and ran gen.py"]).passed


@pytest.mark.parametrize("excluded", [".venv", "__pycache__", ".git", "node_modules"])
@pytest.mark.parametrize("parent", ["", "nested"])
def test_excluded_tree_links_do_not_reject_delivery(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                                   excluded: str, parent: str) -> None:
    # #164: ignored environments/caches are not part of the executed project copy.
    ws = _fresh(tmp_path)
    _cfg_reference(ws)
    ignored = ws / parent / excluded
    write(ignored, "escape", "ignored")
    original_resolve = Path.resolve

    def resolve_link(path: Path, strict: bool = False) -> Path:
        return tmp_path.parent / "outside" if path == ignored / "escape" else original_resolve(path, strict=strict)

    monkeypatch.setattr(Path, "resolve", resolve_link)
    assert _cfg_check(ws, [""]).passed
