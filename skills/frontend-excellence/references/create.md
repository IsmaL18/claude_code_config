# CREATE workflow

Use when establishing a new visual language and no authoritative composition exists. Checks and statuses: `quality-gates.md`.

## Full CREATE

1. **Scope.** `STATE.md` (`assets/project-state.template.md`): scope, branch, targets, real-content source, accessibility target, supported browsers, delegations. Propose the Golden set. Run the preflight and ask the tooling question once (`setup.md`) if STATE has no Tooling section.
2. **Prior fingerprint** (`direction-making.md` §1), before anything product-specific.
3. **Product Brief** (`product-brief.md`): fit facts, critical tasks, expression thesis. Ask the Gate 1 questions in one message.
4. **Gate 1.** No style references before it.
5. **Reference board and directions** (`direction-making.md` §2-5).
6. **Gate 2** (`direction-making.md` §6).
7. **MASTER v0** (`assets/MASTER.template.md`): thesis, signatures, approved direction evidence.
8. **Golden set** in three passes; review structure before spending effort on polish:
   1. structure: layout model, hierarchy, content, states; walk the critical tasks (C2) at the end of this pass, when changes are cheap;
   2. system: tokens, type roles, primitives, archetype and shell components, in the project's mechanisms (`stacks.md`);
   3. polish: details, interaction states, finish.
9. **Golden QA** (`visual-qa.md`): core checks C1-C5, I1-I4 rerun on the implementation, independent review.
10. **Gate 3.**
11. **Lock** (`system-lock.md`), MASTER v1, design-rules section.
12. **Propagate** in coherent batches with the drift procedure (`system-lock.md`); Gate 4 only for a new archetype or material system change, otherwise independent review.
13. **Final audit and teardown**, then report approval status and evidence status.

## Choosing the Golden set

- Small product: one screen. Medium: 1-2 archetypes. Large: 2-3 archetypes.
- The primary archetype always includes the **app shell** (navigation, header, page frame): the most visible and most reused identity carrier.
- Cover the screens of the critical tasks, the densest surface, one critical moment, and an empty or error state.
- Directions are rendered on the primary archetype only; the others are designed during the Golden implementation.

## Lightweight CREATE

For a small isolated surface or low-risk greenfield page where a full system would be disproportionate.

Keep: a short brief with critical tasks and a one-paragraph expression thesis (landing and onboarding pages are where model defaults are strongest); the prior fingerprint; observed references with at least one competitor capture when accessible; the stack control and one or two candidates if the direction is ambiguous; I1-I4; core checks C1-C4.

Skip: multi-archetype Golden set, separate specimen when the surface exercises the system, propagation machinery.

If the surface grows into a multi-screen product, upgrade to Full CREATE.
