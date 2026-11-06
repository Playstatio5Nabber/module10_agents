# Author: Sami Ali

# Define an assistant that combines loan rules, a tool, and a model.
class LoanAssistant:
    # Receive the name, instructions, calculation tool, and model.
    def __init__(self, name, instructions, loan_tool, model):
        # Store the assistant's display name.
        self.name = name
        # Store the instructions for general questions.
        self.instructions = instructions
        # Store the separate loan calculator.
        self.loan_tool = loan_tool
        # Store the supplied model.
        self.model = model
        # Start this assistant's own conversation history.
        self.history = []

    # Record the customer message and assistant response.
    def respond(self, user_message):
        # Save the customer message before choosing a reply.
        self.history.append({"role": "user", "content": user_message})
        # Apply rules first, then use the model if needed.
        reply = self.choose_reply(user_message)
        # Save the reply for later conversation turns.
        self.history.append({"role": "assistant", "content": reply})
        # Return the reply for display.
        return reply

    # Route requests to a human, the calculator, or the model.
    def choose_reply(self, user_message):
        # Normalize capitalization and remove outside spaces.
        text = user_message.lower().strip()
        # Check topics that need human judgment first.
        for word in ["approve", "approval", "qualify", "advice"]:
            # Look for this handoff keyword.
            if word in text:
                # Give the fixed loan-officer handoff.
                return "Please contact a loan officer for approval or personal advice."
        # Split the message into command words.
        parts = text.split()
        # Recognize the loan calculation command.
        if parts and parts[0] == "loan":
            # Use the calculator instead of asking the model.
            return self.loan_reply(parts)
        # Ask the model about requests outside the rules.
        reply = self.model.reply(self.instructions, self.history)
        # Check the model's no-answer signal.
        if reply is None:
            # Return a safe message when the model is unavailable.
            return "Sorry, I can't answer that right now. Please try again in a moment."
        # Return the model's answer.
        return reply

    # Validate a loan command and ask the calculation tool.
    def loan_reply(self, parts):
        # Require the command and exactly three values.
        if len(parts) != 4:
            # Show the correct command format.
            return "Use: loan AMOUNT ANNUAL_RATE MONTHS. Example: loan 10000 6 36"
        # Attempt to convert the supplied values into numbers.
        try:
            # Read the borrowed amount.
            principal = float(parts[1])
            # Read the annual interest percentage.
            annual_rate = float(parts[2])
            # Read the loan term as a whole number of months.
            months = int(parts[3])
        # Handle values that cannot be converted.
        except ValueError:
            # Explain the required number formats.
            return "Enter numeric amounts and rates, and whole-number months."
        # Reject unsupported amounts and rates, including NaN and infinity.
        if not (0 < principal <= 100000000 and 0 <= annual_rate <= 100):
            # Explain the allowed amount and rate ranges.
            return (
                "Use an amount up to 100000000 and above 0, and a rate from 0 to 100."
            )
        # Limit the loan term to one month through fifty years.
        if not 1 <= months <= 600:
            # Explain the allowed term range.
            return "Use whole-number months from 1 to 600."
        # Get the payment from the separate calculator.
        payment = self.loan_tool.monthly_payment(principal, annual_rate, months)
        # Check whether the calculator could not produce a result.
        if payment is None:
            # Avoid inventing a payment when calculation fails.
            return "I couldn't calculate that payment. Please check your inputs."
        # Display the estimate rounded to two decimal places.
        return (
            f"Estimated monthly payment: ${payment:.2f} (principal and interest only)."
        )
