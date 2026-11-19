"""Base commune des decks du skill : texte balisé, formes de base, flèches, images, contrôle de mise en page et
enregistrement. Elle ne connaît aucune charte : chaque deck (Deck pour OCTO dans octo_slides.py, GrosseConfDeck pour
La Grosse Conf dans grosse_conf_slides.py, AccentureDeck pour Accenture dans accenture_slides.py) en hérite et fixe
ses couleurs, sa police, son template et sa bibliothèque de visuels dans ses attributs de classe. Les univers ne
partagent que ce fichier, octo_layout et octo_lint.

Markup des textes : **gras**, ==mot-clé== (accent de la charte, seulement sur fond foncé), \n retour à la ligne,
"- " en début de ligne pour une puce, "> " pour une puce chevron. Coordonnées en pouces (slide de 10 x 5,625 pour
OCTO et La Grosse Conf, 13,333 x 7,5 pour Accenture).
"""
import io
import json
import math
import re
from pathlib import Path

from lxml import etree
from PIL import Image as PILImage
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE, MSO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

import octo_layout
from octo_layout import lines_of, text_height, text_width, typo
from octo_lint import check_slide, gslides_issues, text_extent

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS = SKILL_DIR / "assets"
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Outfit"
AUTO = "auto"  # valeur par défaut d'une couleur : celle de la charte du deck (attributs de classe)


def find_visual(name, dirs):
    """Fichier d'un visuel par son nom, cherché dans les dossiers dirs seulement, puis dans les planches
    assets/atlas/ du zip claude.ai (limité à 200 fichiers, sans archive imbriquée : les visuels y sont regroupés en
    grandes images). Jamais en dehors de dirs : un deck ne pose pas les visuels d'une autre charte."""
    for folder in dirs:
        path = folder / f"{name}.png"
        if path.exists():
            return str(path)
    atlas = ASSETS / "atlas" / "index.json"
    if atlas.exists():
        index = json.loads(atlas.read_text())
        for folder in dirs:
            entry = index.get(f"{folder.relative_to(ASSETS).as_posix()}/{name}")
            if entry:
                x, y, w, h = entry["box"]
                buf = io.BytesIO()
                PILImage.open(ASSETS / "atlas" / entry["sheet"]).crop((x, y, x + w, y + h)).save(buf, "PNG")
                buf.seek(0)
                return buf
    raise FileNotFoundError(f"Visuel « {name} » introuvable dans {', '.join(d.name for d in dirs)} (voir l'index "
                            "des visuels du skill)")


_TOKEN = re.compile(r"(\*\*.+?\*\*|==.+?==)")


def _rect(obj):
    """(x, y, w, h) en pouces d'une forme python-pptx ou d'un rectangle déjà en pouces (tuple ou Frame)."""
    if isinstance(obj, tuple):
        return tuple(obj)
    return tuple(Emu(v).inches for v in (obj.left, obj.top, obj.width, obj.height))


def _runs(text):
    """Découpe un texte balisé en (texte, gras, turquoise), typographie appliquée (espaces insécables : typo)."""
    out = []
    for part in _TOKEN.split(typo(text)):
        if not part:
            continue
        if part.startswith("**"):
            inner = part[2:-2]
            nested = inner.startswith("==") and inner.endswith("==")  # **==mot==** : mot-clé
            out.append((inner[2:-2] if nested else inner, True, nested))
        elif part.startswith("=="):
            out.append((part[2:-2], True, True))
        else:
            out.append((part, False, False))
    return out


def _shape_texts(shapes):
    """Textes d'une liste de formes, groupes et tableaux compris, dans l'ordre du deck."""
    texts = []
    for shape in shapes:
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            texts += _shape_texts(shape.shapes)
        elif shape.has_text_frame and shape.text_frame.text.strip():
            texts.append(shape.text_frame.text.strip())
        elif shape.has_table:
            for row in shape.table.rows:
                texts.append(" | ".join(cell.text.strip() for cell in row.cells))
    return texts


def extract_text(path):
    """Texte d'un deck source (slides + notes), en markdown, pour en tirer la matière d'un nouveau deck."""
    parts = []
    for i, slide in enumerate(Presentation(str(path)).slides, 1):
        parts.append(f"## Slide {i}")
        parts += _shape_texts(slide.shapes)
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame.text.strip():
            parts.append(f"Notes : {slide.notes_slide.notes_text_frame.text.strip()}")
        parts.append("")
    return "\n".join(parts)


class BaseDeck:
    """Deck sans charte : à sous-classer. Attributs de classe à fixer par chaque charte :
    TEMPLATE (template .pptx), VISUAL_DIRS (bibliothèque de visuels, cherchée par picto()), TEXT (texte courant),
    LINE (contours), ACCENT (mot-clé ==…== sur fond foncé), POINT (point final d'un titre), BULLET (puces, hex),
    FLOW et LOOP (flèches de flux et boucles de retour), CHEVRON (chevron de transition), RULE (filets fins),
    PHOTO_SHAPE (découpe par défaut d'une photo), CHARTE (remèdes du contrôle de mise en page, octo_lint.HINTS)
    et CHARTE_FILE (fichier de la charte, cité par les messages)."""
    TEMPLATE = None
    VISUAL_DIRS = []
    TEXT = LINE = FLOW = None
    ACCENT = POINT = LOOP = CHEVRON = RULE = None
    BULLET = None
    PHOTO_SHAPE = "arrondi"
    CHARTE = None
    CHARTE_FILE = None
    FONT = FONT  # police du texte posé par les helpers, et police de mesure (octo_layout.use_font)
    LANG = "fr-FR"  # langue du texte (correcteur d'orthographe) ; hors français, pas de typographie française
    MISE_EN_PAGE = "references/mise_en_page.md §4"  # règles de mise en page citées par save()

    def __init__(self, template=None, target="pptx"):
        """target="gslides" : deck destiné à Google Slides. Le texte est mesuré 5 % plus large (marge pour les retours
        à la ligne de Slides) et save() signale ce que Slides ne rend pas (dégradé, ombre, graphique natif...)."""
        if target not in ("pptx", "gslides"):
            raise ValueError(f"target : « pptx » ou « gslides », pas « {target} »")
        self.target = target
        octo_layout.INK = octo_layout.GSLIDES_INK if target == "gslides" else 1.0
        octo_layout.use_font(self.FONT)
        octo_layout.FRENCH = self.LANG.startswith("fr")
        self.prs = Presentation(str(template or self.TEMPLATE))
        self._layouts = {l.name: l for m in self.prs.slide_masters for l in m.slide_layouts}
        self.warnings = []
        self.image_slots = []  # (identifiant de slide, sujet) : images à insérer, listées à l'enregistrement
        self._as_is = set()  # corps de texte copiés tels quels d'un modèle : pas de contrôle de débordement

    def _visual(self, name):
        """Fichier d'un visuel de la bibliothèque du deck (VISUAL_DIRS) par son nom ; FileNotFoundError sinon."""
        return find_visual(name, self.VISUAL_DIRS)

    def _number(self, slide):
        """Numéro de la slide dans le deck livré."""
        return self.prs.slides.index(slide) + 1

    def _warn(self, shape, message):
        """Alerte de mise en page, affichée tout de suite et rappelée à l'enregistrement."""
        try:
            where = f"slide {self._number(shape.part.slide)}"
        except (AttributeError, ValueError):
            where = "slide ?"
        self.warnings.append(f"{where} : {message}")
        print(f"⚠ {where} : {message}")

    def _check_fits(self):
        """Alerte pour chaque forme dont le texte, mesuré avec la police Outfit comme PowerPoint (marges, retraits de
        puce, interlignes et espaces avant compris), dépasse la hauteur. Ne sont pas contrôlés : les placeholders,
        dont la taille vient du layout (titres : slide()), le texte d'un modèle OCTO laissé tel quel, le texte sur une
        seule ligne (une ligne un peu plus haute que sa forme ne déborde pas à l'œil), le texte réduit
        automatiquement (normAutofit)."""
        def shapes(container):
            for sh in container:
                if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                    yield from shapes(sh.shapes)
                elif sh.has_text_frame and sh.text_frame.text.strip() and not sh.rotation:
                    yield sh
        for slide in self.prs.slides:
            for sh in shapes(slide.shapes):
                if sh.text_frame._txBody in self._as_is:
                    continue
                measured = text_extent(sh)
                if measured is None:
                    continue
                needed, lines = measured
                h = Emu(sh.height).inches
                if lines > 1 and needed > h + 0.03:
                    self._warn(sh, f"texte trop long pour sa forme ({needed:.2f} pouces de haut pour {h:.2f}) :"
                                   f" « {sh.text_frame.text[:50].replace(chr(10), ' / ')}… » ; raccourcir le texte ou "
                                   "agrandir la zone")

    def _placeholder(self, slide, ph_type):
        for ph in slide.placeholders:
            if ph.placeholder_format.type == ph_type:
                return ph
        return None

    def _drop_empty_placeholders(self, slide):
        for ph in list(slide.placeholders):
            if not ph.has_text_frame or not ph.text_frame.text.strip():
                ph._element.getparent().remove(ph._element)

    def _fit_title(self, ph, text, base=20):
        """Réduit le titre d'un layout qui ne tiendrait pas sur une ligne à la taille du gabarit (largeur mesurée en
        Outfit gras), sans descendre sous 12 pt. Alerte seulement si, à 12 pt, il dépasse encore deux lignes."""
        tf = ph.text_frame
        avail = Emu(ph.width - tf.margin_left - tf.margin_right).inches
        bold = "**" + re.sub(r"\*\*|==", "", text).replace("\n", " ") + "**"
        width = text_width(bold, base)
        if width <= avail:
            return
        size = max(12, int(base * avail / width))
        for p in tf.paragraphs:
            for r in p.runs:
                r.font.size = Pt(size)
        if text_width(bold, 12) > 2 * avail:
            print(f"⚠ titre trop long pour ce layout, même à 12 pt : « {text[:40]}… » ; le raccourcir")

    def _fill_placeholder(self, ph, text):
        """Texte balisé dans un placeholder, en gardant le style hérité du layout (seul le gras est forcé)."""
        tf = ph.text_frame
        for i, line in enumerate(lines_of(text)):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            for chunk, is_bold, _ in _runs(line[2:] if line.startswith("- ") else line):
                r = p.add_run()
                r.text = chunk
                if is_bold:
                    r.font.bold = True

    def notes(self, slide, text):
        """Notes de l'orateur de la slide (texte brut) : le discours, ou la description d'une variante (« Variante B
        — focal : le chiffre ; contraste : un seul aplat ; géométrie : 3 colonnes »)."""
        slide.notes_slide.notes_text_frame.text = typo(text)
        return slide

    def text(self, slide, x, y, w, h, text, size=10, color=AUTO, align="left", anchor="top", bold=False,
             line_spacing=None):
        """Zone de texte balisé. h=None : hauteur ajustée au texte mesuré (la forme renvoyée donne sa hauteur, pour
        empiler la suite dessous). Alerte si le texte dépasse une hauteur fixée. color : par défaut le texte courant
        de la charte (TEXT)."""
        color = self.TEXT if color == AUTO else color
        if h is None:
            h = text_height(text, w, size, bold, line_spacing)
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        self._fill_text(tb.text_frame, text, size, color, align, anchor, bold, line_spacing)
        return tb

    def _fill_text(self, tf, text, size, color, align, anchor, bold=False, line_spacing=None):
        """Interligne par défaut (charte) : 1,5 pour le texte courant, 1,2 pour les blocs denses sous 10 pt."""
        line_spacing = line_spacing or (1.5 if size >= 10 else 1.2)
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.08)
        tf.margin_top = tf.margin_bottom = Inches(0.04)
        tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[anchor]
        lines = lines_of(text)
        for i, line in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[align]
            p.line_spacing = line_spacing
            if line.startswith(("- ", "> ")):
                self._bullet(p, "●" if line[0] == "-" else ">")
                line = line[2:]
            for chunk, is_bold, is_turq in _runs(line):
                r = p.add_run()
                r.text = chunk
                r.font.name = self.FONT
                r.font.size = Pt(size)
                r.font.bold = is_bold or bold
                # Mot-clé à la couleur d'accent seulement sur fond foncé (texte blanc) : sur fond clair, couleur du texte.
                r.font.color.rgb = self.ACCENT if is_turq and color == WHITE else color

    def _bullet(self, p, char="●"):
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(Inches(0.18 if char == "●" else 0.24)))
        pPr.set("indent", str(-Inches(0.14 if char == "●" else 0.2)))
        clr = etree.SubElement(pPr, qn("a:buClr"))
        etree.SubElement(clr, qn("a:srgbClr")).set("val", self.BULLET)
        if char != "●":
            etree.SubElement(pPr, qn("a:buFont")).set("typeface", self.FONT)
        etree.SubElement(pPr, qn("a:buChar")).set("char", char)

    def _final_point(self, tf):
        """Point final à la couleur POINT de la charte (couverture, slide message ou héros, accroche, titre)."""
        last = tf.paragraphs[-1].runs[-1]
        if not last.text.endswith("."):
            return
        last.text = last.text[:-1]
        r = tf.paragraphs[-1].add_run()
        r.text = "."
        r.font.name, r.font.size, r.font.bold = self.FONT, last.font.size, True
        r.font.color.rgb = self.POINT

    def statement(self, slide, text, y=1.6, h=2.4, size=24):
        """Grosse phrase-message centrée, en gras ; si elle finit par un point, il prend la couleur POINT."""
        width = Emu(self.prs.slide_width).inches
        tb = self.text(slide, 0.7, y, width - 1.4, h, text, size=size, align="center", anchor="middle", bold=True)
        self._final_point(tb.text_frame)
        return tb

    def _shape(self, slide, kind, x, y, w, h, fill=None, line=AUTO, line_w=0.75, dash=False, adj=None, name=None):
        """Forme de base. name : nom lisible (« Bloc « Titre » »), repris par les alertes du contrôle de mise en page
        quand la forme ne porte pas de texte elle-même. line : contour (par défaut LINE de la charte, None : sans)."""
        line = self.LINE if line == AUTO else line
        sh = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
        if name:
            sh.name = name[:80]
        if fill is None:
            sh.fill.background()
        else:
            sh.fill.solid()
            sh.fill.fore_color.rgb = fill
        if line is None:
            sh.line.fill.background()
        else:
            sh.line.color.rgb = line
            sh.line.width = Pt(line_w)
            if dash:
                sh.line.dash_style = 4  # MSO_LINE.DASH
        if adj:
            for i, v in enumerate(adj):
                sh.adjustments[i] = v
        sh.shadow.inherit = False
        return sh

    HEAD_ANGLE = math.radians(38.4)

    HEAD_RATIO = 3.9

    def _bar(self, shapes, p1, p2, t, color):
        """Barre à bouts ronds dont les extrémités extérieures sont p1 et p2 (pouces), épaisseur t."""
        (x1, y1), (x2, y2) = p1, p2
        length = max(math.hypot(x2 - x1, y2 - y1), t)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        sh = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cx - length / 2), Inches(cy - t / 2),
                              Inches(length), Inches(t))
        sh.adjustments[0] = 0.5
        sh.rotation = math.degrees(math.atan2(y2 - y1, x2 - x1))
        sh.fill.solid()
        sh.fill.fore_color.rgb = color
        sh.line.fill.background()
        sh.shadow.inherit = False
        return sh

    def _head(self, shapes, tip, u, t, color):
        """Chevron ouvert dont la pointe extérieure est en tip, orienté selon le vecteur unitaire u."""
        kx, ky = tip[0] - u[0] * t / 2, tip[1] - u[1] * t / 2  # centre de l'arrondi commun des deux barres
        reach = self.HEAD_RATIO * t
        for a in (self.HEAD_ANGLE, -self.HEAD_ANGLE):
            dx = -u[0] * math.cos(a) + u[1] * math.sin(a)
            dy = -u[0] * math.sin(a) - u[1] * math.cos(a)
            self._bar(shapes, (kx - dx * t / 2, ky - dy * t / 2), (kx + dx * (reach - t / 2), ky + dy * (reach - t / 2)),
                      t, color)

    def arrow_path(self, slide, points, loop=False, weight=4, head=True):
        """Flèche le long d'une ligne brisée (pouces) : tronçons à bouts ronds, chevron sur le dernier point, couleur de
        flux de la charte (FLOW). loop=True : boucle de retour (LOOP). weight : épaisseur en points (3 à 4)."""
        t = weight / 72
        color = self.LOOP if loop else self.FLOW
        grp = slide.shapes.add_group_shape()
        # Le nom porte les deux bouts, puis le point d'où part le dernier tronçon : le contrôle de mise en page
        # (octo_lint) vérifie que les bouts touchent une forme et que la pointe a une tige derrière elle.
        (sx, sy), (ex, ey), (px, py) = points[0], points[-1], points[-2]
        grp.name = f"Flèche {sx:.3f},{sy:.3f} → {ex:.3f},{ey:.3f} | {px:.3f},{py:.3f}"
        last = len(points) - 2
        for k, (p1, p2) in enumerate(zip(points[:-1], points[1:])):
            # À chaque coude, les tronçons dépassent d'une demi-épaisseur : leurs arrondis sont alors centrés sur le
            # même point, et le coude est rond et net (sans cran) ; une fourche ne se pince plus à son point de
            # partage. Aux deux bouts de la flèche, l'extrémité reste sur le point donné.
            d = math.dist(p1, p2) or 1
            ux, uy = (p2[0] - p1[0]) / d, (p2[1] - p1[1]) / d
            a = p1 if k == 0 else (p1[0] - ux * t / 2, p1[1] - uy * t / 2)
            b = p2 if k == last else (p2[0] + ux * t / 2, p2[1] + uy * t / 2)
            self._bar(grp.shapes, a, b, t, color)
        if head:
            (x1, y1), (x2, y2) = points[-2], points[-1]
            dist = math.hypot(x2 - x1, y2 - y1) or 1
            self._head(grp.shapes, (x2, y2), ((x2 - x1) / dist, (y2 - y1) / dist), t, color)
        return grp

    def arrow(self, slide, x1, y1, x2, y2, elbow=True, dash=False, both=False, loop=False, weight=4):
        """Flèche de flux épaisse à chevron ouvert (couleur FLOW de la charte) ; loop=True : boucle de retour (LOOP) ;
        dash=True : lien secondaire en pointillés fins, petite pointe ouverte.
        elbow=True : coudée horizontal → vertical → horizontal quand les deux points ne sont pas alignés.
        Pour relier deux boîtes, préférer connect(), qui calcule les points sur leurs bords."""
        if elbow and abs(x1 - x2) > 0.01 and abs(y1 - y2) > 0.01:
            xm = (x1 + x2) / 2
            points = [(x1, y1), (xm, y1), (xm, y2), (x2, y2)]
        else:
            points = [(x1, y1), (x2, y2)]
        if dash:
            return self._dash_path(slide, points, both=both, loop=loop)
        grp = self.arrow_path(slide, points, loop=loop, weight=weight)
        if both:
            dist = math.hypot(points[1][0] - x1, points[1][1] - y1) or 1
            self._head(grp.shapes, (x1, y1), ((x1 - points[1][0]) / dist, (y1 - points[1][1]) / dist),
                       weight / 72, self.LOOP if loop else self.FLOW)
        return grp

    @staticmethod
    def _connector(shapes, x1, y1, x2, y2):
        """Filet droit (coordonnées en EMU), sans l'ombre que le style par défaut d'un connecteur prend au thème OCTO
        (style d'effet 1 : ombre portée, que Google Slides rend à sa façon)."""
        c = shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
        c.shadow.inherit = False
        return c

    def _dash_line(self, shapes, p1, p2, color, ends=()):
        """Filet pointillé fin de p1 à p2 (pouces) ; ends : « a:headEnd », « a:tailEnd », petites pointes ouvertes."""
        c = self._connector(shapes, Inches(p1[0]), Inches(p1[1]), Inches(p2[0]), Inches(p2[1]))
        c.line.color.rgb = color
        c.line.width = Pt(0.75)
        c.line.dash_style = 4
        ln = c.line._get_or_add_ln()
        ln.set("cap", "rnd")
        for end in ends:
            e = etree.SubElement(ln, qn(end))
            e.set("type", "arrow"), e.set("w", "sm"), e.set("len", "sm")
        return c

    def _dash_path(self, slide, points, both=False, loop=False):
        """Lien secondaire pointillé le long d'une ligne brisée. Un coude est tracé en filets droits groupés, pas en
        connecteur coudé : Google Slides replace le coude d'un connecteur à sa façon, un filet droit reste où il est."""
        color = self.LOOP if loop else self.FLOW
        if len(points) == 2:
            return self._dash_line(slide.shapes, *points, color, (["a:headEnd"] if both else []) + ["a:tailEnd"])
        grp = slide.shapes.add_group_shape()
        (sx, sy), (ex, ey) = points[0], points[-1]
        grp.name = f"Flèche {sx:.3f},{sy:.3f} → {ex:.3f},{ey:.3f}"
        last = len(points) - 2
        for k, (p1, p2) in enumerate(zip(points[:-1], points[1:])):
            ends = (["a:headEnd"] if both and k == 0 else []) + (["a:tailEnd"] if k == last else [])
            self._dash_line(grp.shapes, p1, p2, color, ends)
        return grp

    def chevron(self, slide, x, y, size=0.16, direction="right", color=AUTO):
        """Chevron de transition « > » entre deux blocs : pointe en (x, y), size = hauteur en pouces, couleur CHEVRON
        de la charte par défaut."""
        color = self.CHEVRON if color == AUTO else color
        u = {"right": (1, 0), "left": (-1, 0), "down": (0, 1), "up": (0, -1)}[direction]
        t = size / (2 * self.HEAD_RATIO * math.sin(self.HEAD_ANGLE))
        grp = slide.shapes.add_group_shape()
        self._head(grp.shapes, (x, y), u, max(t, 0.03), color)
        return grp

    def connect(self, slide, a, b, gap=0.06, dash=False, loop=False, weight=4):
        """Flèche de la boîte a vers la boîte b, de bord à bord. a et b : formes renvoyées par les helpers ou
        rectangles (x, y, w, h). Côte à côte : flèche horizontale à mi-hauteur de la partie commune des deux boîtes
        (droite si leurs hauteurs se recouvrent, coudée sinon) ; l'une sous l'autre : idem à la verticale.
        gap : écart entre la flèche et chaque bord."""
        (ax, ay, aw, ah), (bx, by, bw, bh) = _rect(a), _rect(b)
        h_gap = max(bx - (ax + aw), ax - (bx + bw))
        v_gap = max(by - (ay + ah), ay - (by + bh))
        if h_gap >= v_gap:
            right = bx >= ax + aw
            x1, x2 = (ax + aw + gap, bx - gap) if right else (ax - gap, bx + bw + gap)
            lo, hi = max(ay, by), min(ay + ah, by + bh)
            y1, y2 = ((lo + hi) / 2,) * 2 if hi - lo > 0.1 else (ay + ah / 2, by + bh / 2)
        else:
            down = by >= ay + ah
            y1, y2 = (ay + ah + gap, by - gap) if down else (ay - gap, by + bh + gap)
            lo, hi = max(ax, bx), min(ax + aw, bx + bw)
            x1, x2 = ((lo + hi) / 2,) * 2 if hi - lo > 0.1 else (ax + aw / 2, bx + bw / 2)
            if x1 != x2:  # coude vertical → horizontal → vertical
                ym = (y1 + y2) / 2
                points = [(x1, y1), (x1, ym), (x2, ym), (x2, y2)]
                if dash:
                    return self._dash_path(slide, points, loop=loop)
                return self.arrow_path(slide, points, loop=loop, weight=weight)
        return self.arrow(slide, x1, y1, x2, y2, elbow=True, dash=dash, loop=loop, weight=weight)

    def seg(self, slide, x1, y1, x2, y2):
        """Tronçon de boucle de retour (LOOP), épais, sans pointe. Se termine par arrow(..., loop=True).
        Préférer loop_back(), qui trace toute la boucle d'un seul tenant."""
        return self._bar(slide.shapes, (x1, y1), (x2, y2), 4 / 72, self.LOOP)

    def loop_back(self, slide, points):
        """Boucle de retour en L ou en U : tronçons (LOOP) entre les points (pouces), pointe sur le dernier."""
        return self.arrow_path(slide, points, loop=True)

    def fan(self, slide, src, dsts, dash=False):
        """Éventail : une flèche coudée d'un point source vers chaque point cible, ou de chaque point vers un même
        point cible si src est une liste et dsts un point. Points en pouces (x, y), sur les bords des boîtes."""
        if isinstance(src, list):
            return [self.arrow(slide, sx, sy, dsts[0], dsts[1], dash=dash) for sx, sy in src]
        return [self.arrow(slide, src[0], src[1], dx, dy, dash=dash) for dx, dy in dsts]

    def _branches(self, src, dsts, gap, trunk, reverse):
        """Tracés d'une fourche (de src vers chaque dst) : même point de départ, même tronc, puis une branche par
        cible. reverse=True : tracés d'une jonction (chaque dst vers src), lus à l'envers."""
        sx, sy, sw, sh = _rect(src)
        rects = [_rect(b) for b in dsts]
        # Axe de la fourche (0 : horizontal, 1 : vertical) et sens (+1 : cibles à droite / dessous, -1 : à gauche /
        # dessus). En coordonnées « le long de l'axe » (a) et « en travers » (c), les quatre cas n'en font qu'un.
        for axis, sign in ((0, 1), (1, 1), (0, -1), (1, -1)):
            if all((r[axis] >= (sx, sy)[axis] + (sw, sh)[axis]) if sign > 0 else
                   (r[axis] + r[axis + 2] <= (sx, sy)[axis]) for r in rects):
                break
        else:
            raise ValueError("fourche : les cibles doivent être toutes du même côté de la source (droite, gauche, "
                             "dessous ou dessus)")
        src_a, src_c, src_la, src_lc = ((sx, sy, sw, sh) if axis == 0 else (sy, sx, sh, sw))
        a0 = src_a + src_la + gap if sign > 0 else src_a - gap
        c0 = src_c + src_lc / 2
        near = [(r[axis] - gap if sign > 0 else r[axis] + r[axis + 2] + gap) for r in rects]
        nearest = min(near) if sign > 0 else max(near)
        # Jonction : le tronc final porte la pointe, il prend plus de la moitié de l'écart pour garder une tige.
        af = a0 + sign * (trunk if trunk is not None else max(0.15, abs(nearest - a0) * (0.55 if reverse else 0.4)))
        room = abs(nearest - af)
        point = (lambda a, c: (a, c)) if axis == 0 else (lambda a, c: (c, a))
        paths = []
        for r, end in zip(rects, near):
            cc = r[1 - axis] + r[3 - axis] / 2
            paths.append([point(a0, c0), point(af, c0), point(af, cc), point(end, cc)])
        issues = []
        if room < 0.25:
            issues.append(f"{'jonction' if reverse else 'fourche'} trop serrée ({room:.2f} pouce entre la barre et "
                          "les boîtes) : élargir l'écart (0,8 pouce au moins), ou réduire trunk")
        centers = [r[1 - axis] + r[3 - axis] / 2 for r in rects]
        if len(rects) > 1 and not min(centers) + 0.02 < c0 < max(centers) - 0.02:
            issues.append(f"{'jonction décentrée : la cible' if reverse else 'fourche décentrée : la source'} est dans "
                          "l'axe d'une boîte extrême, les autres branches rejoignent sa tige en cours de route ; "
                          "centrer la boîte sur les autres, ou regrouper les boîtes dans un container et une seule "
                          "flèche (connect)")
        cleaned = []
        for pts in paths:
            pts = [p for k, p in enumerate(pts) if k == 0 or math.dist(p, pts[k - 1]) > 0.005]
            cleaned.append(pts[::-1] if reverse else pts)
        return cleaned, issues

    def fork(self, slide, src, dsts, gap=0.06, trunk=None, loop=False):
        """Fourche : un seul tronc sort de la boîte src, puis une branche vers chaque boîte de dsts (une PR qui part
        en dev et en prod, une commande qui lance trois agents). Cibles toutes à droite de src (fourche horizontale)
        ou toutes en dessous (verticale). Le tronc part du milieu du bord de src et se divise à trunk pouces du bord
        (défaut : 40 % de l'écart) ; chaque branche arrive au milieu du bord de sa cible. À préférer à plusieurs
        connect() ou à fan() depuis une même boîte : leurs flèches partent de points voisins et se croisent.
        Écart conseillé : 0,8 pouce, pour que chaque branche garde une tige derrière sa pointe ; la source est
        centrée sur les cibles (alerte sinon). Renvoie les flèches."""
        paths, issues = self._branches(src, dsts, gap, trunk, False)
        arrows = [self.arrow_path(slide, pts, loop=loop) for pts in paths]
        for issue in issues:
            self._warn(arrows[0], issue)
        return arrows

    def join(self, slide, srcs, dst, gap=0.06, trunk=None, loop=False):
        """Jonction, l'inverse de fork() : une branche part de chaque boîte de srcs, elles se rejoignent en un seul
        tronc qui entre dans dst (trois preuves qui mènent à une conclusion). Sources toutes à gauche de dst ou
        toutes au-dessus. trunk : longueur du tronc final, qui porte la pointe (défaut : 55 % de l'écart) ; sous
        0,35 pouce la pointe se colle à la barre. Écart conseillé : 0,8 pouce ; dst centrée sur les sources, sinon
        une branche rejoint la tige d'une autre en cours de route (alerte) : regrouper alors les sources dans un
        container et tracer une seule flèche (connect). Renvoie les flèches."""
        paths, issues = self._branches(dst, srcs, gap, trunk, True)
        arrows = [self.arrow_path(slide, pts, loop=loop) for pts in paths]
        for issue in issues:
            self._warn(arrows[0], issue)
        return arrows

    def picto(self, slide, name, x, y, size=0.6):
        """Visuel de la bibliothèque du deck (VISUAL_DIRS) par son nom (sans .png), à la hauteur size."""
        return slide.shapes.add_picture(self._visual(name), Inches(x), Inches(y), height=Inches(size))

    _PHOTO_SHAPES = {"tl-br": MSO_SHAPE.ROUND_2_DIAG_RECTANGLE, "goutte": MSO_SHAPE.TEAR, "rond": MSO_SHAPE.OVAL,
                     "arrondi": MSO_SHAPE.ROUNDED_RECTANGLE, "droit": MSO_SHAPE.RECTANGLE}

    def photo(self, slide, image, x, y, w, h, shape=AUTO, anchor="mc", line=AUTO):
        """Photo, capture ou une de presse qui remplit la zone, recadrée sans déformation et découpée : shape =
        "arrondi", "rond", "tl-br" (coins opposés arrondis), "goutte" ou "droit" (angles droits : charte Accenture
        seulement) ; par défaut la découpe de la charte (PHOTO_SHAPE). anchor = "mc" recadre au centre, "tc" garde le haut (capture d'écran,
        visage, une de journal). image : chemin d'un fichier, ou nom d'un visuel de la bibliothèque du deck. line :
        contour fin (par défaut LINE de la charte, None : sans contour). Une image sous licence libre se crédite dans
        le deck (slide de crédits)."""
        line = self.LINE if line == AUTO else line
        shape = self.PHOTO_SHAPE if shape == AUTO else shape
        path = image if Path(str(image)).exists() else self._visual(image)
        pic = slide.shapes.add_picture(path if isinstance(path, io.BytesIO) else str(path), Inches(x), Inches(y),
                                       Inches(w), Inches(h))
        iw, ih = pic.image.size
        rz, ri = w / h, iw / ih
        if ri > rz:
            pic.crop_left = pic.crop_right = (1 - rz / ri) / 2
        elif anchor == "tc":
            pic.crop_bottom = 1 - ri / rz
        else:
            pic.crop_top = pic.crop_bottom = (1 - ri / rz) / 2
        pic.auto_shape_type = self._PHOTO_SHAPES[shape]
        if line is not None:
            pic.line.color.rgb = line
            pic.line.width = Pt(0.75)
        return pic

    def photo_fit(self, slide, image, x, y, w, h):
        """Image entière, proportions gardées, centrée dans la zone : un schéma ou une capture à lire en entier. Posée
        dans une forme à coins arrondis, garder une marge d'au moins 0,36 rayon (Frame.pad(0.36 * radius)) : sinon le
        coin carré de l'image sort de l'arrondi."""
        path = image if Path(str(image)).exists() else self._visual(image)
        pic = slide.shapes.add_picture(path if isinstance(path, io.BytesIO) else str(path), 0, 0)
        iw, ih = pic.image.size
        k = min(w / iw, h / ih)
        pic.width, pic.height = Inches(iw * k), Inches(ih * k)
        pic.left, pic.top = Inches(x + (w - iw * k) / 2), Inches(y + (h - ih * k) / 2)
        return pic

    def circle(self, slide, cx, cy, r, fill=WHITE, line=AUTO, line_w=0.75, dash=False):
        """Cercle de centre (cx, cy) et de rayon r : point d'un nuage, neurone, jalon, bille d'un mini-schéma. line :
        contour (par défaut LINE de la charte)."""
        return self._shape(slide, MSO_SHAPE.OVAL, cx - r, cy - r, 2 * r, 2 * r, fill=fill, line=line,
                           line_w=line_w, dash=dash)

    def rule(self, slide, x1, y1, x2, y2, color=AUTO, width=0.75, dash=False):
        """Filet fin : séparateur de colonnes (vertical), sous un intertitre (horizontal), ou lien d'un picto vers sa
        forme. dash=True : pointillés. color : par défaut RULE de la charte."""
        color = self.RULE if color == AUTO else color
        line = self._connector(slide.shapes, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        line.line.color.rgb = color
        line.line.width = Pt(width)
        if dash:
            line.line.dash_style = 4
        return line

    def _set_language(self, lang="fr-FR"):
        """Langue de tout le texte des slides et des notes : sans elle, PowerPoint et Google Slides vérifient
        l'orthographe en anglais et soulignent en rouge les mots français."""
        parts = [s._element for s in self.prs.slides]
        parts += [s.notes_slide._element for s in self.prs.slides if s.has_notes_slide]
        for root in parts:
            for run in root.iter(qn("a:r"), qn("a:fld")):
                if run.find(qn("a:rPr")) is None:
                    run.insert(0, etree.Element(qn("a:rPr")))
            for rpr in root.iter(qn("a:rPr"), qn("a:endParaRPr")):
                rpr.set("lang", lang)

    def save(self, path):
        self._set_language(self.LANG)
        self._check_fits()
        for i, slide in enumerate(self.prs.slides, 1):
            issues = check_slide(slide, self._as_is, self.CHARTE)
            if self.target == "gslides":
                issues += gslides_issues(slide, self._as_is)
            for issue in issues:
                self.warnings.append(f"slide {i} : {issue}")
                print(f"⚠ slide {i} : {issue}")
        self.prs.save(str(path))
        if self.warnings:
            print(f"⚠ {len(self.warnings)} alerte(s) de mise en page, à corriger avant le rendu "
                  f"({self.MISE_EN_PAGE}) :")
            for w in self.warnings:
                print(f"   - {w}")
        numbers = {s.slide_id: i for i, s in enumerate(self.prs.slides, 1)}
        slots = [(numbers[sid], subject) for sid, subject in self.image_slots if sid in numbers]
        if slots:
            print(f"{len(slots)} image(s) à insérer (à donner à la livraison) :")
            for n, subject in slots:
                print(f"   - slide {n} : {subject}")
        return path
