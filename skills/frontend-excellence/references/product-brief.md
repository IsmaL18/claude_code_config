# Product Brief

Use for CREATE and REDESIGN, after the prior fingerprint and before references or directions. Template: `assets/product-brief.template.md`. Keep it to about one page.

The brief has two layers because they do different jobs:
- **Fit facts** make the interface right for its users. Competitors serving the same users usually share most of them, so fit alone does not create identity.
- **The expression thesis** makes it recognizably this product. It cannot be derived from code; it comes from the people who own the product.

## Layer 1: Fit facts (5-8)

Capture what is known about:
- **Users and context**: role, expertise, environment, devices, session length and frequency.
- **Dominant task**: what users do most and how often.
- **Core objects**: the nouns of the product (cases, orders, documents, incidents...).
- **Data shape**: sparse or dense, tabular or narrative, comparison-heavy or single-object, live or static.
- **Critical moments**: irreversible actions, approvals, errors, high-attention or emotionally important moments.
- **Constraints**: brand assets, accessibility target, localization, compliance, fixed elements.
- **Existing habits** (REDESIGN): muscle memory and what current users would miss.

### Critical tasks (2-3)

The tasks that must never become slower or less clear: usually the dominant task, the most consequential one (irreversible, financial, safety) and one recovery path. For each, note the expected path, the information needed at each decision, the primary action and the possible errors. They drive the task walkthrough (`quality-gates.md` C2) and help choose the Golden set.

Evidence order: user statements → product copy, data, code, routes → docs and brand assets → assumptions, marked as such.

### Implications must be falsifiable

For each fact, write the implication and its counterfactual:

| Fact | Implication | Counterfactual |
|---|---|---|
| Operators compare 40-80 rows many times a day | Stable column rhythm and scan speed over decorative separation | If they opened one record at a time, a detail-first layout would win |

If no plausible counterfactual exists, the "implication" is a default with a justification attached, not a product-derived decision. Do not count it in the fit trace.

Never jump from category to style ("fintech → blue", "AI → purple gradient").

## Layer 2: Expression thesis

- **Competitive frame**: the 2-4 alternatives users actually compare this product with. Capture them (screenshots of real screens, not marketing pages, when accessible) into `references/`. Write down what they all share: that is the **category convention**.
- **Brand ambition**: the attitude in three words, plus one thing it must never feel like. Translate the adjectives into constraints with `craft.md` §Adjectives.
- **Stakeholder taste**: interfaces or objects from any domain they admire or dislike, with the reason.
- **Visible differentiator**: where the product's real difference could become visible: a data treatment, a workflow object, a voice, a moment.
- **Thesis**: two or three sentences: how it should feel, which category conventions it departs from and why, what it refuses.
- **Signature candidates**: two to four hypotheses for signature decisions (see `craft.md` §Signature decisions). Directions may adopt, combine or replace them.

## Gate 1 questions

Ask only what cannot be derived from the product, in one message:

1. What makes this product different from its alternatives, from the user's point of view rather than marketing's?
2. Which two to four products or tools do your users compare it with? Links or screenshots if possible.
3. How should it feel, in three words? What must it never feel like?
4. Name interfaces or objects, from any domain, that you admire or dislike, and say why.
5. What is fixed: logo, colors, typefaces, components, accessibility or market constraints?
6. Only if not evident from the product: which two or three tasks must never get slower or harder?

If the user cannot answer, propose two or three concrete options for the unanswered items and mark the chosen one as an assumption. Assumptions on the differentiator or the brand ambition block direction generation until confirmed or explicitly delegated.

## Brief quality check

Before Gate 1, the brief is ready only if:
- at least three fit facts come from evidence rather than assumption;
- critical tasks are listed with their expected path;
- each counted implication has a counterfactual;
- the category convention is written down, with captures or marked `not verified`;
- the thesis states at least one convention it departs from;
- open assumptions are listed.
