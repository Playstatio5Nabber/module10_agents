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
