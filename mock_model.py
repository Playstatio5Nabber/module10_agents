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
