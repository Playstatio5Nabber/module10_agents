# Week 12 answers

## Exercise 1
1. The customer typed: "I want to change my shipping address", "It's order A102", and "9 Pine Street, Tampa".
2. Two tool requests were refused. The first invented an order ID the customer had not supplied. The second used a made-up address, even though the order ID had now been supplied.
3. Ollama receives 14 messages: one system message, nine history entries, the new "thanks" message, and three extra assistant tool-call messages because each tool entry becomes two messages.
4. "Do you sell gift cards?" contains the handoff word "card", so the rule sends it to a person before the model sees it. This is an acceptable conservative handoff because a person can answer safely, although the rule could be improved to distinguish gift cards from payment-card questions.

## Exercise 2
Added check_return to OrderLookup, registered it in tool_list, and added the checked routing branch in Toolbox.run. Tests cover delivered and undelivered orders, missing and unknown IDs, an ID the customer never supplied, and a FakeModel choosing the tool. The sample data has no delivery dates, so this tool states the 30-day return rule rather than claiming to verify an actual delivery age.

## Exercise 3 — live model observation
I temporarily disabled customer_said by adding return True before its checks. I typed "I want to change my shipping address", and Sunny asked for the order ID instead of inventing one. In this run, the model requested missing information even with the guardrail disabled. This does not guarantee that other runs will behave safely, so I removed the temporary line afterward. All 37 tests passed with the guardrail restored.

## Exercise 4
FallbackModel asks its primary model first and only uses its backup if the primary returns None. main.py now wraps OllamaModel with KeywordModel as the backup. The automated test uses SilentModel to verify the greeting and order lookup without a running Ollama server.

## Validation
All 37 tests passed on my Mac after restoring the guardrail. In the live support conversation, the A102 address change waited for staff review and was applied after approval. Penny calculated a $304.22 monthly payment, queued the car estimate for review, and saved it after approval. In a fresh conversation, Penny asked for the missing annual rate and correctly referred a qualification question to a loan officer. With Ollama unavailable, the backup model successfully looked up order A100. The initial code was pushed in commit 4256500; these observations still need to be committed and pushed. Canvas has not been submitted.
