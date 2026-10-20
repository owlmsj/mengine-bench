"""Hand-computed cases for docs/SCORING.md."""

import pytest

from mengine_bench.scoring import (
    TaskOutcome,
    score_suite,
    score_task,
)


def outcome(**overrides: object) -> TaskOutcome:
    base: dict[str, object] = dict(
        task_id="t", category="coding",
        check_score=1.0, mandatory_ok=True, passed=True, agent_s=100.0, status="ok",
    )
    base.update(overrides)
    return TaskOutcome(**base)  # type: ignore[arg-type]


def test_solved_scores_100_whatever_the_time() -> None:
    task = score_task(outcome(agent_s=10_000.0))
    assert (task.correctness, task.objective, task.solved) == (1.0, 100.0, True)


def test_unsolved_partial_checks_score_their_share() -> None:
    task = score_task(outcome(check_score=0.6, passed=False))
    assert task.solved is False and task.objective == pytest.approx(60.0)


def test_mandatory_failure_zeroes_correctness() -> None:
    task = score_task(outcome(check_score=0.9, mandatory_ok=False, passed=True))
    assert task.correctness == 0.0 and task.solved is False


@pytest.mark.parametrize("status", ["timeout", "crash"])
def test_timeout_and_crash_score_zero(status: str) -> None:
    task = score_task(outcome(status=status))
    assert (task.correctness, task.objective, task.solved) == (0.0, 0.0, False)


@pytest.mark.parametrize("status", ["oops", "unsupported"])
def test_unknown_status_is_rejected_with_value(status: str) -> None:
    with pytest.raises(ValueError, match=repr(status)):
        score_task(outcome(status=status))


def test_every_task_counts_the_same() -> None:
    suite = score_suite([outcome(task_id="a"), outcome(task_id="b", check_score=0.5, passed=False)])
    assert (suite.objective, suite.accuracy, suite.solved, suite.total) == (75.0, 75.0, 1, 2)
    assert suite.total_agent_s == 200.0


def test_votes_without_judge_name_are_rejected() -> None:
    with pytest.raises(ValueError, match="judge"):
        score_suite([outcome(judge_votes=(50,))])


def test_empty_run_is_rejected() -> None:
    with pytest.raises(ValueError, match="no task outcomes"):
        score_suite([])
