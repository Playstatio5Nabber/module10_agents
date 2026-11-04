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
