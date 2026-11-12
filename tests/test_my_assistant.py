# Import the dependency used by this file.
import pytest

# Import the dependency used by this file.
from fake_model import FakeModel

# Import the dependency used by this file.
from loan_queue import LoanQueue

# Import the dependency used by this file.
from loan_toolbox import LoanToolbox

# Import the dependency used by this file.
from my_assistant import LoanAssistant

# Import the dependency used by this file.
from my_tool import LoanCalculator


# Define make_bot so this operation can be called and tested separately.
def make_bot(decisions):
    # Store calculator for the following checks or operations.
    calculator = LoanCalculator()
    # Store queue for the following checks or operations.
    queue = LoanQueue(calculator)
    # Store tools for the following checks or operations.
    tools = LoanToolbox(calculator, queue)
    # Return LoanAssistant('Penny', 'Use customer values only.', tools, FakeModel(decisions)) to t...
    return LoanAssistant(
        "Penny", "Use customer values only.", tools, FakeModel(decisions)
    )


# Define request so this operation can be called and tested separately.
def request(name, **values):
    # Return {'tool': name, 'arguments': values} to the caller.
    return {"tool": name, "arguments": values}


# Define test_estimate_is_chosen_by_model_and_calculated so this operation can be called and t...
def test_estimate_is_chosen_by_model_and_calculated():
    # Store bot for the following checks or operations.
    bot = make_bot(
        [
            request(
                "estimate_payment", principal="10000", annual_rate="6", months="36"
            ),
            {"text": "Your estimate is ready."},
        ]
    )
    # Run bot.respond('Estimate 10000 at 6 percent for 36 months') to perform this step.
    bot.respond("Estimate 10000 at 6 percent for 36 months")
    assert "$304.22" in bot.history[1]["content"]


# Define test_invented_rate_is_refused so this operation can be called and tested separately.
def test_invented_rate_is_refused():
    # Store bot for the following checks or operations.
    bot = make_bot(
        [
            request(
                "estimate_payment", principal="10000", annual_rate="6", months="36"
            ),
            {"text": "What rate?"},
        ]
    )
    # Run bot.respond('Estimate 10000 for 36 months') to perform this step.
    bot.respond("Estimate 10000 for 36 months")
    assert "has not given that annual_rate" in bot.history[1]["content"]


# Define test_save_waits_for_review_and_applies_once so this operation can be called and teste...
def test_save_waits_for_review_and_applies_once():
    # Store bot for the following checks or operations.
    bot = make_bot(
        [
            request(
                "request_save_estimate",
                label="car",
                principal="10000",
                annual_rate="6",
                months="36",
            ),
            {"text": "Waiting for review."},
        ]
    )
    # Run bot.respond('Save car: 10000 at 6 percent for 36 months') to perform this step.
    bot.respond("Save car: 10000 at 6 percent for 36 months")
    # Store queue for the following checks or operations.
    queue = bot.tools.change_queue
    assert len(queue.waiting()) == 1
    assert bot.tools.calculator.saved_estimates == {}
    assert queue.approve(1) == "Request 1 approved."
    assert bot.tools.calculator.saved_estimates["car"] == (10000, 6, 36)
    assert queue.approve(1) == "Request 1 is already approved."


# Define test_handoff_happens_before_model so this operation can be called and tested separately.
def test_handoff_happens_before_model():
    # Store bot for the following checks or operations.
    bot = make_bot([])
    assert "loan officer" in bot.respond("Do I qualify for this loan?")
    assert bot.model.calls == 0


# Define test_reject_does_not_save so this operation can be called and tested separately.
def test_reject_does_not_save():
    # Store bot for the following checks or operations.
    bot = make_bot([])
    # Store queue for the following checks or operations.
    queue = bot.tools.change_queue
    # Run queue.request_save_estimate('car', '10000', '6', '36') to perform this step.
    queue.request_save_estimate("car", "10000", "6", "36")
    # Run queue.reject(1) to perform this step.
    queue.reject(1)
    assert "already rejected" in queue.approve(1)
    assert bot.tools.calculator.saved_estimates == {}


# Define test_unknown_and_empty_values_are_refused so this operation can be called and tested ...
def test_unknown_and_empty_values_are_refused():
    # Store bot for the following checks or operations.
    bot = make_bot([])
    assert "no tool" in bot.tools.run("delete_loan", {}, [])
    assert "missing" in bot.tools.run("estimate_payment", {}, [])


# Define test_number_fragments_are_not_customer_values so this operation can be called and tes...
def test_number_fragments_are_not_customer_values():
    # Store bot for the following checks or operations.
    bot = make_bot([])
    # Store history for the following checks or operations.
    history = [{"role": "user", "content": "10000 16 360"}]
    assert not bot.tools.customer_said(history, "6")
    assert not bot.tools.customer_said(history, "36")


# Define test_invalid_values_and_zero_interest so this operation can be called and tested sepa...
def test_invalid_values_and_zero_interest():
    # Store calculator for the following checks or operations.
    calculator = LoanCalculator()
    assert "valid" not in calculator.estimate_payment("10000", "6", "36")
    assert "whole-number" in calculator.estimate_payment("nan", "6", "36")
    assert "whole-number" in calculator.estimate_payment("10000", "6", "3.5")
    assert calculator.monthly_payment(1200, 0, 12) == 100
    assert calculator.monthly_payment(10000, 6, 36) == pytest.approx(304.2193745)


# Define test_made_up_save_label_is_refused so this operation can be called and tested separat...
def test_made_up_save_label_is_refused():
    # Store bot for the following checks or operations.
    bot = make_bot(
        [
            request(
                "request_save_estimate",
                label="car",
                principal="10000",
                annual_rate="6",
                months="36",
            ),
            {"text": "What label?"},
        ]
    )
    # Run bot.respond('Save 10000 at 6 percent for 36 months') to perform this step.
    bot.respond("Save 10000 at 6 percent for 36 months")
    assert "has not given that label" in bot.history[1]["content"]
    assert bot.tools.change_queue.waiting() == []
