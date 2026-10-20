"""Hand-computed cases for docs/SCORING.md: Correct %, Judge, Score, Time and Cost."""

import pytest

from mengine_bench import scoring
from mengine_bench.runner.agents import Usage
from mengine_bench.scoring import Price, TaskOutcome, parse_price, score_run


def usage(inp: int = 1_000_000, cached: int = 0, out: int = 100_000, cost: float | None = None) -> Usage:
    return Usage(inp, cached, out, None, cost, "harness" if cost is not None else "none")


def outcome(**overrides: object) -> TaskOutcome:
    base: dict[str, object] = dict(task_id="t", status="ok", correctness=1.0, solved=True, agent_s=100.0,
                                   step_usages=(usage(cost=1.0),))
    base.update(overrides)
    return TaskOutcome(**base)  # type: ignore[arg-type]


def test_no_weights_par_speed_or_scoring_version() -> None:
    for removed in ("SCORING_VERSION", "SPEED_SHARE", "MANDATORY_CAP", "COMPOSITE_OBJECTIVE_SHARE", "score_suite"):
        assert not hasattr(scoring, removed), removed


def test_correct_is_the_mean_share_and_time_is_the_total() -> None:
    run = score_run([outcome(task_id="a"), outcome(task_id="b", correctness=0.5, solved=False, agent_s=50.0)])
    assert (run.correct, run.solved, run.total, run.time_s) == (75.0, 1, 2, 150.0)
    assert run.judge is None and run.score is None


@pytest.mark.parametrize("status", ["timeout", "crash"])
def test_timeout_and_crash_count_zero_but_keep_their_time(status: str) -> None:
    run = score_run([outcome(status=status, correctness=0.8, agent_s=900.0, step_usages=(None,))])
    assert (run.correct, run.solved, run.time_s) == (0.0, 0, 900.0)
    assert run.tasks[0].correctness == 0.0


def test_score_blends_correct_and_judge_70_30() -> None:
    run = score_run([outcome(task_id="a", judge=80), outcome(task_id="b", correctness=0.5, solved=False, judge=50)])
    assert (run.correct, run.judge, run.score) == (75.0, 65.0, 72.0)


def test_partial_judging_is_rejected() -> None:
    with pytest.raises(ValueError, match="1 of 2"):
        score_run([outcome(task_id="a", judge=80), outcome(task_id="b")])


@pytest.mark.parametrize("bad", [{"status": "unsupported"}, {"correctness": 1.5}, {"judge": 101}, {"judge": True}])
def test_invalid_outcomes_are_rejected_with_the_value(bad: dict[str, object]) -> None:
    with pytest.raises(ValueError, match=repr(next(iter(bad.values())))):
        score_run([outcome(**bad)])


def test_empty_run_is_rejected() -> None:
    with pytest.raises(ValueError, match="no task outcomes"):
        score_run([])


def test_harness_cost_is_used_when_every_step_reports_usd() -> None:
    run = score_run([outcome(task_id="a"), outcome(task_id="b", step_usages=(usage(cost=0.25), usage(cost=0.5)))])
    assert (run.cost.usd, run.cost.basis, run.cost.lower_bound) == (1.75, "harness", False)
    assert [task.cost_usd for task in run.tasks] == [1.0, 0.75]


def test_price_cost_when_the_harness_reports_no_usd() -> None:
    price = Price(input=2.0, cached=0.5, output=10.0)
    # (1_000_000 - 400_000) * 2 + 400_000 * 0.5 + 100_000 * 10 per Mtok = 1.2 + 0.2 + 1.0
    run = score_run([outcome(step_usages=(usage(cached=400_000),))], price=price)
    assert run.cost.usd == pytest.approx(2.4) and run.cost.basis == "price"


def test_unknown_cost_is_na_never_zero() -> None:
    run = score_run([outcome(step_usages=(usage(),))])
    assert (run.cost.usd, run.cost.basis) == (None, "n/a")
    assert run.tasks[0].cost_usd is None


def test_price_zero_declares_free_inference() -> None:
    run = score_run([outcome(step_usages=(usage(),))], price=parse_price("0"))
    assert (run.cost.usd, run.cost.basis) == (0.0, "price")


def test_a_step_without_usage_makes_the_cost_a_lower_bound_and_tokens_stay_counted() -> None:
    run = score_run([outcome(step_usages=(usage(cost=0.5), None)), outcome(task_id="b", status="timeout",
                                                                          step_usages=(None,))])
    assert (run.cost.usd, run.cost.basis, run.cost.lower_bound) == (0.5, "harness", True)
    assert (run.tokens.input, run.tokens.output) == (1_000_000, 100_000)


def test_parse_price() -> None:
    assert parse_price("input=3,cached=0.3,output=15") == Price(input=3.0, cached=0.3, output=15.0)
    assert parse_price(" output=1 , input=2,cached=0 ") == Price(input=2.0, cached=0.0, output=1.0)
    assert parse_price("0") == Price(0.0, 0.0, 0.0)


@pytest.mark.parametrize("text", ["3", "input=3,output=15", "input=x,cached=0,output=1", "input=-1,cached=0,output=1",
                                  "input=1,cached=0,output=1,extra=2", "input=nan,cached=0,output=1"])
def test_parse_price_errors_name_the_value_and_the_shape(text: str) -> None:
    with pytest.raises(ValueError, match="input=X,cached=Y,output=Z") as error:
        parse_price(text)
    assert repr(text) in str(error.value)


def test_docs_worked_example() -> None:
    """Locks the worked example in docs/SCORING.md: the numbers and the lines that show them."""
    from pathlib import Path

    from mengine_bench.report import cost_text, time_text

    rows = [
        outcome(task_id="A", correctness=1.0, solved=True, agent_s=120.0, judge=80, step_usages=(usage(cost=0.40),)),
        outcome(task_id="B", correctness=0.6, solved=False, agent_s=300.0, judge=60, step_usages=(usage(cost=0.90),)),
        outcome(task_id="C", status="timeout", correctness=0.0, solved=False, agent_s=900.0, judge=30,
                step_usages=(None,)),
    ]
    run = score_run(rows)
    assert (run.correct, run.solved, run.judge, run.score, run.time_s) == (53.3, 1, 56.7, 54.3, 1320.0)
    totals = {"cost_usd": run.cost.usd, "cost_basis": run.cost.basis, "cost_lower_bound": run.cost.lower_bound}
    assert (time_text(run.time_s), cost_text(totals)) == ("22 min 00 s", ">= $1.30 (harness)")
    codex = Usage(2_000_000, 1_500_000, 100_000, None, None, "none")
    assert round(parse_price("input=1.25,cached=0.125,output=10").cost_usd(codex) or 0, 2) == 1.81
    doc = (Path(__file__).resolve().parents[1] / "docs" / "SCORING.md").read_text(encoding="utf-8")
    for line in ("Correct % = 100 x (1.00 + 0.60 + 0.00) / 3 = 53.3; Solved 1/3",
                 "Judge = (80 + 60 + 30) / 3 = 56.7", "Score = 0.7 x 53.3 + 0.3 x 56.7 = 54.3",
                 "Time = 120 + 300 + 900 = 1320 s (22 min 00 s)", "Cost = 0.40 + 0.90 = >= $1.30 (harness)",
                 "(500,000 x 1.25 + 1,500,000 x 0.125 + 100,000 x 10) / 1,000,000 = $1.81"):
        assert line in " ".join(doc.split()), line


def test_declared_free_inference_costs_zero_even_without_token_counts() -> None:
    # `cmd` reports no usage; `--price 0` still declares a known $0 (#23 review).
    run = score_run([outcome(step_usages=(None,)), outcome(task_id="b", step_usages=())], parse_price("0"))
    assert (run.cost.usd, run.cost.basis, run.cost.lower_bound) == (0.0, "price", False)
    assert [task.cost_usd for task in run.tasks] == [0.0, 0.0]
