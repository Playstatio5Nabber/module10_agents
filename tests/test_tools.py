# Import the dependency used by this file.
from change_queue import ChangeQueue

# Import the dependency used by this file.
from order_tool import OrderLookup

# Import the dependency used by this file.
from stock_tool import StockLookup

# Import the dependency used by this file.
from toolbox import Toolbox


# Define make_tools so this operation can be called and tested separately.
def make_tools():
    """Build fresh tools with two orders for each test."""
    # Store orders for the following checks or operations.
    orders = {
        "A100": {"status": "shipped", "address": "14 Bay Road"},
        "A101": {"status": "processing", "address": "3 Gull Lane"},
    }
    # Store order_tool for the following checks or operations.
    order_tool = OrderLookup(orders)
    # Store stock_tool for the following checks or operations.
    stock_tool = StockLookup({"rain jacket": 12, "day pack": 0})
    # Return Toolbox(order_tool, stock_tool, ChangeQueue(order_tool)) to the caller.
    return Toolbox(order_tool, stock_tool, ChangeQueue(order_tool))


# Define customer so this operation can be called and tested separately.
def customer(text):
    """Build a history that holds one customer message."""
    # Return [{'role': 'user', 'content': text}] to the caller.
    return [{"role": "user", "content": text}]


# Define test_look_up_known_order so this operation can be called and tested separately.
def test_look_up_known_order():
    # Store tools for the following checks or operations.
    tools = make_tools()
    assert tools.order_tool.look_up_order("A100") == "Order A100 is shipped."


# Define test_look_up_unknown_order so this operation can be called and tested separately.
def test_look_up_unknown_order():
    # Store tools for the following checks or operations.
    tools = make_tools()
    assert "No order" in tools.order_tool.look_up_order("A999")


# Define test_check_stock_for_known_and_unknown_products so this operation can be called and t...
def test_check_stock_for_known_and_unknown_products():
    # Store tools for the following checks or operations.
    tools = make_tools()
    assert (
        tools.stock_tool.check_stock("day pack")
        == "We have 0 of the day pack in stock."
    )
    assert tools.stock_tool.check_stock("tent") == "That product was not found."


# Define test_request_waits_and_changes_nothing so this operation can be called and tested sep...
def test_request_waits_and_changes_nothing():
    # Store tools for the following checks or operations.
    tools = make_tools()
    # Run tools.change_queue.request_address_change('A100', '9 Pine Street') to perform this step.
    tools.change_queue.request_address_change("A100", "9 Pine Street")
    assert tools.change_queue.waiting()[0]["status"] == "waiting"
    assert tools.order_tool.orders["A100"]["address"] == "14 Bay Road"


# Define test_approve_makes_the_change_once so this operation can be called and tested separat...
def test_approve_makes_the_change_once():
    # Store tools for the following checks or operations.
    tools = make_tools()
    # Run tools.change_queue.request_address_change('A100', '9 Pine Street') to perform this step.
    tools.change_queue.request_address_change("A100", "9 Pine Street")
    assert tools.change_queue.approve(1) == "Request 1 approved."
    assert tools.order_tool.orders["A100"]["address"] == "9 Pine Street"
    assert tools.change_queue.approve(1) == "Request 1 is already approved."


# Define test_reject_changes_nothing_and_cannot_be_approved_later so this operation can be cal...
def test_reject_changes_nothing_and_cannot_be_approved_later():
    # Store tools for the following checks or operations.
    tools = make_tools()
    # Run tools.change_queue.request_address_change('A100', '9 Pine Street') to perform this step.
    tools.change_queue.request_address_change("A100", "9 Pine Street")
    # Run tools.change_queue.reject(1) to perform this step.
    tools.change_queue.reject(1)
    assert tools.change_queue.approve(1) == "Request 1 is already rejected."
    assert tools.order_tool.orders["A100"]["address"] == "14 Bay Road"


# Define test_approve_unknown_request so this operation can be called and tested separately.
def test_approve_unknown_request():
    # Store tools for the following checks or operations.
    tools = make_tools()
    assert tools.change_queue.approve(7) == "There is no request 7."


# Define test_missing_argument_is_refused so this operation can be called and tested separately.
def test_missing_argument_is_refused():
    # Store tools for the following checks or operations.
    tools = make_tools()
    # Store reply for the following checks or operations.
    reply = tools.run("look_up_order", {}, customer("Where is my order?"))
    assert "missing" in reply


# Define test_order_id_must_come_from_the_customer so this operation can be called and tested ...
def test_order_id_must_come_from_the_customer():
    # Store tools for the following checks or operations.
    tools = make_tools()
    # Store reply for the following checks or operations.
    reply = tools.run("look_up_order", {"order_id": "A101"}, customer("Where is A100?"))
    assert "has not given that order ID" in reply


# Define test_customer_said_ignores_capitals so this operation can be called and tested separa...
def test_customer_said_ignores_capitals():
    # Store tools for the following checks or operations.
    tools = make_tools()
    assert tools.customer_said(customer("Ship it to 9 PINE STREET"), "9 Pine Street")


# Define test_unknown_order_containing_a_known_id_is_not_queued so this operation can be calle...
def test_unknown_order_containing_a_known_id_is_not_queued():
    # Store tools for the following checks or operations.
    tools = make_tools()
    # Store reply for the following checks or operations.
    reply = tools.change_queue.request_address_change("A1000", "9 Pine Street")
    assert "No order" in reply
    assert tools.change_queue.waiting() == []


# Define test_check_return_checks_status_and_customer_id so this operation can be called and t...
def test_check_return_checks_status_and_customer_id():
    # Store tools for the following checks or operations.
    tools = make_tools()
    # Store tools.order_tool.orders['A102'] for the following checks or operations.
    tools.order_tool.orders["A102"] = {
        "status": "delivered",
        "address": "88 Pier Street",
    }
    assert "within 30 days" in tools.run(
        "check_return", {"order_id": "A102"}, customer("A102")
    )
    assert "cannot be returned yet" in tools.order_tool.check_return("A100")
    assert "No order" in tools.order_tool.check_return("A999")
    assert "missing" in tools.run("check_return", {}, customer("return it"))
    assert "has not given" in tools.run(
        "check_return", {"order_id": "A102"}, customer("A100")
    )
