---
name: pre-delivery-check
description: Perform final verification before delivering a code change. Use after implementation and review to verify requirements, tests, static checks, diff scope, documentation, and delivery readiness.
---

# Pre-delivery check

Do not introduce new functionality during this workflow.

Verify the task contract (see `task-kickoff`), not a fixed checklist. If no contract line exists, report `STATUT: BLOQUÉ contrat`. You run as the `pre-delivery-checker` agent: you change nothing.

Touch-up runs a reduced check: steps 1, 3 and 7 only, plus the diff-scope, debug-code and secret checks of step 5. Prototype never runs this check: it is never delivered.

1. Inspect the final diff and identify the intended scope.
2. Compare the implementation against the specification and acceptance criteria when available.
3. Check that every proof the contract chose was produced: screenshot shown, human validation obtained, checks run. A proof not produced is NOT RUN.
4. Run the most relevant verification available in the repository:
   - the full test suite, once (see "Run targeted tests, then the full suite once" in `AGENTS.md` for the slow-suite exception). If it takes longer than the command timeout, launch it in the background and read the result when it ends;
   - regression tests;
   - lint;
   - formatting check;
   - typecheck;
   - build;
   - project-specific validation commands.
5. Check for:
   - failing or skipped relevant tests;
   - with separation only: tests, fixtures, snapshots or test configuration modified outside the `test-writer` role (compare the test-file diff with the test-writer reports);
   - traceability and budget: run `python3 ~/.claude/skills/test-authoring/covers_matrix.py --changed-since <base>` for the tests of the change, and `covers_matrix.py` for the whole repository. A new or changed test without a `covers:` marker is a blocker (owner `test-writer`). A criterion of the task's spec with no test and no contract proof is a blocker. More than one new test for a criterion, with no justification in the coverage reports, is a blocker (owner `test-writer`). Report the tests-per-criterion ratio of the change;
   - new shape tests (DOM structure, CSS classes, exact non-contractual text, snapshots) or tests failing "What deserves a test" in `AGENTS.md`;
   - the reviews set in the contract not run;
   - accidental unrelated changes;
   - debug code;
   - temporary files;
   - obvious secrets or credentials;
   - unresolved TODOs introduced by the change;
   - missing durable documentation.
6. Confirm relevant review findings have been resolved or explicitly accepted, by whom it belongs to:
   - **non-blocking findings** on production code may be accepted by the agent that wrote the code, if each is listed in its report with a one-line reason;
   - **findings about tests**, with separation, are never accepted by the agent that wrote the code: they go to the `test-writer` agent, or to the user if there is a disagreement;
   - **blocking findings** need the user's agreement to be accepted.
7. Do not claim success for checks that were not executed.

Return a concise checklist with:
- the contract line;
- PASS / FAIL / NOT RUN for each relevant check and each contract proof;
- **Seuils franchis**, when a threshold was crossed during the task;
- unresolved blockers;
- non-blocking concerns;
- final verdict: READY or NOT READY.

## Report

End with `STATUT: READY` or `STATUT: NOT READY` (see "Relay protocol" in `AGENTS.md`). Tag each blocker with its owner: `implementer`, `bug-investigator` or `refactorer` for code, `test-writer` for tests, `architect` for an ADR, `product-owner` for a spec gap, `user` for a risk to accept.
