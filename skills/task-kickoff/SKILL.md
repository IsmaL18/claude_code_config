---
name: task-kickoff
description: Mandatory kickoff form run at the start of every task. Sets the level, the upstream roles, the reviews, the test strategy, the code/test separation and the proof of done, as a contract the developer validates. Use before any work, and before rounds 2-3 when a workflow skill is invoked directly.
---
# Task kickoff

Every task starts with this form. No exception: not for a typo, a config change or a one-line fix.

The form sets the **contract** of the task. The developer decides. You recommend.

## Rules

* Ask through `AskUserQuestion`. If the tool does not exist, ask the same questions as a numbered text list and wait for the answers.
* Ask the user in French. Keep this file's identifiers (level and option names) recognizable.
* Put your recommended option first, labelled `(Recommandé)`, with a one-line reason.
* Prefill every question from the level preset. Adjust the recommendation to the risk zones touched (see below).
* Inspect the request and the affected code before round 1, just enough to recommend a level. Do not start the work.
* Do not start the work before the contract is validated.
* Skip a round or a question that has no object for the chosen level. Never skip round 1 unless a workflow skill was invoked directly.
* For Touch-up, Prototype and Bug, replace rounds 2 and 3 with one question: confirm the preset (`oui`) or adjust it (`ajuster`, then ask rounds 2 and 3).

## Round 1 — Level

One question: the level. Options (up to 4 per call; give the 3 most plausible plus your recommendation, the developer uses "Other" for the rest):

| Level | Label FR | Entry criteria | Roles (via `orchestrate`) |
|---|---|---|---|
| Out of workflow | Hors workflow | The developer wants no framework. | none, no orchestration |
| Touch-up | Retouche | Presentation only: styles, layout, labels, order or visibility of elements, in existing components or by composing existing components. Also log messages, CLI text, cosmetic config. No new or changed API call. No state or data logic. No auth. No critical path altered. | `implementer` |
| Prototype | Prototype | Exploration, spike, demo. Code is disposable. | `implementer` |
| Bug | Bug | Incorrect, flaky or unexplained behavior. | `bug-investigator` |
| Feature | Feature | New or changed behavior. | `[product-owner]` → `[architect]` → `implementer` |
| Structural | Structurel | New subsystem, new external integration, database architecture, auth, major cross-module change, architectural decision. | `[product-owner]` → `[architect]` → `implementer` |
| UI redesign | Refonte UI | Global rework of screens, layout or visual language, with no change to API contracts or data logic. | `implementer` |
| Refactor | Refactor | Structural change without intended behavior change. | `[architect]` → `refactorer` |

A touch-up that needs any change outside its entry criteria is not a touch-up. Split it: the presentation part stays Touch-up, the rest becomes Feature.

**Out of workflow** ends the form. No rule of this workflow applies. Follow the user's instructions only.

**Prototype** works on a dedicated branch (`proto/<name>`). The prototype is never merged as is. To ship it, start a new task at the target level with the prototype as reference.

When a workflow skill is invoked directly (`/bug-investigation`, `/refactor-module`, `/tdd-implementation`…), the level comes from the skill. Skip round 1. Ask rounds 2 and 3. Exception: `tdd-implementation` serves both Feature and Structural, whose presets differ. Replace round 1 with one question, Feature or Structural. Then run `orchestrate`: the skill invoked is the procedure of the matching agent, not a reason to do the work in this session.

Role agents (`product-owner`, `architect`, `test-writer`, `implementer`, `bug-investigator`, `refactorer`, reviewers, `pre-delivery-checker`, `deliver`) never run the form. They inherit the contract line from the brief that launched them. If it is missing, they report `STATUT: BLOQUÉ` (see "Relay protocol" in `AGENTS.md`).

## Round 2 — Framework

Up to four questions:

1. **Spec** — `non` / `oui (agent product-owner, sans accès au code)`.
2. **ADR** — `non` / `oui (architect)`.
3. **Revues** — `aucune` / `fusionnée (code-reviewer en mode fusionné)` / `séparées (tester + code-reviewer + security-reviewer si pertinent)`.
4. **Enchaînement** — `validation à chaque étape` / `auto`. `validation à chaque étape`: the orchestrator stops after each role's deliverable for your go. `auto`: it chains the roles and stops only on a question, a disputed test, a blocker, a blocking finding or a consequential Git action (see `orchestrate`).

## Round 3 — Tests and proof

Up to three questions:

1. **Stratégie de tests** — `écriture directe` / `aucun test`.
   * `écriture directe`: the test author writes the tests directly under "What deserves a test" in `AGENTS.md`, at most one per acceptance criterion. No plan to validate, no seams to confirm: the review judges the tests afterwards.
   * `aucun test`: write no test. Existing tests must still pass.
2. **Séparation code/tests** — `test-writer en contexte neuf` / `même session`. Skip if `aucun test`.
   * `test-writer en contexte neuf`: the rule "the one who writes the code never writes the tests" applies in full.
   * `même session`: the agent that writes the code also writes the tests, test-first when practical, and records them in `TESTS.md`.
3. **Preuve de fin** (multiSelect) — `capture d'écran par l'agent` / `lint + typecheck + build` / `tests ciblés` / `validation humaine`.

Test execution is fixed, not asked: targeted tests during the work (the touched test files only), the full suite once before the push, in `pre-delivery-check`.

## Presets

| Level | Spec | ADR | Reviews | Enchaînement | Tests | Separation | Proof |
|---|---|---|---|---|---|---|---|
| Touch-up | non | non | aucune | auto | aucun | — | capture + lint/typecheck |
| Prototype | non | non | aucune | auto | aucun | — | validation humaine (demo) |
| Bug | non | non | fusionnée* | auto | écriture directe (1 regression test) | test-writer neuf* | tests ciblés |
| Feature | if ambiguous | if decision | fusionnée* | validation | écriture directe | test-writer neuf* | tests ciblés + lint |
| Structural | oui | oui | séparées | validation | écriture directe | test-writer neuf | tests ciblés + lint/typecheck/build |
| UI redesign | non (mockup or reference capture) | non | fusionnée* | validation | écriture directe, behavior only | même session | capture + validation humaine |
| Refactor | non | if decision | fusionnée* | validation | écriture directe (characterization) | test-writer neuf* | tests ciblés + lint/typecheck/build |

\* Default only when the task touches a risk zone. Otherwise recommend `aucune` and `même session`.

## Risk zones

* business logic in the backend;
* data: schema, migrations, persistence, data pipelines;
* security: authentication, authorization, secrets, untrusted input;
* external integration: third-party API, database, file or message format;
* API contract between components;
* a critical user path.

When the task touches one, say which in the round 1 reason.

## Contract

Once validated, restate the contract in one line and keep it for the whole task:

```text
Contrat — Niveau : Feature · Spec : non · ADR : non · Revues : fusionnée · Enchaînement : validation à chaque étape · Tests : écriture directe · Séparation : test-writer neuf · Preuve : tests ciblés + lint
```

* Pass the contract line in every sub-agent brief.
* `pre-delivery-check` verifies the contract, not a fixed checklist.
* Do not change the contract without the developer's agreement.

Once the contract is validated, run `orchestrate` in this same session (every level except Out of workflow). Do not start the work yourself.

## Threshold crossed during the task

When the work turns out to touch a risk zone the contract did not anticipate, or to leave the entry criteria of its level, continue. You must report it in the final summary, under **Seuils franchis**: the zone, the file, what the contract did not cover, and the level you would recommend.
