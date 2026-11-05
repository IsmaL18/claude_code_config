---
name: tdd-implementation
description: Implement behavior test-first from a specification or acceptance criteria, following the task contract — tests written by the separate test-writer role when separation is chosen, by this session otherwise. Use for features and fixes where expected behavior can be verified with automated tests.
---
# Test-Driven Development

TDD is the red → green loop. The task contract (see `task-kickoff`) sets who writes the tests:

* `test-writer en contexte neuf`: the **test-writer** (agent `test-writer`, skill `test-authoring`) writes the failing tests and records them in `TESTS.md`; **this session** writes the production code that makes them pass. "The rule" below applies.
* `même session`: this session writes the tests first, under the `test-authoring` skill, then the code. "The rule" does not apply. Skip steps 3 and 5 of the loop.

Every test follows the contract's strategy (`plan validé` or `sélection stricte`) and "What deserves a test" in `AGENTS.md`.

## The rule (separation chosen)

**You are not allowed to modify tests. Absolutely.**

This session must never create, modify, delete, rename, skip, disable, mark as expected-failure or weaken:

* a test file;
* a test fixture, test data, snapshot or test helper;
* a test configuration (test runner config, `conftest.py`, setup files, coverage thresholds);
* `TESTS.md`.

No exception: not for a typo, a broken import, an obviously wrong assertion, a renamed symbol or a snapshot update. Do not regenerate snapshots. Do not change the test command or its filters to exclude a failing test. Do not write production code that detects it is running under test.

When a test looks wrong, stop and send it back to the test-writer with the evidence (see below). Making a correct implementation pass a wrong test, or a wrong implementation pass a right test, are both failures.

## Before the loop

0. **Baseline.** Before any test is added, run the tests of the touched scope and note the failures already present (test IDs and a one-line reason). Run the full suite as baseline only when it is fast. At the end of each slice, compare with this baseline instead of stashing your changes to find out whether a failure is yours.
1. Read the specification or acceptance criteria.
2. Write down the seams under test (the public interfaces where behavior is observed) and confirm them with the user. No test is requested at an unconfirmed seam. If the user's prompt already names the seams (files, interfaces, variables, spec reference), restate them in your answer and proceed: that is the confirmation, do not wait for another.
3. Cut the work into vertical slices: one seam, one behavior per slice. Horizontal slicing (all tests first, then all code) is an anti-pattern.
4. With `plan validé`: get the test plan for all slices (from the test-writer, or written by this session), submit it to the developer, and keep only the approved tests.

## The loop, per slice

1. **Red.** With separation: launch the `test-writer` agent with a brief containing: the contract line, the test strategy and the approved plan if any, the spec path or acceptance criteria, the confirmed seams, the slice to cover, and the test conventions of the repository (location, runner, command). Do not include your implementation ideas. For the next slices, continue the same test-writer agent rather than starting a new one, so it keeps the test-side context. Choose its model for the slice (see "Choose the sub-agent model for the task" in `AGENTS.md`): its default `sonnet` for ordinary slices, `opus` for a tricky seam or a disputed test.
2. **Check the red.** Run the tests it reports. They must fail for the expected reason (missing behavior or missing interface). If they fail for another reason, or already pass, send that back to the test-writer — do not fix it yourself.
3. **Freeze the tests.** Stage the test files and `TESTS.md` the test-writer reported (`git add <files>`): the index is now the baseline. Do not stage anything else, and do not stage anything until the slice is green.
4. **Green.** Inspect the implementation in detail and write only enough production code to make the tests pass. Don't anticipate future tests or add speculative features.
5. **Prove you didn't touch the tests.** `git diff --name-only` must list no test file and not `TESTS.md`. If one appears, revert your change to it (`git checkout -- <file>`) and fix the production code instead.
6. Run the targeted tests, then lint, typecheck and build checks. Compare with the baseline: only new failures are yours. Do not run the full suite here: it runs once in `pre-delivery-check`.

Refactoring is not part of the loop. It belongs to the review stage (`code-reviewer` findings), not the red → green implementation cycle.

## When a test looks wrong

Stop implementing that slice. Send to the test-writer (continue the agent) or, if it is gone, to a new one:

* the test (`file › name` and `TESTS.md` ID);
* why you believe it contradicts the spec or the agreed seam, quoting the spec;
* the behavior you believe is expected.

The test-writer decides from the specification. If you still disagree with its answer, ask the user. Never resolve the disagreement by editing the test.

## Implementation rules

For an external integration, make the thinnest end-to-end path work against the real system before deepening — a mock never validates an external contract. If a real-client test is missing, ask the test-writer for it.

Any behavior you state as a guarantee, in a docstring or a commit message, must have a test that holds it. If it doesn't, get one from the test author the contract sets, or don't state it. Never state a visual or design rule as a guarantee.

Do not derive expected behavior from existing code when a specification defines it.

End with a concise mapping of acceptance criteria to `TESTS.md` IDs (or to the contract's proof when a criterion is not tested), the verification results, and, with separation, the confirmation that no test file was modified by this session (`git diff --name-only` output).

## Next step

When the contract sets Next step to `oui`, end with the **Next step** block defined in `AGENTS.md` (role, skill, session, ready-to-send prompt). Otherwise, end with the 3-line summary.

Routing:

* all slices green, reviews `fusionnée` → `code-reviewer` in merged mode, fresh context.
* all slices green, reviews `séparées` → `tester` and `code-reviewer` (and `security-reviewer` when security is relevant), each in a fresh context.
* Launch reviewers as agents from this session (model chosen per `AGENTS.md`: `sonnet` by default, `opus` for a structural or high-risk diff) or give one prompt per reviewer for a new session. Each prompt gives the contract line, the spec path, the ADRs, `TESTS.md`, the branch and the diff range to review.
* all slices green, reviews `aucune`, or reviews done and findings fixed → `pre-delivery-check`, continue this session.
* a test is disputed → `test-writer` agent with the evidence (see "When a test looks wrong"); the user decides if the disagreement remains.
