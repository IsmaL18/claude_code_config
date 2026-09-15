---
name: tdd-implementation
description: Implement behavior test-first from a specification or acceptance criteria. Use for features and fixes where expected behavior can be verified with automated tests.
---
# Test-Driven Development
TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle: consult them before and during the loop, not after.

## What a good test is
Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

See tests.md for examples and mocking.md for mocking guidelines.

## Seams: where tests go
A seam is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

Test only at pre-agreed seams. Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything, so agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

Ask: "What's the public interface, and which seams should we test?"

When the shape of that interface is itself in question (how deep the module is, where the seam belongs, what the interface should expose), call the Skill tool with "codebase-design" for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage and locality terms, and it is a reference to consult, not a session to run.

## Anti-patterns
Implementation-coupled: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
Tautological: the assertion recomputes the expected value the way the code does (expect(add(a, b)).toBe(a + b), a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
Horizontal slicing: writing all tests first, then all implementation. Bulk tests verify imagined behavior: you test the shape of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in vertical slices instead: one test → one implementation → repeat, each test a tracer bullet that responds to what the last cycle taught you.

## Rules of the loop
Red before green. Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
One slice at a time. One seam, one test, one minimal implementation per cycle.
Refactoring is not part of the loop. It belongs to the review stage (see the code-review skill), not the red → green implementation cycle.

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
