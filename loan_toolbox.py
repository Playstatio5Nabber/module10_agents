# Author: Sami Ali
# Import the dependency used by this file.
import re

# Import the dependency used by this file.
from toolbox import Toolbox


# Define LoanToolbox to keep this responsibility in a separate object.
class LoanToolbox(Toolbox):
    """Check all model-requested calculations and estimate-save requests."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, calculator, queue):
        # Store self.calculator for the following checks or operations.
        self.calculator = calculator
        # Store self.change_queue for the following checks or operations.
        self.change_queue = queue

    # Define tool_list so this operation can be called and tested separately.
    def tool_list(self):
        # Return [self.calculator.estimate_payment, self.change_queue.request_save_estimate] to the ca...
        return [
            self.calculator.estimate_payment,
            self.change_queue.request_save_estimate,
        ]

    # Define customer_said so this operation can be called and tested separately.
    def customer_said(self, history, text):
        # Check not text before continuing.
        if not text:
            # Return False to the caller.
            return False
        # Store pattern for the following checks or operations.
        pattern = r"(?<![\w.])" + re.escape(text) + r"(?![\w.])"
        # Inspect each message in history.
        for message in history:
            # Check message['role'] == 'user' and re.search(pattern, message['content'], re.IGNORECASE) be...
            if message["role"] == "user" and re.search(
                pattern, message["content"], re.IGNORECASE
            ):
                # Return True to the caller.
                return True
        # Return False to the caller.
        return False

    # Define run so this operation can be called and tested separately.
    def run(self, name, arguments, history):
        # Check name not in ['estimate_payment', 'request_save_estimate'] before continuing.
        if name not in ["estimate_payment", "request_save_estimate"]:
            # Return f'There is no tool named {name}.' to the caller.
            return f"There is no tool named {name}."
        # Store keys for the following checks or operations.
        keys = ["principal", "annual_rate", "months"]
        # Check name == 'request_save_estimate' before continuing.
        if name == "request_save_estimate":
            # Store keys for the following checks or operations.
            keys = ["label"] + keys
        # Store values for the following checks or operations.
        values = {}
        # Inspect each key in keys.
        for key in keys:
            # Store value for the following checks or operations.
            value = self.clean(arguments, key)
            # Check value == '' before continuing.
            if value == "":
                # Return f'The {key} is missing. Ask the customer for it.' to the caller.
                return f"The {key} is missing. Ask the customer for it."
            # Check not self.customer_said(history, value) before continuing.
            if not self.customer_said(history, value):
                # Return f'The customer has not given that {key}. Ask them for it.' to the caller.
                return f"The customer has not given that {key}. Ask them for it."
            # Store values[key] for the following checks or operations.
            values[key] = value
        # Check name == 'estimate_payment' before continuing.
        if name == "estimate_payment":
            # Return self.calculator.estimate_payment(**values) to the caller.
            return self.calculator.estimate_payment(**values)
        # Return self.change_queue.request_save_estimate(**values) to the caller.
        return self.change_queue.request_save_estimate(**values)
