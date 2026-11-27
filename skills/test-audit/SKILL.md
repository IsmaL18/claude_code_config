---
name: test-audit
description: Audit a repository's test suite on demand: measure volume, duration, traceability to acceptance criteria, duplicates and obsolete tests, then propose a purge for the user to validate. Use when the suite feels too big, slow or opaque, or before migrating a project to `covers:` markers. Reads and measures only; the purge itself is done by the test-writer after the user's validation.
---
# Test audit

Invoked explicitly by the user, never automatically. Outside the task pipeline: no kickoff contract is needed for the audit itself. A purge, once validated, is a task of its own (level Refactor, characterization not needed: tests are removed, behavior is untouched).

The audit changes nothing. Do not edit a test, a helper, a spec or a configuration. The only file you may write is the report, in the scratchpad.

## 1. Measure

Run from the repository (or the bundle) root. Use the project's `CLAUDE.md` for commands.

1. **Volume.** Test files, test functions (`grep -c`), parametrized cases, lines of test code against lines of production code, number of helper and double files and their size.
2. **Traceability.** `python3 ~/.claude/skills/test-authoring/covers_matrix.py --format json` (add `--tests` / `--specs` for the project layout): tests without marker, criteria without test, criteria with more than one test, markers naming a criterion absent from the specs. In a project not yet migrated, every test is « without marker »: say so once, and rely on test names, a legacy `TESTS.md` (frozen, read-only) and the specs to cluster tests by criterion.
3. **Duration.** Never launch the full suite on your own: it is slow. Ask the user through `AskUserQuestion` whether to run it with durations (`pytest -n auto --durations=30`, `vitest --reporter=verbose`) or to rely on a recent known figure. Report the slowest tests and files.
4. **Fragility signals** (counts, not verdicts): skipped or environment-gated tests (a leg skipped without its resource is NOT VERIFIED), `sleep` and clock use, tests depending on execution order, heavy mocking (`monkeypatch`, `patch`), snapshots, shape assertions (CSS classes, DOM structure).

## 2. Find candidates

Count and cluster first with commands, then read. For a large suite, delegate the reading to read-only sub-agents (`Explore` or `general-purpose`, model `sonnet`; `haiku` for pure inventory), each with a disjoint file scope, a progress file in the scratchpad and a fixed output format (see AGENTS.md, « Delegate to sub-agents »). A sub-agent report is a claim: spot-check every candidate you propose to delete.

A test is a purge candidate when one of these holds:

* **Duplicate.** Another test covers the same criterion at the same seam with the same observable assertion.
* **Per-variant.** One test per input variant, call site or hardening step where one property test over the inputs would do.
* **Obsolete.** Its criterion no longer exists in the specs, or its behavior was removed or rewritten.
* **Shape.** Asserts DOM structure, CSS classes, exact non-contractual text or a snapshot.
* **Already guaranteed.** Re-checks what the typecheck, the lint, a schema or the design system enforces.
* **Tautological or implementation-coupled.** See the anti-patterns in `test-authoring`.
* **Over-parametrized.** More than 4 cases with no distinct risk.
* **No source.** No marker and no criterion it can be traced to. These are proposed for a marker or a deletion, never deleted silently.

Also list **keep for sure**: tests on security, data, external contracts and critical paths, and the only test of an acceptance criterion.

## 3. Report

Write the report in French, in the scratchpad, and summarize it in the chat in at most 15 lines:

```text
Audit des tests — <projet>
Mesures : <n tests, n fichiers, ratio test/prod, durée, ratio tests/critère, critères sans test>
Fragilité : <jambes ignorées, sleep/horloge, mocks, snapshots>
Purge proposée : <n tests> sur <N> (≈ <x %> du volume, ≈ <t> de durée), répartis en :
  - doublons : n · par variante : n · obsolètes : n · forme : n · déjà garantis : n · sans source : n
Gardés d'office : <n>
```

The full report lists each candidate: `file › name`, category, the criterion it covers (or none), why it is redundant, what remains covering the behavior, and the risk of removing it (low / medium / high). Group the candidates by file or by criterion so the user can accept a group at once.

## 4. Validate, then purge

Put the groups to the user through `AskUserQuestion` (calls of 4 at most): accept, reject or keep as is, per group. Recommended option first. Nothing is removed without an explicit « accept ». Any test with no source needs its own answer.

After validation, the purge is a task: kickoff, then `orchestrate` with the test-writer (fresh context) as the author of every change. Its brief carries the validated list, and nothing else. After the purge:

* targeted tests of the touched files, then the full suite once;
* `covers_matrix.py` again, and the before / after counts and duration reported to the user;
* a criterion left with no test is a failure of the purge: restore or rewrite.

## What this skill never does

* Delete or edit a test itself.
* Run the full suite without the user's agreement.
* Propose to delete the only test of an acceptance criterion, or a test on security, data or an external contract, without marking the risk `high`.
