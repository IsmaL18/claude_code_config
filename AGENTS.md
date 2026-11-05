# AI-assisted development workflow

This file defines my default development workflow across all repositories.

Project-specific instructions always take precedence over these defaults.
Explicit user instructions take precedence over the workflow below.

The goal is to use the **smallest workflow that provides sufficient confidence** for the task.

---

## 1. Start every task with `task-kickoff`

Every task starts with the `task-kickoff` skill. No exception.

The form sets the task contract: level, spec, ADR, reviews, Next step, test strategy, code/test separation, proof of done. The developer validates it. Every rule below applies within that contract.

Levels and their carriers:

* **Out of workflow** — no rule of this workflow applies.
* **Touch-up** — presentation only. No skill.
* **Prototype** — disposable code on a dedicated branch. Never merged as is.
* **Bug** — `bug-investigation`. Do not patch symptoms. After two similar failed attempts, stop and reassess the diagnosis.
* **Feature** — `start-feature`, then `tdd-implementation`.
* **Structural** — `start-feature`, then `tdd-implementation`, full role chain below.
* **UI redesign** — no skill. The contract still sets tests and proof.
* **Refactor** — `refactor-module`.

Other skills, invoked explicitly: `existing-project-bootstrap`, `architecture-audit`.

### Session boundaries

A fresh context is mandatory where independence is the point. Continuity is an asset everywhere else.

| Step | When | Context | May read | Must NOT read | Produces |
|---|---|---|---|---|---|
| `product-owner` | spec chosen | fresh, **mandatory** | `PRODUCT.md`, `USER.md`, `specs/` | source code | `specs/NNN-*.md` |
| `architect` | ADR chosen | fresh, recommended | spec, `ARCHITECTURE.md`, ADRs, code structure | — | `docs/adr/NNNN-*.md` |
| `test-writer` (skill `test-authoring`) | separation chosen | fresh, **mandatory** | spec, ADRs, public interfaces, existing tests, `TESTS.md` | implementation internals | tests + `TESTS.md` |
| implementation | every level except Out of workflow | continuous | everything | — | production code; tests only if separation is `même session` |
| `code-reviewer` (merged mode) | reviews `fusionnée` | fresh, **mandatory** | everything | — | findings only |
| `tester` + `code-reviewer` + `security-reviewer` | reviews `séparées` | fresh, **mandatory** | everything | — | findings only |
| corrections | after reviews | continuous | everything | — | code + amended ADRs |
| `pre-delivery-check` → `deliver` | Bug, Feature, Structural, UI redesign, Refactor; Touch-up: reduced check only (see `pre-delivery-check`); Prototype: never | continuous | everything | — | delivery |

`security-reviewer` runs only with reviews `séparées`, when security is relevant. In merged mode, `code-reviewer` flags the security issues it notices as findings, with no escalation.

When reviews are not `aucune`, the implementation session is never the only reviewer of its own work.

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

* Run only the tests of the touched scope during the work.
* Run the full suite once, in `pre-delivery-check`. Exception: when the contract says `aucun test` and the suite is slow, run the targeted tests instead.
* Run a full baseline before the work only when the suite is fast. Otherwise, run a targeted baseline.

---

### The one who writes the code never writes the tests

This rule applies when the contract sets separation to `test-writer en contexte neuf`. The developer chooses it at kickoff. It is the default for risk zones.

When it applies, tests and production code are written by two separate roles, in two separate contexts:

* the `test-writer` role (agent `test-writer`, skill `test-authoring`) writes and modifies tests, test fixtures, test helpers and test configuration, and records every test it writes in `TESTS.md` at the repository root;
* the implementation session writes production code only.

The implementation session **must never** create, modify, delete, skip, disable or weaken a test, a fixture, a snapshot, a test configuration or `TESTS.md` — not even to fix a typo, an import or an obviously wrong assertion. When a test looks wrong, it stops and sends the evidence back to the `test-writer`; if they disagree on the expected behavior, the user decides.

When the contract sets separation to `même session`, the implementation session writes its tests, test-first when practical, follows "What deserves a test", and records every test in `TESTS.md`.

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

1. Before compacting, make sure what matters survives: the decisions, the files touched, the open questions, what is not verified (see "Hand off before ending a session" for the content, kept in the project memory).
2. Use `/compact` with a focus instruction naming what to keep (e.g. `/compact keep the agreed plan, the failing test names and the files modified`). If you cannot run it yourself, tell the user in one line why now is a good moment and give the exact command to type.
3. Prefer `/clear` plus a self-contained prompt (the "Next step" block) when the next step is a new role or a fresh context anyway.
4. Prefer delegating bulky exploration to a sub-agent so the raw output never enters the main context.

Compacting never replaces a fresh-context role set in the contract (`product-owner`, `test-writer`, reviewers): those still start in a new session.

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

### Hand off before ending a session

When the contract sets Next step to `oui`, before ending the session, record:

1. **what is done**, and where to verify it (commits, tests);
2. **what is not verified** — assumptions, paths never executed, estimated figures. This is the most important section, and the one that gets forgotten;
3. **the decisions taken alone**, not yet reviewed;
4. **the next step**, and the role that should take it.

Record this in the project memory, not in a repository file: progress state is not documentation and it expires fast.

---

### End every role with the next step and its prompt

When the contract sets Next step to `oui` and a role finishes (product owner, architect, implementation, test writer, reviewer, delivery, bug investigation, refactoring, bootstrap, audit…), its last output to the user is a **Next step** block:

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

* **Self-contained.** A new session has none of this context: give the repository, the contract line, the paths of the spec, ADRs, `TESTS.md` and branch, what is done, what remains, and the open questions or review findings to process.
* **Respect the boundary of the next role.** The prompt for `product-owner` contains no code or implementation detail; the brief for `test-writer` contains no implementation idea; the prompt for a reviewer does not argue that the change is correct.
* **One block per turn.** If the user already asked for the following steps (e.g. `pre-delivery-check` then `deliver`), do them in sequence and produce a single **Next step** block, at the very end. Same when a review is launched from the implementation session: no intermediate block.
* **Pick one.** Recommend a single next step; list alternatives only with the condition that would select them.
* **Say when the workflow ends.** If nothing remains (delivered, audit only), say so instead of inventing a step, and give the follow-up prompt only if a follow-up was identified.

Add **Seuils franchis** before the block when a threshold was crossed (see `task-kickoff`).

The routing for each role is in the "Next step" section of its skill or agent. This block complements the memory hand-off above: the memory records the state, the block tells the user what to launch.

When the contract sets Next step to `non`, end with a 3-line summary: what changed, the proof, what is not verified. Add **Seuils franchis** when a threshold was crossed (see `task-kickoff`).

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

## 10. Independent roles

Use specialized agents when an independent context improves review quality.

### `test-writer`

Writes the tests, before the implementation, from the specification and the agreed seams — never from the implementation.

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

Available workflow Skills:

* `task-kickoff` — first, on every task
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
* `grilling` (alias `grill-me`)

The detailed procedure belongs in each Skill, not in this file.
