# Craft doctrine

Read when writing candidate theses, implementing the Golden set, and composing any new reusable pattern. This file says how to build quality; `anti-patterns.md` only says what to distrust. Values below are starting points to reason from, not a house style.

Two kinds of guidance are mixed below. Unmarked items are **universal principles**. Items marked **(work tool)** are heuristics for task-heavy, frequently used software (back-office, SaaS, dashboards, professional tools); apply them only when the brief says the product is used that way, and see §When the product is not a work tool otherwise. Applied everywhere, they would produce their own kind of sameness.

Contents: Typography · Color · Space and density · Hierarchy and composition · Data display · Geometry and depth · Motion · Icons · Voice · When the product is not a work tool · Signature decisions · Building divergent theses · Adjectives → constraints

## Typography

- **Roles before sizes.** Define roles (display, title, section, body, label, data, code) and map each to one size, weight, line-height and tracking. Feature code uses roles, never raw sizes.
- **Few steps.** Five to seven sizes cover most interfaces. Dense work tools want a tight ratio (about 1.125-1.2) and a 13-14px body; reading-heavy or expressive products take 1.25 and above with a 16px+ body.
- **Two or three weights (work tool).** Hierarchy comes from size, weight, color and space combined; do not lean on weight alone.
- **Line-height falls as size rises.** About 1.5 for body, 1.2-1.3 for titles, close to 1.1 for display. Tighten tracking slightly on large sizes; add a little on small uppercase labels, and use those sparingly.
- **Data needs tabular figures** (`font-variant-numeric: tabular-nums`) and right alignment for comparable numbers. Choose a family whose figures and small sizes hold up.
- **Choose families for measurable reasons**: x-height and legibility at the body size, figure style, width (a narrower face buys columns in dense tables), language coverage, available weights, loading cost. Then for character. One deliberate typographic choice is often the cheapest durable signature.
- **Pair only when the roles differ** (for example display versus body, or text versus data). Two families is the usual ceiling.
- Prose measure of 60-75 characters. Load only the weights in use.

## Color

- **Build ramps in a perceptual space** (OKLCH) so equal steps look equal across hues.
- **Neutrals carry most of the interface.** Give them a deliberate temperature tied to the thesis (slightly warm, cool, or tinted toward the brand hue) instead of an untouched default gray.
- **Semantic roles, not hues, in components**: surface levels, text levels (primary, secondary, muted, disabled), border levels, accent, focus, and status (success, warning, danger, info).
- **Accent is scarce (work tool).** Reserve it for primary action, selection or a single meaning. Keep status colors distinct from the accent.
- **Dark mode is its own ramp**, not an inversion: lower contrast between surface levels, desaturated accents, elevation expressed by lighter surfaces.
- **Data-viz palette**: categorical (distinguishable, colorblind-safe), sequential and diverging ramps, defined as tokens.
- Contrast: at least 4.5:1 for body text, 3:1 for large text and essential UI boundaries.

## Space and density

- One base unit (4px) and a limited scale. Proximity encodes grouping: space inside a group is smaller than space between groups.
- **Density is a system decision.** Define it per archetype (row height, control height, padding) rather than per screen. **(work tool)** At most two levels, such as compact and regular.
- Prefer whitespace, alignment, dividers or a surface shift to separate content before adding a card. A container should encode structure, not decoration.
- Align to shared edges. Few column widths and container widths, chosen deliberately.

## Hierarchy and composition

- **One dominant element per screen**, matching the dominant task. Check the scan order (squint or blur test): what is seen first, second, third.
- **Choose the layout model from the core object and task**, not from the template at hand: index plus detail (master-detail or split view), inbox/triage, ledger, board, timeline, canvas, document, wizard, comparison grid. The layout model is the strongest structural lever and the first thing generic interfaces get wrong.
- Primary action placed where the task ends, not automatically top-right.
- Progressive disclosure: secondary information on demand, not removed.
- Empty, loading and error states reuse the populated layout's skeleton.

## Data display

- Numbers right-aligned with tabular figures, units consistent, precision deliberate.
- Text left-aligned; truncation with full value available.
- Sticky headers and first column when tables scroll. Column priority defined for narrow viewports (hide, stack or switch to cards on purpose).
- Status shown inline next to the object, by text plus color or shape, never color alone.
- Comparison is a first-class mode when the brief says users compare.

## Geometry and depth

- Radius by role and size, not one value everywhere. Nested corners: inner radius ≈ outer radius minus the padding between them.
- Choose borders or shadows as the primary separator and use the other rarely.
- **(work tool)** Two or three elevation levels, each with a meaning (flat, raised, overlay).

## Motion

- Motion explains change: where something came from, what changed, what is loading. **(work tool)** 120-250ms for most UI, eased out on enter.
- Respect `prefers-reduced-motion`. Motion is rarely a good signature for work tools; use it as one only when the thesis demands it.

## Icons

- One family, one stroke weight, sizes tied to the type scale.
- An icon must add recognition or save space. Not one beside every label.

## Voice

- Microcopy carries identity cheaply: verbs from the user's work, the product's nouns, a consistent tone in empty states and errors.
- Labels say what happens ("Approve 3 invoices"), not what the control is ("Submit").

## When the product is not a work tool

Consumer, editorial, marketing, brand, entertainment or occasional-use products reward different choices. Keep the universal principles, then consider:
- an expressive type scale (ratios of 1.333 and above, display sizes that carry the brand) and more than one voice in type;
- color as a primary carrier of brand and mood, used generously, with status colors still distinct;
- imagery, illustration or texture as content when the brief supports it, not as filler;
- motion as part of the identity (transitions, choreography, scroll) with reduced-motion alternatives;
- more surprise in composition, as long as the critical tasks stay obvious.

Occasional-use products (onboarding, checkout, forms used once a year) need guidance and reassurance more than density.

## Signature decisions

A signature is a decision a user would notice and associate with this product, which the system can repeat. Good signatures:
- are **systemic**: encodable as a token, primitive, archetype or rule, and repeated across screens;
- **serve the thesis** and, ideally, a fit fact;
- are **absent from the competitor captures** and the prior fingerprint;
- **survive density and dark mode**.

Families of signatures:
- a typographic voice (a distinctive face used in one role, a data face, an unusual but consistent scale relationship);
- a color behavior (color appears only for state; one hue owns one meaning; a non-default neutral temperature);
- a structural motif (a recurring way of framing the core object, a timeline spine, a ledger rule);
- a navigation model (object-centric navigation, command-first, a persistent context rail);
- a data treatment (inline comparisons, a distinctive status grammar, density with rhythm);
- a voice (the way the product speaks in actions and states).

Not signatures: one-off illustrations, gradients, glows, grain, logo placement, a hero section, decorative motion.

## Building divergent theses

Each candidate takes a position on every axis below. Candidates must differ from one another on at least two **structural** axes, not only on surface axes.

| Structural axes | Surface axes |
|---|---|
| layout model | palette and neutral temperature |
| density | type families |
| hierarchy carrier (type-led, structure-led, color-led) | radius and depth |
| navigation model | motion |
| content treatment (table, list, cards, document) | iconography |

Write each thesis as positions plus a reason for each, for example: "split view (operators triage then act), compact density (60+ rows), structure-led hierarchy, persistent object rail, warm neutrals with color only for state, one condensed data face".

## Adjectives → constraints

Never use an adjective as a direction. Translate it, then tie it to a brief fact.

| Adjective | Possible observable constraints |
|---|---|
| premium | fewer, larger decisions; restrained palette; generous but exact spacing; refined type with careful tracking; no decorative effects |
| calm | low surface contrast; accent rare; stable layout without motion on load; muted status until action is needed |
| fast / efficient | compact density; keyboard paths visible; primary action near the end of the task; few clicks to the core object |
| trustworthy | explicit states and confirmations; consistent numbers formatting; visible audit details; no ambiguity in irreversible actions |
| playful | a confident accent used consistently; looser radius in one role; voice with personality; motion with purpose |
| professional | consistency over novelty; strict alignment; restrained color; precise microcopy |

The same adjective can lead to opposite constraints in different products. The brief decides which.
