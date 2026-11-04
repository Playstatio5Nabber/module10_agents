# chatbot.py
# Author: Sami Ali

HANDOFF_WORDS = ["address", "payment", "card"]


class SupportChatbot:
    """A mock support chatbot. Its replies come from simple rules, not from AI."""

    def __init__(self, name, instructions, order_tool, stock_tool):
        """Set up one chatbot with its own name, instructions, tool, and history."""
        self.name = name
        self.instructions = instructions
        self.order_tool = order_tool
        # Store the stock tool so other methods can use it.
        self.stock_tool = stock_tool
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Choose a reply with keyword rules. This is the mock part."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't help with that here. I'm passing you to a human agent."
        if "order" in text:
            return self.order_reply(user_message)
        # Check whether the customer is asking about stock.
        if "stock" in text:
            # Use the stock reply method to answer.
            return self.stock_reply(user_message)
        if "hello" in text:
            return f"Hello! I'm {self.name}. I can check an order status for you."
        return "I'm not sure how to help with that. I can check an order status."

    def needs_human(self, text):
        """Return True if the message is about something a person must handle."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def order_reply(self, user_message):
        """Use the order tool to answer a question about an order."""
        order_id = self.order_tool.find_order_id(user_message)
        if order_id is None:
            return "Which order? Please send an order ID like A100."
        status = self.order_tool.find_status(order_id)
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
