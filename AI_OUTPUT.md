# Lab 11 AI output

Generated with Codex. Comments explain the generated class statements. This preserves the generated source for the assignment disclosure.

## mock_model.py

```python
# Author: Sami Ali
# AI-generated class; each executable line is explained below.
# Define the interchangeable stand-in used without Ollama.
class MockModel:
    # Match the interface expected by both assistants.
    def reply(self, instructions, history):
        # Read the newest user message, ignoring capitalization.
        last_message = history[-1]["content"].lower()
        # Recognize a greeting for a predictable test response.
        if "hello" in last_message:
            # Return the same greeting on every run.
            return "Hello! How can I help you today?"
        # Give a predictable fallback for all other messages.
        return "I'm not sure how to help with that. I can check an order or stock."

```

## echo_model.py

```python
# Author: Sami Ali
# AI-generated class; each executable line is explained below.
# Define another model with the same reply interface.
class EchoModel:
    # Accept instructions and history so the chatbot can use this model.
    def reply(self, instructions, history):
        # Repeat the last message to demonstrate interchangeable models.
        return "You said: " + history[-1]["content"]

```

## ollama_model.py

```python
# Author: Sami Ali
from ollama import ResponseError, chat


# AI-generated class; each executable line is explained below.
# Adapt the local Ollama service to the chatbot's model interface.
class OllamaModel:
    # Receive the downloaded model's name.
    def __init__(self, model_name):
        # Keep the name for later requests.
        self.model_name = model_name

    # Accept the assistant's instructions and recorded conversation.
    def reply(self, instructions, history):
        # Put the instructions first as a system message.
        messages = [{"role": "system", "content": instructions}]
        # Include the conversation without changing the original history.
        messages = messages + history
        # Attempt a request that can fail if the service is unavailable.
        try:
            # Ask the selected local model to complete the conversation.
            response = chat(model=self.model_name, messages=messages)
        # Handle an unavailable Ollama service.
        except ConnectionError:
            # Signal the assistant to use its safe fallback.
            return None
        # Handle service errors such as a missing downloaded model.
        except ResponseError:
            # Use the same failure signal for service errors.
            return None
        # Return the model's text to the assistant.
        return response.message.content

```

## chatbot.py

```python
# chatbot.py
# Author: Sami Ali

HANDOFF_WORDS = ["address", "payment", "card"]


# Define the assistant that combines rules, tools, and a replaceable model.
class SupportChatbot:
    """A support chatbot. Rules handle what must be right. A model handles the rest."""

    # Receive the name, instructions, two tools, and model for this instance.
    def __init__(self, name, instructions, order_tool, stock_tool, model):
        """Store the collaborators and create an independent history."""
        # Store the display name for the running program.
        self.name = name
        # Save the instructions sent with every model request.
        self.instructions = instructions
        # Save the order lookup so order facts come from data.
        self.order_tool = order_tool
        # Store the stock tool so other methods can use it.
        self.stock_tool = stock_tool
        # Store the supplied model for messages outside the rules.
        self.model = model
        # Give this chatbot its own initially empty conversation.
        self.history = []

    # Manage one user message and one assistant response.
    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, and return it."""
        # Record the user before choosing a reply so the model sees this question.
        self.history.append({"role": "user", "content": user_message})
        # Select a reply using rules before consulting the model.
        reply = self.choose_reply(user_message)
        # Save the response so later calls see the whole conversation.
        self.history.append({"role": "assistant", "content": reply})
        return reply

    # Route messages to the handoff, tools, or model in that order.
    def choose_reply(self, user_message):
        """Apply rules first and ask the model for other messages."""
        # Ignore capitalization when checking rule keywords.
        text = user_message.lower()
        # Give sensitive requests priority over tool and model answers.
        if self.needs_human(text):
            # Return the fixed handoff message without asking the model.
            return "I can't help with that here. I'm passing you to a human agent."
        # Recognize order requests before general model questions.
        if "order" in text:
            # Get the order response from the order tool.
            return self.order_reply(user_message)
        # Check whether the customer is asking about stock.
        if "stock" in text:
            # Use the stock reply method to answer.
            return self.stock_reply(user_message)
        # Ask the supplied model only after the rules have been checked.
        return self.model_reply()

    # Ask the model through the common reply interface.
    def model_reply(self):
        # Pass the instructions and complete conversation, including this question.
        reply = self.model.reply(self.instructions, self.history)
        # Detect the failure signal returned by an unavailable model.
        if reply is None:
            # Give a safe answer instead of inventing information.
            return "Sorry, I can't answer that right now. Please try again in a moment."
        # Return the model's answer when it supplied one.
        return reply

    # Check whether the request matches a human-only topic.
    def needs_human(self, text):
        """Return True if the message is about something a person must handle."""
        # Examine every configured handoff keyword.
        for word in HANDOFF_WORDS:
            # Detect this keyword anywhere in the normalized message.
            if word in text:
                # Report that a human is required.
                return True
        # Report that no handoff keyword matched.
        return False

    # Build an answer from the order lookup tool.
    def order_reply(self, user_message):
        """Use the order tool to answer a question about an order."""
        # Extract a known order ID from the original message.
        order_id = self.order_tool.find_order_id(user_message)
        # Detect a message without a recognized order ID.
        if order_id is None:
            # Ask for an ID rather than inventing a status.
            return "Which order? Please send an order ID like A100."
        # Read the actual stored order status.
        status = self.order_tool.find_status(order_id)
        # Format the tool result for the customer.
        return f"Order {order_id} is {status}."
        # Define a method that needs only the current chatbot object.

    def count_user_messages(self):
        # Start at zero before checking the conversation.
        count = 0
        # Look at each saved message.
        for message in self.history:
            # Count only user messages, excluding assistant replies.
            if message["role"] == "user":
                # Add one for each user message found.
                count += 1
        # Return the total after checking every message.
        return count
        # Define a method to answer stock questions.

    def stock_reply(self, user_message):
        # Find a known product mentioned in the message.
        product = self.stock_tool.find_product(user_message)
        # Check whether no known product was found.
        if product is None:
            # Ask the customer to name a product.
            return "Which product? Please name the item you want me to check."
        # Look up the product's stock count using the tool.
        count = self.stock_tool.count_for(product)
        # Build a reply containing the count and product name.
        return f"We have {count} of the {product} in stock."

```

## my_assistant.py

```python
# Author: Sami Ali

# Define an assistant that uses a separate loan tool.
class LoanAssistant:
    # Receive the name, factual instructions, calculation tool, and model.
    def __init__(self, name, instructions, loan_tool, model):
        # Store the name for greetings and printed replies.
        self.name = name
        # Store the tool instead of putting calculations in the assistant.
        self.loan_tool = loan_tool
        # Store the factual instructions for general model questions.
        self.instructions = instructions
        # Store the interchangeable model supplied by the caller.
        self.model = model
        # Create a separate conversation history for this assistant.
        self.history = []

    # Record both messages for each conversation turn.
    def respond(self, user_message):
        # Save the customer's original message.
        self.history.append({"role": "user", "content": user_message})
        # Choose a reply using the assistant's rules.
        reply = self.choose_reply(user_message)
        # Save the assistant's reply.
        self.history.append({"role": "assistant", "content": reply})
        # Return the reply so the main program can display it.
        return reply
        # Choose a response using simple keyword rules.

    def choose_reply(self, user_message):
        # Normalize capitalization and remove outside spaces.
        text = user_message.lower().strip()
        # Check requests requiring a person's judgment.
        for word in ["approve", "approval", "qualify", "advice"]:
            # Look for each handoff keyword in the message.
            if word in text:
                # Explain the limitation and direct the customer to a person.
                return "Please contact a loan officer for approval or personal advice."
        # Split the message into individual words.
        parts = text.split()
        # Recognize the loan calculation command.
        if parts and parts[0] == "loan":
            # Pass the words to the calculation reply method.
            return self.loan_reply(parts)
        # Send messages outside the calculation and handoff rules to the model.
        reply = self.model.reply(self.instructions, self.history)
        # Detect an unavailable model before returning its answer.
        if reply is None:
            # Give a safe retry message without inventing lending information.
            return "Sorry, I can't answer that right now. Please try again in a moment."
        # Return the model answer when one is available.
        return reply

    def loan_reply(self, parts):
        # Require the command plus exactly three values.
        if len(parts) != 4:
            # Show the expected input when values are missing or extra.
            return "Use: loan AMOUNT ANNUAL_RATE MONTHS. Example: loan 10000 6 36"
        # Try converting the typed values into numbers.
        try:
            # Read the amount borrowed as a decimal number.
            principal = float(parts[1])
            # Read the annual interest percentage as a decimal number.
            annual_rate = float(parts[2])
            # Require the number of months to be a whole number.
            months = int(parts[3])
        # Handle text that cannot be converted into the required numbers.
        except ValueError:
            # Explain how to correct the input.
            return "Enter numeric amounts and rates, and whole-number months."
        # Limit inputs to a supported range, also rejecting NaN and infinity.
        if not (0 < principal <= 100000000 and 0 <= annual_rate <= 100):
            # Explain the supported amount and rate ranges.
            return (
                "Use an amount up to 100000000 and above 0, and a rate from 0 to 100."
            )
        # Limit the term to between one month and fifty years.
        if not 1 <= months <= 600:
            # Explain the supported term range.
            return "Use whole-number months from 1 to 600."
        # Ask the separate tool to calculate the payment.
        payment = self.loan_tool.monthly_payment(principal, annual_rate, months)
        # Handle a calculation that returns no result.
        if payment is None:
            # Give a helpful reply instead of making up a payment.
            return "I couldn't calculate that payment. Please check your inputs."
        # Show the estimate with two decimal places.
        return (
            f"Estimated monthly payment: ${payment:.2f} (principal and interest only)."
        )

```

## tests/test_chatbot.py

```python
from chatbot import SupportChatbot
from echo_model import EchoModel
from mock_model import MockModel
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
        MockModel(),
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


# AI-generated class: define a model that simulates an unavailable service.
class SilentModel:
    # Accept the common model arguments so either chatbot can use this object.
    def reply(self, instructions, history):
        # Signal that no answer is available, exercising the safe fallback.
        return None


def make_bot_with_silent_model():
    bot = make_bot()
    bot.model = SilentModel()
    return bot


def test_other_messages_go_to_the_model():
    assert make_bot().respond("hello") == "Hello! How can I help you today?"


def test_safe_reply_when_the_model_has_no_answer():
    assert "try again" in make_bot_with_silent_model().respond("hello")


def test_order_rule_does_not_need_the_model():
    assert (
        make_bot_with_silent_model().respond("Where is order A100?")
        == "Order A100 is shipped."
    )


def test_handoff_rule_does_not_need_the_model():
    assert "human" in make_bot_with_silent_model().respond(
        "Please change my shipping address"
    )


def test_echo_model_can_be_given_to_chatbot():
    bot = make_bot()
    bot.model = EchoModel()
    assert bot.respond("good morning") == "You said: good morning"

```

