# Author: Sami Ali
# Define LoanCalculator to keep this responsibility in a separate object.
class LoanCalculator:
    """Calculate fictional loan estimates without making lending decisions."""

    # Define __init__ so this operation can be called and tested separately.
    def __init__(self, payments_per_year=12):
        # Store self.payments_per_year for the following checks or operations.
        self.payments_per_year = payments_per_year
        # Store self.saved_estimates for the following checks or operations.
        self.saved_estimates = {}

    # Define monthly_payment so this operation can be called and tested separately.
    def monthly_payment(self, principal, annual_rate, months):
        # Check principal <= 0 or annual_rate < 0 or months <= 0 before continuing.
        if principal <= 0 or annual_rate < 0 or months <= 0:
            # Return None to the caller.
            return None
        # Store rate for the following checks or operations.
        rate = annual_rate / 100 / self.payments_per_year
        # Check rate == 0 before continuing.
        if rate == 0:
            # Return principal / months to the caller.
            return principal / months
        # Return principal * rate / (1 - (1 + rate) ** (-months)) to the caller.
        return principal * rate / (1 - (1 + rate) ** (-months))

    # Define estimate_payment so this operation can be called and tested separately.
    def estimate_payment(self, principal, annual_rate, months):
        """Estimate a monthly payment using values the customer supplied.

        Args:
            principal: The borrowed amount as text, like 10000.
            annual_rate: The annual percentage as text, like 6.
            months: The whole-number loan term as text, like 36.
        """
        # Store values for the following checks or operations.
        values = self.validated(principal, annual_rate, months)
        # Check values is None before continuing.
        if values is None:
            # Return 'Use a positive amount up to 100000000, rate 0 to 100, and whole-number months 1 to 6...
            return "Use a positive amount up to 100000000, rate 0 to 100, and whole-number months 1 to 600."
        # Store payment for the following checks or operations.
        payment = self.monthly_payment(*values)
        # Return f'Estimated monthly payment: ${payment:.2f} (principal and interest only).' to the ca...
        return (
            f"Estimated monthly payment: ${payment:.2f} (principal and interest only)."
        )

    # Define validated so this operation can be called and tested separately.
    def validated(self, principal, annual_rate, months):
        # Attempt the operation while handling expected failures below.
        try:
            # Store amount for the following checks or operations.
            amount = float(principal)
            # Store rate for the following checks or operations.
            rate = float(annual_rate)
            # Store term for the following checks or operations.
            term = int(str(months))
        except (ValueError, TypeError, OverflowError):
            # Return None to the caller.
            return None
        # Check not (0 < amount <= 100000000 and 0 <= rate <= 100 and (1 <= term <= 600)) before conti...
        if not (0 < amount <= 100000000 and 0 <= rate <= 100 and 1 <= term <= 600):
            # Return None to the caller.
            return None
        # Return (amount, rate, term) to the caller.
        return amount, rate, term

    # Define save_estimate so this operation can be called and tested separately.
    def save_estimate(self, label, values):
        """Store a reviewed estimate; only the queue's approval calls this."""
        # Store self.saved_estimates[label] for the following checks or operations.
        self.saved_estimates[label] = tuple(values)
