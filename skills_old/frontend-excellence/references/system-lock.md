# Lock the System

Run after Golden approval, before propagation. Update `MASTER.md` to v1 at the same time.

Goal: make drift hard to write, not just possible to see. In a large app, drift mostly comes from the many small changes made later by agents or people who never load this skill. The lock must therefore live in code, in CI and in the instructions every agent reads.

Lock **properties, not a particular architecture**. Use the project's existing mechanisms (component kit theme, internal design system, CSS-in-JS theme...) whenever they deliver the guarantee; examples below are illustrations and `stacks.md` lists equivalents per stack. Do not add a parallel abstraction next to one that already works.

## Guarantees

Each ends as `done` (with its mechanism and location) or `exception` (concrete reason, recorded in STATE, told to the user). "Not useful" is not an acceptable reason for L1, L2, L3 or L6.

**L1. Governed tokens.** All design values come from one governed source; the framework's or kit's default palette cannot be used by accident; components consume semantic roles (`surface-raised`, `text-muted`, `status-danger`...) rather than raw ramps. A primitive-ramp layer feeding a semantic layer is recommended because it makes theming and dark mode safe.

**L2. Constrained component API.** Type roles and identity-bearing visual properties (intent, size, density, emphasis) are exposed as enumerated inputs (variants, typed props, component styles). Free style overrides on primitives are limited to layout and placement. Feature code uses type roles, not raw sizes and weights.

**L3. Reusable composition.** The app shell and each Golden archetype exist as a reusable layout, component or documented recipe with a canonical example. Encode stable composition, not visual sameness; never force an archetype onto an unrelated workflow.

**L4. Automated drift checks that fail.** In CI, or a pre-commit hook when there is no CI:
- a source check for raw values and default-palette bypasses (`scripts/audit-tokens.mjs --baseline`, stylelint, framework lint), which exits non-zero on new findings;
- an import restriction so feature code uses the project's wrapped primitives rather than raw library components, when such wrappers exist;
- a saved `scripts/style-inventory.mjs` baseline over the Golden routes and specimen.

What each tool catches: source checks catch raw values written in code; the style inventory catches new rendered values and one-off values (a 13px size, a near-duplicate gray), including those reached through valid utilities. Neither knows intent: a legitimate token used in the wrong role is caught only by L2 (roles exposed as variants), review, and the regression anchors.

**L5. Regression anchors.** Golden set, specimen, app shell and identity-bearing primitives under visual regression (Playwright `toHaveScreenshot`, Storybook/Chromatic, platform snapshot tests), run in CI when CI exists; otherwise canonical captures in `canon/` tied to a commit.

**L6. Durable agent instructions.** A short design-rules section from `assets/design-rules.template.md` in the project's agent instructions (`CLAUDE.md`, `AGENTS.md` or equivalent). It applies to all frontend work, not only work done with this skill, and points to `MASTER.md`, the token source, the primitives and the archetypes.

## Specimen

A private route or story set (for example `/__design/specimen`) under the same providers and theme as the app, showing type roles, color roles in every theme, primitives and their states including focus, density levels, archetype recipes, data-viz palette when relevant, and empty, error and loading states.

## Migration mechanisms

Temporary `v2` primitives, theme flags and route scoping are acceptable during propagation if each has a name, an owner and a removal plan recorded in STATE. No permanent parallel design system.

## Drift during propagation

For each batch:
1. `style-inventory.mjs --baseline` on the batch routes. Each new value is a finding: replace it with an existing token or role, or record a system decision in `MASTER.md` and refresh the baseline.
2. `audit-tokens.mjs --baseline` (or the stack's lint).
3. Visual comparison of grouped captures with the canon, focused on composition (layout model, archetype use, hierarchy) and role use, which neither script judges.
4. Inventory and findings updated in STATE.

## Exit

Before propagation, record in STATE: L1-L6 each `done` or `exception`, specimen running, baselines saved, temporary mechanisms documented.
