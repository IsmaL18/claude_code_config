---
name: test-authoring
description: Write tests from a specification or acceptance criteria, before the implementation, mark each with a `covers:` comment and report coverage. Used by the test-writer role when the task contract sets separation, and by the implementer when it sets `même session`. Writes the tests directly, without a plan to validate.
---
# Test authoring

When the task contract sets separation to `test-writer en contexte neuf`, you are the only role allowed to write tests. The implementer will make your tests pass without being allowed to touch them, so they are the contract it is held to: they must be correct, readable and derived from the requirements.

When the contract sets `même session`, the implementer follows this skill itself. The Boundaries section then does not apply.

## Boundaries

You may create, modify or delete:

* test files;
* test fixtures, test data, snapshots and test helpers;
* test configuration (test runner config, `conftest.py`, setup files).

A legacy `TESTS.md` (project not yet migrated to `covers:` markers) is frozen: do not edit it, do not add rows.

You must never modify production code — not even to add a missing symbol, an export or a stub so that your test compiles. A test that fails because the behavior or the interface does not exist yet is a correct red.

Derive tests from the specification, the acceptance criteria, and the ADRs. You may read public interfaces (signatures, types, routes, schemas) to place the tests correctly. Do not read implementation internals to decide what to assert: a test copied from the code encodes the code's mistakes.

## What a good test is
Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

See tests.md for examples and mocking.md for mocking guidelines.

## Seams: where tests go
A seam is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

Pick the seam yourself: the highest public interface that already exists in the project for that behavior (an HTTP route, a port, a public function), taken from the spec, the ADRs and the brief. No confirmation is needed. Name the seams you used in your report.

Reuse the project's shared test helpers (app factory, stores, fixtures) instead of building the system under test by hand in each file. A rule that applies to many tests (a new guard, a new dependency) must be absorbed by one helper, not by every test file.

Never create a new helper file or test double (`aides_*`, `doubles_*`, `fakes`) while an existing one can be extended. When you do create one, name it in the report with the reason no existing one fits.

Only when the interface does not exist yet and its shape is itself in question (how deep the module is, what it should expose), report it. Do not decide the interface.

## What deserves a test

Apply "What deserves a test" in `AGENTS.md`. Every test must pass all four:

* **Real risk.** A regression would cost more than the test costs to maintain: business rule, data, security, contract, critical path.
* **Behavior, not shape.** Never assert DOM structure, CSS classes, exact non-contractual text or snapshots. Test the UI through accessible roles and observable effects.
* **Highest fast level.** Prefer one fast integration test over several coupled unit tests. Do not unit-test a detail already covered.
* **Not already guaranteed.** Never test what the typecheck, the lint, a schema or the design system already enforces.

Never write an improbable edge case, a test of a framework or a library, or a test whose only purpose is coverage.

Automated visual regression only when the project already has it or the brief asks for it.

## Test strategy

Write the tests directly, under "What deserves a test" (strategy `écriture directe`; an older brief may still say `sélection stricte` or `plan validé`: treat both the same way). There is no plan to submit. With `aucun test`, write none.

Keep it small: a slice usually needs a handful of tests. Prefer one test that walks an acceptance criterion end to end over several tests of its parts.

### Budget and markers (see "Every test names what it covers" in `AGENTS.md`)

* **Marker.** Put `# covers: AC-3` (or `// covers: AC-3`) on the line right above each test, above its decorators. Tokens: `AC-n`, `ADR-NNNN#<guarantee>`, `regression:<ref>`, `characterization`. No marker, no test: if you cannot name what a test covers, do not write it.
* **One test per criterion.** A parametrized test counts for one, with at most 4 cases. Every extra test, and every test not covering an acceptance criterion, gets a one-line justification in the report.
* **Merge before adding.** Before writing, search the existing tests for the same criterion or the same seam (`grep` the `covers:` markers and the seam name) and extend the existing test. A criterion that changed replaces its old tests: delete or rewrite them in the same slice, never stack a new test next to an obsolete one.
* **One property, one test.** A guard, a normalization, a bound or a hardening is one property test over its inputs, never one test per variant, per call site or per hardening step.

## Anti-patterns
Implementation-coupled: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
Tautological: the assertion recomputes the expected value the way the code does (expect(add(a, b)).toBe(a + b), a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
Shape-coupled: asserts DOM structure, CSS classes, exact text that is not part of a contract, or a snapshot. The tell: the test breaks on a visual touch-up while behavior hasn't changed.
Horizontal slicing: writing all tests first, then all implementation. Bulk tests verify imagined behavior: you test the shape of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in vertical slices instead: write only the tests of the slice you were asked for, so the next slice can respond to what the last cycle taught.

## Procedure

1. Read the specification or acceptance criteria and the relevant ADRs. Find the existing tests of the same criteria or seams (`grep` the `covers:` markers, or run `covers_matrix.py`): never read the whole suite.
2. Write the smallest useful set of tests for the requested slice, under "What deserves a test" and the budget above. Map each acceptance criterion of the slice to at most one test, extending an existing test when there is one.
3. For an external integration, include at least one test exercising the real client's validation path (request construction, schema transformation, serialization) — a mock never validates an external contract.
4. Any property stated as a guarantee (spec, ADR, docstring) gets a test named so the guarantee can be traced back to it.
5. Run only the test files you touched (never the full suite) and confirm the new tests fail for the expected reason: missing behavior or missing interface — never a typo, a broken import of a test helper or a syntax error in the test itself.
   - If a test already passes, check whether the behavior already exists or the test is insufficient, and say which.
6. Check the markers: run `python3 ~/.claude/skills/test-authoring/covers_matrix.py` from the repository root and confirm every test you wrote or changed has a `covers:` marker and every criterion of the slice appears in the matrix, or is listed as discarded in the report.
7. Run the lint (and typecheck when the project has one) on the test files you created or modified and fix what it reports: unused imports, formatting, types. Use the project's own command (e.g. `ruff`, `eslint`). Test files must be lint-clean before you report.
8. Report to the caller.

### When the implementer challenges a test

You are the one who decides whether a test changes, based on the specification — not on the convenience of the implementation. If the test is wrong, fix it and give the reason in the report. If the test is right, keep it and explain why. If the specification itself is ambiguous, say so: the user decides.

## Coverage report

Return this block, in French, short and readable without opening the tests. The orchestrator shows it to the user as is.

```text
Couverture de la slice <nom>
- Protégé : AC-3 <comportement en une phrase> → <fichier › test>
- Écarté : AC-5 <raison : déjà garanti par le schéma, risque faible…>
- Ajouts : <n> tests ajoutés, <m> étendus, <k> supprimés ou remplacés
- Écarts au budget : <test> — <raison en une ligne>   (ou « aucun »)
- Helpers : <réutilisés | nouveau fichier ou double nommé, avec la raison>
- Durée du run ciblé : <x s>
```

Then, for the caller:

* the slice and the seams tested;
* the test files written or changed;
* the command to run them and the red result with its failure reason;
* the lint / typecheck command run on the test files and its result (must be green);
* any acceptance criterion you could not test, and why;
* any ambiguity found in the specification.

## Report

As the `test-writer` agent, launched by `orchestrate`: your report goes back to the orchestrator, which shows the coverage report to the user and hands the rest to the agent that writes the code. No implementation idea. Follow the "Relay protocol" in `AGENTS.md`: `STATUT: FAIT`, or `STATUT: BLOQUÉ <raison>` when the spec or the slice is missing.

With `même session`, the agent that writes the code follows this skill itself and produces the same coverage report for the orchestrator.

## Traceability matrix

`python3 ~/.claude/skills/test-authoring/covers_matrix.py` (run from the repository root, `--help` for the options) lists, from the `covers:` markers and the acceptance criteria found in `specs/`: criterion → tests, criteria without test, tests without marker, tests per criterion. It reads, it never writes.
