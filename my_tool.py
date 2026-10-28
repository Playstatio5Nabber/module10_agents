# Author: Sami Ali

# Define a tool that calculates fixed-rate loan payments.
class LoanCalculator:
    # Accept the number of monthly payments made in one year.
    def __init__(self, payments_per_year=12):
        # Store this value for converting annual interest to monthly interest.
        self.payments_per_year = payments_per_year

    # Calculate a monthly payment from principal, annual percent, and months.
    def monthly_payment(self, principal, annual_rate, months):
        # Reject a nonpositive amount, negative rate, or nonpositive term.
        if principal <= 0 or annual_rate < 0 or months <= 0:
            # Signal that the inputs cannot produce a valid estimate.
            return None
        # Convert the annual percentage into a monthly decimal rate.
        rate = annual_rate / 100 / self.payments_per_year
        # Handle zero interest without dividing by zero.
        if rate == 0:
            # Split the amount borrowed equally across the months.
            return principal / months
        # Calculate the discount factor for all monthly payments.
        discount = (1 + rate) ** (-months)
        # Apply the fixed-payment loan formula.
        return principal * rate / (1 - discount)
