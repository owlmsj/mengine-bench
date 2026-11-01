"""#99: the word universe eval. Any valid view and data shape passes; each of the site's traps costs the check it touches."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import pytest

from mengine_bench import catalog, visual
from mengine_bench.core import CheckResult
from mengine_bench.runner import task_run
from mengine_bench.tasks import words

TASK = next(task for task in catalog.all_tasks() if task.id == "web-word-universe")
WORDS_CHECK = "collected exactly the site's words"
SAMPLE_CHECK = "relations of a sample of words"
NOISE_CHECK = "no relation from a sidebar or a footer"
RESULT_CHECK = "result.json has the right words, relations and most_connected"
SEARCH_CHECK = "the page has a search field"
QUERY_CHECK = words.QUERY_CHECK
GOLD = words._relations()
GOLD_PAIRS = len(words._pairs(GOLD))


# --- opening a page with a query ---


def _fake_browser(tmp_path: Path, stdout: str, exit_code: int = 0) -> list[str]:
    script = tmp_path / "browser.py"
    script.write_text(f"import sys\nsys.stdout.write({stdout!r} + sys.argv[-1])\nsys.exit({exit_code})\n", encoding="utf-8")
    return [sys.executable, "-I", str(script)]


def test_the_dump_reads_the_dom_of_the_page_with_its_query(tmp_path: Path) -> None:
    page = tmp_path / "index.html"
    page.write_text("x", encoding="utf-8")
    status, dom = visual.dump_page_dom(page, "word=pa%C3%ADs", _fake_browser(tmp_path, "<p>dom</p>"))
    assert status == visual.RENDERED and dom.startswith("<p>dom</p>file:") and dom.endswith("index.html?word=pa%C3%ADs")


def test_a_browser_that_fails_is_a_status_and_never_a_crash(tmp_path: Path) -> None:
    page = tmp_path / "index.html"
    page.write_text("x", encoding="utf-8")
    assert visual.is_render_failure(visual.dump_page_dom(page, "word=a", _fake_browser(tmp_path, "", 3))[0])
    assert visual.is_render_failure(visual.dump_page_dom(page, "word=a", [str(tmp_path / "missing.exe")])[0])


def test_no_browser_is_reported_as_such(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(visual, "find_browser", lambda: None)
    assert visual.dump_page_dom(tmp_path / "index.html", "word=a") == (visual.NO_BROWSER, "")


# --- the site ---


def test_the_site_is_the_same_every_time_and_its_size_is_as_briefed(tmp_path: Path) -> None:
    first, second = tmp_path / "a", tmp_path / "b"
    first.mkdir()
    second.mkdir()
    words._word_setup(first)
    words._word_setup(second)
    pages = {path.name: path.read_bytes() for path in (first / "site").iterdir()}
    assert pages == {path.name: path.read_bytes() for path in (second / "site").iterdir()}
    assert len(words.WORDS) == 250 == sum(len(group.split()) for group in words.THEMES.values()) and len(words.THEMES) == 10
    assert len(pages) == len(words.WORDS) + len(words.VARIANTS) + len(words.NON_WORD_PAGES) + 1


def test_a_person_reads_the_gold_from_the_pages_alone_and_needs_the_links_to_do_it(tmp_path: Path) -> None:
    words._word_setup(tmp_path)
    home = (tmp_path / "site" / "index.html").read_text(encoding="utf-8")
    assert home.split("<main>")[1].split("</main>")[0].count("<li>") == 30
    assert {word: set(others) for word, others in words._crawl(tmp_path / "site").items()} == GOLD


def test_pais_and_país_are_two_pages(tmp_path: Path) -> None:
    words._word_setup(tmp_path)
    assert "<h1>pais</h1>" in (tmp_path / "site" / words.FILES["pais"]).read_text(encoding="utf-8")
    assert "<h1>país</h1>" in (tmp_path / "site" / words.FILES["país"]).read_text(encoding="utf-8")
    assert not GOLD["pais"] & GOLD["país"]


def test_the_most_connected_is_a_tie_by_construction() -> None:
    top = max(map(len, GOLD.values()))
    assert {word for word, others in GOLD.items() if len(others) == top} == set(words.HUBS)


@pytest.mark.parametrize("word", list(words.QUERY_DECOYS))
def test_a_decoy_is_far_from_its_word_so_a_view_of_second_neighbours_stays_fair(word: str) -> None:
    close_by = GOLD[word] | {other for neighbour in GOLD[word] for other in GOLD[neighbour]}
    assert words.QUERY_DECOYS[word] not in close_by


# --- words.json and result.json ---


def _summary(**changed: object) -> dict[str, object]:
    return {"words": len(GOLD), "relations": GOLD_PAIRS, "most_connected": "tempo", **changed}


def _deliver(ws: Path, links: object, summary: dict[str, object] | None = None) -> None:
    (ws / "words.json").write_text(json.dumps(links, ensure_ascii=False), encoding="utf-8")
    (ws / "result.json").write_text(json.dumps(summary or _summary(), ensure_ascii=False), encoding="utf-8")


def _gold_lists() -> dict[str, list[str]]:
    return {word: sorted(others) for word, others in GOLD.items()}


def _panel_dom(query: str) -> str:
    word = unquote(query.split("=", 1)[1])
    items = "".join(f"<li>{other}</li>" for other in sorted(GOLD[word]))
    return f"<html><body><input><h2>{word}</h2><ul>{items}</ul></body></html>"


@pytest.fixture
def graded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A workspace with a good answer and a browser that shows a panel: each test spoils one thing."""
    monkeypatch.setattr(words, "dump_page_dom", lambda page, query: (visual.RENDERED, _panel_dom(query)))
    TASK.setup(tmp_path)
    (tmp_path / "universe").mkdir()
    (tmp_path / words.PAGE).write_text("<input><canvas></canvas>", encoding="utf-8")
    _deliver(tmp_path, _gold_lists())
    return tmp_path


def _check(ws: Path) -> CheckResult:
    return TASK.check(ws, [""])


def test_the_reference_passes_and_the_browser_part_runs_or_says_why_not(tmp_path: Path) -> None:
    TASK.setup(tmp_path)
    result = TASK.check(tmp_path, TASK.reference(tmp_path))
    assert result.passed, result.details
    assert QUERY_CHECK in dict(result.checks) or result.notes


def test_an_untouched_workspace_earns_nothing_and_every_check_says_why(tmp_path: Path) -> None:
    TASK.setup(tmp_path)
    result = _check(tmp_path)
    assert result.score == 0.0 and not result.passed
    assert all(result.details.get(name) for name, _ in result.checks), result.details


def test_the_good_answer_passes(graded: Path) -> None:
    assert _check(graded).passed, _check(graded).details


@pytest.mark.parametrize("shape", [
    lambda others: others,
    lambda others: {"synonyms": others[:1], "analogous": others[1:]},
    lambda others: {"theme": "x", "relations": {"synonyms": others[:1], "analogous": others[1:]}},
    lambda others: {"links": [{"word": other, "kind": "analogous"} for other in others]},
    lambda others: {other: "analogous" for other in others},
    lambda others: {"links": others, "aliases": ["saudades"], "sources": ["saudade.html"], "themes": ["corpo"]},
], ids=["list", "two keys", "nested with a text field", "rows", "word to kind", "notes beside the links"])
def test_any_plain_shape_of_an_entry_passes(graded: Path, shape) -> None:
    _deliver(graded, {word: shape(others) for word, others in _gold_lists().items()})
    assert _check(graded).passed, _check(graded).details


def test_a_list_of_rows_and_a_wrapper_pass(graded: Path) -> None:
    _deliver(graded, [{"word": word, "links": others} for word, others in _gold_lists().items()])
    assert _check(graded).passed
    _deliver(graded, {"words": _gold_lists()})
    assert _check(graded).passed


def test_case_and_spaces_do_not_matter(graded: Path) -> None:
    _deliver(graded, {f" {word.upper()} ": [other.capitalize() for other in others] for word, others in _gold_lists().items()})
    assert _check(graded).passed, _check(graded).details


def test_a_link_written_on_one_side_links_both_words(graded: Path) -> None:
    _deliver(graded, {word: [other for other in others if word < other] for word, others in _gold_lists().items()})
    assert _check(graded).passed, _check(graded).details


@pytest.mark.parametrize("extra", ["rascunho-3", "em-construção", "saudades", "sobre", "contato"])
def test_a_broken_link_a_variant_or_a_page_that_is_no_word_is_not_a_word(graded: Path, extra: str) -> None:
    for links in ({**_gold_lists(), extra: []}, {**_gold_lists(), "saudade": [*_gold_lists()["saudade"], extra]}):
        _deliver(graded, links)
        result = _check(graded)
        assert WORDS_CHECK in result.failed() and extra in result.details[WORDS_CHECK]


def test_words_only_reached_by_following_links_are_required(graded: Path) -> None:
    home = {word for group in words.THEMES.values() for word in group.split()[:3]}
    _deliver(graded, {word: sorted(GOLD[word] & home) for word in home})
    assert WORDS_CHECK in _check(graded).failed()


def test_a_relation_through_the_variant_page_belongs_to_the_word(graded: Path) -> None:
    # The site's relation links to saudade all go through saudades.html: a crawl that drops the redirect loses them.
    _deliver(graded, {word: [other for other in others if other != "saudade"]
                      for word, others in _gold_lists().items() if word != "saudade"})
    assert {WORDS_CHECK, SAMPLE_CHECK} <= set(_check(graded).failed())


def test_a_missing_relation_in_the_sample_fails_and_says_which(graded: Path) -> None:
    lost = _gold_lists()["nostalgia"][0]
    links = _gold_lists()
    links["nostalgia"].remove(lost)
    links[lost].remove("nostalgia")
    _deliver(graded, links)
    result = _check(graded)
    assert SAMPLE_CHECK in result.failed() and "nostalgia" in result.details[SAMPLE_CHECK] and lost in result.details[SAMPLE_CHECK]


@pytest.mark.parametrize("source", [next(word for word in words._day_words("saudade") if word not in GOLD["saudade"]), words.FOOTER_WORDS[0]],
                         ids=["sidebar", "footer"])
def test_a_link_from_the_sidebar_or_the_footer_is_a_false_relation(graded: Path, source: str) -> None:
    assert source not in GOLD["saudade"]
    _deliver(graded, {**_gold_lists(), "saudade": [*_gold_lists()["saudade"], source]})
    result = _check(graded)
    assert NOISE_CHECK in result.failed() and source in result.details[NOISE_CHECK]


def test_an_empty_words_json_does_not_earn_the_noise_check(graded: Path) -> None:
    _deliver(graded, {})
    assert NOISE_CHECK in _check(graded).failed()


def test_merging_two_words_that_differ_by_an_accent_fails(graded: Path) -> None:
    links = _gold_lists()
    merged = sorted(set(links.pop("país")) | set(links["pais"]))
    _deliver(graded, {**{word: [other.replace("país", "pais") for other in others] for word, others in links.items()}, "pais": merged})
    result = _check(graded)
    assert {WORDS_CHECK, SAMPLE_CHECK} <= set(result.failed()) and "país" in result.details[WORDS_CHECK]


@pytest.mark.parametrize("winner", ["tempo", "palavra", "PALAVRA ", {"word": "tempo", "links": 16}, ["palavra", "tempo"]])
def test_either_word_of_the_tie_passes(graded: Path, winner: object) -> None:
    _deliver(graded, _gold_lists(), _summary(most_connected=winner))
    assert _check(graded).passed, _check(graded).details


@pytest.mark.parametrize("changed", [
    {"most_connected": "amor"}, {"most_connected": ["tempo", "amor"]}, {"most_connected": []}, {"most_connected": None},
    {"words": len(GOLD) + 1}, {"relations": 2 * GOLD_PAIRS}, {"relations": GOLD_PAIRS - 1},
], ids=["footer word", "one wrong in a list", "empty list", "none", "words off by one", "pairs counted twice", "pairs off by one"])
def test_a_wrong_summary_fails(graded: Path, changed: dict[str, object]) -> None:
    _deliver(graded, _gold_lists(), _summary(**changed))
    assert _check(graded).failed() == [RESULT_CHECK]


def test_the_summary_may_write_numbers_as_text(graded: Path) -> None:
    _deliver(graded, _gold_lists(), _summary(words=f"{len(GOLD)} palavras", relations=str(GOLD_PAIRS)))
    assert _check(graded).passed


# --- the page ---


@pytest.mark.parametrize("page", [
    '<input type="search">', "<INPUT id=q>", '<div contenteditable="true"></div>', '<div role="searchbox"></div>',
    "<div role=searchbox></div>", "<textarea></textarea>", "<script>document.createElement('input')</script>",
])
def test_any_search_field_counts(graded: Path, page: str) -> None:
    (graded / words.PAGE).write_text(page, encoding="utf-8")
    assert SEARCH_CHECK not in _check(graded).failed()


@pytest.mark.parametrize("page", ["<p>no search here</p>", "<!-- <input> -->"])
def test_a_page_without_a_search_field_fails(graded: Path, page: str) -> None:
    (graded / words.PAGE).write_text(page, encoding="utf-8")
    assert _check(graded).failed() == [SEARCH_CHECK]


def test_the_page_runs_under_the_existing_page_checks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[Path] = []
    monkeypatch.setattr(task_run, "add_page_checks", lambda result, html: seen.append(html))
    monkeypatch.setattr(words, "dump_page_dom", lambda page, query: (visual.RENDERED, _panel_dom(query)))
    TASK.setup(tmp_path)
    record = task_run.TaskRunRecord(task_id=TASK.id, answers=TASK.reference(tmp_path), workspace=tmp_path)
    task_run._grade(TASK, record)
    assert seen == [tmp_path / words.PAGE] and record.check is not None and record.check.passed


@pytest.mark.parametrize("status", [visual.NO_BROWSER, f"{visual.RENDER_FAILED}: timeout after 120s"])
def test_a_machine_that_cannot_open_the_page_gets_a_note_and_no_grade(graded: Path, monkeypatch: pytest.MonkeyPatch, status: str) -> None:
    monkeypatch.setattr(words, "dump_page_dom", lambda page, query: (status, ""))
    result = _check(graded)
    assert result.passed and QUERY_CHECK not in dict(result.checks) and result.notes == [f"?word= not run: {status}"]


def test_no_page_fails_the_query_check_and_starts_no_browser(graded: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def refuses(page: Path, query: str) -> tuple[str, str]:
        raise AssertionError("opened a missing page")

    monkeypatch.setattr(words, "dump_page_dom", refuses)
    (graded / words.PAGE).unlink()
    assert set(_check(graded).failed()) == {SEARCH_CHECK, QUERY_CHECK}


def test_the_query_goes_out_percent_encoded(graded: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    asked: list[str] = []

    def dump(page: Path, query: str) -> tuple[str, str]:
        asked.append(query)
        return visual.RENDERED, _panel_dom(query)

    monkeypatch.setattr(words, "dump_page_dom", dump)
    assert _check(graded).passed
    assert asked == ["word=saudade", "word=pa%C3%ADs"]


LEGEND = "<p>Mais ligadas: tempo, palavra</p>"
ALL_WORDS = "".join(f"<text>{word}</text>" for word in words.WORDS)


def _items(names: object) -> str:
    return "".join(f"<li>{name}</li>" for name in sorted(names))


def _second_neighbours(word: str) -> set[str]:
    return GOLD[word] | {other for neighbour in GOLD[word] for other in GOLD[neighbour]}


def _views(render) -> dict[str, str]:
    return {word: render(word) for word in words.QUERY_DECOYS}


@pytest.mark.parametrize("render", [
    lambda word: f"<ul>{_items(GOLD[word])}</ul>",
    lambda word: f"{LEGEND}<ul>{_items(GOLD[word])}</ul>",
    lambda word: f"<svg>{ALL_WORDS}<g class='hit-{word}'></g></svg>",
    lambda word: f"<ul>{ALL_WORDS}</ul><ul id='focus'>{_items(GOLD[word])}</ul>",
    lambda word: "".join(f'<a aria-label="{other}"></a>' for other in sorted(GOLD[word])) + "<canvas></canvas>",
    lambda word: "".join(f'<circle title="{other.upper()}"></circle>' for other in sorted(GOLD[word])),
    lambda word: "<canvas></canvas><script>new URLSearchParams(location.search)</script>",
    lambda word: f"{LEGEND}<canvas></canvas><script>location.search</script>",
    lambda word: f"<ul>{ALL_WORDS}</ul><canvas></canvas><script>location.search</script>",
    lambda word: f"<ul>{_items(_second_neighbours(word))}</ul>",
], ids=["panel", "panel and legend", "chart that highlights", "full list and panel", "canvas with labels", "chart with titles",
        "canvas", "canvas and legend", "canvas and full list", "second neighbours too"])
def test_a_valid_view_passes_the_query_check(render) -> None:
    assert words._query_problem(_views(render), GOLD) == ""


@pytest.mark.parametrize(("render", "reason"), [
    (lambda word: "<p>Nothing</p>", "missing"),
    (lambda word: f"<svg>{ALL_WORDS}</svg>", "the same for any"),
    (lambda word: f"<ul>{_items(GOLD['saudade'])}</ul>", "the same for any"),
    (lambda word: f"<ul>{_items(GOLD['pais' if word == 'país' else word])}</ul>", "mãe"),
    (lambda word: f"<ul>{_items(GOLD[word])}<li>{words.QUERY_DECOYS[word]}</li></ul>", "no link"),
    (lambda word: f"<ul>{_items(sorted(GOLD[word])[:1])}</ul>", "missing"),
    (lambda word: f"<canvas></canvas><ul>{_items(sorted(GOLD[word])[:1])}</ul><script>location.search</script>", "missing"),
    (lambda word: "<canvas></canvas><script>draw()</script>", "missing"),
    (lambda word: f"<script>const data = '{_items(GOLD[word])}'</script><p>Nothing</p>", "missing"),
], ids=["nothing", "chart that never reacts", "always the same panel", "accent folded, shows the relations of pais", "wrong word in the panel",
        "panel with one relation", "canvas and panel with one relation", "canvas that ignores the query", "relations only in a script"])
def test_a_broken_view_fails_the_query_check(render, reason: str) -> None:
    assert reason in words._query_problem(_views(render), GOLD)
