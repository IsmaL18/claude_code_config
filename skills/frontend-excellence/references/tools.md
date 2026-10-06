# Tool roles and precedence

`frontend-excellence` owns mode, scope, brief, gates, source of truth, lock and exit criteria. Specialist instructions never override them. If a specialist skill triggered first, return control to this process.

Availability and installation of every tool below are handled once per project by `setup.md`; never install one without the user's approval.

## frontend-design

A craft specialist with a known bias toward bold editorial aesthetics (display serifs, warm or cream neutrals, grain and texture, asymmetric heroes, dramatic type contrast). Several overlap the markers in `anti-patterns.md`, so its output is accepted only when traced to the brief or the thesis.

Invoke it only:
1. inside a candidate's sub-agent, after that candidate's thesis is written, to refine typography and composition within it;
2. for the polish pass of the Golden set;
3. to critique a Golden surface against the brief and thesis.

Contract:
- Input: Product Brief, expression thesis, the candidate thesis or approved direction, prior fingerprint, anti-patterns, and the boundary (sandbox or primitives in scope).
- Output: concrete changes inside that boundary, plus the decisions made and the thesis axis each serves.
- Not allowed: proposing a new direction, changing the families or palette of an approved direction without flagging a deviation, overwriting tokens, bypassing gates.

## Sub-agents

Use isolated sub-agents for the prior fingerprint, each candidate and independent reviews. Give reviewers evidence and criteria, not the implementer's reasoning.

Without sub-agents: write the fingerprint before any product-specific work; write all theses before rendering any; review later from evidence files only. Mark each such check `reduced independence`; it never counts as independent review.

## Behavior libraries

Use the project's existing primitives and headless libraries first (`stacks.md` §Behavior libraries). Prefer existing behavior over new dependencies.

## 21st.dev

A React/Tailwind-oriented component source. In React projects, use it only when the stack lacks a behavior-heavy pattern (command palette, complex combobox, data-table interactions, advanced menus and forms); in other stacks, use it at most as a behavior reference and port the logic.

Never for identity-bearing regions: app shell, Golden header or hero, brand typography and color language, product-specific composition, signatures.

After import: rebuild on project tokens and primitives; remove foreign colors, radii and shadows; no new dependency without justification and approval; run `audit-tokens.mjs` and the style inventory on affected routes.

## Playwright and browser tooling

- Interactive browser or MCP when evidence must enter the model's context immediately.
- `scripts/capture.mjs` and `scripts/style-inventory.mjs` for deterministic batches; both load Playwright from the project and accept `--browser chromium|firefox|webkit`.
- Browser matrix: derived from the project's supported browsers (browserslist, docs, analytics) and recorded in STATE. Capture everything in the primary engine; capture the critical surfaces once in each other supported engine at the gates.
- A PNG on disk has not been reviewed until it is opened.

Without browser tooling: IMPLEMENT asks for exported evidence; CREATE/REDESIGN produces routes the user can open. The affected core checks are `not verified`, so the status is `incomplete` until evidence returns. Never pass a visual check from source code alone.

Native apps: see `stacks.md` §Evidence outside the browser.

## Figma and other design tools

For IMPLEMENT, extract variables, styles and variants through the tool's developer mode or MCP connector (`implement.md`). In CREATE and REDESIGN, a design file is a reference, not a direction source, unless the user says it is approved.

## Accessibility

The baseline in `quality-gates.md` C3 is the mechanism: automated scan (`capture.mjs --axe` with `@axe-core/playwright` installed in the project, or the project's tooling), keyboard pass, forms and names, measured contrast. Published interface guidelines (for example Vercel's Web Interface Guidelines, as a skill or document) are a complementary checklist on the Golden set and near release, never the main check.

## Optional category checklists

UI/UX Pro Max and similar tools: only for a narrow UX or category checklist, never as art direction, never allowed to write into `design-system/frontend-excellence/`. Product evidence and the brief win any conflict.
