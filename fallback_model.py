# Author: Sami Ali
# Define FallbackModel to keep this responsibility in a separate object.
class FallbackModel:
    """Try a backup model only when the primary model is unavailable."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, primary, backup):
        # Store self.primary for the following checks or operations.
        self.primary = primary
        # Store self.backup for the following checks or operations.
        self.backup = backup

    # Define decide so this operation can be called and tested separately.
    def decide(self, instructions, history, tools):
        # Store decision for the following checks or operations.
        decision = self.primary.decide(instructions, history, tools)
        # Check decision is None before continuing.
        if decision is None:
            # Return self.backup.decide(instructions, history, tools) to the caller.
            return self.backup.decide(instructions, history, tools)
        # Return decision to the caller.
        return decision
