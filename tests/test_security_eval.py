"""#124: the security review eval fails each leak on its own, accepts every safe route and reads only delivered files."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.core import write
from mengine_bench.tasks import security
from mengine_bench.tasks.security import AGENT, FAKE_TOKEN, FIXED_CONFIG

TARFILE_ADD = "        packed.add(folder, arcname=Path(folder).name)\n"


def _task() -> object:
    return next(task for task in catalog.all_tasks() if task.id == "sec-leak-fix")


def _solved(ws: Path) -> Path:
    security._sec_setup(ws)
    security._sec_reference(ws)
    return ws


def _replace(ws: Path, rel: str, old: str, new: str) -> None:
    text = (ws / rel).read_text(encoding="utf-8")
    assert old in text, old
    write(ws, rel, text.replace(old, new))


def test_the_reference_passes_and_the_untouched_folder_fails(tmp_path: Path) -> None:
    task = _task()
    (tmp_path / "bare").mkdir()
    (tmp_path / "solved").mkdir()
    task.setup(tmp_path / "bare")
    bare = task.check(tmp_path / "bare", [""])
    assert not bare.passed
    assert "hidden form input never runs as a command" in bare.failed()
    task.setup(tmp_path / "solved")
    result = task.check(tmp_path / "solved", task.reference(tmp_path / "solved"))
    assert result.passed, (result.failed(), result.details)


@pytest.mark.skipif(shutil.which("tar") is None, reason="the list-argument route needs a tar binary")
def test_a_list_argument_tar_and_a_token_read_at_import_pass(tmp_path: Path) -> None:
    security._sec_setup(tmp_path)
    write(tmp_path, "config.py", 'import os\n\nAPI_URL = "https://backup.example.invalid/v1/upload"\n'
                                 'API_TOKEN = os.environ["BACKUP_TOKEN"]\nARCHIVE_DIR = "archives"\n')
    agent = AGENT.replace(
        '    subprocess.run(f"tar -czf {target} {folder}", shell=True, check=True)\n',
        "    source = Path(folder)\n"
        '    subprocess.run(["tar", "-czf", str(target), "-C", str(source.parent), source.name], check=True)\n'
    ).replace('    log.info("uploading %s with token %s", path, config.API_TOKEN)\n', '    log.info("uploading %s", path)\n')
    write(tmp_path, "backup_agent.py", agent)
    result = security._sec_check(tmp_path, ["The token now comes from the environment."])
    assert result.passed, (result.failed(), result.details)


@pytest.mark.parametrize(("rel", "old", "new", "check"), [
    ("backup_agent.py", "send_archive(path, config.API_URL, token)", 'send_archive(path, config.API_URL, "")',
     "hidden the upload uses the token from BACKUP_TOKEN"),
    ("backup_agent.py", '    log.info("uploading %s", path)\n', '    log.debug("uploading %s with %s", path, token)\n',
     "hidden the token stays out of every log"),
    ("config.py", '    token = os.environ.get("BACKUP_TOKEN")\n    if not token:\n',
     '    token = os.environ.get("BACKUP_TOKEN", "")\n    if token is None:\n',
     "hidden a missing BACKUP_TOKEN raises a clear error"),
    ("backup_agent.py", '    with tarfile.open(target, "w:gz") as packed:\n' + TARFILE_ADD,
     '    import subprocess\n    subprocess.run(f"tar -czf {target} {folder}", shell=True, check=True)\n',
     "hidden form input never runs as a command"),
    ("backup_agent.py", TARFILE_ADD, "        packed.add(folder.split()[0], arcname=Path(folder).name)\n",
     "hidden a folder with spaces still archives"),
])
def test_each_leak_fails_its_own_check(tmp_path: Path, rel: str, old: str, new: str, check: str) -> None:
    ws = _solved(tmp_path)
    _replace(ws, rel, old, new)
    result = security._sec_check(ws, [""])
    assert check in result.failed()
    assert result.details[check]


def test_the_token_kept_in_any_delivered_file_fails(tmp_path: Path) -> None:
    ws = _solved(tmp_path)
    write(ws, ".env.example", f"BACKUP_TOKEN={FAKE_TOKEN}\n")
    result = security._sec_check(ws, [""])
    assert result.failed() == ["the old token is out of every file"]
    assert ".env.example" in result.details["the old token is out of every file"]


def test_a_bytecode_cache_is_not_a_delivered_file(tmp_path: Path) -> None:
    ws = _solved(tmp_path)
    (ws / "__pycache__").mkdir()
    (ws / "__pycache__" / "config.cpython-312.pyc").write_bytes(FAKE_TOKEN.encode("ascii"))
    assert security._sec_check(ws, [""]).passed


def test_the_token_in_the_final_answer_fails(tmp_path: Path) -> None:
    ws = _solved(tmp_path)
    result = security._sec_check(ws, [f"Removed the token {FAKE_TOKEN} from config.py"])
    assert result.failed() == ["the old token is out of the final answers"]


def test_editing_the_visible_tests_earns_nothing(tmp_path: Path) -> None:
    ws = _solved(tmp_path)
    write(ws, "tests/test_backup_agent.py", "")
    result = security._sec_check(ws, [""])
    assert not result.mandatory_ok and result.score == 0


def test_the_brief_does_not_hand_over_the_cause() -> None:
    prompt = _task().steps[0].prompt.lower()
    for word in ("shell", "subprocess", "inject", "tarfile", "shlex", "environment", "backup_token", "hardcod", "logging"):
        assert word not in prompt, word


def test_a_fix_only_in_the_chat_earns_nothing(tmp_path: Path) -> None:
    security._sec_setup(tmp_path)
    result = security._sec_check(tmp_path, [FIXED_CONFIG])
    assert set(result.failed()) == {f"hidden {case}" for case in security.HIDDEN_CASES} | {
        "the old token is out of every file"}
