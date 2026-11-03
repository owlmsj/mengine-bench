"""#164: a correct file must not hide a contradictory final answer."""

from pathlib import Path

import pytest

from mengine_bench.tasks import funnel


def test_reference_passes_and_untouched_fails(tmp_path: Path) -> None:
    funnel._funnel_setup(tmp_path)
    assert not funnel._funnel_check(tmp_path, [""]).passed
    assert funnel._funnel_check(tmp_path, funnel._funnel_reference(tmp_path)).passed


def test_sonnet_funnel_contradiction(tmp_path: Path) -> None:
    funnel._funnel_reference(tmp_path)
    # #164: verbatim result bullets from the Sonnet bundle; the file was correct.
    answer = (
        "- **pc:** biggest_drop is `first_match` (0.825). It is close to the others: "
        "0.828 for `tutorial_complete` and 0.838 for `purchase`.\n"
        "- **steamdeck:** biggest_drop is `tutorial_complete` (0.667), then 0.680 "
        "for `first_match` and 0.701 for `purchase`. Steam Deck loses a third of "
        "installs before the tutorial finishes."
    )
    result = funnel._funnel_check(tmp_path, [answer])
    assert result.failed() == ["final answer does not contradict biggest drops"]
    assert not result.mandatory


@pytest.mark.parametrize("answer", [
    "done", "", "The counts are in result.json.",
    "- **PC:** biggest_drop is `PURCHASE`.\n- Steam Deck: largest drop is tutorial complete.",
    "- **PC:** biggest_drop is `PURCHASE`\n- **Steam Deck:** largest drop is tutorial complete",
    "PC: biggest drop is purchase, Steam Deck: biggest drop is tutorial_complete",
    "The biggest drop on PC is purchase; the lowest conversion for steamdeck is tutorial_complete.",
    "Purchase is the biggest drop for PC. Tutorial complete is the largest drop on Steam Deck.",
    "PC loses the most players at purchase. Steamdeck loses the most players at tutorial_complete.",
    "PC: first_match converts at 0.838; purchase converts at 0.825.",
    "PC's biggest drop is not first_match but purchase.",
    "PC: purchase is the biggest drop. Steamdeck: tutorial_complete is the largest drop.",
    "PC: the largest drop is from first_match to purchase.",
    "Steam Deck: the largest drop is install -> tutorial_complete.",
])
def test_funnel_allows_omission_and_valid_wording(tmp_path: Path, answer: str) -> None:
    funnel._funnel_reference(tmp_path)
    assert funnel._funnel_check(tmp_path, [answer]).passed


@pytest.mark.parametrize("answer", [
    "- **PC:** biggest_drop is `FIRST_MATCH`.",
    "The biggest drop on pc is tutorial complete.",
    "First match is the largest drop for PC.",
    "PC loses the most players at first match.",
    "Steam Deck: lowest conversion is purchase.",
    "PC: biggest drop is purchase. Steamdeck: biggest drop is first_match.",
    "PC: biggest drop is purchase. PC: biggest drop is first_match.",
    "PC: first_match is the biggest drop.",
    "PC: the largest drop is from tutorial_complete to first_match.",
])
def test_funnel_rejects_explicit_wrong_drop(tmp_path: Path, answer: str) -> None:
    funnel._funnel_reference(tmp_path)
    assert "final answer does not contradict biggest drops" in funnel._funnel_check(tmp_path, [answer]).failed()
