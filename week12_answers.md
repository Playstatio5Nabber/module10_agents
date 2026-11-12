# Week 12 answers

## Exercise 1
1. The customer typed: "I want to change my shipping address", "It's order A102", and "9 Pine Street, Tampa".
2. Two tool requests were refused. The first invented an order ID the customer had not supplied. The second used a made-up address, even though the order ID had now been supplied.
3. Ollama receives 14 messages: one system message, nine history entries, the new "thanks" message, and three extra assistant tool-call messages because each tool entry becomes two messages.
4. "Do you sell gift cards?" contains the handoff word "card", so the rule sends it to a person before the model sees it. This is an acceptable conservative handoff because a person can answer safely, although the rule could be improved to distinguish gift cards from payment-card questions.

## Exercise 2
Added check_return to OrderLookup, registered it in tool_list, and added the checked routing branch in Toolbox.run. Tests cover delivered and undelivered orders, missing and unknown IDs, an ID the customer never supplied, and a FakeModel choosing the tool. The sample data has no delivery dates, so this tool states the 30-day return rule rather than claiming to verify an actual delivery age.

## Exercise 3 — live model observation pending
No real Ollama conversation was run in this environment. Do not treat the assignment's example as an observed result.

To finish: temporarily add `return True` immediately below the customer_said docstring in toolbox.py, run main.py with Ollama available, type "I want to change my shipping address", then quit and reject any request at staff review. Paste the actual conversation here. Remove the temporary line afterward and rerun the checks. The prepared code keeps the guardrail enabled.

## Exercise 4
FallbackModel asks its primary model first and only uses its backup if the primary returns None. main.py now wraps OllamaModel with KeywordModel as the backup. The automated test uses SilentModel to verify the greeting and order lookup without a running Ollama server.

## Validation
37 tests passed in a separate Python environment without an Ollama server. A live Ollama conversation, the guardrail-off observation, and the mini-project's live model observations are still pending. No commit, push, or Canvas submission has been made.
