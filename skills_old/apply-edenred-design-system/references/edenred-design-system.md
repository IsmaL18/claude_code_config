# Edenred Design System — Full Reference

Complete design-system reference for the `apply-edenred-design-system` skill:
color tokens, the two reds, typography, iconography, flags, component classes,
and EdenChat platform constraints. Loaded from `SKILL.md` when implementing
visual work. **This is a reference document, not a standalone skill** — it has
no front-matter `name:` on purpose, to avoid colliding with the skill identity.

## When to use this reference

- Building any single-file HTML app for EdenChat (chat.edenred.com).
- Styling components, choosing colors, or adding icons.
- Reviewing an app for brand/DA compliance.
- Establishing tokens and patterns for the future SDK.

## Core principles

The Edenred design language is **quiet and operational**. Interfaces should feel
calm, structured, and trustworthy — not loud. Concretely:

- **Neutral by default.** Greys carry text and surfaces. Color is used with
  intent, never decoratively.
- **Brand red is for identity and primary action only.** `#F72717` marks the
  single most important action on a view — never as a background wash or accent
  spam.
- **Semantic colors mean one thing each.** Green = success, orange = warning,
  red (semantic scale) = error/destructive, blue = info/emphasis. Do not mix
  brand red with semantic error red.
- **Rhythm on a 4px grid.** Spacing, sizing, and alignment follow the 4px scale.
- **One consistent icon language.** Wired 24px stroke icons, never emoji in
  production UI.

## Two distinct reds (critical)

Edenred uses two reds that must never be confused:

- **Brand red — `--brand-red: #F72717`** — Edenred identity, primary CTAs,
  brand gradient. This is the corporate red.
- **Semantic error red — `--red-500: #ca0e00`** (Reds scale 50→900) — error
  messages and destructive actions only.

Using the wrong red breaks either the brand or the error semantics. When in
doubt: is it *the main action / brand*? → brand red. Is it *an error / delete*?
→ semantic red.

## Color system

Full token definitions live in `assets/edenred-theme.css`. Summary of anchors:

| Family  | Role                    | DEFAULT   | Scale        |
|---------|-------------------------|-----------|--------------|
| Brand   | Identity, primary CTA   | `#F72717` | brand red    |
| Brand   | Secondary brand         | `#FF007D` | brand pink   |
| Greys   | Text, surfaces (default)| `#64748B` | 50→900       |
| Blues   | Info / emphasis         | `#0060df` | 50→900       |
| Greens  | Success                 | `#0dba69` | 50→900       |
| Oranges | Warning                 | `#ed571c` | 50→900       |
| Reds    | Error / destructive     | `#ca0e00` | 50→900       |

Each semantic scale has three named anchors: **BACKGROUND** (50, subtle fills),
**DEFAULT** (the main usable tone), **DARK** (700, emphasis/hover). Greys are the
first choice for any new element; reach for color only when it carries meaning.

**Brand gradient** (`--gradient-brand`, red→pink) is reserved for hero CTAs and
brand moments, not general surfaces.

Dark mode is supported via `[data-theme="dark"]` and `prefers-color-scheme`.
Both blocks must hold the same values (the media query only applies when no
explicit theme is set). Always test both.

### Token layers

| Layer | Tokens | Who uses it |
|-------|--------|-------------|
| 1. Primitives | `--brand-red`, `--brand-pink`, `--grey-*`, `--blue-*`, `--green-*`, `--orange-*`, `--red-*` | Semantic layer; brand moments only |
| 2. Semantic | `--color-primary/success/warning/error/info`, `--bg-*`, `--text-*`, `--border-default`, `--focus-*` | All components |
| 3. Legacy aliases | `--brand-primary`, `--brand-primary-dark`, `--brand-secondary`, `--brand-accent`, `--gradient-button` | Older apps only; never in new code |

Rules:
- **One token block per app.** Paste `edenred-theme.css` once. Do not add a
  second `:root` later in the stylesheet that re-declares the same tokens with
  other values: whichever comes last silently wins and the two palettes mix
  (typically the dark-mode media query keeps the old values).
- **App-specific tokens alias DS tokens** (`--app-accent: var(--blue-500)`),
  they do not introduce new hex values.
- **No raw hex in components or inline `style=""`.** If a value is missing,
  add it to the token block first.

### Migrating a v1 app (pre-v2 palette)

Apps scaffolded before v2 hard-code the old palette. Replace values, or keep the
v1 names and let the legacy aliases resolve them:

| v1 value | v1 token | v2 replacement |
|----------|----------|----------------|
| `#ff0000` | `--brand-primary` | `--brand-red` `#F72717` |
| `#cc0000` | `--brand-primary-dark` | `--brand-red-700` (hover) |
| `#ff5978` | `--brand-secondary` | `--brand-pink` `#FF007D` |
| `#00a184` | `--brand-accent` | `--blue-500` for info/emphasis, `--green-400` for success |
| `#10b981` | `--color-success` | `--green-400` `#0dba69` |
| `#ef4444` | `--color-error` | `--red-500` `#ca0e00` |
| `#f59e0b` | `--color-warning` | `--orange-400` `#ed571c` |
| `#3b82f6` | `--color-info` | `--blue-500` `#0060df` |
| `linear-gradient(#ff0000, #cc0000)` | `--gradient-brand` | `--gradient-brand` (red→pink) |

## Typography

Load tokens from `edenred-theme.css` (`--font-sans`, `--text-*`). The Edenred
Foundation brand uses a rounded display typeface for headings — confirm the exact
brand font name with the design team before final SDK release; `Inter` is the
current fallback. Body text is always high-contrast grey (`--text-primary`),
never pure black.

## Iconography

Two separate sprites, used differently:

**Icons — `assets/icons.html`** (1074 symbols)
- Wired 24px stroke 1.5, monochrome, recolorable via `currentColor`.
- Paste the sprite once near the top of `<body>`, then reference:
  `<svg class="eds-icon" aria-hidden="true"><use href="#ic-<name>"/></svg>`
- Recoloring: the icon inherits the parent's text color — set `color` on the
  parent (or a utility class) to tint. Sizes: `.eds-icon` 20px, `.eds-icon-sm`
  16px, `.eds-icon-lg` 24px.
- IDs are prefixed `ic-` (e.g. `#ic-settings`, `#ic-search`, `#ic-wallet`).

**Flags — `assets/flags.html`** (206 country flags)
- Multicolor, 40×40 viewBox, IDs prefixed `flag-` (e.g. `#flag-pays-france`).
- **Never** apply `currentColor` or a `color` tint — flags keep their own
  colors. Reference: `<svg width="24" height="24" viewBox="0 0 40 40"><use
  href="#flag-pays-france"/></svg>` (set explicit width/height; do not use the
  monochrome `.eds-icon` class, which forces sizing meant for stroke icons).
- Use only for country/language selectors and locale UI — not as decoration.

**Rule:** never use emoji as UI icons in production apps. Replace any emoji with
the corresponding Wired symbol from `icons.html`.

## Components

Base patterns live in `assets/ui-components.html`. Key rules:

- **Buttons** follow the full state matrix (default, hover, disabled, pressed,
  loading) across variants: dark solid, outline, ghost, brand-red solid,
  brand-red outline. Loading state shows an inline spinner and disables input.
  Primary action per view = brand red solid; destructive = semantic red.
- **Surfaces:** cards on `--bg-card`, page on `--bg-page`, subtle fills on
  `--bg-subtle`. Borders `--border-default`, radius from the `--radius-*` scale.
- **Focus:** buttons, links, tabs and other controls show
  `outline: var(--focus-outline); outline-offset: var(--focus-offset)` on
  `:focus-visible`. Fields use `border-color: var(--brand-red)` +
  `box-shadow: var(--focus-ring)`. Never remove an outline without a replacement.
- **Badges / status:** semantic BACKGROUND (50) fill + DEFAULT text, and always a
  text label: color alone never carries the state.
- **No native `alert`/`confirm`/`prompt`** (EdenChat sandbox) — use custom HTML
  modals styled with these tokens.

## Layout & templates

Full-page templates live in `assets/templates/` — clone these as starting points
rather than assembling from scratch. They encode the correct header/nav/main
hierarchy, spacing rhythm, and responsive behavior. (Templates are being built
out; see `references/art-direction.md` for the composition rules they follow.)

## EdenChat platform constraints (always respect)

Apps are **single-file HTML + Vanilla JS + Edenred Design System CSS**, running
in a sandboxed `srcdoc` iframe. Non-negotiable:

- No `alert`/`confirm`/`prompt` → custom HTML modals.
- External links via `openLink()` using `window.top.open()`.
- Exports via blob download; previews via `iframe.srcdoc` (not blob URL).
- File inputs as `opacity:0` overlays.
- **Always** escape `</script>`, `</style>`, `</head>`, `</html>`, `</body>` as
  `\x3c/…` inside JS strings, to avoid breaking the srcdoc parser.
- Follow the v7 guide conventions (EdenChatClient, i18n FR/EN, accessibility
  panel, §21 quality checklist).

## Guardrails

- Brand red (`#F72717`) ≠ error red (`#ca0e00`). Keep them separate.
- Greys first; color only when it means something.
- Wired 24px stroke icons via `<use>`; never emoji in production.
- One primary action per view.
- Respect the 4px spacing grid.
- Test light and dark mode.
- Confirm the brand display font before SDK release.

## Resources

- `assets/edenred-theme.css` — full color/spacing/typo/shadow tokens + dark mode.
- `assets/icons.html` — Wired 24px monochrome icon sprite (`currentColor`).
- `assets/flags.html` — multicolor country flags (separate; no recoloring).
- `assets/ui-components.html` — base component patterns.
- `assets/templates/` — full-page layout templates to clone.
- `references/art-direction.md` — DA principles, do/don't, composition rules.
