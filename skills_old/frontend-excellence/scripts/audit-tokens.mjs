#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);

function value(flag, fallback = undefined) {
  const i = args.indexOf(flag);
  return i >= 0 && args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : fallback;
}

function has(flag) {
  return args.includes(flag);
}

if (has('--help') || args.length === 0) {
  console.log(`Usage: node audit-tokens.mjs <path...> [--json] [--baseline report.json] [--exclude text1,text2] [--ext .foo,.bar]

Scans scripts, styles and templates (JS/TS, CSS/Sass/Less/Stylus, Vue, Svelte, Astro, HTML, MDX,
ERB, Blade, Twig, Jinja, Nunjucks, Handlebars, Liquid, Razor, HEEx...; add more with --ext)
for likely design-token drift:
- literal colors not expressed through CSS variables;
- default Tailwind palette utilities (zinc/blue/etc.);
- arbitrary Tailwind values;
- inline/CSS border-radius and box-shadow values;
- explicit font-size values.

Use --baseline to report only findings that are new versus an existing --json report
(compared by file, kind and value, not line number). Exit code 2 when (new) findings exist,
so it can gate CI or a pre-commit hook.`);
  process.exit(0);
}

const json = has('--json');
const baselinePath = value('--baseline');
const excludes = (value('--exclude', '') || '').split(',').map((s) => s.trim()).filter(Boolean);
const roots = [];
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === '--baseline' || a === '--exclude' || a === '--ext') { i++; continue; }
  if (a === '--json') continue;
  if (!a.startsWith('--')) roots.push(a);
}

if (!roots.length) {
  console.error('No scan path provided.');
  process.exit(4);
}
for (const root of roots) {
  if (!fs.existsSync(root)) {
    console.error(`Scan path does not exist: ${root}`);
    process.exit(4);
  }
}
if (baselinePath && !fs.existsSync(baselinePath)) {
  console.error(`Baseline report does not exist: ${baselinePath}`);
  process.exit(4);
}

const ignoredDirs = new Set(['node_modules', 'dist', 'build', '.next', '.nuxt', '.svelte-kit', '.astro', '.output', '.git', 'coverage', 'vendor']);
const exts = new Set([
  '.css', '.scss', '.sass', '.less', '.styl', '.pcss',
  '.js', '.jsx', '.mjs', '.cjs', '.ts', '.tsx', '.mts', '.cts',
  '.vue', '.svelte', '.astro', '.mdx', '.html', '.htm',
  '.erb', '.haml', '.slim', '.twig', '.jinja', '.jinja2', '.j2', '.njk', '.hbs', '.handlebars', '.mustache',
  '.liquid', '.ejs', '.pug', '.cshtml', '.razor', '.heex', '.leex', '.eex', '.gohtml', '.tmpl',
]);
for (const e of (value('--ext', '') || '').split(',').map((x) => x.trim()).filter(Boolean)) exts.add(e.startsWith('.') ? e : `.${e}`);
const hasScannedExtension = (p) => exts.has(path.extname(p)) || p.endsWith('.blade.php');

function walk(p, out = []) {
  const st = fs.statSync(p);
  if (st.isFile()) {
    if (hasScannedExtension(p)) out.push(p);
    return out;
  }
  for (const name of fs.readdirSync(p)) {
    if (ignoredDirs.has(name)) continue;
    walk(path.join(p, name), out);
  }
  return out;
}

const tailwindPalette = /\b(?:bg|text|border|ring|outline|divide|fill|stroke)-(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-(?:50|100|200|300|400|500|600|700|800|900|950)\b/g;
const arbitraryTailwind = /\b(?:[a-z0-9-]+:)*[a-z0-9-]+-\[[^\]]+\]/gi;
const hexColor = /#[0-9a-fA-F]{3,8}\b/g;
const rgbColor = /\b(?:rgb|rgba|hsl|hsla|oklch|oklab)\([^\n)]*\)/gi;
const camelRadius = /\bborderRadius\s*[:=]\s*["'`]?\d+(?:\.\d+)?(?:px|rem|em)?/gi;
const cssRadius = /\bborder-radius\s*:\s*[^;]+/gi;
const camelShadow = /\bboxShadow\s*[:=]\s*["'`][^"'`]+/gi;
const cssShadow = /\bbox-shadow\s*:\s*[^;]+/gi;
const fontSize = /\b(?:fontSize|font-size)\s*[:=]\s*["'`]?\d+(?:\.\d+)?(?:px|rem|em)/gi;

function isLikelyAnchorOrText(line, match) {
  const idx = line.indexOf(match);
  const before = line.slice(Math.max(0, idx - 20), idx).toLowerCase();
  if (/href\s*=\s*["']?$/.test(before)) return true;
  if (/issue\s*$/.test(before)) return true;
  return false;
}

function addMatches(findings, file, lineNo, line, kind, regex, predicate = () => true) {
  regex.lastIndex = 0;
  for (const match of line.matchAll(regex)) {
    const value = match[0];
    if (!predicate(value, match)) continue;
    findings.push({ file, line: lineNo, kind, value: value.slice(0, 180) });
  }
}

const files = [...new Set(roots.flatMap((r) => walk(r)))].filter((file) => !excludes.some((x) => file.includes(x)));
const findings = [];

for (const file of files) {
  const text = fs.readFileSync(file, 'utf8');
  const lines = text.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNo = i + 1;

    addMatches(findings, file, lineNo, line, 'tailwind default palette', tailwindPalette);
    addMatches(findings, file, lineNo, line, 'arbitrary Tailwind value', arbitraryTailwind);
    addMatches(findings, file, lineNo, line, 'literal hex color', hexColor, (v) => !isLikelyAnchorOrText(line, v));
    addMatches(findings, file, lineNo, line, 'literal functional color', rgbColor, (v) => !/var\(\s*--/.test(v));
    addMatches(findings, file, lineNo, line, 'inline border radius', camelRadius);
    addMatches(findings, file, lineNo, line, 'CSS border radius', cssRadius, (v) => !/var\(\s*--/.test(v));
    addMatches(findings, file, lineNo, line, 'inline box shadow', camelShadow, (v) => !/var\(\s*--/.test(v));
    addMatches(findings, file, lineNo, line, 'CSS box shadow', cssShadow, (v) => !/var\(\s*--/.test(v));
    addMatches(findings, file, lineNo, line, 'explicit font size', fontSize, (v) => !/var\(\s*--/.test(v));
  }
}

// Baseline comparison ignores line numbers so unrelated edits that shift lines
// do not create false "new" findings. A finding is new when its
// (file, kind, value) occurs more often than in the baseline.
function key(f) {
  return `${path.resolve(f.file)}|${f.kind}|${f.value}`;
}

const baselineCounts = new Map();
if (baselinePath) {
  const baseline = JSON.parse(fs.readFileSync(baselinePath, 'utf8'));
  for (const f of baseline.findings || []) baselineCounts.set(key(f), (baselineCounts.get(key(f)) || 0) + 1);
}

const seen = new Map();
const newFindings = baselinePath
  ? findings.filter((f) => {
      const k = key(f);
      const n = (seen.get(k) || 0) + 1;
      seen.set(k, n);
      return n > (baselineCounts.get(k) || 0);
    })
  : findings;
const result = {
  scannedFiles: files.length,
  totalFindings: findings.length,
  baseline: baselinePath || null,
  newFindingsCount: newFindings.length,
  findings,
  newFindings,
};

if (json) {
  console.log(JSON.stringify(result, null, 2));
} else {
  const rows = baselinePath ? newFindings : findings;
  if (!rows.length) console.log(baselinePath ? 'No new likely token drift found.' : 'No likely token drift found.');
  for (const f of rows) console.log(`${f.file}:${f.line} [${f.kind}] ${f.value}`);
  console.log(`\nScanned files: ${files.length}`);
  console.log(`Total findings: ${findings.length}`);
  if (baselinePath) console.log(`New findings: ${newFindings.length}`);
}

process.exit((baselinePath ? newFindings.length : findings.length) ? 2 : 0);
