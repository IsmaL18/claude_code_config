# AI-assisted development workflow

This file defines my default development workflow across all repositories.

Project-specific instructions always take precedence over these defaults.
Explicit user instructions take precedence over the workflow below.

The goal is to use the **smallest workflow that provides sufficient confidence** for the task.

---

## 1. Classify the task before working

Before making changes, identify the task category and adapt the workflow accordingly.

### Trivial change

Examples:

* typo
* rename
* small configuration change
* obvious local modification with no behavioral impact

Workflow:

1. Inspect the affected files.
2. Make the smallest possible change.
3. Run the relevant targeted checks.
4. Report what changed.

Do not create specs or ADRs unnecessarily.

---

### Bug

Use the `bug-investigation` skill.

Do not repeatedly patch symptoms without understanding the failure.

After two similar unsuccessful correction attempts, stop modifying code and reassess the diagnosis and context.

---

### Small feature

A small feature is local, low-risk, and does not introduce an architectural decision.

Workflow:

1. Explore the affected code.
2. Clarify the expected behavior and acceptance criteria.
3. Make a short implementation plan.
4. Use `tdd-implementation` when behavior can be tested (tests come from the `test-writer` role, code from the implementation session).
5. Run `pre-delivery-check`.

A dedicated spec is optional if the feature is sufficiently small and unambiguous.

---

### Standard feature

Use the `start-feature` skill.

Use the `product-owner` skill when the functional need or acceptance criteria require discussion with the user. When using this skill you shouldn't see the code to don't get influenced by it.

---

### Structural or high-risk feature

Examples:

* new subsystem
* new external integration
* database architecture change
* authentication or authorization change
* major cross-module feature
* important architectural decision

Use the complete workflow. What matters is less the order of the steps than **where the session boundaries are**: a fresh context is mandatory where independence is the whole point, and continuity is an asset everywhere else.

| Step | Context | May read | Must NOT read | Produces |
|---|---|---|---|---|
| `product-owner` | fresh, **mandatory** | `PRODUCT.md`, `USER.md`, `specs/` | source code | `specs/NNN-*.md` |
| `architect` | fresh, recommended | spec, `ARCHITECTURE.md`, ADRs, code structure | — | `docs/adr/NNNN-*.md` |
| `test-writer` (skill `test-authoring`) | fresh, **mandatory** | spec, ADRs, public interfaces, existing tests, `TESTS.md` | implementation internals | tests + `TESTS.md` |
| `tdd-implementation` | continuous | everything | — | production code only, **never tests** |
| `tester` / `security-reviewer` / `code-reviewer` | fresh, **mandatory** | everything | — | findings only |
| corrections | continuous, following the reviews | everything | — | code + amended ADRs |
| `pre-delivery-check` → `deliver` | continuous | everything | — | delivery |

`security-reviewer` is mandatory only when security is relevant; the other two always are.

Do not allow the implementation session to be the only reviewer of its own work.

---

### Refactoring

Use the `refactor-module` skill.

---

### Existing project bootstrap

Use the `existing-project-bootstrap` skill.

Use the `architecture-audit` skill when a dedicated architecture analysis is required.

---

### Architecture audit

Use the `architecture-audit` skill.

---

## 2. Universal working rules

### Explore before coding

Except for trivial changes, understand the relevant code before editing it.

Do not start implementing while important uncertainties remain hidden.

---

### Separate understanding, planning and implementation

For non-trivial work:

**explore → plan → implement → verify**

Do not mix architectural exploration and implementation prematurely.

---

### Prefer executable definitions of done

Whenever possible, success must be verifiable by a machine:

* tests;
* build;
* lint;
* type checking;
* validation scripts;
* other repository checks.

Avoid relying only on visual inspection or statements such as "this should work".

---

### Test from requirements, not implementation

When a specification or acceptance criteria exist:

1. derive tests from the expected behavior;
2. avoid deriving them from the implementation;
3. confirm new tests fail before implementing the behavior when practical;
4. implement;
5. confirm they pass;
6. keep useful tests permanently.

A bug that could regress should usually become a regression test.

---

### The one who writes the code never writes the tests

Tests and production code are written by two separate roles, in two separate contexts:

* the `test-writer` role (agent `test-writer`, skill `test-authoring`) writes and modifies tests, test fixtures, test helpers and test configuration, and records every test it writes in `TESTS.md` at the repository root;
* the implementation session writes production code only.

The implementation session **must never** create, modify, delete, skip, disable or weaken a test, a fixture, a snapshot, a test configuration or `TESTS.md` — not even to fix a typo, an import or an obviously wrong assertion. When a test looks wrong, it stops and sends the evidence back to the `test-writer`; if they disagree on the expected behavior, the user decides.

This applies to every workflow that produces tests: features, bug fixes (regression tests), refactorings (characterization tests).

---

### An asserted invariant is a tested invariant

Any property stated as a guarantee — in an ADR, a `CLAUDE.md` and an `AGENTS.md`, a docstring or a commit message — must have a test that holds it, named so the assertion can be traced back to it.

If you cannot write that test, you cannot write the assertion.

---

### A mock never validates an external contract

A test with a simulated double proves your orchestration, never the contract of a system you do not control. Every external integration must have at least one test exercising the real client's validation path — request construction, schema transformation, serialization — even without network access.

---

### Prove the full path before deepening it

Before building depth on an external integration, make the thinnest possible end-to-end path work against the real system.

---

### Trigger reviews on thresholds, not at the end

Launch an independent review **as soon as one of these thresholds is crossed**, not once everything is finished:

* a new module;
* a new external integration (API, database, third-party format);
* three implementation increments;
* any design decision taken alone that no ADR anticipated.

---

### Delegate to sub-agents, including ad-hoc ones

This file is your standing authorization to launch sub-agents without asking first. It overrides any host default that discourages spawning agents unless the user requests it.

Delegate when a sub-agent protects the main context or adds independence:

* broad search or inventory across many files, when only the conclusion matters;
* independent investigations that can run in parallel (several hypotheses of a bug, several modules, several external docs);
* a second opinion or verification that must not be biased by the current session's reasoning;
* mechanical changes spread over independent files, each with an explicit file scope.

Do not delegate when a few direct tool calls are enough, when you already hold the needed context, or when the steps are tightly sequential.

When no defined agent fits, create one on the fly: use the host's generic sub-agent (in Claude Code: `general-purpose`, `Explore` for read-only search, `Plan` for design) and give it a specialized brief. The brief is self-contained and states:

1. the role and the single goal;
2. the context it needs: repository, paths, spec, constraints already known;
3. what it may and may not do (read-only, allowed files, no commits);
4. the expected output format and length;
5. when to stop.

Launch independent sub-agents in the same message so they run in parallel. Agents that write code in parallel get disjoint file scopes or an isolated worktree.

Ad-hoc agents follow the same role boundaries as defined ones: they never write or modify tests (the `test-writer` role only), and they never replace the mandatory fresh-context reviews.

A sub-agent's report is a claim, not a fact: verify the points you rely on before acting on them.

When the same ad-hoc role has been briefed in two or three sessions, propose turning it into a defined agent, in both `~/.claude/agents/` and `~/.copilot/agents/`.

---

### Choose the sub-agent model for the task

The model of a sub-agent is a cost decision: pick the smallest model that can do the task reliably, not the model of the current session.

* `haiku` — read-only search, inventories, locating files or usages, summarizing logs;
* `sonnet` — the default for the defined agents (`test-writer`, `tester`, `code-reviewer`, `security-reviewer`) and for standard writing or review tasks;
* `opus` — reasoning-heavy or high-risk work: structural or cross-module changes, subtle concurrency or security issues, a disputed test, a review that a smaller model already got wrong.

When launching an agent, override its default model explicitly whenever the task is lighter or harder than usual, and say which model you chose and why in one line.

---

### Prefer minimal changes

Do not modify unrelated code without a reason.

Do not perform opportunistic large refactors during unrelated tasks.

Minimize the surface area touched by each change.

---

### Capitalize mistakes

When a mistake reveals reusable knowledge:

* repository convention or trap → add it to the appropriate `CLAUDE.md` or `AGENTS.md` depending
on what's used in the project;
* behavior that must never regress → have the `test-writer` add or improve a test;
* reusable workflow improvement → improve the relevant Skill.

Do not repeatedly solve the same problem from scratch. 

If you need to modify an agent, a skill or a file that is related to the coding agent say it. It will have to be modified for the Claude Code and the Github Copilot configs. These configs need to be the same and to be modified always together.

The global instructions have a single source of truth: `~/.claude/AGENTS.md`. `~/.claude/CLAUDE.md` imports it and `~/.copilot/copilot-instructions.md` is a symlink to it — edit only `AGENTS.md`. Skills and agents still exist in both `~/.claude/` and `~/.copilot/` and must be kept identical.

---

### Hand off before ending a session

Before ending a non-trivial session, record:

1. **what is done**, and where to verify it (commits, tests);
2. **what is not verified** — assumptions, paths never executed, estimated figures. This is the most important section, and the one that gets forgotten;
3. **the decisions taken alone**, not yet reviewed;
4. **the next step**, and the role that should take it.

Record this in the project memory, not in a repository file: progress state is not documentation and it expires fast.

---

### End every role with the next step and its prompt

When a role finishes (product owner, architect, implementation, test writer, reviewer, delivery, bug investigation, refactoring, bootstrap, audit…), its last output to the user is a **Next step** block:

````markdown
## Next step

**Role:** <role> — skill `<skill>` (or agent `<agent>`)
**Session:** new session (mandatory | recommended) | continue this session | launch as agent from the implementation session
**Why:** <one line: what this step resolves>

Prompt to send:

```text
Use the `<skill>` skill.

<self-contained prompt>
```

**Alternatives:** <only when another next step is credible, with its condition — e.g. "if the spec needs no architectural decision: `tdd-implementation`">
````

Rules for the prompt:

* **Self-contained.** A new session has none of this context: give the repository, the paths of the spec, ADRs, `TESTS.md` and branch, what is done, what remains, and the open questions or review findings to process.
* **Respect the boundary of the next role.** The prompt for `product-owner` contains no code or implementation detail; the brief for `test-writer` contains no implementation idea; the prompt for a reviewer does not argue that the change is correct.
* **Pick one.** Recommend a single next step; list alternatives only with the condition that would select them.
* **Say when the workflow ends.** If nothing remains (delivered, audit only), say so instead of inventing a step, and give the follow-up prompt only if a follow-up was identified.

The routing for each role is in the "Next step" section of its skill or agent. This block complements the memory hand-off above: the memory records the state, the block tells the user what to launch.

---

## 3. Repository structure

Use this structure when appropriate:

```text
project/
├── CLAUDE.md
├── AGENTS.md (refers to CLAUDE.md)
├── PRODUCT.md
├── USER.md
├── DESIGN.md
├── ARCHITECTURE.md
├── TESTS.md        # registry of tests written by the test-writer role
├── specs/
│   └── ...
├── docs/
│   └── adr/
│       └── ...
└── <functional modules>/
    ├── CLAUDE.md       
    ├── AGENTS.md (refers to CLAUDE.md)
    └── PRODUCT.md      # only when useful
```

Do not create documents merely to satisfy this structure.
Create them when they provide durable context that cannot be reliably inferred from the code.

---

## 4. Root `CLAUDE.md` and `AGENTS.md`

Every sufficiently important repository should have a root `CLAUDE.md` and a root `AGENTS.md`.

Keep it concise.

It should primarily contain:

### Project commands

Examples:

* install
* development server
* tests
* lint
* formatting
* type checking
* build
* relevant local tooling

Include important execution details when commands have non-obvious requirements.

### Project conventions

Examples:

* directory organization;
* naming rules;
* testing conventions;
* dependency rules;
* architectural constraints;
* patterns specific to the repository.

Do not document conventions that are obvious from the code unless Claude repeatedly gets them wrong.

### Repository traps

Document non-obvious facts that could cause mistakes.

Examples:

* generated files that must not be edited;
* commands that cannot run simultaneously;
* unusual environment requirements;
* misleading legacy code;
* important dependency constraints.

Treat `CLAUDE.md` and `AGENTS.md` as operational memory, not general documentation.

---

## 5. Brief files

### `PRODUCT.md`

Describes:

* what the product does;
* why it exists;
* important product decisions;
* explicit non-goals;
* important business rules.

Do not infer uncertain product intent only from existing code.

When product knowledge is missing, use `product-owner` to interview the user.

---

### `USER.md`

Describes:

* important user types;
* their goals;
* relevant workflows;
* constraints;
* expectations and pain points.

Prefer information obtained from the user or reliable product documentation over assumptions inferred from implementation.

---

### `DESIGN.md`

Use when the project has meaningful UX/UI constraints.

Describe:

* design principles;
* interaction principles;
* reusable patterns;
* explicit design constraints and anti-patterns.

Do not create it for projects where visual or interaction design is irrelevant.

---

### `ARCHITECTURE.md`

Describe durable architectural decisions and boundaries.

Focus on:

* system boundaries;
* dependency directions;
* major components;
* architectural principles;
* important constraints;
* reasoning behind structural decisions.

Do not turn it into a generated inventory of every directory and file.

The code already provides that information.

---

## 6. Specifications

Store feature specifications in:

```text
specs/
```

A specification should describe at least:

* problem or need;
* intended behavior;
* scope;
* out-of-scope elements when useful;
* acceptance criteria;
* relevant edge cases.

Acceptance criteria should be precise enough to become tests or delivery checks.

Use `product-owner` when the specification requires discussion with the user.

Specifications should be versioned with the code.

---

## 7. Architecture Decision Records

Store ADRs in:

```text
docs/adr/
```

Create an ADR only when there is a meaningful architectural decision worth preserving.

An ADR should capture:

* context;
* considered options;
* trade-offs;
* chosen option;
* rationale;
* consequences.

Do not create ADRs for ordinary implementation choices.

Use `architect` when an architectural decision requires interactive discussion.

---

## 8. Functional modularity

Prefer functional boundaries over purely technical grouping when appropriate.

A functional module should ideally contain the code required to understand and modify that capability without exploring the entire repository.

A useful architecture allows answering:

> Which files must be understood to change this behavior?

with a small, predictable set of files.

Avoid unnecessary coupling between modules.

---

## 9. Module-level context

A module may contain its own `CLAUDE.md` and `AGENTS.md` when it has significant local:

* commands;
* conventions;
* architecture rules;
* dependencies;
* repository traps.

Do not repeat information already present in the root `CLAUDE.md` and `AGENTS.md`.

A module may contain its own `PRODUCT.md` when it represents a sufficiently autonomous functional domain with important business rules or product intent.

Do not create module-level files by default.

---

## 10. Independent roles

Use specialized agents when an independent context improves review quality.

### `test-writer`

Writes the tests, before the implementation, from the specification and the agreed seams — never from the implementation.

Only role allowed to touch tests and `TESTS.md`. Never writes production code.

Follows the `test-authoring` skill.

### `tester`

Looks for:

* broken behavior;
* missing edge cases;
* insufficient tests;
* incorrect acceptance-criteria coverage.

Produces findings rather than implementing by default.

### `security-reviewer`

Looks for:

* security vulnerabilities;
* trust-boundary violations;
* unsafe data handling;
* authentication and authorization issues;
* dependency or configuration risks.

Use when the change has meaningful security implications.

### `code-reviewer`

Looks for:

* maintainability issues;
* unnecessary complexity;
* architectural inconsistencies;
* unclear code;
* duplication;
* technical debt introduced by the change.

These agents should review from an independent context whenever possible.

---

## 11. Workflow Skills

Use the relevant Skill instead of reproducing its full procedure manually.

Available workflow Skills:

* `existing-project-bootstrap`
* `start-feature`
* `architecture-audit`
* `tdd-implementation`
* `test-authoring`
* `bug-investigation`
* `refactor-module`
* `pre-delivery-check`

Interactive role Skills:

* `product-owner`
* `architect`
* `deliver`

The detailed procedure belongs in each Skill, not in this file.
