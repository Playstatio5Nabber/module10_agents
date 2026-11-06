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
