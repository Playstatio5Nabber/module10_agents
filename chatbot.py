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
