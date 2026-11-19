"""Fichier de retours d'un deck (references/retours.md) : le texte de chaque slide, repéré [slide.élément], que
l'utilisateur corrige sur place, avec ses consignes « → » et ses remarques de design ; puis la lecture de ses retours.

    uv run --with python-pptx python retours.py write deck.pptx <dossier du rendu> [retours.md]
    uv run --with python-pptx python retours.py diff retours.md deck.pptx

write : écrit retours.md à côté du deck (captures du rendu en tête de chaque slide). Un retours.md déjà présent est
remplacé s'il est resté intact, archivé en retours_v1.md, retours_v2.md… s'il a été rempli : rien ne se perd.
diff : compare le fichier rempli au texte du deck et liste les textes modifiés, les consignes, les remarques de design
et les remarques libres, à reporter dans build.py.
"""
import hashlib
import os
import re
import sys
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Emu

from octo_lint import run_rgb

TURQ = "00D2DD"
CONTENEURS = ("Bloc", "Panneau", "Périmètre", "Capsule", "Fenêtre")  # noms donnés aux formes par octo_slides
VIDE = {"", "-", "n.a", "na", "n/a", "ras", "rien", "ok"}  # puces laissées vides ou « rien à signaler »
EMPREINTE = re.compile(r"<!-- empreinte : (\w+) ; deck : (\w+) -->\s*$")
ITEM = re.compile(r"^- \[(\d+)\.(\d+)\] ([^:]+?) : (.*)$")

ENTETE = """# Retours : {deck}

> [!info]- Mode d'emploi : trois gestes, et ce qui convient reste tel quel
> **1. Corriger un texte** : réécrivez-le après les deux-points, sans toucher au repère.
> `- [1.9] Texte : Sans données désensibilisées, aucune expérimentation.`
> devient `- [1.9] Texte : Sans données anonymisées, aucune expérimentation possible.`
>
> **2. Confier une consigne à l'agent** : une ligne `→` sous l'élément.
> `- [1.12] Texte : Dans vos standards technologiques…`
> `  → précise que l'environnement servira aussi aux devs de la DSI`
>
> **3. Remarque de design** : une puce sous « Design », avec un repère ou une position.
> `- [1.20] pastille trop voyante, plutôt une info discrète`
> `- bandeau du bas : élargir les cas d'usage`
>
> Notations : `/` retour à la ligne · `**gras**` · `==mot-clé==` (couleur d'accent, sur fond foncé) · `→ Claude :` notes de \
l'agent, à garder ou effacer.

## Tout le deck
-
"""


# ---------------------------------------------------------------- extraction du texte
def _runs_md(par):
    """Paragraphe en markdown du skill : segments de même style fusionnés ; gras omis si tout le paragraphe l'est."""
    segs = []
    for r in par.runs:
        color = run_rgb(r)  # lue sans toucher au run (python-pptx y poserait un remplissage vide)
        style = "turq" if color == TURQ else ("bold" if r.font.bold else "")
        if segs and (segs[-1][0] == style or not r.text.strip()):
            segs[-1][1] += r.text
        else:
            segs.append([style, r.text])
    tout_gras = all(s in ("bold", "turq") for s, _ in segs)
    out = []
    for style, txt in segs:
        core = txt.strip()
        if not core or not style or (style == "bold" and tout_gras):
            out.append(txt)
            continue
        mark = "==" if style == "turq" else "**"
        lead, trail = txt[:len(txt) - len(txt.lstrip())], txt[len(txt.rstrip()):]
        out.append(f"{lead}{mark}{core}{mark}{trail}")
    return "".join(out)


def _text_md(shape):
    return " / ".join(p for p in (_runs_md(p) for p in shape.text_frame.paragraphs) if p.strip())


def _shapes(shapes):
    """Formes d'une slide, groupes dépliés."""
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from _shapes(sh.shapes)
        else:
            yield sh


def _inside(inner, outer, tol=Emu(91440)):  # 0,1 pouce : une étiquette posée à cheval sur le bord compte dedans
    return (inner.left >= outer.left - tol and inner.top >= outer.top - tol
            and inner.left + inner.width <= outer.left + outer.width + tol
            and inner.top + inner.height <= outer.top + outer.height + tol)


def _is_title(sh):
    return sh.is_placeholder and sh.placeholder_format.type in (1, 3)


def extract(pptx_path):
    """Slides du deck : [(titre, [(repère, rôle, texte)])], dans l'ordre de lecture, groupés par bloc."""
    slides = []
    for i, slide in enumerate(Presentation(pptx_path).slides, 1):
        shapes = list(_shapes(slide.shapes))
        conteneurs = [sh for sh in shapes if sh.name.startswith(CONTENEURS)
                      and not (sh.has_text_frame and sh.text_frame.text.strip())]
        textes = [sh for sh in shapes  # un glyphe seul (« i » d'une note, numéro de pastille) n'est pas à relire
                  if sh.has_text_frame and len(sh.text_frame.text.strip()) > 1]
        textes.sort(key=lambda sh: (not sh.is_placeholder, sh.is_placeholder and not _is_title(sh)))
        titre = next((sh.text_frame.text for sh in textes if _is_title(sh)), "")
        items, titres_vus, prec = [], set(), None
        for sh in textes:
            groupe = None
            if sh.is_placeholder:
                role = "Titre" if _is_title(sh) else "Sous-titre"
            else:
                parents = [c for c in conteneurs if _inside(sh, c)]
                groupe = min(parents, key=lambda c: c.width * c.height) if parents else None
                if groupe is None:
                    role = "Texte"
                elif sh.shape_type != MSO_SHAPE_TYPE.TEXT_BOX:  # pilule posée sur le bloc
                    role = "Étiquette"
                elif id(groupe) in titres_vus:
                    role = "Texte"
                else:
                    role = "Titre de bloc"
                    titres_vus.add(id(groupe))
            items.append((groupe is not prec and bool(items), role, _text_md(sh)))
            prec = groupe
        slides.append((titre, [(f"{i}.{n}", role, txt, sep) for n, (sep, role, txt) in enumerate(items, 1)]))
    return slides


def _empreinte(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def _deck_empreinte(slides):
    return _empreinte(repr([(t, [(r, ro, tx) for r, ro, tx, _ in it]) for t, it in slides]))


# ---------------------------------------------------------------- write
def render_md(pptx_path, render_dir, out_dir):
    slides = extract(pptx_path)
    rel = os.path.relpath(render_dir, out_dir)
    lines = [ENTETE.format(deck=Path(pptx_path).stem)]
    for i, (titre, items) in enumerate(slides, 1):
        lines += [f"\n## Slide {i} · {titre}", f"![]({rel}/slide_{i:02d}.png)", "", "### Texte"]
        for ref, role, txt, sep in items:
            if sep:
                lines.append("")
            lines.append(f"- [{ref}] {role} : {txt}")
        lines += ["", "### Design", "-", "", "### Remarques", "-"]
    body = "\n".join(lines) + "\n"
    return body, _deck_empreinte(slides)


def write(pptx_path, render_dir, out=None):
    out = Path(out or Path(pptx_path).with_name("retours.md"))
    body, deck = render_md(pptx_path, render_dir, out.parent)
    if out.exists():
        old = out.read_text(encoding="utf-8")
        m = EMPREINTE.search(old)
        intact = m and _empreinte(old[:m.start()]) == m.group(1)
        if not intact:
            n = 1
            while (archive := out.with_name(f"{out.stem}_v{n}.md")).exists():
                n += 1
            out.rename(archive)
            print(f"{out.name} rempli : archivé en {archive.name}")
    out.write_text(body + f"<!-- empreinte : {_empreinte(body)} ; deck : {deck} -->\n", encoding="utf-8")
    print(f"{out} : {body.count(chr(10) + '- [')} éléments")


# ---------------------------------------------------------------- diff
def _parse(text):
    """Fichier de retours → textes {repère: (rôle, texte)}, consignes [(repère ou section, consigne)],
    remarques {section: [lignes]}."""
    textes, consignes, remarques = {}, [], {}
    slide, section, dernier = "Tout le deck", None, None
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)  # commentaires : empreinte, ancien mode d'emploi
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(">"):  # mode d'emploi
            continue
        if raw.startswith("## "):
            slide = "Tout le deck" if raw.startswith("## Tout le deck") else raw[3:].split(" · ")[0]
            section, dernier = ("Remarques" if slide == "Tout le deck" else None), None
            continue
        if raw.startswith("### "):
            section, dernier = raw[4:].strip(), None
            continue
        if re.match(r"^(→|-+>)", line):
            consigne = re.sub(r"^(→|-+>)\s*", "", line)
            if consigne and not consigne.startswith("Claude :"):
                consignes.append((dernier or slide, consigne))
            continue
        m = ITEM.match(line)
        if m and section == "Texte":
            dernier = f"{m.group(1)}.{m.group(2)}"
            textes[dernier] = (m.group(3), m.group(4).strip())
            continue
        if section in ("Design", "Remarques") and line.lstrip("- ").strip().lower() not in VIDE:
            remarques.setdefault(f"{slide} · {section}", []).append(line.lstrip("- ").strip())
    return textes, consignes, remarques


def diff(retours_path, pptx_path):
    text = Path(retours_path).read_text(encoding="utf-8")
    slides = extract(pptx_path)
    m = EMPREINTE.search(text)
    if m and m.group(2) != _deck_empreinte(slides):
        print("⚠ le deck a changé depuis l'écriture du fichier de retours : les repères peuvent ne plus correspondre.\n")
    origine = {ref: (role, txt) for _, items in slides for ref, role, txt, _ in items}
    textes, consignes, remarques = _parse(text)
    modifies = [(ref, origine[ref][0], origine[ref][1], txt) for ref, (_, txt) in textes.items()
                if ref in origine and " ".join(txt.split()) != " ".join(origine[ref][1].split())]
    absents = [ref for ref in origine if ref not in textes]
    print(f"## Textes modifiés ({len(modifies)})")
    for ref, role, avant, apres in modifies:
        print(f"- [{ref}] {role}\n  avant : {avant}\n  après : {apres}")
    print(f"\n## Consignes ({len(consignes)})")
    for ou, c in consignes:
        print(f"- [{ou}] → {c}" if re.match(r"\d+\.\d+$", ou) else f"- {ou} → {c}")
    print(f"\n## Remarques ({sum(len(v) for v in remarques.values())})")
    for ou, lignes in remarques.items():
        for ligne in lignes:
            print(f"- {ou} : {ligne}")
    if absents:
        print(f"\n## Repères effacés du fichier ({len(absents)}) : texte supprimé ou repère abîmé, à vérifier")
        for ref in absents:
            print(f"- [{ref}] {origine[ref][0]} : {origine[ref][1]}")


if __name__ == "__main__":
    cmd, *args = sys.argv[1:] or ["--help"]
    if cmd == "write" and len(args) in (2, 3):
        write(*args)
    elif cmd == "diff" and len(args) == 2:
        diff(*args)
    else:
        print(__doc__)
        sys.exit(1)
