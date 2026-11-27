---
name: tdd-implementation
description: Implement behavior test-first from a specification or acceptance criteria, following the task contract — tests written by the separate test-writer role when separation is chosen, by the implementer itself otherwise. Loaded by the `implementer` agent. Use for features and fixes where expected behavior can be verified with automated tests.
---
# Test-Driven Development

TDD is the red → green loop. The task contract (see `task-kickoff`) sets who writes the tests:

* `test-writer en contexte neuf`: the **test-writer** (agent `test-writer`, skill `test-authoring`) writes the failing tests and records them in `TESTS.md`; **you** (agent `implementer`) write the production code that makes them pass. "The rule" below applies.
* `même session`: you write the tests first, under the `test-authoring` skill, then the code. "The rule" does not apply. Skip steps 3 and 5 of the loop.

You run as the `implementer` agent, launched and resumed by `orchestrate`. You cannot launch the test-writer yourself: you ask for its tests with `STATUT: BESOIN_TESTS`, and the orchestrator resumes you with its report. Follow the "Relay protocol" in `AGENTS.md`.

Tests are written directly, with no plan to validate, under "What deserves a test" in `AGENTS.md`.

## The rule (separation chosen)

**You are not allowed to modify tests. Absolutely.**

You must never create, modify, delete, rename, skip, disable, mark as expected-failure or weaken:

* a test file;
* a test fixture, test data, snapshot or test helper;
* a test configuration (test runner config, `conftest.py`, setup files, coverage thresholds);
* `TESTS.md`.

No exception: not for a typo, a broken import, an obviously wrong assertion, a renamed symbol or a snapshot update. Do not regenerate snapshots. Do not change the test command or its filters to exclude a failing test. Do not write production code that detects it is running under test.

When a test looks wrong, stop and send it back to the test-writer with the evidence (see below). Making a correct implementation pass a wrong test, or a wrong implementation pass a right test, are both failures.

## Before the loop

0. **Baseline.** Before any test is added, run the test files of the touched scope (never the full suite) and note the failures already present. At the end of each slice, compare with this baseline instead of stashing your changes to find out whether a failure is yours.
1. Read the specification or acceptance criteria, the ADRs, and the hand-off memory `handoff-<task-slug>.md` named in your brief. If the brief has no contract line, report `STATUT: BLOQUÉ contrat`.
2. Cut the work into vertical slices: one behavior per slice, each tied to acceptance criteria. Horizontal slicing (all tests first, then all code) is an anti-pattern. Report them with `STATUT: PLAN`. No seam confirmation: the test author picks the seams, the review judges the tests.

## The loop, per slice

1. **Red.** With separation: report `STATUT: BESOIN_TESTS <slice>` with the slice to cover and the test conventions of the repository (location, runner, command). No implementation idea. The orchestrator gets the tests from the test-writer and resumes you with its report.
2. **Check the red.** Run the tests it reports. They must fail for the expected reason (missing behavior or missing interface). If they fail for another reason, or already pass, report it with `STATUT: TEST_CONTESTÉ` — do not fix it yourself.
3. **Freeze the tests.** Stage the test files the test-writer reported (`git add <files>`): the index is now the baseline. Do not stage anything else, and do not stage anything until the slice is green.
4. **Green.** Inspect the implementation in detail and write only enough production code to make the tests pass. Don't anticipate future tests or add speculative features.
5. **Prove you didn't touch the tests.** `git diff --name-only` must list no test file (a `covers:` marker is part of the test). If one appears, revert your change to it (`git checkout -- <file>`) and fix the production code instead.
6. Run the targeted tests, then lint, typecheck and build checks. Compare with the baseline: only new failures are yours. Do not run the full suite here: it runs once in `pre-delivery-check`.

Refactoring is not part of the loop. It belongs to the review stage (`code-reviewer` findings), not the red → green implementation cycle.

## When a test looks wrong

Stop implementing that slice. Report `STATUT: TEST_CONTESTÉ` with:

* the test (`file › name` and its `covers:` marker);
* why you believe it contradicts the spec, quoting the spec;
* the behavior you believe is expected.

The orchestrator sends it to the test-writer, which decides from the specification; if you still disagree, the user decides. Never resolve the disagreement by editing the test.

## Implementation rules

For an external integration, make the thinnest end-to-end path work against the real system before deepening — a mock never validates an external contract. If a real-client test is missing, ask for it with `STATUT: BESOIN_TESTS`.

Any behavior you state as a guarantee, in a docstring or a commit message, must have a test that holds it. If it doesn't, get one from the test author the contract sets, or don't state it. Never state a visual or design rule as a guarantee.

Do not derive expected behavior from existing code when a specification defines it.

End with a concise mapping of acceptance criteria to tests (`file › name`) (or to the contract's proof when a criterion is not tested), the verification results, and, with separation, the confirmation that you modified no test file (`git diff --name-only` output).

## Report

End each turn with one status line (see "Relay protocol" in `AGENTS.md`):

* first turn → `STATUT: PLAN` with the slices;
* tests needed for a slice → `STATUT: BESOIN_TESTS <slice>`;
* a test looks wrong → `STATUT: TEST_CONTESTÉ` with the evidence;
* slice green → `STATUT: VERT <slice>` with the mapping above for that slice;
* review corrections applied → `STATUT: FAIT` with each finding and how it was fixed;
* a spec or ADR gap, or a decision the contract did not anticipate → `STATUT: BLOQUÉ <raison>`.

Reviews, pre-delivery and delivery are launched by the orchestrator, not by you.
