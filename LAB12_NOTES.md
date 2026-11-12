# Lab 12 work status

Prepared with AI assistance. LAB12_AI_OUTPUT.md contains the Python output; comments explain the code. Review it and be able to explain it before submission.

## Completed checks
- Customer-provided IDs and addresses are checked before support tools run.
- Address changes wait for staff and cannot be applied twice.
- check_return is registered and tested.
- FallbackModel keeps simple lookups working without the real model.
- The loan mini-project uses model-chosen tools and a checked toolbox.
- Saving a fictional loan estimate waits for staff review. This is not loan approval.
- Automated tests run without a real model.

## Live work remaining
Run main.py and my_main.py with Ollama and granite4.1:3b on a machine that supports it. Complete Exercise 3 with the real model, reject the request, restore the guardrail, and record the actual output in week12_answers.md. Add your actual mini-project observations to README.md. If using a classmate's machine, record their name as the assignment requires.

## Final local checks
From the repository root, with Ollama stopped:

```sh
ruff format .
ruff check .
pytest -v
```

These prepared files passed 37 tests and Ruff in a separate environment; the complete repository also needs its final check after the edited files are saved. Commits, pushes, and Canvas submission were deliberately left to Sami.
