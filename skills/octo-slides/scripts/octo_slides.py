"""Helpers python-pptx pour produire des slides conformes à la charte OCTO.

Usage :
    import sys; sys.path.insert(0, "<skill>/scripts")
    from octo_slides import Deck
    deck = Deck()
    s = deck.slide("Titre affirmatif de la slide", "Sous-titre qui dit le message en une phrase.")
    gauche, droite = CONTENT.cols(2, gap=0)                    # zones : references/mise_en_page.md
    deck.bloc(s, *gauche, title="Lead en gras", body="Explication courte.", corners="tl-br")
    deck.save("out.pptx")

Markup dans les textes : **gras**, ==mot-clé== (gras ; turquoise seulement sur fond marine, cf. charte),
\n pour un retour à la ligne, "- " en début de ligne pour une puce, "> " pour une puce chevron turquoise.
Toutes les coordonnées sont en pouces. Slide : 10 x 5.625.
"""
import copy
import math
import re
from pathlib import Path

from lxml import etree
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.parts.image import Image
from pptx.util import Emu, Inches, Pt

import deck_base
from octo_lint import check_slide, gslides_issues, text_extent  # noqa: F401 (réexportés)
from deck_base import (AUTO, FONT, WHITE, BaseDeck, _rect, _runs, _shape_texts, extract_text,  # noqa: F401
                       _TOKEN)
from octo_layout import (CONTENT, CONTENT_WIDE, LINE_HEIGHT, NBSP, PAGE_NUMBER, SLIDE, Frame,  # noqa: F401
                         lines_of, text_height, text_width, typo, wrap)

SKILL_DIR, ASSETS = deck_base.SKILL_DIR, deck_base.ASSETS
TEMPLATE = ASSETS / "template_octo.pptx"
# Ordre de recherche d'un picto par son nom : pictos du deck de référence, puis bibliothèque OCTO.
# "blanc/<nom>" désigne la déclinaison blanche (fond marine) de la bibliothèque OCTO.
PICTO_DIRS = [ASSETS / "pictos", ASSETS / "pictos-octo" / "bichrome", ASSETS / "pictos-octo",
              ASSETS / "avatars", ASSETS / "illustrations", ASSETS / "logos"]

# Palette de la charte OCTO (references/charte.md). Aucune autre couleur.
NAVY = RGBColor(0x0E, 0x23, 0x56)
NAVY_90 = RGBColor(0x26, 0x39, 0x67)
NAVY_80 = RGBColor(0x3E, 0x4F, 0x78)  # texte secondaire
NAVY_70 = RGBColor(0x58, 0x65, 0x86)  # texte discret
NAVY_60 = RGBColor(0x6E, 0x7B, 0x9A)
NAVY_50 = RGBColor(0x86, 0x91, 0xAB)
NAVY_40 = RGBColor(0x9F, 0xA7, 0xBB)
NAVY_30 = RGBColor(0xB7, 0xBD, 0xCC)
NAVY_20 = RGBColor(0xCF, 0xD3, 0xDD)  # filets clairs
NAVY_15 = RGBColor(0xDB, 0xDE, 0xE6)
NAVY_10 = RGBColor(0xE7, 0xE9, 0xEE)  # fond des cadres "fenêtre"
NAVY_5 = RGBColor(0xF3, 0xF4, 0xF7)  # fond d'alternance
TURQ = RGBColor(0x00, 0xD2, 0xDD)  # fonds, accents, puces ; jamais de texte sur fond clair
TURQ_90 = RGBColor(0x3C, 0xD7, 0xE0)
TURQ_80 = RGBColor(0x5B, 0xDD, 0xE4)
TURQ_70 = RGBColor(0x72, 0xDF, 0xE7)  # pastilles
TURQ_60 = RGBColor(0x8A, 0xE4, 0xEB)
TURQ_50 = RGBColor(0x9E, 0xE9, 0xED)
TURQ_40 = RGBColor(0xB2, 0xEE, 0xF2)
TURQ_30 = RGBColor(0xC6, 0xF1, 0xF5)  # étiquettes claires
TURQ_20 = RGBColor(0xDA, 0xF6, 0xF9)  # regroupements
TURQ_10 = RGBColor(0xEB, 0xFA, 0xFB)  # fond d'alternance
DARK_FILLS = {NAVY, NAVY_90, NAVY_80, NAVY_70}  # fonds sur lesquels le texte passe en blanc (charte, contrastes)

LAYOUTS = {
    "cover": "40 - Couverture [1]",
    "chapter": "50 - Chapitre [1]",
    "title_sub_content": "01 - Titre, sous-titre et contenu",
    "title_content": "02 - Titre et contenu",
    "title_sub": "03 - Titre et sous-titre",
    "title_only": "04 - Titre seul",
    "blank": "06 - Slide vide",
}
# Layouts marqués « Ne pas utiliser » dans le template (references/layouts.md).
FORBIDDEN_LAYOUTS = {"07", "60", "61", "62"}

def bloc_height(w, title=None, body=None, title_size=14, size=10, pad=0.22, picto_size=0):
    """Hauteur (pouces) d'un bloc() de largeur w ajustée à son titre et à son corps : pour un bloc sans vide en bas,
    ou pour donner à N blocs côte à côte la hauteur du plus rempli. Mêmes paramètres que Deck.bloc()."""
    tw = w - 2 * pad + 0.16
    th = text_height(f"**{title}**", tw - (picto_size + 0.1 if picto_size else 0), title_size,
                     line_spacing=1.1) if title else 0
    bh = text_height(body, tw, size) if body else 0
    return 1.6 * pad + th + bh + 0.02


def find_visual(name, dirs=None):
    """Fichier d'un visuel OCTO par son nom. Cherche dans les dossiers d'assets OCTO (dirs, par défaut PICTO_DIRS),
    puis dans les planches assets/atlas/ du zip claude.ai (limité à 200 fichiers, sans archive imbriquée : les
    visuels y sont regroupés en grandes images)."""
    return deck_base.find_visual(name, dirs or PICTO_DIRS)


class Pyramid:
    """Géométrie d'une pyramide posée par Deck.pyramid : niveaux, flanc droit, cassures entre niveaux."""

    def __init__(self, tiers, cx, slope):
        self.tiers, self.cx, self.slope = tiers, cx, slope
        self.apex = tiers[0].y

    def edge(self, y):
        """Abscisse du flanc droit à l'ordonnée y (le flanc gauche est symétrique autour de cx)."""
        return self.cx + self.slope * (y - self.apex)

    def cut(self, i):
        """Ordonnée de la cassure entre le niveau i et le suivant : y poser un filet pointillé vers les légendes."""
        return (self.tiers[i].bottom + self.tiers[i + 1].y) / 2


class Deck(BaseDeck):
    """Deck OCTO : template, palette et bibliothèque de visuels de la charte OCTO (references/charte.md). Les helpers
    génériques (texte, flèches, images, enregistrement) viennent de deck_base.BaseDeck."""
    TEMPLATE = TEMPLATE
    VISUAL_DIRS = PICTO_DIRS
    TEXT = LINE = FLOW = NAVY
    ACCENT = POINT = LOOP = CHEVRON = TURQ
    RULE = NAVY_30
    BULLET = "00D2DD"
    PHOTO_SHAPE = "tl-br"  # photos à coins opposés arrondis (charte)
    CHARTE = "octo"  # remèdes du contrôle de mise en page (octo_lint.HINTS)
    CHARTE_FILE = "references/charte.md"

    def __init__(self, template=TEMPLATE, target="pptx"):
        """target="gslides" : deck destiné à Google Slides. Le texte est mesuré 5 % plus large (marge pour les retours
        à la ligne de Slides) et save() signale ce que Slides ne rend pas (dégradé, ombre, graphique natif...)."""
        super().__init__(template, target)

    # ---------- slides ----------
    def _new(self, key):
        return self.prs.slides.add_slide(self._layouts[LAYOUTS[key]])

    # ---------- layouts préformatés du template (references/layouts.md) ----------
    def layout(self, number, texts=None, visuals=None):
        """Slide sur un layout préformaté du template, désigné par son numéro ("05", "41", "65"…).
        texts : {idx du placeholder: texte balisé} ; le style du layout (taille, couleur, puces) est conservé.
        visuals : un élément par emplacement photo du layout, dans l'ordre de references/layouts.md :
        chemin d'une photo, ou nom d'un picto / d'une illustration (posé sur une goutte turquoise pâle).
        Un emplacement non fourni est couvert d'un aplat turquoise pâle (jamais de « ici mettre une photo »)."""
        assert number not in FORBIDDEN_LAYOUTS, f"Layout {number} marqué « Ne pas utiliser » dans le template"
        layout = next(l for name, l in self._layouts.items() if name.startswith(f"{number} - "))
        s = self.prs.slides.add_slide(layout)
        texts = texts or {}
        for ph in list(s.placeholders):
            idx = ph.placeholder_format.idx
            if texts.get(idx):
                self._fill_placeholder(ph, texts[idx])
                if idx == 0:
                    self._fit_title(ph, texts[idx])
            else:
                ph._element.getparent().remove(ph._element)
        visuals = visuals or []
        for i, slot in enumerate(self._photo_slots(layout)):
            self._fill_slot(s, slot, visuals[i] if i < len(visuals) else None)
        return s

    def _photo_slots(self, layout):
        """Emplacements « ici mettre une photo » d'un layout : la forme qui porte la découpe (goutte, coins arrondis)."""
        slots = []
        statics = [sh for sh in layout.shapes if not sh.is_placeholder]
        for sh in statics:
            if "ici mettre" not in "".join(sh._element.xpath(".//a:t/text()")):
                continue
            if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                slots.append(sh)
                continue
            # Texte isolé posé sur la forme : l'emplacement est la plus grande forme qui le contient.
            cx, cy = sh.left + sh.width // 2, sh.top + sh.height // 2
            under = [o for o in statics if o is not sh and o.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE
                     and o.left <= cx <= o.left + o.width and o.top <= cy <= o.top + o.height]
            slots.append(max(under, key=lambda o: o.width * o.height))
        return slots

    def _fill_slot(self, slide, slot, visual):
        """Recopie la forme de l'emplacement sur la slide (même découpe) et la remplit."""
        el = copy.deepcopy(slot._element)
        for sp in el.xpath(".//p:sp[.//a:t[contains(., 'ici mettre')]]"):
            sp.getparent().remove(sp)
        geom = el if el.tag == qn("p:sp") else el.xpath(".//p:sp")[0]
        spPr = geom.find(qn("p:spPr"))
        for old in spPr.xpath("a:solidFill|a:noFill|a:blipFill|a:gradFill"):
            spPr.remove(old)
        photo = visual is not None and Path(str(visual)).is_file()
        fill = self._blip_fill(slide, Path(str(visual)), slot) if photo else self._solid_fill(TURQ_30)
        spPr.insert(list(spPr).index(spPr.find(qn("a:prstGeom"))) + 1, fill)
        ln = spPr.find(qn("a:ln"))
        if ln is not None:
            spPr.remove(ln)
        slide.shapes._spTree.append(el)
        if visual is not None and not photo:
            side = min(slot.width, slot.height) * 0.6
            pic = self.picto(slide, visual, 0, 0, Emu(int(side)).inches)
            pic.left = slot.left + (slot.width - pic.width) // 2
            pic.top = slot.top + (slot.height - pic.height) // 2

    def _solid_fill(self, color):
        fill = etree.Element(qn("a:solidFill"))
        etree.SubElement(fill, qn("a:srgbClr")).set("val", str(color))
        return fill

    def _blip_fill(self, slide, path, slot):
        """Remplissage photo recadré au format de l'emplacement, sans rotation avec la forme."""
        _, rId = slide.part.get_or_add_image_part(str(path))
        w, h = Image.from_file(str(path)).size
        fill = etree.Element(qn("a:blipFill"), rotWithShape="0")
        etree.SubElement(fill, qn("a:blip")).set(qn("r:embed"), rId)
        src = etree.SubElement(fill, qn("a:srcRect"))
        target, image = slot.width / slot.height, w / h
        if image > target:
            crop = int((1 - target / image) / 2 * 100000)
            src.set("l", str(crop)), src.set("r", str(crop))
        else:
            crop = int((1 - image / target) / 2 * 100000)
            src.set("t", str(crop)), src.set("b", str(crop))
        etree.SubElement(etree.SubElement(fill, qn("a:stretch")), qn("a:fillRect"))
        return fill

    def cover(self, title, subtitle, date, tag, variant=1):
        """Couverture. variant=1 : photo du template (layout 40) ; variant=2 : aplat marine sans photo (41).
        Un titre qui finit par un point reçoit le point final turquoise de la charte."""
        s = self.layout("40" if variant == 1 else "41", {0: title, 1: subtitle, 2: date, 3: tag})
        for ph in s.placeholders:
            if ph.placeholder_format.idx == 0:
                self._final_point(ph.text_frame)
        return s

    def chapter(self, title, number, visual=None, variant=1, parts=None):
        """Slide chapitre (layout 50, goutte ronde ; variant=2 : layout 51, goutte carrée).
        visual : photo, picto ou illustration (défaut : visuel du deck de référence).
        parts : noms des parties du deck (« Ouverture », « Histoire »…) : un fil d'onglets sous le titre situe le
        public dans la session, la partie en cours en marine (number doit alors être un entier)."""
        s = self.layout("50" if variant == 1 else "51", {0: title, 1: f"{number:02d}" if isinstance(number, int) else number},
                        [visual or SKILL_DIR / "assets" / "chapitre_visuel.png"])
        for ph in s.placeholders:
            if ph.placeholder_format.idx == 1:
                pPr = ph.text_frame.paragraphs[0]._p.get_or_add_pPr()
                pPr.set("marL", "0")
                pPr.set("indent", "0")
                etree.SubElement(pPr, qn("a:buNone"))
        if parts:
            self.steps(s, 4.8, 3.75, parts, active=int(number) - 1, size=8.5, h=0.3)
        return s

    def focus(self, title, subtitle=None, body=None):
        """Slide « focus » (layout 05) : cadre blanc sur fond #3E4F78, pour un message clé ou le « pourquoi »."""
        return self.layout("05", {0: title, 1: subtitle, 2: body})

    def toc(self, items, title="Sommaire"):
        """Table des matières à pastilles goutte 01…n (layouts 90 à 98), de 2 à 10 entrées."""
        assert 2 <= len(items) <= 10, "toc : 2 à 10 entrées"
        idxs = list(range(1, 10)) + [13]  # la 10e entrée du layout 98 est le placeholder 13
        return self.layout(str(88 + len(items)), {0: title, **dict(zip(idxs, items))})

    def closing(self):
        """Slide de clôture « There is a better way. » (layout 59)."""
        return self.layout("59")

    def slide(self, title, subtitle=None, subtitle_size=None):
        """Slide de contenu standard : titre (phrase affirmative) + sous-titre optionnel, zone libre dessous.
        subtitle_size : réduit le sous-titre (13 pt) pour le garder sur une ligne au-dessus d'une slide dense."""
        s = self._new("title_sub_content")
        for ph in s.placeholders:
            idx = ph.placeholder_format.idx
            if idx == 0:
                self._fill_placeholder(ph, title)
                if len(title) > 70:
                    # Au-delà de 70 caractères le titre passe sur 2 lignes et mord sur le sous-titre.
                    for r in ph.text_frame.paragraphs[0].runs:
                        r.font.size = Pt(15)
            elif idx == 2 and subtitle:
                self._fill_placeholder(ph, subtitle)
                if subtitle_size:
                    for r in ph.text_frame.paragraphs[0].runs:
                        r.font.size = Pt(subtitle_size)
        self._drop_empty_placeholders(s)
        return s

    def blank(self):
        return self._new("blank")

    # ---------- texte ----------
    # ---------- formes de base ----------
    def box(self, slide, x, y, w, h, text="", header=False, size=8.75, fill=None, align=None):
        """Boîte de schéma : coins légèrement arrondis, contour marine fin. header=True : fond turquoise, texte gras.
        fill=NAVY : aplat de plus haut niveau, texte blanc (un seul par schéma)."""
        fill = fill if fill is not None else (TURQ if header else WHITE)
        sh = self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=fill, adj=[0.08])
        if text:
            # Corps à puces aligné à gauche, texte court centré.
            align = align or ("left" if any(m in f"\n{text}" for m in ("\n- ", "\n> ")) else "center")
            self._fill_text(sh.text_frame, text, size, WHITE if fill == NAVY else NAVY, align, "middle",
                            bold=header)
        return sh

    def titled_box(self, slide, x, y, w, h, header, body, header_h=0.42, size=8.75, align=None):
        """Boîte à en-tête turquoise + corps blanc (ex. Espace projet A / Registre MLflow...).
        align : alignement du corps (par défaut à gauche s'il a des puces, centré sinon)."""
        self.box(slide, x, y, w, header_h, header, header=True, size=size)
        self.box(slide, x, y + header_h, w, h - header_h, body, size=size, align=align)
        return x, y, w, h

    def container(self, slide, x, y, w, h, label=None):
        """Regroupement en pointillés (ex. 'la plateforme', un périmètre externe)."""
        sh = self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, dash=True, adj=[0.12],
                         name=f"Périmètre « {label} »" if label else "Périmètre pointillé")
        if label:
            self.text(slide, x + 0.1, y + 0.03, w - 0.2, 0.25, f"**{label}**", size=8)
        return sh

    def window(self, slide, x, y, w, h, title):
        """Cadre façon fenêtre d'appli (fond gris pâle, 2 pastilles, titre à droite) : cluster, plateforme..."""
        self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=NAVY_10, adj=[0.04],
                    name=f"Fenêtre « {title} »")
        self._shape(slide, MSO_SHAPE.OVAL, x + 0.1, y + 0.08, 0.1, 0.1, fill=NAVY, line=NAVY)
        self._shape(slide, MSO_SHAPE.OVAL, x + 0.25, y + 0.08, 0.1, 0.1, fill=WHITE, line=NAVY)
        self.text(slide, x + 0.4, y + 0.0, w - 0.5, 0.28, f"**{title}**", size=9, align="right")
        line = self._connector(slide.shapes, Inches(x), Inches(y + 0.27), Inches(x + w),
                                          Inches(y + 0.27))
        line.line.color.rgb = NAVY
        line.line.width = Pt(0.66)

    # ---------- flèches (géométrie du modèle OCTO n° 10, « Éléments graphiques 3/3 ») ----------
    # Une flèche de flux OCTO n'est pas un trait à pointe triangle : c'est une tige en barre à bouts ronds, et une
    # pointe en chevron faite de deux barres arrondies inclinées à 38,4° de part et d'autre de la tige, longues de
    # 3,9 fois l'épaisseur. Le tout est groupé : la flèche se déplace d'un bloc dans Google Slides.
    # ---------- schémas (references/style.md : un schéma montre le mécanisme) ----------
    def pyramid(self, slide, x, y, w, h, levels, heights=None, gap=0.1, size=11):
        """Pyramide à niveaux (modèle OCTO 231) : une pointe en triangle puis des trapèzes, tous sur la même pente,
        séparés par gap. Pour une hiérarchie : peu en haut, beaucoup en bas (pyramide de tests, de besoins).
        levels : [(texte balisé, fond), ...] de la pointe à la base ; texte blanc sur les fonds marine foncés, marine
        sinon. heights : hauteurs des niveaux, syntaxe de Frame.rows (None : parts égales).
        Renvoie une Pyramid : .tiers (zones des niveaux), .cut(i) (ordonnée de la cassure sous le niveau i),
        .edge(y) (abscisse du flanc droit à l'ordonnée y), pour poser légendes et filets pointillés à droite."""
        tiers = Frame(x, y, w, h).rows(heights or len(levels), gap=gap)
        pyr = Pyramid(tiers, x + w / 2, w / 2 / h)
        for i, (tier, (text, fill)) in enumerate(zip(tiers, levels)):
            w_bottom = 2 * (pyr.edge(tier.bottom) - pyr.cx)
            left = pyr.cx - w_bottom / 2
            name = f"Niveau « {lines_of(text)[0][:30]} »"
            if i == 0:
                self._shape(slide, MSO_SHAPE.ISOSCELES_TRIANGLE, left, tier.y, w_bottom, tier.h, fill=fill,
                            line=None, name=name)
                # Le texte de la pointe se pose dans sa moitié basse, là où elle est assez large.
                zone = Frame(left + 0.1, tier.y + tier.h * 0.45, w_bottom - 0.2, tier.h * 0.5)
            else:
                # Trapèze : le bord haut est rentré de inset de chaque côté (ajustement relatif au petit côté).
                inset = pyr.edge(tier.bottom) - pyr.edge(tier.y)
                self._shape(slide, MSO_SHAPE.TRAPEZOID, left, tier.y, w_bottom, tier.h, fill=fill, line=None,
                            adj=[inset / min(w_bottom, tier.h)], name=name)
                w_top = 2 * (pyr.edge(tier.y) - pyr.cx)
                zone = Frame(pyr.cx - w_top / 2, tier.y + 0.08, w_top, tier.h - 0.16)
            self.text(slide, *zone, text, size=size - (1 if i == 0 else 0),
                      color=WHITE if fill in DARK_FILLS else NAVY, align="center", anchor="middle", line_spacing=1.15)
        return pyr

    def nested(self, slide, x, y, w, h, levels, dx=0.55, dy=None, radius=0.35, size=10.5):
        """Notions emboîtées en escalier (modèle OCTO 187, « A few definitions… ») : chaque niveau est un bloc posé
        dans le précédent, décalé de dx vers la droite et de dy vers le bas, tous alignés sur les bords droit et bas.
        Du plus large au plus précis, une définition puis un exemple par niveau : le bon moyen d'introduire des
        termes avant de s'en servir. levels : [(texte balisé, fond)], du plus large au plus précis ; texte blanc sur
        marine (==mots-clés== turquoise). dy : hauteur de la bande de texte de chaque niveau (défaut : le dernier
        niveau a une fois et demie la place des autres). Renvoie les zones de texte."""
        n = len(levels)
        dy = dy or h / (n + 0.5)
        zones = []
        for i, (text, fill) in enumerate(levels):
            zone = Frame(x + i * dx, y + i * dy, w - i * dx, h - i * dy)
            self.bloc(slide, *zone, corners="tl", radius=radius, fill=fill, line=None)
            last = i == n - 1
            inner = zone.pad(0.25, 0.14, 0.2, 0.14) if last else Frame(zone.x + 0.25, zone.y + 0.06, zone.w - 0.45,
                                                                         dy - 0.1)
            # Le dernier niveau a plus de place que les autres : son texte y est centré, sinon un texte court laisse
            # le bas du bloc vide.
            self.text(slide, *inner, text, size=size, color=WHITE if fill in DARK_FILLS else NAVY, line_spacing=1.25,
                      anchor="middle")
            zones.append(inner)
        return zones

    def cycle(self, slide, cx, cy, labels, w=1.6, h=0.5, rx=2.2, ry=1.2, key=None, size=9.5):
        """Cycle de N étapes posées sur une ellipse autour de (cx, cy), reliées par des flèches de flux ; la dernière
        flèche, qui ferme la boucle, est turquoise. key : index de l'étape mise en avant (fond turquoise).
        Renvoie les centres des boîtes."""
        import math
        n = len(labels)
        centers = [(cx + rx * math.sin(2 * math.pi * k / n), cy - ry * math.cos(2 * math.pi * k / n)) for k in range(n)]
        for k, ((x, y), label) in enumerate(zip(centers, labels)):
            self.box(slide, x - w / 2, y - h / 2, w, h, f"**{label}**", size=size, header=k == key)
        for k in range(n):
            (x1, y1), (x2, y2) = centers[k], centers[(k + 1) % n]
            # Flèche de bord à bord, raccourcie le long de la direction entre les centres.
            dx, dy = x2 - x1, y2 - y1
            dist = math.hypot(dx, dy)
            ux, uy = dx / dist, dy / dist
            shrink = min(w / 2 / max(abs(ux), 1e-6), h / 2 / max(abs(uy), 1e-6)) + 0.05
            self.arrow(slide, x1 + ux * shrink, y1 + uy * shrink, x2 - ux * shrink, y2 - uy * shrink, elbow=False,
                       loop=k == n - 1)
        return centers

    def lane(self, slide, x, y, w, label, label_w=1.6, size=9):
        """Couloir d'un Gantt ou d'une série temporelle de principe : libellé à gauche, filet pointillé marine."""
        self.text(slide, x, y - 0.15, label_w, 0.3, f"**{label}**", size=size, anchor="middle")
        self._dashed_rule(slide, x + label_w, x + w, y)

    def bar(self, slide, x, y, w, text="", key=False, h=0.26, size=8):
        """Barre de Gantt centrée sur le couloir y : pilule turquoise pâle, turquoise plein si key (charte :
        intensité du turquoise = priorité), contour marine fin."""
        sh = self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y - h / 2, w, h, fill=TURQ if key else TURQ_30,
                         adj=[0.5])
        if text:
            self._fill_text(sh.text_frame, text, size, NAVY, "center", "middle", bold=key)
            sh.text_frame.margin_top = sh.text_frame.margin_bottom = 0
        return sh

    # ---------- images (references/images.md) ----------
    def image_slot(self, slide, x, y, w, h, subject, shape="tl-br"):
        """Emplacement d'une image à insérer, quand l'utilisateur le demande et qu'aucun visuel OCTO ni aucune image
        libre ne convient : bloc gris pâle, picto photo, « Image à insérer » et le sujet (shape="goutte" : petite
        goutte, le sujet écrit dedans). Chaque emplacement est listé à l'enregistrement avec son numéro de slide,
        pour la livraison."""
        if shape == "goutte":
            self.goutte(slide, x, y, w, corner="tr", fill=NAVY_5, line=NAVY_40)
            self.text(slide, *Frame(x, y, w, w).pad(w * 0.06), f"**Image**\n{subject}",
                      size=7.5 if w < 1.05 else 8.5, color=NAVY_80, align="center", anchor="middle", line_spacing=1.1)
        else:
            self.bloc(slide, x, y, w, h, corners=shape, radius=min(0.45, w / 3, h / 3), fill=NAVY_5, line=NAVY_40)
            txt = f"**Image à insérer**\n{subject}"
            th = text_height(txt, w - 0.3, 9)
            top = y + (h - 0.48 - th) / 2
            p = self.picto(slide, "photo", x + w / 2 - 0.21, top, 0.42)
            p.left = Inches(x + w / 2) - p.width // 2
            self.text(slide, x + 0.15, top + 0.48, w - 0.3, th, txt, size=9, color=NAVY_80, align="center")
        self.image_slots.append((slide.slide_id, subject))

    # ---------- formes de la Com (modèles 8, 9 et 41 à 49 : éléments graphiques, suggestions de mise en page) ----------
    _CORNERS = {  # coins arrondis -> (forme, ajustements à multiplier par le rayon relatif, flipH, flipV)
        "tl-br": (MSO_SHAPE.ROUND_2_DIAG_RECTANGLE, (1, 0), False, False),
        "tr-bl": (MSO_SHAPE.ROUND_2_DIAG_RECTANGLE, (0, 1), False, False),
        "tr": (MSO_SHAPE.ROUND_1_RECTANGLE, (1,), False, False),
        "tl": (MSO_SHAPE.ROUND_1_RECTANGLE, (1,), True, False),
        "br": (MSO_SHAPE.ROUND_1_RECTANGLE, (1,), False, True),
        "bl": (MSO_SHAPE.ROUND_1_RECTANGLE, (1,), True, True),
        "top": (MSO_SHAPE.ROUND_2_SAME_RECTANGLE, (1, 0), False, False),
        "bottom": (MSO_SHAPE.ROUND_2_SAME_RECTANGLE, (0, 1), False, False),
        "all": (MSO_SHAPE.ROUNDED_RECTANGLE, (1,), False, False),
        "none": (MSO_SHAPE.RECTANGLE, (), False, False),
    }

    def _flip(self, sh, h=False, v=False):
        xfrm = sh._element.spPr.find(qn("a:xfrm"))
        if h:
            xfrm.set("flipH", "1")
        if v:
            xfrm.set("flipV", "1")

    def bloc(self, slide, x, y, w, h, corners="tl-br", radius=0.45, fill=WHITE, line=NAVY, line_w=0.75,
             title=None, body=None, picto=None, pad=0.22, title_size=14, size=10, picto_size=0.45):
        """Bloc OCTO : rectangle à grands coins arrondis, contour marine fin, la forme de base des suggestions de mise
        en page de la Com. corners : "tl-br" ou "tr-bl" (deux coins opposés, le plus courant), "tl", "tr", "bl", "br"
        (un seul coin), "top", "bottom" (deux coins d'un même côté), "all", "none". radius : rayon en pouces
        (0,45 dans les modèles ; plafonné à la moitié du petit côté).
        Blocs emboîtés : zones voisines sans écart (Frame.cols(..., gap=0)), les contours se superposent.
        title, body : texte posé dans la zone intérieure (marge pad), titre gras puis corps dessous ; picto : nom d'un
        picto, posé en haut à droite (picto_size : côté en pouces). fill=NAVY : texte blanc (un seul aplat marine par
        slide)."""
        kind, adj, flip_h, flip_v = self._CORNERS[corners]
        rel = min(radius / min(w, h), 0.5)
        sh = self._shape(slide, kind, x, y, w, h, fill=fill, line=line, line_w=line_w,
                         adj=[a * rel for a in adj] or None, name=f"Bloc « {title} »" if title else "Bloc")
        self._flip(sh, flip_h, flip_v)
        if title or body or picto:
            color = WHITE if fill == NAVY else NAVY
            inner = Frame(x, y, w, h).pad(pad, pad * 0.8)
            if picto:
                p = self.picto(slide, f"blanc/{picto}" if fill == NAVY and "/" not in picto else picto,
                               inner.right - picto_size, inner.y, picto_size)
                p.left = Inches(inner.right) - p.width
            ty = inner.y
            if title:
                tw = inner.w - (picto_size + 0.1 if picto else 0)
                t = self.text(slide, inner.x - 0.08, ty - 0.04, tw + 0.16, None, f"**{title}**", size=title_size,
                              color=color, line_spacing=1.1)
                ty += Emu(t.height).inches + 0.04
            elif picto:
                ty += picto_size + 0.1
            if body:
                tb = self.text(slide, inner.x - 0.08, ty - 0.04, inner.w + 0.16, inner.bottom - ty + 0.08, body,
                               size=size, color=color)
                if fill in (TURQ, TURQ_90, TURQ_80, TURQ_70, TURQ_60):  # puces turquoise invisibles : en marine
                    for clr in tb._element.iter(qn("a:buClr")):
                        clr[0].set("val", str(NAVY))
        return sh

    def goutte(self, slide, x, y, d, corner="br", fill=WHITE, line=NAVY, line_w=0.75, text=None, picto=None,
               size=10):
        """Goutte OCTO (modèles 8 et 44) : cercle de diamètre d dont un coin reste carré (corner : "tr", "br", "bl",
        "tl"). Pour un picto, un numéro, un mot ou une courte phrase centrés ; plusieurs gouttes se touchent pour
        former une chaîne."""
        sh = self._shape(slide, MSO_SHAPE.TEAR, x, y, d, d, fill=fill, line=line, line_w=line_w, adj=[1.0],
                         name=f"Goutte « {text or picto or ''} »")
        sh.rotation = {"tr": 0, "br": 90, "bl": 180, "tl": 270}[corner]
        if picto:
            side = d * 0.55
            self.picto(slide, picto, x + (d - side) / 2, y + (d - side) / 2, side)
        if text:
            inner = Frame(x, y, d, d).pad(d * 0.12)
            self.text(slide, *inner, f"**{text}**", size=size, align="center", anchor="middle",
                      color=WHITE if fill == NAVY else NAVY, line_spacing=1.1)
        return sh

    # ---------- le style filaire des modèles OCTO (references/modeles.md, « Le style filaire OCTO ») ----------
    def medaillon(self, slide, cx, cy, d=0.9, picto=None, number=None, text=None, fill=WHITE, size=10):
        """Médaillon (modèles 98 à 100, 145, 156) : cercle au trait fin centré en (cx, cy), picto bichrome au centre
        (55 % du diamètre), et en option une pastille numérotée « 01 » à coins opposés arrondis, en bas à droite.
        C'est ainsi que les modèles posent un picto dans un contenu : dans un médaillon, pas nu au milieu du texte.
        text : un mot ou un chiffre à la place du picto. Le médaillon peut chevaucher le bord d'une carte (à cheval) :
        le contrôle de mise en page ne le compte pas comme un bloc. Renvoie le cercle."""
        circ = self._shape(slide, MSO_SHAPE.OVAL, cx - d / 2, cy - d / 2, d, d, fill=fill, line=NAVY,
                           name=f"Médaillon « {picto or text or ''} »")
        if picto:
            side = d * 0.55
            pic = self.picto(slide, picto, cx - side / 2, cy - side / 2, side)
            pic.left = Inches(cx) - pic.width // 2
        if text:
            self.text(slide, *Frame(cx - d / 2, cy - d / 2, d, d).pad(d * 0.12), f"**{text}**", size=size,
                      align="center", anchor="middle", line_spacing=1.0)
        if number is not None:
            pw, ph = d * 0.56, min(d * 0.21, 0.29)
            tab = self._shape(slide, MSO_SHAPE.ROUND_2_DIAG_RECTANGLE, cx, cy + d * 0.29, pw, ph, fill=WHITE,
                              line=NAVY, adj=[0.4, 0.0], name=f"Médaillon numéro {number}")
            self._fill_text(tab.text_frame, f"**{number:02d}**" if isinstance(number, int) else f"**{number}**",
                            max(7, min(size, ph * 72 * 0.55)), NAVY, "center", "middle", line_spacing=1.0)
            tab.text_frame.margin_top = tab.text_frame.margin_bottom = 0
        return circ

    def target_dot(self, slide, cx, cy, d=0.28):
        """Puce cible (modèles 97, 153 à 155) : anneau au trait et point turquoise au centre ; repère d'un onglet,
        d'un jalon ou d'une étape. d reste sous 0,3 pouce : la puce n'est pas un bloc pour le contrôle."""
        self._shape(slide, MSO_SHAPE.OVAL, cx - d / 2, cy - d / 2, d, d, fill=WHITE, line=NAVY,
                    name="Puce cible")
        r = d * 0.27
        return self._shape(slide, MSO_SHAPE.OVAL, cx - r, cy - r, 2 * r, 2 * r, fill=TURQ, line=NAVY,
                           name="Puce cible (point)")

    def numero(self, slide, cx, y, number, d=0.8, stem=0.6, size=16):
        """Numéro d'étape au trait (modèle 97) : « 1. » dans une goutte cerclée centrée sur cx, une puce cible à son
        pied, puis un filet vertical de stem pouces qui mène au texte de l'étape. Renvoie l'ordonnée du bas du filet,
        où poser le texte."""
        self.goutte(slide, cx - d / 2, y, d, corner="tr", text=f"{number}.", size=size)
        self.target_dot(slide, cx + d * 0.27, y + d * 0.92)
        if stem:
            self.rule(slide, cx + d * 0.27, y + d * 0.92 + 0.14, cx + d * 0.27, y + d * 0.92 + 0.14 + stem,
                      color=NAVY)
        return y + d * 0.92 + 0.14 + stem

    def tab_card(self, slide, x, y, w, h, tab, body=None, tab_w=None, tab_h=0.37, size=10, tab_size=10,
                 fill=WHITE, radius=0.3):
        """Carte à onglet (modèles 153 à 155) : onglet au trait posé sur le bord haut, qui porte le titre, une puce
        cible à cheval sur le bord gauche, et le corps au trait dessous (coin haut droit arrondi). La façon OCTO de
        titrer une rubrique, plutôt qu'un aplat. Renvoie la zone intérieure du corps (pour y poser autre chose)."""
        tab_w = tab_w or max(w * 0.45, text_width(f"**{tab}**", tab_size) + 0.6)  # même largeur sur une série
        onglet = self._shape(slide, MSO_SHAPE.ROUND_1_RECTANGLE, x, y, tab_w, tab_h, fill=fill, line=NAVY,
                             adj=[0.5], name=f"Onglet « {tab} »")
        self._fill_text(onglet.text_frame, f"**{tab}**", tab_size, NAVY, "left", "middle", line_spacing=1.0)
        onglet.text_frame.margin_left = Inches(0.24)
        onglet.text_frame.margin_top = onglet.text_frame.margin_bottom = 0
        self.target_dot(slide, x, y + tab_h / 2)
        self.bloc(slide, x, y + tab_h, w, h - tab_h, corners="tr", radius=radius, fill=fill)
        inner = Frame(x, y + tab_h, w, h - tab_h).pad(0.22, 0.14)
        if body:
            self.text(slide, inner.x - 0.08, inner.y, inner.w + 0.16, inner.h, body, size=size, line_spacing=1.3)
        return inner

    def capsule(self, slide, x, y, w, h, title=None, body=None, picto=None, number=None, size=9.5, title_size=11,
                fill=WHITE):
        """Colonne pilule (modèles 156, 157) : capsule au trait aux bouts entièrement arrondis ; en haut un numéro
        cerclé (number, modèle 157), puis le titre et le texte centrés ; en pied un médaillon (picto, modèle 156).
        Pour 4 à 6 étapes, piliers ou familles côte à côte. Renvoie la capsule."""
        cap = self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=fill, line=NAVY, adj=[0.5],
                          name=f"Capsule « {title or ''} »")
        top = y + w * 0.18
        if number is not None:
            dn = min(w * 0.42, 0.55)
            self.medaillon(slide, x + w / 2, top + dn / 2, dn, text=str(number), size=13)
            top += dn + 0.1
        dm, margin = min(w * 0.6, 0.95), min(w * 0.12, 0.2)  # médaillon de pied, plafonné sur une capsule large
        bottom = y + h - (dm + margin if picto else w * 0.3)
        if picto:
            self.medaillon(slide, x + w / 2, y + h - margin - dm / 2, dm, picto=picto)
        txt = "\n".join(part for part in (f"**{title}**" if title else None, body) if part)
        if txt:
            self.text(slide, x + 0.1, top, w - 0.2, max(bottom - top, 0.3), txt, size=size, align="center",
                      anchor="middle", line_spacing=1.25)
        return cap

    def steps(self, slide, x, y, labels, active=0, w=None, h=0.34, gap=0.05, size=11):
        """Onglets d'étapes (modèle 8, « Trackers ») : coins opposés arrondis, l'étape en cours en marine à texte blanc,
        les autres en blanc cerné de marine. Situe la slide dans un parcours (phases d'une démarche, partie d'un deck).
        w : largeur de chaque onglet (défaut : ajustée à son texte). Renvoie les formes."""
        out = []
        for i, label in enumerate(labels):
            tw = w or text_width(f"**{label}**", size) + 0.45
            on = i == active
            sh = self._shape(slide, MSO_SHAPE.ROUND_2_DIAG_RECTANGLE, x, y, tw, h, fill=NAVY if on else WHITE,
                             line=None if on else NAVY, adj=[0.38, 0.0])
            self._fill_text(sh.text_frame, f"**{label}**" if on else label, size, WHITE if on else NAVY, "center",
                            "middle", line_spacing=1.0)
            sh.text_frame.margin_top = sh.text_frame.margin_bottom = 0
            out.append(sh)
            x += tw + gap
        return out

    def tracker(self, slide, x, y, w, number, text, h=0.33, active=True, size=11):
        """Jalon numéroté (modèle 8) : goutte « 1. » cerclée de marine, posée sur une pilule gris clair qui porte le
        texte. active=False : jalon à venir, contour et texte estompés. Renvoie la pilule."""
        line, color = (NAVY, NAVY) if active else (NAVY_30, NAVY_60)
        pill = self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x + h / 2, y, w - h / 2, h, fill=NAVY_10 if active
                           else WHITE, line=line, adj=[0.5])
        self._fill_text(pill.text_frame, text, size, color, "center", "middle", line_spacing=1.0)
        pill.text_frame.margin_left = Inches(h / 2 + 0.08)
        pill.text_frame.margin_top = pill.text_frame.margin_bottom = 0
        drop = self._shape(slide, MSO_SHAPE.TEAR, x, y, h, h, fill=WHITE, line=line, adj=[1.0])
        drop.rotation = 90
        tf = self.text(slide, x, y, h, h, f"{number}.", size=size, color=color, align="center", anchor="middle",
                       line_spacing=1.0).text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        return pill

    def separator(self, slide, x, y, w=1.0, kind="accent"):
        """Séparateurs de la Com (modèle 9) : "accent" (barre marine courte suivie d'une barre turquoise, pour
        ouvrir une rubrique), "line" (filet gris clair), "dots" (pointillés marine), "bold" (barre turquoise épaisse
        à bouts ronds)."""
        if kind == "accent":
            for i, color in enumerate((NAVY, TURQ)):
                self._shape(slide, MSO_SHAPE.RECTANGLE, x + i * 0.4, y - 0.03, 0.35, 0.06, fill=color, line=None)
        elif kind == "bold":
            self._bar(slide.shapes, (x, y), (x + w, y), 0.07, TURQ)
        else:
            self.rule(slide, x, y, x + w, y, color=NAVY_30 if kind == "line" else NAVY, dash=kind == "dots")

    # ---------- blocs composés ----------
    def card(self, slide, x, y, w, h, lead, body, picto=None, size=10.5):
        """Carte à coins diagonaux arrondis : lead en gras plus gros + explication. Picto qui chevauche le coin haut gauche."""
        sh = self._shape(slide, MSO_SHAPE.ROUND_2_DIAG_RECTANGLE, x, y, w, h, fill=WHITE, line_w=1, adj=[0.0, 0.3])
        tf = sh.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.15)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = 1.2
        for chunk, bold, turq, sz in [(lead + " ", True, False, size + 3)] + [(t, b, q, size) for t, b, q in
                                                                                _runs(body)]:
            r = p.add_run()
            r.text = chunk
            r.font.name = FONT
            r.font.size = Pt(sz)
            r.font.bold = bold
            r.font.color.rgb = NAVY
        if picto:
            self.picto(slide, picto, x - 0.28, y - 0.25, 0.6)
        return sh

    def column(self, slide, x, y, w, h, header, body, picto=None, header_h=0.44, size=9.5):
        """Colonne : picto au-dessus relié par un filet, en-tête à coins hauts arrondis, corps encadré."""
        if picto:
            self.picto(slide, picto, x + w / 2 - 0.35, y - 1.0, 0.7)
            line = self._connector(slide.shapes, Inches(x + w / 2), Inches(y - 0.25),
                                              Inches(x + w / 2), Inches(y))
            line.line.color.rgb = NAVY
            line.line.width = Pt(0.5)
            line.line.dash_style = 4
        hd = self._shape(slide, MSO_SHAPE.ROUND_2_SAME_RECTANGLE, x, y, w, header_h, fill=WHITE, line_w=0.75,
                         adj=[0.34, 0.0])
        self._fill_text(hd.text_frame, f"**{header}**", 11, NAVY, "center", "middle")
        bd = self._shape(slide, MSO_SHAPE.ROUND_1_RECTANGLE, x, y + header_h, w, h - header_h, fill=WHITE,
                         line_w=0.75, adj=[0.08])
        self._fill_text(bd.text_frame, body, size, NAVY, "left", "top")
        return bd

    def band(self, slide, x, y, w, h, lead, body, picto=None, size=10):
        """Bande pleine largeur (liste de constats) : picto à gauche, lead en gras puis explication."""
        self._shape(slide, MSO_SHAPE.RECTANGLE, x, y, w, h, fill=WHITE, line_w=0.75, name=f"Bande « {lead} »")
        tx = x + (0.85 if picto else 0.15)
        if picto:
            self.picto(slide, picto, x + 0.12, y + (h - 0.6) / 2, 0.6)
        self.text(slide, tx, y + 0.05, w - (tx - x) - 0.15, h - 0.1, f"**{lead}** {body}", size=size,
                  anchor="middle")
        return x, y, w, h

    def chip(self, slide, x, y, w, text, number=None, h=0.24):
        """Pastille turquoise clair (brique, techno), avec numéro rond optionnel."""
        sh = self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=TURQ_70, adj=[0.17])
        self._fill_text(sh.text_frame, text, 8, NAVY, "center", "middle")
        if number:
            self.picto(slide, f"num_{number}", x - 0.05, y - 0.08, 0.22)
        return sh

    def takeaway(self, slide, text, picto=None, y=4.6):
        """Phrase de conclusion en bas de slide, en gras, avec picto à gauche."""
        if picto:
            self.picto(slide, picto, 0.5, y - 0.05, 0.6)
        self.text(slide, 1.2 if picto else 0.6, y, 8.1, 0.6, f"**{text}**", size=12, anchor="middle")

    def banner(self, slide, x, y, w, h, text, fill=NAVY, picto=None, corners="tr", size=10.5, radius=0.3):
        """Bandeau de message dans un bloc plein : ce qu'il faut retenir, une analogie, une ambition. Picto à
        gauche (déclinaison blanche sur marine), texte centré verticalement, blanc sur marine, marine sinon."""
        self.bloc(slide, x, y, w, h, corners=corners, radius=radius, fill=fill)
        tx = x + 0.22
        if picto:
            self.picto(slide, f"blanc/{picto}" if fill == NAVY and "/" not in picto else picto, tx, y + h / 2 - 0.2,
                       0.4)
            tx += 0.55
        return self.text(slide, tx - 0.08, y, x + w - tx - 0.1, h, text, size=size,
                         color=WHITE if fill == NAVY else NAVY, anchor="middle", line_spacing=1.3)

    def chat(self, slide, x, y, w, messages, size=8.5, gap=0.08, ratio=0.86, heights=None):
        """Échange en bulles, pour montrer par l'exemple ce que répond un modèle : messages = [("Vous", texte),
        ("Le modèle", texte), …]. Les messages de « Vous » sont à droite sur gris pâle, les réponses à gauche sur
        blanc. heights : hauteur de chaque bulle, pour aligner les bulles de plusieurs colonnes (une même demande
        posée à chaque étape) ; par défaut, mesurée sur le texte. Renvoie l'ordonnée sous la dernière bulle."""
        bw = w * ratio
        for k, (who, msg) in enumerate(messages):
            txt = f"**{who}** : {msg}"
            bh = heights[k] if heights else text_height(txt, bw, size) + 0.02
            mine = who.lower() in ("vous", "utilisateur", "moi")
            self.box(slide, x + w - bw if mine else x, y, bw, bh, txt, size=size, fill=NAVY_10 if mine else WHITE,
                     align="left")
            y += bh + gap
        return y - gap

    def quote(self, slide, x, y, w, h, text, size=9, align="center"):
        """Verbatim entre guillemets typographiques, mots clés en gras."""
        return self.text(slide, x, y, w, h, f"“{text}”", size=size, align=align)

    def persona(self, slide, x, y, picto, label, size=0.75):
        """Avatar OCTO + étiquette dans un petit cadre arrondi."""
        self.picto(slide, picto, x, y, size)
        self.box(slide, x - 0.25, y + size + 0.02, size + 0.5, 0.22, f"**{label}**", size=6.5)

    def _dashed_rule(self, slide, x1, x2, y, color=NAVY):
        line = self._connector(slide.shapes, Inches(x1), Inches(y), Inches(x2), Inches(y))
        line.line.color.rgb = color
        line.line.width = Pt(1)
        line.line.dash_style = 4
        return line

    def label(self, slide, x, y, text, w=None, h=0.2, size=7.5, fill=TURQ_30):
        """Étiquette pilule (« Ambition », « Le why ») : fond turquoise, texte marine gras."""
        w = w or text_width(f"**{text}**", size) + 0.3  # largeur mesurée en Outfit gras, marges et arrondis compris
        sh = self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=fill, line=None, adj=[0.5])
        self._fill_text(sh.text_frame, f"**{text}**", size, NAVY, "center", "middle")
        sh.text_frame.margin_top = sh.text_frame.margin_bottom = 0
        return sh

    def panel(self, slide, x, y, w, h, tag=None, corner="tr"):
        """Zone foncée d'une slide contrastée : aplat marine à un grand coin arrondi (« tr » haut droit, « tl » haut
        gauche), étiquette pilule optionnelle. Y poser du texte blanc (color=WHITE), des ==mots-clés== turquoise,
        des kpi(dark=True) ou des pictos « blanc/<nom> ». Un seul panneau par slide, jamais la page entière.
        Le panneau ne descend pas sous y = 5,05 à droite de x = 9,2 : la pastille du numéro de page doit rester visible."""
        assert not (x + w > 9.2 and y + h > 5.05), "panneau sur la pastille du numéro de page : réduire h ou w"
        sh = self._shape(slide, MSO_SHAPE.ROUND_1_RECTANGLE, x, y, w, h, fill=NAVY, line=None, adj=[0.17],
                         name=f"Panneau « {tag} »" if tag else "Panneau marine")
        if corner == "tl":
            sh._element.spPr.find(qn("a:xfrm")).set("flipH", "1")
        if tag:
            self.label(slide, x + 0.22, y + 0.22, tag, h=0.22, size=8.5, fill=TURQ_70)
        return sh

    def why_panel(self, slide, x, y, w, h, statement, intro=None, bullets=(), tag="Le why", split=0.52, size=10.5,
                  bullet_size=7):
        """Panneau « why » d'une vue d'ensemble : aplat marine à grand coin arrondi en haut à droite, étiquette,
        phrase-ambition blanche avec ==mots-clés== turquoise, filet pointillé, puis puces chevron « lead. suite »."""
        self._shape(slide, MSO_SHAPE.ROUND_1_RECTANGLE, x, y, w, h, fill=NAVY, line=None, adj=[0.17],
                    name=f"Panneau « {tag} »")
        self.label(slide, x + 0.22, y + 0.22, tag, h=0.22, size=8.5, fill=TURQ_70)
        sep = y + h * split
        self.text(slide, x + 0.16, y + 0.55, w - 0.4, sep - y - 0.6, statement, size=size, color=WHITE,
                  bold=True, line_spacing=1.1)
        self._dashed_rule(slide, x + 0.22, x + w - 0.22, sep, NAVY_30)
        lines = ([intro] if intro else []) + [f"> {b}" for b in bullets]
        tb = self.text(slide, x + 0.16, sep + 0.08, w - 0.4, y + h - sep - 0.15, "\n".join(lines),
                       size=bullet_size, color=WHITE, line_spacing=1.2)
        for p in tb.text_frame.paragraphs:
            p.space_before = Pt(3)
        return tb

    def pillar_card(self, slide, x, y, w, h, number, title, body, detail=None, picto=None, tag="Ambition",
                    split=0.58, size=6, title_size=8.5):
        """Carte de pilier d'une vue d'ensemble : onglet « .01 » posé sur le bord haut, titre gras sur 1 ou 2 lignes,
        picto en haut à droite, description, filet pointillé, étiquette (« Ambition ») et détail."""
        self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=WHITE, line_w=1.25, adj=[0.09],
                    name=f"Carte « {title} »")
        tab = self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x + 0.15, y - 0.11, 0.36, 0.22, fill=WHITE,
                          line_w=1.25, adj=[0.5])
        tf = tab.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        # Point turquoise du numéro, comme le « .12 » des numéros de page du template.
        for chunk, color in [(".", TURQ), (str(number).lstrip("."), NAVY)]:
            r = p.add_run()
            r.text = chunk
            r.font.name, r.font.size, r.font.bold = FONT, Pt(8.5), True
            r.font.color.rgb = color
        if picto:
            self.picto(slide, picto, x + w - 0.5, y + 0.12, 0.4)
        self.text(slide, x + 0.1, y + 0.1, w - (0.6 if picto else 0.2), 0.38, f"**{title}**", size=title_size,
                  line_spacing=1.0, anchor="middle")
        sep = y + h * split if detail else y + h - 0.1
        self.text(slide, x + 0.08, y + 0.5, w - 0.13, sep - y - 0.52, body, size=size, line_spacing=1.05)
        if detail:
            self._dashed_rule(slide, x + 0.15, x + w - 0.15, sep)
            self.label(slide, x + 0.13, sep + 0.06, tag, h=0.16, size=size + 0.5)
            self.text(slide, x + 0.08, sep + 0.22, w - 0.13, y + h - sep - 0.24, detail, size=size, line_spacing=1.05)

    def timeline(self, slide, items, y=2.6, x0=0.8, x1=9.3):
        """Frise horizontale : flèche marine épaisse, jalons en anneaux turquoise, libellés alternés haut / bas.
        items = [(libellé, texte), ...]."""
        self.arrow(slide, x0, y, x1, y, elbow=False)
        step = (x1 - x0 - 0.4) / max(len(items), 1)
        for i, (label, body) in enumerate(items):
            cx = x0 + 0.2 + step * (i + 0.5)
            up = i % 2 == 0
            self._shape(slide, MSO_SHAPE.OVAL, cx - 0.08, y - 0.08, 0.16, 0.16, fill=TURQ, line=NAVY)
            ty = y - 0.85 if up else y + 0.25
            c = self._connector(slide.shapes, Inches(cx), Inches(y - 0.22 if up else y),
                                           Inches(cx), Inches(y if up else y + 0.22))
            c.line.color.rgb = NAVY
            c.line.width = Pt(0.66)
            self.text(slide, cx - step / 2, ty, step, 0.22, label, size=8, align="center", bold=True)
            self.text(slide, cx - step / 2, ty + 0.22, step, 0.4, body, size=7.5, align="center")

    # ---------- tableaux et chiffres clés (references/graphiques-tableaux.md) ----------
    def table(self, slide, x, y, w, rows, col_widths=None, row_h=0.3, size=9):
        """Tableau OCTO : en-tête marine (texte blanc gras), corps blanc à filets verticaux marine,
        lignes séparées en pointillés, bande turquoise en pied. rows[0] = en-têtes. Tableau natif, éditable."""
        n_rows, n_cols = len(rows) + 1, len(rows[0])
        col_widths = col_widths or [w / n_cols] * n_cols
        gf = slide.shapes.add_table(n_rows, n_cols, Inches(x), Inches(y), Inches(w), Inches(row_h * len(rows) + 0.17))
        tbl = gf.table
        tbl.first_row = False
        tbl.horz_banding = False
        for j, cw in enumerate(col_widths):
            tbl.columns[j].width = Inches(cw)
        for i in range(n_rows):
            tbl.rows[i].height = Inches(0.17 if i == n_rows - 1 else row_h)
            for j in range(n_cols):
                cell = tbl.cell(i, j)
                header, footer = i == 0, i == n_rows - 1
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY if header else TURQ if footer else WHITE
                cell.margin_top = cell.margin_bottom = Inches(0 if footer else 0.04)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                if footer:
                    cell.text_frame.paragraphs[0].font.size = Pt(4)
                else:
                    self._fill_text(cell.text_frame, rows[i][j], size, WHITE if header else NAVY,
                                    "left" if j == 0 else "center", "middle", bold=header, line_spacing=1.1)
                self._cell_borders(cell, bottom_dotted=not header and not footer)
        return gf

    def _cell_borders(self, cell, bottom_dotted):
        """Filets marine fins sur les côtés ; séparateur de ligne en pointillés pour le corps du tableau."""
        tcPr = cell._tc.get_or_add_tcPr()
        for k, side in enumerate(["a:lnL", "a:lnR", "a:lnT", "a:lnB"]):
            ln = etree.Element(qn(side), w=str(Pt(0.75)), cap="flat", cmpd="sng")
            fill = etree.SubElement(ln, qn("a:solidFill"))
            etree.SubElement(fill, qn("a:srgbClr")).set("val", "0E2356")
            etree.SubElement(ln, qn("a:prstDash")).set("val", "sysDot" if side == "a:lnB" and bottom_dotted else "solid")
            tcPr.insert(k, ln)

    def kpi(self, slide, x, y, w, value, label, size=28, dark=False):
        """Chiffre clé : valeur Bold très grande + libellé Regular sur la même ligne, filet pointillé dessous.
        Si le libellé ne tient pas à côté de la valeur dans la largeur w, il passe sur une ligne à lui, sous la valeur.
        dark=True sur un panneau marine : valeur turquoise, libellé blanc (charte : turquoise permis sur marine)."""
        label_size = size * 0.4
        value, label = typo(value), typo(label)
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(1))
        tf = tb.text_frame
        tf.word_wrap = True
        inner = w - Emu(tf.margin_left + tf.margin_right).inches
        # Largeurs mesurées en Outfit : le libellé passe sous la valeur s'il ne tient pas à côté d'elle.
        stacked = text_width(f"**{value} **", size) + text_width(label, label_size) > inner
        runs = [(value + ("" if stacked else " "), size, True, TURQ if dark else NAVY, 0),
                (label, label_size, False, WHITE if dark else NAVY, 1 if stacked else 0)]
        for chunk, sz, bold, color, para in runs:
            p = tf.paragraphs[0] if para == 0 else (tf.paragraphs[1] if len(tf.paragraphs) > 1 else tf.add_paragraph())
            r = p.add_run()
            r.text = chunk
            r.font.name, r.font.size, r.font.bold = FONT, Pt(sz), bold
            r.font.color.rgb = color
        # Hauteur mesurée comme le contrôle de mise en page la mesure : jamais d'alerte sur le chiffre clé lui-même.
        height = text_extent(tb)[0]
        tb.height = Inches(height)
        rule_y = y + height + 0.05 * (not stacked)
        line = self._connector(slide.shapes, Inches(x + 0.08), Inches(rule_y),
                                          Inches(x + 0.68), Inches(rule_y))
        line.line.color.rgb = NAVY_30 if dark else NAVY
        line.line.width = Pt(0.75)
        line.line.dash_style = 4
        return tb

