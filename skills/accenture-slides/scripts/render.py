"""Rend un .pptx en PNG (une image par slide + planches contact) pour relecture visuelle, et contrôle le rendu.

    uv run --with python-pptx --with pymupdf --with pillow python render.py deck.pptx [out_dir]

Export PDF via Microsoft PowerPoint (AppleScript, macOS), sur une copie au nom unique : PowerPoint garde en cache les
présentations déjà ouvertes, et réexporter un fichier du même nom peut donner l'ancienne version. La copie et le PDF
passent par le conteneur sandbox de PowerPoint (~/Library/Containers/com.microsoft.Powerpoint/Data/Documents) : il y
lit et écrit sans demander « Accorder l'accès », alors qu'un fichier du projet déclenche cette boîte de dialogue.
Sans PowerPoint (bac à sable de claude.ai ou Claude Desktop, Linux), repli sur LibreOffice (soffice), avec les polices
du skill installées depuis assets/fonts* (Outfit ; Liberation Sans, aux métriques d'Arial, pour Accenture) : rendu
approximatif (coupures de ligne, formes du gabarit), à ne pas suivre à la lettre.
Les slides masquées sont rendues visibles dans la copie (relues comme les autres) ; le deck d'origine n'est pas touché.
La police de la charte (Outfit pour OCTO et La Grosse Conf, Arial pour Accenture) doit être installée pour un rendu
fidèle (sinon substitution).

Contrôles sur le PDF, là où PowerPoint a vraiment placé le texte :
- rendu périmé (le texte du PDF ne correspond pas à celui du deck) : erreur, rien n'est relu ;
- police de substitution ;
- lignes de texte qui se superposent (deux blocs l'un sur l'autre, un titre sur deux lignes qui mord sur le
  sous-titre) ;
- texte hors de la slide ;
- texte qui déborde de sa forme (une boîte trop petite pour ses lignes).
"""
from itertools import combinations
import re
import subprocess
import sys
import time
import unicodedata
import zipfile
from pathlib import Path

import os
import shutil
import tempfile

import fitz
from PIL import Image

TOL = 2.0  # points : marge tolérée avant de signaler un débordement
ASSETS = Path(__file__).resolve().parent.parent / "assets"
FONTS = ASSETS / "fonts"
# Polices acceptées dans le PDF pour chaque police du thème du deck (noms normalisés : minuscules, lettres seules ;
# un nom accepté en couvre les variantes, « arial » couvre Arial Black). Charte Accenture : Arial, Arial Black pour les
# titres, Palatino Linotype pour les sous-titres de couverture ; Liberation Sans et Arimo ont les métriques d'Arial
# (rendu LibreOffice sans Arial).
FONT_ALIASES = {"arial": ("arial", "liberationsans", "arimo", "palatino", "bookantiqua")}
POWERPOINT = Path("/Applications/Microsoft PowerPoint.app")
# Dossier du conteneur sandbox de PowerPoint : il y a accès d'office, sans boîte de dialogue d'autorisation.
PPT_SANDBOX = Path.home() / "Library/Containers/com.microsoft.Powerpoint/Data/Documents/octo_slides_render"


def _unhidden_copy(pptx: Path, out_dir: Path) -> Path:
    """Copie du deck au nom unique, slides masquées rendues visibles (PowerPoint ne les exporte pas en PDF)."""
    copy = out_dir / f"rendu_{pptx.stem}_{time.strftime('%H%M%S')}.pptx"
    with zipfile.ZipFile(pptx) as src, zipfile.ZipFile(copy, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", item.filename):
                data = re.sub(rb'(<p:sld\b[^>]*?)\sshow="(0|false)"', rb"\1", data, count=1)
            dst.writestr(item, data)
    return copy


def _osascript(script):
    return subprocess.run(["osascript", "-e", script], capture_output=True, text=True)


def to_pdf(pptx: Path, out_dir: Path) -> Path:
    """Exporte pptx en PDF (out_dir/<nom du deck>.pdf) via PowerPoint, à partir d'une copie au nom unique. Un échec
    qui n'est pas un blocage (erreur -1728, export vide) est retenté une fois en entier, réouverture comprise ;
    PowerPoint n'est jamais quitté (les présentations de l'utilisateur y sont ouvertes)."""
    try:
        return _to_pdf_once(pptx, out_dir)
    except RuntimeError as e:
        if any(code in str(e) for code in ("-1712", "-9074", "-128")):
            raise  # PowerPoint bloqué par une boîte de dialogue : réessayer ne sert à rien
        time.sleep(5)
        return _to_pdf_once(pptx, out_dir)


def _to_pdf_once(pptx: Path, out_dir: Path) -> Path:
    """Un essai d'export (voir to_pdf)."""
    pdf = out_dir / (pptx.stem + ".pdf")
    pdf.unlink(missing_ok=True)  # un PDF d'un rendu précédent ne doit jamais passer pour le nouveau
    # Copie et export dans le conteneur de PowerPoint : pas de demande d'accès au fichier (sinon un clic par rendu).
    PPT_SANDBOX.mkdir(parents=True, exist_ok=True)
    copy = _unhidden_copy(pptx, PPT_SANDBOX)
    exported = PPT_SANDBOX / (copy.stem + ".pdf")
    exported.unlink(missing_ok=True)
    # La présentation est désignée par son nom, pas « active presentation » : sinon PowerPoint peut exporter un autre
    # deck resté ouvert. On ne ferme que cette copie, jamais les présentations de l'utilisateur.
    # Délai de l'export : 120 s, ou 6 s par slide pour un gros deck (un deck de 40 slides dépasse 120 s).
    delay = max(120, 6 * slide_count(pptx))
    save_script = f'''
    with timeout of {delay} seconds
    tell application "Microsoft PowerPoint"
      save presentation "{copy.name}" in (POSIX file "{exported}") as save as PDF
      close presentation "{copy.name}" saving no
    end tell
    end timeout'''
    try:
        # `open -g -a` plutôt que « open POSIX file » en AppleScript (qui échoue parfois en -9074) : ouverture en
        # arrière-plan, sans voler le focus ; on attend ensuite que la présentation apparaisse sous son nom.
        launched = subprocess.run(["open", "-g", "-a", "Microsoft PowerPoint", str(copy)], capture_output=True,
                                  text=True)
        if launched.returncode != 0:
            raise RuntimeError(f"PowerPoint refuse d'ouvrir la copie de rendu ({launched.stderr.strip()})")
        deadline = time.time() + 120
        while time.time() < deadline:
            seen = _osascript(f'tell application "Microsoft PowerPoint" to exists presentation "{copy.name}"')
            if seen.stdout.strip() == "true":
                break
            time.sleep(2)
        else:
            raise RuntimeError("PowerPoint n'a pas ouvert la copie de rendu en 120 s (-9074) : une boîte de dialogue "
                               "est sans doute ouverte dans PowerPoint ; demander à l'utilisateur de la fermer, puis "
                               "relancer")
        # Le premier export après ouverture expire souvent (PowerPoint froid) : on réessaie.
        error = ""
        for attempt in range(4):
            time.sleep(4 + 2 * attempt)
            saved = _osascript(save_script)
            if saved.returncode == 0 and exported.exists():
                shutil.move(exported, pdf)
                return pdf
            error = saved.stderr.strip()
        busy = "-1712" in error  # AppleEvent expiré : PowerPoint ne répond pas, bloqué par une boîte de dialogue
        raise RuntimeError(f"Export PDF PowerPoint impossible après quatre essais ({error}) : "
                           + ("PowerPoint est bloqué, sans doute par une boîte de dialogue ouverte, ou par le deck "
                              "lui-même ouvert dans PowerPoint ; demander à l'utilisateur de le fermer, puis relancer"
                              if busy else
                              "relancer une fois, puis vérifier qu'aucune boîte de dialogue n'est ouverte"))
    finally:
        # Notre copie seulement, si elle est restée ouverte après un échec ; puis on la supprime.
        _osascript(f'tell application "Microsoft PowerPoint" to if exists presentation "{copy.name}" then '
                   f'close presentation "{copy.name}" saving no')
        for leftover in (copy, copy.with_name("~$" + copy.name)):
            leftover.unlink(missing_ok=True)


def _soffice():
    for name in ("soffice", "libreoffice"):
        if shutil.which(name):
            return shutil.which(name)
    mac = Path("/Applications/LibreOffice.app/Contents/MacOS/soffice")
    return str(mac) if mac.exists() else None

# Le gabarit nomme les graisses comme des familles (« Outfit Light »…) ; assets/fonts n'a que la police variable
# « Outfit » : des alias fontconfig y renvoient ces familles, à la bonne graisse.
WEIGHTS = {"Thin": "thin", "ExtraLight": "extralight", "Light": "light", "Medium": "medium", "SemiBold": "demibold",
           "Bold": "bold", "ExtraBold": "extrabold", "Black": "black"}
FC_ALIAS = """<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
{}</fontconfig>
""".format("".join(f"""  <match target="pattern">
    <test name="family"><string>Outfit {name}</string></test>
    <edit name="family" mode="assign" binding="strong"><string>Outfit</string></edit>
    <edit name="weight" mode="assign" binding="strong"><const>{weight}</const></edit>
  </match>
""" for name, weight in WEIGHTS.items()))

def _install_outfit():
    """Installe les polices du skill (Outfit et ses alias de graisse ; Liberation Sans pour Accenture) pour
    l'utilisateur, pour que LibreOffice ne les remplace pas."""
    target = Path.home() / ("Library/Fonts" if sys.platform == "darwin" else ".fonts")
    target.mkdir(parents=True, exist_ok=True)
    changed = False
    for ttf in ASSETS.glob("fonts*/*.ttf"):
        if not (target / ttf.name).exists():
            shutil.copy(ttf, target / ttf.name)
            changed = True
    conf = Path.home() / ".config" / "fontconfig" / "conf.d" / "60-outfit-weights.conf"
    if sys.platform != "darwin" and not conf.exists():
        conf.parent.mkdir(parents=True, exist_ok=True)
        conf.write_text(FC_ALIAS)
        changed = True
    if changed and shutil.which("fc-cache"):
        subprocess.run(["fc-cache", "-f"], capture_output=True)

def to_pdf_libreoffice(pptx: Path, out_dir: Path, soffice: str) -> Path:
    """Exporte pptx en PDF via LibreOffice (sans interface), à partir d'une copie aux slides masquées visibles."""
    pdf = out_dir / (pptx.stem + ".pdf")
    pdf.unlink(missing_ok=True)
    _install_outfit()
    copy = _unhidden_copy(pptx, out_dir)
    exported = out_dir / (copy.stem + ".pdf")
    profile = tempfile.mkdtemp(prefix="lo_profile_")  # profil neuf : un LibreOffice déjà ouvert ne bloque pas
    try:
        done = subprocess.run([soffice, f"-env:UserInstallation=file://{profile}", "--headless", "--convert-to", "pdf",
                               "--outdir", str(out_dir), str(copy)], capture_output=True, text=True, timeout=300)
        if not exported.exists():
            raise RuntimeError(f"Export PDF LibreOffice impossible : {(done.stderr or done.stdout).strip()}")
        exported.rename(pdf)
        return pdf
    finally:
        copy.unlink(missing_ok=True)
        shutil.rmtree(profile, ignore_errors=True)

def slide_count(pptx: Path) -> int:
    with zipfile.ZipFile(pptx) as z:
        return sum(1 for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n))


def _shapes(shapes):
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from _shapes(sh.shapes)
        else:
            yield sh


def _squash(text):
    # NFKC : PowerPoint écrit les ligatures d'Outfit dans le PDF (« artiﬁcielle » pour « artificielle »).
    return re.sub(r"[\s ­\-‐]", "", unicodedata.normalize("NFKC", text))


def check_fresh(prs, doc):
    """Slides dont le PDF ne contient pas le texte du deck : rendu d'une autre version (cache de PowerPoint)."""
    stale = []
    for i, (slide, page) in enumerate(zip(prs.slides, doc), 1):
        words = {w for sh in _shapes(slide.shapes) if sh.has_text_frame
                 for w in re.findall(r"[A-Za-zÀ-ÿ]{6,}", sh.text_frame.text)}
        if len(words) < 3:
            continue
        rendered = _squash(page.get_text())
        missing = [w for w in words if w not in rendered]
        if len(missing) > 0.3 * len(words):
            stale.append((i, sorted(missing)[:3]))
    return stale


def check_overflow(prs, doc):
    """Texte qui déborde de sa forme dans le rendu réel : on cherche dans le PDF les derniers mots (et les premiers)
    de chaque forme ; s'ils ne sont nulle part dans son cadre, on compare au cadre leur occurrence la plus proche.
    (Les mêmes mots ailleurs sur la slide, « Le gain » dans un titre et dans le corps, ne déclenchent plus d'alerte.)"""
    from pptx.util import Emu
    issues = []
    scale = doc[0].rect.width / Emu(prs.slide_width).inches  # points par pouce
    for i, (slide, page) in enumerate(zip(prs.slides, doc), 1):
        for sh in _shapes(slide.shapes):
            if sh.is_placeholder or not sh.has_text_frame or sh.rotation:
                continue
            words = sh.text_frame.text.replace(" ", " ").split()
            if len(words) < 2:
                continue
            box = fitz.Rect(*(Emu(v).inches * scale for v in (sh.left, sh.top)),
                            *(Emu(a + b).inches * scale for a, b in ((sh.left, sh.width), (sh.top, sh.height))))
            for probe in (" ".join(words[-2:]), " ".join(words[:2])):
                hits = page.search_for(probe)
                if not hits or any(box.contains(h) for h in hits):
                    continue  # absent, ou rendu dans sa forme : les mêmes mots ailleurs sur la slide ne comptent pas
                hit = min(hits, key=lambda r: abs(r.x0 + r.x1 - box.x0 - box.x1) + abs(r.y0 + r.y1 - box.y0 - box.y1))
                if not hit.intersects(box + (-36, -36, 36, 36)):
                    continue  # trouvé ailleurs sur la slide : pas ce texte-là
                over = max(box.x0 - hit.x0, hit.x1 - box.x1, box.y0 - hit.y0, hit.y1 - box.y1)
                if over > TOL:
                    issues.append((i, f"texte qui déborde de sa forme ({over / scale:.2f} pouce) : "
                                      f"« {sh.text_frame.text.strip()[:40]} » ; raccourcir le texte ou agrandir la "
                                      "forme"))
                    break
    return issues


SYMBOLS = set("●•>›»«–—-·.,;:!?%()[]“”\"'  ")


def _norm(font):
    """Nom de police normalisé : sans préfixe de sous-ensemble (« ABCDEF+ »), minuscules, lettres seules."""
    return re.sub(r"[^a-z]", "", font.split("+")[-1].lower())


def deck_fonts(pptx):
    """Polices attendues dans le rendu, normalisées : {« outfit »} pour un deck qui demande Outfit quelque part (OCTO,
    La Grosse Conf : leur thème reste en Arial, Outfit est posé par les layouts), sinon les polices du thème
    ({« arial »} pour Accenture)."""
    found = set()
    with zipfile.ZipFile(pptx) as z:
        xml = [n for n in z.namelist() if re.fullmatch(r"ppt/(slides|slideLayouts|slideMasters)/\w+\.xml", n)]
        if any(b'typeface="Outfit' in z.read(n) for n in xml):
            return {"outfit"}
        for name in z.namelist():
            if re.fullmatch(r"ppt/theme/theme\d+\.xml", name):
                fonts = re.search(rb"<a:fontScheme.*?</a:fontScheme>", z.read(name), re.S)
                if fonts:
                    found |= set(re.findall(rb'<a:(?:majorFont|minorFont)><a:latin typeface="([^"]+)"', fonts.group()))
    return {_norm(f.decode()) for f in found} - {""} or {"outfit"}


def _expected(font, wanted):
    """La police du PDF est-elle l'une des polices demandées (ou un équivalent métrique) ?"""
    name = _norm(font)
    return any(name.startswith(alias) for w in wanted for alias in FONT_ALIASES.get(w, (w,)))


def shape_boxes(prs, page_width):
    """Cadres (en points du PDF) des formes de texte de chaque slide : [[fitz.Rect, ...] par slide], pour rattacher
    une ligne du PDF à sa forme."""
    from pptx.util import Emu
    scale = page_width / Emu(prs.slide_width).inches
    out = []
    for slide in prs.slides:
        boxes = []
        for sh in _shapes(slide.shapes):
            if sh.has_text_frame and sh.text_frame.text.strip() and sh.width is not None:
                boxes.append(fitz.Rect(Emu(sh.left).inches * scale, Emu(sh.top).inches * scale,
                                       Emu(sh.left + sh.width).inches * scale, Emu(sh.top + sh.height).inches * scale))
        out.append(boxes)
    return out


def _owner(rect, boxes):
    """Indice de la plus petite forme qui contient le centre de la ligne, None sinon."""
    centre = fitz.Point((rect.x0 + rect.x1) / 2, (rect.y0 + rect.y1) / 2)
    inside = [k for k, b in enumerate(boxes) if b.contains(centre)]
    return min(inside, key=lambda k: boxes[k].get_area()) if inside else None


def check_pdf(pdf, wanted=("outfit",), boxes=None):
    """Alertes sur le rendu réel : [(numéro de slide, message)]. wanted : polices demandées par le deck
    (deck_fonts) ; toute autre police du PDF est une substitution. boxes : cadres des formes par slide
    (shape_boxes) ; deux lignes d'une même forme ne sont pas signalées comme superposées."""
    issues = []
    main_font = "Arial" if any(w.startswith("arial") for w in wanted) else "Outfit"
    for i, page in enumerate(fitz.open(pdf), 1):
        lines, fonts, outfit = [], {}, False
        for block_no, block in enumerate(page.get_text("dict")["blocks"]):
            for line in block.get("lines", []):
                text = "".join(sp["text"] for sp in line["spans"]).strip()
                if not text:
                    continue
                for sp in line["spans"]:
                    if _expected(sp["font"], wanted):
                        outfit = True
                    elif not set(sp["text"]) <= SYMBOLS and not sp["font"].startswith("Cambria"):  # équations
                        fonts.setdefault(sp["font"], set()).update(sp["text"].strip())
                if abs(line["dir"][1]) > 0.1:
                    continue  # mentions légales verticales du gabarit
                lines.append((block_no, fitz.Rect(line["bbox"]), text))
                if not page.rect.contains(fitz.Rect(line["bbox"])):
                    issues.append((i, f"texte hors de la slide : « {text[:40]} »"))
        for font, chars in sorted(fonts.items()):
            if outfit and len(chars) <= 3:
                issues.append((i, f"caractère(s) absent(s) de {main_font}, rendu(s) en {font} : « {''.join(sorted(chars))} »"
                                  " ; le remplacer (charte : une seule police)"))
            else:
                issues.append((i, f"police de substitution « {font} » : installer {main_font}, puis relancer "
                                  "PowerPoint"))
        # Deux lignes de zones différentes ne se recouvrent pas : un recouvrement net vient de deux zones posées l'une
        # sur l'autre. Dans une même zone, des lignes serrées (interligne de 90 % des titres Accenture) se touchent
        # sans gêner la lecture : pas d'alerte.
        page_boxes = boxes[i - 1] if boxes and i <= len(boxes) else []
        for (ba, ra, ta), (bb, rb, tb) in combinations(lines, 2):
            if ba == bb:
                continue
            if ta == tb and abs(ra.x0 - rb.x0) < 2 and abs(ra.y0 - rb.y0) < 2:
                continue  # même texte au même endroit : l'un cache l'autre (pied de page du masque sous le layout)
            owner = _owner(ra, page_boxes)
            if owner is not None and owner == _owner(rb, page_boxes):
                continue  # même forme : lignes serrées d'un même texte
            inter = ra & rb
            if inter.is_empty:
                continue
            smaller = min(ra.get_area(), rb.get_area()) or 1
            if inter.get_area() / smaller > 0.3:
                issues.append((i, f"textes superposés : « {ta[:30]} » et « {tb[:30]} »"))
    return issues


def main():
    pptx = Path(sys.argv[1]).resolve()
    out_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else pptx.parent / (pptx.stem + "_render")
    out_dir.mkdir(parents=True, exist_ok=True)
    soffice = None
    if not (sys.platform == "darwin" and POWERPOINT.exists()) or os.environ.get("OCTO_RENDER") == "libreoffice":
        soffice = _soffice()
        if soffice is None:
            raise RuntimeError("Ni Microsoft PowerPoint ni LibreOffice : pas de rendu. Installer LibreOffice "
                               "(apt-get install -y libreoffice-impress), ou livrer le .pptx sans relecture visuelle "
                               "et le dire à l'utilisateur")
        print("⚠ Rendu LibreOffice (PowerPoint absent) : approximatif. Coupures de ligne et formes du gabarit peuvent "
              "différer de PowerPoint et de Google Slides ; ne corriger que les défauts nets, pas un mot qui passe à "
              "la ligne ni un trait décoratif du gabarit")
    pdf = to_pdf_libreoffice(pptx, out_dir, soffice) if soffice else to_pdf(pptx, out_dir)
    doc = fitz.open(pdf)
    n_pages, n_slides = len(doc), slide_count(pptx)
    if n_pages != n_slides:
        raise RuntimeError(f"Le PDF a {n_pages} pages pour {n_slides} slides : PowerPoint a exporté un autre deck")
    try:
        from pptx import Presentation
        prs = Presentation(str(pptx))
    except ImportError:
        prs = None
        print("python-pptx absent : contrôles de fraîcheur et de débordement sautés (ajouter --with python-pptx)")
    if prs is not None:
        stale = check_fresh(prs, doc)
        if stale:
            detail = " ; ".join(f"slide {i} (manque {', '.join(m)})" for i, m in stale)
            raise RuntimeError(f"Rendu périmé : le PDF ne contient pas le texte du deck ({detail}). PowerPoint a "
                               "exporté une version en cache : fermer le deck dans PowerPoint et relancer")
    pages = []
    for i, page in enumerate(doc, 1):
        png = out_dir / f"slide_{i:02d}.png"
        page.get_pixmap(dpi=150).save(png)  # assez fin pour relire un alignement ou un débordement
        pages.append(png)
    for old in out_dir.glob("slide_*.png"):  # slides d'un rendu précédent plus long
        if old not in pages:
            old.unlink()
    w, h = (round(v * 110 / 150) for v in Image.open(pages[0]).size)
    for old in out_dir.glob("sheet_*.png"):
        old.unlink()
    for k in range(0, len(pages), 4):
        sheet = Image.new("RGB", (w * 2, h * 2), "white")
        for j, png in enumerate(pages[k:k + 4]):
            sheet.paste(Image.open(png).resize((w, h)), ((j % 2) * w, (j // 2) * h))
        sheet.save(out_dir / f"sheet_{k // 4 + 1}.png")
    print(f"{len(pages)} slides -> {out_dir}")
    boxes = shape_boxes(prs, doc[0].rect.width) if prs is not None else None
    issues = check_pdf(pdf, deck_fonts(pptx), boxes) + (check_overflow(prs, doc) if prs is not None else [])
    for i, message in sorted(issues):
        print(f"⚠ slide {i} : {message}")
    print(f"{len(issues)} alerte(s) sur le rendu" if issues else "Rendu : aucune alerte")


if __name__ == "__main__":
    main()
