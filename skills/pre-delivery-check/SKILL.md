---
name: pre-delivery-check
description: Perform final verification before delivering a code change. Use after implementation and review to verify requirements, tests, static checks, diff scope, documentation, and delivery readiness.
---

# Pre-delivery check

Do not introduce new functionality during this workflow.

Verify the task contract (see `task-kickoff`), not a fixed checklist. If no contract line exists, ask the developer for it before checking.

1. Inspect the final diff and identify the intended scope.
2. Compare the implementation against the specification and acceptance criteria when available.
3. Check that every proof the contract chose was produced: screenshot shown, human validation obtained, checks run. A proof not produced is NOT RUN.
4. Run the most relevant verification available in the repository:
   - the full test suite, once (unless the contract says `aucun test` and the suite is slow: then the targeted tests). If it takes longer than the command timeout, launch it in the background and read the result when it ends;
   - regression tests;
   - lint;
   - formatting check;
   - typecheck;
   - build;
   - project-specific validation commands.
5. Check for:
   - failing or skipped relevant tests;
   - with separation only: tests, fixtures, snapshots, test configuration or `TESTS.md` modified outside the `test-writer` role (compare the test-file diff with the `TESTS.md` entries and the test-writer reports);
   - new or changed tests missing from `TESTS.md`;
   - new shape tests (DOM structure, CSS classes, exact non-contractual text, snapshots) or tests failing "What deserves a test" in `AGENTS.md`;
   - the reviews set in the contract not run;
   - accidental unrelated changes;
   - debug code;
   - temporary files;
   - obvious secrets or credentials;
   - unresolved TODOs introduced by the change;
   - missing durable documentation.
6. Confirm relevant review findings have been resolved or explicitly accepted, by whom it belongs to:
   - **non-blocking findings** on production code may be accepted by this session, if each is listed in the report with a one-line reason;
   - **findings about tests**, with separation, are never accepted by this session: they go to the `test-writer` agent, or to the user if there is a disagreement;
   - **blocking findings** need the user's agreement to be accepted.
7. Do not claim success for checks that were not executed.

Return a concise checklist with:
- the contract line;
- PASS / FAIL / NOT RUN for each relevant check and each contract proof;
- **Seuils franchis**, when a threshold was crossed during the task;
- unresolved blockers;
- non-blocking concerns;
- final verdict: READY or NOT READY.

## Next step

When the contract sets Next step to `oui`, end with the **Next step** block defined in `AGENTS.md` (role, skill, session, ready-to-send prompt).

Routing:

* READY → `deliver`, continue this session.
* NOT READY → back to the role that owns the blocker: implementation (`tdd-implementation`, continue this session) for code, `test-writer` agent for tests, `product-owner` (new session) for a spec gap. The prompt lists the failing checks and blockers.
