# Import the dependency used by this file.
from change_queue import ChangeQueue

# Import the dependency used by this file.
from chatbot import SupportChatbot

# Import the dependency used by this file.
from fake_model import FakeModel

# Import the dependency used by this file.
from keyword_model import KeywordModel

# Import the dependency used by this file.
from order_tool import OrderLookup

# Import the dependency used by this file.
from stock_tool import StockLookup

# Import the dependency used by this file.
from toolbox import Toolbox


# Define SilentModel to keep this responsibility in a separate object.
class SilentModel:
    """A model that never has an answer. It stands in for Ollama being switched off."""

    # Define decide so this operation can be called and tested separately.
    def decide(self, instructions, history, tools):
        # Return None to the caller.
        return None


# Define make_bot so this operation can be called and tested separately.
def make_bot(model):
    """Build a fresh chatbot with its own tools and the model it is given."""
    # Store orders for the following checks or operations.
    orders = {
        "A100": {"status": "shipped", "address": "14 Bay Road"},
        "A101": {"status": "processing", "address": "3 Gull Lane"},
    }
    # Store order_tool for the following checks or operations.
    order_tool = OrderLookup(orders)
    # Store stock_tool for the following checks or operations.
    stock_tool = StockLookup({"rain jacket": 12, "day pack": 0})
    # Store tools for the following checks or operations.
    tools = Toolbox(order_tool, stock_tool, ChangeQueue(order_tool))
    # Return SupportChatbot('Sunny', 'Be friendly.', tools, model) to the caller.
    return SupportChatbot("Sunny", "Be friendly.", tools, model)


# Define ask_for_tool so this operation can be called and tested separately.
def ask_for_tool(name, arguments):
    """Build the decision a model returns when it wants a tool."""
    # Return {'tool': name, 'arguments': arguments} to the caller.
    return {"tool": name, "arguments": arguments}


# Define test_respond_records_both_messages so this operation can be called and tested separat...
def test_respond_records_both_messages():
    # Store bot for the following checks or operations.
    bot = make_bot(KeywordModel())
    # Run bot.respond('hello') to perform this step.
    bot.respond("hello")
    assert len(bot.history) == 2
    assert bot.history[0]["role"] == "user"
    assert bot.history[1]["role"] == "assistant"


# Define test_order_question_uses_the_tool so this operation can be called and tested separately.
def test_order_question_uses_the_tool():
    # Store bot for the following checks or operations.
    bot = make_bot(KeywordModel())
    assert bot.respond("Where is order A100?") == "Order A100 is shipped."


# Define test_tool_use_is_recorded_in_the_history so this operation can be called and tested s...
def test_tool_use_is_recorded_in_the_history():
    # Store bot for the following checks or operations.
    bot = make_bot(KeywordModel())
    # Run bot.respond('Where is order A100?') to perform this step.
    bot.respond("Where is order A100?")
    assert len(bot.history) == 3
    assert bot.history[1]["role"] == "tool"
    assert bot.history[1]["tool_name"] == "look_up_order"


# Define test_model_can_ask_for_a_tool_without_keywords so this operation can be called and te...
def test_model_can_ask_for_a_tool_without_keywords():
    # Store model for the following checks or operations.
    model = FakeModel(
        [
            ask_for_tool("look_up_order", {"order_id": "A101"}),
            {"text": "Your package A101 is still processing."},
        ]
    )
    # Store bot for the following checks or operations.
    bot = make_bot(model)
    # Run bot.respond('Has my package A101 shipped?') to perform this step.
    bot.respond("Has my package A101 shipped?")
    assert bot.history[1]["content"] == "Order A101 is processing."


# Define test_payment_question_never_reaches_the_model so this operation can be called and tes...
def test_payment_question_never_reaches_the_model():
    # Store bot for the following checks or operations.
    bot = make_bot(FakeModel([]))
    assert "human" in bot.respond("Can I pay with a different card?")


# Define test_safe_reply_when_the_model_has_no_answer so this operation can be called and test...
def test_safe_reply_when_the_model_has_no_answer():
    # Store bot for the following checks or operations.
    bot = make_bot(SilentModel())
    assert "try again" in bot.respond("hello")


# Define test_unknown_tool_is_refused so this operation can be called and tested separately.
def test_unknown_tool_is_refused():
    # Store model for the following checks or operations.
    model = FakeModel(
        [ask_for_tool("delete_order", {"order_id": "A100"}), {"text": "Sorry."}]
    )
    # Store bot for the following checks or operations.
    bot = make_bot(model)
    # Run bot.respond('Delete order A100') to perform this step.
    bot.respond("Delete order A100")
    assert bot.history[1]["content"] == "There is no tool named delete_order."


# Define test_loop_stops_after_three_tool_rounds so this operation can be called and tested se...
def test_loop_stops_after_three_tool_rounds():
    # Store request for the following checks or operations.
    request = ask_for_tool("look_up_order", {"order_id": "A100"})
    # Store bot for the following checks or operations.
    bot = make_bot(FakeModel([request, request, request]))
    # Store reply for the following checks or operations.
    reply = bot.respond("Where is order A100?")
    assert "human" in reply
    assert len(bot.history) == 5


# Define test_made_up_address_is_refused so this operation can be called and tested separately.
def test_made_up_address_is_refused():
    # Store model for the following checks or operations.
    model = FakeModel(
        [
            ask_for_tool(
                "request_address_change",
                {"order_id": "A100", "new_address": "123 Main St"},
            ),
            {"text": "What is the new address?"},
        ]
    )
    # Store bot for the following checks or operations.
    bot = make_bot(model)
    # Run bot.respond('Please change the address on order A100') to perform this step.
    bot.respond("Please change the address on order A100")
    assert "has not given that address" in bot.history[1]["content"]
    assert bot.tools.change_queue.waiting() == []


# Define test_blank_address_is_refused so this operation can be called and tested separately.
def test_blank_address_is_refused():
    # Store model for the following checks or operations.
    model = FakeModel(
        [
            ask_for_tool(
                "request_address_change", {"order_id": "A100", "new_address": ""}
            ),
            {"text": "What is the new address?"},
        ]
    )
    # Store bot for the following checks or operations.
    bot = make_bot(model)
    # Run bot.respond('Please change the address on order A100') to perform this step.
    bot.respond("Please change the address on order A100")
    assert bot.tools.change_queue.waiting() == []


# Define test_address_change_waits_for_staff so this operation can be called and tested separa...
def test_address_change_waits_for_staff():
    # Store model for the following checks or operations.
    model = FakeModel(
        [
            ask_for_tool(
                "request_address_change",
                {"order_id": "A100", "new_address": "9 Pine Street"},
            ),
            {"text": "Sent to staff."},
        ]
    )
    # Store bot for the following checks or operations.
    bot = make_bot(model)
    # Run bot.respond('Change the address on order A100 to 9 Pine Street') to perform this step.
    bot.respond("Change the address on order A100 to 9 Pine Street")
    assert len(bot.tools.change_queue.waiting()) == 1
    assert bot.tools.order_tool.orders["A100"]["address"] == "14 Bay Road"


# Define test_number_argument_does_not_crash so this operation can be called and tested separa...
def test_number_argument_does_not_crash():
    # Store model for the following checks or operations.
    model = FakeModel(
        [ask_for_tool("look_up_order", {"order_id": 100}), {"text": "Not found."}]
    )
    # Store bot for the following checks or operations.
    bot = make_bot(model)
    assert bot.respond("Where is order 100?") == "Not found."


# Define test_two_chatbots_keep_separate_histories so this operation can be called and tested ...
def test_two_chatbots_keep_separate_histories():
    # Store first for the following checks or operations.
    first = make_bot(KeywordModel())
    # Store second for the following checks or operations.
    second = make_bot(KeywordModel())
    # Run first.respond('hello') to perform this step.
    first.respond("hello")
    assert len(first.history) == 2
    assert len(second.history) == 0


# Define test_count_user_messages_skips_tool_entries so this operation can be called and teste...
def test_count_user_messages_skips_tool_entries():
    # Store bot for the following checks or operations.
    bot = make_bot(KeywordModel())
    # Run bot.respond('hello') to perform this step.
    bot.respond("hello")
    # Run bot.respond('Where is order A100?') to perform this step.
    bot.respond("Where is order A100?")
    assert bot.count_user_messages() == 2


# Define test_model_can_choose_return_tool so this operation can be called and tested separately.
def test_model_can_choose_return_tool():
    # Store model for the following checks or operations.
    model = FakeModel(
        [ask_for_tool("check_return", {"order_id": "A101"}), {"text": "Not yet."}]
    )
    # Store bot for the following checks or operations.
    bot = make_bot(model)
    # Run bot.respond('Can I return A101?') to perform this step.
    bot.respond("Can I return A101?")
    assert "cannot be returned yet" in bot.history[1]["content"]


# Define test_fallback_keeps_lookups_working so this operation can be called and tested separa...
def test_fallback_keeps_lookups_working():
    # Import the dependency used by this file.
    from fallback_model import FallbackModel

    # Store bot for the following checks or operations.
    bot = make_bot(FallbackModel(SilentModel(), KeywordModel()))
    assert bot.respond("hello") == "Hello! How can I help you today?"
    assert bot.respond("Where is order A100?") == "Order A100 is shipped."
