---
name: pre-delivery-check
description: Perform final verification before delivering a code change. Use after implementation and review to verify requirements, tests, static checks, diff scope, documentation, and delivery readiness.
---

# Pre-delivery check

Do not introduce new functionality during this workflow.

1. Inspect the final diff and identify the intended scope.
2. Compare the implementation against the specification and acceptance criteria when available.
3. Run the most relevant verification available in the repository:
   - targeted tests;
   - regression tests;
   - lint;
   - formatting check;
   - typecheck;
   - build;
   - project-specific validation commands.
4. Check for:
   - failing or skipped relevant tests;
   - accidental unrelated changes;
   - debug code;
   - temporary files;
   - obvious secrets or credentials;
   - unresolved TODOs introduced by the change;
   - missing durable documentation.
5. Confirm relevant review findings have been resolved or explicitly accepted.
6. Do not claim success for checks that were not executed.

Return a concise checklist with:
- PASS / FAIL / NOT RUN for each relevant check;
- unresolved blockers;
- non-blocking concerns;
- final verdict: READY or NOT READY.
