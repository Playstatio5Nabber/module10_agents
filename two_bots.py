# two_bots.py
# Author: Sami Ali

# Import the dependency used by this file.
from change_queue import ChangeQueue

# Import the dependency used by this file.
from chatbot import SupportChatbot

# Import the dependency used by this file.
from keyword_model import KeywordModel

# Import the dependency used by this file.
from order_tool import OrderLookup

# Import the dependency used by this file.
from stock_tool import StockLookup

# Import the dependency used by this file.
from toolbox import Toolbox

# Store order_tool for the following checks or operations.
order_tool = OrderLookup({"A100": {"status": "shipped", "address": "14 Bay Road"}})
# Store stock_tool for the following checks or operations.
stock_tool = StockLookup({"rain jacket": 12, "day pack": 0})
# Store tools for the following checks or operations.
tools = Toolbox(order_tool, stock_tool, ChangeQueue(order_tool))

# Store model for the following checks or operations.
model = KeywordModel()

# Store sunny for the following checks or operations.
sunny = SupportChatbot("Sunny", "You are cheerful and brief.", tools, model)
# Store river for the following checks or operations.
river = SupportChatbot("River", "You are formal and detailed.", tools, model)

# Run sunny.respond('hello') to perform this step.
sunny.respond("hello")
# Run sunny.respond('Where is order A100?') to perform this step.
sunny.respond("Where is order A100?")
# Run river.respond('hello') to perform this step.
river.respond("hello")

# Run print(sunny.name, len(sunny.history)) to perform this step.
print(sunny.name, len(sunny.history))
# Run print(river.name, len(river.history)) to perform this step.
print(river.name, len(river.history))
# Run print(sunny.history[1]['content']) to perform this step.
print(sunny.history[1]["content"])
# Run print(river.history[1]['content']) to perform this step.
print(river.history[1]["content"])
# Run print(sunny.instructions) to perform this step.
print(sunny.instructions)
# Run print(river.instructions) to perform this step.
print(river.instructions)
