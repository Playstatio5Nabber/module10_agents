# Author: Sami Ali

# Define a separate tool for looking up product stock.
class StockLookup:
    # Accept the stock dictionary when creating the tool.
    def __init__(self, stock):
        # Store the dictionary so other methods can use it.
        self.stock = stock

    # Search a message for a known product name.
    def find_product(self, text):
        # Lowercase the message to ignore capitalization.
        text = text.lower()
        # Check each product name in the stock dictionary.
        for product in self.stock:
            # Compare the lowercase product name with the message.
            if product.lower() in text:
                # Return the matching dictionary key.
                return product
        # Return None when no known product is mentioned.
        return None

    # Look up the stock count for a product.
    def count_for(self, product):
        # Check that the product exists before accessing it.
        if product in self.stock:
            # Return its count, including zero if it is sold out.
            return self.stock[product]
        # Return None for an unknown product.
        return None
