# ollama_model.py
# Author: Sami Ali

# Import the dependency used by this file.
from ollama import ResponseError, chat


# Define OllamaModel to keep this responsibility in a separate object.
class OllamaModel:
    """A real AI model that runs on this computer through Ollama."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, model_name):
        """Remember which model to ask."""
        # Store self.model_name for the following checks or operations.
        self.model_name = model_name

    # Define reply so this operation can be called and tested separately.
    def reply(self, instructions, history):
        """Send the instructions and the conversation to the model. Return its reply."""
        # Store messages for the following checks or operations.
        messages = [{"role": "system", "content": instructions}]
        # Store messages for the following checks or operations.
        messages = messages + history
        # Attempt the operation while handling expected failures below.
        try:
            # Store response for the following checks or operations.
            response = chat(model=self.model_name, messages=messages)
        except ConnectionError:
            # Return None to the caller.
            return None
        except ResponseError:
            # Return None to the caller.
            return None
        # Return response.message.content to the caller.
        return response.message.content

    # Define decide so this operation can be called and tested separately.
    def decide(self, instructions, history, tools):
        """Send the conversation and the tools. Return a reply or a tool request."""
        # Store messages for the following checks or operations.
        messages = [{"role": "system", "content": instructions}]
        # Inspect each message in history.
        for message in history:
            # Check message['role'] == 'tool' before continuing.
            if message["role"] == "tool":
                # Store messages for the following checks or operations.
                messages = messages + self.tool_messages(message)
            else:
                # Run messages.append(message) to perform this step.
                messages.append(message)
        # Attempt the operation while handling expected failures below.
        try:
            # Store response for the following checks or operations.
            response = chat(model=self.model_name, messages=messages, tools=tools)
        except ConnectionError:
            # Return None to the caller.
            return None
        except ResponseError:
            # Return None to the caller.
            return None
        # Check response.message.tool_calls before continuing.
        if response.message.tool_calls:
            # Store call for the following checks or operations.
            call = response.message.tool_calls[0]
            # Return {'tool': call.function.name, 'arguments': call.function.arguments} to the caller.
            return {"tool": call.function.name, "arguments": call.function.arguments}
        # Return {'text': response.message.content} to the caller.
        return {"text": response.message.content}

    # Define tool_messages so this operation can be called and tested separately.
    def tool_messages(self, message):
        """Turn one tool entry into the two messages Ollama expects."""
        # Store name for the following checks or operations.
        name = message["tool_name"]
        # Store request for the following checks or operations.
        request = {"function": {"name": name, "arguments": message["arguments"]}}
        # Return [{'role': 'assistant', 'content': '', 'tool_calls': [request]}, {'role': 'tool', 'too...
        return [
            {"role": "assistant", "content": "", "tool_calls": [request]},
            {"role": "tool", "tool_name": name, "content": message["content"]},
        ]
