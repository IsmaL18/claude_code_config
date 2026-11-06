# EXTEND and MODIFY

## Always first

1. Read the design-rules section in the project's agent instructions, `MASTER.md`, and the token, primitive and archetype sources it points to.
2. Use existing roles, primitives and archetypes before creating anything. A new value or pattern is a system decision, not a local one.

## Existing-system health check

Before EXTEND or a `polish` MODIFY, judge whether the current system is worth extending.

If no MASTER or canon exists and the work spans multiple surfaces, extract a mini-system first: tokens in use, a `scripts/style-inventory.mjs` run on 3-5 representative routes, recurring page and component patterns, 2-3 observed captures, and the generic markers from `anti-patterns.md`.

If the system is clearly generic and the user wants a professional, distinctive or better-looking result: say that extending it will propagate the weakness, recommend REDESIGN or a bounded foundation cleanup, and do not silently treat it as approved. If the user explicitly wants consistency with it, record that and proceed.

## EXTEND

1. Inspect adjacent screens and real product data; identify the critical task of the new screen.
2. Choose the archetype; if none fits, compose with `craft.md` and treat the result as a new pattern.
3. Add only the minimum reusable token, role or primitive, through the system.
4. Prefer the project's existing behavior libraries (`tools.md`).
5. Render the first representative screen and compare it with the canon and adjacent screens.
6. For a new identity-bearing pattern: prior fingerprint for that pattern (written) and I1-I4.
7. Multi-screen EXTEND: checkpoint with the user the first screen that introduces a reusable pattern.
8. Core checks C1-C4 on the new screen (`quality-gates.md`), and `style-inventory.mjs` on touched routes against the baseline, resolving every new value.
9. Update MASTER, archetype recipes and, if needed, the design-rules section, for reusable decisions only.

Reclassify to REDESIGN if the work needs a new language, shell, hierarchy model or broad primitive rewrite.

## MODIFY

### Intensity `local`

1. Read the local design source and adjacent states.
2. Make the smallest coherent change with existing roles and primitives.
3. Render affected states when the change is visually meaningful.
4. Check that it imports no generic default and adds no unexplained style value.
5. One narrow new semantic token or state is allowed and does not make it a REDESIGN.

### Intensity `polish`

The surface should feel materially better without changing the approved language.

1. Capture the current surface.
2. Prioritize issues: hierarchy → layout → density → typography → spacing → component/state finish (`craft.md`).
3. Fix in structure → system → polish passes, only as needed; fixes that belong in a shared primitive go there.
4. Compare before and after next to adjacent screens; run the style inventory on the route; check that the screen's task did not get slower.
5. If the fix needs a new composition thesis or language, reclassify to REDESIGN / SCOPED.
