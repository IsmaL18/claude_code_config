---
name: bug-investigation
description: Investigate and fix a software bug systematically. Use when behavior is incorrect, flaky, failing, or unexplained and the root cause must be established before patching.
---

# Bug investigation

1. Reproduce or precisely characterize the failure.
2. Record expected behavior versus observed behavior.
3. Inspect relevant logs, tests, code paths, recent changes, and dependencies.
4. Form a small set of plausible hypotheses.
5. Test hypotheses with evidence; do not patch blindly.
6. Identify the root cause and affected surface.
7. Have the `test-writer` agent write a regression test from the expected behavior when possible. Give it expected versus observed behavior and the reproduction, not your fix. It records the test in `TESTS.md`.
8. Confirm the regression test fails for the expected reason, then stage it (`git add`) as the baseline.
9. Implement the smallest correct fix. You must not modify any test, fixture, test configuration or `TESTS.md`; if a test looks wrong, send it back to the `test-writer` (see `tdd-implementation`).
10. Confirm the regression test and relevant existing tests pass, and that `git diff --name-only` lists no test file.
11. Run applicable static checks.
12. Capitalize the lesson:
    - regression risk -> keep the test written by the `test-writer`;
    - repository convention or trap -> update the relevant `CLAUDE.md`.

After two similar failed correction attempts, stop changing code and reassess the diagnosis and context.

End with: root cause, fix, regression test, checks run, and any remaining uncertainty.
