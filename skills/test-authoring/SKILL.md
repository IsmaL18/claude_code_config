---
name: test-authoring
description: Write tests from a specification or acceptance criteria, before the implementation, and record them in TESTS.md. Used by the test-writer role when the task contract sets separation, and by the implementer when it sets `même session`. Writes the tests directly, without a plan to validate.
---
# Test authoring

When the task contract sets separation to `test-writer en contexte neuf`, you are the only role allowed to write tests. The implementer will make your tests pass without being allowed to touch them, so they are the contract it is held to: they must be correct, readable and derived from the requirements.

When the contract sets `même session`, the implementer follows this skill itself. The Boundaries section then does not apply.

## Boundaries

You may create, modify or delete:

* test files;
* test fixtures, test data, snapshots and test helpers;
* test configuration (test runner config, `conftest.py`, setup files);
* `TESTS.md`.

You must never modify production code — not even to add a missing symbol, an export or a stub so that your test compiles. A test that fails because the behavior or the interface does not exist yet is a correct red.

Derive tests from the specification, the acceptance criteria, and the ADRs. You may read public interfaces (signatures, types, routes, schemas) to place the tests correctly. Do not read implementation internals to decide what to assert: a test copied from the code encodes the code's mistakes.

## What a good test is
Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

See tests.md for examples and mocking.md for mocking guidelines.

## Seams: where tests go
A seam is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

Pick the seam yourself: the highest public interface that already exists in the project for that behavior (an HTTP route, a port, a public function), taken from the spec, the ADRs and the brief. No confirmation is needed. Name the seams you used in your report.

Reuse the project's shared test helpers (app factory, stores, fixtures) instead of building the system under test by hand in each file. A rule that applies to many tests (a new guard, a new dependency) must be absorbed by one helper, not by every test file.

Only when the interface does not exist yet and its shape is itself in question (how deep the module is, what it should expose), report it. Do not decide the interface.

## What deserves a test

Apply "What deserves a test" in `AGENTS.md`. Every test must pass all four:

* **Real risk.** A regression would cost more than the test costs to maintain: business rule, data, security, contract, critical path. At most one test per acceptance criterion, unless justified in the report.
* **Behavior, not shape.** Never assert DOM structure, CSS classes, exact non-contractual text or snapshots. Test the UI through accessible roles and observable effects.
* **Highest fast level.** Prefer one fast integration test over several coupled unit tests. Do not unit-test a detail already covered.
* **Not already guaranteed.** Never test what the typecheck, the lint, a schema or the design system already enforces.

Never write an improbable edge case, a test of a framework or a library, or a test whose only purpose is coverage.

Automated visual regression only when the project already has it or the brief asks for it.

## Test strategy

Write the tests directly, under "What deserves a test" (strategy `écriture directe`; an older brief may still say `sélection stricte` or `plan validé`: treat both the same way). There is no plan to submit. With `aucun test`, write none.

Keep it small: a slice usually needs a handful of tests. Prefer one test that walks an acceptance criterion end to end over several tests of its parts.

## Anti-patterns
Implementation-coupled: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
Tautological: the assertion recomputes the expected value the way the code does (expect(add(a, b)).toBe(a + b), a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
Shape-coupled: asserts DOM structure, CSS classes, exact text that is not part of a contract, or a snapshot. The tell: the test breaks on a visual touch-up while behavior hasn't changed.
Horizontal slicing: writing all tests first, then all implementation. Bulk tests verify imagined behavior: you test the shape of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in vertical slices instead: write only the tests of the slice you were asked for, so the next slice can respond to what the last cycle taught.

## Procedure

1. Read the specification or acceptance criteria and the relevant ADRs. In `TESTS.md`, read only the next free ID and the section you will extend (`grep`, `tail`): never the whole file.
2. Write the smallest useful set of tests for the requested slice, under "What deserves a test". Map each acceptance criterion of the slice to at most one test, unless justified.
3. For an external integration, include at least one test exercising the real client's validation path (request construction, schema transformation, serialization) — a mock never validates an external contract.
4. Any property stated as a guarantee (spec, ADR, docstring) gets a test named so the guarantee can be traced back to it.
5. Run only the test files you touched (never the full suite) and confirm the new tests fail for the expected reason: missing behavior or missing interface — never a typo, a broken import of a test helper or a syntax error in the test itself.
   - If a test already passes, check whether the behavior already exists or the test is insufficient, and say which.
6. Record every test you wrote, changed or removed in `TESTS.md` (format below).
7. Run the lint (and typecheck when the project has one) on the test files you created or modified and fix what it reports: unused imports, formatting, types. Use the project's own command (e.g. `ruff`, `eslint`). Test files must be lint-clean before you report.
8. Report to the caller.

### When the implementer challenges a test

You are the one who decides whether a test changes, based on the specification — not on the convenience of the implementation. If the test is wrong, fix it and record the change in `TESTS.md` with the reason. If the test is right, keep it and explain why. If the specification itself is ambiguous, say so: the user decides.

## TESTS.md

`TESTS.md` lives at the repository root. Create it if it does not exist. It is the registry of every test written, whoever the author, and it is append-only: a test that is modified or removed keeps its row, with its status and the reason.

```markdown
# Tests registry

Records every test written. When separation applies, only the test-writer role edits this file.

## specs/012-checkout.md — Checkout with saved card

| ID | Test (file › name) | Seam | Covers | Kind | Added | Status |
|---|---|---|---|---|---|---|
| T-0041 | tests/checkout.test.ts › user can checkout with valid cart | `checkout()` | AC-1 | integration | 2026-10-04 | active |
| T-0042 | tests/checkout.test.ts › expired card is rejected | `checkout()` | AC-3 | integration | 2026-10-04 | modified 2026-10-06: AC-3 clarified, error code is `CARD_EXPIRED` |
```

* **ID**: sequential across the whole file, never reused.
* **Section**: one per spec, bug or refactoring (`bug: <short description>`, `refactor: <module>` when there is no spec).
* **Covers**: acceptance criterion, ADR guarantee, bug reference or `characterization`, then the risk covered (e.g. `AC-3 — expired card charged`).
* **Kind**: unit / integration / e2e / contract / regression / characterization.
* **Status**: `active`, `modified <date>: <reason>`, or `removed <date>: <reason>`.

## Report

Return:

* the slice and the seams tested;
* the test files written or changed;
* the `TESTS.md` IDs added or changed;
* the command to run them and the red result with its failure reason;
* the lint / typecheck command run on the test files and its result (must be green);
* any acceptance criterion you could not test, and why;
* any acceptance criterion you chose not to test under "What deserves a test", and why;
* any ambiguity found in the specification.

## Report

As the `test-writer` agent, launched by `orchestrate`: your report goes back to the orchestrator, which hands it to the agent that writes the code. List the test files, the `TESTS.md` IDs, the test command and the expected red. No implementation idea. Follow the "Relay protocol" in `AGENTS.md`: `STATUT: FAIT`, or `STATUT: BLOQUÉ <raison>` when the spec or the slice is missing.

With `même session`, the agent that writes the code follows this skill itself: no separate report.
