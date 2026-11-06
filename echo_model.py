# echo_model.py
# Author: Sami Ali
# AI assistance: ChatGPT provided this class with explanations.

# Define a model that repeats the customer's latest message.
class EchoModel:
    # Match the model interface used by the chatbot.
    def reply(self, instructions, history):
        # Prefix the last message's content with "You said: ".
        return "You said: " + history[-1]["content"]
