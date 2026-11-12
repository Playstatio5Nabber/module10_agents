# Lab 12 AI-generated output

With  AI assistance. Each Python file below is reproduced exactly; review the explanations before submitting. Real model observations were not fabricated.

## my_main.py

```python
# Author: Sami Ali
# Import the dependency used by this file.
from loan_queue import LoanQueue

# Import the dependency used by this file.
from loan_toolbox import LoanToolbox

# Import the dependency used by this file.
from my_assistant import LoanAssistant

# Import the dependency used by this file.
from my_tool import LoanCalculator

# Import the dependency used by this file.
from ollama_model import OllamaModel

# Store INSTRUCTIONS for the following checks or operations.
INSTRUCTIONS = """You are Penny, an assistant for a fictional lending business.
Answer in one short sentence.
The office is open Monday through Friday from 9 am to 5 pm.
Payment estimates include principal and interest only, excluding fees and insurance.
Use only facts in these instructions or tool results. Never invent a rate or promise approval.
If the customer only says hello, greet them and ask how you can help.
Ask for missing amount, annual percentage, and term in whole months before estimating.
Use exactly the customer's numeric text in tool arguments, without commas or currency signs.
Only request an estimate save when the customer explicitly asks to save and supplies a label.
A save request waits for staff; never say it is saved before approval.
If you do not know, say so and refer the customer to a loan officer."""


# Define main so this operation can be called and tested separately.
def main():
    # Store calculator for the following checks or operations.
    calculator = LoanCalculator()
    # Store queue for the following checks or operations.
    queue = LoanQueue(calculator)
    # Store tools for the following checks or operations.
    tools = LoanToolbox(calculator, queue)
    # Store model for the following checks or operations.
    model = OllamaModel("granite4.1:3b")
    # Store bot for the following checks or operations.
    bot = LoanAssistant("Penny", INSTRUCTIONS, tools, model)
    # Run print('Ask for a payment estimate using an amount, annual rate, and months.') to perform...
    print("Ask for a payment estimate using an amount, annual rate, and months.")
    # Run print('Use fictional values. Type quit to stop.') to perform this step.
    print("Use fictional values. Type quit to stop.")
    # Repeat while True, keeping the loop bounded.
    while True:
        # Store message for the following checks or operations.
        message = input("You: ")
        # Check message.strip().lower() == 'quit' before continuing.
        if message.strip().lower() == "quit":
            # Leave the loop when the stopping condition has been met.
            break
        # Run print(f'{bot.name}: {bot.respond(message)}') to perform this step.
        print(f"{bot.name}: {bot.respond(message)}")
    # Run print('Staff review (saving estimates only, not approving loans)') to perform this step.
    print("Staff review (saving estimates only, not approving loans)")
    # Inspect each request in queue.waiting().
    for request in queue.waiting():
        # Store number for the following checks or operations.
        number = request["number"]
        # Run print(f"Request {number}: {request['label']}, {request['values']}") to perform this step.
        print(f"Request {number}: {request['label']}, {request['values']}")
        # Check input('Approve save? yes or no: ') == 'yes' before continuing.
        if input("Approve save? yes or no: ") == "yes":
            # Run print(queue.approve(number)) to perform this step.
            print(queue.approve(number))
        else:
            # Run print(queue.reject(number)) to perform this step.
            print(queue.reject(number))
    # Run print('Saved estimates:', calculator.saved_estimates) to perform this step.
    print("Saved estimates:", calculator.saved_estimates)


# Check __name__ == '__main__' before continuing.
if __name__ == "__main__":
    # Run main() to perform this step.
    main()
```

## my_assistant.py

```python
# Author: Sami Ali
# Import the dependency used by this file.
from chatbot import SupportChatbot


# Define LoanAssistant to keep this responsibility in a separate object.
class LoanAssistant(SupportChatbot):
    """Use the limited tool loop while keeping lending decisions with people."""

    # Define choose_reply so this operation can be called and tested separately.
    def choose_reply(self, user_message):
        # Check self.needs_human(user_message.lower()) before continuing.
        if self.needs_human(user_message.lower()):
            # Return 'Please contact a loan officer for approval or personal advice.' to the caller.
            return "Please contact a loan officer for approval or personal advice."
        # Return self.model_reply() to the caller.
        return self.model_reply()

    # Define needs_human so this operation can be called and tested separately.
    def needs_human(self, text):
        # Inspect each word in ['approve', 'approval', 'qualify', 'advice'].
        for word in ["approve", "approval", "qualify", "advice"]:
            # Check word in text before continuing.
            if word in text:
                # Return True to the caller.
                return True
        # Return False to the caller.
        return False
```

## loan_toolbox.py

```python
# Author: Sami Ali
# Import the dependency used by this file.
import re

# Import the dependency used by this file.
from toolbox import Toolbox


# Define LoanToolbox to keep this responsibility in a separate object.
class LoanToolbox(Toolbox):
    """Check all model-requested calculations and estimate-save requests."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, calculator, queue):
        # Store self.calculator for the following checks or operations.
        self.calculator = calculator
        # Store self.change_queue for the following checks or operations.
        self.change_queue = queue

    # Define tool_list so this operation can be called and tested separately.
    def tool_list(self):
        # Return [self.calculator.estimate_payment, self.change_queue.request_save_estimate] to the ca...
        return [
            self.calculator.estimate_payment,
            self.change_queue.request_save_estimate,
        ]

    # Define customer_said so this operation can be called and tested separately.
    def customer_said(self, history, text):
        # Check not text before continuing.
        if not text:
            # Return False to the caller.
            return False
        # Store pattern for the following checks or operations.
        pattern = r"(?<![\w.])" + re.escape(text) + r"(?![\w.])"
        # Inspect each message in history.
        for message in history:
            # Check message['role'] == 'user' and re.search(pattern, message['content'], re.IGNORECASE) be...
            if message["role"] == "user" and re.search(
                pattern, message["content"], re.IGNORECASE
            ):
                # Return True to the caller.
                return True
        # Return False to the caller.
        return False

    # Define run so this operation can be called and tested separately.
    def run(self, name, arguments, history):
        # Check name not in ['estimate_payment', 'request_save_estimate'] before continuing.
        if name not in ["estimate_payment", "request_save_estimate"]:
            # Return f'There is no tool named {name}.' to the caller.
            return f"There is no tool named {name}."
        # Store keys for the following checks or operations.
        keys = ["principal", "annual_rate", "months"]
        # Check name == 'request_save_estimate' before continuing.
        if name == "request_save_estimate":
            # Store keys for the following checks or operations.
            keys = ["label"] + keys
        # Store values for the following checks or operations.
        values = {}
        # Inspect each key in keys.
        for key in keys:
            # Store value for the following checks or operations.
            value = self.clean(arguments, key)
            # Check value == '' before continuing.
            if value == "":
                # Return f'The {key} is missing. Ask the customer for it.' to the caller.
                return f"The {key} is missing. Ask the customer for it."
            # Check not self.customer_said(history, value) before continuing.
            if not self.customer_said(history, value):
                # Return f'The customer has not given that {key}. Ask them for it.' to the caller.
                return f"The customer has not given that {key}. Ask them for it."
            # Store values[key] for the following checks or operations.
            values[key] = value
        # Check name == 'estimate_payment' before continuing.
        if name == "estimate_payment":
            # Return self.calculator.estimate_payment(**values) to the caller.
            return self.calculator.estimate_payment(**values)
        # Return self.change_queue.request_save_estimate(**values) to the caller.
        return self.change_queue.request_save_estimate(**values)
```

## loan_queue.py

```python
# Author: Sami Ali
# Import the dependency used by this file.
from change_queue import ChangeQueue


# Define LoanQueue to keep this responsibility in a separate object.
class LoanQueue(ChangeQueue):
    """Queue fictional estimate saves; no application or loan is approved."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, calculator):
        # Store self.calculator for the following checks or operations.
        self.calculator = calculator
        # Store self.requests for the following checks or operations.
        self.requests = []

    # Define request_save_estimate so this operation can be called and tested separately.
    def request_save_estimate(self, label, principal, annual_rate, months):
        """Ask staff to save an estimate; do not save it yet.

        Args:
            label: The customer-supplied estimate label.
            principal: The borrowed amount as text.
            annual_rate: The annual percentage as text.
            months: The term in whole months as text.
        """
        # Store values for the following checks or operations.
        values = self.calculator.validated(principal, annual_rate, months)
        # Check not label.strip() or values is None before continuing.
        if not label.strip() or values is None:
            # Return 'A label and valid loan values are required.' to the caller.
            return "A label and valid loan values are required."
        # Store number for the following checks or operations.
        number = len(self.requests) + 1
        # Run self.requests.append({'number': number, 'label': label, 'values': values, 'status': 'wai...
        self.requests.append(
            {"number": number, "label": label, "values": values, "status": "waiting"}
        )
        # Return f'Request {number} sent to staff. The estimate has not been saved yet.' to the caller.
        return f"Request {number} sent to staff. The estimate has not been saved yet."

    # Define approve so this operation can be called and tested separately.
    def approve(self, number):
        # Store request for the following checks or operations.
        request = self.find(number)
        # Check request is None before continuing.
        if request is None:
            # Return f'There is no request {number}.' to the caller.
            return f"There is no request {number}."
        # Check request['status'] != 'waiting' before continuing.
        if request["status"] != "waiting":
            # Return f"Request {number} is already {request['status']}." to the caller.
            return f"Request {number} is already {request['status']}."
        # Run self.calculator.save_estimate(request['label'], request['values']) to perform this step.
        self.calculator.save_estimate(request["label"], request["values"])
        # Store request['status'] for the following checks or operations.
        request["status"] = "approved"
        # Return f'Request {number} approved.' to the caller.
        return f"Request {number} approved."
```

## my_tool.py

```python
# Author: Sami Ali
# Define LoanCalculator to keep this responsibility in a separate object.
class LoanCalculator:
    """Calculate fictional loan estimates without making lending decisions."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, payments_per_year=12):
        # Store self.payments_per_year for the following checks or operations.
        self.payments_per_year = payments_per_year
        # Store self.saved_estimates for the following checks or operations.
        self.saved_estimates = {}

    # Define monthly_payment so this operation can be called and tested separately.
    def monthly_payment(self, principal, annual_rate, months):
        # Check principal <= 0 or annual_rate < 0 or months <= 0 before continuing.
        if principal <= 0 or annual_rate < 0 or months <= 0:
            # Return None to the caller.
            return None
        # Store rate for the following checks or operations.
        rate = annual_rate / 100 / self.payments_per_year
        # Check rate == 0 before continuing.
        if rate == 0:
            # Return principal / months to the caller.
            return principal / months
        # Return principal * rate / (1 - (1 + rate) ** (-months)) to the caller.
        return principal * rate / (1 - (1 + rate) ** (-months))

    # Define estimate_payment so this operation can be called and tested separately.
    def estimate_payment(self, principal, annual_rate, months):
        """Estimate a monthly payment using values the customer supplied.

        Args:
            principal: The borrowed amount as text, like 10000.
            annual_rate: The annual percentage as text, like 6.
            months: The whole-number loan term as text, like 36.
        """
        # Store values for the following checks or operations.
        values = self.validated(principal, annual_rate, months)
        # Check values is None before continuing.
        if values is None:
            # Return 'Use a positive amount up to 100000000, rate 0 to 100, and whole-number months 1 to 6...
            return "Use a positive amount up to 100000000, rate 0 to 100, and whole-number months 1 to 600."
        # Store payment for the following checks or operations.
        payment = self.monthly_payment(*values)
        # Return f'Estimated monthly payment: ${payment:.2f} (principal and interest only).' to the ca...
        return (
            f"Estimated monthly payment: ${payment:.2f} (principal and interest only)."
        )

    # Define validated so this operation can be called and tested separately.
    def validated(self, principal, annual_rate, months):
        # Attempt the operation while handling expected failures below.
        try:
            # Store amount for the following checks or operations.
            amount = float(principal)
            # Store rate for the following checks or operations.
            rate = float(annual_rate)
            # Store term for the following checks or operations.
            term = int(str(months))
        except (ValueError, TypeError, OverflowError):
            # Return None to the caller.
            return None
        # Check not (0 < amount <= 100000000 and 0 <= rate <= 100 and (1 <= term <= 600)) before conti...
        if not (0 < amount <= 100000000 and 0 <= rate <= 100 and 1 <= term <= 600):
            # Return None to the caller.
            return None
        # Return (amount, rate, term) to the caller.
        return amount, rate, term

    # Define save_estimate so this operation can be called and tested separately.
    def save_estimate(self, label, values):
        """Store a reviewed estimate; only the queue's approval calls this."""
        # Store self.saved_estimates[label] for the following checks or operations.
        self.saved_estimates[label] = tuple(values)
```

## fallback_model.py

```python
# Author: Sami Ali
# Define FallbackModel to keep this responsibility in a separate object.
class FallbackModel:
    """Try a backup model only when the primary model is unavailable."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, primary, backup):
        # Store self.primary for the following checks or operations.
        self.primary = primary
        # Store self.backup for the following checks or operations.
        self.backup = backup

    # Define decide so this operation can be called and tested separately.
    def decide(self, instructions, history, tools):
        # Store decision for the following checks or operations.
        decision = self.primary.decide(instructions, history, tools)
        # Check decision is None before continuing.
        if decision is None:
            # Return self.backup.decide(instructions, history, tools) to the caller.
            return self.backup.decide(instructions, history, tools)
        # Return decision to the caller.
        return decision
```

## stock_tool.py

```python
# Author: Sami Ali
# Define StockLookup to keep this responsibility in a separate object.
class StockLookup:
    """Look up product names and stock counts."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, stock):
        # Store self.stock for the following checks or operations.
        self.stock = stock

    # Define find_product so this operation can be called and tested separately.
    def find_product(self, text):
        # Inspect each product in self.stock.
        for product in self.stock:
            # Check product.lower() in text.lower() before continuing.
            if product.lower() in text.lower():
                # Return product to the caller.
                return product
        # Return None to the caller.
        return None

    # Define count_for so this operation can be called and tested separately.
    def count_for(self, product):
        # Return self.stock.get(product) to the caller.
        return self.stock.get(product)

    # Define check_stock so this operation can be called and tested separately.
    def check_stock(self, item):
        """Check how many of one product are in stock.

        Args:
            item: The product name, like rain jacket.
        """
        # Store product for the following checks or operations.
        product = self.find_product(item)
        # Check product is None before continuing.
        if product is None:
            # Return 'That product was not found.' to the caller.
            return "That product was not found."
        # Return f'We have {self.count_for(product)} of the {product} in stock.' to the caller.
        return f"We have {self.count_for(product)} of the {product} in stock."
```

## main.py

```python
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
```

## ollama_model.py

```python
# ollama_model.py
# Author: Sami Ali

# Import the dependency used by this file.
from ollama import ResponseError, chat


# Define OllamaModel to keep this responsibility in a separate object.
class OllamaModel:
    """A real AI model that runs on this computer through Ollama."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, model_name):
        """Remember which model to ask."""
        # Store self.model_name for the following checks or operations.
        self.model_name = model_name

    # Define reply so this operation can be called and tested separately.
    def reply(self, instructions, history):
        """Send the instructions and the conversation to the model. Return its reply."""
        # Store messages for the following checks or operations.
        messages = [{"role": "system", "content": instructions}]
        # Store messages for the following checks or operations.
        messages = messages + history
        # Attempt the operation while handling expected failures below.
        try:
            # Store response for the following checks or operations.
            response = chat(model=self.model_name, messages=messages)
        except ConnectionError:
            # Return None to the caller.
            return None
        except ResponseError:
            # Return None to the caller.
            return None
        # Return response.message.content to the caller.
        return response.message.content

    # Define decide so this operation can be called and tested separately.
    def decide(self, instructions, history, tools):
        """Send the conversation and the tools. Return a reply or a tool request."""
        # Store messages for the following checks or operations.
        messages = [{"role": "system", "content": instructions}]
        # Inspect each message in history.
        for message in history:
            # Check message['role'] == 'tool' before continuing.
            if message["role"] == "tool":
                # Store messages for the following checks or operations.
                messages = messages + self.tool_messages(message)
            else:
                # Run messages.append(message) to perform this step.
                messages.append(message)
        # Attempt the operation while handling expected failures below.
        try:
            # Store response for the following checks or operations.
            response = chat(model=self.model_name, messages=messages, tools=tools)
        except ConnectionError:
            # Return None to the caller.
            return None
        except ResponseError:
            # Return None to the caller.
            return None
        # Check response.message.tool_calls before continuing.
        if response.message.tool_calls:
            # Store call for the following checks or operations.
            call = response.message.tool_calls[0]
            # Return {'tool': call.function.name, 'arguments': call.function.arguments} to the caller.
            return {"tool": call.function.name, "arguments": call.function.arguments}
        # Return {'text': response.message.content} to the caller.
        return {"text": response.message.content}

    # Define tool_messages so this operation can be called and tested separately.
    def tool_messages(self, message):
        """Turn one tool entry into the two messages Ollama expects."""
        # Store name for the following checks or operations.
        name = message["tool_name"]
        # Store request for the following checks or operations.
        request = {"function": {"name": name, "arguments": message["arguments"]}}
        # Return [{'role': 'assistant', 'content': '', 'tool_calls': [request]}, {'role': 'tool', 'too...
        return [
            {"role": "assistant", "content": "", "tool_calls": [request]},
            {"role": "tool", "tool_name": name, "content": message["content"]},
        ]
```

## two_bots.py

```python
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
```

## chatbot.py

```python
# chatbot.py
# Author: Sami Ali

# Store HANDOFF_WORDS for the following checks or operations.
HANDOFF_WORDS = ["payment", "card"]
# Store MAX_TOOL_ROUNDS for the following checks or operations.
MAX_TOOL_ROUNDS = 3


# Define SupportChatbot to keep this responsibility in a separate object.
class SupportChatbot:
    """A support chatbot. The model decides. The toolbox checks every tool request."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, name, instructions, tools, model):
        """Set up one chatbot with its own name, instructions, tools, model, and history."""
        # Store self.name for the following checks or operations.
        self.name = name
        # Store self.instructions for the following checks or operations.
        self.instructions = instructions
        # Store self.tools for the following checks or operations.
        self.tools = tools
        # Store self.model for the following checks or operations.
        self.model = model
        # Store self.history for the following checks or operations.
        self.history = []

    # Define respond so this operation can be called and tested separately.
    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, and return it."""
        # Run self.history.append({'role': 'user', 'content': user_message}) to perform this step.
        self.history.append({"role": "user", "content": user_message})
        # Store reply for the following checks or operations.
        reply = self.choose_reply(user_message)
        # Run self.history.append({'role': 'assistant', 'content': reply}) to perform this step.
        self.history.append({"role": "assistant", "content": reply})
        # Return reply to the caller.
        return reply

    # Define choose_reply so this operation can be called and tested separately.
    def choose_reply(self, user_message):
        """Pass payment questions to a person. Send everything else to the model."""
        # Check self.needs_human(user_message.lower()) before continuing.
        if self.needs_human(user_message.lower()):
            # Return "I can't help with that here. I'm passing you to a human agent." to the caller.
            return "I can't help with that here. I'm passing you to a human agent."
        # Return self.model_reply() to the caller.
        return self.model_reply()

    # Define needs_human so this operation can be called and tested separately.
    def needs_human(self, text):
        """Return True if the message is about something a person must handle."""
        # Inspect each word in HANDOFF_WORDS.
        for word in HANDOFF_WORDS:
            # Check word in text before continuing.
            if word in text:
                # Return True to the caller.
                return True
        # Return False to the caller.
        return False

    # Define model_reply so this operation can be called and tested separately.
    def model_reply(self):
        """Ask the model. Run each tool it asks for, then ask again, up to a limit."""
        # Store rounds for the following checks or operations.
        rounds = 0
        # Repeat while rounds < MAX_TOOL_ROUNDS, keeping the loop bounded.
        while rounds < MAX_TOOL_ROUNDS:
            # Store tool_list for the following checks or operations.
            tool_list = self.tools.tool_list()
            # Store decision for the following checks or operations.
            decision = self.model.decide(self.instructions, self.history, tool_list)
            # Check decision is None before continuing.
            if decision is None:
                # Return "Sorry, I can't answer that right now. Please try again in a moment." to the caller.
                return "Sorry, I can't answer that right now. Please try again in a moment."
            # Check 'text' in decision before continuing.
            if "text" in decision:
                # Return decision['text'] to the caller.
                return decision["text"]
            # Store name for the following checks or operations.
            name = decision["tool"]
            # Store arguments for the following checks or operations.
            arguments = decision["arguments"]
            # Store result for the following checks or operations.
            result = self.tools.run(name, arguments, self.history)
            # Run self.history.append({'role': 'tool', 'tool_name': name, 'arguments': arguments, 'content...
            self.history.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "arguments": arguments,
                    "content": result,
                }
            )
            # Update rounds after this step.
            rounds += 1
        # Return "Sorry, I couldn't finish that. I'm passing you to a human agent." to the caller.
        return "Sorry, I couldn't finish that. I'm passing you to a human agent."

    # Define count_user_messages so this operation can be called and tested separately.
    def count_user_messages(self):
        """Return how many messages the user has sent so far."""
        # Store count for the following checks or operations.
        count = 0
        # Inspect each message in self.history.
        for message in self.history:
            # Check message['role'] == 'user' before continuing.
            if message["role"] == "user":
                # Update count after this step.
                count += 1
        # Return count to the caller.
        return count
```

## fake_model.py

```python
# fake_model.py
# Author: Sami Ali


# Define FakeModel to keep this responsibility in a separate object.
class FakeModel:
    """A model for tests. It plays back a list of decisions, one per call."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, decisions):
        """Store the decisions to play back, in order."""
        # Store self.decisions for the following checks or operations.
        self.decisions = decisions
        # Store self.calls for the following checks or operations.
        self.calls = 0

    # Define decide so this operation can be called and tested separately.
    def decide(self, instructions, history, tools):
        """Return the next decision in the list."""
        # Store decision for the following checks or operations.
        decision = self.decisions[self.calls]
        # Update self.calls after this step.
        self.calls += 1
        # Return decision to the caller.
        return decision
```

## keyword_model.py

```python
# keyword_model.py
# Author: Sami Ali


# Define KeywordModel to keep this responsibility in a separate object.
class KeywordModel:
    """A stand-in model that decides with keyword rules. It needs no AI."""

    # Define decide so this operation can be called and tested separately.
    def decide(self, instructions, history, tools):
        """Return a reply or a tool request, based on the last message."""
        # Store last for the following checks or operations.
        last = history[-1]
        # Check last['role'] == 'tool' before continuing.
        if last["role"] == "tool":
            # Return {'text': last['content']} to the caller.
            return {"text": last["content"]}
        # Store text for the following checks or operations.
        text = last["content"].lower()
        # Check 'order' in text before continuing.
        if "order" in text:
            # Return {'tool': 'look_up_order', 'arguments': {'order_id': last['content']}} to the caller.
            return {"tool": "look_up_order", "arguments": {"order_id": last["content"]}}
        # Check 'stock' in text before continuing.
        if "stock" in text:
            # Return {'tool': 'check_stock', 'arguments': {'item': last['content']}} to the caller.
            return {"tool": "check_stock", "arguments": {"item": last["content"]}}
        # Check 'hello' in text before continuing.
        if "hello" in text:
            # Return {'text': 'Hello! How can I help you today?'} to the caller.
            return {"text": "Hello! How can I help you today?"}
        # Return {'text': "I'm not sure how to help with that. I can check an order or stock."} to the...
        return {
            "text": "I'm not sure how to help with that. I can check an order or stock."
        }
```

## toolbox.py

```python
# toolbox.py
# Author: Sami Ali


# Define Toolbox to keep this responsibility in a separate object.
class Toolbox:
    """Every tool request from the model comes through here and is checked."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, order_tool, stock_tool, change_queue):
        """Hold the tools the model is allowed to ask for."""
        # Store self.order_tool for the following checks or operations.
        self.order_tool = order_tool
        # Store self.stock_tool for the following checks or operations.
        self.stock_tool = stock_tool
        # Store self.change_queue for the following checks or operations.
        self.change_queue = change_queue

    # Define tool_list so this operation can be called and tested separately.
    def tool_list(self):
        """Return the tools the model may ask for. They are not called here."""
        # Return [self.order_tool.look_up_order, self.order_tool.check_return, self.stock_tool.check_s...
        return [
            self.order_tool.look_up_order,
            self.order_tool.check_return,
            self.stock_tool.check_stock,
            self.change_queue.request_address_change,
        ]

    # Define run so this operation can be called and tested separately.
    def run(self, name, arguments, history):
        """Check one tool request. Run the tool only if every check passes."""
        # Check name in ['look_up_order', 'check_return'] before continuing.
        if name in ["look_up_order", "check_return"]:
            # Store order_id for the following checks or operations.
            order_id = self.clean(arguments, "order_id")
            # Check order_id == '' before continuing.
            if order_id == "":
                # Return 'The order ID is missing. Ask the customer for it.' to the caller.
                return "The order ID is missing. Ask the customer for it."
            # Check not self.customer_said(history, order_id) before continuing.
            if not self.customer_said(history, order_id):
                # Return 'The customer has not given that order ID. Ask them for it.' to the caller.
                return "The customer has not given that order ID. Ask them for it."
            # Check name == 'check_return' before continuing.
            if name == "check_return":
                # Return self.order_tool.check_return(order_id) to the caller.
                return self.order_tool.check_return(order_id)
            # Return self.order_tool.look_up_order(order_id) to the caller.
            return self.order_tool.look_up_order(order_id)
        # Check name == 'check_stock' before continuing.
        if name == "check_stock":
            # Store item for the following checks or operations.
            item = self.clean(arguments, "item")
            # Check item == '' before continuing.
            if item == "":
                # Return 'The product is missing. Ask the customer which product.' to the caller.
                return "The product is missing. Ask the customer which product."
            # Return self.stock_tool.check_stock(item) to the caller.
            return self.stock_tool.check_stock(item)
        # Check name == 'request_address_change' before continuing.
        if name == "request_address_change":
            # Store order_id for the following checks or operations.
            order_id = self.clean(arguments, "order_id")
            # Store new_address for the following checks or operations.
            new_address = self.clean(arguments, "new_address")
            # Check order_id == '' or new_address == '' before continuing.
            if order_id == "" or new_address == "":
                # Return 'The order ID and the new address are both needed.' to the caller.
                return "The order ID and the new address are both needed."
            # Check not self.customer_said(history, order_id) before continuing.
            if not self.customer_said(history, order_id):
                # Return 'The customer has not given that order ID. Ask them for it.' to the caller.
                return "The customer has not given that order ID. Ask them for it."
            # Check not self.customer_said(history, new_address) before continuing.
            if not self.customer_said(history, new_address):
                # Return 'The customer has not given that address. Ask them for it.' to the caller.
                return "The customer has not given that address. Ask them for it."
            # Return self.change_queue.request_address_change(order_id, new_address) to the caller.
            return self.change_queue.request_address_change(order_id, new_address)
        # Return f'There is no tool named {name}.' to the caller.
        return f"There is no tool named {name}."

    # Define clean so this operation can be called and tested separately.
    def clean(self, arguments, key):
        """Return one argument as text without extra spaces, or "" if it is missing."""
        # Return str(arguments.get(key, '')).strip() to the caller.
        return str(arguments.get(key, "")).strip()

    # Define customer_said so this operation can be called and tested separately.
    def customer_said(self, history, text):
        """Return True if text appears in a message the customer typed."""
        # Inspect each message in history.
        for message in history:
            # Check message['role'] == 'user' and text.lower() in message['content'].lower() before contin...
            if message["role"] == "user" and text.lower() in message["content"].lower():
                # Return True to the caller.
                return True
        # Return False to the caller.
        return False
```

## change_queue.py

```python
# change_queue.py
# Author: Sami Ali


# Define ChangeQueue to keep this responsibility in a separate object.
class ChangeQueue:
    """Changes waiting for a person to approve. Nothing changes until they do."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, order_tool):
        """Start with no requests. Approved changes go through the order tool."""
        # Store self.order_tool for the following checks or operations.
        self.order_tool = order_tool
        # Store self.requests for the following checks or operations.
        self.requests = []

    # Define request_address_change so this operation can be called and tested separately.
    def request_address_change(self, order_id, new_address):
        """Ask staff to change the shipping address on one order. Staff must approve it.

        Args:
            order_id: The order ID, like A100.
            new_address: The full new shipping address.
        """
        # Store order_id for the following checks or operations.
        order_id = order_id.upper()
        # Check self.order_tool.find_status(order_id) is None before continuing.
        if self.order_tool.find_status(order_id) is None:
            # Return 'No order with that ID was found. Order IDs look like A100.' to the caller.
            return "No order with that ID was found. Order IDs look like A100."
        # Store number for the following checks or operations.
        number = len(self.requests) + 1
        # Store request for the following checks or operations.
        request = {
            "number": number,
            "order_id": order_id,
            "new_address": new_address,
            "status": "waiting",
        }
        # Run self.requests.append(request) to perform this step.
        self.requests.append(request)
        # Return f'Request {number} was sent to staff. The address has not changed yet.' to the caller.
        return f"Request {number} was sent to staff. The address has not changed yet."

    # Define waiting so this operation can be called and tested separately.
    def waiting(self):
        """Return the requests that are still waiting for a decision."""
        # Store result for the following checks or operations.
        result = []
        # Inspect each request in self.requests.
        for request in self.requests:
            # Check request['status'] == 'waiting' before continuing.
            if request["status"] == "waiting":
                # Run result.append(request) to perform this step.
                result.append(request)
        # Return result to the caller.
        return result

    # Define find so this operation can be called and tested separately.
    def find(self, number):
        """Return the request with this number, or None."""
        # Inspect each request in self.requests.
        for request in self.requests:
            # Check request['number'] == number before continuing.
            if request["number"] == number:
                # Return request to the caller.
                return request
        # Return None to the caller.
        return None

    # Define approve so this operation can be called and tested separately.
    def approve(self, number):
        """Approve one waiting request and make the change."""
        # Store request for the following checks or operations.
        request = self.find(number)
        # Check request is None before continuing.
        if request is None:
            # Return f'There is no request {number}.' to the caller.
            return f"There is no request {number}."
        # Check request['status'] != 'waiting' before continuing.
        if request["status"] != "waiting":
            # Return f"Request {number} is already {request['status']}." to the caller.
            return f"Request {number} is already {request['status']}."
        # Store request['status'] for the following checks or operations.
        request["status"] = "approved"
        # Run self.order_tool.change_address(request['order_id'], request['new_address']) to perform t...
        self.order_tool.change_address(request["order_id"], request["new_address"])
        # Return f'Request {number} approved.' to the caller.
        return f"Request {number} approved."

    # Define reject so this operation can be called and tested separately.
    def reject(self, number):
        """Reject one waiting request. Nothing changes."""
        # Store request for the following checks or operations.
        request = self.find(number)
        # Check request is None before continuing.
        if request is None:
            # Return f'There is no request {number}.' to the caller.
            return f"There is no request {number}."
        # Check request['status'] != 'waiting' before continuing.
        if request["status"] != "waiting":
            # Return f"Request {number} is already {request['status']}." to the caller.
            return f"Request {number} is already {request['status']}."
        # Store request['status'] for the following checks or operations.
        request["status"] = "rejected"
        # Return f'Request {number} rejected.' to the caller.
        return f"Request {number} rejected."
```

## order_tool.py

```python
# order_tool.py
# Author: Sami Ali


# Define OrderLookup to keep this responsibility in a separate object.
class OrderLookup:
    """A tool that knows about orders. It knows nothing about chatting."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, orders):
        """Store the orders this tool can look up."""
        # Store self.orders for the following checks or operations.
        self.orders = orders

    # Define find_order_id so this operation can be called and tested separately.
    def find_order_id(self, text):
        """Return the first known order ID mentioned in text, or None."""
        # Inspect each order_id in self.orders.
        for order_id in self.orders:
            # Check order_id in text.upper() before continuing.
            if order_id in text.upper():
                # Return order_id to the caller.
                return order_id
        # Return None to the caller.
        return None

    # Define find_status so this operation can be called and tested separately.
    def find_status(self, order_id):
        """Return the status of one order, or None if there is no such order."""
        # Check order_id in self.orders before continuing.
        if order_id in self.orders:
            # Return self.orders[order_id]['status'] to the caller.
            return self.orders[order_id]["status"]
        # Return None to the caller.
        return None

    # Define look_up_order so this operation can be called and tested separately.
    def look_up_order(self, order_id):
        """Look up the status of one order.

        Args:
            order_id: The order ID, like A100.
        """
        # Store found for the following checks or operations.
        found = self.find_order_id(order_id)
        # Check found is None before continuing.
        if found is None:
            # Return 'No order with that ID was found. Order IDs look like A100.' to the caller.
            return "No order with that ID was found. Order IDs look like A100."
        # Return f'Order {found} is {self.find_status(found)}.' to the caller.
        return f"Order {found} is {self.find_status(found)}."

    # Define change_address so this operation can be called and tested separately.
    def change_address(self, order_id, new_address):
        """Change the shipping address on one order. Only an approval calls this."""
        # Store self.orders[order_id]['address'] for the following checks or operations.
        self.orders[order_id]["address"] = new_address

    # Define check_return so this operation can be called and tested separately.
    def check_return(self, order_id):
        """Check whether an order has reached the return stage.

        Args:
            order_id: The order ID, like A100.
        """
        # Store status for the following checks or operations.
        status = self.find_status(order_id.upper())
        # Check status is None before continuing.
        if status is None:
            # Return 'No order with that ID was found. Order IDs look like A100.' to the caller.
            return "No order with that ID was found. Order IDs look like A100."
        # Check status == 'delivered' before continuing.
        if status == "delivered":
            # Return 'This delivered order can be returned within 30 days with a receipt.' to the caller.
            return "This delivered order can be returned within 30 days with a receipt."
        # Return 'This order cannot be returned yet.' to the caller.
        return "This order cannot be returned yet."
```

## tests/test_my_assistant.py

```python
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
```

## tests/test_chatbot.py

```python
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
```

## tests/test_tools.py

```python
# Import the dependency used by this file.
from change_queue import ChangeQueue

# Import the dependency used by this file.
from order_tool import OrderLookup

# Import the dependency used by this file.
from stock_tool import StockLookup

# Import the dependency used by this file.
from toolbox import Toolbox


# Define make_tools so this operation can be called and tested separately.
def make_tools():
    """Build fresh tools with two orders for each test."""
    # Store orders for the following checks or operations.
    orders = {
        "A100": {"status": "shipped", "address": "14 Bay Road"},
        "A101": {"status": "processing", "address": "3 Gull Lane"},
    }
    # Store order_tool for the following checks or operations.
    order_tool = OrderLookup(orders)
    # Store stock_tool for the following checks or operations.
    stock_tool = StockLookup({"rain jacket": 12, "day pack": 0})
    # Return Toolbox(order_tool, stock_tool, ChangeQueue(order_tool)) to the caller.
    return Toolbox(order_tool, stock_tool, ChangeQueue(order_tool))


# Define customer so this operation can be called and tested separately.
def customer(text):
    """Build a history that holds one customer message."""
    # Return [{'role': 'user', 'content': text}] to the caller.
    return [{"role": "user", "content": text}]


# Define test_look_up_known_order so this operation can be called and tested separately.
def test_look_up_known_order():
    # Store tools for the following checks or operations.
    tools = make_tools()
    assert tools.order_tool.look_up_order("A100") == "Order A100 is shipped."


# Define test_look_up_unknown_order so this operation can be called and tested separately.
def test_look_up_unknown_order():
    # Store tools for the following checks or operations.
    tools = make_tools()
    assert "No order" in tools.order_tool.look_up_order("A999")


# Define test_check_stock_for_known_and_unknown_products so this operation can be called and t...
def test_check_stock_for_known_and_unknown_products():
    # Store tools for the following checks or operations.
    tools = make_tools()
    assert (
        tools.stock_tool.check_stock("day pack")
        == "We have 0 of the day pack in stock."
    )
    assert tools.stock_tool.check_stock("tent") == "That product was not found."


# Define test_request_waits_and_changes_nothing so this operation can be called and tested sep...
def test_request_waits_and_changes_nothing():
    # Store tools for the following checks or operations.
    tools = make_tools()
    # Run tools.change_queue.request_address_change('A100', '9 Pine Street') to perform this step.
    tools.change_queue.request_address_change("A100", "9 Pine Street")
    assert tools.change_queue.waiting()[0]["status"] == "waiting"
    assert tools.order_tool.orders["A100"]["address"] == "14 Bay Road"


# Define test_approve_makes_the_change_once so this operation can be called and tested separat...
def test_approve_makes_the_change_once():
    # Store tools for the following checks or operations.
    tools = make_tools()
    # Run tools.change_queue.request_address_change('A100', '9 Pine Street') to perform this step.
    tools.change_queue.request_address_change("A100", "9 Pine Street")
    assert tools.change_queue.approve(1) == "Request 1 approved."
    assert tools.order_tool.orders["A100"]["address"] == "9 Pine Street"
    assert tools.change_queue.approve(1) == "Request 1 is already approved."


# Define test_reject_changes_nothing_and_cannot_be_approved_later so this operation can be cal...
def test_reject_changes_nothing_and_cannot_be_approved_later():
    # Store tools for the following checks or operations.
    tools = make_tools()
    # Run tools.change_queue.request_address_change('A100', '9 Pine Street') to perform this step.
    tools.change_queue.request_address_change("A100", "9 Pine Street")
    # Run tools.change_queue.reject(1) to perform this step.
    tools.change_queue.reject(1)
    assert tools.change_queue.approve(1) == "Request 1 is already rejected."
    assert tools.order_tool.orders["A100"]["address"] == "14 Bay Road"


# Define test_approve_unknown_request so this operation can be called and tested separately.
def test_approve_unknown_request():
    # Store tools for the following checks or operations.
    tools = make_tools()
    assert tools.change_queue.approve(7) == "There is no request 7."


# Define test_missing_argument_is_refused so this operation can be called and tested separately.
def test_missing_argument_is_refused():
    # Store tools for the following checks or operations.
    tools = make_tools()
    # Store reply for the following checks or operations.
    reply = tools.run("look_up_order", {}, customer("Where is my order?"))
    assert "missing" in reply


# Define test_order_id_must_come_from_the_customer so this operation can be called and tested ...
def test_order_id_must_come_from_the_customer():
    # Store tools for the following checks or operations.
    tools = make_tools()
    # Store reply for the following checks or operations.
    reply = tools.run("look_up_order", {"order_id": "A101"}, customer("Where is A100?"))
    assert "has not given that order ID" in reply


# Define test_customer_said_ignores_capitals so this operation can be called and tested separa...
def test_customer_said_ignores_capitals():
    # Store tools for the following checks or operations.
    tools = make_tools()
    assert tools.customer_said(customer("Ship it to 9 PINE STREET"), "9 Pine Street")


# Define test_unknown_order_containing_a_known_id_is_not_queued so this operation can be calle...
def test_unknown_order_containing_a_known_id_is_not_queued():
    # Store tools for the following checks or operations.
    tools = make_tools()
    # Store reply for the following checks or operations.
    reply = tools.change_queue.request_address_change("A1000", "9 Pine Street")
    assert "No order" in reply
    assert tools.change_queue.waiting() == []


# Define test_check_return_checks_status_and_customer_id so this operation can be called and t...
def test_check_return_checks_status_and_customer_id():
    # Store tools for the following checks or operations.
    tools = make_tools()
    # Store tools.order_tool.orders['A102'] for the following checks or operations.
    tools.order_tool.orders["A102"] = {
        "status": "delivered",
        "address": "88 Pier Street",
    }
    assert "within 30 days" in tools.run(
        "check_return", {"order_id": "A102"}, customer("A102")
    )
    assert "cannot be returned yet" in tools.order_tool.check_return("A100")
    assert "No order" in tools.order_tool.check_return("A999")
    assert "missing" in tools.run("check_return", {}, customer("return it"))
    assert "has not given" in tools.run(
        "check_return", {"order_id": "A102"}, customer("A100")
    )
```

