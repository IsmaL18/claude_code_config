<!-- Paste into the project's agent instructions (CLAUDE.md, AGENTS.md or equivalent) at system lock. Keep it under ~40 lines. -->
## Design system rules (all frontend work)

Source of truth: `design-system/frontend-excellence/MASTER.md` and the code it points to. Read it before any visual change.

- Tokens: `<path>`. Use semantic roles only (`surface-*`, `text-*`, `border-*`, `accent`, `status-*`). No raw colors, sizes or shadows, no default palette, no one-off values in feature code.
- Typography: use the type roles in `<component, classes or styles>`. No raw size or weight values.
- Primitives: use `<path>`, never the underlying library directly. Visual changes go through variants; free class/style overrides only for layout and placement.
- Layout: start new pages from the shell and archetypes in `<path>` (`<ListPage, DetailPage, ...>`).
- Signatures to preserve: <1-2 lines>.
- Avoid: <product-specific rejected patterns>.
- A new value or pattern is a system decision: add it to the tokens or primitives and to MASTER, never locally.
- Before finishing visual work: run `<drift check command>`; for multi-route changes, `<style inventory command>`; open captures of what changed; walk the affected critical task.
- Substantial visual work (new screen type, redesign, shell change): use the `frontend-excellence` skill.
