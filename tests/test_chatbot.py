from chatbot import SupportChatbot
from order_tool import OrderLookup
from stock_tool import StockLookup


def make_bot():
    """Build a fresh chatbot with both tools for each test."""
    orders = {"A100": "shipped", "A101": "processing"}
    stock = {"rain jacket": 12}
    return SupportChatbot(
        "Sunny",
        "Be friendly.",
        OrderLookup(orders),
        StockLookup(stock),
    )


def test_tool_finds_known_status():
    tool = OrderLookup({"A100": "shipped"})
    assert tool.find_status("A100") == "shipped"


def test_tool_returns_none_for_unknown_order():
    tool = OrderLookup({"A100": "shipped"})
    assert tool.find_status("A999") is None


def test_respond_records_both_messages():
    bot = make_bot()
    bot.respond("hello")
    assert len(bot.history) == 2
    assert bot.history[0]["role"] == "user"
    assert bot.history[1]["role"] == "assistant"


def test_order_question_uses_the_tool():
    bot = make_bot()
    assert bot.respond("Where is order A100?") == "Order A100 is shipped."


def test_order_question_without_an_id_asks_for_one():
    bot = make_bot()
    assert "order ID" in bot.respond("Where is my order?")


def test_address_change_goes_to_a_human():
    bot = make_bot()
    assert "human" in bot.respond("Please change my shipping address")


def test_unknown_request_gets_a_safe_reply():
    bot = make_bot()
    assert "not sure" in bot.respond("What is the weather today?")


def test_two_chatbots_keep_separate_histories():
    first = make_bot()
    second = make_bot()
    first.respond("hello")
    assert len(first.history) == 2
    assert len(second.history) == 0


def test_count_user_messages():
    bot = make_bot()
    assert bot.count_user_messages() == 0
    bot.respond("hello")
    bot.respond("Where is order A100?")
    assert bot.count_user_messages() == 2


def test_stock_question_uses_the_tool():
    bot = make_bot()
    assert bot.respond("Is the rain jacket in stock?") == (
        "We have 12 of the rain jacket in stock."
    )
    assert bot.respond("Do you have it in stock?") == (
        "Which product? Please name the item you want me to check."
    )
