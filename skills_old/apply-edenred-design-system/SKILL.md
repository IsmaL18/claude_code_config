---
name: apply-edenred-design-system
description: Apply the Edenred Foundation design system to EdenChat apps. Use when building or styling any EdenChat single-file HTML app, widget, or UI — design tokens, colors, dark/light theme, typography, icons, flags, forms, panels, cards, badges, buttons, loaders, toasts, chat components, or full layouts. Ensures Edenred brand and DA compliance.
---

# Apply Edenred Design System

Design foundation for EdenChat (Open WebUI) apps and the future EdenChat SDK.
Keep the UI **quiet, operational, and Edenred-branded**: brand red for the one
primary action, neutral greys for surfaces, clear hierarchy, both themes tested.

For apps with multiple views or interacting surfaces, use
`../apply-edenchat-app-layout` to decide hierarchy, navigation, and responsive
behavior before styling. This skill owns the visual language and components;
it does not choose the app typology or impose a page structure. Simple
single-view apps can proceed directly from their user flow.

## Core workflow

1. Inspect the app; identify the smallest CSS/HTML changes needed.
2. Load `references/edenred-design-system.md` for the full DA reference (tokens,
   colors, icons, flags, components, platform constraints).
3. Load `references/art-direction.md` for do/don't rules when making judgment
   calls (color usage, hierarchy, composition).
4. Copy `assets/edenred-theme.css` tokens into the app's single `<style>` block.
5. Paste `assets/icons.html` (and `assets/flags.html` if needed) once near the
   top of `<body>`; reference symbols via `<use>`.
6. Reuse `assets/ui-components.html` snippets and `assets/theme-toggle.js`;
   rewrite handlers/text for the target app. Start from `assets/templates/`
   when building a full page.

## Guardrails

- Brand red (`#F72717`) = identity + one primary action. Error/destructive =
  semantic red (`#ca0e00`). Never confuse the two.
- Greys first; color only when it carries meaning.
- Icons: Wired stroke via `<use href="#ic-…">`, never emoji. Flags keep their
  own colors — never tint them.
- One primary action per view; respect the 4px grid; test light + dark.
- One token block per app: never add a second `:root` that re-declares tokens
  with other values. App-specific tokens alias DS tokens; no raw hex in
  components or inline styles. Migrating a v1 app (`#ff0000`, `#ff5978`): see
  the mapping table in `references/edenred-design-system.md`.
- Every interactive control has a visible `:focus-visible` style
  (`--focus-outline`).
- No native `alert`/`confirm`/`prompt` (sandbox) — use custom HTML modals.
- Keep components accessible: visible focus, labels, semantic controls, contrast.
- Keep the app one file; don't split theme/toggle/toast into separate skills.

## Resources

- `references/edenred-design-system.md` — full DA reference: tokens, color
  system, typography, iconography, flags, components, platform constraints.
- `references/art-direction.md` — DA principles and do/don't guidance.
- `assets/edenred-theme.css` — color/spacing/typo/shadow tokens + dark mode.
- `assets/icons.html` — 1074 Wired 24px monochrome icons (`ic-*`, currentColor).
- `assets/flags.html` — 206 multicolor country flags (`flag-*`, no recoloring).
- `assets/ui-components.html` — component patterns (buttons, cards, badges,
  inputs, loaders, chat bubbles, chips, chat input, progress, typing).
- `assets/theme-toggle.js` — dark/light toggle (SVG icon swap, persisted).
- `assets/templates/` — full-page layouts to clone.

## Done criteria

- Styling consistent across states, panels, buttons, forms, result areas.
- Icons via `<use>`, no emoji; flags keep colors.
- Works on mobile + desktop, light + dark, one file, in the sandbox.