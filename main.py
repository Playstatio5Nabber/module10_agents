# main.py
# Author: Sami Ali

# Import the dependency used by this file.
from change_queue import ChangeQueue

# Import the dependency used by this file.
from chatbot import SupportChatbot

# Import the dependency used by this file.
from fallback_model import FallbackModel

# Import the dependency used by this file.
from keyword_model import KeywordModel

# Import the dependency used by this file.
from ollama_model import OllamaModel

# Import the dependency used by this file.
from order_tool import OrderLookup

# Import the dependency used by this file.
from stock_tool import StockLookup

# Import the dependency used by this file.
from toolbox import Toolbox

# Store MODEL_NAME for the following checks or operations.
MODEL_NAME = "granite4.1:3b"

# Store INSTRUCTIONS for the following checks or operations.
INSTRUCTIONS = """You are Sunny, a support assistant for Bayside Outfitters.
Answer in one short sentence.
Store hours are 10 am to 7 pm every day.
Returns are accepted within 30 days with a receipt.
Only state facts that appear in these instructions or in tool results.
If you do not know, say you do not know and offer to pass the customer to a human agent."""

# Store ORDERS for the following checks or operations.
ORDERS = {
    "A100": {"status": "shipped", "address": "14 Bay Road"},
    "A101": {"status": "processing", "address": "3 Gull Lane"},
    "A102": {"status": "delivered", "address": "88 Pier Street"},
}

# Store STOCK for the following checks or operations.
STOCK = {
    "rain jacket": 12,
    "day pack": 0,
    "trail hat": 5,
}

# Store order_tool for the following checks or operations.
order_tool = OrderLookup(ORDERS)
# Store stock_tool for the following checks or operations.
stock_tool = StockLookup(STOCK)
# Store change_queue for the following checks or operations.
change_queue = ChangeQueue(order_tool)
# Store tools for the following checks or operations.
tools = Toolbox(order_tool, stock_tool, change_queue)
# Store model for the following checks or operations.
model = FallbackModel(OllamaModel(MODEL_NAME), KeywordModel())
# Store bot for the following checks or operations.
bot = SupportChatbot("Sunny", INSTRUCTIONS, tools, model)

# Run print('Type a message, or type quit to stop.') to perform this step.
print("Type a message, or type quit to stop.")
# Store user_message for the following checks or operations.
user_message = input("You: ")
# Repeat while user_message != 'quit', keeping the loop bounded.
while user_message != "quit":
    # Run print(f'{bot.name}: {bot.respond(user_message)}') to perform this step.
    print(f"{bot.name}: {bot.respond(user_message)}")
    # Store user_message for the following checks or operations.
    user_message = input("You: ")

# Run print(f'Messages in this conversation: {len(bot.history)}') to perform this step.
print(f"Messages in this conversation: {len(bot.history)}")

# Run print('Staff review') to perform this step.
print("Staff review")
# Inspect each request in change_queue.waiting().
for request in change_queue.waiting():
    # Store number for the following checks or operations.
    number = request["number"]
    # Run print(f"Request {number}: {request['order_id']} to {request['new_address']}") to perform...
    print(f"Request {number}: {request['order_id']} to {request['new_address']}")
    # Store answer for the following checks or operations.
    answer = input("Approve? yes or no: ")
    # Check answer == 'yes' before continuing.
    if answer == "yes":
        # Run print(change_queue.approve(number)) to perform this step.
        print(change_queue.approve(number))
    else:
        # Run print(change_queue.reject(number)) to perform this step.
        print(change_queue.reject(number))

# Inspect each order_id in ORDERS.
for order_id in ORDERS:
    # Run print(order_id, ORDERS[order_id]['address']) to perform this step.
    print(order_id, ORDERS[order_id]["address"])
