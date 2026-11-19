"""Lit une maquette HTML de slide et la traduit en mesures pour la reproduire en .pptx.

    uv run --with python-pptx python maquette.py maquette.html [dossier_de_sortie]

Le navigateur (Chrome ou Chromium, sans interface) affiche la maquette, mesure chaque élément visible, puis le
script écrit dans le dossier de sortie :
- maquette.md : un élément par ligne, en pouces sur une slide de 10 x 5,625 : position, taille, forme (fond,
  contour, coins arrondis traduits en `corners` de bloc()), texte (taille en pt, gras, couleur) ; les couleurs sont
  ramenées à la teinte de la charte la plus proche, et signalées quand elles en sont loin ;
- maquette.json : les mêmes mesures, brutes ;
- maquette.png : la capture de la maquette, à comparer au rendu du .pptx.
La slide est le plus grand élément au format 16:9 (ou l'élément marqué data-slide, ou class="slide").
Sans navigateur, lire le HTML et sa CSS directement (references/mise_en_page.md §7).
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHROMES = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
           "/Applications/Chromium.app/Contents/MacOS/Chromium", "google-chrome", "chromium", "chromium-browser"]

MEASURE = r"""
<script>
window.addEventListener("load", () => document.fonts.ready.then(() => {
  const all = [...document.querySelectorAll("body *")];
  const ratio = el => { const r = el.getBoundingClientRect(); return r.height ? r.width / r.height : 0; };
  const root = document.querySelector("[data-slide], .slide") ||
    all.filter(el => Math.abs(ratio(el) - 16 / 9) < 0.08).sort((a, b) =>
      b.getBoundingClientRect().width - a.getBoundingClientRect().width)[0] || document.body;
  const R = root.getBoundingClientRect(), k = 10 / R.width;  // pouces par pixel
  // Texte d'un élément avec ses enfants en ligne (b, strong, span…) recomposés en balisage **gras** : une phrase
  // reste une phrase. Les enfants en bloc (div, p, inline-block) sont des éléments à part.
  const inline = el => getComputedStyle(el).display === "inline";
  const consumed = new Set();
  const own = el => {
    let out = "";
    for (const n of el.childNodes) {
      if (n.nodeType === 3) out += n.textContent;
      else if (n.nodeType === 1 && inline(n) && n.tagName !== "BR") {
        consumed.add(n);
        n.querySelectorAll("*").forEach(c => consumed.add(c));
        const t = n.innerText;
        out += parseInt(getComputedStyle(n).fontWeight) >= 600 && parseInt(getComputedStyle(el).fontWeight) < 600
          ? `**${t.trim()}**${/\s$/.test(t) ? " " : ""}` : t;
      } else if (n.tagName === "BR") out += "\n";
    }
    return out.replace(/[ \t]+/g, " ").replace(/ *\n */g, "\n").trim();
  };
  const items = [];
  for (const el of root.querySelectorAll("*")) {
    if (consumed.has(el)) continue;
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    if (r.width < 1 || r.height < 1 || cs.visibility === "hidden" || cs.display === "none") continue;
    const border = parseFloat(cs.borderTopWidth) + parseFloat(cs.borderRightWidth) +
      parseFloat(cs.borderBottomWidth) + parseFloat(cs.borderLeftWidth);
    const bg = cs.backgroundColor, text = own(el);
    const filled = bg && !bg.endsWith(", 0)") && bg !== "transparent";
    const media = ["IMG", "SVG", "svg", "CANVAS"].includes(el.tagName) || cs.backgroundImage !== "none";
    if (!filled && !border && !text && !media) continue;
    items.push({
      tag: el.tagName.toLowerCase(), cls: el.className && el.className.baseVal === undefined ? el.className : "",
      x: (r.left - R.left) * k, y: (r.top - R.top) * k, w: r.width * k, h: r.height * k,
      fill: filled ? bg : null, border: border ? cs.borderTopColor : null, border_px: border / 4,
      dashed: cs.borderTopStyle === "dashed" || cs.borderTopStyle === "dotted",
      radii: [cs.borderTopLeftRadius, cs.borderTopRightRadius, cs.borderBottomRightRadius,
              cs.borderBottomLeftRadius].map(v => parseFloat(v) * k),
      text, size_pt: parseFloat(cs.fontSize) * k * 72, bold: parseInt(cs.fontWeight) >= 600,
      color: cs.color, align: cs.textAlign, media,
      src: el.tagName === "IMG" ? el.getAttribute("src") : null,
    });
  }
  const out = {slide_px: [R.width, R.height], scale: k, items};
  document.body.innerHTML = "";
  const pre = document.createElement("pre");
  pre.id = "__maquette";
  pre.textContent = JSON.stringify(out);
  document.body.appendChild(pre);
}));
</script>
"""


def find_chrome():
    for c in CHROMES:
        if Path(c).exists() or shutil.which(c):
            return c if Path(c).exists() else shutil.which(c)
    return None


def run_chrome(chrome, *args):
    return subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", *args],
                          capture_output=True, text=True, timeout=90)


def measure(chrome, html):
    """Mesures de la maquette, par le DOM final de Chrome (le script remplace la page par ses mesures)."""
    src = html.read_text(encoding="utf-8")
    src = src.replace("</body>", MEASURE + "</body>") if "</body>" in src else src + MEASURE
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=html.parent, delete=False, encoding="utf-8") as f:
        f.write(src)  # même dossier que la maquette : ses images et feuilles de style relatives restent valides
        tmp = Path(f.name)
    try:
        dom = run_chrome(chrome, "--virtual-time-budget=8000", "--window-size=1600,900", "--dump-dom",
                         tmp.as_uri()).stdout
    finally:
        tmp.unlink()
    start = dom.find('<pre id="__maquette">')
    if start < 0:
        raise RuntimeError("mesure impossible : la page n'a pas fini de charger (voir la console du navigateur)")
    import html as h
    return json.loads(h.unescape(dom[start + len('<pre id="__maquette">'):dom.find("</pre>", start)]))


def _rgb(css):
    if not css or not css.startswith("rgb"):
        return None
    parts = css[css.index("(") + 1:css.index(")")].replace("/", ",").split(",")
    return tuple(int(float(p)) for p in parts[:3])


def _palette():
    import octo_slides
    from pptx.dml.color import RGBColor
    return {name: tuple(value) for name, value in vars(octo_slides).items()
            if isinstance(value, RGBColor) and name.isupper()}


def nearest(css, palette):
    """Teinte de la charte la plus proche d'une couleur CSS, et l'écart (distance RVB)."""
    rgb = _rgb(css)
    if rgb is None:
        return None, 0
    name, ref = min(palette.items(), key=lambda kv: sum((a - b) ** 2 for a, b in zip(kv[1], rgb)))
    return name, sum((a - b) ** 2 for a, b in zip(ref, rgb)) ** 0.5


def corners(radii, threshold=0.06):
    """Coins arrondis (pouces, ordre haut gauche, haut droit, bas droit, bas gauche) -> argument corners de bloc()."""
    names = ["tl", "tr", "br", "bl"]
    on = {n for n, r in zip(names, radii) if r >= threshold}
    if len(on) == 3:
        return f"goutte (coin carré {({*names} - on).pop()})"
    return {frozenset(): "none", frozenset(names): "all", frozenset({"tl", "br"}): "tl-br",
            frozenset({"tr", "bl"}): "tr-bl", frozenset({"tl", "tr"}): "top",
            frozenset({"bl", "br"}): "bottom"}.get(frozenset(on), next(iter(on)) if len(on) == 1 else
                                                    "+".join(sorted(on)))


def describe(data):
    palette = _palette()
    lines = ["# Maquette mesurée", "",
             f"Slide : {data['slide_px'][0]:.0f} x {data['slide_px'][1]:.0f} px dans la maquette, ramenée à "
             "10 x 5,625 pouces. Coordonnées en pouces, tailles de texte en pt. Couleur : teinte de la charte la "
             "plus proche (⚠ si l'écart dépasse 40 : couleur hors charte, à ramener dans la charte).", "",
             "| # | x | y | w | h | forme | texte |", "|---|---|---|---|---|---|---|"]
    for i, it in enumerate(data["items"], 1):
        shape = []
        if it["fill"]:
            name, gap = nearest(it["fill"], palette)
            shape.append(f"fond {name}{' ⚠' if gap > 40 else ''}")
        if it["border"]:
            name, gap = nearest(it["border"], palette)
            shape.append(f"contour {name} {it['border_px'] * data['scale'] * 72:.2f} pt"
                         f"{' pointillé' if it['dashed'] else ''}{' ⚠' if gap > 40 else ''}")
        if it["fill"] or it["border"]:
            r = max(it["radii"])
            shape.append(f"coins {corners(it['radii'])}" + (f" r {r:.2f}" if r >= 0.06 else ""))
        if it["media"]:
            shape.append(f"image {it['src'] or '(fond ou svg)'}")
        text = ""
        if it["text"]:
            name, gap = nearest(it["color"], palette)
            text = (f"« {it['text'][:90].replace(chr(10), ' / ')} » {it['size_pt']:.1f} pt{' gras' if it['bold'] else ''} {name}"
                    f"{' ⚠' if gap > 40 else ''}{' centré' if it['align'] == 'center' else ''}")
        lines.append(f"| {i} | {it['x']:.2f} | {it['y']:.2f} | {it['w']:.2f} | {it['h']:.2f} | "
                     f"{', '.join(shape) or it['tag']} | {text} |")
    return "\n".join(lines) + "\n"


def main():
    html = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else html.parent / (html.stem + "_mesures")
    out.mkdir(parents=True, exist_ok=True)
    chrome = find_chrome()
    if not chrome:
        sys.exit("Aucun navigateur Chrome / Chromium trouvé : lire le HTML et sa CSS directement.")
    data = measure(chrome, html)
    (out / "maquette.json").write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    (out / "maquette.md").write_text(describe(data), encoding="utf-8")
    w, h = (round(v) for v in data["slide_px"])
    run_chrome(chrome, f"--window-size={w},{h}", f"--screenshot={out / 'maquette.png'}", html.as_uri())
    print(f"{len(data['items'])} éléments mesurés -> {out / 'maquette.md'}")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
