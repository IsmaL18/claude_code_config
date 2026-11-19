"""Contrôle géométrique et de lecture des slides : ce que l'œil d'un relecteur voit et qu'une planche de rendu cache.

Appelé par Deck.save() sur les slides créées ; utilisable seul sur n'importe quel deck :

    uv run --with python-pptx python octo_lint.py deck.pptx [--gslides] [--grosse-conf | --accenture]

--gslides (Deck(target="gslides") à l'enregistrement) : texte mesuré 5 % plus large, et signale ce que Google Slides
ne rend pas à l'import (liste GSLIDES : dégradé, ombre, graphique natif, SmartArt, SVG, réduction auto du texte...).

Contrôles (pouces) :
- bords presque alignés : deux blocs dont les bords gauches, droits, hauts ou bas diffèrent de 0,01 à 0,06 (une
  rangée de hauteurs presque égales, une colonne qui déborde de celle du dessus) ;
- écarts irréguliers : dans une suite d'au moins trois blocs de même rangée (ou colonne), des écarts qui diffèrent
  de 0,01 à 0,08 ;
- chevauchement partiel de deux blocs (des blocs emboîtés partagent un bord, ils ne se chevauchent pas) ;
- deux textes posés l'un sur l'autre (d'après le texte mesuré, ancrage compris) ;
- zone de texte posée dans un bloc mais dont le texte mesuré sort du bloc (un chiffre clé et sa légende dans une
  boîte trop basse) ;
- forme sur la pastille du numéro de page, ou hors des marges de la slide ;
- flèche dont un bout ne touche aucune forme ;
- deux flèches qui partent (ou arrivent) de points voisins mais distincts : elles se croisent, une fourche
  (Deck.fork / join) les fait partir du même point ;
- flèche à coude cranté : deux tronçons dont les arrondis se touchent sans être centrés au même point ;
- flèche sans tige : pointe posée seule entre deux boîtes trop proches, ou collée à la barre d'une jonction ;
- trait de liaison pointillé en biais (ni horizontal ni vertical) ;
- texte sous 6 pt ;
- bloc à moitié vide : le contenu s'arrête haut et laisse en bas un vide plus du double de la marge du haut ;
- lead gras d'une boîte coupé sur deux lignes, mot court seul en fin de paragraphe (texte de 8 pt et plus) ;
- image dont un coin sort de l'arrondi du bloc où elle est posée ;
- contraste du texte sur son fond sous le seuil de la matrice de charte.md (4,5:1, 3:1 en gros caractères).
Un « bloc » est une forme visible (fond ou contour) d'au moins 0,3 x 0,3 pouce : les étiquettes, pictos, puces et
zones de texte posées dans un bloc n'entrent pas dans les contrôles d'alignement.
"""
import math
import re
import sys
from itertools import combinations

from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu

from octo_layout import LINE_HEIGHT, _length, _wrap_runs, wrap_runs

EPS = 0.01            # en dessous : bords considérés comme alignés
NEAR = 0.06           # jusqu'à : bords « presque » alignés, à aligner
GAP_NEAR = 0.08       # écarts d'une même suite qui diffèrent de moins : à égaliser
TOUCH = 0.15          # distance maximale entre un bout de flèche et une forme
SPLIT = 0.25          # deux bouts de flèche plus proches que ça, sans être confondus : départ dédoublé
DEFAULT_NAME = re.compile(r"^[A-Za-z][A-Za-z ]* \d+$")  # « Rounded Rectangle 12 » : nom donné par python-pptx
PAGE_NUMBER = (9.2, 5.05, 9.75, 5.45)
# Géométrie du masque, par charte : taille de la slide, pastille du numéro de page ou pied de page à ne pas recouvrir
# (x1, y1, x2, y2), marges (gauche, droite, bas) au-delà desquelles un bloc qui n'est pas à fond perdu sort des marges.
GEOMETRY = {
    "octo": ((10, 5.625), PAGE_NUMBER, (0.3, 9.6, 5.35)),
    "grosse_conf": ((10, 5.625), PAGE_NUMBER, (0.3, 9.6, 5.35)),
    "accenture": ((13.333, 7.5), (9.05, 7.0, 12.95, 7.4), (0.4, 12.95, 7.0)),  # copyright et numéro de page
}
# « Flèche x1,y1 → x2,y2 | px,py » : les deux bouts, puis le point d'où part le dernier tronçon (decks récents).
ARROW = re.compile(r"^Flèche ([-\d.]+),([-\d.]+) → ([-\d.]+),([-\d.]+)(?: \| ([-\d.]+),([-\d.]+))?$")
# Posés à cheval sur une carte ou une fenêtre, exprès : pas des blocs. OCTO : médaillon, puce cible ; grosse conf :
# ombre décalée, onglet et ascenseur de fenêtre, cercles emboîtés.
ORNAMENTS = ("Médaillon", "Puce cible", "Ombre de fenêtre", "Ombre de carte", "Onglet de fenêtre", "Ascenseur",
             "Cercle de cible")
MIN_SHAFT = 0.08      # tige visible minimale derrière la pointe d'une flèche (pouces)
HEAD_REACH = 3.56     # longueur de la pointe le long de la tige, en épaisseurs (chevron du modèle 10)


def text_extent(sh):
    """(hauteur en pouces, nombre de lignes) du texte d'une forme, mesuré comme PowerPoint : police Outfit, marges,
    retraits de puce, interlignes et espaces avant. None si non mesurable (taille héritée du layout, texte réduit
    automatiquement)."""
    tf = sh.text_frame
    body_pr = tf._txBody.bodyPr
    if body_pr.find(qn("a:normAutofit")) is not None:
        return None
    no_wrap = body_pr.get("wrap") == "none"
    inner = Emu(sh.width - tf.margin_left - tf.margin_right).inches
    needed, lines = Emu(tf.margin_top + tf.margin_bottom).inches, 0
    for p in tf.paragraphs:
        sizes = [r.font.size.pt for r in p.runs if r.font.size]
        if len(sizes) != len(p.runs):
            return None
        if not p.runs:
            continue
        pPr = p._p.pPr
        indent = Emu(int(pPr.get("marL", 0))).inches if pPr is not None else 0
        spacing = p.line_spacing if isinstance(p.line_spacing, float) else 1.0
        runs = [(r.text, bool(r.font.bold), r.font.size.pt, r.font.name) for r in p.runs]
        heights = [max(sizes)] if no_wrap else wrap_runs(runs, inner - indent)
        lines += len(heights)
        needed += sum(heights) * LINE_HEIGHT * spacing / 72 + (p.space_before.pt if p.space_before else 0) / 72
    return needed, lines


def _text_rect(sh):
    """Rectangle réellement occupé par le texte d'une zone (hauteur mesurée, position selon l'ancrage)."""
    measured = text_extent(sh)
    x, y, w, h = _box(sh)
    if measured is None:
        return None
    needed = measured[0]
    tf = sh.text_frame
    anchor = tf.vertical_anchor
    if anchor == MSO_ANCHOR.MIDDLE:
        y += (h - needed) / 2
    elif anchor == MSO_ANCHOR.BOTTOM:
        y += h - needed
    # Largeur réellement encrée : la plus longue ligne, plafonnée à la largeur utile, placée selon l'alignement.
    margins = Emu(tf.margin_left + tf.margin_right).inches
    ink = min(w - margins, max(sum(_length(r.text, r.font.size.pt, bool(r.font.bold), r.font.name) for r in p.runs)
                               for p in tf.paragraphs)) + margins
    align = tf.paragraphs[0].alignment
    x += (w - ink) / 2 if align == PP_ALIGN.CENTER else (w - ink) if align == PP_ALIGN.RIGHT else 0
    return x, y, ink, needed


def _text_overlaps(slide, skip):
    """Deux textes posés l'un sur l'autre, d'après le texte mesuré (sans attendre le rendu PowerPoint)."""
    rects = []
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip() and not sh.is_placeholder and not sh.rotation \
                and sh.text_frame._txBody not in skip:
            r = _text_rect(sh)
            if r:
                tf = sh.text_frame
                ml, mr = Emu(tf.margin_left).inches, Emu(tf.margin_right).inches
                mt = Emu(tf.margin_top).inches
                rects.append((sh, (r[0] + ml, r[1] + mt, r[2] - ml - mr, r[3] - 2 * mt)))
    issues = []
    for (a, (ax, ay, aw, ah)), (b, (bx, by, bw, bh)) in combinations(rects, 2):
        ow = min(ax + aw, bx + bw) - max(ax, bx)
        oh = min(ay + ah, by + bh) - max(ay, by)
        if ow > 0.05 and oh > 0.04 and ow * oh > 0.3 * min(aw * ah, bw * bh):
            issues.append(f"textes superposés : {_label(a)} et {_label(b)}")
    return issues


def _box(sh):
    return tuple(Emu(v).inches for v in (sh.left, sh.top, sh.width, sh.height))


def _extent(sh):
    """Rectangle réellement couvert par une forme : rotation comprise (une barre verticale de flèche est un
    rectangle horizontal tourné de 90°), et pour un groupe, l'union de ses éléments (python-pptx calcule le cadre
    d'un groupe sans tenir compte de la rotation de ses éléments)."""
    if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
        boxes = [_extent(c) for c in sh.shapes]
        if not boxes:
            return _box(sh)
        x1, y1 = min(b[0] for b in boxes), min(b[1] for b in boxes)
        x2, y2 = max(b[0] + b[2] for b in boxes), max(b[1] + b[3] for b in boxes)
        # Les éléments d'un groupe sont dans son repère (chOff, chExt) : un groupe emprunté à un modèle et déplacé
        # (ModeleDeck.borrow) garde le repère d'origine. On ramène l'union dans le repère de la slide.
        xfrm = sh._element.find(qn("p:grpSpPr")).find(qn("a:xfrm"))
        ch_off, ch_ext = xfrm.find(qn("a:chOff")), xfrm.find(qn("a:chExt"))
        if ch_off is not None and ch_ext is not None and int(ch_ext.get("cx")) and int(ch_ext.get("cy")):
            ox, oy, ow, oh = _box(sh)
            cx0, cy0 = Emu(int(ch_off.get("x"))).inches, Emu(int(ch_off.get("y"))).inches
            sx, sy = ow / Emu(int(ch_ext.get("cx"))).inches, oh / Emu(int(ch_ext.get("cy"))).inches
            x1, x2 = ox + (x1 - cx0) * sx, ox + (x2 - cx0) * sx
            y1, y2 = oy + (y1 - cy0) * sy, oy + (y2 - cy0) * sy
        return x1, y1, x2 - x1, y2 - y1
    x, y, w, h = _box(sh)
    rot = math.radians(getattr(sh, "rotation", 0) or 0)
    if abs(math.sin(rot)) < 1e-6:
        return x, y, w, h
    cw = abs(w * math.cos(rot)) + abs(h * math.sin(rot))
    ch = abs(w * math.sin(rot)) + abs(h * math.cos(rot))
    return x + (w - cw) / 2, y + (h - ch) / 2, cw, ch


def _visible(sh):
    """Forme dessinée : fond ou contour visible (une zone de texte nue ne l'est pas)."""
    spPr = sh._element.find(qn("p:spPr"))
    if spPr is None:
        return False
    fill = spPr.find(qn("a:solidFill")) is not None or spPr.find(qn("a:blipFill")) is not None
    ln = spPr.find(qn("a:ln"))
    line = ln is not None and ln.find(qn("a:noFill")) is None
    if not fill and not line and sh.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
        style = sh._element.find(qn("p:style"))  # contour hérité du style de forme
        line = style is not None and ln is None
    return fill or line


def _label(sh):
    x, y, w, h = _box(sh)
    text = sh.text_frame.text.strip().split("\n")[0][:30] if sh.has_text_frame else ""
    if text:
        return f"« {text} »"
    if sh.name and not DEFAULT_NAME.match(sh.name) and not ARROW.match(sh.name):
        return f"{sh.name} en ({x:.2f} ; {y:.2f})"  # nom posé par les helpers (« Bloc « Titre » »)
    return f"forme en ({x:.2f} ; {y:.2f})"


def _blocks(slide, skip):
    out = []
    for sh in slide.shapes:
        if sh.is_placeholder or sh._element in skip or sh.rotation or ARROW.match(sh.name) \
                or sh.name.startswith(ORNAMENTS):
            continue
        if sh.shape_type in (MSO_SHAPE_TYPE.AUTO_SHAPE, MSO_SHAPE_TYPE.FREEFORM) and _visible(sh):
            x, y, w, h = _box(sh)
            if w >= 0.3 and h >= 0.3:
                out.append(sh)
    return out


def _near_aligned(blocks):
    issues = []
    sides = {"gauches": lambda b: b[0], "droits": lambda b: b[0] + b[2], "hauts": lambda b: b[1],
             "bas": lambda b: b[1] + b[3]}
    for side, edge in sides.items():
        seen = set()
        for a, b in combinations(blocks, 2):
            ba, bb = _box(a), _box(b)
            center = 1 if side in ("hauts", "bas") else 0  # deux blocs centrés sur la même ligne : voulu
            if abs(ba[center] + ba[center + 2] / 2 - bb[center] - bb[center + 2] / 2) <= EPS and \
                    abs(ba[center + 2] - bb[center + 2]) > EPS:
                continue
            ea, eb = edge(ba), edge(bb)
            d = abs(ea - eb)
            key = (round(min(ea, eb), 2), round(max(ea, eb), 2))
            if EPS < d < NEAR and key not in seen:
                seen.add(key)
                issues.append(f"bords {side} presque alignés ({ea:.2f} et {eb:.2f}, écart {d:.2f}) : {_label(a)} et "
                              f"{_label(b)} ; découper une même zone (Frame.cols / rows / grid) pour les aligner")
    return issues


def _uneven_gaps(blocks):
    issues = []
    for axis, (pos, size, other, other_size) in {"rangée": (0, 2, 1, 3), "colonne": (1, 3, 0, 2)}.items():
        groups = {}
        for b in blocks:
            box = _box(b)
            groups.setdefault((round(box[other], 2), round(box[other_size], 2)), []).append(box)
        for row in groups.values():
            if len(row) < 3:
                continue
            row.sort(key=lambda r: r[pos])
            gaps = [b[pos] - (a[pos] + a[size]) for a, b in zip(row, row[1:])]
            if all(-EPS <= g < 1.0 for g in gaps) and EPS < max(gaps) - min(gaps) < GAP_NEAR:
                issues.append(f"écarts irréguliers dans une {axis} de {len(row)} blocs ("
                              + ", ".join(f"{g:.2f}" for g in gaps) + ") : même écart partout (gap=)")
    return issues


def _overlaps(blocks):
    issues = []
    for a, b in combinations(blocks, 2):
        (ax, ay, aw, ah), (bx, by, bw, bh) = _box(a), _box(b)
        ow = min(ax + aw, bx + bw) - max(ax, bx)
        oh = min(ay + ah, by + bh) - max(ay, by)
        if ow <= 0.03 or oh <= 0.03:
            continue  # disjoints, ou emboîtés le long d'un bord
        inside = lambda x, y, w, h, X, Y, W, H: x >= X - EPS and y >= Y - EPS and x + w <= X + W + EPS \
            and y + h <= Y + H + EPS  # noqa: E731
        if inside(ax, ay, aw, ah, bx, by, bw, bh) or inside(bx, by, bw, bh, ax, ay, aw, ah):
            continue  # un bloc posé dans un autre
        issues.append(f"chevauchement partiel ({ow:.2f} x {oh:.2f}) : {_label(a)} et {_label(b)} ; emboîter "
                      "(bords partagés) ou séparer")
    return issues


def _text_outside_block(slide, blocks, skip):
    """Zone de texte nue (sans fond ni contour) qui commence dans un bloc et dont le texte mesuré en sort : le
    texte paraît déborder du bloc, alors que la forme du bloc et la zone de texte sont chacune sans alerte."""
    issues = []
    for sh in slide.shapes:
        if sh.is_placeholder or _visible(sh) or not sh.has_text_frame or not sh.text_frame.text.strip() \
                or sh.rotation or sh.text_frame._txBody in skip:
            continue
        r = _text_rect(sh)
        if r is None:
            continue
        tf = sh.text_frame
        ml, mt = Emu(tf.margin_left).inches, Emu(tf.margin_top).inches
        tx, ty, tw, th = r[0] + ml, r[1] + mt, r[2] - 2 * ml, r[3] - 2 * mt  # encre, marges retirées
        hosts = [b for b in blocks if _box(b)[0] - EPS <= tx <= _box(b)[0] + _box(b)[2] - 0.1
                 and _box(b)[1] - EPS <= ty <= _box(b)[1] + _box(b)[3] - 0.1]
        if not hosts:
            continue
        bx, by, bw, bh = _box(min(hosts, key=lambda b: _box(b)[2] * _box(b)[3]))  # le bloc le plus proche
        over = max(tx + tw - (bx + bw), ty + th - (by + bh))
        if over > -0.01:  # l'encre doit rester dans le bloc : un texte qui touche le contour déborde à l'œil
            issues.append(f"texte qui sort de son bloc ({over:.2f} pouce) : {_label(sh)} ; agrandir le bloc, "
                          "raccourcir le texte ou réduire sa taille")
    return issues


def _fmt(v):
    return f"{v:g}".replace(".", ",")


def _out_of_bounds(slide, skip, charte="octo"):
    issues = []
    (sw, sh_), (px1, py1, px2, py2), (left, right, bottom) = GEOMETRY.get(charte, GEOMETRY["octo"])
    for sh in slide.shapes:
        if sh.is_placeholder or sh._element in skip:
            continue
        x, y, w, h = _extent(sh)
        if not _visible(sh) and sh.has_text_frame and sh.text_frame.text.strip():
            x, y, w, h = _text_rect(sh) or (x, y, w, h)  # zone de texte nue : seul le texte compte
        if x < px2 and x + w > px1 + EPS and y < py2 and y + h > py1 + EPS and (w > 0.05 or h > 0.05):
            issues.append(f"{_label(sh)} recouvre la pastille du numéro de page (coin bas droit) : arrêter la zone "
                          f"en x = {_fmt(px1)} ou en y = {_fmt(py1)}")
        if x < -0.02 or y < -0.02 or x + w > sw + 0.02 or y + h > sh_ + 0.02:
            issues.append(f"{_label(sh)} sort de la slide (x {x:.2f} → {x + w:.2f}, y {y:.2f} → {y + h:.2f})")
            continue
        bleed = x <= 0.02 or x + w >= sw - 0.02 or y + h >= sh_ - 0.025  # aplat posé à fond perdu : voulu
        if not bleed and (x + w > right or y + h > bottom or x < left):
            issues.append(f"{_label(sh)} sort des marges (x {x:.2f} → {x + w:.2f}, y {y:.2f} → {y + h:.2f})")
    return issues


def _dist(px, py, box):
    x, y, w, h = box
    dx = max(x - px, 0, px - (x + w))
    dy = max(y - py, 0, py - (y + h))
    return (dx * dx + dy * dy) ** 0.5


def _arrows(slide):
    issues = []
    targets = [sh for sh in slide.shapes if not ARROW.match(sh.name)]  # un filet (axe, couloir) est une cible
    ends = []
    for sh in slide.shapes:
        m = ARROW.match(sh.name)
        if not m:
            continue
        ends.append(tuple(map(float, m.groups()[:4])))
    for sh in slide.shapes:  # liens secondaires : connecteurs pointillés à pointe
        if sh.shape_type == MSO_SHAPE_TYPE.LINE and sh._element.find(".//" + qn("a:tailEnd")) is not None:
            ends.append(tuple(Emu(v).inches for v in (sh.begin_x, sh.begin_y, sh.end_x, sh.end_y)))
    for x1, y1, x2, y2 in ends:
        for (px, py), end in (((x1, y1), "départ"), ((x2, y2), "arrivée")):
            own = lambda t: t.shape_type == MSO_SHAPE_TYPE.LINE and \
                {round(Emu(v).inches, 2) for v in (t.begin_x, t.begin_y, t.end_x, t.end_y)} >= \
                {round(v, 2) for v in (x1, y1, x2, y2)}  # noqa: E731 (le connecteur lui-même)
            if not any(_dist(px, py, _box(t)) <= TOUCH for t in targets if not own(t)):
                issues.append(f"flèche sans forme à son {end} ({px:.2f} ; {py:.2f}) : la tracer avec connect(a, b)")
    for k, end in ((0, "partent"), (2, "arrivent")):
        points = sorted({(round(e[k], 3), round(e[k + 1], 3)) for e in ends})
        for (ax, ay), (bx, by) in combinations(points, 2):
            if 0.01 < math.dist((ax, ay), (bx, by)) < SPLIT:
                issues.append(f"deux flèches {end} de points voisins ({ax:.2f} ; {ay:.2f}) et ({bx:.2f} ; {by:.2f}) : "
                              "elles se croisent ; une seule fourche (fork / join) ou deux bords différents")
    return issues


def _arrow_shafts(slide):
    """Flèche sans tige : le dernier tronçon est à peine plus long que la pointe, qui paraît posée seule entre deux
    boîtes trop proches, ou collée à la barre d'une jonction dont le tronc final est trop court."""
    issues, seen = [], set()
    for sh in slide.shapes:
        m = ARROW.match(sh.name) if sh.shape_type == MSO_SHAPE_TYPE.GROUP else None
        if not m or m.group(5) is None:
            continue
        x1, y1, ex, ey, px, py = map(float, m.groups())
        if (ex, ey, px, py) in seen:
            continue  # branches d'une jonction : un seul tronc final, une seule alerte
        seen.add((ex, ey, px, py))
        t = max(_box(bar)[3] for bar in sh.shapes)
        shaft = math.dist((px, py), (ex, ey)) - HEAD_REACH * t
        if shaft < MIN_SHAFT:
            joined = (px, py) != (x1, y1)
            issues.append(f"flèche sans tige en ({ex:.2f} ; {ey:.2f}) : {max(shaft, 0):.2f} pouce derrière la pointe ; "
                          + ("allonger le tronc final (trunk de join ≥ 0,35, écart de 0,8 pouce) ou le dernier "
                             "tronçon" if joined else "écarter les deux boîtes (0,45 pouce au moins)"))
    return issues


def _oblique_leaders(slide):
    """Trait de liaison en biais : un filet pointillé droit (repère vers sa boîte, piste vers des blocs) ni
    horizontal ni vertical. Les liaisons se tracent à l'horizontale, à la verticale ou en angle droit (deux filets) ;
    si l'alignement est impossible, on relie par un numéro. Les arêtes pleines d'un schéma oblique par nature
    (neurone, réseau) ne sont pas concernées."""
    issues = []
    for sh in slide.shapes:
        if sh.shape_type != MSO_SHAPE_TYPE.LINE:
            continue
        geom = sh._element.find(".//" + qn("a:prstGeom"))
        dash = sh._element.find(".//" + qn("a:prstDash"))
        if geom is None or geom.get("prst") not in ("line", "straightConnector1") or dash is None \
                or dash.get("val") in (None, "solid"):
            continue
        x1, y1, x2, y2 = (Emu(v).inches for v in (sh.begin_x, sh.begin_y, sh.end_x, sh.end_y))
        if abs(x2 - x1) > 0.03 and abs(y2 - y1) > 0.03 and math.dist((x1, y1), (x2, y2)) > 0.2:
            issues.append(f"trait pointillé en biais de ({x1:.2f} ; {y1:.2f}) à ({x2:.2f} ; {y2:.2f}) : une liaison "
                          "est horizontale, verticale ou en angle droit (deux rule) ; sinon relier par un numéro")
    return issues


def _small_text(slide, skip):
    sizes = []
    for sh in slide.shapes:
        if sh.has_text_frame and sh._element not in skip and sh.text_frame._txBody not in skip:
            sizes += [r.font.size.pt for p in sh.text_frame.paragraphs for r in p.runs
                      if r.font.size and r.text.strip()]
    small = [s for s in sizes if s < 6]
    return [f"{len(small)} passage(s) de texte sous 6 pt ({min(small):g} pt) : illisible projeté"] if small else []


def _arrow_joints(slide):
    """Coude cranté : dans une flèche, deux tronçons dont les arrondis se touchent sans être centrés sur le même
    point. Le coude montre un cran, une fourche se pince à son point de partage (flèches d'une ancienne version
    d'arrow_path : il suffit de régénérer le deck)."""
    issues = []
    for sh in slide.shapes:
        if sh.shape_type != MSO_SHAPE_TYPE.GROUP or not ARROW.match(sh.name) \
                or any(bar.shape_type == MSO_SHAPE_TYPE.LINE for bar in sh.shapes):  # lien pointillé : des filets
            continue
        caps, t = [], 0
        for k, bar in enumerate(sh.shapes):
            x, y, w, h = _box(bar)
            rot = math.radians(bar.rotation or 0)
            reach = max(w - h, 0) / 2  # du centre de la barre au centre de chacun de ses arrondis
            ux, uy = math.cos(rot) * reach, math.sin(rot) * reach
            caps += [(k, (x + w / 2 + ux, y + h / 2 + uy)), (k, (x + w / 2 - ux, y + h / 2 - uy))]
            t = max(t, h)
        if any(a != b and 0.005 < math.dist(p, q) <= 1.05 * t for (a, p), (b, q) in combinations(caps, 2)):
            issues.append(f"flèche à coude cranté en ({_box(sh)[0]:.2f} ; {_box(sh)[1]:.2f}) : tracée par une "
                          "ancienne version d'arrow_path, régénérer le deck")
    return issues


def _runs(p):
    return [(r.text, bool(r.font.bold), r.font.size.pt) for r in p.runs if r.font.size and r.text]


def _inner_width(sh):
    """Largeur utile du texte d'une forme. Dans un rectangle arrondi (Deck.box), PowerPoint rentre la zone de texte
    de 0,29 rayon de chaque côté (géométrie prédéfinie roundRect) : sans ce retrait, un lead qui passe à la mesure
    se coupe au rendu. Dans un triangle, la zone de texte n'occupe que la moitié centrale de la largeur."""
    tf = sh.text_frame
    inner = Emu(sh.width - tf.margin_left - tf.margin_right).inches
    geom = sh._element.find(".//" + qn("a:prstGeom"))
    margins = Emu(tf.margin_left + tf.margin_right).inches
    if geom is not None and geom.get("prst") == "triangle":  # zone de texte de la géométrie : la moitié centrale
        return Emu(sh.width).inches / 2 - margins
    if geom is not None and geom.get("prst") == "trapezoid":
        # Géométrie OOXML : retrait de chaque côté = largeur / 3 x adj / adj max (adj max = 0,5 x largeur / petit côté).
        w, ss = Emu(sh.width).inches, min(Emu(sh.width).inches, Emu(sh.height).inches)
        adj = min(sh.adjustments[0] if len(sh.adjustments) else 0.25, 0.5 * w / ss)
        return w - 2 * (w / 3) * adj / (0.5 * w / ss) - margins
    if geom is not None and geom.get("prst") == "roundRect":
        adj = sh.adjustments[0] if len(sh.adjustments) else 0.16667
        inner -= 2 * 0.29289 * adj * min(Emu(sh.width).inches, Emu(sh.height).inches)
    return inner


def _split_lead(slide, skip):
    """Lead gras d'une boîte (« **Avant de pousser**\\nun hook… ») coupé sur deux lignes : le titre se lit mal et la
    boîte paraît trop étroite. La règle de style.md : élargir la colonne qui coupe un titre en deux."""
    issues = []
    for sh in slide.shapes:
        if sh.is_placeholder or not _visible(sh) or not sh.has_text_frame or sh.text_frame._txBody in skip:
            continue
        paras = [p for p in sh.text_frame.paragraphs if p.text.strip()]
        if len(paras) < 2:
            continue
        lead = paras[0]
        runs = _runs(lead)
        if not runs or not all(r.font.bold for r in lead.runs if r.text.strip()) or len(lead.text.split()) < 2:
            continue
        if len(_wrap_runs(runs, _inner_width(sh))) > 1:
            issues.append(f"lead gras coupé sur deux lignes : {_label(sh)} ; élargir la colonne (part plus grande "
                          "dans cols) ou raccourcir le lead")
    return issues


def _orphans(slide, skip):
    """Mot court seul sur la dernière ligne d'un paragraphe (« changé par / PR », « la marge du / mois ») : la
    ligne paraît vide et le paragraphe mal coupé."""
    issues = []
    for sh in slide.shapes:
        if sh.is_placeholder or not sh.has_text_frame or sh.rotation or sh.text_frame._txBody in skip:
            continue
        if sh.text_frame._txBody.bodyPr.get("wrap") == "none":
            continue
        for p in sh.text_frame.paragraphs:
            runs = _runs(p)
            if not runs or max(r[2] for r in runs) < 8:
                continue  # vue d'ensemble en 6 à 7 pt : densité assumée
            pPr = p._p.pPr
            indent = Emu(int(pPr.get("marL", 0))).inches if pPr is not None else 0
            width = _inner_width(sh) - indent
            lines = _wrap_runs(runs, width)
            last = lines[-1][0].strip()
            # Un mot seul : court (« PR », « mois »), ou perdu sur une ligne large (« entreprendre. » sur 8 pouces).
            # Une étiquette de deux ou trois mots (« mise à / jour ») s'empile exprès : seules les phrases comptent.
            short = len(last.strip(".,;:!?»)")) <= 6 or _length(last, max(r[2] for r in runs), False) < 0.2 * width
            if len(lines) > 1 and len(p.text.split()) >= 5 and " " not in last and short:
                issues.append(f"mot seul en fin de paragraphe (« {last} ») : {_label(sh)} ; reformuler ou élargir")
                break
    return issues


def _starts_in(r, box):
    """Le rectangle r commence dans box : son centre horizontal et son bord haut sont dedans."""
    bx, by, bw, bh = box
    return bx - EPS <= r[0] + r[2] / 2 <= bx + bw + EPS and by - EPS <= r[1] <= by + bh


# Rayon de chaque coin (tl, tr, br, bl) d'une forme arrondie, avant retournement : ajustements par défaut, puis lus
# dans le XML ; rayon = ajustement / 100 000 x petit côté.
ROUNDED = {
    "roundRect": ((16667,), lambda a: (a[0],) * 4),
    "round1Rect": ((16667,), lambda a: (0, a[0], 0, 0)),
    "round2DiagRect": ((16667, 0), lambda a: (a[0], a[1], a[0], a[1])),
    "round2SameRect": ((16667, 0), lambda a: (a[0], a[0], a[1], a[1])),
}


def _corner_radii(sh):
    """{(sx, sy): rayon} des coins arrondis d'une forme, sx / sy = -1 (gauche / haut) ou +1. Vide si la forme n'a
    pas de coin arrondi ou si elle est tournée."""
    geom = sh._element.find(qn("p:spPr") + "/" + qn("a:prstGeom"))
    if geom is None or geom.get("prst") not in ROUNDED or sh.rotation:
        return {}
    defaults, corners = ROUNDED[geom.get("prst")]
    adj = list(defaults)
    for k, gd in enumerate(geom.iter(qn("a:gd"))):
        if k < len(adj) and gd.get("fmla", "").startswith("val "):
            adj[k] = int(gd.get("fmla")[4:])
    xfrm = sh._element.find(qn("p:spPr") + "/" + qn("a:xfrm"))
    fh = -1 if xfrm is not None and xfrm.get("flipH") == "1" else 1
    fv = -1 if xfrm is not None and xfrm.get("flipV") == "1" else 1
    _, _, w, h = _box(sh)
    side = min(w, h)
    return {(sx * fh, sy * fv): min(a, 50000) / 100000 * side
            for (sx, sy), a in zip(((-1, -1), (1, -1), (1, 1), (-1, 1)), corners(adj)) if a > 0}


def _image_corners(slide):
    """Image (capture, photo) posée dans un bloc à coins arrondis, dont un coin sort de l'arrondi : avec une marge
    de moins de 0,29 rayon, le coin carré de l'image dépasse de l'arc du bloc."""
    issues = []
    rounded = [(sh, _corner_radii(sh)) for sh in slide.shapes if sh.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE]
    for pic in slide.shapes:
        if pic.shape_type != MSO_SHAPE_TYPE.PICTURE or pic.rotation:
            continue
        geom = pic._element.find(qn("p:spPr") + "/" + qn("a:prstGeom"))
        if geom is not None and geom.get("prst") != "rect":
            continue  # image déjà découpée en forme (photo())
        px, py, pw, ph = _box(pic)
        for sh, radii in rounded:
            x, y, w, h = _box(sh)
            if not radii or not (x - EPS <= px and y - EPS <= py and px + pw <= x + w + EPS and py + ph <= y + h + EPS):
                continue
            for (sx, sy), r in radii.items():
                cx, cy = (x + r if sx < 0 else x + w - r), (y + r if sy < 0 else y + h - r)
                qx, qy = (px if sx < 0 else px + pw), (py if sy < 0 else py + ph)
                if (qx - cx) * sx > 0 and (qy - cy) * sy > 0 and math.dist((qx, qy), (cx, cy)) > r + 0.005:
                    need = r * (1 - 1 / math.sqrt(2))
                    issues.append(f"image qui sort du coin arrondi de son bloc en ({qx:.2f} ; {qy:.2f}) : marge "
                                  f"d'au moins {need + 0.02:.2f} pouce dans un bloc de rayon {r:.2f}, "
                                  "ou rayon plus petit")
    return issues


def _half_empty(slide, blocks, skip):
    """Bloc dont le contenu (texte, picto, blocs posés dedans) s'arrête haut et laisse un vide en bas nettement
    plus grand que la marge du haut : le bloc paraît à moitié vide (style.md : ne pas étirer un bloc pour occuper
    la place)."""
    issues = []
    texts = []
    for sh in slide.shapes:
        if sh.is_placeholder or sh.rotation or (sh.has_text_frame and sh.text_frame._txBody in skip):
            continue
        if sh.has_text_frame and sh.text_frame.text.strip():
            r = _text_rect(sh)
            if r:
                mt = Emu(sh.text_frame.margin_top).inches
                texts.append((sh, (r[0], r[1] + mt, r[2], r[3] - 2 * mt)))
        elif sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
            texts.append((sh, _box(sh)))
    for b in blocks:
        bx, by, bw, bh = box = _box(b)
        content = [r for sh, r in texts if sh is b or (not _visible(sh) and _starts_in(r, box))]
        content += [_box(o) for o in blocks
                    if o is not b and _starts_in(_box(o), box) and _box(o)[2] * _box(o)[3] < bw * bh]
        if not content:
            continue
        top = min(r[1] for r in content) - by
        bottom = by + bh - max(r[1] + r[3] for r in content)
        if bottom > max(0.3, 0.25 * bh) and bottom > 2 * max(top, 0):
            issues.append(f"bloc à moitié vide ({bottom:.2f} pouce vide en bas, {max(top, 0):.2f} en haut) : "
                          f"{_label(b)} ; réduire la hauteur du bloc au texte (text_height) ou y répartir le contenu")
    return issues


CONTRAST_MIN, CONTRAST_LARGE = 4.5, 3.0  # WCAG AA, comme la matrice de charte.md (gros : 18 pt, ou 14 pt gras)
_SCHEME_ALIAS = {"bg1": "lt1", "tx1": "dk1", "bg2": "lt2", "tx2": "dk2"}
_THEMES = {}  # couleurs du thème, par master


def run_rgb(run):
    """Couleur RVB écrite sur un run (« 0E2356 »), None si elle est héritée ou de thème. Lue dans le XML : lire
    run.font.color dans python-pptx pose un remplissage plein vide sur le run, que PowerPoint rend en noir."""
    rpr = run._r.find(qn("a:rPr"))
    fill = rpr.find(qn("a:solidFill")) if rpr is not None else None
    srgb = fill.find(qn("a:srgbClr")) if fill is not None else None
    return srgb.get("val").upper() if srgb is not None else None


def _luminance(hex_):
    c = [int(hex_[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(fg, bg):
    """Rapport de contraste WCAG entre deux couleurs hexadécimales (« 00D2DD », « 0E2356 ») : 8,1 pour le turquoise
    sur marine, 1,9 sur blanc."""
    hi, lo = sorted((_luminance(fg), _luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def _theme(slide):
    """Couleurs du thème du master de la slide : {"dk1": "0E2356", "lt1": "FFFFFF", ...}."""
    from lxml import etree
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    part = slide.slide_layout.slide_master.part
    if part not in _THEMES:
        scheme = etree.fromstring(part.part_related_by(RT.THEME).blob).find(".//" + qn("a:clrScheme"))
        _THEMES[part] = {el.tag.split("}")[1]: el[0].get("val") or el[0].get("lastClr")
                         for el in (scheme if scheme is not None else []) if len(el)}
    return _THEMES[part]


def _fill_color(container, theme):
    """Couleur (hex) d'un a:solidFill sous container (spPr, bgPr) ; None si absent ou modulé (teinte calculée)."""
    if container is None:
        return None
    fill = container.find(qn("a:solidFill"))
    if fill is None or not len(fill) or len(fill[0]):
        return None
    clr = fill[0]
    if clr.tag == qn("a:srgbClr"):
        return clr.get("val").upper()
    if clr.tag == qn("a:schemeClr"):
        val = theme.get(_SCHEME_ALIAS.get(clr.get("val"), clr.get("val")))
        return val.upper() if val else None
    return None


def _filled(sh):
    """Forme qui cache ce qu'il y a dessous : fond plein, dégradé, motif ou image, ou groupe (contenu inconnu)."""
    if sh.shape_type in (MSO_SHAPE_TYPE.PICTURE, MSO_SHAPE_TYPE.GROUP):
        return True
    spPr = sh._element.find(qn("p:spPr"))
    return spPr is not None and any(spPr.find(qn(f"a:{kind}")) is not None
                                    for kind in ("solidFill", "gradFill", "pattFill", "blipFill"))


def _background(slide, theme):
    """Couleur du fond de la slide (slide, puis layout, puis master) ; None si image, dégradé ou inconnue."""
    for part in (slide, slide.slide_layout, slide.slide_layout.slide_master):
        bg = part._element.find(qn("p:cSld")).find(qn("p:bg"))
        if bg is not None:
            return _fill_color(bg.find(qn("p:bgPr")), theme)
    return "FFFFFF"


# Remèdes proposés par le contrôle de contraste, par charte : (fond clair, fond foncé, fichier de la charte).
HINTS = {
    "octo": ("fond clair : texte marine #0E2356, #3E4F78 en secondaire",
             "fond foncé : texte blanc, #CFD3DD en secondaire", "matrice des contrastes, charte.md"),
    "grosse_conf": ("fond clair ou rose : texte anthracite #38383F ; le rouge #FF0042 seulement au-dessus de 18 pt "
                    "ou en gras au-dessus de 14 pt",
                    "fond anthracite : texte blanc ou rose #FF80A1 (jamais rouge) ; fond rouge : blanc au-dessus de "
                    "18 pt ou en gras au-dessus de 14 pt", "accessibilité, charte_grosse_conf.md"),
    "accenture": ("fond clair : texte noir #000000, accent violet #A100FF ou plus foncé (jamais #BE82FF ni #DCAFFF "
                  "en texte)", "fond violet foncé ou noir : texte blanc, #DCAFFF en secondaire",
                  "contrastes, charte_accenture.md"),
}


def _inherited(sh, p, theme):
    """(couleur hex, taille en pt) du texte d'un paragraphe de placeholder sans couleur ni taille écrites : celles de
    son niveau dans le placeholder de la slide, puis du layout, puis du masque, puis du style de texte du masque
    (titre ou corps). None pour ce qui n'est pas résolu (texte hors placeholder, couleur modulée)."""
    if not sh.is_placeholder:
        return None, None
    pPr = p._p.pPr
    level = f"a:lvl{int(pPr.get('lvl', 0)) + 1 if pPr is not None else 1}pPr"
    node, chain = sh, []
    while node is not None:
        chain.append(node._element.find(qn("p:txBody") + "/" + qn("a:lstStyle")))
        node = getattr(node, "_base_placeholder", None)
    styles = sh.part.slide.slide_layout.slide_master._element.find(qn("p:txStyles")) \
        if hasattr(sh.part, "slide") else None
    if styles is not None:
        kind = "p:titleStyle" if str(sh.placeholder_format.type).split(".")[-1].split(" ")[0] in (
            "TITLE", "CENTER_TITLE") else "p:bodyStyle"
        chain.append(styles.find(qn(kind)))
    color = size = None
    for lst in chain:
        lvl = lst.find(qn(level)) if lst is not None else None
        rpr = lvl.find(qn("a:defRPr")) if lvl is not None else None
        if rpr is None:
            continue
        if color is None and rpr.find(qn("a:solidFill")) is not None:
            color = _fill_color(rpr, theme) or "?"
        if size is None and rpr.get("sz"):
            size = int(rpr.get("sz")) / 100
    return (None if color == "?" else color), size


def _contrasts(slide, skip, charte="octo"):
    """Texte dont le contraste avec son fond est sous le seuil de la charte (matrice de charte.md, WCAG AA) : 4,5:1,
    3:1 pour les gros caractères. charte : « octo », « grosse_conf » ou « accenture » (remèdes proposés, seuils
    identiques). Le fond est celui de la forme du texte, sinon la forme pleine posée dessous, sinon
    le fond de la slide. Le point final turquoise (titre héros, accroche) est une exception de la charte. Un texte de
    placeholder sans couleur ni taille écrites prend celles héritées du layout ou du masque (_inherited)."""
    theme = _theme(slide)
    shapes = list(slide.shapes)
    # Sous les formes de la slide, celles du layout : le cadre blanc du layout focus, posé sur un fond #3E4F78.
    decor = [o for o in slide.slide_layout.shapes if not o.is_placeholder]
    issues = []
    # Formes de texte, groupes compris (étiquettes d'un Gantt de modèle) : (forme, formes posées dessous, fond par
    # défaut). Dans un groupe, les formes du dessous sont ses sœurs (mêmes coordonnées), et le fond par défaut celui
    # qui est sous le groupe.
    entries = []

    def under_color(sh, below, default):
        x, y, w, h = _box(sh)
        under = [o for o in below if _filled(o) and _dist(x + w / 2, y + h / 2, _extent(o)) == 0]
        return _fill_color(under[-1]._element.find(qn("p:spPr")), theme) if under else default

    def collect(container, context, default):
        for i, sh in enumerate(container):
            below = context + container[:i]
            if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                collect(list(sh.shapes), [], under_color(sh, [o for o in below if o.shape_type != MSO_SHAPE_TYPE.GROUP],
                                                         default))
            else:
                entries.append((sh, below, default))

    collect(shapes, decor, _background(slide, theme))
    for sh, below, default in entries:
        if not sh.has_text_frame or not sh.text_frame.text.strip() or sh.text_frame._txBody in skip:
            continue
        if _filled(sh):
            bg = _fill_color(sh._element.find(qn("p:spPr")), theme)
        else:
            bg = under_color(sh, below, default)
        if bg is None:
            continue  # fond en dégradé, image ou groupe : contraste non mesurable
        worst = None
        for p in sh.text_frame.paragraphs:
            inherited, inherited_size = _inherited(sh, p, theme)
            for r in p.runs:
                text = r.text.strip()
                size = r.font.size.pt if r.font.size else inherited_size
                if not text or not size or not re.search(r"\w", text):
                    continue  # ponctuation seule : le point final turquoise de la charte
                rpr = r._r.find(qn("a:rPr"))
                fg = run_rgb(r) or (_fill_color(rpr, theme) if rpr is not None else None) or inherited
                if fg is None:
                    continue  # couleur non résolue (modulée, hors placeholder)
                bold = bool(r.font.bold)
                need = CONTRAST_LARGE if size >= 18 or (bold and size >= 14) else CONTRAST_MIN
                ratio = contrast(fg, bg)
                if ratio < need and (worst is None or ratio < worst[0]):
                    worst = (ratio, need, fg, text)
        if worst:
            ratio, need, fg, text = worst
            light, dark, source = HINTS[charte]
            hint = light if _luminance(bg) > 0.18 else dark
            issues.append(f"contraste insuffisant {ratio:.1f}:1 (minimum {need:g}:1) : texte #{fg} sur #{bg}, "
                          f"« {text[:30]} » ; {hint} ({source})")
    return issues


def _shrinks(sh):
    """Texte réduit automatiquement par PowerPoint (normAutofit), sur la forme ou hérité de son layout : il rapetisse
    au lieu de couper un mot."""
    node = sh
    while node is not None:
        if node.has_text_frame and node.text_frame._txBody.bodyPr.find(qn("a:normAutofit")) is not None:
            return True
        node = getattr(node, "_base_placeholder", None)
    return False


def _default_size(sh, p, default):
    """Taille (pt) d'un paragraphe de forme sans taille écrite : celle de son niveau dans le style de la forme, sinon
    la taille par défaut de la présentation (default)."""
    pPr = p._p.pPr
    level = f"a:lvl{int(pPr.get('lvl', 0)) + 1 if pPr is not None else 1}pPr"
    lst = sh._element.find(qn("p:txBody") + "/" + qn("a:lstStyle"))
    rpr = lst.find(qn(level) + "/" + qn("a:defRPr")) if lst is not None else None
    if pPr is not None and pPr.find(qn("a:defRPr")) is not None and pPr.find(qn("a:defRPr")).get("sz"):
        return int(pPr.find(qn("a:defRPr")).get("sz")) / 100
    return int(rpr.get("sz")) / 100 if rpr is not None and rpr.get("sz") else default


def _long_words(slide, skip):
    """Mot plus large que la zone de son texte : PowerPoint le coupe en deux (« Volum / e »), ce que la mesure ligne
    à ligne, qui ne coupe qu'aux espaces, ne voit pas. La taille d'un texte qui ne l'écrit pas est héritée (layout,
    masque, style de la forme, taille par défaut de la présentation : 18 pt)."""
    issues = []
    theme = _theme(slide)
    pres = slide.part.package.presentation_part._element.find(qn("p:defaultTextStyle"))
    sz = pres.find(qn("a:lvl1pPr") + "/" + qn("a:defRPr")) if pres is not None else None
    default = int(sz.get("sz")) / 100 if sz is not None and sz.get("sz") else 18

    def flat(container):
        for sh in container:
            if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                yield from flat(sh.shapes)
            else:
                yield sh

    for sh in flat(slide.shapes):
        if not sh.has_text_frame or sh.text_frame._txBody in skip or sh._element in skip:
            continue
        if sh.text_frame._txBody.bodyPr.get("wrap") == "none" or _shrinks(sh):
            continue
        width = _inner_width(sh)
        for p in sh.text_frame.paragraphs:
            inherited = _inherited(sh, p, theme)[1] if sh.is_placeholder else _default_size(sh, p, default)
            for r in p.runs:
                size = r.font.size.pt if r.font.size else inherited
                if not size:
                    continue
                for word in r.text.split():
                    if _length(word, size, bool(r.font.bold), r.font.name) > width + 0.02:
                        issues.append(f"mot plus large que sa zone, coupé en deux au rendu : « {word} » dans "
                                      f"{_label(sh)} ; élargir la zone ou réduire la taille")
    return issues


def check_slide(slide, skip=frozenset(), charte="octo"):
    """Liste des problèmes géométriques d'une slide. skip : éléments XML à ignorer (formes de modèles laissées
    telles quelles). charte : « octo », « grosse_conf » ou « accenture » (géométrie du masque, remèdes du contrôle
    de contraste)."""
    blocks = _blocks(slide, skip)
    return (_near_aligned(blocks) + _uneven_gaps(blocks) + _overlaps(blocks) + _text_overlaps(slide, skip)
            + _text_outside_block(slide, blocks, skip) + _half_empty(slide, blocks, skip)
            + _out_of_bounds(slide, skip, charte) + _arrows(slide) + _arrow_joints(slide) + _arrow_shafts(slide)
            + _oblique_leaders(slide) + _small_text(slide, skip)
            + _split_lead(slide, skip) + _orphans(slide, skip) + _contrasts(slide, skip, charte)
            + _long_words(slide, skip)
            + _image_corners(slide))


# Ce que Google Slides ne rend pas comme PowerPoint à l'import d'un .pptx : (motif XPath, problème, remède). Liste
# tirée de la documentation et des retours connus de l'import, pas d'un test sur chaque version de Slides.
GSLIDES = [
    ("p:spPr/a:gradFill", "dégradé (Slides n'a pas de dégradé de forme : aplat ou image)", "aplat de la charte"),
    ("p:spPr/a:effectLst/*", "ombre ou effet (lueur, bords adoucis, reflet : retirés ou simplifiés)",
     "supprimer l'effet"),
    ("p:spPr/a:scene3d|p:spPr/a:sp3d", "effet 3D ou biseau (perdu)", "supprimer l'effet"),
    ("p:style/a:effectRef[@idx!='0'][not(../../p:spPr/a:effectLst)]",
     "ombre héritée du thème (rendue autrement dans Slides)", "shape.shadow.inherit = False"),
    (".//a:graphicData[contains(@uri, '/chart')]", "graphique natif (image figée dans Slides)",
     "schéma en formes, ou image du graphique"),
    (".//a:graphicData[contains(@uri, '/diagram')]", "SmartArt (aplati en image)", "formes et flèches du skill"),
    (".//*[local-name()='svgBlip']", "image SVG (Slides garde la copie PNG de repli)", "PNG en bonne définition"),
    (".//a:bodyPr/a:normAutofit", "texte réduit automatiquement (Slides ne réduit pas : il déborde)",
     "taille fixe et zone à la hauteur du texte"),
    (".//a:bodyPr[@numCol > 1]", "zone de texte en colonnes (une seule colonne dans Slides)", "une zone par colonne"),
    (".//a:bodyPr/a:prstTxWarp", "texte déformé WordArt (perdu)", "texte droit"),
    (".//a:rPr[@cap='all' or @cap='small']|.//a:defRPr[@cap='all' or @cap='small']",
     "capitales par attribut (Slides affiche le texte tel que tapé)", "pas de capitales (charte)"),
    (".//a:rPr[@spc and @spc!='0']", "espacement des lettres (ignoré)", "espacement normal"),
    ("p:spPr/a:prstGeom[starts-with(@prst, 'bent') or starts-with(@prst, 'curved')]",
     "connecteur coudé ou courbe (Slides replace le coude à sa façon)", "arrow_path, ou connect(..., dash=True)"),
    (".//a:videoFile|.//a:audioFile|.//*[local-name()='media']", "vidéo ou son intégré (non lu par Slides)",
     "lien YouTube ou Drive"),
]


def gslides_issues(slide, skip=frozenset()):
    """Ce qui ne passera pas à l'import dans Google Slides, regroupé par problème. skip : comme check_slide (le texte
    d'un modèle OCTO laissé tel quel n'est pas signalé pour ses attributs de texte)."""
    def shapes(container):
        for sh in container:
            yield sh
            if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                yield from shapes(sh.shapes)
    found = {}
    for sh in shapes(slide.shapes):
        el = sh._element
        if el in skip or (sh.has_text_frame and sh.text_frame._txBody in skip):
            continue
        group = sh.shape_type == MSO_SHAPE_TYPE.GROUP
        for pattern, problem, fix in GSLIDES:
            if not (group and pattern.startswith(".//")) and el.xpath(pattern):  # un groupe : ses formes suffisent
                found.setdefault((problem, fix), []).append(_label(sh))
    return [f"Google Slides : {problem}, {len(names)} forme(s) ({', '.join(names[:3])}"
            f"{'…' if len(names) > 3 else ''}) ; {fix}" for (problem, fix), names in found.items()]


def main():
    from pptx import Presentation
    import octo_layout
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    gslides = "--gslides" in sys.argv
    # Géométrie du masque, police de mesure et remèdes du contrôle de contraste
    charte = "grosse_conf" if "--grosse-conf" in sys.argv else "accenture" if "--accenture" in sys.argv else "octo"
    octo_layout.use_font("Arial" if charte == "accenture" else "Outfit")
    if gslides:
        octo_layout.INK = octo_layout.GSLIDES_INK
    total = 0
    for i, slide in enumerate(Presentation(args[0]).slides, 1):
        for issue in check_slide(slide, charte=charte) + (gslides_issues(slide) if gslides else []):
            total += 1
            print(f"⚠ slide {i} : {issue}")
    print(f"{total} alerte(s) de mise en page")


if __name__ == "__main__":
    main()
