# IMPLEMENT workflow

Use only when an authoritative visual spec covers the composition of the target surfaces (approved Figma, Penpot or Sketch files, mockups, screenshots, specs). Brand colors, fonts, logos or tokens alone are constraints for CREATE or REDESIGN, not an IMPLEMENT spec.

1. **Record** in STATE: authoritative sources, covered surfaces, fidelity expectations, known ambiguities, and the **precedence rule** for conflicts between the spec and the existing system, chosen with the user:
   - `spec overrides system`: the spec wins; new values become tokens and are recorded in MASTER;
   - `system constrains spec`: the closest existing token or primitive wins; deviations from the spec are listed;
   - `ask on conflicts` (default when the user does not choose): each conflict is batched and asked.
   Every later deviation follows this rule.
2. **Extract values from the source, not by eye.** Use the design tool's developer mode, variables and styles, or its MCP connector, when available: colors, type styles, spacing, radii, effects, component variants. From screenshots only, measure at native scale and mark values as approximate.
3. **Map to the system** under the precedence rule: tokens and roles first, then existing primitives and archetypes, before creating anything.
4. **List unspecified behavior**: responsive states, loading, empty, error, interactions, dark mode, missing assets or fonts. Resolve with the user or the derived canon, and record the decision.
5. **Implement the smallest faithful system.** No alternative directions for covered surfaces unless asked.
6. **Measure fidelity (C5).** Render at the spec's viewport (`scripts/capture.mjs`), compare side by side, and check key elements through DOM measurements (computed styles, bounding boxes):
   - colors, type family, weight and size: exact match with the mapped token;
   - spacing, sizes and positions: within about 2px at the same viewport;
   - composition, order and hierarchy: identical.
   Run `scripts/style-inventory.mjs` on implemented routes to confirm no value outside the expected token set appears.
7. **Material deviation** not covered by the precedence rule is blocking until the user approves it.
8. **Core checks** C1-C4 (`quality-gates.md`).
9. **Derive the canon** from covered surfaces when the work spans several screens: MASTER, archetypes and the relevant guarantees of `system-lock.md`.
10. **Uncovered surfaces**: EXTEND if the covered spec establishes a coherent enough canon; REDESIGN constrained by the spec if major composition remains open.
