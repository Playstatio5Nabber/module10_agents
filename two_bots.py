# Author: Sami Ali

from chatbot import SupportChatbot
from mock_model import MockModel
from order_tool import OrderLookup
from stock_tool import StockLookup

# Create tools that both chatbots will share.
order_tool = OrderLookup({"A100": "shipped"})
stock_tool = StockLookup({"rain jacket": 12})

model = MockModel()

# Create two separate chatbot objects with the same tools.
sunny = SupportChatbot(
    "Sunny",
    "You are cheerful and brief.",
    order_tool,
    stock_tool,
    model,
)

river = SupportChatbot(
    "River",
    "You are formal and detailed.",
    order_tool,
    stock_tool,
    model,
)

# Give Sunny two turns and River one turn.
sunny_first_reply = sunny.respond("hello")
sunny.respond("Where is order A100?")
river_first_reply = river.respond("hello")

# Show their separate history lengths, replies, and instructions.
print(sunny.name, len(sunny.history))
print(river.name, len(river.history))
print(sunny_first_reply)
print(river_first_reply)
print(sunny.instructions)
print(river.instructions)
