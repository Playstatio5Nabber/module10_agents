# keyword_model.py
# Author: Sami Ali


# Define KeywordModel to keep this responsibility in a separate object.
class KeywordModel:
    """A stand-in model that decides with keyword rules. It needs no AI."""

    # Define decide so this operation can be called and tested separately.
    def decide(self, instructions, history, tools):
        """Return a reply or a tool request, based on the last message."""
        # Store last for the following checks or operations.
        last = history[-1]
        # Check last['role'] == 'tool' before continuing.
        if last["role"] == "tool":
            # Return {'text': last['content']} to the caller.
            return {"text": last["content"]}
        # Store text for the following checks or operations.
        text = last["content"].lower()
        # Check 'order' in text before continuing.
        if "order" in text:
            # Return {'tool': 'look_up_order', 'arguments': {'order_id': last['content']}} to the caller.
            return {"tool": "look_up_order", "arguments": {"order_id": last["content"]}}
        # Check 'stock' in text before continuing.
        if "stock" in text:
            # Return {'tool': 'check_stock', 'arguments': {'item': last['content']}} to the caller.
            return {"tool": "check_stock", "arguments": {"item": last["content"]}}
        # Check 'hello' in text before continuing.
        if "hello" in text:
            # Return {'text': 'Hello! How can I help you today?'} to the caller.
            return {"text": "Hello! How can I help you today?"}
        # Return {'text': "I'm not sure how to help with that. I can check an order or stock."} to the...
        return {
            "text": "I'm not sure how to help with that. I can check an order or stock."
        }
