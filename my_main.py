# Author: Sami Ali

from my_assistant import LoanAssistant
from my_tool import LoanCalculator
from ollama_model import OllamaModel

INSTRUCTIONS = """You are Penny, an assistant for a fictional lending business.
Answer in one short sentence.
The office is open Monday through Friday from 9 am to 5 pm.
Payment estimates include principal and interest only; they exclude fees and insurance.
Only state facts from these instructions.
If you do not know, say so and refer the customer to a loan officer.
Never promise approval or invent interest rates."""

# Create the calculation tool and give it to the assistant.
tool = LoanCalculator()
model = OllamaModel("granite4.1:3b")
bot = LoanAssistant("Penny", INSTRUCTIONS, tool, model)

print("Type: loan AMOUNT ANNUAL_RATE MONTHS")
print("Example: loan 10000 6 36")
print("Type quit to stop.")

# Read the first message.
user_message = input("You: ")

# Continue until the customer enters quit, ignoring case and outside spaces.
while user_message.strip().lower() != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")
