"""#124: the web-research eval grades delivered files offline, accepts every valid writing and fails wrong work."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.core import write
from mengine_bench.tasks import webresearch as web
from mengine_bench.tasks.webresearch import WEB_PLANS, WEB_TOP3, web_reference_rows, web_rubric_score

TASK = next(task for task in catalog.all_tasks() if task.id == "web-plan-ranking")
CHECK_NAMES = ["all six plans recorded", "launch dates", "inflation before and after", "months lasted",
               "scores follow the rubric", "top 3", "every plan has a source", "dossier"]


def _solved(ws: Path) -> Path:
    ws.mkdir(parents=True, exist_ok=True)
    TASK.setup(ws)
    TASK.reference(ws)
    return ws


def _rewrite(ws: Path, change: object) -> None:
    got = json.loads((ws / "result.json").read_text(encoding="utf-8"))
    change(got)
    write(ws, "result.json", json.dumps(got))


def _row(got: dict[str, object], name: str) -> dict[str, object]:
    return next(row for row in got["plans"] if row["plan"] == name)


def test_the_reference_passes_and_the_untouched_folder_fails(tmp_path: Path) -> None:
    result = TASK.check(_solved(tmp_path / "solved"), ["done"])
    assert result.passed, result.details
    (tmp_path / "bare").mkdir()
    TASK.setup(tmp_path / "bare")
    bare = TASK.check(tmp_path / "bare", [""])
    assert bare.score == 0.0 and [name for name, _ in bare.checks] == CHECK_NAMES


def test_another_valid_route_and_writing_passes(tmp_path: Path) -> None:
    ws = _solved(tmp_path)
    names = {"Cruzado": "Plano Cruzado", "Bresser": "Plano Bresser", "Verao": "Plano Verão", "Collor I": "plano collor 1",
             "Collor II": "Collor II (1991)", "Real": "Real Plan"}
    dates = {"Cruzado": "27/02/1986", "Bresser": "June 12, 1987", "Verao": "16 de janeiro de 1989",
             "Collor I": "1990-03-15", "Collor II": "1991-02-01", "Real": "1994-07-01"}
    months = {"Collor I": 11, "Collor II": 41, "Real": 392}

    def other_route(got: dict[str, object]) -> None:
        for row in got["plans"]:
            name = row["plan"]
            # IPCA as fractions in Brazilian writing; the rubric's ratio does not change.
            before, after = row["ipca_before"] / 100, row["ipca_after"] / 100
            row["months_lasted"] = months.get(name, row["months_lasted"])
            row["score"] = f"{100 * web_rubric_score(before, after, row['months_lasted']):.1f}%"
            row["ipca_before"], row["ipca_after"] = f"{before:.4f}".replace(".", ","), f"{after:.4f}".replace(".", ",")
            row["plan"], row["launch_date"] = names[name], dates[name]
            row["sources"] = [f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"]
        got["top3"] = ["Plano Real", "Plano Collor I", "plano collor ii"]

    _rewrite(ws, other_route)
    result = TASK.check(ws, [""])
    assert result.passed, result.details


def _drop_plan(got: dict[str, object]) -> None:
    got["plans"] = [row for row in got["plans"] if row["plan"] != "Verao"]


def _late_date(got: dict[str, object]) -> None:
    _row(got, "Bresser")["launch_date"] = "1987-07-30"


def _wrong_ipca(got: dict[str, object]) -> None:
    row = _row(got, "Collor I")  # IGP-DI style 1991 figure instead of the IPCA
    row["ipca_after"] = 496.0
    row["score"] = round(web_rubric_score(row["ipca_before"], 496.0, row["months_lasted"]), 3)


def _wrong_months(got: dict[str, object]) -> None:
    row = _row(got, "Collor II")  # counted to the cruzeiro real of 1993, not to the next plan
    row["months_lasted"] = 30
    row["score"] = round(web_rubric_score(row["ipca_before"], row["ipca_after"], 30), 3)


def _wrong_score(got: dict[str, object]) -> None:
    _row(got, "Verao")["score"] = 0.3


def _wrong_top3(got: dict[str, object]) -> None:
    got["top3"] = ["Real", "Collor II", "Collor I"]


def _no_source(got: dict[str, object]) -> None:
    _row(got, "Cruzado")["sources"] = ["Wikipedia"]


@pytest.mark.parametrize(("check", "break_it"), [
    ("all six plans recorded", _drop_plan), ("launch dates", _late_date), ("inflation before and after", _wrong_ipca),
    ("months lasted", _wrong_months), ("scores follow the rubric", _wrong_score), ("top 3", _wrong_top3),
    ("every plan has a source", _no_source),
])
def test_each_check_fails_on_its_own_wrong_answer(tmp_path: Path, check: str, break_it: object) -> None:
    ws = _solved(tmp_path)
    _rewrite(ws, break_it)
    result = TASK.check(ws, [""])
    assert check in result.failed() and check in result.details
    # A missing plan also takes its dates, rates and score with it; every other break hits one check only.
    if break_it is not _drop_plan:
        assert result.failed() == [check]


@pytest.mark.parametrize("dossier", [None, "Real won. https://a.example https://b.example https://c.example",
                                     "Real, Collor and Cruzado plans. " * 30])
def test_a_missing_thin_or_unsourced_dossier_fails(tmp_path: Path, dossier: str | None) -> None:
    ws = _solved(tmp_path)
    (ws / web.DOSSIER_FILE).unlink()
    if dossier is not None:
        write(ws, web.DOSSIER_FILE, dossier)
    assert TASK.check(ws, [""]).failed() == ["dossier"]


def test_a_bare_collor_is_not_a_plan_name() -> None:
    assert web._web_plan_named("Collor") is None
    assert web._web_plan_named("Plano Verão").name == "Verao"


def test_the_brief_asks_for_the_web_but_hands_over_no_answer() -> None:
    prompt = TASK.steps[0].prompt
    assert "web" in prompt and "web" in TASK.needs and TASK.timeout_s == 300
    for leaked in ("Collor", "Cruzado", "IPCA", "1994", "1993", "2477", "0.7", "60 months", "URV"):
        assert leaked not in prompt, leaked


def test_a_correct_answer_in_the_chat_alone_earns_nothing(tmp_path: Path) -> None:
    TASK.setup(tmp_path)
    answer = json.dumps({"plans": web_reference_rows(), "top3": list(WEB_TOP3)})
    assert TASK.check(tmp_path, [answer]).score == 0.0


def test_the_canonical_top3_holds_across_every_accepted_tolerance() -> None:
    # Every IPCA at its accepted extremes and every months count the checks accept: the ranking must not move,
    # or the "top 3" check would fail an agent whose numbers all pass (#124).
    extremes: dict[str, list[tuple[float, float, float]]] = {}
    for plan in WEB_PLANS:
        year = plan.launches[0].year
        tol_b = web.WEB_IPCA_WIDE_TOL.get(year - 1, web.WEB_IPCA_TOL)
        tol_a = web.WEB_IPCA_WIDE_TOL.get(year + 1, web.WEB_IPCA_TOL)
        befores = [web.WEB_IPCA_ANNUAL[year - 1] * (1 + s * tol_b) for s in (-1, 1)]
        afters = [web.WEB_IPCA_ANNUAL[year + 1] * (1 + s * tol_a) for s in (-1, 1)]
        wants = web.web_expected_months(plan)
        months = [59, 60] if wants == {60} else [min(wants) - 1, max(wants) + 1]
        extremes[plan.name] = list(itertools.product(befores, afters, months))
    worst: dict[str, tuple[float, float]] = {}
    for name, options in extremes.items():
        scores = [web_rubric_score(*option) for option in options]
        worst[name] = (min(scores), max(scores))
    ranked = [name for name in WEB_TOP3]
    for better, worse in zip(ranked, ranked[1:]):
        assert worst[better][0] > worst[worse][1], (better, worse, worst)
    rest = [name for name in worst if name not in WEB_TOP3]
    assert worst[WEB_TOP3[-1]][0] > max(worst[name][1] for name in rest), worst
