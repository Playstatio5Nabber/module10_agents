import pytest

from mock_model import MockModel
from my_assistant import LoanAssistant
from my_tool import LoanCalculator
from tests.test_chatbot import SilentModel


def make_assistant():
    return LoanAssistant("Penny", "Be friendly.", LoanCalculator(), MockModel())


def test_tool_calculates_interest_payment():
    tool = LoanCalculator()
    assert tool.monthly_payment(10000, 6, 36) == pytest.approx(304.21937)


def test_tool_handles_zero_interest():
    tool = LoanCalculator()
    assert tool.monthly_payment(1200, 0, 12) == 100


def test_assistant_uses_tool_and_records_messages():
    bot = make_assistant()
    reply = bot.respond("loan 10000 6 36")
    assert "$304.22" in reply
    assert bot.history == [
        {"role": "user", "content": "loan 10000 6 36"},
        {"role": "assistant", "content": reply},
    ]


def test_missing_values_get_help():
    bot = make_assistant()
    assert "Use: loan" in bot.respond("loan")


def test_invalid_numbers_get_help():
    bot = make_assistant()
    assert "numeric" in bot.respond("loan abc 6 36")
    assert "above 0" in bot.respond("loan -100 6 36")
    assert "1 to 600" in bot.respond("loan 1000 6 0")


def test_unknown_request_gets_safe_reply():
    bot = make_assistant()
    assert "not sure" in bot.respond("What is the weather?")


def test_approval_request_goes_to_person():
    bot = make_assistant()
    assert "loan officer" in bot.respond("Can you approve my loan?")


def test_general_message_goes_to_model():
    assert make_assistant().respond("hello") == "Hello! How can I help you today?"


def test_model_unavailable_gets_safe_reply():
    bot = make_assistant()
    bot.model = SilentModel()
    assert "try again" in bot.respond("hello")


def test_calculation_and_handoff_work_without_model():
    bot = make_assistant()
    bot.model = SilentModel()
    assert "$304.22" in bot.respond("loan 10000 6 36")
    assert "loan officer" in bot.respond("Can you approve my loan?")
