# Author: Sami Ali
# Import the dependency used by this file.
from change_queue import ChangeQueue


# Define LoanQueue to keep this responsibility in a separate object.
class LoanQueue(ChangeQueue):
    """Queue fictional estimate saves; no application or loan is approved."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, calculator):
        # Store self.calculator for the following checks or operations.
        self.calculator = calculator
        # Store self.requests for the following checks or operations.
        self.requests = []

    # Define request_save_estimate so this operation can be called and tested separately.
    def request_save_estimate(self, label, principal, annual_rate, months):
        """Ask staff to save an estimate; do not save it yet.

        Args:
            label: The customer-supplied estimate label.
            principal: The borrowed amount as text.
            annual_rate: The annual percentage as text.
            months: The term in whole months as text.
        """
        # Store values for the following checks or operations.
        values = self.calculator.validated(principal, annual_rate, months)
        # Check not label.strip() or values is None before continuing.
        if not label.strip() or values is None:
            # Return 'A label and valid loan values are required.' to the caller.
            return "A label and valid loan values are required."
        # Store number for the following checks or operations.
        number = len(self.requests) + 1
        # Run self.requests.append({'number': number, 'label': label, 'values': values, 'status': 'wai...
        self.requests.append(
            {"number": number, "label": label, "values": values, "status": "waiting"}
        )
        # Return f'Request {number} sent to staff. The estimate has not been saved yet.' to the caller.
        return f"Request {number} sent to staff. The estimate has not been saved yet."

    # Define approve so this operation can be called and tested separately.
    def approve(self, number):
        # Store request for the following checks or operations.
        request = self.find(number)
        # Check request is None before continuing.
        if request is None:
            # Return f'There is no request {number}.' to the caller.
            return f"There is no request {number}."
        # Check request['status'] != 'waiting' before continuing.
        if request["status"] != "waiting":
            # Return f"Request {number} is already {request['status']}." to the caller.
            return f"Request {number} is already {request['status']}."
        # Run self.calculator.save_estimate(request['label'], request['values']) to perform this step.
        self.calculator.save_estimate(request["label"], request["values"])
        # Store request['status'] for the following checks or operations.
        request["status"] = "approved"
        # Return f'Request {number} approved.' to the caller.
        return f"Request {number} approved."
