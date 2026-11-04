# Mini-Project: Penny Loan Assistant

Penny is a loan calculator assistant for a fictional lending business that estimates monthly principal-and-interest payments for fixed-rate loans.
Users enter `loan AMOUNT ANNUAL_RATE MONTHS`, such as `loan 10000 6 36`, and a separate LoanCalculator tool performs the calculation.
The conversation is mock because it uses keyword rules rather than an AI model, and it does not connect to a lender or actually transfer customers to a person.
Requests about approval, qualification, or personal advice are directed to a loan officer because they require human review.
Missing values, invalid numbers, and unsupported requests receive helpful replies instead of invented answers.
If real customer data were entered, the conversation history could expose private financial information to someone with access to the running program.