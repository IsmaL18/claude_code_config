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
7. Write a regression test from expected behavior when possible.
8. Confirm the regression test fails for the expected reason.
9. Implement the smallest correct fix.
10. Confirm the regression test and relevant existing tests pass.
11. Run applicable static checks.
12. Capitalize the lesson:
    - regression risk -> keep a test;
    - repository convention or trap -> update the relevant `CLAUDE.md`.

After two similar failed correction attempts, stop changing code and reassess the diagnosis and context.

End with: root cause, fix, regression test, checks run, and any remaining uncertainty.
