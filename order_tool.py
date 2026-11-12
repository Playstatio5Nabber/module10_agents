# order_tool.py
# Author: Sami Ali


# Define OrderLookup to keep this responsibility in a separate object.
class OrderLookup:
    """A tool that knows about orders. It knows nothing about chatting."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, orders):
        """Store the orders this tool can look up."""
        # Store self.orders for the following checks or operations.
        self.orders = orders

    # Define find_order_id so this operation can be called and tested separately.
    def find_order_id(self, text):
        """Return the first known order ID mentioned in text, or None."""
        # Inspect each order_id in self.orders.
        for order_id in self.orders:
            # Check order_id in text.upper() before continuing.
            if order_id in text.upper():
                # Return order_id to the caller.
                return order_id
        # Return None to the caller.
        return None

    # Define find_status so this operation can be called and tested separately.
    def find_status(self, order_id):
        """Return the status of one order, or None if there is no such order."""
        # Check order_id in self.orders before continuing.
        if order_id in self.orders:
            # Return self.orders[order_id]['status'] to the caller.
            return self.orders[order_id]["status"]
        # Return None to the caller.
        return None

    # Define look_up_order so this operation can be called and tested separately.
    def look_up_order(self, order_id):
        """Look up the status of one order.

        Args:
            order_id: The order ID, like A100.
        """
        # Store found for the following checks or operations.
        found = self.find_order_id(order_id)
        # Check found is None before continuing.
        if found is None:
            # Return 'No order with that ID was found. Order IDs look like A100.' to the caller.
            return "No order with that ID was found. Order IDs look like A100."
        # Return f'Order {found} is {self.find_status(found)}.' to the caller.
        return f"Order {found} is {self.find_status(found)}."

    # Define change_address so this operation can be called and tested separately.
    def change_address(self, order_id, new_address):
        """Change the shipping address on one order. Only an approval calls this."""
        # Store self.orders[order_id]['address'] for the following checks or operations.
        self.orders[order_id]["address"] = new_address

    # Define check_return so this operation can be called and tested separately.
    def check_return(self, order_id):
        """Check whether an order has reached the return stage.

        Args:
            order_id: The order ID, like A100.
        """
        # Store status for the following checks or operations.
        status = self.find_status(order_id.upper())
        # Check status is None before continuing.
        if status is None:
            # Return 'No order with that ID was found. Order IDs look like A100.' to the caller.
            return "No order with that ID was found. Order IDs look like A100."
        # Check status == 'delivered' before continuing.
        if status == "delivered":
            # Return 'This delivered order can be returned within 30 days with a receipt.' to the caller.
            return "This delivered order can be returned within 30 days with a receipt."
        # Return 'This order cannot be returned yet.' to the caller.
        return "This order cannot be returned yet."
