# Anti-pattern heuristics

Signals of missing decisions, not automatic bans. Judge combinations and product fit. An exception that affects identity needs a fit-fact trace and human or reviewer acceptance. For what to do instead, see `craft.md`.

Last reviewed: 2026-10. Fashionable markers age; refresh this list when the prior fingerprints of recent projects show new recurring choices.

## Absence-of-decision markers

Investigate when these appear as untouched defaults:
- framework or system font with no typographic rationale;
- a component kit's default palette and geometry (shadcn/zinc, MUI blue, Bootstrap, Vuetify, Angular Material...);
- the same radius on nearly every surface;
- one card per logical block;
- the same page header + sidebar + table pattern applied to unrelated workflows;
- imported library colors, radii or shadows surviving unchanged;
- arbitrary local values instead of system roles;
- placeholder content driving the composition.

## Fashionable model-prior markers

Investigate combinations such as:
- dark Linear-like chrome with one acid accent;
- cream background + editorial serif + terracotta without a product reason;
- broadsheet or hairline-rule styling used as an escape from SaaS conventions;
- uppercase or monospace eyebrow labels everywhere;
- grain, glow or gradient text as identity shortcuts;
- automatic bento grids;
- fade-up on every section;
- an icon beside every label;
- KPI-card rows with generic green deltas and sparklines;
- centered SaaS hero + CTA + logo cloud.

These can be legitimate. They become suspicious when the brief does not explain them and they appear in the prior fingerprint. Design skills tuned for boldness (see `tools.md` §frontend-design) tend to produce the editorial items on this list.

## Process anti-patterns

- Using adjectives (modern, premium, clean) as the direction.
- Starting references before understanding the product, or choosing them from memory.
- Writing the brief from code alone without asking the Gate 1 questions.
- Fit traces written after the design and without counterfactuals (rationalization).
- Calling judgment checks "mechanical" or reporting `not verified` checks as passed.
- Validating the look without walking the critical tasks.
- Treating fit as identity: a design that is right for the users but interchangeable with competitors.
- Signatures that are decoration (a gradient, a hero illustration) rather than systemic decisions.
- Candidates that differ only on surface axes.
- Candidates confined to token changes, then judged on composition.
- Generating candidates in one unbounded context when isolation is possible; rendering one before all theses are written.
- Selecting from prose instead of rendered evidence; hybrids not rerendered.
- Letting a specialist skill replace this process; the implementer as sole approver.
- Screenshots never opened.
- Polish before hierarchy.
- Propagation before Golden approval and system lock.
- Treating a generic existing system as authoritative because it exists.

## Implementation anti-patterns

- Foreign tokens or styles imported unchanged; new dependencies for cosmetic benefit.
- Raw colors, radii, shadows or font sizes outside the canonical system.
- Visual overrides on primitives through free class or style props (`className`, `class`, `style`, `::ng-deep`...) instead of variants.
- Feature code importing raw library components instead of the project's wrapped primitives.
- A new abstraction layer added next to an existing design system that already provides the same guarantee.
- Route-specific styling that should be a shared primitive or archetype.
- Permanent parallel component systems.
- Scoped themes that ignore portals and overlays.
- Old themes, flags or prototype routes left unintentionally.
