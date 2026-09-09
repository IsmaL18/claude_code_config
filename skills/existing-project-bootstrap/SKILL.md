---
name: existing-project-bootstrap
description: Bootstrap an existing repository for disciplined AI-assisted development. Use when taking over a project that lacks clear Claude instructions, architecture documentation, specs, tests, or functional boundaries.
---

# Existing project bootstrap

1. Explore the repository before modifying anything.
2. Identify:
   - project commands;
   - functional modules and boundaries;
   - important dependencies;
   - existing tests;
   - conventions;
   - generated files and repository traps;
   - architectural risks and highly coupled areas.
3. Summarize the current system before proposing changes.
4. Create or improve the root `CLAUDE.md` with commands, conventions, and repository traps only.
5. Create or improve `ARCHITECTURE.md` with durable boundaries, dependency directions, constraints, and structural decisions.
6. Create `PRODUCT.md`, `USER.md`, or `DESIGN.md` only when useful. Do not invent product intent from code. To create these documents, please ask several questions to the user to gather the necessary context and as much information as possible.
7. Create `specs/` and `docs/adr/` if the project needs them.
8. Identify missing test coverage and the safest areas for incremental improvement.
9. Propose a prioritized bootstrap roadmap.
10. Do not perform a broad rewrite unless explicitly requested.

Prefer incremental improvement: **map -> document -> verify -> improve -> repeat**.

End with:
- documents created or updated;
- main architectural risks;
- missing knowledge requiring user input;
- recommended next actions.
