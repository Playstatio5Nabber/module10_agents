# Author: Sami Ali

# Define an assistant that uses a separate loan tool.
class LoanAssistant:
    # Receive the name, factual instructions, calculation tool, and model.
    def __init__(self, name, instructions, loan_tool, model):
        # Store the name for greetings and printed replies.
        self.name = name
        # Store the tool instead of putting calculations in the assistant.
        self.loan_tool = loan_tool
        # Store the factual instructions for general model questions.
        self.instructions = instructions
        # Store the interchangeable model supplied by the caller.
        self.model = model
        # Create a separate conversation history for this assistant.
        self.history = []

    # Record both messages for each conversation turn.
    def respond(self, user_message):
        # Save the customer's original message.
        self.history.append({"role": "user", "content": user_message})
        # Choose a reply using the assistant's rules.
        reply = self.choose_reply(user_message)
        # Save the assistant's reply.
        self.history.append({"role": "assistant", "content": reply})
        # Return the reply so the main program can display it.
        return reply
        # Choose a response using simple keyword rules.

    def choose_reply(self, user_message):
        # Normalize capitalization and remove outside spaces.
        text = user_message.lower().strip()
        # Check requests requiring a person's judgment.
        for word in ["approve", "approval", "qualify", "advice"]:
            # Look for each handoff keyword in the message.
            if word in text:
                # Explain the limitation and direct the customer to a person.
                return "Please contact a loan officer for approval or personal advice."
        # Split the message into individual words.
        parts = text.split()
        # Recognize the loan calculation command.
        if parts and parts[0] == "loan":
            # Pass the words to the calculation reply method.
            return self.loan_reply(parts)
        # Send messages outside the calculation and handoff rules to the model.
        reply = self.model.reply(self.instructions, self.history)
        # Detect an unavailable model before returning its answer.
        if reply is None:
            # Give a safe retry message without inventing lending information.
            return "Sorry, I can't answer that right now. Please try again in a moment."
        # Return the model answer when one is available.
        return reply

    def loan_reply(self, parts):
        # Require the command plus exactly three values.
        if len(parts) != 4:
            # Show the expected input when values are missing or extra.
            return "Use: loan AMOUNT ANNUAL_RATE MONTHS. Example: loan 10000 6 36"
        # Try converting the typed values into numbers.
        try:
            # Read the amount borrowed as a decimal number.
            principal = float(parts[1])
            # Read the annual interest percentage as a decimal number.
            annual_rate = float(parts[2])
            # Require the number of months to be a whole number.
            months = int(parts[3])
        # Handle text that cannot be converted into the required numbers.
        except ValueError:
            # Explain how to correct the input.
            return "Enter numeric amounts and rates, and whole-number months."
        # Limit inputs to a supported range, also rejecting NaN and infinity.
        if not (0 < principal <= 100000000 and 0 <= annual_rate <= 100):
            # Explain the supported amount and rate ranges.
            return (
                "Use an amount up to 100000000 and above 0, and a rate from 0 to 100."
            )
        # Limit the term to between one month and fifty years.
        if not 1 <= months <= 600:
            # Explain the supported term range.
            return "Use whole-number months from 1 to 600."
        # Ask the separate tool to calculate the payment.
        payment = self.loan_tool.monthly_payment(principal, annual_rate, months)
        # Handle a calculation that returns no result.
        if payment is None:
            # Give a helpful reply instead of making up a payment.
            return "I couldn't calculate that payment. Please check your inputs."
        # Show the estimate with two decimal places.
        return (
            f"Estimated monthly payment: ${payment:.2f} (principal and interest only)."
        )
