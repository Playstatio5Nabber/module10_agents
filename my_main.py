# Author: Sami Ali

from my_assistant import LoanAssistant
from my_tool import LoanCalculator

# Create the calculation tool and give it to the assistant.
tool = LoanCalculator()
bot = LoanAssistant("Penny", tool)

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
