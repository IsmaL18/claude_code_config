# Edenred Design System — Artistic Direction (DA)

Detailed art-direction rules for EdenChat apps and the future SDK. This document
turns the principles in `SKILL.md` into concrete do/don't guidance. When a
judgment call arises, this file is the tie-breaker.

## 1. Design ethos

Edenred interfaces are **quiet, operational, trustworthy**. They help people get
work done without visual noise. The measure of a good Edenred screen is not how
striking it is, but how effortless it feels.

- Favor clarity over decoration.
- Let whitespace and hierarchy do the work before color does.
- Every visual choice should earn its place; if it carries no meaning, remove it.

## 2. Color usage

### The neutral-first rule
Greys are the default for text, surfaces, borders, and most UI. Reach for color
only when it communicates state or draws the eye to the single most important
action.

**Do**
- Use `--text-primary` (grey 900) for body text, `--text-secondary` for support.
- Build cards/surfaces from greys and white; keep backgrounds calm.
- Introduce one accent per view, tied to the primary action.

**Don't**
- Don't paint large areas in brand red or the brand gradient.
- Don't use multiple saturated colors competing on one screen.
- Don't use color purely for decoration.

### The two reds
- **Brand red `#F72717`** → identity + the primary action. One per view.
- **Semantic error red `#ca0e00`** → errors and destructive actions only.

**Do**: "Delete account" button → semantic red. Main "Generate" CTA → brand red.
**Don't**: an error toast in brand red; a primary CTA in semantic red; both reds
side by side implying different things without distinction.

### Semantic colors
Each means exactly one thing: green = success, orange = warning, blue =
info/emphasis, semantic red = error. Use the DEFAULT tone for the element, the
BACKGROUND (50) tone for subtle fills behind it, DARK (700) for hover/emphasis.

**Do**: success banner = green 50 background + green 400 text/icon + green 700
accent. **Don't**: a green "delete" or a red "success".

### Brand gradient
`--gradient-brand` (red→pink) is a brand moment — hero CTAs, splash, empty-state
illustration accents. Never a page background, never behind body text.

## 3. Typography

- Headings: brand display face (rounded) once confirmed; `Inter` fallback today.
- Body: `--font-sans`, grey, high contrast. Never pure black on white.
- Scale from `--text-*`; don't invent sizes. Maintain clear hierarchy (one H1
  per view, consistent step-downs).
- Line length comfortable (~60–80 chars); don't stretch text full-width on large
  screens.

## 4. Iconography

- One language: **Wired 24px stroke 1.5**, monochrome, via `<use href="#ic-…">`.
- Icons inherit `currentColor` — tint by setting the parent's color, not by
  editing the SVG.
- Pair icons with labels for primary actions; icon-only is acceptable only for
  universally understood actions (close, search) and must have `aria-label`.

**Do**: `<svg class="eds-icon"><use href="#ic-search"/></svg>` inside a labeled
button. **Don't**: emoji (🔍 ✨ ⚙️) as UI icons; mixing filled and stroke icon
styles; scaling an icon to arbitrary sizes outside the 16/20/24 set.

### Flags (distinct from icons)
Flags live in `assets/flags.html` (206, multicolor, 40×40, prefix `flag-`).
They are the ONE exception to the monochrome rule — they must keep their own
colors and must never be tinted with `currentColor`. Reference them with
explicit width/height, not the `.eds-icon` class. Use them only for
country/language selection and locale contexts, never decoratively and never
as a substitute for a semantic icon.

## 5. Spacing & layout

- Everything snaps to the **4px grid** (`--space-*`). No off-grid margins.
- Group related elements with consistent spacing; separate groups with larger,
  deliberate gaps — spacing communicates structure.
- Use the `--radius-*` scale for corners; be consistent within a component.
- Prefer a clear single-column reading flow; introduce columns only when the
  content is genuinely parallel.

## 6. Components

- **One primary action per view.** Everything else is secondary (outline) or
  tertiary (ghost).
- Buttons carry full states (default/hover/disabled/pressed/loading). Loading =
  inline spinner + disabled input; never leave an action ambiguous.
- Destructive actions use semantic red and, when consequential, a confirm modal
  (custom HTML — no native `confirm`).
- Cards: subtle border or shadow, never both heavy; content breathes inside
  padding from the spacing scale.

## 7. Accessibility (non-negotiable)

- Meet contrast on text and interactive elements in **both** light and dark mode.
- Every icon-only control has an `aria-label`.
- Respect `prefers-reduced-motion`; keep motion subtle and purposeful.
- Don't rely on color alone to convey state — pair with icon or text.

## 8. Do / Don't at a glance

**Do**
- Neutral greys first, one intentional accent.
- Brand red for the one primary action.
- Wired stroke icons via `<use>`.
- 4px grid, defined type scale, both themes tested.

**Don't**
- Brand gradient as a background.
- Emoji as icons.
- Two reds meaning the same thing.
- Multiple competing accents on one screen.
- Color as decoration.

## 9. SDK note

As this becomes the SDK's design foundation, treat every token and rule here as
an API contract: components should consume tokens (`var(--…)`), never hardcode
hex values. Any new pattern added to the SDK must be expressible in these tokens
and must pass the do/don't checks above before inclusion.