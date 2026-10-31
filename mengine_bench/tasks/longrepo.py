"""Long-horizon one-shot task: ~100-file game server, integration-only bug.

Two layered bugs across two modules (config precedence and profile codec).
Unit tests pass; the visible integration test fails; fixing one bug reveals
the next. Payout rounding already follows docs/ECONOMY.md.
Ported from the private suite with a neutral test profile.
"""

from __future__ import annotations

import hashlib
import random
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import (
    CheckResult,
    EvalTask,
    Step,
    read,
    run_hidden_tests,
    write,
)

CORE = {
    "arena_server/__init__.py": "",
    "arena_server/config/__init__.py": "",
    "arena_server/config/defaults.py": '''DEFAULTS = {
    "win_base": 900,
    "loss_base": 600,
    "kill_bonus": 50,
    "event_multiplier": 1.0,
}
''',
    "arena_server/config/loader.py": '''"""Runtime config. Precedence, lowest to highest: DEFAULTS < JSON file < env (docs/CONFIG.md)."""

import json
import os

from arena_server.config.defaults import DEFAULTS


def _coerce(raw, like):
    return type(like)(raw)


def load_config(file_path=None, env=None):
    cfg = dict(DEFAULTS)
    env = os.environ if env is None else env
    for key, default in DEFAULTS.items():
        value = env.get(f"ARENA_{key.upper()}")
        if value is not None:
            cfg[key] = _coerce(value, default)
    if file_path:
        with open(file_path, encoding="utf-8") as fh:
            cfg.update(json.load(fh))
    return cfg
''',
    "arena_server/models/__init__.py": "",
    "arena_server/models/profile.py": '''from dataclasses import dataclass, field


@dataclass
class Profile:
    name: str
    level: int = 1
    credits: int = 0
    cosmetics: list = field(default_factory=list)
''',
    "arena_server/economy/__init__.py": "",
    "arena_server/economy/payout.py": '''"""Match payout. Rules live in docs/ECONOMY.md."""

import math


def match_payout(won, kills, cfg):
    base = cfg["win_base"] if won else cfg["loss_base"]
    raw = (base + kills * cfg["kill_bonus"]) * cfg["event_multiplier"]
    return int(math.floor(raw / 10 + 0.5) * 10)
''',
    "arena_server/economy/legacy_payout.py": '''"""DEPRECATED since 0.12 - kept for old replays only; not used by the live economy."""


def legacy_payout(won, kills):
    return (1000 if won else 500) + kills * 40
''',
    "arena_server/persistence/__init__.py": "",
    "arena_server/persistence/codec.py": '''import json

from arena_server.models.profile import Profile


def encode(profile):
    return json.dumps({"name": profile.name, "level": profile.level,
                       "credits": profile.credits, "cosmetics": profile.cosmetics})


def decode(blob):
    data = json.loads(blob)
    return Profile(name=data["name"], level=data.get("level", 1), cosmetics=data.get("cosmetics", []))
''',
    "arena_server/persistence/store.py": '''from pathlib import Path

from arena_server.persistence.codec import decode, encode


def save(profile, path):
    Path(path).write_text(encode(profile), encoding="utf-8")


def load(path):
    return decode(Path(path).read_text(encoding="utf-8"))
''',
    "arena_server/services/__init__.py": "",
    "arena_server/services/match_service.py": '''from arena_server.economy.payout import match_payout


def finish_match(profile, won, kills, cfg):
    profile.credits += match_payout(won, kills, cfg)
    return profile
''',
    "docs/CONFIG.md": "# Config\n\nPrecedence (lowest to highest): `DEFAULTS` < JSON file < environment variables "
                      "`ARENA_<KEY>`. The environment always wins: that is how live-ops changes events without "
                      "a deploy.\n",
    "docs/ECONOMY.md": "# Economy\n\nPayout = (base + kills x kill_bonus) x event_multiplier, rounded to the nearest "
                       "TEN, with halves always rounding up (1425 -> 1430, 1585 -> 1590). Base: win 900, loss 600. "
                       "Credits persist in the profile and survive save/load.\n",
    "README.md": "# arena-server\n\nBackend of Pixel Arena: config, economy, profiles, matchmaking and live-ops "
                 "services. Tests: `python -m unittest discover -s tests -t .`\n",
    "tests/__init__.py": "",
    "tests/unit/__init__.py": "",
    "tests/integration/__init__.py": "",
    "tests/unit/test_core_units.py": '''import unittest

from arena_server.config.loader import load_config
from arena_server.models.profile import Profile


class CoreUnits(unittest.TestCase):
    def test_defaults_load(self):
        self.assertEqual(load_config(env={})["win_base"], 900)

    def test_profile_defaults(self):
        self.assertEqual(Profile("x").credits, 0)


if __name__ == "__main__":
    unittest.main()
''',
    "tests/integration/test_match_flow.py": '''import json
import tempfile
import unittest
from pathlib import Path

from arena_server.config.loader import load_config
from arena_server.models.profile import Profile
from arena_server.persistence.store import load, save
from arena_server.services.match_service import finish_match


class MatchFlow(unittest.TestCase):
    def test_event_weekend_win_is_paid_and_persisted(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
            cfg_file = Path(tmp) / "live.json"
            cfg_file.write_text(json.dumps({"kill_bonus": 50, "event_multiplier": 1.25}))
            cfg = load_config(cfg_file, env={"ARENA_KILL_BONUS": "75"})
            profile = Profile("player1", level=12, credits=100, cosmetics=["neoplastic_skin"])
            finish_match(profile, won=True, kills=5, cfg=cfg)
            save(profile, Path(tmp) / "player1.json")
            reloaded = load(Path(tmp) / "player1.json")
            self.assertEqual(reloaded.credits, 100 + 1590)


if __name__ == "__main__":
    unittest.main()
''',
}

DOMAINS = ["cosmetics", "locales", "telemetry", "matchmaking", "anticheat",
           "leaderboard", "chat", "store", "quests", "notifications"]
MODULES = ["registry", "rules", "formatters", "validators", "events", "cache", "schema", "adapters", "metrics"]


def _filler() -> dict[str, str]:
    rng = random.Random(6335)
    files: dict[str, str] = {}
    for domain in DOMAINS:
        files[f"arena_server/{domain}/__init__.py"] = ""
        for module in MODULES:
            n = rng.randint(2, 40)
            files[f"arena_server/{domain}/{module}.py"] = (
                f'"""{domain}.{module}: part of the Pixel Arena live backend."""\n\n\n'
                f"def {module}_limit():\n    return {n}\n\n\n"
                f"def describe():\n    return \"{domain}/{module} v{rng.randint(1, 9)}\"\n")
        files[f"tests/unit/test_{domain}.py"] = (
            "import unittest\n\n"
            f"from arena_server.{domain} import registry, rules\n\n\n"
            f"class {domain.title()}Test(unittest.TestCase):\n"
            "    def test_describe(self):\n"
            f"        self.assertIn(\"{domain}\", registry.describe())\n"
            f"        self.assertGreater(rules.rules_limit(), 0)\n")
    return files


FILES = {**CORE, **_filler()}
PROTECTED = [rel for rel in FILES if rel.startswith("tests/")]

HIDDEN = '''import json
import tempfile
import unittest
from pathlib import Path

from arena_server.config.loader import load_config
from arena_server.models.profile import Profile
from arena_server.persistence.store import load, save
from arena_server.services.match_service import finish_match


def play(cfg_file_data, env, won, kills, credits=0, name="p"):
    with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
        path = None
        if cfg_file_data is not None:
            path = Path(tmp) / "c.json"
            path.write_text(json.dumps(cfg_file_data))
        cfg = load_config(path, env=env)
        profile = Profile(name, level=7, credits=credits, cosmetics=["a", "b"])
        finish_match(profile, won=won, kills=kills, cfg=cfg)
        save(profile, Path(tmp) / "p.json")
        return load(Path(tmp) / "p.json")


class Hidden(unittest.TestCase):
    def test_config_override_and_persistence(self):
        self.assertEqual(play({"kill_bonus": 50, "event_multiplier": 1.25}, {"ARENA_KILL_BONUS": "75"}, True, 5, 100).credits, 1690)

    def test_env_float_wins_over_file(self):
        self.assertEqual(play({"event_multiplier": 1.1}, {"ARENA_EVENT_MULTIPLIER": "1.5"}, False, 2).credits, 1050)

    def test_round_trip_keeps_everything(self):
        p = play(None, {}, False, 0, 40)
        self.assertEqual((p.level, p.credits, p.cosmetics), (7, 640, ["a", "b"]))

    # #28: documented behavior the visible test does not exercise; a fix must keep it.
    # Each scenario also goes through a fixed bug, so the untouched backend earns none of them.
    def test_half_up_tie_rounds_up(self):
        self.assertEqual(play({"win_base": 1000}, {"ARENA_WIN_BASE": "1425"}, True, 0).credits, 1430)

    def test_persisted_name_survives(self):
        p = play(None, {}, True, 1, 10, name="Player One")
        self.assertEqual((p.name, p.credits), ("Player One", 960))

    def test_real_environment_when_env_is_none(self):
        import os
        saved = os.environ.get("ARENA_KILL_BONUS")
        os.environ["ARENA_KILL_BONUS"] = "80"
        try:
            with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
                path = Path(tmp) / "c.json"
                path.write_text(json.dumps({"kill_bonus": 50}))
                self.assertEqual(load_config(path, env=None)["kill_bonus"], 80)
        finally:
            if saved is None:
                del os.environ["ARENA_KILL_BONUS"]
            else:
                os.environ["ARENA_KILL_BONUS"] = saved


if __name__ == "__main__":
    unittest.main()
'''


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _setup(ws: Path) -> None:
    for rel, text in FILES.items():
        write(ws, rel, text)


def _check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    untouched = all(_sha(read(ws, rel) or "") == _sha(FILES[rel]) for rel in PROTECTED)
    result.mandatory.append(("existing tests untouched", untouched))
    for scenario in ("config_override_and_persistence", "env_float_wins_over_file", "round_trip_keeps_everything",
                     "half_up_tie_rounds_up", "persisted_name_survives", "real_environment_when_env_is_none"):
        selection = ("\n\ndef load_tests(loader, tests, pattern):\n"
                     f"    return unittest.TestSuite([Hidden('test_{scenario}')])\n")
        ok, _ = run_hidden_tests(ws, HIDDEN + selection)
        result.add(f"hidden {scenario.replace('_', ' ')}", ok)
    return result


def _reference(ws: Path) -> list[str]:
    loader = FILES["arena_server/config/loader.py"].replace(
        '''    for key, default in DEFAULTS.items():
        value = env.get(f"ARENA_{key.upper()}")
        if value is not None:
            cfg[key] = _coerce(value, default)
    if file_path:
        with open(file_path, encoding="utf-8") as fh:
            cfg.update(json.load(fh))
''', '''    if file_path:
        with open(file_path, encoding="utf-8") as fh:
            cfg.update(json.load(fh))
    for key, default in DEFAULTS.items():
        value = env.get(f"ARENA_{key.upper()}")
        if value is not None:
            cfg[key] = _coerce(value, default)
''')
    codec = FILES["arena_server/persistence/codec.py"].replace(
        'Profile(name=data["name"], level=data.get("level", 1), cosmetics=data.get("cosmetics", []))',
        'Profile(name=data["name"], level=data.get("level", 1), credits=data.get("credits", 0),\n'
        '                   cosmetics=data.get("cosmetics", []))')
    write(ws, "arena_server/config/loader.py", loader)
    write(ws, "arena_server/persistence/codec.py", codec)
    return ["fixed loader precedence and codec credits"]


TASKS = [
    EvalTask(
        id="gd-integration-repo", category="gamedev",
        provenance="Long-horizon SWE: ~100-file game backend, 2 layered bugs only visible end to end; spec in docs/",
        summary="Fix configuration priority and saved player credits in a game server without changing existing tests.",
        setup=_setup, check=_check, reference=_reference,
        timeout_s=1800,
        steps=(Step("The backend in {WS} (Pixel Arena) has the integration test in {WS}/tests/integration failing, "
                    "while the unit tests pass. Find and fix ALL root causes following the specification in {WS}/docs "
                    "(not just the symptom of the visible test). Do not change any existing test. Use the Python "
                    "standard library only. At the end run the "
                    "whole suite with `python -m unittest discover -s tests -t .` from {WS}. This is your ONLY "
                    "request: there will be no second turn; deliver everything fixed and summarize the root cause + "
                    "file:line of each bug."),),
    ),
]
