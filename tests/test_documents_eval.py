"""#124: doc-lab-pdf grades a per-marker history in the first report's units and what got worse."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.tasks import documents

TASK = next(task for task in catalog.all_tasks() if task.id == "doc-lab-pdf")
GOOD = {"history": {"glucose": {"2026-02-10": 92, "2026-08-18": 109.9},
                    "LDL": {"2026-02-10": 118, "2026-08-18": 143.1},
                    "creatinine": {"2026-02-10": 0.95, "2026-08-18": 0.86},
                    "HbA1c": {"2026-02-10": 5.4, "2026-08-18": 5.54}},
        "worse": ["glucose", "LDL"]}


def _deliver(ws: Path, payload: object) -> None:
    (ws / "result.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _workspace(tmp_path: Path) -> Path:
    TASK.setup(tmp_path)
    return tmp_path


def _with(marker: str, day: str, value: object) -> dict[str, object]:
    history = {name: dict(series) for name, series in GOOD["history"].items()}
    history[marker][day] = value
    return {**GOOD, "history": history}


def test_the_reference_passes_and_the_untouched_folder_fails(tmp_path: Path) -> None:
    (tmp_path / "bare").mkdir()
    (tmp_path / "solved").mkdir()
    TASK.setup(tmp_path / "bare")
    bare = TASK.check(tmp_path / "bare", [""])
    assert not bare.passed and bare.score == 0
    TASK.setup(tmp_path / "solved")
    result = TASK.check(tmp_path / "solved", TASK.reference(tmp_path / "solved"))
    assert result.passed, result.failed()


def test_the_pdfs_are_well_formed_and_readable_raw(tmp_path: Path) -> None:
    ws = _workspace(tmp_path)
    for name in ("laudo_alfa.pdf", "resultado_beta.pdf"):
        raw = (ws / "exams" / name).read_bytes()
        assert raw.startswith(b"%PDF-1.4") and raw.rstrip().endswith(b"%%EOF")
        start = int(re.search(rb"startxref\n(\d+)", raw)[1])
        assert raw[start:start + 4] == b"xref"
        offsets = [int(found) for found in re.findall(rb"(\d{10}) 00000 n", raw)]
        assert [raw[offset:].split(b" ", 1)[0] for offset in offsets] == [b"1", b"2", b"3", b"4", b"5"]
    alfa = (ws / "exams" / "laudo_alfa.pdf").read_bytes()
    beta = (ws / "exams" / "resultado_beta.pdf").read_bytes()
    assert b"(GLICOSE EM JEJUM)" in alfa and b"(Resultado: 5,4 %)" in alfa
    assert b"(mmol/mol)" in beta and b"(\xb5mol/L)" in beta and b"(Coleta: 18/08/2026" in beta


@pytest.mark.skipif(shutil.which("pdftotext") is None, reason="pdftotext not installed")
def test_pdftotext_reads_the_values(tmp_path: Path) -> None:
    ws = _workspace(tmp_path)
    text = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", str(ws / "exams" / "resultado_beta.pdf"), "-"],
                          capture_output=True, check=True).stdout.decode("utf-8")
    assert re.search(r"Glicose em jejum\s+6,1\s+mmol/L", text)
    assert "\u00b5mol/L" in text and "Diagn\u00f3sticos" in text


@pytest.mark.parametrize("payload", [
    GOOD,
    {"history": {"Glicose em jejum (mg/dL)": {"10/02/2026": "92 mg/dL", "18/08/2026": "109,8 mg/dL"},
                 "Colesterol LDL": {"10/02/2026": {"value": 118, "unit": "mg/dL"}, "18/08/2026": {"value": 143.08, "unit": "mg/dL"}},
                 "Creatinina": {"2026-02-10": "0,95", "2026-08-18": "0,859"},
                 "Hemoglobina glicada (HbA1c)": {"2026-02-10": "5,4 %", "2026-08-18": "5,5 %"}},
     "worse": ["Glicose em jejum", "Colesterol LDL"]},
    {**GOOD, "worse": {"fasting glucose": "109.9 > 99", "LDL cholesterol": "143 >= 130"}},
])
def test_every_valid_answer_passes(tmp_path: Path, payload: dict[str, object]) -> None:
    ws = _workspace(tmp_path)
    _deliver(ws, payload)
    result = TASK.check(ws, [""])
    assert result.passed, (result.failed(), result.details)


@pytest.mark.parametrize(("payload", "check"), [
    (_with("glucose", "2026-08-18", 6.1), "glucose history"),
    (_with("LDL", "2026-08-18", 3.70), "ldl history"),
    (_with("LDL", "2026-08-18", 128.0), "ldl history"),
    (_with("creatinine", "2026-08-18", 76), "creatinine history"),
    (_with("creatinine", "2026-08-18", 8.6), "creatinine history"),
    (_with("HbA1c", "2026-08-18", 37), "hba1c history"),
    (_with("HbA1c", "2026-08-18", 3.39), "hba1c history"),
    (_with("glucose", "2026-08-19", 109.9), "glucose history"),
    ({**GOOD, "worse": ["glucose"]}, "flags what got worse and left the range"),
    ({**GOOD, "worse": ["glucose", "LDL", "HbA1c"]}, "leaves out what stayed in range"),
    # #164: a marker the reports never had used to drop out silently; impossible dates used to crash the grader.
    ({**GOOD, "worse": ["glucose", "LDL", "Troponin"]}, "leaves out what stayed in range"),
    (_with("glucose", "2026-99-01", 100), "glucose history"),
    (_with("glucose", "31/02/2026", 100), "glucose history"),
])
def test_each_check_fails_on_its_own_wrong_answer(tmp_path: Path, payload: dict[str, object], check: str) -> None:
    ws = _workspace(tmp_path)
    _deliver(ws, payload)
    result = TASK.check(ws, [""])
    assert result.failed() == [check], result.failed()
    assert check in result.details


def test_the_brief_does_not_hand_over_the_conversions() -> None:
    prompt = TASK.steps[0].prompt.lower()
    for word in ("18.0", "38.67", "88.4", "10.929", "2.15", "mmol", "mg/dl", "glicose", "ldl", "hba1c", "convert"):
        assert word not in prompt, word
    assert all(key in prompt for key in ("history", "worse"))


def test_a_correct_answer_only_in_the_chat_earns_nothing(tmp_path: Path) -> None:
    ws = _workspace(tmp_path)
    result = TASK.check(ws, [json.dumps(GOOD)])
    assert not result.passed and result.score == 0
    assert documents.LAB_WORSE == {"glucose", "ldl"}
