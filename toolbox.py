# toolbox.py
# Author: Sami Ali


# Define Toolbox to keep this responsibility in a separate object.
class Toolbox:
    """Every tool request from the model comes through here and is checked."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, order_tool, stock_tool, change_queue):
        """Hold the tools the model is allowed to ask for."""
        # Store self.order_tool for the following checks or operations.
        self.order_tool = order_tool
        # Store self.stock_tool for the following checks or operations.
        self.stock_tool = stock_tool
        # Store self.change_queue for the following checks or operations.
        self.change_queue = change_queue

    # Define tool_list so this operation can be called and tested separately.
    def tool_list(self):
        """Return the tools the model may ask for. They are not called here."""
        # Return [self.order_tool.look_up_order, self.order_tool.check_return, self.stock_tool.check_s...
        return [
            self.order_tool.look_up_order,
            self.order_tool.check_return,
            self.stock_tool.check_stock,
            self.change_queue.request_address_change,
        ]

    # Define run so this operation can be called and tested separately.
    def run(self, name, arguments, history):
        """Check one tool request. Run the tool only if every check passes."""
        # Check name in ['look_up_order', 'check_return'] before continuing.
        if name in ["look_up_order", "check_return"]:
            # Store order_id for the following checks or operations.
            order_id = self.clean(arguments, "order_id")
            # Check order_id == '' before continuing.
            if order_id == "":
                # Return 'The order ID is missing. Ask the customer for it.' to the caller.
                return "The order ID is missing. Ask the customer for it."
            # Check not self.customer_said(history, order_id) before continuing.
            if not self.customer_said(history, order_id):
                # Return 'The customer has not given that order ID. Ask them for it.' to the caller.
                return "The customer has not given that order ID. Ask them for it."
            # Check name == 'check_return' before continuing.
            if name == "check_return":
                # Return self.order_tool.check_return(order_id) to the caller.
                return self.order_tool.check_return(order_id)
            # Return self.order_tool.look_up_order(order_id) to the caller.
            return self.order_tool.look_up_order(order_id)
        # Check name == 'check_stock' before continuing.
        if name == "check_stock":
            # Store item for the following checks or operations.
            item = self.clean(arguments, "item")
            # Check item == '' before continuing.
            if item == "":
                # Return 'The product is missing. Ask the customer which product.' to the caller.
                return "The product is missing. Ask the customer which product."
            # Return self.stock_tool.check_stock(item) to the caller.
            return self.stock_tool.check_stock(item)
        # Check name == 'request_address_change' before continuing.
        if name == "request_address_change":
            # Store order_id for the following checks or operations.
            order_id = self.clean(arguments, "order_id")
            # Store new_address for the following checks or operations.
            new_address = self.clean(arguments, "new_address")
            # Check order_id == '' or new_address == '' before continuing.
            if order_id == "" or new_address == "":
                # Return 'The order ID and the new address are both needed.' to the caller.
                return "The order ID and the new address are both needed."
            # Check not self.customer_said(history, order_id) before continuing.
            if not self.customer_said(history, order_id):
                # Return 'The customer has not given that order ID. Ask them for it.' to the caller.
                return "The customer has not given that order ID. Ask them for it."
            # Check not self.customer_said(history, new_address) before continuing.
            if not self.customer_said(history, new_address):
                # Return 'The customer has not given that address. Ask them for it.' to the caller.
                return "The customer has not given that address. Ask them for it."
            # Return self.change_queue.request_address_change(order_id, new_address) to the caller.
            return self.change_queue.request_address_change(order_id, new_address)
        # Return f'There is no tool named {name}.' to the caller.
        return f"There is no tool named {name}."

    # Define clean so this operation can be called and tested separately.
    def clean(self, arguments, key):
        """Return one argument as text without extra spaces, or "" if it is missing."""
        # Return str(arguments.get(key, '')).strip() to the caller.
        return str(arguments.get(key, "")).strip()

    # Define customer_said so this operation can be called and tested separately.
    def customer_said(self, history, text):
        """Check customer-provided details."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
