"""#214: the archery game brief. Basic checks pass any playable self-contained game; the judge plays it (#213)."""

from __future__ import annotations

from pathlib import Path

import pytest

from mengine_bench import bundle_judge, catalog, visual
from mengine_bench.core import CheckResult
from mengine_bench.candidates import archery

TASK = next(task for task in catalog.candidate_tasks() if task.id == "web-archery-game")
LIVE = pytest.mark.skipif(visual.find_browser() is None, reason="no Chromium-family browser on PATH")


@pytest.fixture(autouse=True)
def _scripted_play(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch) -> None:
    """Hermetic by default: the basic play reads a rising score; only the scripted-play tests open a browser."""
    if "scripted_basic_play" not in request.node.name:
        monkeypatch.setattr(archery, "basic_play_scores", lambda page: [0, 0, 10])


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


def test_a_score_that_never_rises_fails_only_the_score_check(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(archery, "basic_play_scores", lambda page: [0, 0, 0, None])
    result = TASK.check(_solved(tmp_path), ["done"])
    assert result.failed() == [archery.SCORE_CHECK]
    assert result.details[archery.SCORE_CHECK] == "expected 'a score that rises after a few shots', received [0, 0, 0, None]"


def test_without_a_browser_the_basic_play_is_a_note_never_a_lost_point(tmp_path: Path,
                                                                        monkeypatch: pytest.MonkeyPatch) -> None:
    def no_browser(page: Path) -> list[int | None]:
        raise archery.CdpError(visual.NO_BROWSER)

    monkeypatch.setattr(archery, "basic_play_scores", no_browser)
    result = TASK.check(_solved(tmp_path), ["done"])
    assert result.passed and archery.SCORE_CHECK not in dict(result.checks)
    assert result.notes == [f"basic play not run: {visual.NO_BROWSER}"]


@pytest.mark.parametrize("reads,rose", [
    ([0, 0, 10], True), ([None, 0, 50, 0, 0], True), ([0, 0, 0], False), ([None, None], False), ([], False),
    ([40, 40, 0, 10], False),
])
def test_a_rise_is_a_score_above_the_first_one_read(reads: list[int | None], rose: bool) -> None:
    # A restart drops to 0 after an earlier rise and keeps it; a run that only restarts from a high title value does not.
    assert archery.score_rose(reads) is rose


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


@LIVE
@pytest.mark.parametrize("change,rises", [(None, True), ("b.hit = true; score += 10;", False)])
def test_a_scripted_basic_play_raises_the_gold_score_and_not_a_frozen_one(tmp_path: Path, change: str | None,
                                                                          rises: bool) -> None:
    html = archery.GAME_REFERENCE
    if change:
        assert change in html
        html = html.replace(change, "b.hit = true;")
    reads = archery.basic_play_scores(_solved(tmp_path, html) / archery.PAGE)
    assert archery.score_rose(reads) is rises, reads
    assert reads[0] == 0, "the score is read from the canvas text the game draws"


@LIVE
def test_the_reference_runs_and_draws_in_a_browser(tmp_path: Path) -> None:
    result = CheckResult()
    visual.add_page_checks(result, _solved(tmp_path) / archery.PAGE)
    assert result.checks == [(visual.SCRIPT_ERROR_CHECK, True), (visual.DRAWS_CHECK, True)], result.notes


def test_the_judge_has_its_reference_page() -> None:
    # The Opus 5.5 xhigh probe's page, rendered at 8 s (CONTRIBUTING.md); a vote copies it next to the frames.
    [reference] = bundle_judge._reference_images(TASK.id).values()
    assert reference.stat().st_size > 10_000
