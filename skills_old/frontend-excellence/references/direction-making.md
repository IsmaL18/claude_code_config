# Direction making

Use for CREATE and REDESIGN (both variants). Checks and statuses are defined in `quality-gates.md`; this file says how to produce directions worth judging.

## 1. Prior fingerprint (before the brief)

Two different defaults threaten identity. The **stack/current control** shows the framework's default look. The **prior fingerprint** shows the model's "distinctive" default: what it produces when merely asked to be original (cream and editorial serif, dark chrome with an acid accent, bento grids...). Candidates should not land there by accident.

1. At scope time, before writing the brief or gathering references, give an isolated sub-agent only the product category, the purpose of the primary Golden screen and a sample of its content. Ask for 3 independent "distinctive, professional" directions in the compact format below, written, not rendered.
2. Axis choices appearing in at least two samples form the fingerprint; add the matching markers from `anti-patterns.md`.
3. Save it in `directions/prior-fingerprint.md` (`assets/prior-fingerprint.template.md`).

Without sub-agents, write the samples yourself before any product-specific work and mark `reduced independence`. The fingerprint is a signal (I3), never a blocker: overlap is acceptable when explained.

Compact format, one line per axis: layout model · density · hierarchy carrier · navigation · typography · palette and neutral temperature · geometry and depth · signature · motion.

## 2. Reference board

Prefer, in order: brand assets; user-provided screenshots, Figma or URLs; **competitor captures** from the brief's competitive frame (real product screens, not marketing pages, when accessible); domain references close to the workflow; optionally a non-software reference that illuminates one axis.

- Open or capture every reference before using it. A product named from memory is a hypothesis.
- Tie each reference to a brief fact or the thesis, and to one axis. Extract observable decisions ("rows about 32px high, figures in a condensed face"), not mood words.
- Write down what competitors share: the category convention, which candidates knowingly keep or break.
- Avoid reference monoculture.

## 3. Candidate theses

Write 2-3 theses **before rendering any**, so they cannot converge. Use `craft.md` §Building divergent theses and `assets/direction-brief.template.md`. Each states its axis positions, a fit trace (three decisions with counterfactuals), its reading of the expression thesis with one or two signatures, the conventions it breaks, and its sacrifices. Candidates differ from each other on at least two structural axes.

Independence: one sub-agent per candidate, given the brief, its thesis, the Golden content, `craft.md`, `anti-patterns.md`, the prior fingerprint ("avoid unless explained") and its subset of references, never the other candidates. Without sub-agents, build sequentially from the pre-written theses and mark `reduced independence`.

## 4. Render in sandboxes

Each candidate owns a private sandbox in the real app (a route such as `/__design/directions/a`, or a story set), rendering the **primary Golden archetype including the app shell** with the real providers, fonts and representative content.

- Inside its sandbox a candidate may change anything: layout model, composition, local presentation of navigation and information, component structure, local forks of primitives, a theme scoped to its root (overlays: see `stacks.md`).
- Outside it, nothing: no edits to shared primitives, tokens or global styles, no new dependency without approval, no change to data or behavior contracts.
- Greenfield without an app: scaffold the intended stack first; that scaffold is the stack. Avoid standalone mockups that cannot survive implementation.

Also render the stack/current control: the same content with current or default conventions. Capture each at the primary viewport and a narrow one when responsive behavior matters (`scripts/capture.mjs`), and open the captures.

## 5. Checks before the human

Run I1, I2 and I4, and list I3 overlaps (`quality-gates.md`). A candidate failing a structured check gets one revision; if it still fails, drop it or show it labeled as failed.

## 6. Gate 2: comparative review

Build the review page (`scripts/build-review-page.mjs` with `assets/review-manifest.template.json`, or an in-app route) grouped as: competitor captures; stack control; prior fingerprint; candidates (primary and narrow) with one-line thesis, signatures, fit trace, conventions broken and I3 overlaps.

An independent reviewer (fresh context, no implementer reasoning) ranks candidates on fit, strength of expression, distinctiveness and how well the signatures systemize, and names the most interchangeable one. The agent's recommendation is shown separately.

Ask 3-5 focused questions and give a response format: approve one, reject all, or hybrid by axis.
- A hybrid becomes a new candidate: new thesis, rerender, rerun the checks.
- If all are rejected, run at most two more rounds, then ask for new constraints or references.
- Record the exact decision in STATE and in the chosen direction brief.
