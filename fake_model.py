# fake_model.py
# Author: Sami Ali


# Define FakeModel to keep this responsibility in a separate object.
class FakeModel:
    """A model for tests. It plays back a list of decisions, one per call."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, decisions):
        """Store the decisions to play back, in order."""
        # Store self.decisions for the following checks or operations.
        self.decisions = decisions
        # Store self.calls for the following checks or operations.
        self.calls = 0

    # Define decide so this operation can be called and tested separately.
    def decide(self, instructions, history, tools):
        """Return the next decision in the list."""
        # Store decision for the following checks or operations.
        decision = self.decisions[self.calls]
        # Update self.calls after this step.
        self.calls += 1
        # Return decision to the caller.
        return decision
