# REDESIGN workflows

Checks and statuses: `quality-gates.md`.

## REDESIGN / PRODUCT

Same backbone as Full CREATE (`create.md`), plus what an existing product requires.

### Scope and baseline

STATE also records: fixed and open scope; behavior and IA constraints; **strengths to preserve**; route/surface inventory with a mode per surface; rollback and stop conditions.

Before any design work, capture the baseline:
- key workflows and representative secondary surfaces (`scripts/capture.mjs`);
- one `scripts/style-inventory.mjs` run, which shows the current inconsistency and gives a before/after;
- the current path and step count of each critical task, the reference for the walkthrough (C2);
- current accessibility results (`capture.mjs --axe` or project tools), so regressions are visible.

### Isolation strategy

Document a reversible migration plan before editing shared primitives: a theme scoped on the root element, a feature flag, route groups, or temporary `v2` primitives when tokens alone cannot change density, DOM or classes (each with name, owner and removal plan). Check how overlays inherit the scoped theme in this stack (`stacks.md` §Theme scoping and overlays). Account for old/new × light/dark when theming is in scope. A global primitive rewrite is not an isolation strategy.

### Directions and Golden

Follow `create.md` steps 2-10, with these additions:
- the current UI is the stack/current control, and each candidate receives the strengths to preserve;
- the Golden reviewer also receives the baseline captures and checks that no preserved strength was lost and no critical task got slower.

### Lock and propagation

Lock before propagation (`system-lock.md`). Every route or surface ends as `migrated`, `out of scope` or `blocked`, including non-route surfaces: overlays, auth, error and admin pages, charts, embedded surfaces, emails and social images. Secondary screens are not exempt from QA.

### Teardown and final audit

Remove, or retain with rationale: old theme, flags, temporary `v2` primitives, direction sandboxes, obsolete dependencies. Final regression, accessibility, performance and consistency checks, with a final style inventory and accessibility run compared with the baseline.

## REDESIGN / SCOPED

One screen or bounded flow gets a new composition while the product language stays.

1. Read the design-rules section, `MASTER.md` and the canon; without them, extract a mini-system (`extend-modify.md`).
2. Short brief for the target workflow: fit facts with counterfactuals, its critical tasks. The expression thesis is inherited; note the existing signatures the screen must carry.
3. Prior fingerprint for this screen type (written). Generic local compositions, such as a KPI card row above a table, are the main risk.
4. Gate 1 (short).
5. Two candidates differing on at least one structural axis, in sandboxes, with the current screen as control; I1-I4 (I4: inherited signatures present).
6. Gate 2.
7. Implement in structure → system → polish passes; core checks C1-C5; compare with neighboring approved screens and run the style inventory against the product baseline.
8. Gate 3 on the target surface.
9. Promote a pattern to the system only when it is a reusable rule (MASTER, primitives, design-rules section).
10. If the screen needs broad token, shell or primitive changes, reclassify to REDESIGN / PRODUCT.
