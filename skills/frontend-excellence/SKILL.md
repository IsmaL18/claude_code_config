---
name: frontend-excellence
description: "Process owner for substantial visual interface work in any web stack (React, Vue, Svelte, Angular, Astro, web components, server-rendered templates...) and, with reduced tooling, native apps: creating a new interface or visual identity, redesigning a product, app shell or flow, adding screens or patterns to an existing design system, polishing a screen within its existing language, or implementing an approved Figma/mockup/screenshots. Use it whenever a request involves visual design decisions on at least one full screen, flow or shared component, e.g. 'redesign the dashboard', 'make the app look professional/distinctive', 'our UI looks generic', 'build the settings area', 'implement this Figma', even when no design vocabulary is used. When frontend-design or another design skill also applies, this skill owns the process and calls them in bounded roles. Not for non-visual logic, data/state bugs, tests, or one-property tweaks; those follow the project's design rules file when one exists."
---

# Frontend Excellence

This skill owns mode, scope, Product Brief, human gates, source of truth, system lock and exit criteria. Specialist skills and tools contribute only inside the roles defined in `references/tools.md`. It is stack-agnostic: wherever an example names a framework, `references/stacks.md` gives the equivalent for the project's stack.

Three things decide the final quality. The process exists to protect them.

1. **Identity = fit + expression.** *Fit* is the set of decisions derived from product facts (users, tasks, data shape). *Expression* is a deliberate thesis about how this product should feel, carried by one or two systemic signature decisions. Fit alone is shared with every competitor serving the same users; expression alone is decoration. A direction needs both.
2. **The interface must serve the tasks.** A distinctive, consistent interface that slows down a critical task is a failure. Critical tasks are walked through before propagation.
3. **Coherence lives in code.** Approved choices become governed tokens, a constrained component API, reusable compositions, automated drift checks, regression anchors and instructions every future agent reads. Screenshots and review detect drift; only code prevents it.

## 1. Select the mode

Choose by design intent and supplied evidence, not file count. Announce the mode in one line. Reclassify when scope changes, and track the mode per surface in mixed projects.

- **IMPLEMENT**: an authoritative visual spec covers the composition of the target surfaces (approved Figma, mockups, screenshots, spec).
- **CREATE**: no approved visual language exists yet.
- **REDESIGN / PRODUCT**: materially change the product-wide language, shell/navigation, hierarchy model, density or shared component language.
- **REDESIGN / SCOPED**: materially rethink one screen or bounded flow while keeping the wider language.
- **EXTEND**: add a screen, flow or substantial component inside an acceptable existing language.
- **MODIFY** (intensity `local` or `polish`): a localized change, or a hierarchy/spacing/typography/finish pass, without changing the language.

Tie-breakers:
- Brand guidelines or tokens alone are constraints, not an IMPLEMENT spec. Use CREATE or REDESIGN constrained by them unless composition is also specified.
- A partial Figma is IMPLEMENT only for covered surfaces; uncovered surfaces become EXTEND or REDESIGN using the derived canon.
- Existing app without a coherent system + request for a better or distinctive look → REDESIGN, not CREATE.
- One bad screen needing a new composition → REDESIGN / SCOPED, not MODIFY.
- Adding one semantic token or state does not force REDESIGN.
- If EXTEND or MODIFY reveals a generic system and the user wants a professional or distinctive result, say so and recommend REDESIGN before propagating the weakness.

## 2. What to read, and when

Read a reference when you reach its step, not upfront. `quality-gates.md` is the only place where checks, statuses and pass criteria are defined; other files say when to run them.

| Mode | Read |
|---|---|
| CREATE | `create.md` → `product-brief.md` → `direction-making.md` + `craft.md` + `anti-patterns.md` → `visual-qa.md` → `system-lock.md` + `stacks.md` |
| REDESIGN | `redesign.md`, then the same sequence as CREATE |
| EXTEND / MODIFY | the project's design-rules file and `MASTER.md` first, then `extend-modify.md`; `craft.md` when composing a new pattern |
| IMPLEMENT | `implement.md`, `visual-qa.md` |
| First substantial task in a project | `setup.md`: preflight, then one grouped question about missing tools |
| Any mode | `quality-gates.md` at each gate; `tools.md` before using any specialist; `stacks.md` whenever an example does not match the stack |

Scripts (web stacks; Playwright and optional add-ons are loaded from the target project):
- `scripts/preflight.mjs`: read-only check of Node, Playwright, launchable browsers and the accessibility add-on.
- `scripts/capture.mjs`: deterministic route × viewport × theme × browser captures, overflow signals, optional automated accessibility scan (`--axe`).
- `scripts/build-review-page.mjs`: grouped side-by-side review pages for human gates.
- `scripts/audit-tokens.mjs`: source scan for raw values and default-palette bypasses (scripts, styles and common template languages), with a CI baseline.
- `scripts/style-inventory.mjs`: computed-style inventory across rendered routes; detects value drift and one-off values, not semantic misuse.

## 3. CREATE / REDESIGN at a glance

Orientation only; the mode file has the detail.

1. Scope, Golden set candidates, `STATE.md`; preflight and tooling question (`setup.md`) if not done for this project.
2. Prior fingerprint (cheap, written, before the brief).
3. **Product Brief**: fit facts, critical tasks, expression thesis. Ask the Gate 1 questions.
4. **Gate 1**: scope, brief, Golden set.
5. Observed reference board, including competitor captures.
6. Two or three structurally different candidate directions, each free to recompose inside its own sandbox, rendered on the primary Golden archetype including the app shell.
7. **Gate 2**: comparative review; the human chooses.
8. `MASTER.md` v0, then the Golden set in passes: structure → system → polish, with the task walkthrough and accessibility checks.
9. **Gate 3**: Golden approval.
10. **Lock the system** (`system-lock.md`), `MASTER.md` v1, design-rules file.
11. Propagate by complete inventory with drift checks per batch. **Gate 4** only when a batch introduces a new archetype or material system change.
12. Final audit, teardown, final status.

## 4. Human gates and approval status

| Gate | The human sees | The human decides |
|---|---|---|
| 1. Scope + Brief + Golden set | Scope contract, brief with marked assumptions, critical tasks, proposed Golden set | Confirms facts, answers expression questions, approves scope |
| 2. Direction | Competitors, stack control, prior fingerprint, candidates with traces, signatures and flags, reviewer ranking | Chooses, rejects, or asks for a hybrid by axis |
| 3. Golden | Approved direction next to implementation, task walkthrough, QA summary, known non-blocking findings | Approves or requests changes |
| 4. Propagation | Only batches with a new archetype or material system change | Approves the new pattern |

IMPLEMENT asks for approval when fidelity is ambiguous or a deviation is material. Multi-screen EXTEND checkpoints the first screen that introduces a reusable pattern.

Rules:
- Never self-approve a gate, including in headless, CI or background use.
- Distinctiveness and expression are human judgments. Reviewers run the structured checks and rank candidates; they do not certify identity.
- Delegation can name gates or be global. Record it verbatim. Under delegation, still build the review pages and record each choice with its rationale.
- **Approval status** of CREATE and REDESIGN / PRODUCT work: `approved` only if a human decided Gate 2 or Gate 3; otherwise `provisional`, and the final report lists the agent-decided gates.
- **Evidence status** of every gate and of the final result: `verified`, `degraded` or `incomplete`, as defined in `quality-gates.md`. Never report `degraded` or `incomplete` work as verified.

## 5. State and files

For substantial CREATE, REDESIGN, multi-screen IMPLEMENT or large EXTEND:

```text
design-system/frontend-excellence/
├── STATE.md            durable: progress, approvals, statuses, inventory, findings
├── PRODUCT-BRIEF.md    durable: fit facts, critical tasks, expression thesis
├── MASTER.md           durable: design rules; points to code
├── references/         working: observed captures (competitors, domain, other)
├── directions/         working: prior fingerprint, controls, candidate briefs and captures
├── canon/              durable: approved canon captures tied to a commit
├── qa/                 working: captures, inventories, QA reports
└── review/             working: review manifests and generated pages
```

Templates are in `assets/`. Working files support decisions and can be archived or deleted after the final audit; durable files are kept up to date. Also write a short design-rules section into the project's agent instructions (`CLAUDE.md`, `AGENTS.md` or equivalent) at system lock, from `assets/design-rules.template.md`.

Update STATE at each gate transition, after approvals or delegations, after each propagation batch, and before ending a long turn or a likely context compaction. Each fact lives in one durable file; others link to it.

## 6. Core invariants

- Product understanding and an expression thesis precede art direction.
- References must be observed (opened, captured). Products named from memory are hypotheses, not evidence.
- Use realistic content and fixtures whenever available.
- Candidate directions may change anything inside their sandbox and nothing shared.
- Tokens and components live in code. `MASTER.md` documents intent and points to code.
- Prefer the project's existing design-system mechanisms over adding parallel abstractions.
- Component libraries provide behavior, not identity.
- The implementing agent is never the only approver of major design work. A second pass by the same agent is `reduced independence`, never independent review.
- At most three QA/fix loops per screen or batch, and at most two extra direction rounds; then escalate with new questions.
- Preserve behavior unless the approved scope changes it.
- No visual gate passes from source code alone. An image is evidence only once it has been opened and inspected.
- Never install tools, skills or MCP servers without the user's explicit approval (`setup.md`). Ask once; a decline is respected.
- Degrade honestly: missing tools or evidence lower the evidence status; they never turn into a pass.

## 7. Completion

Major work is complete when:
- required gates are decided and recorded, and the approval status (`approved` or `provisional`) is stated;
- the final evidence status is stated, with every degraded or incomplete check listed;
- no blocking finding remains unless the user explicitly downgraded it;
- the system-lock guarantees are met, with exceptions recorded and known to the user;
- the design-rules section exists in the project's agent instructions;
- Golden set, specimen and regression anchors match the approved canon, and drift checks show no unexplained new values;
- every in-scope surface is `migrated`, `out of scope` or `blocked`;
- temporary routes, flags, old themes and migration scaffolding are removed or retained with rationale;
- remaining non-blocking findings are listed.
