# AI-assisted development workflow

This file defines my default development workflow across all repositories.

Project-specific instructions always take precedence over these defaults.
Explicit user instructions take precedence over the workflow below.

The goal is to use the **smallest workflow that provides sufficient confidence** for the task.

---

## 1. Start every task with `task-kickoff`, then `orchestrate`

Every task starts with the `task-kickoff` skill. No exception.

The form sets the task contract: level, spec, ADR, reviews, chaining (`Enchaînement`), test strategy, code/test separation, proof of done. The developer validates it. Every rule below applies within that contract.

Then the same session runs the `orchestrate` skill, for every level except Out of workflow. **One session per task.** The orchestrating session only orchestrates: it may read anything, code included, to understand and route, but the only file it writes is the hand-off memory. Every role is an agent launched by it, in its own context, that loads the role's skill:

| Agent | Skill | Produces |
|---|---|---|
| `product-owner` | `product-owner` | `specs/NNN-*.md` |
| `architect` | `architect` | `docs/adr/NNNN-*.md`, amended ADRs |
| `test-writer` | `test-authoring` | tests + `TESTS.md` |
| `implementer` | `tdd-implementation` | production code, corrections |
| `bug-investigator` | `bug-investigation` | diagnosis, fix, corrections |
| `refactorer` | `refactor-module` | refactoring, corrections |
| `tester`, `code-reviewer`, `security-reviewer` | — | findings only |
| `pre-delivery-checker` | `pre-delivery-check` | READY / NOT READY |
| `deliver` | `deliver` | commits, push, PR |

Levels and their pipeline (details in `orchestrate`):

* **Out of workflow** — no rule of this workflow applies. No orchestration.
* **Touch-up** — presentation only. `implementer`, then a reduced pre-delivery check.
* **Prototype** — disposable code on a dedicated branch, by the `implementer`. Never merged as is.
* **Bug** — `bug-investigator`. Do not patch symptoms. After two similar failed attempts, stop and reassess the diagnosis.
* **Feature** — `[product-owner]` → `[architect]` → `implementer` slice by slice with the `test-writer`.
* **Structural** — same as Feature, full role chain below.
* **UI redesign** — `implementer`. The contract still sets tests and proof.
* **Refactor** — `[architect]` → `refactorer`.

Other skills, invoked explicitly, outside the pipeline: `existing-project-bootstrap`, `architecture-audit`.

### Session boundaries

A fresh context is mandatory where independence is the point. Continuity is an asset everywhere else: it is kept by **resuming the same agent** (`SendMessage`, by name), never by doing the work in the orchestrating session.

| Step | When | Context | May read | Must NOT read | Produces |
|---|---|---|---|---|---|
| `product-owner` | spec chosen | fresh, **mandatory**, enforced by a hook | `PRODUCT.md`, `USER.md`, `specs/` | source code | `specs/NNN-*.md` |
| `architect` | ADR chosen, or an ADR to amend | fresh, resumed for amendments | spec, `ARCHITECTURE.md`, ADRs, code structure | — | `docs/adr/NNNN-*.md` |
| `test-writer` (skill `test-authoring`) | separation chosen | fresh, **mandatory**, resumed slice after slice | spec, ADRs, public interfaces, existing tests, `TESTS.md` | implementation internals | tests + `TESTS.md` |
| `implementer` / `bug-investigator` / `refactorer` | every level except Out of workflow | one agent per task, resumed for every slice and correction round | everything | — | production code; tests only if separation is `même session` |
| `code-reviewer` (merged mode) | reviews `fusionnée` | fresh, **mandatory** | everything | — | findings only |
| `tester` + `code-reviewer` + `security-reviewer` | reviews `séparées` | fresh, **mandatory** | everything | — | findings only |
| corrections | after reviews | the agent that produced the code (code), the `architect` (ADR), the `test-writer` (tests) | everything | — | code + amended ADRs |
| `pre-delivery-checker` → `deliver` | Bug, Feature, Structural, UI redesign, Refactor; Touch-up: reduced check only (see `pre-delivery-check`); Prototype: never | fresh | everything | — | READY verdict, then delivery |
| orchestrator (`orchestrate`) | every level except Out of workflow | continuous, compacted at phase ends | everything | — | hand-off memory only |

`security-reviewer` runs only with reviews `séparées`, when security is relevant. In merged mode, `code-reviewer` flags the security issues it notices as findings, with no escalation.

When reviews are not `aucune`, the agent that wrote the code is never the only reviewer of its own work.

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

The proof of done is the one set in the contract. A screenshot or a human validation is valid proof only when the contract chose it.

Never claim done on statements such as "this should work".

---

### Test from requirements, not implementation

When the contract includes tests and a specification or acceptance criteria exist:

1. derive tests from the expected behavior;
2. never derive them from the implementation;
3. confirm new tests fail before implementing the behavior when practical;
4. implement;
5. confirm they pass;
6. keep useful tests permanently.

A bug that could regress gets a regression test, unless the contract says `aucun test`.

---

### What deserves a test

Write a test only when all of these hold:

* **Real risk.** A regression would cost more than the test costs to maintain: business rule, data, security, contract, critical path. At most one test per acceptance criterion, unless justified.
* **Behavior, not shape.** Never assert DOM structure, CSS classes, exact non-contractual text or snapshots. Test the UI through accessible roles and observable effects.
* **Highest fast level.** Prefer one fast integration test over several coupled unit tests. Do not unit-test a detail already covered.
* **Not already guaranteed.** Never test what the typecheck, the lint, a schema or the design system already enforces.

Visual and design rules belong to the lint, the design tokens or the design system. Never to a test.

Automated visual regression (`toHaveScreenshot`, native snapshots) only when the project already has it or the user asks for it.

---

### Run targeted tests, then the full suite once

* Run only the touched test files during the work. Never the full suite, not even as a baseline.
* Run the full suite once, before the push, in `pre-delivery-check`. Exception: when the contract says `aucun test` and the suite is slow, run the targeted tests instead.
* Run the full suite in parallel when the runner allows it (`pytest -n auto` with `pytest-xdist`, vitest by default).

---

### The one who writes the code never writes the tests

This rule applies when the contract sets separation to `test-writer en contexte neuf`. The developer chooses it at kickoff. It is the default for risk zones.

When it applies, tests and production code are written by two separate roles, in two separate contexts:

* the `test-writer` role (agent `test-writer`, skill `test-authoring`) writes and modifies tests, test fixtures, test helpers and test configuration, and records every test it writes in `TESTS.md` at the repository root;
* the agent that writes the code (`implementer`, `bug-investigator`, `refactorer`) writes production code only.

That agent **must never** create, modify, delete, skip, disable or weaken a test, a fixture, a snapshot, a test configuration or `TESTS.md` — not even to fix a typo, an import or an obviously wrong assertion. When a test looks wrong, it stops and sends the evidence back to the `test-writer`; if they disagree on the expected behavior, the user decides.

When the contract sets separation to `même session`, the agent that writes the code also writes its tests, test-first when practical, follows "What deserves a test", and records every test in `TESTS.md`.

`TESTS.md` records every test written, whoever the author.

---

### An asserted behavior is a tested behavior

Any **behavior** stated as a guarantee — in an ADR, a `CLAUDE.md`, an `AGENTS.md`, a docstring or a commit message — must have a test that holds it, named so the assertion can be traced back to it.

If you cannot write that test, you cannot write the assertion.

Never state a visual or design rule as a guarantee. Enforce it with the lint, the design tokens or the design system.

---

### A mock never validates an external contract

A test with a simulated double proves your orchestration, never the contract of a system you do not control. Every external integration must have at least one test exercising the real client's validation path — request construction, schema transformation, serialization — even without network access.

---

### Prove the full path before deepening it

Before building depth on an external integration, make the thinnest possible end-to-end path work against the real system.

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

Ad-hoc agents follow the same role boundaries as defined ones: when separation applies, they never write or modify tests (the `test-writer` role only). They never replace the reviews set in the contract.

Sub-agents cannot launch sub-agents. A role that needs another role (the implementer needs tests, a reviewer's findings need a fix) reports it, and the orchestrating session launches the other role.

A sub-agent's report is a claim, not a fact: verify the points you rely on before acting on them.

When the same ad-hoc role has been briefed in two or three sessions, propose turning it into a defined agent in `~/.claude/agents/`.

#### Keep the user informed while a sub-agent runs

The user must never wait on a sub-agent without knowing where it stands.

1. **At launch**, in one or two lines: what the agent does, the steps it will go through, and a rough duration. Say it is a guess.
2. **During the run**, launch the agent in the background and put in its brief a progress file in the scratchpad (e.g. `<scratchpad>/progress-<agent>.md`) that it overwrites at each step with: `step n/N`, what is done, what remains. Read that file about every minute and relay it to the user in one line: step reached, what remains, whether it is nearly done. If nothing changed since the last relay, say so rather than staying silent.
3. **If the agent seems stuck** (no progress across several checks), say so and propose waiting, stopping it, or continuing it with a narrower brief.
4. **On return**, summarize the result in a few lines before anything else.

Do not poll a sub-agent that finishes in well under a minute: launch it in the foreground and report the result.

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

### Keep the context short: compact when it pays off

Tokens are a cost. When the context becomes long and compacting is worthwhile, compact or compress the conversation with the commands available instead of dragging the full history along.

Compact when:

* a phase is finished (exploration done, plan agreed, a slice implemented and verified) and the next one does not need the raw history;
* the context is full of bulky outputs already digested (long logs, large file reads, search results);
* the session switches to an unrelated subtask.

Do not compact when:

* you are in the middle of a delicate diagnosis or an unfinished edit whose details are not written down yet;
* the context is short, or the next steps still rely on exact outputs you would lose.

How:

1. Before compacting, make sure what matters survives: the decisions, the files touched, the open questions, what is not verified (the hand-off memory, see "Keep the hand-off up to date").
2. Use `/compact` with a focus instruction naming what to keep (e.g. `/compact keep the agreed plan, the failing test names and the files modified`). If you cannot run it yourself, tell the user in one line why now is a good moment and give the exact command to type.
3. In the orchestrating session, compact at the end of each phase (spec, ADR, slices green, reviews processed), once the hand-off is up to date. A new role never needs `/clear`: it is a fresh agent.
4. Prefer delegating bulky exploration to a sub-agent so the raw output never enters the main context.

Compacting never replaces a fresh-context role set in the contract (`product-owner`, `test-writer`, reviewers): those are always fresh agents.

---

### Capitalize mistakes

When a mistake reveals reusable knowledge:

* repository convention or trap → add it to the appropriate `CLAUDE.md` or `AGENTS.md` depending
on what's used in the project;
* behavior that must never regress → add or improve a test, by the author the contract sets;
* reusable workflow improvement → improve the relevant Skill.

Do not repeatedly solve the same problem from scratch. 

The global instructions have a single source of truth: `~/.claude/AGENTS.md`, imported by `~/.claude/CLAUDE.md`. Edit only `AGENTS.md`.

---

### Keep the hand-off up to date

The orchestrating session overwrites the hand-off memory `handoff-<task-slug>.md` at every transition between roles (format in `orchestrate`). It records:

1. **the contract line, the branch, the current step** and the plan with the status of each slice;
2. **the agents launched**, by name and id, so they can be resumed;
3. **what is done**, and where to verify it (commits, tests);
4. **what is not verified** — assumptions, paths never executed, estimated figures. This is the most important section, and the one that gets forgotten;
5. **the decisions taken alone**, not yet reviewed;
6. **the next action**.

Record it in the project memory, not in a repository file: progress state is not documentation and it expires fast. A task is resumed from it (« reprends <tâche> ») in any later session.

#### Where each kind of information lives

| Kind | Where | Examples |
|---|---|---|
| **Durable decisions** | the artifact the role produces, versioned: spec (`Decisions and non-goals`), ADR (`consequences`) | non-goals, rejected options, business rules, constraints the implementation must respect |
| **Progress state** | project memory, file `handoff-<task-slug>.md` (update it, never duplicate) | contract line, plan and slices, agents, what is done, what is not verified, open questions |
| **Everything else** | the conversation of an agent or of the orchestrator — lost on compaction or restart | reasoning, discarded drafts, conversational agreements |

Never put a durable decision in memory only (it is local, unversioned and invisible to a fresh-context role). Never put progress state in the spec or ADR. A role that must not read code (`product-owner`) gets no code detail in its brief.

---

### Relay protocol

Agents cannot talk to the user and cannot launch agents. Every role agent ends each turn with **one** status line, which the orchestrating session routes:

| Status | Meaning |
|---|---|
| `QUESTIONS` | the agent needs the user; the block below follows |
| `PLAN` | slices or steps proposed (implementer, refactorer) |
| `BESOIN_TESTS <what>` | tests needed from the test-writer: a slice, a regression test (expected vs observed, reproduction), characterization tests |
| `TEST_CONTESTÉ` | a test looks wrong; the evidence follows (see `tdd-implementation`) |
| `LIVRABLE <path>` | spec or ADR written or amended |
| `VERT` / `FAIT` | slice green / work done and verified |
| `FINDINGS <bloquant \| non bloquant>` | review verdict, findings follow |
| `READY` / `NOT READY` | pre-delivery verdict, blockers tagged with their owner |
| `LIVRÉ` | delivered |
| `BLOQUÉ <raison>` | the agent cannot continue without a decision |

Questions use this block, at most 4 per turn, 2 to 4 options each, the recommended option first. Ask the whole current frontier at once:

```text
STATUT: QUESTIONS
- id: q1
  header: <max 12 chars>
  question: <full, self-contained question, ending with ?>
  multiSelect: false
  options:
    - <label> (Recommandé) :: <what it implies, trade-off>
    - <label> :: <...>
```

The orchestrating session relays the questions to the user **verbatim** and resumes the same agent with the answers verbatim. It never answers in the user's place and never adds context, so an isolated role stays isolated.

A skill's procedure that says "ask the user" means, for an agent, "ask through this block".

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
├── TESTS.md        # registry of every test written
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

## 10. Roles

Every role is an agent in `~/.claude/agents/`, launched by `orchestrate` (see §1). The production roles (`product-owner`, `architect`, `implementer`, `bug-investigator`, `refactorer`, `pre-delivery-checker`, `deliver`) load the skill of the same procedure. The independent roles below review or test from a fresh context.

### `test-writer`

Writes the tests, before the implementation, from the specification, at seams it picks itself — never from the implementation.

When separation applies, only role allowed to touch tests and `TESTS.md`. Never writes production code.

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

In merged mode (reviews `fusionnée`), also checks behavior against the acceptance criteria and flags shape or superfluous tests.

These agents review from a fresh context.

---

## 11. Workflow Skills

Use the relevant Skill instead of reproducing its full procedure manually.

Run in the orchestrating session:

* `task-kickoff` — first, on every task
* `orchestrate` — right after, for every level except Out of workflow; also to resume a task

Role procedures, loaded by their agent:

* `product-owner`, `architect`, `tdd-implementation`, `test-authoring`, `bug-investigation`, `refactor-module`, `pre-delivery-check`, `deliver`

Invoked explicitly, outside the pipeline:

* `existing-project-bootstrap`
* `architecture-audit`
* `grilling` (alias `grill-me`)

The detailed procedure belongs in each Skill, not in this file.
