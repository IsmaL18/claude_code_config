# Stack equivalents

Read when an example elsewhere does not match the project's stack, at system lock, and when planning REDESIGN isolation. Rule: use the mechanism the project already has; add a new one only when nothing equivalent exists.

## Governed token source

| Stack | Mechanism |
|---|---|
| Any web stack | CSS custom properties in one tokens file: primitive ramps feeding semantic roles |
| Tailwind v4 | `@theme` with namespace resets (e.g. `--color-*: initial;`), then only the system's tokens |
| Tailwind v3 | `theme.colors` and other scales defined directly, not under `extend` |
| Sass | token maps and accessor functions; raw values banned by stylelint |
| CSS-in-JS (styled-components, Emotion, vanilla-extract, Panda...) | one typed theme or theme contract |
| Component kits (MUI, Chakra, Mantine, Vuetify, PrimeVue/PrimeNG, Angular Material, Bootstrap...) | the kit's theme object or variables *are* the token source; restrict it by overriding the theme, not by adding a parallel layer |
| Multi-platform | a token pipeline (Style Dictionary, Tokens Studio) generating each platform's format |
| SwiftUI / Jetpack Compose / Flutter | asset-catalog colors + a custom theme type / a custom theme via `CompositionLocal` / `ThemeData` + `ThemeExtension` |

## Constrained component API

Visual intent (variant, size, density, emphasis) is an enumerated, typed input; free style overrides are limited to layout and placement.

| Stack | Mechanism |
|---|---|
| React / Solid / Preact | typed props, `cva` or tailwind-variants; `className` for layout only |
| Vue | typed props or validators; control `class`/attribute passthrough (`inheritAttrs`) |
| Svelte | typed props; `class` prop for layout only |
| Angular | inputs typed as string-literal unions; no `::ng-deep` overrides of primitives |
| Web components | attributes or properties for variants; expose `::part` sparingly |
| Server templates (Rails ViewComponent/Phlex, Django/Jinja macros or components, Blade components, Twig components...) | components with named variants instead of free-form class strings |
| Native | views, composables or widgets with enum styles; no ad-hoc modifiers on primitives |

## Reusable composition

- Component frameworks: layout primitives (stack, inline, grid, page) and one component per archetype.
- App shell: the framework's layout mechanism (Next.js or Remix layouts, Nuxt layouts, SvelteKit `+layout`, Angular shell component, Astro layouts, server layout templates).
- Server-rendered: layout templates plus one partial or component per archetype.
- Native: container views, scaffold composables, shared widgets.
- When a full component is overkill, a documented recipe in `MASTER.md` with a canonical example route is acceptable.

## Static checks that fail

| Concern | Mechanism |
|---|---|
| Imports bypassing wrapped primitives | ESLint `no-restricted-imports` (equivalents in angular-eslint, eslint-plugin-vue, eslint-plugin-svelte) |
| Raw values in styles | stylelint (`color-no-hex`, `declaration-property-value-disallowed-list`...) |
| Raw values and default palette in markup | `scripts/audit-tokens.mjs --baseline` (scripts, styles and common templates); framework-specific lint where available |
| Templates | djLint (Django, Jinja, Nunjucks, Handlebars), erb_lint (ERB), or audit-tokens |
| Native | SwiftLint custom rules, detekt or Android Lint custom rules, Dart `custom_lint` |

## Visual regression anchors

- Any web stack: Playwright `toHaveScreenshot`; Storybook + Chromatic (React, Vue, Svelte, Angular, web components, HTML); Percy; BackstopJS.
- Server components with previews: Lookbook (ViewComponent) or equivalent preview routes, captured by Playwright.
- Native: swift-snapshot-testing (iOS), Paparazzi or Roborazzi (Android), golden tests with `matchesGoldenFile` (Flutter).

## Theme scoping and overlays (REDESIGN isolation)

- Scope the new theme by an attribute or class on the root (`<html data-theme="v2">`), behind a flag or per route group.
- Content moved elsewhere in the DOM (React portals, Vue `<Teleport>`, Angular CDK overlay containers, Svelte portal actions, library popovers) only inherits a theme set on `<html>`/`<body>` or on its overlay container. Native `<dialog>` and popover elements stay in place in the DOM and inherit normally.
- Temporary `v2` primitives when tokens alone cannot change density, DOM or classes; each with name, owner and removal plan.

## Behavior (headless) libraries

React: Radix, React Aria, Ark UI, Headless UI · Vue: Reka UI, Ark UI, Headless UI · Svelte: Bits UI, Melt UI · Angular: Angular CDK · Solid: Kobalte, Ark UI · Web components: Shoelace/Web Awesome. Prefer the one already installed.

## Evidence outside the browser

The bundled scripts need a browser. For native apps:
- captures: simulator or emulator screenshots, or snapshot-test outputs;
- accessibility: Xcode Accessibility Inspector, Espresso `AccessibilityChecks`, Flutter `meetsGuideline` matchers, plus a manual keyboard, switch or screen-reader pass;
- drift: lint rules and snapshot tests replace the style inventory.

Record in STATE which checks used platform tools, and set evidence statuses accordingly.
