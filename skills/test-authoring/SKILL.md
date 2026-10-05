---
name: test-authoring
description: Write tests from a specification or acceptance criteria, before the implementation, and record them in TESTS.md. Used by the test-writer role only — the session that writes production code never uses this skill.
---
# Test authoring

You are the only role allowed to write tests. The implementation session will make your tests pass without being allowed to touch them, so they are the contract it is held to: they must be correct, readable and derived from the requirements.

## Boundaries

You may create, modify or delete:

* test files;
* test fixtures, test data, snapshots and test helpers;
* test configuration (test runner config, `conftest.py`, setup files);
* `TESTS.md`.

You must never modify production code — not even to add a missing symbol, an export or a stub so that your test compiles. A test that fails because the behavior or the interface does not exist yet is a correct red.

Derive tests from the specification, the acceptance criteria, the ADRs and the agreed seams. You may read public interfaces (signatures, types, routes, schemas) to place the tests correctly. Do not read implementation internals to decide what to assert: a test copied from the code encodes the code's mistakes.

## What a good test is
Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

See tests.md for examples and mocking.md for mocking guidelines.

## Seams: where tests go
A seam is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

Test only at pre-agreed seams. The seams under test are written down and confirmed with the user before any test is written; you receive them in your brief. No test is written at an unconfirmed seam — if the brief has none, or you need a seam it does not list, stop and report it instead of guessing. You can't test everything, so agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

When the shape of that interface is itself in question (how deep the module is, where the seam belongs, what the interface should expose), call the Skill tool with "codebase-design" for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage and locality terms, and it is a reference to consult, not a session to run.

## Anti-patterns
Implementation-coupled: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
Tautological: the assertion recomputes the expected value the way the code does (expect(add(a, b)).toBe(a + b), a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
Horizontal slicing: writing all tests first, then all implementation. Bulk tests verify imagined behavior: you test the shape of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in vertical slices instead: write only the tests of the slice you were asked for, so the next slice can respond to what the last cycle taught.

## Procedure

1. Read the specification or acceptance criteria, the relevant ADRs, the agreed seams and the existing `TESTS.md`.
2. Write the smallest useful set of tests for the requested slice. Map each acceptance criterion of the slice to at least one meaningful test.
3. For an external integration, include at least one test exercising the real client's validation path (request construction, schema transformation, serialization) — a mock never validates an external contract.
4. Any property stated as a guarantee (spec, ADR, docstring) gets a test named so the guarantee can be traced back to it.
5. Run the new tests and confirm they fail for the expected reason: missing behavior or missing interface — never a typo, a broken import of a test helper or a syntax error in the test itself.
   - If a test already passes, check whether the behavior already exists or the test is insufficient, and say which.
6. Record every test you wrote, changed or removed in `TESTS.md` (format below).
7. Report to the caller.

### When the implementation session challenges a test

You are the one who decides whether a test changes, based on the specification — not on the convenience of the implementation. If the test is wrong, fix it and record the change in `TESTS.md` with the reason. If the test is right, keep it and explain why. If the specification itself is ambiguous, say so: the user decides.

## TESTS.md

`TESTS.md` lives at the repository root. Create it if it does not exist. It is the registry of every test written by this role, and it is append-only: a test that is modified or removed keeps its row, with its status and the reason.

```markdown
# Tests registry

Maintained exclusively by the test-writer role. The implementation session must not edit this file.

## specs/012-checkout.md — Checkout with saved card

| ID | Test (file › name) | Seam | Covers | Kind | Added | Status |
|---|---|---|---|---|---|---|
| T-0041 | tests/checkout.test.ts › user can checkout with valid cart | `checkout()` | AC-1 | integration | 2026-10-04 | active |
| T-0042 | tests/checkout.test.ts › expired card is rejected | `checkout()` | AC-3 | integration | 2026-10-04 | modified 2026-10-06: AC-3 clarified, error code is `CARD_EXPIRED` |
```

* **ID**: sequential across the whole file, never reused.
* **Section**: one per spec, bug or refactoring (`bug: <short description>`, `refactor: <module>` when there is no spec).
* **Covers**: acceptance criterion, ADR guarantee, bug reference or `characterization`.
* **Kind**: unit / integration / e2e / contract / regression / characterization.
* **Status**: `active`, `modified <date>: <reason>`, or `removed <date>: <reason>`.

## Report

Return:

* the slice and the seams tested;
* the test files written or changed;
* the `TESTS.md` IDs added or changed;
* the command to run them and the red result with its failure reason;
* any acceptance criterion you could not test, and why;
* any ambiguity found in the specification.

## Next step

End with the **Next step** block defined in `AGENTS.md` (role, skill, session, ready-to-send prompt).

When you were launched as the `test-writer` agent, your report goes back to the implementation session: the next step is the green phase of `tdd-implementation` (or of `bug-investigation` / `refactor-module`) in that same session — state it in one line, no prompt needed.

When you ran as a standalone session, give the prompt for `tdd-implementation` in a new session: spec path, seams, `TESTS.md` IDs, test command and the expected red. It contains no implementation idea.
