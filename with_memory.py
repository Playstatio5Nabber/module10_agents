# Author: Sami Ali
from ollama import chat

MODEL_NAME = "granite4.1:3b"
INSTRUCTIONS = "You are Sunny, a support assistant for Bayside Outfitters. Answer in one short sentence."
messages = [{"role": "system", "content": INSTRUCTIONS}]
for question in ["Hello, my name is Dana.", "What is my name?"]:
    messages.append({"role": "user", "content": question})
    response = chat(model=MODEL_NAME, messages=messages)
    print(response.message.content)
    messages.append({"role": "assistant", "content": response.message.content})
print(len(messages))
