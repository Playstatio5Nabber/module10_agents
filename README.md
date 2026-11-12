# Mini-Project: Penny Loan Assistant

Penny is a loan calculator assistant for a fictional lending business that estimates monthly principal-and-interest payments for fixed-rate loans.
Users enter `loan AMOUNT ANNUAL_RATE MONTHS`, such as `loan 10000 6 36`, and a separate LoanCalculator tool performs the calculation.
The conversation is mock because it uses keyword rules rather than an AI model, and it does not connect to a lender or actually transfer customers to a person.
Requests about approval, qualification, or personal advice are directed to a loan officer because they require human review.
Missing values, invalid numbers, and unsupported requests receive helpful replies instead of invented answers.
If real customer data were entered, the conversation history could expose private financial information to someone with access to the running program.
## Lab 11: Giving Penny a local model

Penny now receives a model for questions outside its loan-calculation and handoff rules.
When I asked about office hours, the model correctly answered Monday through Friday from 9 am to 5 pm.
When I asked whether the business offers business loans, it said it did not know and referred me to a loan officer.
I kept payment calculations and input validation in code because incorrect numbers could mislead customers.
Approval and personal-advice requests also stay in code so the model cannot decide whether someone qualifies.
If the model is unavailable, Penny gives a safe retry message while its calculation and handoff rules still work.


## Lab 12: Model-chosen tools and review

This section supersedes the earlier command-routing description: Penny now lets the model choose a tool through decide in a loop limited to three rounds. In an automated FakeModel test, the request to estimate 10000 at 6 percent for 36 months produced a monthly payment of $304.22 from the calculator. A second FakeModel test requested an annual rate the customer had never supplied, and the toolbox refused it before calculation. I added an instruction to greet customers normally when they only say hello, and another to keep save requests waiting for staff review. Saving an estimate is a fictional in-memory change that only the approval queue applies, and a second approval does nothing. Live Ollama observations are still pending and must be recorded after actual conversations; these examples describe automated tests, not real-model runs.

AI assistance and explanations are recorded in LAB12_AI_OUTPUT.md; remaining checks are listed in LAB12_NOTES.md.
