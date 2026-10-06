#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
function value(flag) {
  const i = args.indexOf(flag);
  return i >= 0 ? args[i + 1] : undefined;
}

if (args.includes('--help') || !value('--manifest') || !value('--out')) {
  console.log(`Usage:
  node build-review-page.mjs --manifest review/gate-2.json --out review/gate-2.html

Manifest schema (paths relative to the manifest):
{
  "title": "Direction review",
  "subtitle": "optional",
  "groups": ["Competitors", "Controls", "Candidates"],   // optional display order
  "items": [
    {"group": "Candidates", "label": "Direction A", "image": "../directions/a.png", "note": "optional"},
    {"group": "Controls", "label": "Prior fingerprint", "text": "text-only card"}
  ],
  "instructions": ["..."],
  "questions": ["..."],
  "responseFormat": "optional"
}`);
  process.exit(args.includes('--help') ? 0 : 4);
}

const manifestPath = path.resolve(value('--manifest'));
const outPath = path.resolve(value('--out'));
if (!fs.existsSync(manifestPath)) {
  console.error(`Manifest not found: ${manifestPath}`);
  process.exit(4);
}

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
if (!Array.isArray(manifest.items) || !manifest.items.length) {
  console.error('Manifest must contain a non-empty items array.');
  process.exit(4);
}

fs.mkdirSync(path.dirname(outPath), { recursive: true });

function esc(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function relativeImage(image) {
  if (!image) return '';
  const absolute = path.resolve(path.dirname(manifestPath), image);
  return path.relative(path.dirname(outPath), absolute).split(path.sep).join('/');
}

function card(item, i) {
  const label = esc(item.label || `Item ${i + 1}`);
  const src = relativeImage(item.image);
  let body;
  if (src) body = `<a href="${esc(src)}" target="_blank"><img src="${esc(src)}" alt="${label}"></a>`;
  else if (item.text) body = `<div class="text">${esc(item.text)}</div>`;
  else body = '<div class="missing">No image</div>';
  return `<article class="card">
    <div class="meta"><span class="index">${i + 1}</span><h3>${label}</h3></div>
    ${body}
    ${item.note ? `<p>${esc(item.note)}</p>` : ''}
  </article>`;
}

const numbered = manifest.items.map((item, i) => ({ item, i }));
const declaredGroups = Array.isArray(manifest.groups) ? manifest.groups : [];
const usedGroups = [...new Set(numbered.map(({ item }) => item.group || ''))];
const groupOrder = [...declaredGroups.filter((g) => usedGroups.includes(g)), ...usedGroups.filter((g) => !declaredGroups.includes(g))];
const cards = groupOrder.map((group) => {
  const inGroup = numbered.filter(({ item }) => (item.group || '') === group).map(({ item, i }) => card(item, i)).join('\n');
  return `${group ? `<h2 class="group">${esc(group)}</h2>` : ''}<div class="grid">${inGroup}</div>`;
}).join('\n');

const instructions = (manifest.instructions || []).map((x) => `<li>${esc(x)}</li>`).join('');
const questions = (manifest.questions || []).map((x) => `<li>${esc(x)}</li>`).join('');

const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(manifest.title || 'Frontend Excellence Review')}</title>
<style>
:root{font-family:Inter,ui-sans-serif,system-ui,sans-serif;color:#161616;background:#f5f5f3}
*{box-sizing:border-box} body{margin:0;padding:28px} main{max-width:1600px;margin:auto}
h1{font-size:28px;margin:0 0 10px} .intro{max-width:900px;color:#555;margin-bottom:24px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:18px;align-items:start}
.card{background:#fff;border:1px solid #d9d9d6;border-radius:12px;padding:14px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.meta{display:flex;gap:10px;align-items:center;margin-bottom:10px}.meta h3{font-size:16px;margin:0}
h2.group{font-size:18px;margin:28px 0 12px;padding-bottom:6px;border-bottom:1px solid #d9d9d6}
.text{padding:16px;background:#fafafa;border:1px dashed #ccc;border-radius:8px;font-size:14px;line-height:1.5;white-space:pre-wrap}.index{font:12px ui-monospace,monospace;border:1px solid #ccc;border-radius:999px;padding:2px 7px}
img{width:100%;height:auto;display:block;border:1px solid #e5e5e2;border-radius:8px;background:#fafafa}
section{margin-top:28px;max-width:1000px} li{margin:6px 0}.missing{padding:80px 20px;text-align:center;background:#eee;color:#777}
</style>
</head><body><main>
<h1>${esc(manifest.title || 'Frontend Excellence Review')}</h1>
${manifest.subtitle ? `<p class="intro">${esc(manifest.subtitle)}</p>` : ''}
${cards}
${instructions ? `<section><h2>Review instructions</h2><ul>${instructions}</ul></section>` : ''}
${questions ? `<section><h2>Decision questions</h2><ol>${questions}</ol></section>` : ''}
${manifest.responseFormat ? `<section><h2>How to answer</h2><p><code>${esc(manifest.responseFormat)}</code></p></section>` : ''}
</main></body></html>`;

fs.writeFileSync(outPath, html);
console.log(`Review page: ${outPath}`);
console.log(`Open: ${pathToFileURL(outPath).href}`);
