# change_queue.py
# Author: Sami Ali


# Define ChangeQueue to keep this responsibility in a separate object.
class ChangeQueue:
    """Changes waiting for a person to approve. Nothing changes until they do."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, order_tool):
        """Start with no requests. Approved changes go through the order tool."""
        # Store self.order_tool for the following checks or operations.
        self.order_tool = order_tool
        # Store self.requests for the following checks or operations.
        self.requests = []

    # Define request_address_change so this operation can be called and tested separately.
    def request_address_change(self, order_id, new_address):
        """Ask staff to change the shipping address on one order. Staff must approve it.

        Args:
            order_id: The order ID, like A100.
            new_address: The full new shipping address.
        """
        # Store order_id for the following checks or operations.
        order_id = order_id.upper()
        # Check self.order_tool.find_status(order_id) is None before continuing.
        if self.order_tool.find_status(order_id) is None:
            # Return 'No order with that ID was found. Order IDs look like A100.' to the caller.
            return "No order with that ID was found. Order IDs look like A100."
        # Store number for the following checks or operations.
        number = len(self.requests) + 1
        # Store request for the following checks or operations.
        request = {
            "number": number,
            "order_id": order_id,
            "new_address": new_address,
            "status": "waiting",
        }
        # Run self.requests.append(request) to perform this step.
        self.requests.append(request)
        # Return f'Request {number} was sent to staff. The address has not changed yet.' to the caller.
        return f"Request {number} was sent to staff. The address has not changed yet."

    # Define waiting so this operation can be called and tested separately.
    def waiting(self):
        """Return the requests that are still waiting for a decision."""
        # Store result for the following checks or operations.
        result = []
        # Inspect each request in self.requests.
        for request in self.requests:
            # Check request['status'] == 'waiting' before continuing.
            if request["status"] == "waiting":
                # Run result.append(request) to perform this step.
                result.append(request)
        # Return result to the caller.
        return result

    # Define find so this operation can be called and tested separately.
    def find(self, number):
        """Return the request with this number, or None."""
        # Inspect each request in self.requests.
        for request in self.requests:
            # Check request['number'] == number before continuing.
            if request["number"] == number:
                # Return request to the caller.
                return request
        # Return None to the caller.
        return None

    # Define approve so this operation can be called and tested separately.
    def approve(self, number):
        """Approve one waiting request and make the change."""
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
        # Store request['status'] for the following checks or operations.
        request["status"] = "approved"
        # Run self.order_tool.change_address(request['order_id'], request['new_address']) to perform t...
        self.order_tool.change_address(request["order_id"], request["new_address"])
        # Return f'Request {number} approved.' to the caller.
        return f"Request {number} approved."

    # Define reject so this operation can be called and tested separately.
    def reject(self, number):
        """Reject one waiting request. Nothing changes."""
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
        # Store request['status'] for the following checks or operations.
        request["status"] = "rejected"
        # Return f'Request {number} rejected.' to the caller.
        return f"Request {number} rejected."
