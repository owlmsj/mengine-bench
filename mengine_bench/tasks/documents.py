"""Documents task: index two lab exam PDFs into one history per marker (#124).

Mirrors indexing a patient's lab reports. The second lab reports in SI units, so the
agent must know the conversions; the brief never states them. One marker rises but stays
in range, so "got worse" alone is not the answer. The PDFs come from a minimal stdlib
writer (uncompressed streams, Helvetica, WinAnsi) so any extractor, or a raw read, works.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from datetime import date
from pathlib import Path

from mengine_bench.core import (
    CheckResult,
    EvalTask,
    Step,
    WROTE_RESULT,
    checkpoints,
    number,
    result_json,
    saw,
)

LAB_FIRST_DATE = date(2026, 2, 10)
LAB_SECOND_DATE = date(2026, 8, 18)
LAB_TOLERANCE = 0.015
# Marker -> (pattern a result key must match, first report value in mg/dL or %, second report value in SI).
# HbA1c comes first: "hemoglobina glicada" also matches the glucose pattern.
LAB_MARKERS: dict[str, tuple[str, float, float]] = {
    "hba1c": (r"a1c|glicad|glycat|hemoglob", 5.4, 37.0),
    "glucose": (r"glic|gluc", 92.0, 6.1),
    "ldl": (r"ldl", 118.0, 3.70),
    "creatinine": (r"creat", 0.95, 76.0),
}
LAB_WORSE = frozenset({"glucose", "ldl"})


def _lab_to_first_unit(marker: str, si: float) -> float:
    if marker == "glucose":
        return si * 18.016
    if marker == "ldl":
        return si * 38.67
    if marker == "creatinine":
        return si / 88.42
    return si / 10.929 + 2.15


def _lab_expected() -> dict[str, dict[date, float]]:
    return {marker: {LAB_FIRST_DATE: first, LAB_SECOND_DATE: _lab_to_first_unit(marker, si)}
            for marker, (_, first, si) in LAB_MARKERS.items()}


# ------------------------------------------------------------ PDF writer --


def _pdf_escape(text: str) -> bytes:
    raw = text.encode("cp1252")
    return raw.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def lab_pdf_bytes(lines: Sequence[tuple[float, float, int, str]]) -> bytes:
    """One A4 page; each line is (x, y, font size, text). Bold-free Helvetica keeps it a base-14 font."""
    stream = b"".join(b"BT /F1 %d Tf %.1f %.1f Td (" % (size, x, y) + _pdf_escape(text) + b") Tj ET\n"
                      for x, y, size, text in lines)
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"endstream",
    ]
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for index, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % index + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    out += b"".join(b"%010d 00000 n \n" % offset for offset in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, xref)
    return bytes(out)


def _br(value: float, digits: int) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


def _lab_first_report() -> list[tuple[float, float, int, str]]:
    rows = [
        ("GLICOSE EM JEJUM", f"{_br(92, 0)} mg/dL", "70 a 99 mg/dL"),
        ("COLESTEROL LDL", f"{_br(118, 0)} mg/dL", "Desej\u00e1vel: inferior a 130 mg/dL"),
        ("CREATININA", f"{_br(0.95, 2)} mg/dL", "0,70 a 1,30 mg/dL"),
        ("HEMOGLOBINA GLICADA (HbA1c)", f"{_br(5.4, 1)} %", "4,0 a 5,6 %"),
    ]
    lines = [(50.0, 790.0, 16, "Laborat\u00f3rio Alfa de An\u00e1lises Cl\u00ednicas"),
             (50.0, 770.0, 10, "Rua Exemplo, 100 - Campinas/SP"),
             (50.0, 740.0, 11, "Paciente: Teste Sint\u00e9tico 0042    Sexo: F    Nascimento: 01/01/1980"),
             (50.0, 724.0, 11, f"Data da coleta: {LAB_FIRST_DATE:%d/%m/%Y}    Pedido: 2026-0217"),
             (50.0, 690.0, 12, "RESULTADOS")]
    y = 664.0
    for name, value, reference in rows:
        lines += [(50.0, y, 11, name), (70.0, y - 16, 11, f"Resultado: {value}"),
                  (70.0, y - 32, 10, f"Valor de refer\u00eancia: {reference}")]
        y -= 60
    lines.append((50.0, 120.0, 9, "Liberado eletronicamente. Respons\u00e1vel t\u00e9cnico: CRF-SP 00000."))
    return lines


def _lab_second_report() -> list[tuple[float, float, int, str]]:
    rows = [
        ("Glicose em jejum", _br(6.1, 1), "mmol/L", "3,9 - 5,5"),
        ("Colesterol LDL", _br(3.70, 2), "mmol/L", "< 3,4"),
        ("Creatinina", _br(76, 0), "\u00b5mol/L", "62 - 115"),
        ("Hemoglobina glicada (HbA1c)", _br(37, 0), "mmol/mol", "20 - 38"),
    ]
    lines = [(50.0, 790.0, 16, "Beta Diagn\u00f3sticos"),
             (50.0, 770.0, 10, "Unidade Porto Alegre - Laudo laboratorial"),
             (50.0, 740.0, 11, "Nome: TESTE SINT\u00c9TICO 0042"),
             (50.0, 724.0, 11, f"Coleta: {LAB_SECOND_DATE:%d/%m/%Y} 07:40    Emiss\u00e3o: 19/08/2026"),
             (50.0, 690.0, 11, "Exame"), (260.0, 690.0, 11, "Resultado"), (350.0, 690.0, 11, "Unidade"),
             (440.0, 690.0, 11, "Valores de refer\u00eancia")]
    y = 668.0
    for name, value, unit, reference in rows:
        lines += [(50.0, y, 11, name), (260.0, y, 11, value), (350.0, y, 11, unit), (440.0, y, 11, reference)]
        y -= 22
    lines.append((50.0, 120.0, 9, "M\u00e9todo: enzim\u00e1tico colorim\u00e9trico; HbA1c por HPLC (IFCC)."))
    return lines


def _lab_setup(ws: Path) -> None:
    folder = ws / "exams"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "laudo_alfa.pdf").write_bytes(lab_pdf_bytes(_lab_first_report()))
    (folder / "resultado_beta.pdf").write_bytes(lab_pdf_bytes(_lab_second_report()))


# ----------------------------------------------------------------- check --


def _lab_marker_of(name: str) -> str | None:
    return next((marker for marker, (pattern, _, _) in LAB_MARKERS.items() if re.search(pattern, name, re.IGNORECASE)), None)


def _lab_date_of(key: str) -> date | str | None:
    """The date a history key names, the key itself when its date is impossible (#164), None when it names none."""
    iso = re.search(r"(\d{4})-(\d{2})-(\d{2})", key)
    # Brazilian reports write day first.
    local = re.search(r"(\d{1,2})[/.](\d{1,2})[/.](\d{4})", key)
    parts = (iso[1], iso[2], iso[3]) if iso else (local[3], local[2], local[1]) if local else None
    if parts is None:
        return None
    try:
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        return key


def _lab_value_of(value: object) -> float | None:
    if isinstance(value, dict):
        value = value.get("value", value.get("valor"))
    # #124: core.number reads "0,859" as 859 (a thousands comma); no marker here reaches a thousand,
    # so a lone comma is the Brazilian decimal the reports themselves use.
    if isinstance(value, str) and "." not in value and re.search(r"\d,\d", value):
        value = value.replace(",", ".")
    return number(value)


def _lab_series(got: Mapping[str, object]) -> dict[str, dict[date | str, float | None]]:
    history = got.get("history")
    if not isinstance(history, dict):
        return {}
    found: dict[str, dict[date | str, float | None]] = {}
    for name, series in history.items():
        marker = _lab_marker_of(str(name))
        if marker is None or not isinstance(series, dict):
            continue
        found[marker] = {day: _lab_value_of(value) for key, value in series.items() if (day := _lab_date_of(str(key)))}
    return found


def _lab_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    expected = _lab_expected()
    series = _lab_series(result_json(ws))
    for marker, want in expected.items():
        got = series.get(marker, {})
        wrong = [day for day, value in want.items()
                 if got.get(day) is None or abs(float(got[day] or 0) - value) > value * LAB_TOLERANCE]
        result.add(f"{marker} history", not wrong and len(got) == len(want),
                   saw({str(day): value for day, value in got.items()}, {str(day): round(value, 2) for day, value in want.items()}))
    worse = result_json(ws).get("worse")
    names = list(worse) if isinstance(worse, (list, dict)) else []
    flagged = {_lab_marker_of(str(name)) for name in names}
    result.add("flags what got worse and left the range", LAB_WORSE <= flagged, saw(worse, sorted(LAB_WORSE)))
    # #124: HbA1c rose but stays in range; an empty list flags nothing wrong but finds nothing either.
    # #164: a name that is none of the reports' markers (None here) is an invented flag, not a dropped one.
    result.add("leaves out what stayed in range", bool(flagged - {None}) and not flagged - LAB_WORSE,
               saw(worse, sorted(LAB_WORSE)))
    return result


def _lab_reference(ws: Path) -> list[str]:
    names = {"glucose": "Glicose em jejum (mg/dL)", "ldl": "Colesterol LDL (mg/dL)",
             "creatinine": "Creatinina (mg/dL)", "hba1c": "Hemoglobina glicada HbA1c (%)"}
    history = {names[marker]: {day.isoformat(): round(value, 2) for day, value in series.items()}
               for marker, series in _lab_expected().items()}
    (ws / "result.json").write_text(json.dumps({"history": history, "worse": [names["glucose"], names["ldl"]]},
                                               ensure_ascii=False), encoding="utf-8")
    return ["done"]


TASKS = [
    EvalTask(
        id="doc-lab-pdf", category="documents",
        provenance="Indexing a patient's lab exam PDFs from two labs into one history per marker",
        summary="Turn two lab exam PDFs from different labs into one comparable history per marker.",
        setup=_lab_setup, check=_lab_check, reference=_lab_reference, timeout_s=60,
        checkpoints=checkpoints(("opened the exams", r"exams|\.pdf"),
                                ("extracted the text", r"pdftotext|pypdf|PyPDF2|fitz|pdfplumber|pdfminer|Tj\b|stream"),
                                WROTE_RESULT),
        steps=(Step("A patient brought lab exam PDFs from two different labs, months apart; they are in {WS}/exams. "
                    "Build one history per marker, every value in the units of the first report, and say what got worse. "
                    "Record in {WS}/result.json: history (marker -> {date: value}) and worse (a list of the markers that "
                    "got worse and are now outside the first report's reference range)."),),
    ),
]
