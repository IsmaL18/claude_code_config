---
name: refactor-module
description: Refactor or extract a module incrementally while preserving behavior. Use when improving boundaries, reducing coupling, splitting a monolith, or reorganizing an existing codebase without intentionally changing product behavior.
---

# Refactor module

1. Define the target boundary and the reason for the refactor.
2. Map current behavior, entry points, dependencies, callers, state, and tests.
3. Establish characterization or regression tests before structural changes when coverage is insufficient.
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
