"""Config drift: one source generates the harness configs, and a generated copy was hand-edited (#124).

The owner's rule is that a generated file is never the place to fix a value: the fix goes into the source and the
copies are rebuilt from it. The gold runs the original generator on the delivered source, so editing the source and
running the generator passes, and so does editing the source and patching every copy by hand to the same result.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import tomllib
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import CheckResult, EvalTask, Step, checkpoints, read, saw, scratch_root, write

CFG_FAST_CODER = "fast-coder"
CFG_WANTED_CONTEXT = 262144
CFG_OLD_CONTEXT = 131072
CFG_OUTPUTS = ("out/opencode.json", "out/codex.toml", "out/claude.json")
CFG_GEN_LIMIT_S = 60

CFG_SOURCE = """{
  "models": [
    {"name": "fast-coder", "context_window": 131072, "max_output": 16384, "tool_calling": true},
    {"name": "deep-thinker", "context_window": 200000, "max_output": 32768, "tool_calling": true},
    {"name": "tiny-chat", "context_window": 32768, "max_output": 4096, "tool_calling": false}
  ]
}
"""

CFG_GEN = '''"""Writes the harness configs in out/ from models.json. Python stdlib only."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def opencode(models):
    entries = {
        model["name"]: {
            "name": model["name"],
            "limit": {"context": model["context_window"], "output": model["max_output"]},
            "tool_call": model["tool_calling"],
        }
        for model in models
    }
    config = {"provider": {"workstation": {"npm": "@ai-sdk/openai-compatible", "models": entries}}}
    return json.dumps(config, indent=2) + "\\n"


def codex(models):
    lines = []
    for model in models:
        lines += [
            f'[models."{model["name"]}"]',
            f'context_window = {model["context_window"]}',
            f'max_output_tokens = {model["max_output"]}',
            f'tool_calling = {"true" if model["tool_calling"] else "false"}',
            "",
        ]
    return "\\n".join(lines)


def claude(models):
    entries = [
        {
            "id": model["name"],
            "contextWindow": model["context_window"],
            "maxOutputTokens": model["max_output"],
            "supportsTools": model["tool_calling"],
        }
        for model in models
    ]
    return json.dumps({"models": entries}, indent=2) + "\\n"


def main():
    models = json.loads((ROOT / "models.json").read_text(encoding="utf-8"))["models"]
    out = ROOT / "out"
    out.mkdir(exist_ok=True)
    for name, render in (("opencode.json", opencode), ("codex.toml", codex), ("claude.json", claude)):
        (out / name).write_text(render(models), encoding="utf-8", newline="\\n")
        print(f"wrote out/{name}")


if __name__ == "__main__":
    main()
'''

CFG_README = """# Harness model configs

The model settings that OpenCode, Codex and Claude Code read on the workstation.

- `models.json`: the models we serve and their limits.
- `gen.py`: writes `out/` from `models.json` (`python gen.py`).
- `out/`: generated; the install step copies these files into each harness.
"""

CFG_GEN_FILE = "gen.py"
CFG_SOURCE_FILE = "models.json"


def _cfg_sha(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def _cfg_generate(source_text: str) -> dict[str, str]:
    """The original generator run on a source text, in a temp dir: out/ file -> text, or {} when it fails."""
    with tempfile.TemporaryDirectory(prefix="bench-cfg-", dir=scratch_root()) as tmp:
        root = Path(tmp)
        write(root, CFG_GEN_FILE, CFG_GEN)
        write(root, CFG_SOURCE_FILE, source_text)
        try:
            done = subprocess.run([sys.executable, "-I", str(root / CFG_GEN_FILE)], cwd=root, capture_output=True,
                                  text=True, timeout=CFG_GEN_LIMIT_S, check=False)
        except subprocess.TimeoutExpired:
            return {}
        if done.returncode != 0:
            return {}
        return {rel: read(root, rel) or "" for rel in CFG_OUTPUTS}


def _cfg_parse(rel: str, text: str | None) -> object | None:
    """A generated file as data, so a copy patched by hand in another layout still compares equal."""
    if text is None:
        return None
    try:
        return tomllib.loads(text) if rel.endswith(".toml") else json.loads(text)
    except (ValueError, tomllib.TOMLDecodeError):
        return None


def _cfg_dig(value: object, *keys: str) -> object:
    """value[k1][k2]..., or None when the shape differs (a hand edit may break any level)."""
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def _cfg_fast_coder_contexts(outputs: dict[str, str]) -> dict[str, object]:
    """fast-coder's context window as each generated config states it."""
    opencode = _cfg_parse(CFG_OUTPUTS[0], outputs.get(CFG_OUTPUTS[0]))
    codex = _cfg_parse(CFG_OUTPUTS[1], outputs.get(CFG_OUTPUTS[1]))
    claude = _cfg_dig(_cfg_parse(CFG_OUTPUTS[2], outputs.get(CFG_OUTPUTS[2])), "models")
    entries = claude if isinstance(claude, list) else []
    return {
        "opencode": _cfg_dig(opencode, "provider", "workstation", "models", CFG_FAST_CODER, "limit", "context"),
        "codex": _cfg_dig(codex, "models", CFG_FAST_CODER, "context_window"),
        "claude": next((entry.get("contextWindow") for entry in entries
                        if isinstance(entry, dict) and entry.get("id") == CFG_FAST_CODER), None),
    }


def _cfg_models_by_name(source_text: str | None) -> dict[str, dict[str, object]] | None:
    models = _cfg_dig(_cfg_parse(CFG_SOURCE_FILE, source_text), "models")
    if not isinstance(models, list):
        return None
    return {str(model.get("name")): model for model in models if isinstance(model, dict)}


def _cfg_without_target(models: dict[str, dict[str, object]] | None) -> dict[str, dict[str, object]] | None:
    """Every model setting except fast-coder's context window, which the first check grades on its own."""
    if models is None:
        return None
    rest = {name: dict(model) for name, model in models.items()}
    rest.get(CFG_FAST_CODER, {}).pop("context_window", None)
    return rest


def _cfg_setup(ws: Path) -> None:
    write(ws, "README.md", CFG_README)
    write(ws, CFG_SOURCE_FILE, CFG_SOURCE)
    write(ws, CFG_GEN_FILE, CFG_GEN)
    generated = _cfg_generate(CFG_SOURCE)
    if not generated:
        raise RuntimeError(f"cfg-source-drift setup received a failing generator; expected {CFG_OUTPUTS} written")
    # The drift: someone fixed OpenCode's copy by hand and never touched the source (#124).
    opencode = generated[CFG_OUTPUTS[0]]
    drifted = opencode.replace(f'"context": {CFG_OLD_CONTEXT},', f'"context": {CFG_WANTED_CONTEXT},', 1)
    if drifted == opencode:
        raise RuntimeError(f"cfg-source-drift setup found no context {CFG_OLD_CONTEXT} in {opencode[:120]!r}")
    generated[CFG_OUTPUTS[0]] = drifted
    for rel, text in generated.items():
        write(ws, rel, text)


def _cfg_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    result.mandatory.append(("the generator is left untouched", _cfg_sha(read(ws, CFG_GEN_FILE) or "") == _cfg_sha(CFG_GEN)))
    source = read(ws, CFG_SOURCE_FILE)
    regenerated = _cfg_generate(source) if source is not None else {}
    contexts = _cfg_fast_coder_contexts(regenerated)
    want_contexts = {name: CFG_WANTED_CONTEXT for name in ("opencode", "codex", "claude")}
    result.add("regenerating gives fast-coder 262144 in all three configs", contexts == want_contexts,
               saw(contexts, want_contexts))
    stale = [rel for rel in CFG_OUTPUTS
             if not regenerated or _cfg_parse(rel, read(ws, rel)) != _cfg_parse(rel, regenerated.get(rel))]
    result.add("the delivered configs equal what the source generates", not stale,
               saw(f"{stale} differ from a fresh generation", "every out/ file as gen.py writes it"))
    models = _cfg_without_target(_cfg_models_by_name(source))
    expected = _cfg_without_target(_cfg_models_by_name(CFG_SOURCE))
    result.add("the other models and fields are unchanged", models == expected, saw(models, expected))
    return result


def _cfg_reference(ws: Path) -> list[str]:
    source = (read(ws, CFG_SOURCE_FILE) or "").replace(
        f'"name": "fast-coder", "context_window": {CFG_OLD_CONTEXT}',
        f'"name": "fast-coder", "context_window": {CFG_WANTED_CONTEXT}')
    write(ws, CFG_SOURCE_FILE, source)
    subprocess.run([sys.executable, "-I", str(ws / CFG_GEN_FILE)], cwd=ws, capture_output=True, timeout=CFG_GEN_LIMIT_S,
                   check=True)
    return ["fast-coder now has 262144 in models.json and the configs were regenerated"]


TASKS = [
    EvalTask(
        id="cfg-source-drift", category="engineering",
        provenance="Owner's rule: one source of truth generates every harness config; a hand-edited generated copy is a bug",
        summary="Make three harness configs agree on a model's context window, for good.",
        setup=_cfg_setup, check=_cfg_check, reference=_cfg_reference, timeout_s=180,
        checkpoints=checkpoints(("read the readme", r"README"), ("ran the generator", r"gen\.py")),
        steps=(Step("The model configs our coding harnesses use are in {WS}: OpenCode, Codex and Claude Code each get "
                    "one. They disagree about the context window of fast-coder: OpenCode's config says 262144, the other "
                    "two say 131072. 262144 is the right value. Make all three agree, for good. Every other model "
                    "setting stays as it is."),),
    ),
]
