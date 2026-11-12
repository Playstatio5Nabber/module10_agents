# Lab 11 AI assistance

ChatGPT supplied the following code during step-by-step assistance. Comments explain the generated class statements.


## chatbot.py

```python
# chatbot.py
# Author: Sami Ali
HANDOFF_WORDS = ["address", "payment", "card"]


# Define a chatbot that combines rules, tools, and a model.
class SupportChatbot:
    """A support chatbot. Rules handle what must be right. A model handles the rest."""

    # Receive the chatbot's settings, tools, and model.
    def __init__(self, name, instructions, order_tool, stock_tool, model):
        # Store the chatbot's display name.
        self.name = name
        # Store the instructions supplied to the model.
        self.instructions = instructions
        # Store the tool used to look up orders.
        self.order_tool = order_tool
        # Store the tool used to check stock.
        self.stock_tool = stock_tool
        # Store the model used for other questions.
        self.model = model
        # Start an independent conversation history.
        self.history = []

    # Handle one customer message and record both sides.
    def respond(self, user_message):
        # Record the customer message before choosing a reply.
        self.history.append({"role": "user", "content": user_message})
        # Choose a response using rules first.
        reply = self.choose_reply(user_message)
        # Record the assistant's reply for future model calls.
        self.history.append({"role": "assistant", "content": reply})
        # Give the response back to the calling program.
        return reply

    # Apply handoff and tool rules before asking the model.
    def choose_reply(self, user_message):
        # Ignore capitalization when checking keywords.
        text = user_message.lower()
        # Check sensitive topics before all other requests.
        if self.needs_human(text):
            # Return the fixed handoff response.
            return "I can't help with that here. I'm passing you to a human agent."
        # Recognize an order question.
        if "order" in text:
            # Use the order tool instead of the model.
            return self.order_reply(user_message)
        # Recognize a stock question.
        if "stock" in text:
            # Use the stock tool instead of the model.
            return self.stock_reply(user_message)
        # Send all remaining messages to the model.
        return self.model_reply()

    # Ask the model and handle its no-answer signal.
    def model_reply(self):
        # Send the instructions and recorded conversation.
        reply = self.model.reply(self.instructions, self.history)
        # Check whether the model could not provide an answer.
        if reply is None:
            # Give a safe fallback instead of inventing information.
            return "Sorry, I can't answer that right now. Please try again in a moment."
        # Return the answer supplied by the model.
        return reply

    # Determine whether a human must handle this request.
    def needs_human(self, text):
        # Check each configured sensitive keyword.
        for word in HANDOFF_WORDS:
            # Look for this keyword in the customer's message.
            if word in text:
                # Signal that a human is needed.
                return True
        # Signal that no handoff keyword matched.
        return False

    # Build an order response from stored order data.
    def order_reply(self, user_message):
        # Ask the tool to identify an order in the message.
        order_id = self.order_tool.find_order_id(user_message)
        # Check whether the tool found no recognized order ID.
        if order_id is None:
            # Ask for an order ID rather than guessing.
            return "Which order? Please send an order ID like A100."
        # Look up the status using the order tool.
        status = self.order_tool.find_status(order_id)
        # Return the status in the required wording.
        return f"Order {order_id} is {status}."

    # Count customer messages in this chatbot's history.
    def count_user_messages(self):
        # Begin the count at zero.
        count = 0
        # Examine every recorded message.
        for message in self.history:
            # Count only messages from the customer.
            if message["role"] == "user":
                # Add one for this customer message.
                count += 1
        # Return the completed count.
        return count

    # Build a stock response from stored inventory data.
    def stock_reply(self, user_message):
        # Ask the stock tool to identify the product.
        product = self.stock_tool.find_product(user_message)
        # Check whether no recognized product was found.
        if product is None:
            # Ask the customer to identify the product.
            return "Which product? Please name the item you want me to check."
        # Get the inventory count from the stock tool.
        count = self.stock_tool.count_for(product)
        # Return the count in the required wording.
        return f"We have {count} of the {product} in stock."
```


## mock_model.py

```python
# mock_model.py
# Author: Sami Ali
# AI assistance: ChatGPT reproduced the lab code with explanations.

# Define a stand-in model so tests do not need Ollama.
class MockModel:
    """A stand-in that gives predictable replies."""

    # Accept instructions and history using the chatbot's model interface.
    def reply(self, instructions, history):
        """Choose a fixed reply from the latest message."""
        # Get the last message's text and make it lowercase.
        last_message = history[-1]["content"].lower()
        # Check whether the latest message contains a greeting.
        if "hello" in last_message:
            # Return a predictable greeting.
            return "Hello! How can I help you today?"
        # Return a fixed fallback for every other message.
        return "I'm not sure how to help with that. I can check an order or stock."
```


## ollama_model.py

```python
# ollama_model.py
# Author: Sami Ali

from ollama import ResponseError, chat


# Connect the chatbot's model interface to local Ollama.
class OllamaModel:
    """A real AI model that runs on this computer through Ollama."""

    # Receive the name of the model to use.
    def __init__(self, model_name):
        # Store the name for later requests.
        self.model_name = model_name

    # Accept the chatbot's instructions and conversation history.
    def reply(self, instructions, history):
        # Put the instructions first as a system message.
        messages = [{"role": "system", "content": instructions}]
        # Add the history without changing the original list.
        messages = messages + history
        # Attempt a model call that might fail.
        try:
            # Send the messages to the selected local model.
            response = chat(model=self.model_name, messages=messages)
        # Handle Ollama being unavailable.
        except ConnectionError:
            # Signal the chatbot to use its safe fallback.
            return None
        # Handle errors such as a model that is not downloaded.
        except ResponseError:
            # Use the same no-answer signal.
            return None
        # Return the model's reply text.
        return response.message.content
```


## echo_model.py

```python
# echo_model.py
# Author: Sami Ali
# AI assistance: ChatGPT provided this class with explanations.

# Define a model that repeats the customer's latest message.
class EchoModel:
    # Match the model interface used by the chatbot.
    def reply(self, instructions, history):
        # Prefix the last message's content with "You said: ".
        return "You said: " + history[-1]["content"]
```


## my_assistant.py

```python
# Author: Sami Ali

# Define an assistant that combines loan rules, a tool, and a model.
class LoanAssistant:
    # Receive the name, instructions, calculation tool, and model.
    def __init__(self, name, instructions, loan_tool, model):
        # Store the assistant's display name.
        self.name = name
        # Store the instructions for general questions.
        self.instructions = instructions
        # Store the separate loan calculator.
        self.loan_tool = loan_tool
        # Store the supplied model.
        self.model = model
        # Start this assistant's own conversation history.
        self.history = []

    # Record the customer message and assistant response.
    def respond(self, user_message):
        # Save the customer message before choosing a reply.
        self.history.append({"role": "user", "content": user_message})
        # Apply rules first, then use the model if needed.
        reply = self.choose_reply(user_message)
        # Save the reply for later conversation turns.
        self.history.append({"role": "assistant", "content": reply})
        # Return the reply for display.
        return reply

    # Route requests to a human, the calculator, or the model.
    def choose_reply(self, user_message):
        # Normalize capitalization and remove outside spaces.
        text = user_message.lower().strip()
        # Check topics that need human judgment first.
        for word in ["approve", "approval", "qualify", "advice"]:
            # Look for this handoff keyword.
            if word in text:
                # Give the fixed loan-officer handoff.
                return "Please contact a loan officer for approval or personal advice."
        # Split the message into command words.
        parts = text.split()
        # Recognize the loan calculation command.
        if parts and parts[0] == "loan":
            # Use the calculator instead of asking the model.
            return self.loan_reply(parts)
        # Ask the model about requests outside the rules.
        reply = self.model.reply(self.instructions, self.history)
        # Check the model's no-answer signal.
        if reply is None:
            # Return a safe message when the model is unavailable.
            return "Sorry, I can't answer that right now. Please try again in a moment."
        # Return the model's answer.
        return reply

    # Validate a loan command and ask the calculation tool.
    def loan_reply(self, parts):
        # Require the command and exactly three values.
        if len(parts) != 4:
            # Show the correct command format.
            return "Use: loan AMOUNT ANNUAL_RATE MONTHS. Example: loan 10000 6 36"
        # Attempt to convert the supplied values into numbers.
        try:
            # Read the borrowed amount.
            principal = float(parts[1])
            # Read the annual interest percentage.
            annual_rate = float(parts[2])
            # Read the loan term as a whole number of months.
            months = int(parts[3])
        # Handle values that cannot be converted.
        except ValueError:
            # Explain the required number formats.
            return "Enter numeric amounts and rates, and whole-number months."
        # Reject unsupported amounts and rates, including NaN and infinity.
        if not (0 < principal <= 100000000 and 0 <= annual_rate <= 100):
            # Explain the allowed amount and rate ranges.
            return (
                "Use an amount up to 100000000 and above 0, and a rate from 0 to 100."
            )
        # Limit the loan term to one month through fifty years.
        if not 1 <= months <= 600:
            # Explain the allowed term range.
            return "Use whole-number months from 1 to 600."
        # Get the payment from the separate calculator.
        payment = self.loan_tool.monthly_payment(principal, annual_rate, months)
        # Check whether the calculator could not produce a result.
        if payment is None:
            # Avoid inventing a payment when calculation fails.
            return "I couldn't calculate that payment. Please check your inputs."
        # Display the estimate rounded to two decimal places.
        return (
            f"Estimated monthly payment: ${payment:.2f} (principal and interest only)."
        )
```


## tests/test_chatbot.py

```python
from chatbot import SupportChatbot
from mock_model import MockModel
from order_tool import OrderLookup
from stock_tool import StockLookup


# AI-assisted class: simulate a model that cannot answer.
class SilentModel:
    # Accept the same arguments as the real and mock models.
    def reply(self, instructions, history):
        # Signal that the chatbot should use its safe fallback.
        return None


def make_bot():
    """Build a fresh chatbot with tools and a mock model."""
    order_tool = OrderLookup({"A100": "shipped", "A101": "processing"})
    stock_tool = StockLookup({"rain jacket": 12, "day pack": 0})
    return SupportChatbot("Sunny", "Be friendly.", order_tool, stock_tool, MockModel())


def make_bot_with_silent_model():
    """Build a chatbot whose model cannot answer."""
    order_tool = OrderLookup({"A100": "shipped", "A101": "processing"})
    stock_tool = StockLookup({"rain jacket": 12, "day pack": 0})
    return SupportChatbot(
        "Sunny", "Be friendly.", order_tool, stock_tool, SilentModel()
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


def test_other_messages_go_to_the_model():
    bot = make_bot()
    assert bot.respond("hello") == "Hello! How can I help you today?"


def test_safe_reply_when_the_model_has_no_answer():
    bot = make_bot_with_silent_model()
    assert "try again" in bot.respond("hello")


def test_order_rule_does_not_need_the_model():
    bot = make_bot_with_silent_model()
    assert bot.respond("Where is order A100?") == "Order A100 is shipped."


def test_handoff_rule_does_not_need_the_model():
    bot = make_bot_with_silent_model()
    assert "human" in bot.respond("Please change my shipping address")


def test_echo_model_repeats_the_last_message():
    from echo_model import EchoModel

    order_tool = OrderLookup({"A100": "shipped"})
    stock_tool = StockLookup({"rain jacket": 12})
    bot = SupportChatbot("Sunny", "Be friendly.", order_tool, stock_tool, EchoModel())
    assert bot.respond("good morning") == "You said: good morning"
```


## tests/test_my_assistant.py

```python
import pytest

from mock_model import MockModel
from my_assistant import LoanAssistant
from my_tool import LoanCalculator


# AI-assisted class: simulate an unavailable model.
class SilentModel:
    # Match the model interface used by Penny.
    def reply(self, instructions, history):
        # Signal that no model answer is available.
        return None


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
    assert "Use: loan" in make_assistant().respond("loan")


def test_invalid_numbers_get_help():
    bot = make_assistant()
    assert "numeric" in bot.respond("loan abc 6 36")
    assert "above 0" in bot.respond("loan -100 6 36")
    assert "1 to 600" in bot.respond("loan 1000 6 0")


def test_unknown_request_gets_safe_reply():
    assert "not sure" in make_assistant().respond("What is the weather?")


def test_approval_request_goes_to_person():
    assert "loan officer" in make_assistant().respond("Can you approve my loan?")


def test_general_message_goes_to_model():
    assert make_assistant().respond("hello") == "Hello! How can I help you today?"


def test_model_unavailable_gets_safe_reply():
    bot = LoanAssistant("Penny", "Be friendly.", LoanCalculator(), SilentModel())
    assert "try again" in bot.respond("hello")


def test_rules_work_without_model():
    bot = LoanAssistant("Penny", "Be friendly.", LoanCalculator(), SilentModel())
    assert "$304.22" in bot.respond("loan 10000 6 36")
    assert "loan officer" in bot.respond("Can you approve my loan?")
```
