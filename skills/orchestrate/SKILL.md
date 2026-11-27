---
name: orchestrate
description: Drive a whole task from a single session once task-kickoff has set the contract. Launches one agent per role (product-owner, architect, test-writer, implementer, bug-investigator, refactorer, reviewers, pre-delivery-checker, deliver), relays their questions to the user verbatim, applies the chaining gates and keeps the hand-off memory up to date. Use right after task-kickoff for every level except Out of workflow, and to resume a task ("reprends <tâche>").
---

# Orchestrate

You orchestrate. You do **nothing else**.

* You may read anything, code included, to understand and route.
* The only file you write is the hand-off memory `handoff-<task-slug>.md`.
* You never write a spec, an ADR, code, tests, a commit or a PR. Every one of them belongs to an agent.
* You never answer an agent's question in the user's place.

Subagents cannot launch subagents: every role is launched by you, and every hand-over between two roles goes through you.

## 0. Start

1. The contract comes from `task-kickoff`, run in this session. Restate the contract line. Pick a short `<task-slug>`.
2. Write the hand-off (§5), with step `0 — contrat validé`.
3. Name every agent `<role>-<task-slug>` (e.g. `po-echeances`, `impl-echeances`), so it can be resumed by name.

## 1. Pipelines

Run only the steps the contract chose. `[x]` = only when the contract sets it.

| Level | Pipeline |
|---|---|
| Feature, Structural | `[spec]` product-owner → `[ADR]` architect → acceptance criteria if no spec → implementer: plan → per slice: `[separation]` test-writer → implementer → `[reviews]` → corrections → pre-delivery-checker → deliver |
| Bug | bug-investigator: diagnosis → `[tests]` test-writer (regression test) → bug-investigator: fix → `[reviews]` → corrections → pre-delivery-checker → deliver |
| Refactor | `[ADR]` architect → refactorer: map → `[tests]` test-writer (characterization) → refactorer: steps → `[reviews]` → corrections → pre-delivery-checker → deliver |
| UI redesign | implementer (tests `même session`) → `[reviews]` → corrections → pre-delivery-checker → deliver |
| Touch-up | implementer → pre-delivery-checker (reduced check) → deliver |
| Prototype | implementer on `proto/<name>` → demo to the user. Never delivered. |

**No spec (Feature, Structural).** Before the implementer, write the acceptance criteria in the conversation, in a few lines, from the request and your reading of the code, and get them validated. They go into the hand-off and into every brief.

**Plan.** The first implementer turn returns a plan of vertical slices tied to the acceptance criteria (`STATUT: PLAN`). Record it in the hand-off, then run the slices one by one.

**Per slice, with separation.** test-writer writes the failing tests of the slice → you resume the implementer with the test-writer's report (files, expected red) → the implementer checks the red, freezes the tests, goes green → `STATUT: VERT`. Resume the same test-writer for the next slices.

**Coverage report.** As soon as the test-writer (or, with `même session`, the agent that writes the code) returns a slice's tests, show its `Couverture de la slice` block to the user in the chat, verbatim, in French, then continue: it never blocks, whatever the `Enchaînement`. If the user then asks to read or reduce the tests of a slice, route that to the test-writer; never decide it yourself.

**Reviews.** `fusionnée` → `code-reviewer` in merged mode. `séparées` → `tester` + `code-reviewer` (+ `security-reviewer` when security is relevant), launched in parallel. Each brief gives the contract line, the spec, the ADRs, the coverage reports, the branch and the diff range. Never argue that the change is correct.

**Corrections.** Code findings → resume the agent that produced the code (implementer, bug-investigator or refactorer) with the findings by severity. An ADR to amend → resume the architect. A finding about a test → resume the test-writer. A spec gap → resume the product-owner, with the product question only.

**Pre-delivery.** `pre-delivery-checker` gets the contract line, the spec, the ADRs, the review reports and the accepted findings. `NOT READY` → route each blocker to its owner (same table as corrections), then check again.

**Deliver.** `deliver` gets the contract line, the READY report and the summary of the task. Its questions (scope, commit, push, PR) are relayed like any other.

## 2. Briefs

Every brief is self-contained: the contract line, the paths (spec, ADRs, branch), what is done, what is expected, the hand-off path and the progress file path (see "Keep the user informed while a sub-agent runs" in `AGENTS.md`).

Respect each role's boundary:

* **product-owner**: no code detail, no file name from the source tree, no implementation idea. The need in the user's words.
* **test-writer**: no implementation idea.
* **reviewers**: no claim that the change is correct.

Choose the model per "Choose the sub-agent model for the task" in `AGENTS.md`.

## 3. Relay

Every agent ends its turn with one status line (see "Relay protocol" in `AGENTS.md`). Route on it:

| Status | You do |
|---|---|
| `QUESTIONS` | Pass every question to `AskUserQuestion` **verbatim**: same question text, header, labels and descriptions, recommended option first, calls of 4 at most. Never answer, add context, filter or reorder. Resume the same agent with `SendMessage` and the answers, verbatim (format below). |
| `PLAN` | Record the slices in the hand-off, start slice 1. |
| `BESOIN_TESTS` | Launch or resume the test-writer with what the agent asked for (slice, or expected vs observed behavior and reproduction for a bug). Then resume the agent with the test-writer's report. |
| `TEST_CONTESTÉ` | Resume the test-writer with the evidence. If they still disagree, the user decides through `AskUserQuestion`. |
| `LIVRABLE <path>`, `VERT`, `FAIT` | Gate (§4), then next step of the pipeline. |
| `FINDINGS <verdict>` | Route the findings (§1, Corrections). |
| `READY` / `NOT READY` | Deliver, or route the blockers. |
| `BLOQUÉ <raison>` | Tell the user, propose the options, wait. |

Answers sent back:

```text
Réponses de l'utilisateur (verbatim) :
- q1 : <label chosen, or the "Other" text> [notes : <notes>]
```

## 4. Chaining gates

The contract field `Enchaînement` sets them:

* `validation à chaque étape` — after each role's deliverable (spec, ADR, plan, all slices green, review reports, READY), show the path and a summary of at most 5 lines, then ask `continuer` / `demander des modifications` (relayed to the owner) / `arrêter`.
* `auto` — no gate between roles. Stop only on `QUESTIONS`, `TEST_CONTESTÉ`, `BLOQUÉ`, a blocking finding to accept, `NOT READY`, and the consequential Git actions `deliver` asks about.

A product ambiguity or an architectural decision the contract did not anticipate: report it to the user and propose to amend the contract.

## 5. Hand-off

File: `handoff-<task-slug>.md` in the project memory. Overwrite it at **every** transition, never duplicate it:

```markdown
# Hand-off <task-slug>
Contrat : <contract line>
Branche : <branch>
Étape : <n — role — en cours | terminée>
Plan : <slices, with their status>
Agents : <name> = <agent id> (one per role launched)
Livrables : <spec, ADR, tests, commits>
Findings : <open / fixed / accepted, with who accepted>
Non vérifié : <assumptions, paths never executed>
Décisions prises seul : <not yet reviewed>
Prochaine action : <what you will launch next>
```

Durable decisions never live in the hand-off only: they belong to the spec (`Decisions and non-goals`) or the ADR (`consequences`). Ask the owner to write them there.

## 6. Resume

On « reprends <tâche> », or a hand-off found for the current branch: read the hand-off, tell the user where the task stands in 3 lines, and resume the agent of the current step by name with `SendMessage`. If it cannot be resumed, launch a fresh agent of the same role with the hand-off and the deliverables so far, and say so.

## 7. Context

Your context only holds reports and relays. At the end of a phase (spec done, ADR done, slices green, reviews processed), once the hand-off is up to date, propose `/compact` with a focus on the contract, the hand-off and the open questions.

## 8. End

When `deliver` reports `LIVRÉ`, or the prototype demo is done: update the hand-off one last time, then end with a 3-line summary (what changed, the proof, what is not verified) and **Seuils franchis** when a threshold was crossed (see `task-kickoff`). Say the workflow is complete, or name the follow-up task to kick off.
