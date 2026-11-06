#!/usr/bin/env node
// Computed-style inventory across rendered routes.
// Detects value drift that source scans miss: one-off font sizes, colors, spacings,
// radii or shadows (including those reached through valid utilities) and
// inconsistent type styles. It sees rendered values, not intent: a legitimate
// token used in the wrong role is invisible to it.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const args = process.argv.slice(2);

function value(flag, fallback = undefined) {
  const i = args.indexOf(flag);
  return i >= 0 && args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : fallback;
}

function has(flag) {
  return args.includes(flag);
}

if (has('--help') || args.length === 0) {
  console.log(`Usage:
  node style-inventory.mjs --base http://localhost:3000 --routes /,/orders,/orders/42 \\
    --out design-system/frontend-excellence/qa/style-inventory.json

Options:
  --viewports 1440x1000,390x844   Viewports to inspect (default: 1440x1000)
  --color-schemes light,dark      Color schemes (default: light)
  --scope <css>                   Only inspect elements inside this selector (default: body)
  --ready <selector>              Wait for a product-specific ready selector
  --storage-state <file>          Playwright storageState JSON for authenticated apps
  --wait-ms <n>                   Stabilization wait after ready/fonts (default: 150)
  --max-elements <n>              Cap per page (default: 5000)
  --rare <n>                      Flag values used at most n times overall (default: 2)
  --baseline <file>               Previous --out report; report values not present in it
  --browser chromium|firefox|webkit  Browser engine (default: chromium)
  --json                          Print the full report to stdout

Properties collected on visible elements:
  typeStyle (family/size/line-height/weight), fontSize, fontWeight, lineHeight,
  letterSpacing, fontFamily, color (text), backgroundColor, borderColor,
  borderRadius, boxShadow, padding, gap, margin.

Exit codes: 0 ok · 2 new values versus --baseline · 3 Playwright missing · 4 bad input ·
5 one or more pages failed to load (never a silent pass).
Playwright is loaded from the current project (run from the app root).`);
  process.exit(0);
}

const base = (value('--base', 'http://localhost:3000') || '').replace(/\/$/, '');
const routes = (value('--routes', '/') || '/').split(',').map((s) => s.trim()).filter(Boolean);
const viewportSpecs = (value('--viewports', '1440x1000') || '').split(',').map((s) => s.trim()).filter(Boolean);
const colorSchemes = (value('--color-schemes', 'light') || 'light').split(',').map((s) => s.trim()).filter(Boolean);
const scope = value('--scope', 'body');
const readySelector = value('--ready');
const storageState = value('--storage-state');
const waitMs = Number(value('--wait-ms', '150'));
const maxElements = Number(value('--max-elements', '5000'));
const rareThreshold = Number(value('--rare', '2'));
const baselinePath = value('--baseline');
const outPath = value('--out', 'design-system/frontend-excellence/qa/style-inventory.json');
const json = has('--json');
const browserName = value('--browser', 'chromium');
if (!['chromium', 'firefox', 'webkit'].includes(browserName)) {
  console.error(`Invalid --browser: ${browserName} (use chromium, firefox or webkit)`);
  process.exit(4);
}

for (const spec of viewportSpecs) {
  if (!/^\d+x\d+$/.test(spec)) {
    console.error(`Invalid viewport: ${spec}`);
    process.exit(4);
  }
}
if (!colorSchemes.every((s) => ['light', 'dark', 'no-preference'].includes(s))) {
  console.error(`Invalid --color-schemes: ${colorSchemes.join(',')}`);
  process.exit(4);
}
if (storageState && !fs.existsSync(storageState)) {
  console.error(`Storage state not found: ${storageState}`);
  process.exit(4);
}
if (baselinePath && !fs.existsSync(baselinePath)) {
  console.error(`Baseline report not found: ${baselinePath}`);
  process.exit(4);
}

function loadPlaywrightFromProject() {
  const projectRequire = createRequire(path.join(process.cwd(), 'package.json'));
  for (const pkg of ['playwright', '@playwright/test']) {
    try {
      const mod = projectRequire(pkg);
      if (mod?.chromium) return mod;
    } catch {
      // try next package
    }
  }
  return null;
}

const playwright = loadPlaywrightFromProject();
if (!playwright?.[browserName]) {
  console.error('Playwright was not found in the current project. Install "playwright" or "@playwright/test", or run from the app root.');
  process.exit(3);
}

// Runs in the page. Returns a list of [property, value, descriptor] tuples.
function collect({ scopeSelector, cap }) {
  const root = document.querySelector(scopeSelector) || document.body;
  const out = [];
  const isZero = (v) => !v || /^0(px)?$/.test(v) || v === 'normal' || v === 'none' || v === 'auto';
  const transparent = (c) => !c || c === 'transparent' || /rgba\([^)]*,\s*0\)$/.test(c) || /\/\s*0\)$/.test(c);
  const describe = (el) => {
    const cls = typeof el.className === 'string' ? el.className.trim().split(/\s+/).slice(0, 3).join('.') : '';
    const text = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
    return `${el.tagName.toLowerCase()}${el.id ? `#${el.id}` : ''}${cls ? `.${cls}` : ''}${text ? ` "${text}"` : ''}`;
  };
  const hasOwnText = (el) => [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());

  let count = 0;
  for (const el of root.querySelectorAll('*')) {
    if (count >= cap) break;
    if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'BR'].includes(el.tagName)) continue;
    if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') continue;
    const rect = el.getBoundingClientRect();
    if (!rect.width || !rect.height) continue;
    const s = getComputedStyle(el);
    if (s.visibility === 'hidden' || s.display === 'none') continue;
    count++;
    const d = describe(el);
    const push = (prop, v) => out.push([prop, v, d]);

    if (hasOwnText(el)) {
      const family = s.fontFamily.split(',')[0].trim().replace(/^["']|["']$/g, '');
      push('typeStyle', `${family} ${s.fontSize}/${s.lineHeight} ${s.fontWeight}`);
      push('fontFamily', family);
      push('fontSize', s.fontSize);
      push('fontWeight', s.fontWeight);
      push('lineHeight', s.lineHeight);
      if (!isZero(s.letterSpacing)) push('letterSpacing', s.letterSpacing);
      push('color', s.color);
    }
    if (!transparent(s.backgroundColor)) push('backgroundColor', s.backgroundColor);
    for (const side of ['Top', 'Right', 'Bottom', 'Left']) {
      if (parseFloat(s[`border${side}Width`]) > 0 && s[`border${side}Style`] !== 'none' && !transparent(s[`border${side}Color`])) {
        push('borderColor', s[`border${side}Color`]);
      }
    }
    const radii = [s.borderTopLeftRadius, s.borderTopRightRadius, s.borderBottomRightRadius, s.borderBottomLeftRadius];
    if (radii.some((r) => !isZero(r))) push('borderRadius', [...new Set(radii)].join(' '));
    if (!isZero(s.boxShadow)) push('boxShadow', s.boxShadow);
    for (const side of ['Top', 'Right', 'Bottom', 'Left']) {
      if (!isZero(s[`padding${side}`])) push('padding', s[`padding${side}`]);
      if (!isZero(s[`margin${side}`])) push('margin', s[`margin${side}`]);
    }
    if (/flex|grid/.test(s.display)) {
      for (const g of [s.rowGap, s.columnGap]) if (!isZero(g)) push('gap', g);
    }
  }
  return { tuples: out, inspected: count };
}

const inventory = {}; // prop -> value -> { count, locations:Set, samples:[] }
const pages = [];
const browser = await playwright[browserName].launch({ headless: true });

try {
  for (const spec of viewportSpecs) {
    const [w, h] = spec.split('x').map(Number);
    for (const scheme of colorSchemes) {
      const context = await browser.newContext({
        viewport: { width: w, height: h },
        colorScheme: scheme,
        reducedMotion: 'reduce',
        ...(storageState ? { storageState } : {}),
      });
      const page = await context.newPage();
      for (const route of routes) {
        const url = /^https?:\/\//.test(route) ? route : `${base}${route.startsWith('/') ? route : `/${route}`}`;
        const location = `${route} @${spec} ${scheme}`;
        try {
          await page.goto(url, { waitUntil: 'load' });
          if (readySelector) await page.waitForSelector(readySelector, { timeout: 15000 });
          await page.evaluate(() => document.fonts?.ready);
          if (waitMs > 0) await page.waitForTimeout(waitMs);
          const { tuples, inspected } = await page.evaluate(collect, { scopeSelector: scope, cap: maxElements });
          for (const [prop, v, d] of tuples) {
            inventory[prop] ??= {};
            const entry = (inventory[prop][v] ??= { count: 0, locations: new Set(), samples: [] });
            entry.count++;
            entry.locations.add(location);
            if (entry.samples.length < 3) entry.samples.push(`${location} → ${d}`);
          }
          pages.push({ location, url, inspectedElements: inspected, ok: true });
        } catch (error) {
          pages.push({ location, url, ok: false, error: String(error?.message || error).slice(0, 300) });
        }
      }
      await context.close();
    }
  }
} finally {
  await browser.close();
}

const properties = {};
for (const [prop, values] of Object.entries(inventory)) {
  properties[prop] = Object.entries(values)
    .map(([v, e]) => ({ value: v, count: e.count, locations: [...e.locations], samples: e.samples }))
    .sort((a, b) => b.count - a.count);
}

const summary = Object.fromEntries(Object.entries(properties).map(([p, list]) => [p, list.length]));
const rare = Object.fromEntries(
  Object.entries(properties)
    .map(([p, list]) => [p, list.filter((x) => x.count <= rareThreshold)])
    .filter(([, list]) => list.length),
);

let newValues = null;
if (baselinePath) {
  const baseline = JSON.parse(fs.readFileSync(baselinePath, 'utf8'));
  newValues = {};
  for (const [prop, list] of Object.entries(properties)) {
    const known = new Set((baseline.properties?.[prop] || []).map((x) => x.value));
    const added = list.filter((x) => !known.has(x.value));
    if (added.length) newValues[prop] = added;
  }
}

const report = {
  generatedAt: new Date().toISOString(),
  base,
  options: { routes, viewportSpecs, colorSchemes, scope, readySelector: readySelector || null, rareThreshold, browser: browserName },
  pages,
  summary,
  rare,
  baseline: baselinePath || null,
  newValues,
  properties,
};

fs.mkdirSync(path.dirname(path.resolve(outPath)), { recursive: true });
fs.writeFileSync(outPath, JSON.stringify(report, null, 2));

const newCount = newValues ? Object.values(newValues).reduce((n, l) => n + l.length, 0) : 0;

if (json) {
  console.log(JSON.stringify(report, null, 2));
} else {
  const failed = pages.filter((p) => !p.ok);
  console.log(`Pages inspected: ${pages.length - failed.length}/${pages.length}`);
  for (const p of failed) console.log(`  FAILED ${p.location}: ${p.error}`);
  console.log('\nDistinct values per property:');
  for (const [p, n] of Object.entries(summary).sort((a, b) => b[1] - a[1])) console.log(`  ${p.padEnd(16)} ${n}`);
  const rareProps = Object.entries(rare);
  if (rareProps.length) {
    console.log(`\nRare values (used ≤ ${rareThreshold}×), likely one-offs:`);
    for (const [p, list] of rareProps) {
      for (const x of list.slice(0, 8)) console.log(`  ${p}: ${x.value} ×${x.count}  ${x.samples[0] || ''}`);
      if (list.length > 8) console.log(`  ${p}: … ${list.length - 8} more`);
    }
  }
  if (newValues) {
    console.log(`\nNew values versus baseline: ${newCount}`);
    for (const [p, list] of Object.entries(newValues)) {
      for (const x of list) console.log(`  ${p}: ${x.value} ×${x.count}  ${x.samples[0] || ''}`);
    }
  }
  console.log(`\nReport: ${outPath}`);
}

if (pages.some((p) => !p.ok)) process.exit(5);
process.exit(newCount ? 2 : 0);
