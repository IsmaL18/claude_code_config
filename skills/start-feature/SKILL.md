---
name: start-feature
description: Start a new feature with the right level of rigor. Use when beginning feature work and deciding whether to create a spec, involve product clarification, create an ADR, or proceed directly to implementation.
---

# Start feature

1. Understand the requested behavior and inspect the relevant code.
2. Classify the feature:
   - **small**: local, low-risk, no architectural decision;
   - **standard**: meaningful behavior requiring explicit acceptance criteria;
   - **structural/high-risk**: cross-module, security-sensitive, integration-heavy, or architecture-changing.
3. Resolve important product ambiguity before implementation. Use the `product-owner` workflow when needed — in a fresh session, since it must not read source code.
4. For standard or structural features, create or update a versioned spec in `specs/` containing:
   - problem;
   - scope;
   - out of scope when useful;
   - expected behavior;
   - acceptance criteria;
   - relevant edge cases.
5. Decide whether an architectural decision must be preserved.
   - If no, continue.
   - If yes, use the `architect` workflow and create an ADR in `docs/adr/`.
6. Produce a short implementation plan tied to the acceptance criteria.
7. Continue with `tdd-implementation` when behavior is testable.

Trigger an independent review as soon as a review threshold is crossed (new module, new external integration, three increments, unplanned design decision), not once everything is finished.

Do not create ceremony for trivial work. Use the smallest workflow that provides sufficient confidence.

## Next step

End with the **Next step** block defined in `AGENTS.md` (role, skill, session, ready-to-send prompt).

Routing:

* product ambiguity → `product-owner`, new session mandatory (it must not read code); the prompt describes the need and the open questions, no code.
* architectural decision to preserve → `architect`, new session recommended; the prompt gives the spec path and the decision to make.
* otherwise → `tdd-implementation`, continue this session; the prompt restates the spec path, the plan and the first slice.
