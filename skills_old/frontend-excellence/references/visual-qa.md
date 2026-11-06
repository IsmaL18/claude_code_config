# Visual QA protocol

How to gather and review evidence. Checks, statuses and blocking rules live in `quality-gates.md`.

## Evidence sources

1. Interactive browser or MCP when a state must be inspected immediately.
2. `scripts/capture.mjs`: route × viewport × theme captures in one browser engine per run (`--browser`), overflow and clipping signals, optional accessibility scan (`--axe`).
3. `scripts/style-inventory.mjs`: rendered style values across routes (value drift, one-offs).
4. `scripts/build-review-page.mjs`: grouped review pages for human gates.
5. For native apps, the platform tools in `stacks.md`.

A file on disk is not evidence until it has been opened.

## Stabilize before capture

Deterministic data; authenticated state when needed (`--storage-state`); a product-specific ready selector (`--ready`), not `networkidle`; fonts loaded; animations disabled for screenshots; reduced motion when relevant; frozen time when supported (`--freeze-time`); dynamic regions masked when comparing.

## Coverage

- Viewports: desktop 1280 or 1440; narrow 390; 320 CSS px or 200% zoom for reflow when relevant; tablet only when usage justifies it.
- Themes: every supported theme when theming is in scope.
- Browsers: the matrix recorded in STATE (`tools.md`).
- States: loading, empty, populated, long labels, extreme values, error, disabled, hover, focus, active, open overlays, keyboard traversal, via fixtures, mocks, stories or interaction.

## Measure what vision judges badly

DOM measurements or the style inventory, not full-page vision, for alignment, spacing, sizes, rendered colors and cross-screen consistency. Vision is for composition, hierarchy, scan order and character, with 1:1 crops for typography and detail.

## Task walkthrough and accessibility

Run C2 and C3 (`quality-gates.md`) by real interaction in the browser when possible: click and type through each critical task, then repeat with the keyboard only. Record the path, blockers and focus issues with captures.

## Review pages

Use `assets/review-manifest.template.json` or an equivalent in-app route.
- Gate 2: see `direction-making.md` §6.
- Gate 3: approved direction next to the Golden implementation, controls when useful, the task walkthrough summary, the evidence status and the non-blocking findings.

Always include 3-5 focused decision questions and an explicit response format.

## Independent reviewer

Inputs: Product Brief, expression thesis, prior fingerprint, approved direction brief and captures, stack/current control, Golden or batch captures, MASTER, `anti-patterns.md`, `quality-gates.md`, and for REDESIGN the baseline and strengths to preserve. Never the implementer's reasoning.

The reviewer runs the structured and core checks with recorded evidence, lists I3 overlaps, ranks candidates at Gate 2, and gives an opinion on I5-I6 for the human without deciding them.

## Proof of inspection

For each reviewed image, record at least one localized visible observation ("the filter bar wraps to two lines at 390px"). Pixel-level claims need a crop or a DOM measurement.

## Reports

`assets/qa-report.template.md`: the **batch** tier by default during propagation; the **full** tier at Golden and final release.

## Budget

Keep canonical evidence on disk; load targeted captures and crops into context, not hundreds of full pages.

## Iteration

At most three QA/fix loops per screen or batch. If a blocking finding remains, stop and present it. Only the user may downgrade it.
