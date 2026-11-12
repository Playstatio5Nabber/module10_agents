# Author: Sami Ali
# Import the dependency used by this file.
from loan_queue import LoanQueue

# Import the dependency used by this file.
from loan_toolbox import LoanToolbox

# Import the dependency used by this file.
from my_assistant import LoanAssistant

# Import the dependency used by this file.
from my_tool import LoanCalculator

# Import the dependency used by this file.
from ollama_model import OllamaModel

# Store INSTRUCTIONS for the following checks or operations.
INSTRUCTIONS = """You are Penny, an assistant for a fictional lending business.
Answer in one short sentence.
The office is open Monday through Friday from 9 am to 5 pm.
Payment estimates include principal and interest only, excluding fees and insurance.
Use only facts in these instructions or tool results. Never invent a rate or promise approval.
If the customer only says hello, greet them and ask how you can help.
Ask for missing amount, annual percentage, and term in whole months before estimating.
Use exactly the customer's numeric text in tool arguments, without commas or currency signs.
Only request an estimate save when the customer explicitly asks to save and supplies a label.
A save request waits for staff; never say it is saved before approval.
If you do not know, say so and refer the customer to a loan officer."""


# Define main so this operation can be called and tested separately.
def main():
    # Store calculator for the following checks or operations.
    calculator = LoanCalculator()
    # Store queue for the following checks or operations.
    queue = LoanQueue(calculator)
    # Store tools for the following checks or operations.
    tools = LoanToolbox(calculator, queue)
    # Store model for the following checks or operations.
    model = OllamaModel("granite4.1:3b")
    # Store bot for the following checks or operations.
    bot = LoanAssistant("Penny", INSTRUCTIONS, tools, model)
    # Run print('Ask for a payment estimate using an amount, annual rate, and months.') to perform...
    print("Ask for a payment estimate using an amount, annual rate, and months.")
    # Run print('Use fictional values. Type quit to stop.') to perform this step.
    print("Use fictional values. Type quit to stop.")
    # Repeat while True, keeping the loop bounded.
    while True:
        # Store message for the following checks or operations.
        message = input("You: ")
        # Check message.strip().lower() == 'quit' before continuing.
        if message.strip().lower() == "quit":
            # Leave the loop when the stopping condition has been met.
            break
        # Run print(f'{bot.name}: {bot.respond(message)}') to perform this step.
        print(f"{bot.name}: {bot.respond(message)}")
    # Run print('Staff review (saving estimates only, not approving loans)') to perform this step.
    print("Staff review (saving estimates only, not approving loans)")
    # Inspect each request in queue.waiting().
    for request in queue.waiting():
        # Store number for the following checks or operations.
        number = request["number"]
        # Run print(f"Request {number}: {request['label']}, {request['values']}") to perform this step.
        print(f"Request {number}: {request['label']}, {request['values']}")
        # Check input('Approve save? yes or no: ') == 'yes' before continuing.
        if input("Approve save? yes or no: ") == "yes":
            # Run print(queue.approve(number)) to perform this step.
            print(queue.approve(number))
        else:
            # Run print(queue.reject(number)) to perform this step.
            print(queue.reject(number))
    # Run print('Saved estimates:', calculator.saved_estimates) to perform this step.
    print("Saved estimates:", calculator.saved_estimates)


# Check __name__ == '__main__' before continuing.
if __name__ == "__main__":
    # Run main() to perform this step.
    main()
