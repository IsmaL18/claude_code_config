---
name: bug-investigation
description: Investigate and fix a software bug systematically. Use when behavior is incorrect, flaky, failing, or unexplained and the root cause must be established before patching.
---

# Bug investigation

Follow the task contract (see `task-kickoff`). It sets the regression test, its author, the reviews and the proof.

You run as the `bug-investigator` agent, launched and resumed by `orchestrate`. You own the diagnosis and the fix. Follow the "Relay protocol" in `AGENTS.md`.

1. Reproduce or precisely characterize the failure.
2. Record expected behavior versus observed behavior.
3. Inspect relevant logs, tests, code paths, recent changes, and dependencies.
4. Form a small set of plausible hypotheses.
5. Test hypotheses with evidence; do not patch blindly.
6. Identify the root cause and affected surface.
7. Unless the contract says `aucun test`, get one regression test from the expected behavior, under "What deserves a test" in `AGENTS.md`. With separation, the `test-writer` agent writes it: report `STATUT: BESOIN_TESTS regression` with expected versus observed behavior and the reproduction, not your fix; the orchestrator resumes you with its report. With `même session`, write it yourself. Record it in `TESTS.md`.
8. Confirm the regression test fails for the expected reason. With separation, stage it (`git add`) as the baseline.
9. Implement the smallest correct fix. With separation, you must not modify any test, fixture, test configuration or `TESTS.md`; if a test looks wrong, report `STATUT: TEST_CONTESTÉ` (see `tdd-implementation`).
10. Confirm the regression test and the targeted existing tests pass. With separation, confirm that `git diff --name-only` lists no test file.
11. Run applicable static checks.
12. Capitalize the lesson:
    - regression risk -> keep the regression test;
    - repository convention or trap -> update the relevant `CLAUDE.md`.

After two similar failed correction attempts, stop changing code and reassess the diagnosis and context.

End with: root cause, fix, regression test, checks run, and any remaining uncertainty.

## Report

End each turn with one status line (see "Relay protocol" in `AGENTS.md`):

* root cause established, regression test needed → `STATUT: BESOIN_TESTS regression`;
* fix done and verified, or review corrections applied → `STATUT: FAIT` with root cause, fix, regression test ID, checks run, diff range;
* root cause not established after two attempts → `STATUT: BLOQUÉ diagnostic`, with the reproduction, the hypotheses ruled out and the evidence;
* the "bug" is actually missing or unclear behavior → `STATUT: BLOQUÉ spec`, with the product question only.
