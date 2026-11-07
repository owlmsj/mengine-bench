"""#214: the archery game brief. Basic checks pass any playable self-contained game; the judge plays it (#213)."""

from __future__ import annotations

from pathlib import Path

import pytest

from mengine_bench import bundle_judge, catalog, visual
from mengine_bench.core import CheckResult
from mengine_bench.candidates import archery

TASK = next(task for task in catalog.candidate_tasks() if task.id == "web-archery-game")


def test_it_waits_outside_the_catalog_for_a_release_train() -> None:
    assert TASK.id not in {task.id for task in catalog.all_tasks()} and catalog.task_by_id(TASK.id) is TASK


def _solved(tmp_path: Path, html: str | None = None) -> Path:
    TASK.reference(tmp_path)
    if html is not None:
        (tmp_path / archery.PAGE).write_text(html, encoding="utf-8")
    return tmp_path


def _failed(tmp_path: Path, html: str) -> list[str]:
    return TASK.check(_solved(tmp_path, html), ["done"]).failed()


def test_the_reference_passes_and_an_untouched_workspace_fails(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    TASK.setup(empty)
    assert not TASK.check(empty, [""]).passed
    assert TASK.check(_solved(tmp_path / "solved"), ["done"]).passed


def test_a_stub_page_fails_the_gate(tmp_path: Path) -> None:
    stub = "<canvas></canvas><script>new AudioContext(); onpointerdown = onpointerup = () => 0; score = 0;</script>"
    result = TASK.check(_solved(tmp_path, stub), ["done"])
    assert not result.mandatory_ok and result.partial_score == 0.5, "a stub cut at the limit earns half at most"


@pytest.mark.parametrize("old,new,check", [
    ('"pointerdown"', '"keydown"', archery.MOUSE_CHECK),
    ('"pointerup"', '"keyup"', archery.MOUSE_CHECK),
    ("new AudioContext()", "({})", archery.SOUND_CHECK),
    ("<title>Balloon Bow</title>", '<title>Balloon Bow</title><script src="game.js"></script>', archery.SELF_CONTAINED_CHECK),
    ("<title>Balloon Bow</title>", '<title>Balloon Bow</title><script src="https://cdn.example.org/p.js"></script>',
     archery.SELF_CONTAINED_CHECK),
    ("audio = audio || new AudioContext();", 'new Audio("pop.wav"); audio = audio || new AudioContext();',
     archery.SELF_CONTAINED_CHECK),
])
def test_each_basic_check_fails_alone_when_its_part_is_missing(tmp_path: Path, old: str, new: str, check: str) -> None:
    html = archery.GAME_REFERENCE
    assert old in html
    assert _failed(tmp_path, html.replace(old, new)) == [check]


def test_a_page_without_any_score_fails_the_score_check(tmp_path: Path) -> None:
    html = archery.GAME_REFERENCE.replace("score", "tally").replace("Score", "Tally").replace(" points", "")
    assert _failed(tmp_path, html) == [archery.SCORE_CHECK]


@pytest.mark.parametrize("extra", [
    '<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P" rel="stylesheet">',
    '<audio src="data:audio/wav;base64,UklGRg=="></audio>',
    "<script>const shot = new Image(); shot.src = canvas.toDataURL();</script>",
])
def test_fonts_inline_media_and_variables_stay_self_contained(tmp_path: Path, extra: str) -> None:
    html = archery.GAME_REFERENCE.replace("</head>", extra + "</head>")
    assert _failed(tmp_path, html) == []


def test_the_judge_plays_it_and_the_brief_names_what_it_tries() -> None:
    assert TASK.render_target == archery.PAGE and TASK.judge_play
    prompt = TASK.steps[0].prompt
    for part in ("mouse", "pulling the bow back", "balloons", "score", "start", "lose", "sound"):
        assert part in prompt, part


@pytest.mark.skipif(visual.find_browser() is None, reason="no Chromium-family browser on PATH")
def test_the_reference_runs_and_draws_in_a_browser(tmp_path: Path) -> None:
    result = CheckResult()
    visual.add_page_checks(result, _solved(tmp_path) / archery.PAGE)
    assert result.checks == [(visual.SCRIPT_ERROR_CHECK, True), (visual.DRAWS_CHECK, True)], result.notes


def test_the_judge_has_its_reference_page() -> None:
    # The Opus 5.5 xhigh probe's page, rendered at 8 s (CONTRIBUTING.md); a vote copies it next to the frames.
    [reference] = bundle_judge._reference_images(TASK.id).values()
    assert reference.stat().st_size > 10_000
