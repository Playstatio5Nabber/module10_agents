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
