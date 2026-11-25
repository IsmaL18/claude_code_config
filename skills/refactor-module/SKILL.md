---
name: refactor-module
description: Refactor or extract a module incrementally while preserving behavior. Use when improving boundaries, reducing coupling, splitting a monolith, or reorganizing an existing codebase without intentionally changing product behavior.
---

# Refactor module

Follow the task contract (see `task-kickoff`). It sets the characterization tests, their author, the reviews and the proof.

You run as the `refactorer` agent, launched and resumed by `orchestrate`. Follow the "Relay protocol" in `AGENTS.md`.

1. Define the target boundary and the reason for the refactor.
2. Map current behavior, entry points, dependencies, callers, state, and tests.
3. When coverage of the risky behavior is insufficient, establish characterization tests before structural changes, under "What deserves a test" in `AGENTS.md` (recorded in `TESTS.md`). With separation, the `test-writer` agent writes them: report `STATUT: BESOIN_TESTS characterization` with the behaviors to pin; the orchestrator resumes you with its report.
   With separation, the refactoring session must not modify tests. If a test is coupled to internals and blocks the refactor, report `STATUT: TEST_CONTESTÉ` — a behavior-preserving refactor never needs to change what a good test asserts.
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

## Report

End each turn with one status line (see "Relay protocol" in `AGENTS.md`):

* mapping done → `STATUT: PLAN` with the steps, and `BESOIN_TESTS characterization` when coverage is insufficient;
* all steps done and green, or review corrections applied → `STATUT: FAIT` with the target boundary, the diff range and the characterization test IDs;
* another extraction remains → say so in the `FAIT` report: the orchestrator proposes it as a follow-up task;
* the refactor needs a structural decision not covered by an ADR → `STATUT: BLOQUÉ ADR`.
