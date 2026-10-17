"""Hand-computed cases for docs/SCORING.md."""

import pytest

from mengine_bench.scoring import (
    SCORING_VERSION,
    TaskOutcome,
    score_suite,
    score_task,
)


def outcome(**overrides: object) -> TaskOutcome:
    base: dict[str, object] = dict(
        task_id="t", category="coding", weight=1, par_s=100.0,
        check_score=1.0, mandatory_ok=True, passed=True, agent_s=100.0, status="ok",
    )
    base.update(overrides)
    return TaskOutcome(**base)  # type: ignore[arg-type]


def test_version_is_pinned() -> None:
    assert SCORING_VERSION == "1.0"


def test_solved_at_par_scores_100() -> None:
    task = score_task(outcome())
    assert (task.correctness, task.speed, task.objective, task.solved) == (1.0, 1.0, 100.0, True)


def test_faster_than_par_is_capped_at_100() -> None:
    assert score_task(outcome(agent_s=10.0)).objective == 100.0


def test_solved_twice_as_slow_as_par_scores_90() -> None:
    task = score_task(outcome(agent_s=200.0))
    assert task.speed == 0.5
    assert task.objective == pytest.approx(90.0)


def test_unsolved_partial_checks_get_no_speed() -> None:
    task = score_task(outcome(check_score=0.6, passed=False, agent_s=10.0))
    assert task.solved is False and task.speed == 0.0
    assert task.objective == pytest.approx(48.0)  # 100 * 0.6 * 0.8


def test_mandatory_failure_caps_correctness_and_is_unsolved() -> None:
    task = score_task(outcome(check_score=0.9, mandatory_ok=False, passed=True))
    assert task.correctness == 0.5 and task.solved is False
    assert task.objective == pytest.approx(40.0)


@pytest.mark.parametrize("status", ["timeout", "crash", "unsupported"])
def test_timeout_crash_unsupported_score_zero(status: str) -> None:
    task = score_task(outcome(status=status))
    assert (task.correctness, task.speed, task.objective, task.solved) == (0.0, 0.0, 0.0, False)


def test_unknown_status_is_rejected_with_value() -> None:
    with pytest.raises(ValueError, match="'oops'"):
        score_task(outcome(status="oops"))


def test_weights_two_vs_one() -> None:
    hard = outcome(task_id="hard", weight=2, category="hard")
    easy = outcome(task_id="easy", weight=1, check_score=0.5, passed=False)
    suite = score_suite("full", [hard, easy])
    # (2*100 + 1*40) / 3 = 80.0 ; accuracy (2*1 + 1*0.5) / 3 = 83.3
    assert suite.objective == 80.0
    assert suite.accuracy == 83.3
    assert suite.solved == 1 and suite.total == 2
    assert suite.total_agent_s == 200.0
    assert suite.by_category["hard"].objective == 100.0
    assert suite.by_category["coding"].objective == 40.0


def test_unsupported_tasks_are_listed_separately() -> None:
    suite = score_suite("fast", [outcome(task_id="a"), outcome(task_id="b", status="unsupported")])
    assert suite.unsupported == ("b",)
    assert suite.objective == 50.0


def test_judge_median_of_three_votes() -> None:
    suite = score_suite("fast", [outcome(judge_votes=(70, 90, 80))], judge="judge-x@xhigh")
    assert suite.tasks[0].subjective == 80.0
    assert suite.subjective == 80.0


def test_subjective_is_weighted_and_missing_votes_count_zero() -> None:
    a = outcome(task_id="a", weight=2, judge_votes=(60, 60, 90))
    b = outcome(task_id="b", weight=1)
    suite = score_suite("fast", [a, b], judge="judge-x@xhigh")
    assert suite.subjective == 40.0  # (2*60 + 1*0) / 3


def test_composite_only_when_both_scores_exist() -> None:
    plain = score_suite("fast", [outcome()])
    assert plain.subjective is None and plain.composite is None
    judged = score_suite("fast", [outcome(judge_votes=(50, 50, 50))], judge="judge-x@xhigh")
    assert judged.composite == 80.0  # 0.6*100 + 0.4*50


def test_votes_without_judge_name_are_rejected() -> None:
    with pytest.raises(ValueError, match="judge"):
        score_suite("fast", [outcome(judge_votes=(50,))])


def test_vote_out_of_range_is_rejected() -> None:
    with pytest.raises(ValueError, match="101"):
        score_suite("fast", [outcome(judge_votes=(101,))], judge="j")


def test_empty_suite_is_rejected() -> None:
    with pytest.raises(ValueError, match="no task outcomes"):
        score_suite("fast", [])


def test_docs_worked_example() -> None:
    """Locks the worked example table in docs/SCORING.md."""
    rows = [
        outcome(task_id="A", weight=1, par_s=120, agent_s=90, judge_votes=(80, 85, 90)),
        outcome(task_id="B", weight=2, par_s=300, agent_s=600, judge_votes=(70, 60, 75)),
        outcome(task_id="C", weight=1, par_s=200, agent_s=150, check_score=0.6, passed=False,
                judge_votes=(40, 50, 45)),
        outcome(task_id="D", weight=1, par_s=200, agent_s=100, check_score=0.9, mandatory_ok=False,
                judge_votes=(30, 35, 20)),
        outcome(task_id="E", weight=2, par_s=400, agent_s=900, status="timeout", judge_votes=(10, 0, 5)),
    ]
    suite = score_suite("full", rows, judge="judge-x@xhigh")
    assert [round(t.objective, 1) for t in suite.tasks] == [100.0, 90.0, 48.0, 40.0, 0.0]
    assert (suite.objective, suite.accuracy, suite.solved) == (52.6, 58.6, 2)
    assert (suite.subjective, suite.composite) == (44.3, 49.3)
    assert suite.total_agent_s == 1840.0
