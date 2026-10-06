---
name: refactor-module
description: Refactor or extract a module incrementally while preserving behavior. Use when improving boundaries, reducing coupling, splitting a monolith, or reorganizing an existing codebase without intentionally changing product behavior.
---

# Refactor module

1. Define the target boundary and the reason for the refactor.
2. Map current behavior, entry points, dependencies, callers, state, and tests.
3. When coverage is insufficient, have the `test-writer` agent establish characterization or regression tests before structural changes (recorded in `TESTS.md`). Choose its model per `AGENTS.md` ("Choose the sub-agent model for the task").
   The refactoring session must not modify tests. If a test is coupled to internals and blocks the refactor, send it back to the `test-writer` — a behavior-preserving refactor never needs to change what a good test asserts.
4. Identify the smallest coherent functional unit to extract or reorganize.
5. Plan dependency direction and public interfaces before moving code.
6. Refactor one meaningful step at a time.
7. After each step:
   - run targeted tests;
   - run relevant static checks;
   - verify observable behavior remains unchanged.
8. Remove obsolete code only after callers have migrated and verification is green.
9. Update `ARCHITECTURE.md`, ADRs, or local `CLAUDE.md` only when the refactor changes durable structural knowledge.
10. Stop at a clean deliverable boundary before starting the next extraction.

For large restructures follow:

**map -> extract -> verify -> deliver -> repeat**

Avoid repository-wide rewrites when progressive extraction is possible.

## Next step

End with the **Next step** block defined in `AGENTS.md` (role, skill, session, ready-to-send prompt).

Routing:

* step done and green → `code-reviewer`, fresh context (agent or new-session prompt with the target boundary, the diff range and the characterization tests IDs).
* reviewed → `pre-delivery-check` then `deliver`, continue this session.
* another extraction remains → `refactor-module`, new session; the prompt gives the next unit to extract and what the previous step established.
* the refactor needs a structural decision not covered by an ADR → `architect`, new session recommended.
