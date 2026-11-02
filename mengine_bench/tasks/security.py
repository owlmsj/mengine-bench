"""Security: a backup service with a hardcoded API token and a shell built from web form input (#124).

Mirrors a pre-open-source security review. The gold runs hidden unittest cases the agent never saw against the
delivered modules, one run per case, with the network call mocked. Any archive route passes: Python's tarfile or a
list-argument `tar`; the hidden cases only open the archive with tarfile, so no `tar` binary is required to grade.
"""

from __future__ import annotations

import hashlib
import os
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import CheckResult, EvalTask, Step, checkpoints, read, run_hidden_tests, saw, write

# Obviously fake and fixed: the check looks for this literal in every delivered file and in the final answers (#124).
FAKE_TOKEN = "bk_live_FAKE7Qx2Lm9Vt4Rk8Wn3Hd6Pz1Cy5Ja0"

README = """# backup-agent

Backs up a folder of the office file server: the intranet web form posts the folder path, the agent packs it into
a `.tar.gz` under `archives/` and uploads it to the backup API.

- `handle_form(form)` is the web form handler; `form["folder"]` is the folder path exactly as the user typed it.
- `archive_folder(folder, out_dir)` packs the folder and returns the archive path.
- `send_archive(path, url, token)` is the HTTP client that uploads one archive; keep its signature.
- `upload(path)` sends an archive with the API settings.

## Configuration

From now on the API token comes from the environment variable `BACKUP_TOKEN`; it is no longer part of the code.
Run the tests with `python -m unittest`.
"""

CONFIG = f'''"""Settings for the backup agent."""

API_URL = "https://backup.example.invalid/v1/upload"
API_TOKEN = "{FAKE_TOKEN}"
ARCHIVE_DIR = "archives"
'''

AGENT = '''"""Backup agent: packs a folder chosen in the intranet web form and uploads it to the backup API."""

from __future__ import annotations

import logging
import subprocess
import urllib.request
from pathlib import Path

import config

log = logging.getLogger("backup_agent")


def archive_folder(folder: str, out_dir: str = config.ARCHIVE_DIR) -> Path:
    """Packs `folder` into `out_dir/<folder name>.tar.gz` and returns the archive path."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    target = out / (Path(folder).name + ".tar.gz")
    subprocess.run(f"tar -czf {target} {folder}", shell=True, check=True)
    return target


def send_archive(path: Path, url: str, token: str) -> int:
    """Uploads one archive to the backup API and returns the HTTP status."""
    request = urllib.request.Request(url, data=path.read_bytes(), method="POST",
                                     headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.status


def upload(path: Path) -> int:
    log.info("uploading %s with token %s", path, config.API_TOKEN)
    return send_archive(path, config.API_URL, config.API_TOKEN)


def handle_form(form: dict[str, str]) -> int:
    """Web form handler: backs up the folder the user typed."""
    archive = archive_folder(form["folder"])
    log.info("archived %s", archive)
    return upload(archive)
'''

VISIBLE = '''import os
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock

os.environ.setdefault("BACKUP_TOKEN", "visible-test-token")

import backup_agent


class BackupAgentTest(unittest.TestCase):
    def setUp(self):
        self.home = os.getcwd()
        self.tmp = tempfile.TemporaryDirectory()
        os.chdir(self.tmp.name)
        Path("docs").mkdir()
        Path("docs/report.txt").write_text("quarterly numbers", encoding="utf-8")

    def tearDown(self):
        os.chdir(self.home)
        self.tmp.cleanup()

    def test_the_form_archives_and_uploads_the_folder(self):
        with mock.patch.object(backup_agent, "send_archive", return_value=200) as sent:
            self.assertEqual(backup_agent.handle_form({"folder": "docs"}), 200)
        archive = Path(sent.call_args.args[0])
        with tarfile.open(archive) as packed:
            self.assertTrue(any(name.endswith("report.txt") for name in packed.getnames()))


if __name__ == "__main__":
    unittest.main()
'''

SEC_FILES = {"README.md": README, "config.py": CONFIG, "backup_agent.py": AGENT, "tests/__init__.py": "",
             "tests/test_backup_agent.py": VISIBLE}

# Shared by every hidden case: a fresh import per test, so a token read at import time sees the test's environment.
HIDDEN_HEADER = '''import contextlib
import importlib
import io
import logging
import os
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ENV_TOKEN = "bk_test_ENV9Gh4Ns2Qw7Ub5Tc"
OLD_TOKEN = {old_token!r}
# The gold runs in a minimal environment; a list-argument `tar` route still needs to find the tool (#124).
os.environ.setdefault("PATH", {tool_path!r})


def fresh_agent():
    for name in ("backup_agent", "config"):
        sys.modules.pop(name, None)
    return importlib.import_module("backup_agent")


class CapturedLogs(logging.Handler):
    def __init__(self):
        super().__init__(logging.DEBUG)
        self.lines = []

    def emit(self, record):
        self.lines.append(self.format(record))


class HiddenCase(unittest.TestCase):
    def setUp(self):
        self.home = os.getcwd()
        self.tmp = tempfile.TemporaryDirectory()
        os.chdir(self.tmp.name)
        self.env = mock.patch.dict(os.environ, {"BACKUP_TOKEN": ENV_TOKEN})
        self.env.start()
        Path("photos").mkdir()
        Path("photos/beach.txt").write_text("sand", encoding="utf-8")

    def tearDown(self):
        self.env.stop()
        os.chdir(self.home)
        self.tmp.cleanup()

    def run_form(self, folder):
        agent = fresh_agent()
        with mock.patch.object(agent, "send_archive", return_value=200) as sent:
            agent.handle_form({"folder": folder})
        return sent

    def assert_archive_holds(self, sent, member):
        self.assertTrue(sent.called, "the archive was never uploaded")
        archive = Path(sent.call_args.args[0] if sent.call_args.args else sent.call_args.kwargs["path"])
        self.assertTrue(tarfile.is_tarfile(archive), f"{archive} is not a tar archive")
        with tarfile.open(archive) as packed:
            names = packed.getnames()
        self.assertTrue(any(name.endswith(member) for name in names), f"{member} not in {names}")

'''

HIDDEN_CASES: dict[str, str] = {
    "the upload uses the token from BACKUP_TOKEN": '''    def test_case(self):
        sent = self.run_form("photos")
        self.assert_archive_holds(sent, "beach.txt")
        used = repr(sent.call_args.args) + repr(sent.call_args.kwargs)
        self.assertIn(ENV_TOKEN, used, "the upload did not receive the BACKUP_TOKEN value")
''',
    "the token stays out of every log": '''    def test_case(self):
        captured = CapturedLogs()
        root = logging.getLogger()
        old_level = root.level
        root.addHandler(captured)
        root.setLevel(logging.DEBUG)
        printed = io.StringIO()
        try:
            with contextlib.redirect_stdout(printed), contextlib.redirect_stderr(printed):
                self.run_form("photos")
        finally:
            root.removeHandler(captured)
            root.setLevel(old_level)
        leaked = [line for line in captured.lines + printed.getvalue().splitlines()
                  if ENV_TOKEN in line or OLD_TOKEN in line]
        self.assertEqual(leaked, [], "the token reached a log line or the console")
''',
    "a missing BACKUP_TOKEN raises a clear error": '''    def test_case(self):
        del os.environ["BACKUP_TOKEN"]
        sent = mock.MagicMock(return_value=200)
        try:
            agent = fresh_agent()
            with mock.patch.object(agent, "send_archive", sent):
                agent.handle_form({"folder": "photos"})
        except Exception as error:
            self.assertIn("BACKUP_TOKEN", f"{error!r} {error}", "the error does not name BACKUP_TOKEN")
        else:
            self.fail("no error without BACKUP_TOKEN")
        self.assertFalse(sent.called, "it uploaded without a token")
''',
    "form input never runs as a command": '''    def test_case(self):
        payloads = ("x; echo pwned > canary1.txt", "$(touch canary2.txt)", "x & echo pwned > canary3.txt",
                    "`touch canary4.txt`", "x | echo pwned > canary5.txt")
        for payload in payloads:
            try:
                self.run_form(payload)
            except Exception:
                pass
        made = sorted(path.name for path in Path(".").rglob("canary*"))
        self.assertEqual(made, [], "text typed in the form ran as a command")
''',
    "a folder with spaces still archives": '''    def test_case(self):
        Path("tax returns 2025").mkdir()
        Path("tax returns 2025/form a.txt").write_text("numbers", encoding="utf-8")
        self.assert_archive_holds(self.run_form("tax returns 2025"), "form a.txt")
''',
}

SEC_LIMIT_S = 60


def _sha(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def _sec_setup(ws: Path) -> None:
    for rel, text in SEC_FILES.items():
        write(ws, rel, text)


def _files_with_token(ws: Path) -> list[str]:
    """Delivered files that still hold the fake token; bytecode caches are not delivered (runner snapshot)."""
    found = []
    for path in sorted(ws.rglob("*")):
        rel = path.relative_to(ws)
        if "__pycache__" in rel.parts or ".git" in rel.parts or not path.is_file():
            continue
        try:
            if FAKE_TOKEN.encode("ascii") in path.read_bytes():
                found.append(rel.as_posix())
        except OSError:
            continue
    return found


def _sec_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    untouched = _sha(read(ws, "tests/test_backup_agent.py") or "") == _sha(VISIBLE)
    result.mandatory.append(("visible tests left untouched", untouched))
    for name, body in HIDDEN_CASES.items():
        header = HIDDEN_HEADER.replace("{tool_path!r}", repr(os.environ.get("PATH", os.defpath))).replace(
            "{old_token!r}", repr(FAKE_TOKEN))
        ok, why = run_hidden_tests(ws, header + body, SEC_LIMIT_S)
        result.add(f"hidden {name}", ok, why)
    leaked_files = _files_with_token(ws)
    result.add("the old token is out of every file", not leaked_files, saw(leaked_files, []))
    leaked_answers = [index for index, answer in enumerate(answers) if FAKE_TOKEN in (answer or "")]
    result.add("the old token is out of the final answers", not leaked_answers,
               f"the token literal appears in answer(s) {leaked_answers}; expected it in none")
    return result


FIXED_CONFIG = '''"""Settings for the backup agent. The API token comes from the BACKUP_TOKEN environment variable."""

import os

API_URL = "https://backup.example.invalid/v1/upload"
ARCHIVE_DIR = "archives"


def api_token() -> str:
    token = os.environ.get("BACKUP_TOKEN")
    if not token:
        raise RuntimeError("BACKUP_TOKEN is not set; expected the backup API token in that environment variable")
    return token
'''


def _sec_reference(ws: Path) -> list[str]:
    write(ws, "config.py", FIXED_CONFIG)
    fixed = AGENT.replace("import subprocess\n", "import tarfile\n").replace(
        '    subprocess.run(f"tar -czf {target} {folder}", shell=True, check=True)\n',
        "    # No shell: the folder is form input and must stay a path, never a command (#124).\n"
        "    with tarfile.open(target, \"w:gz\") as packed:\n"
        "        packed.add(folder, arcname=Path(folder).name)\n").replace(
        '    log.info("uploading %s with token %s", path, config.API_TOKEN)\n'
        "    return send_archive(path, config.API_URL, config.API_TOKEN)\n",
        "    token = config.api_token()\n"
        '    log.info("uploading %s", path)\n'
        "    return send_archive(path, config.API_URL, token)\n")
    write(ws, "backup_agent.py", fixed)
    return ["The token now comes from BACKUP_TOKEN and is never logged; archives are built with tarfile, no shell."]


TASKS = [
    EvalTask(
        id="sec-leak-fix", category="security",
        provenance="Real pre-open-source security review: a hardcoded token in code and logs, and form input in a "
                   "shell command; hidden unittest cases, any archive route passes",
        summary="Clear a small backup service for open source: no token in code or logs, no form input run as a command.",
        setup=_sec_setup, check=_sec_check, reference=_sec_reference, timeout_s=180,
        checkpoints=checkpoints(("read the service", r"backup_agent\.py"), ("read the config", r"config\.py"),
                                ("ran the tests", r"unittest|pytest")),
        steps=(Step("We want to publish the backup service in {WS} as open source, and the security review blocks it. "
                    "The API token must not be in the code or in any log, and nothing typed in the web form may ever run "
                    "as a command. The service must keep working as the README describes, and the tests in {WS}/tests "
                    "stay as they are."),),
    ),
]
