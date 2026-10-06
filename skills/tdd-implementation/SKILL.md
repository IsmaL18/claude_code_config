---
name: tdd-implementation
description: Implement behavior test-first from a specification or acceptance criteria, with the tests written by the separate test-writer role and the production code written by this session. Use for features and fixes where expected behavior can be verified with automated tests.
---
# Test-Driven Development

TDD is the red → green loop, split between two roles that never share a context:

* the **test-writer** (agent `test-writer`, skill `test-authoring`) writes the failing tests and records them in `TESTS.md`;
* **this session** writes the production code that makes them pass.

## The rule

**You are not allowed to modify tests. Absolutely.**

This session must never create, modify, delete, rename, skip, disable, mark as expected-failure or weaken:

* a test file;
* a test fixture, test data, snapshot or test helper;
* a test configuration (test runner config, `conftest.py`, setup files, coverage thresholds);
* `TESTS.md`.

No exception: not for a typo, a broken import, an obviously wrong assertion, a renamed symbol or a snapshot update. Do not regenerate snapshots. Do not change the test command or its filters to exclude a failing test. Do not write production code that detects it is running under test.

When a test looks wrong, stop and send it back to the test-writer with the evidence (see below). Making a correct implementation pass a wrong test, or a wrong implementation pass a right test, are both failures.

## Before the loop

1. Read the specification or acceptance criteria.
2. Write down the seams under test (the public interfaces where behavior is observed) and confirm them with the user. No test is requested at an unconfirmed seam.
3. Cut the work into vertical slices: one seam, one behavior per slice. Horizontal slicing (all tests first, then all code) is an anti-pattern.

## The loop, per slice

1. **Red — delegated.** Launch the `test-writer` agent with a brief containing: the spec path or acceptance criteria, the confirmed seams, the slice to cover, and the test conventions of the repository (location, runner, command). Do not include your implementation ideas. For the next slices, continue the same test-writer agent rather than starting a new one, so it keeps the test-side context. Choose its model for the slice (see "Choose the sub-agent model for the task" in `AGENTS.md`): its default `sonnet` for ordinary slices, `opus` for a tricky seam or a disputed test.
2. **Check the red.** Run the tests it reports. They must fail for the expected reason (missing behavior or missing interface). If they fail for another reason, or already pass, send that back to the test-writer — do not fix it yourself.
3. **Freeze the tests.** Stage the test files and `TESTS.md` the test-writer reported (`git add <files>`): the index is now the baseline. Do not stage anything else, and do not stage anything until the slice is green.
4. **Green.** Inspect the implementation in detail and write only enough production code to make the tests pass. Don't anticipate future tests or add speculative features.
5. **Prove you didn't touch the tests.** `git diff --name-only` must list no test file and not `TESTS.md`. If one appears, revert your change to it (`git checkout -- <file>`) and fix the production code instead.
6. Run relevant regression tests, then lint, typecheck and build checks.

Refactoring is not part of the loop. It belongs to the review stage (see the code-review skill), not the red → green implementation cycle.

## When a test looks wrong

Stop implementing that slice. Send to the test-writer (continue the agent) or, if it is gone, to a new one:

* the test (`file › name` and `TESTS.md` ID);
* why you believe it contradicts the spec or the agreed seam, quoting the spec;
* the behavior you believe is expected.

The test-writer decides from the specification. If you still disagree with its answer, ask the user. Never resolve the disagreement by editing the test.

## Implementation rules

For an external integration, make the thinnest end-to-end path work against the real system before deepening — a mock never validates an external contract. If a real-client test is missing, ask the test-writer for it.

Any property you state as a guarantee, in a docstring or a commit message, must have a test that holds it. If it doesn't, ask the test-writer for one, or don't state it.

Do not derive expected behavior from existing code when a specification defines it.

End with a concise mapping of acceptance criteria to `TESTS.md` IDs, the verification results, and the confirmation that no test file was modified by this session (`git diff --name-only` output).

## Next step

End with the **Next step** block defined in `AGENTS.md` (role, skill, session, ready-to-send prompt).

Routing:

* all slices green → independent reviews: `tester` and `code-reviewer` (and `security-reviewer` when security is relevant), each in a fresh context — launch them as agents from this session (model chosen per `AGENTS.md`: `sonnet` by default, `opus` for a structural or high-risk diff) or give one prompt per reviewer for a new session. Each prompt gives the spec path, the ADRs, `TESTS.md`, the branch and the diff range to review.
* reviews done and findings fixed → `pre-delivery-check`, continue this session.
* a review threshold was crossed mid-way (new module, new integration, three increments, unplanned design decision) → the reviews above before the next slice.
* a test is disputed → `test-writer` agent with the evidence (see "When a test looks wrong"); the user decides if the disagreement remains.
