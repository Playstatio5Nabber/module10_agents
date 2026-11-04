# Author: Sami Ali
# AI-generated class; each executable line is explained below.
# Define another model with the same reply interface.
class EchoModel:
    # Accept instructions and history so the chatbot can use this model.
    def reply(self, instructions, history):
        # Repeat the last message to demonstrate interchangeable models.
        return "You said: " + history[-1]["content"]
