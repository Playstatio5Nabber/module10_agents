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
