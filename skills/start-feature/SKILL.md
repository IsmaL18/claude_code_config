---
name: start-feature
description: Start a Feature or Structural task once its contract is set by task-kickoff. Runs the spec and ADR steps the contract chose, then hands off to implementation.
---

# Start feature

Run `task-kickoff` first. The level and the spec and ADR choices come from the contract. Do not classify again.

1. Understand the requested behavior and inspect the relevant code.
2. Spec `oui` → use the `product-owner` workflow in a fresh session, since it must not read source code. It creates or updates a versioned spec in `specs/` containing:
   - problem;
   - scope;
   - out of scope when useful;
   - expected behavior;
   - acceptance criteria;
   - relevant edge cases.
3. Spec `non` → write the acceptance criteria in the conversation, in a few lines, and get them validated.
4. ADR `oui` → use the `architect` workflow and create an ADR in `docs/adr/`.
5. Produce a short implementation plan tied to the acceptance criteria. When the next step is a fresh session, save the plan in the hand-off memory `handoff-<task-slug>.md` (see `AGENTS.md`), since the conversation will be lost.
6. Continue with `tdd-implementation` when the contract includes tests. Otherwise, implement and prove with the contract's proof.

A product ambiguity or an architectural decision the contract did not anticipate: report it to the developer and propose to amend the contract.

## Next step

When the contract sets Next step to `oui`, end with the **Next step** block defined in `AGENTS.md` (role, skill, session, ready-to-send prompt).

Routing:

* spec `oui` → `product-owner`, new session mandatory (it must not read code); the prompt gives the contract line, describes the need and the open questions, no code.
* ADR `oui` → `architect`, new session recommended; the prompt gives the contract line, the spec path and the decision to make.
* otherwise → `tdd-implementation`, continue this session; the prompt restates the contract line, the spec path, the plan and the first slice.
