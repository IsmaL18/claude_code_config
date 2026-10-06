#!/usr/bin/env node
// Preflight: reports which tooling the skill can use in the current project.
// Read-only: it never installs anything.
import path from 'node:path';
import { createRequire } from 'node:module';

const args = process.argv.slice(2);
if (args.includes('--help')) {
  console.log(`Usage: node preflight.mjs [--json] [--browsers chromium,firefox,webkit]

Run from the app root. Checks, without installing anything:
- Node.js version (18+ required by the scripts);
- Playwright resolvable from the project ("playwright" or "@playwright/test");
- which browser engines can actually launch;
- @axe-core/playwright (for capture.mjs --axe).

Skills and MCP servers are not checked here: the agent reads them from its own tool list.
Exit codes: 0 required tooling present · 2 Playwright or every browser missing.`);
  process.exit(0);
}

const json = args.includes('--json');
const i = args.indexOf('--browsers');
const engines = (i >= 0 && args[i + 1] ? args[i + 1] : 'chromium,firefox,webkit').split(',').map((s) => s.trim()).filter(Boolean);

const projectRequire = createRequire(path.join(process.cwd(), 'package.json'));
function resolveFromProject(name) {
  try {
    return projectRequire(name);
  } catch {
    return null;
  }
}

const result = { cwd: process.cwd(), node: process.versions.node, nodeOk: Number(process.versions.node.split('.')[0]) >= 18 };

let playwright = null;
for (const pkg of ['playwright', '@playwright/test']) {
  const mod = resolveFromProject(pkg);
  if (mod?.chromium) {
    playwright = mod;
    result.playwright = pkg;
    break;
  }
}
result.playwrightOk = Boolean(playwright);

result.browsers = {};
if (playwright) {
  for (const name of engines) {
    if (!playwright[name]) {
      result.browsers[name] = 'unknown engine';
      continue;
    }
    try {
      const browser = await Promise.race([
        playwright[name].launch({ headless: true }),
        new Promise((_, reject) => setTimeout(() => reject(new Error('launch timeout')), 20000)),
      ]);
      await browser.close();
      result.browsers[name] = 'ok';
    } catch (error) {
      result.browsers[name] = `missing (${String(error?.message || error).split('\n')[0].slice(0, 120)})`;
    }
  }
}
result.anyBrowserOk = Object.values(result.browsers).includes('ok');
result.axeOk = Boolean(resolveFromProject('@axe-core/playwright'));

const missing = [];
if (!result.nodeOk) missing.push('Node.js 18+ is required by the scripts.');
if (!result.playwrightOk) missing.push('Playwright: npm i -D @playwright/test   (then install browsers)');
const absentEngines = Object.entries(result.browsers).filter(([, v]) => v !== 'ok').map(([k]) => k);
if (result.playwrightOk && absentEngines.length) missing.push(`Browsers: npx playwright install ${absentEngines.join(' ')}   (Linux/CI: add --with-deps)`);
if (!result.axeOk) missing.push('Accessibility scan: npm i -D @axe-core/playwright   (or use the project\'s own a11y tooling)');
result.suggestions = missing;

if (json) {
  console.log(JSON.stringify(result, null, 2));
} else {
  console.log(`Node ${result.node} ${result.nodeOk ? 'ok' : '(18+ required)'}`);
  console.log(`Playwright: ${result.playwright || 'not found in this project'}`);
  for (const [k, v] of Object.entries(result.browsers)) console.log(`  ${k}: ${v}`);
  console.log(`@axe-core/playwright: ${result.axeOk ? 'ok' : 'not found'}`);
  if (missing.length) {
    console.log('\nNot installed (ask the user before installing anything):');
    for (const m of missing) console.log(`  - ${m}`);
  }
}

process.exit(result.nodeOk && result.playwrightOk && result.anyBrowserOk ? 0 : 2);
