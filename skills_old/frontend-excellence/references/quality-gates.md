# Quality gates

Single source of checks, statuses and pass criteria. Other files say when to run them and point here.

## Statuses

**Check result**: `pass`, `fail` or `not verified` (with the reason). Absence of a finding is not a pass.

**Evidence status** of a gate or of the final result:
- `verified`: every required check passed.
- `degraded`: every core check passed, but at least one other required check is `not verified` (no browser for a secondary viewport, no competitor captures, review with reduced independence...). Allowed to proceed; the user is told which checks and why.
- `incomplete`: a core check is `not verified`. The work cannot be reported as finished or verified. Proceeding to the next gate requires an explicit user decision, recorded, and the status stays `incomplete` until the check passes.

A failing check is a finding, handled by severity below, never a status downgrade.

**Core checks** for CREATE, REDESIGN and multi-screen IMPLEMENT (EXTEND: C1-C4 on the new screen):
- **C1 Rendered evidence**: the Golden set (or target surface) was rendered at its target viewports and themes and the captures were opened.
- **C2 Task walkthrough**: critical tasks walked through, see below.
- **C3 Accessibility baseline**: automated scan plus keyboard pass, see below.
- **C4 Functional regression**: existing tests pass, or failures are explained as unrelated.
- **C5 Direction fidelity** (CREATE/REDESIGN) or **spec fidelity** (IMPLEMENT).

## Which checks apply

R = required · C = conditional (note) · — = not applicable

| Check | CREATE full | CREATE light | REDESIGN product | REDESIGN scoped | EXTEND | MODIFY | IMPLEMENT |
|---|---|---|---|---|---|---|---|
| Gate 1 (scope, brief, Golden set) | R | R (short) | R | R (target flow) | — | — | C: ambiguity |
| Prior fingerprint (signal) | R | R | R | R | C: new identity-bearing pattern | — | — |
| Stack/current control | R | R | R | R | — | C: before/after | — |
| Competitor captures | R if accessible | C | R if accessible | — | — | — | — |
| Identity checks I1, I2, I4 | R | R | R | R (I4 inherited) | C: new identity-bearing pattern | — | — |
| Gate 2 (human direction choice) | R | C: if ambiguous | R | R | C: first new pattern | — | C: deviations |
| Core checks C1-C5 | R | R | R | R | R (C1-C4) | C: C1, C4 | R (multi-screen) |
| Gate 3 (Golden approval) | R | R (single surface) | R | R (target surface) | — | — | C: multi-screen |
| System-lock guarantees | R | proportional | R | C: new system rule | C: reusable pattern | — | C: multi-screen canon |
| Drift checks per batch | R | — | R | R vs neighbors | R touched routes | C: shared change | C |

## Identity checks

### Structured checks (reviewer evaluates with recorded evidence)

These are design judgments made explicit, not measurements. A failure blocks unless the human accepts it at Gate 2 or 3.

- **I1 Fit trace.** At least three visible decisions are traced to Product Brief facts, each with a plausible counterfactual (`product-brief.md`). Decisions without a counterfactual do not count.
- **I2 Beyond the stack.** The candidate differs from the stack/current control on at least one structural axis (layout model, density, hierarchy carrier, navigation model, content treatment), not only on palette, radius, shadow or decoration.
- **I4 Signature.** One or two signature decisions (`craft.md` §Signature decisions) are visible on the Golden archetype, encodable in the system, and **materially differentiated in role, combination or execution** from what the observed competitors do. Competitor captures reveal interchangeability and copying; they cannot prove uniqueness, and a familiar motif used in a distinctive role or combination qualifies. In REDESIGN / SCOPED and EXTEND, the existing product signatures must be present instead.

### Signal (non-blocking)

- **I3 Prior overlap.** List the axes where the candidate shares the prior-fingerprint choice. Each shared structural axis needs a one-line reason tied to a fit fact or the thesis, shown at Gate 2. An unexplained overlap is a finding for the human, not an automatic fail.

### Judgment checks (the human decides; the reviewer informs)

- **I5 Substitution.** With name and logo removed, could a competitor ship this design with only their branding? The reviewer gives an opinion with evidence; the human decides at Gates 2 and 3. Without competitor captures, `not verified`.
- **I6 Expression.** Does it feel like the expression thesis? The reviewer points to the visible decisions that carry it or fail to.

At Golden, rerun I2 and I3 on the implementation: implementation tends to slide back toward stack defaults and the prior.

## Task walkthrough (C2)

For each of the 2-3 critical tasks in the Product Brief, walk the rendered Golden screens, by browser interaction when possible, and record:
- the path (screens and actions) and the number of steps compared with the current product (REDESIGN) or the expected path;
- whether the information needed for each decision is visible where the decision is made;
- whether the primary action is obvious and reachable by keyboard;
- feedback, error and recovery states along the path.

Fail when a critical task becomes slower or less clear than the baseline without an approved reason, when needed information is missing at a decision point, or when a step has no feedback. For large products, offer the user a short test with real users before mass propagation; it is optional.

## Accessibility baseline (C3)

Target: recorded in STATE (default WCAG 2.2 AA).
- **Automated scan** of the Golden routes and states: `capture.mjs --axe` (needs `@axe-core/playwright` in the project) or the project's existing tooling (Storybook a11y addon, Lighthouse CI, pa11y...). Pass: no `critical` or `serious` violations without a recorded exception.
- **Keyboard pass** along the critical tasks: every control reachable, visible focus, logical order, no traps, overlays closable and returning focus.
- **Forms and names**: inputs labelled, errors announced or associated, icon-only controls named.
- **Contrast** of text and essential UI boundaries, measured, in every supported theme.

Automated tools catch only part of the issues; the keyboard pass is not optional. External checklists such as published interface guidelines complement this; they never replace it.

## Mechanical checks (measured)

Overflow and clipping (`capture.mjs`), console and page errors, automated accessibility results, measured contrast, token bypasses (`audit-tokens.mjs`), value drift (`style-inventory.mjs`), screenshot regression diffs, DOM measurements in IMPLEMENT. These are the only checks to call mechanical.

## Blocking findings

At Golden approval:
- a core check (C1-C5) failing;
- a structured identity check (I1, I2, I4) failing without human acceptance;
- material drift from the approved direction: hierarchy, typographic character, composition, density, interaction language or a signature changed without approval;
- missing or hidden content at a target viewport; unintended horizontal overflow;
- new console or page errors caused by the UI.

Usually blocking before final release:
- broken responsive or reflow behavior; dark-mode breakage when in scope;
- missing loading, error or empty handling for critical workflows;
- unreadable or ambiguous core microcopy;
- major performance regression from fonts, animation or UI libraries;
- browser-specific breakage on a supported browser for a critical surface;
- new drift values or token bypasses after lock without a recorded system decision;
- a system-lock guarantee missing without a recorded exception.

Only the user may downgrade a blocking finding. Record the exact decision.

## Review dimensions

Use these to find issues; `craft.md` describes what good looks like.
- Structure and hierarchy: dominant task and action, grouping, scan order, density relative to task frequency, containers encoding structure.
- Typography and microcopy: roles, scale, data alignment, truncation and long content, user-intent language.
- Spacing and geometry: system spacing, edge alignment, semantic radii and elevation.
- Color and theming: semantic roles, theme matrix, overlays, charts and third-party palettes.
- Components and interaction: all states, motion purpose, reduced motion, touch targets.
- Responsive: target viewports, 320px or 200% zoom reflow, deliberate narrow strategy for dense data.
- Content and edge cases: empty, long, extreme, localized, permission and error states.
- Performance: font weights loaded, heavy dependencies, layout shift.

## Exit of a major gate

- Evidence status stated (`verified`, `degraded` or `incomplete`); `incomplete` proceeds only by recorded user decision.
- Zero blocking findings, unless downgraded by the user and recorded.
- Reviewer coverage and independence level recorded.
- Human decision or delegation recorded; approval status updated.
