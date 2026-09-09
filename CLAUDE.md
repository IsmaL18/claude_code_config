@RTK.md

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
4. Use `tdd-implementation` when behavior can be tested.
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

Use the complete workflow:

1. `product-owner` skill 
2. Versioned specification in `specs/`
3. `architect` skill 
4. ADR in `docs/adr/`
5. `tdd-implementation` skill 
6. Independent `tester`
7. `security-reviewer` subagent when security is relevant
8. Independent `code-reviewer`subagent
9. Corrections
10. `pre-delivery-check` skill
11. `deliver` skill

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

### Prefer minimal changes

Do not modify unrelated code without a reason.

Do not perform opportunistic large refactors during unrelated tasks.

Minimize the surface area touched by each change.

---

### Capitalize mistakes

When a mistake reveals reusable knowledge:

* repository convention or trap → add it to the appropriate `CLAUDE.md`;
* behavior that must never regress → add or improve a test;
* reusable workflow improvement → improve the relevant Skill.

Do not repeatedly solve the same problem from scratch.

---

## 3. Repository structure

Use this structure when appropriate:

```text
project/
├── CLAUDE.md
├── PRODUCT.md
├── USER.md
├── DESIGN.md
├── ARCHITECTURE.md
├── specs/
│   └── ...
├── docs/
│   └── adr/
│       └── ...
└── <functional modules>/
    ├── CLAUDE.md       
    └── PRODUCT.md      # only when useful
```

Do not create documents merely to satisfy this structure.
Create them when they provide durable context that cannot be reliably inferred from the code.

---

## 4. Root `CLAUDE.md`

Every sufficiently important repository should have a root `CLAUDE.md`.

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

Treat `CLAUDE.md` as operational memory, not general documentation.

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

A module may contain its own `CLAUDE.md` when it has significant local:

* commands;
* conventions;
* architecture rules;
* dependencies;
* repository traps.

Do not repeat information already present in the root `CLAUDE.md`.

A module may contain its own `PRODUCT.md` when it represents a sufficiently autonomous functional domain with important business rules or product intent.

Do not create module-level files by default.

---

## 10. Independent review roles

Use specialized agents when an independent context improves review quality.

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
* `bug-investigation`
* `refactor-module`
* `pre-delivery-check`

Interactive role Skills:

* `product-owner`
* `architect`
* `deliver`

The detailed procedure belongs in each Skill, not in this file.
