# Author: Sami Ali
# Import the dependency used by this file.
from chatbot import SupportChatbot


# Define LoanAssistant to keep this responsibility in a separate object.
class LoanAssistant(SupportChatbot):
    """Use the limited tool loop while keeping lending decisions with people."""

    # Define choose_reply so this operation can be called and tested separately.
    def choose_reply(self, user_message):
        # Check self.needs_human(user_message.lower()) before continuing.
        if self.needs_human(user_message.lower()):
            # Return 'Please contact a loan officer for approval or personal advice.' to the caller.
            return "Please contact a loan officer for approval or personal advice."
        # Return self.model_reply() to the caller.
        return self.model_reply()

    # Define needs_human so this operation can be called and tested separately.
    def needs_human(self, text):
        # Inspect each word in ['approve', 'approval', 'qualify', 'advice'].
        for word in ["approve", "approval", "qualify", "advice"]:
            # Check word in text before continuing.
            if word in text:
                # Return True to the caller.
                return True
        # Return False to the caller.
        return False
