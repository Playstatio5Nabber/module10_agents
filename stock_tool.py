# Author: Sami Ali
# Define StockLookup to keep this responsibility in a separate object.
class StockLookup:
    """Look up product names and stock counts."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, stock):
        # Store self.stock for the following checks or operations.
        self.stock = stock

    # Define find_product so this operation can be called and tested separately.
    def find_product(self, text):
        # Inspect each product in self.stock.
        for product in self.stock:
            # Check product.lower() in text.lower() before continuing.
            if product.lower() in text.lower():
                # Return product to the caller.
                return product
        # Return None to the caller.
        return None

    # Define count_for so this operation can be called and tested separately.
    def count_for(self, product):
        # Return self.stock.get(product) to the caller.
        return self.stock.get(product)

    # Define check_stock so this operation can be called and tested separately.
    def check_stock(self, item):
        """Check how many of one product are in stock.

        Args:
            item: The product name, like rain jacket.
        """
        # Store product for the following checks or operations.
        product = self.find_product(item)
        # Check product is None before continuing.
        if product is None:
            # Return 'That product was not found.' to the caller.
            return "That product was not found."
        # Return f'We have {self.count_for(product)} of the {product} in stock.' to the caller.
        return f"We have {self.count_for(product)} of the {product} in stock."
