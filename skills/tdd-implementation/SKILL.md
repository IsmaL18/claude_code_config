---
name: tdd-implementation
description: Implement behavior test-first from a specification or acceptance criteria. Use for features and fixes where expected behavior can be verified with automated tests.
---

# TDD implementation

1. Read the specification or acceptance criteria first.
2. Derive test cases from expected behavior, not from the implementation.
3. Map each acceptance criterion to at least one meaningful test when appropriate.
4. Inspect only enough repository context to place and run the tests correctly.
5. Write the smallest useful failing test or test set.
6. Run the new tests and confirm they fail for the expected reason.
   - If they already pass, verify whether the behavior already exists or the test is insufficient.
7. Inspect the implementation in detail.
8. Implement the smallest correct change that satisfies the requirements.
9. Run the targeted tests until green.
10. Run relevant regression tests.
11. Run applicable lint, typecheck, and build checks.
12. Keep useful tests in the repository.

For an external integration, make the thinnest end-to-end path work against the real system before deepening, and cover the real client's validation path — a mock never validates an external contract.

Any property you state as a guarantee, in a docstring or a commit message, must have a test that holds it.

Do not weaken tests to make an incorrect implementation pass.
Do not derive expected behavior from existing code when a specification defines it.

End with a concise mapping of acceptance criteria to tests and verification results.
