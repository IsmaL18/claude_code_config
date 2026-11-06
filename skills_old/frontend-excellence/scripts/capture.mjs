#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
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
  node capture.mjs --base http://localhost:3000 --routes /,/dashboard \\
    --viewports 1440x1000,390x844 --out design-system/frontend-excellence/qa/captures

Options:
  --ready <selector>            Wait for a product-specific ready selector
  --storage-state <file>       Playwright storageState JSON for authenticated apps
  --color-schemes light,dark   Capture one or more color schemes (default: light)
  --reduced-motion reduce|no-preference  Context preference (default: reduce)
  --wait-ms <n>                Small stabilization wait after ready/fonts (default: 100)
  --freeze-time <ISO>          Freeze visible time when Playwright clock is available
  --selectors <css,...>        Also capture targeted element/region screenshots
  --full-page                  Also save a full-page screenshot; viewport capture remains canonical
  --browser chromium|firefox|webkit  Browser engine (default: chromium); run once per engine
  --axe                        Run an automated accessibility scan per capture
                               (requires @axe-core/playwright in the project)
  --axe-tags <tags>            axe rule tags (default: wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22aa)

The script resolves Playwright from the current project, writes a partial report even when a route fails,
and reports console/page errors, likely overflow/clipping candidates and, with --axe, accessibility violations.
Exit codes: 0 ok · 2 overflow, console/page errors or critical/serious axe violations · 3 capture failed or
dependency missing · 4 bad input.`);
  process.exit(0);
}

const base = (value('--base', 'http://localhost:3000') || '').replace(/\/$/, '');
const routes = (value('--routes', '/') || '/').split(',').map((s) => s.trim()).filter(Boolean);
const viewportSpecs = (value('--viewports', '1440x1000,390x844') || '').split(',').map((s) => s.trim()).filter(Boolean);
const colorSchemes = (value('--color-schemes', 'light') || 'light').split(',').map((s) => s.trim()).filter(Boolean);
const reducedMotion = value('--reduced-motion', 'reduce');
const readySelector = value('--ready');
const storageState = value('--storage-state');
const selectors = (value('--selectors', '') || '').split(',').map((s) => s.trim()).filter(Boolean);
const waitMs = Number(value('--wait-ms', '100'));
const freezeTime = value('--freeze-time');
const outDir = value('--out', 'design-system/frontend-excellence/qa/captures');
const saveFullPage = has('--full-page');
const browserName = value('--browser', 'chromium');
const runAxe = has('--axe');
const axeTags = (value('--axe-tags', 'wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22aa') || '').split(',').map((s) => s.trim()).filter(Boolean);
if (!['chromium', 'firefox', 'webkit'].includes(browserName)) {
  console.error(`Invalid --browser: ${browserName} (use chromium, firefox or webkit)`);
  process.exit(4);
}

const invalidViewports = viewportSpecs.filter((spec) => !/^(\d+)x(\d+)$/.test(spec));
if (invalidViewports.length) {
  console.error(`Invalid viewport(s): ${invalidViewports.join(', ')}`);
  process.exit(4);
}
if (!['reduce', 'no-preference'].includes(reducedMotion)) {
  console.error(`Invalid --reduced-motion: ${reducedMotion}`);
  process.exit(4);
}
if (!colorSchemes.every((s) => ['light', 'dark', 'no-preference'].includes(s))) {
  console.error(`Invalid --color-schemes: ${colorSchemes.join(',')}`);
  process.exit(4);
}
if (storageState && !fs.existsSync(storageState)) {
  console.error(`Storage state not found: ${storageState}`);
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
  console.error('Playwright was not found in the current project. Install "playwright" or "@playwright/test", or use Playwright CLI/MCP instead.');
  process.exit(3);
}

let AxeBuilder = null;
if (runAxe) {
  try {
    const mod = createRequire(path.join(process.cwd(), 'package.json'))('@axe-core/playwright');
    AxeBuilder = mod?.default ?? mod?.AxeBuilder ?? mod;
  } catch {
    // handled below
  }
  if (typeof AxeBuilder !== 'function') {
    console.error('--axe requires "@axe-core/playwright" installed in the current project.');
    process.exit(3);
  }
}

fs.mkdirSync(outDir, { recursive: true });

const report = {
  generatedAt: new Date().toISOString(),
  base,
  options: { routes, viewportSpecs, colorSchemes, reducedMotion, readySelector, selectors, saveFullPage, browser: browserName, axe: runAxe ? axeTags : false },
  captures: [],
};

const browser = await playwright[browserName].launch({ headless: true });

function slugFor(route) {
  const readable = route.replace(/^https?:\/\//, '').replace(/[^a-zA-Z0-9_-]+/g, '_').replace(/^_+|_+$/g, '').slice(0, 60) || 'root';
  const hash = crypto.createHash('sha1').update(route).digest('hex').slice(0, 8);
  return `${readable}-${hash}`;
}

async function collectLayoutSignals(page) {
  return page.evaluate(() => {
    const root = document.documentElement;
    const viewportWidth = root.clientWidth;
    const horizontalOverflow = root.scrollWidth > viewportWidth + 1;
    const candidates = [];

    for (const el of document.querySelectorAll('*')) {
      const rect = el.getBoundingClientRect();
      if (!rect.width || !rect.height) continue;
      const style = getComputedStyle(el);
      const ownOverflow = el.scrollWidth > el.clientWidth + 1;
      const offViewport = rect.right > viewportWidth + 1 || rect.left < -1;
      const clips = ['hidden', 'clip'].includes(style.overflowX);
      if ((ownOverflow && clips) || offViewport) {
        const label = [el.tagName.toLowerCase(), el.id ? `#${el.id}` : '', el.className && typeof el.className === 'string' ? `.${el.className.trim().split(/\s+/).slice(0, 2).join('.')}` : ''].join('');
        candidates.push({
          element: label.slice(0, 160),
          overflowX: style.overflowX,
          scrollWidth: el.scrollWidth,
          clientWidth: el.clientWidth,
          rect: { left: Math.round(rect.left), right: Math.round(rect.right), width: Math.round(rect.width) },
          ownOverflow,
          offViewport,
        });
      }
      if (candidates.length >= 30) break;
    }

    return { horizontalOverflow, clippedOrOffViewportCandidates: candidates };
  });
}

try {
  for (const spec of viewportSpecs) {
    const [, w, h] = spec.match(/^(\d+)x(\d+)$/);
    const viewport = { width: Number(w), height: Number(h) };

    for (const colorScheme of colorSchemes) {
      const contextOptions = { viewport, reducedMotion, colorScheme };
      if (storageState) contextOptions.storageState = storageState;
      const context = await browser.newContext(contextOptions);

      for (const route of routes) {
        const page = await context.newPage();
        const consoleErrors = [];
        const consoleWarnings = [];
        const pageErrors = [];
        page.on('console', (msg) => {
          if (msg.type() === 'error') consoleErrors.push(msg.text());
          if (msg.type() === 'warning') consoleWarnings.push(msg.text());
        });
        page.on('pageerror', (err) => pageErrors.push(String(err)));

        const url = route.startsWith('http') ? route : `${base}${route.startsWith('/') ? route : `/${route}`}`;
        const stem = `${slugFor(route)}-${viewport.width}x${viewport.height}-${colorScheme}${browserName === 'chromium' ? '' : `-${browserName}`}`;
        const entry = { route, url, viewport, colorScheme, status: 'ok', screenshots: {}, consoleErrors, consoleWarnings, pageErrors };

        try {
          if (freezeTime && page.clock?.install) {
            try {
              await page.clock.install({ time: new Date(freezeTime) });
            } catch (err) {
              entry.clockWarning = String(err);
            }
          }

          const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
          entry.httpStatus = response?.status() ?? null;

          if (readySelector) {
            await page.locator(readySelector).first().waitFor({ state: 'visible', timeout: 15000 });
          }
          await page.evaluate(async () => {
            if (document.fonts?.ready) await document.fonts.ready;
          });
          if (Number.isFinite(waitMs) && waitMs > 0) await page.waitForTimeout(waitMs);

          entry.layout = await collectLayoutSignals(page);

          if (AxeBuilder) {
            const results = await new AxeBuilder({ page }).withTags(axeTags).analyze();
            const byImpact = {};
            for (const v of results.violations) byImpact[v.impact || 'unknown'] = (byImpact[v.impact || 'unknown'] || 0) + 1;
            entry.accessibility = {
              violationsByImpact: byImpact,
              violations: results.violations.map((v) => ({
                id: v.id,
                impact: v.impact,
                help: v.help,
                nodes: v.nodes.length,
                targets: v.nodes.slice(0, 3).map((n) => n.target.join(' ')),
              })),
              incomplete: results.incomplete.length,
            };
          }

          const viewportPath = path.join(outDir, `${stem}-viewport.png`);
          await page.screenshot({ path: viewportPath, fullPage: false, animations: 'disabled', caret: 'hide' });
          entry.screenshots.viewport = viewportPath;

          if (saveFullPage) {
            const fullPath = path.join(outDir, `${stem}-full.png`);
            await page.screenshot({ path: fullPath, fullPage: true, animations: 'disabled', caret: 'hide' });
            entry.screenshots.fullPage = fullPath;
          }

          if (selectors.length) {
            entry.screenshots.regions = [];
            for (let i = 0; i < selectors.length; i++) {
              const selector = selectors[i];
              const locator = page.locator(selector).first();
              if (await locator.count()) {
                const regionPath = path.join(outDir, `${stem}-region-${i + 1}.png`);
                await locator.screenshot({ path: regionPath, animations: 'disabled', caret: 'hide' });
                entry.screenshots.regions.push({ selector, path: regionPath });
              } else {
                entry.screenshots.regions.push({ selector, missing: true });
              }
            }
          }
        } catch (err) {
          entry.status = 'failed';
          entry.error = String(err?.stack || err);
        } finally {
          report.captures.push(entry);
          await page.close().catch(() => {});
        }
      }

      await context.close();
    }
  }
} finally {
  await browser.close().catch(() => {});
  const reportPath = path.join(outDir, 'capture-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
  console.log(`Capture report: ${reportPath}`);
}

const failed = report.captures.some((r) => r.status === 'failed');
const severe = report.captures.some((r) =>
  r.layout?.horizontalOverflow ||
  r.consoleErrors?.length ||
  r.pageErrors?.length ||
  r.accessibility?.violationsByImpact?.critical ||
  r.accessibility?.violationsByImpact?.serious);
if (failed) process.exitCode = 3;
else if (severe) process.exitCode = 2;
