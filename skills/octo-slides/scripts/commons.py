"""Images sous licence libre de Wikimedia Commons, pour illustrer un deck quand la bibliothèque OCTO ne suffit pas
(une photo de turbine, un portrait historique, un parc solaire). API publique, sans clé ; seuls les fichiers du
domaine public, CC0, CC BY et CC BY-SA sont gardés, avec leur auteur et leur licence pour la slide de crédits.

Chercher : une planche de vignettes par requête, pour choisir à l'œil (lire les planches, puis noter les titres).

    python3 -I commons.py search <dossier> "turbine|steam turbine power plant" "solaire|photovoltaic solar park"

    → <dossier>/<clé>_<n>.jpg (vignettes), <dossier>/planche_<clé>.png, <dossier>/index.json (titres, licences)

Télécharger les images retenues (1 400 px de large au plus) et leurs crédits :

    python3 -I commons.py fetch <dossier images du deck> "turbine=File:Westinghouse steam turbine 01.jpg" …

    → <dossier>/<nom>.jpg et <dossier>/credits_commons.json (titre, auteur, licence, page d'origine)

Requêtes en anglais : Commons est indexé surtout en anglais. Une requête en allemand trouve souvent les photos
d'installations industrielles (« Dampfturbine Kraftwerk »). Voir references/images.md.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://commons.wikimedia.org/w/api.php?"
UA = "octo-slides/2.0 (skill de slides OCTO ; https://www.octo.com)"
FREE = re.compile(r"^(Public domain|PD\b|CC0|CC BY(-SA)? [0-9.]+)", re.I)
MIN_WIDTH = 700  # pixels : en dessous, l'image est floue projetée


def _get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
        return r.read()


def _strip(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def _api(**params):
    return json.loads(_get(API + urllib.parse.urlencode({**params, "format": "json"})))


def search(query, limit=8):
    """Fichiers libres de Commons pour une requête : [{title, licence, auteur, w, h, thumb, page}]."""
    data = _api(action="query", generator="search", gsrsearch=f"{query} filetype:bitmap", gsrnamespace=6,
                gsrlimit=25, prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=400)
    pages = sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    found = []
    for p in pages:
        ii = p["imageinfo"][0]
        meta = ii.get("extmetadata", {})
        licence = _strip(meta.get("LicenseShortName", {}).get("value", ""))
        if not FREE.match(licence) or ii["width"] < MIN_WIDTH:
            continue
        auteur = _strip(meta.get("Artist", {}).get("value", ""))
        found.append({"title": p["title"], "licence": licence, "auteur": auteur, "w": ii["width"], "h": ii["height"],
                      "thumb": ii["thumburl"], "page": ii["descriptionurl"]})
        if len(found) == limit:
            break
    return found


def contact_sheet(files, out, size=220, cols=8):
    """Planche de vignettes légendées par leur nom de fichier (Pillow requis)."""
    from PIL import Image, ImageDraw
    rows = (len(files) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * (size + 8), max(rows, 1) * (size + 24)), "white")
    draw = ImageDraw.Draw(canvas)
    for i, f in enumerate(files):
        x, y = (i % cols) * (size + 8), (i // cols) * (size + 24)
        try:
            im = Image.open(f).convert("RGB")
            im.thumbnail((size, size))
            canvas.paste(im, (x, y))
        except OSError as e:
            draw.text((x, y), str(e)[:30], fill="red")
        draw.text((x, y + size + 4), Path(f).stem, fill="black")
    canvas.save(out)


def cmd_search(out, queries):
    out.mkdir(parents=True, exist_ok=True)
    index = json.loads((out / "index.json").read_text()) if (out / "index.json").exists() else {}
    for arg in queries:
        key, query = arg.split("|", 1)
        found = search(query)
        index[key] = found
        files = []
        for k, c in enumerate(found):
            f = out / f"{key}_{k}.jpg"
            f.write_bytes(_get(c["thumb"]))
            files.append(f)
            time.sleep(0.2)
        print(f"{key} : {len(found)} image(s) libre(s)")
        for k, c in enumerate(found):
            print(f"  {k} {c['title'][5:75]} | {c['w']}x{c['h']} | {c['licence']} | {c['auteur'][:40]}")
        if files:
            try:
                contact_sheet(files, out / f"planche_{key}.png")
            except ImportError:
                print("  (Pillow absent : pas de planche, regarder les vignettes une à une)")
    (out / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1))


def cmd_fetch(out, choices, width=1400):
    out.mkdir(parents=True, exist_ok=True)
    path = out / "credits_commons.json"
    credits = json.loads(path.read_text()) if path.exists() else {}
    for arg in choices:
        name, title = arg.split("=", 1)
        page = next(iter(_api(action="query", titles=title, prop="imageinfo", iiprop="url|extmetadata",
                              iiurlwidth=width)["query"]["pages"].values()))
        ii = page["imageinfo"][0]
        meta = ii["extmetadata"]
        (out / f"{name}.jpg").write_bytes(_get(ii.get("thumburl") or ii["url"]))
        auteur = _strip(meta.get("Artist", {}).get("value", ""))
        credits[name] = {"titre": title.removeprefix("File:"), "auteur": auteur,
                         "licence": _strip(meta.get("LicenseShortName", {}).get("value", "")),
                         "page": ii["descriptionurl"]}
        print(f"{name}.jpg | {credits[name]['auteur'][:50]} | {credits[name]['licence']}")
    path.write_text(json.dumps(credits, ensure_ascii=False, indent=1))


def credit_line(credit):
    """« auteur · licence » prêt pour la slide de crédits (auteur raccourci, « domaine public » en français)."""
    import html
    auteur = re.sub(r" (from .*|\(talk\))$", "", html.unescape(credit["auteur"])) or "auteur inconnu"
    licence = {"Public domain": "domaine public"}.get(credit["licence"], credit["licence"])
    return f"{auteur} · {licence}"


if __name__ == "__main__":
    if len(sys.argv) < 4 or sys.argv[1] not in ("search", "fetch"):
        sys.exit(__doc__)
    (cmd_search if sys.argv[1] == "search" else cmd_fetch)(Path(sys.argv[2]), sys.argv[3:])
