# Mini-Project: Penny Loan Assistant

Penny is a loan calculator assistant for a fictional lending business that estimates monthly principal-and-interest payments for fixed-rate loans.
Users enter `loan AMOUNT ANNUAL_RATE MONTHS`, such as `loan 10000 6 36`, and a separate LoanCalculator tool performs the calculation.
The original Week 10 conversation used mock keyword rules; Lab 11 adds a replaceable model, and it does not connect to a lender or actually transfer customers to a person.
Requests about approval, qualification, or personal advice are directed to a loan officer because they require human review.
Missing values and invalid numbers receive coded help; general requests now go to the supplied model.
If real customer data were entered, the conversation history could expose private financial information to someone with access to the running program.

## Lab 11 — local model integration
Penny now receives a model, while loan calculations and loan-officer handoffs still run first in code.
The offline mock answered “hello” with “Hello! How can I help you today?”, and it refused to supply weather information with its fixed “not sure” response.
The actual Ollama run failed to initialize its graphics backend, so a successful real-model answer and a wrong or refused real-model answer still need to be recorded from a normal terminal or a classmate’s laptop.
I kept payment arithmetic, input validation, and approval handoffs in code because an invented payment or approval would mislead a customer.
When a model returns no answer, Penny gives a retry message, and the calculation and handoff tests still pass without Ollama.

### Run and finish
Install dependencies with `python3 -m pip install -r requirements.txt` in your virtual environment.
Install Ollama and pull `granite4.1:3b`, then run `python3 main.py` and `python3 my_main.py`.
Finish the actual conversations in week11_answers.md and replace the pending real-model observation sentence above.
If you use a classmate's laptop, add their name here after working with them.
Run `ruff format . && ruff check . && pytest -v` with Ollama off.

### AI disclosure
Codex generated the Lab 11 additions and edits. The generated class code is preserved in AI_OUTPUT.md, and explanatory comments accompany the changed or generated class lines. Review each explanation and be prepared to explain the code yourself.

### Local runtime installed for this lab
The official standalone Ollama 0.40.14 runtime and the 2.1 GB course model were downloaded to this chat's working folder, outside the repository.
Use the supplied Start-Ollama.command launcher in the chat outputs to start that runtime from a normal macOS terminal; stop it with Ctrl+C.
No Ollama application was installed in Applications and no shell PATH settings were changed.
The model's graphics backend failed to initialize under Codex; this does not establish that the laptop cannot run it from a normal terminal.
The model-generated conversations and the specific real-model README observations are still unfinished. Do not treat the safe fallback as a model-generated answer.
