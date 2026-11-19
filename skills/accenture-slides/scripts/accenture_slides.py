"""Slides Accenture : la classe AccentureDeck, sur le template assets/template_accenture.pptx (starter pack de la
marque, version aux polices système) et la charte de references/charte_accenture.md. Elle ne dépend d'aucun fichier
OCTO ni La Grosse Conf : comme Deck (octo_slides.py), elle hérite de deck_base.BaseDeck, qui ne connaît aucune charte.

    import sys; sys.path.insert(0, "<skill>/scripts")
    from accenture_slides import CONTENT, AccentureDeck
    d = AccentureDeck()                       # AccentureDeck(lang="en-US") pour un deck en anglais
    d.cover("Notre offre data et IA", "Pour la direction des opérations", date="Mars 2027")
    s = d.slide("Trois leviers pour passer à l'échelle", "Le sous-titre dit la chute")
    d.etapes(s, CONTENT, [("Cadrer", "…"), ("Construire", "…"), ("Industrialiser", "…")], focal=2)
    d.save("deck.pptx")

Slide de 13,333 x 7,5 pouces. Police Arial (texte), Arial Black (titres, chiffres, intitulés), Palatino Linotype
(sous-titres de couverture et d'intercalaire). Les helpers génériques de BaseDeck (text, statement, picto, photo,
arrow, connect, fork, join, circle, rule, notes, save…) prennent la palette Accenture (TEXT, LINE, ACCENT, POINT,
BULLET, FLOW, LOOP, CHEVRON, RULE) ; picto() ne cherche que dans les icônes monoline Accenture.
"""
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Emu, Inches, Pt

import octo_layout
from pptx.enum.text import MSO_ANCHOR

from deck_base import ASSETS, AUTO, WHITE, BaseDeck, _runs

MSO_ANCHOR_MIDDLE = MSO_ANCHOR.MIDDLE
from octo_layout import Frame, lines_of, text_height

TEMPLATE = ASSETS / "template_accenture.pptx"

# Palette de la charte (starter pack, « Colors and gradients ») : trois violets cœur de marque, des violets d'accent,
# le noir, deux gris chauds et le blanc.
PURPLE = RGBColor(0xA1, 0x00, 0xFF)  # Core Purple 1 : accent, chiffres, icônes, le « > »
PURPLE_DARK = RGBColor(0x75, 0x00, 0xC0)  # Core Purple 2 : aplats, fonds de rupture
PURPLE_DARKEST = RGBColor(0x46, 0x00, 0x73)  # Core Purple 3 : fonds foncés, texte blanc
MAUVE = RGBColor(0xB4, 0x55, 0xAA)  # accent
LAVENDER = RGBColor(0xBE, 0x82, 0xFF)  # accent clair : aplats secondaires, jamais de texte dessus en blanc
LILAC = RGBColor(0xDC, 0xAF, 0xFF)  # accent très clair : fonds, mot-clé sur fond foncé
LILAC_LIGHT = RGBColor(0xE6, 0xDC, 0xFF)  # sous-titre de couverture sur fond foncé
BLACK = RGBColor(0x00, 0x00, 0x00)  # texte courant, titres
GREY = RGBColor(0x96, 0x96, 0x8C)  # gris chaud : traits, texte secondaire en grand
GREY_LIGHT = RGBColor(0xE6, 0xE6, 0xDC)  # gris très clair : fonds de panneau, filets

# Bibliothèque de visuels Accenture : picto() ne cherche que là (jamais dans celles d'OCTO ou de La Grosse Conf).
VISUAL_DIRS = [ASSETS / "pictos-accenture"]

HEADLINE = "Arial Black"  # titres, chiffres clés, intitulés de carte
SERIF = "Palatino Linotype"  # sous-titres (couverture, intercalaire, sommaire)

# Layouts du template (noms exacts, voir references/layouts_accenture.md).
LAYOUTS = {
    "cover": "Cover Basic - Dark, White Text",
    "cover_light": "Cover Basic - Light, Black Text",
    "cover_image": "Cover Image - Left-aligned, Logo",
    "agenda": "Agenda",
    "section_dark": "Section Divider - Numbered, Gradient Dark Purple",
    "section_mid": "Section Divider - Numbered, Gradient Mid Purple",
    "section_core": "Section Divider - Numbered, Gradient Core Purple",
    "section_light": "Section Divider - Numbered, Gradient Light",
    "message_dark": "Key Message Gradient Dark 1",
    "message_light": "Key Message Gradient Light 1",
    "message_purple": "Key Message Mid Purple",
    "content": "Title and Content - Light",
    "content_dark": "Title and Content - Dark",
    "blank": "Blank - Light",
    "blank_dark": "Blank - Dark",
    "headline_serif": "Columns 2 - Headline + GT Sectra",
    "columns_3": "Columns 3 - List",
    "columns_4": "Columns 4 - List",
    "stat": "Stat 1",
    "quote": "Quote + Portrait 1",
    "text_image": "Text and Image 1",
    "closing": "Greetings + Greater Than L",
    "closing_gradient": "Greetings + Greater Than L Gradient",
}

# Zone de contenu d'une slide de contenu : sous le titre (et son sous-titre), au-dessus du pied de page (logo « > »,
# copyright et numéro de page, y > 7,0).
CONTENT = Frame(0.42, 1.75, 12.5, 5.1)
SLIDE = Frame(0, 0, 13.333, 7.5)


class AccentureDeck(BaseDeck):
    """Deck Accenture : template, palette et icônes de la marque (references/charte_accenture.md)."""
    TEMPLATE = TEMPLATE
    VISUAL_DIRS = VISUAL_DIRS
    TEXT = POINT = BLACK  # texte noir, pas de point final coloré
    LINE = GREY
    RULE = GREY_LIGHT
    FLOW = CHEVRON = PURPLE  # flèches et chevrons violets
    LOOP = PURPLE_DARK
    ACCENT = LILAC  # mot-clé ==…== sur fond foncé
    BULLET = "A100FF"
    PHOTO_SHAPE = "droit"  # photos à angles droits
    CHARTE = "accenture"
    CHARTE_FILE = "references/charte_accenture.md"
    MISE_EN_PAGE = "references/style_accenture.md"
    FONT = "Arial"

    def __init__(self, template=TEMPLATE, target="pptx", lang=None):
        """lang : langue du texte (« fr-FR » par défaut, « en-US »…) ; hors français, pas d'espace insécable avant
        « : ; ! ? »."""
        if lang:
            self.LANG = lang
        self._dark = set()  # slides à fond foncé (slide(dark=True), blank(dark=True)) : texte blanc par défaut
        super().__init__(template, target)

    def save(self, path):
        """Enregistre (voir BaseDeck.save). Pour Google Slides, rappelle les polices à vérifier après import."""
        out = super().save(path)
        if self.target == "gslides":
            print("Google Slides : après import, vérifier qu'Arial Black (titres) et Palatino Linotype (sous-titres) "
                  "ne sont pas remplacés ; sinon les choisir dans le menu des polices (charte_accenture.md).")
        return out

    def _on_dark(self, slide):
        return slide.slide_id in self._dark

    def text(self, slide, x, y, w, h, text, size=10, color=AUTO, align="left", anchor="top", bold=False,
             line_spacing=None):
        """Zone de texte balisé (voir BaseDeck.text). Sur une slide foncée (slide(dark=True), blank(dark=True)), le
        texte est blanc par défaut."""
        if color == AUTO and self._on_dark(slide):
            color = WHITE
        return super().text(slide, x, y, w, h, text, size, color, align, anchor, bold, line_spacing)

    # ---------- texte ----------
    def headline(self, slide, x, y, w, h, text, size=20, color=None, align="left", anchor="top"):
        """Intitulé en Arial Black (titre de carte, de colonne, chiffre) : la graisse de la marque pour les titres.
        h=None : hauteur ajustée au texte mesuré. color : noir par défaut, blanc sur une slide foncée."""
        color = (WHITE if self._on_dark(slide) else BLACK) if color is None else color
        auto = h is None
        if auto:
            h = self._measure(text, w, size, HEADLINE) + size / 72 * 0.3 + 0.06  # jambages de l'Arial Black
        tb = self.text(slide, x, y, w, h, text, size=size, color=color, align=align, anchor=anchor,
                       line_spacing=1.0)
        if auto:
            tb.text_frame.margin_top = Inches(0.1)  # l'Arial Black monte au-dessus de la marge par défaut (0,04)
        self._set_font(tb, HEADLINE)
        return tb

    def serif(self, slide, x, y, w, h, text, size=20, color=None, align="left", anchor="top"):
        """Texte en Palatino Linotype (sous-titre, accroche, citation), violet par défaut, lilas sur une slide
        foncée."""
        color = (LILAC if self._on_dark(slide) else PURPLE) if color is None else color
        if h is None:
            h = self._measure(text, w, size, "Arial", line_spacing=1.2)
        tb = self.text(slide, x, y, w, h, text, size=size, color=color, align=align, anchor=anchor, line_spacing=1.2)
        self._set_font(tb, SERIF)
        return tb

    @staticmethod
    def _set_font(shape, font):
        for p in shape.text_frame.paragraphs:
            for r in p.runs:
                r.font.name = font
                if font == HEADLINE:
                    r.font.bold = False  # Arial Black est déjà la graisse lourde

    @staticmethod
    def _measure(text, w, size, font, line_spacing=1.0):
        """Hauteur d'un texte dans une police donnée (Arial Black : Liberation Sans Bold élargie)."""
        previous = octo_layout.FONT
        octo_layout.use_font(font)
        try:
            return text_height(text, w, size, bold=font == HEADLINE, line_spacing=line_spacing)
        finally:
            octo_layout.use_font(previous)

    def _fit_title(self, ph, text, base=36, lines=1):
        """Titre du layout en Arial Black, mesuré comme tel, réduit (jusqu'à 12 pt) s'il ne tient pas sur lines
        lignes ; sur plusieurs lignes, 15 % de marge pour les coupures aux mots."""
        tf = ph.text_frame
        avail = Emu(ph.width - tf.margin_left - tf.margin_right).inches * lines * (0.85 if lines > 1 else 1)
        previous = octo_layout.FONT
        octo_layout.use_font(HEADLINE)
        try:
            width = octo_layout.text_width("**" + text.replace("\n", " ").replace("**", "") + "**", base)
        finally:
            octo_layout.use_font(previous)
        if width <= avail:
            return
        size = max(12, int(base * avail / width))
        for p in tf.paragraphs:
            for r in p.runs:
                r.font.size = Pt(size)
        if size == 12:
            print(f"⚠ titre trop long pour ce layout, même à 12 pt : « {text[:40]}… » ; le raccourcir")

    def _flush_left(self, ph, text):
        """Retire le retrait suspendu que le layout pose sur ses placeholders (sous-titres, accroches) des lignes
        sans puce : sinon la 2e ligne est décalée. Une ligne « - » reçoit la puce violette de la charte si le layout
        n'en pose pas."""
        from pptx.oxml.ns import qn
        for p, line in zip(ph.text_frame.paragraphs, lines_of(text)):
            if line.startswith("- "):
                if not self._layout_bullet(ph):
                    self._bullet(p)
                    # Retrait à l'échelle du texte du layout (20 pt et plus) : celui de _bullet vaut pour 10 à 14 pt.
                    size = self._layout_size(ph) or 14
                    p._p.pPr.set("marL", str(Inches(0.018 * size)))
                    p._p.pPr.set("indent", str(-Inches(0.014 * size)))
            else:
                pPr = p._p.get_or_add_pPr()
                pPr.set("marL", "0")
                pPr.set("indent", "0")

    # ---------- layouts ----------
    def layout(self, name, texts=None, visuals=None, fit_title=1):
        """Slide sur un layout du template, désigné par son nom complet (« Agenda ») ou une clé de LAYOUTS
        (« section_dark »). texts : {idx du placeholder: texte balisé}, le style du layout est conservé ; un
        placeholder absent de texts est supprimé. visuals : un élément par placeholder image, dans l'ordre des idx :
        chemin d'une photo ou nom d'une icône. Un emplacement sans visuel est supprimé : jamais de cadre vide.
        fit_title : nombre de lignes permises au titre avant de le réduire (0 : jamais réduit)."""
        layout = self._layouts[LAYOUTS.get(name, name)]
        s = self.prs.slides.add_slide(layout)
        texts, visuals = texts or {}, list(visuals or [])
        pictures = sorted((ph for ph in s.placeholders if ph.placeholder_format.type == 18),  # PICTURE
                          key=lambda ph: ph.placeholder_format.idx)
        for ph in list(s.placeholders):
            idx = ph.placeholder_format.idx
            if ph in pictures:
                continue
            if texts.get(idx):
                self._fill_placeholder(ph, texts[idx])
                self._flush_left(ph, texts[idx])
                if idx == 0 and fit_title:
                    self._fit_title(ph, texts[idx], base=self._layout_size(ph) or 36, lines=int(fit_title))
            else:
                ph._element.getparent().remove(ph._element)
        for ph in pictures:
            visual = visuals.pop(0) if visuals else None
            if visual is None:
                ph._element.getparent().remove(ph._element)
            else:
                ph.insert_picture(visual if str(visual).endswith((".png", ".jpg", ".jpeg")) else self._visual(visual))
        return s

    @staticmethod
    def _layout_bullet(ph):
        """Le layout ou le masque pose-t-il une puce au premier niveau de ce placeholder ?"""
        from pptx.oxml.ns import qn
        node = ph
        while node is not None:
            lvl = node._element.find(".//" + qn("a:lstStyle") + "/" + qn("a:lvl1pPr"))
            if lvl is not None and (lvl.find(qn("a:buChar")) is not None or lvl.find(qn("a:buNone")) is not None):
                return lvl.find(qn("a:buChar")) is not None
            node = getattr(node, "_base_placeholder", None)
        return False

    @staticmethod
    def _layout_size(ph):
        """Taille (pt) du premier niveau de texte du placeholder dans son layout, ou dans le masque."""
        node = ph
        while node is not None:
            sizes = node._element.xpath(".//a:lvl1pPr/a:defRPr/@sz")
            if sizes:
                return int(sizes[0]) / 100
            node = node._base_placeholder if hasattr(node, "_base_placeholder") else None
        return None

    def cover(self, title, subtitle=None, date=None, author=None, variant="dark"):
        """Couverture : titre (Arial Black), sous-titre (Palatino), date et auteur ; le logo et le copyright sont dans
        le layout. variant : « dark » (fond violet foncé, texte blanc), « light » (fond blanc), « image » (photo de
        fond du template)."""
        name = {"dark": "cover", "light": "cover_light", "image": "cover_image"}[variant]
        layout = self._layouts[LAYOUTS[name]]
        # idx 1 et 2 n'ont pas le même rôle d'un layout à l'autre : le sous-titre est le placeholder en Palatino.
        serif = next((ph.placeholder_format.idx for ph in layout.placeholders
                      if SERIF in "".join(ph._element.xpath(".//a:latin/@typeface"))), 1)
        other = 2 if serif == 1 else 1
        return self.layout(name, {0: title, serif: subtitle, 10: date, other: author}, fit_title=2)

    def agenda(self, items, title="Agenda", intro=None):
        """Sommaire numéroté (1 à 16 entrées, sur une ou deux colonnes) ; intro : accroche en Palatino sous le titre."""
        assert 1 <= len(items) <= 16, "agenda : 1 à 16 entrées"
        texts = {0: title, 1: intro}
        for k, item in enumerate(items):
            col, row = divmod(k, 8)
            texts[2 + row if col == 0 else 21 + row] = item  # entrées : idx 2 à 9, puis 21 à 28
            texts[13 + row if col == 0 else 29 + row] = f"{k + 1:02d}"  # numéros : idx 13 à 20, puis 29 à 36
        s = self.layout("agenda", texts)
        for ph in s.placeholders:
            if 13 <= ph.placeholder_format.idx <= 20 or ph.placeholder_format.idx >= 29:
                ph.text_frame.word_wrap = False  # « 01 » sur une ligne dans sa colonne étroite
        return s

    def section(self, title, number=None, subtitle=None, style="dark"):
        """Intercalaire numéroté : grand numéro (Arial Black), titre, sous-titre en Palatino. style : « dark »,
        « mid », « core » (fonds violets en dégradé, texte blanc) ou « light »."""
        layout = self._layouts[LAYOUTS[f"section_{style}"]]
        # Le grand numéro est le placeholder du haut, quel que soit son idx (il change d'un layout à l'autre).
        others = [ph for ph in layout.placeholders if ph.placeholder_format.idx != 0]
        num = min(others, key=lambda ph: ph.top).placeholder_format.idx
        sub = max(others, key=lambda ph: ph.top + ph.left).placeholder_format.idx
        number = f"{number:02d}" if isinstance(number, int) else number
        s = self.layout(f"section_{style}", {0: title, num: number, sub: subtitle}, fit_title=2)
        for ph in s.placeholders:
            idx = ph.placeholder_format.idx
            if idx == num:
                ph.text_frame.word_wrap = False  # « 01 » sur une ligne
                if style != "light":  # blanc sur tous les dégradés violets, même ceux assez clairs pour du noir
                    for r in ph.text_frame.paragraphs[0].runs:
                        r.font.color.rgb = WHITE
        return s

    def key_message(self, text, style="dark"):
        """Message clé seul sur la slide (Arial Black, 54 pt dans le layout). style : « dark » (dégradé foncé),
        « light » (dégradé clair, texte noir) ou « purple » (aplat violet)."""
        return self.layout(f"message_{style}", {0: text}, fit_title=3)

    def slide(self, title, subtitle=None, dark=False):
        """Slide de contenu : titre en Arial Black sur une ligne (réduit si besoin), sous-titre facultatif, zone libre
        CONTENT dessous. dark=True : fond violet foncé ; les helpers y écrivent alors en blanc par défaut."""
        s = self.layout("content_dark" if dark else "content", {0: title})
        if dark:
            self._dark.add(s.slide_id)
        if subtitle:
            self.serif(s, 0.42, 1.08, 12.5, 0.5, subtitle, size=20)
        return s

    def blank(self, title=None, dark=False):
        """Slide libre : masque (logo, copyright, numéro de page) et titre facultatif. dark=True : fond violet foncé,
        texte blanc par défaut."""
        s = self.layout("blank_dark" if dark else "blank", {0: title})
        if dark:
            self._dark.add(s.slide_id)
        return s

    def closing(self, text="Merci", gradient=False):
        """Slide de fin : grand « > » de la marque et un mot (« Merci », « Questions ? »)."""
        return self.layout("closing_gradient" if gradient else "closing", {0: text}, fit_title=2)

    # ---------- composants ----------
    def gt(self, slide, x, y, h, color=None):
        """Le « > » de la marque (Greater Than), plein, de hauteur h : signature visuelle, ou flèche entre deux
        blocs. Un seul par slide en dehors du masque."""
        color = PURPLE if color is None else color
        w = h * 0.78
        pts = [(0, 0), (1, 0.39), (1, 0.61), (0, 1), (0, 0.76), (0.66, 0.5), (0, 0.24)]
        ff = slide.shapes.build_freeform(Inches(x), Inches(y), scale=1.0)
        ff.add_line_segments([(Inches(x + px * w), Inches(y + py * h)) for px, py in pts[1:]] +
                             [(Inches(x), Inches(y))], close=True)
        sh = ff.convert_to_shape()
        sh.name = "Greater Than"
        sh.fill.solid()
        sh.fill.fore_color.rgb = color
        sh.line.fill.background()
        sh.shadow.inherit = False
        return sh

    def chiffre(self, slide, x, y, w, value, label, size=54, color=None):
        """Chiffre clé : valeur en Arial Black violette, libellé en dessous. Renvoie la zone de la valeur."""
        color = (LILAC if self._on_dark(slide) else PURPLE) if color is None else color
        vh = size / 72 * 1.5
        tb = self.headline(slide, x, y, w, vh, value, size=size, color=color, anchor="bottom")
        self.text(slide, x, y + vh + 0.05, w, None, label, size=14)
        return tb

    def point(self, slide, x, y, w, h, number, title, body="", frame=True, size=12):
        """Case numérotée façon starter pack (« 1. » violet, intitulé en Arial Black, texte court) dans un cadre gris
        clair : une règle, un principe, une étape indépendante. h=None : hauteur ajustée au contenu (pour aligner une
        rangée de cases, leur donner la plus grande, point_height). Renvoie la forme du cadre."""
        pad = 0.15
        h = h or self.point_height(w, title, body, size)
        sh = self._shape(slide, MSO_SHAPE.RECTANGLE, x, y, w, h, fill=None, line=GREY_LIGHT if frame else None,
                         name=f"Case « {title} »")
        top = y + pad
        self.text(slide, x + pad, top, w - 2 * pad, 0.3, f"**{number}.**", size=12, color=PURPLE, line_spacing=1.0)
        head_h = self._measure(title, w - 2 * pad, 18, HEADLINE)
        self.headline(slide, x + pad, top + 0.32, w - 2 * pad, head_h, title, size=18)
        top += 0.32 + head_h + 0.08
        if body:
            self.text(slide, x + pad, top, w - 2 * pad, y + h - top - pad, body, size=size)
        return sh

    def point_height(self, w, title, body="", size=12):
        """Hauteur d'une case point() à son contenu."""
        pad = 0.15
        h = 2 * pad + 0.32 + self._measure(title, w - 2 * pad, 18, HEADLINE) + 0.08
        return h + (text_height(body, w - 2 * pad, size) if body else 0)

    def colonnes(self, slide, zone, items, numbered=True, size=13):
        """Colonnes côte à côte (2 à 5) façon layouts « Columns » : numéro violet, intitulé en Arial Black, filet
        violet court, texte. items : [(intitulé, texte), …]. Renvoie les zones des colonnes."""
        assert 2 <= len(items) <= 5, "colonnes : 2 à 5"
        cols = zone.cols(len(items), gap=0.4)
        heads = [self._measure(t, c.w, 20, HEADLINE) for c, (t, _) in zip(cols, items)]
        head_h = max(heads)
        for k, (col, (title, body)) in enumerate(zip(cols, items)):
            top = col.y
            if numbered:
                self.text(slide, col.x, top, col.w, 0.45, f"{k + 1:02d}", size=24, color=PURPLE, line_spacing=1.0)
                top += 0.55
            self.headline(slide, col.x, top, col.w, head_h, title, size=20)
            top += head_h + 0.1
            self.rule(slide, col.x + 0.08, top, col.x + 0.68, top, color=PURPLE, width=2.25)
            top += 0.2
            self.text(slide, col.x, top, col.w, col.y + col.h - top, body, size=size)
        return cols

    def carte(self, slide, x, y, w, h, picto, title, body="", size=12, dark=None):
        """Carte à icône : icône monoline violette (blanche si dark), intitulé en gras, texte court ; sans cadre, un
        filet violet sous l'icône. dark : par défaut, celui de la slide (slide(dark=True)). picto : nom d'une icône
        de assets/pictos-accenture. Renvoie la forme de la carte (invisible, pour relier avec connect)."""
        dark = self._on_dark(slide) if dark is None else dark
        sh = self._shape(slide, MSO_SHAPE.RECTANGLE, x, y, w, h, fill=None, line=None, name=f"Carte « {title} »")
        side = min(0.7, h * 0.3)
        self.picto(slide, f"{picto}-blanc" if dark else picto, x + 0.08, y, side)
        top = y + side + 0.12
        self.rule(slide, x + 0.08, top, x + 0.58, top, color=LILAC if dark else PURPLE, width=2.25)
        top += 0.15
        color = WHITE if dark else BLACK
        text = f"**{title}**" + (f"\n{body}" if body else "")
        self.text(slide, x, top, w, y + h - top, text, size=size, color=color)
        return sh

    def aplat(self, slide, x, y, w, h, text="", fill=None, size=16, align="center"):
        """Aplat à angles droits. Texte blanc sur les violets foncés et le noir, noir sur les violets clairs et le
        gris clair."""
        fill = PURPLE if fill is None else fill
        sh = self._shape(slide, MSO_SHAPE.RECTANGLE, x, y, w, h, fill=fill, line=None)
        if text:
            dark = str(fill) in {str(c) for c in (PURPLE, PURPLE_DARK, PURPLE_DARKEST, BLACK)}
            self._fill_text(sh.text_frame, text, size, WHITE if dark else BLACK, align, "middle")
        return sh

    def etapes(self, slide, zone, items, focal=None, size=12):
        """Processus linéaire : chevrons en gris clair (texte noir), l'étape focal en violet (texte blanc), un texte
        sous chaque chevron. items : [(intitulé, texte), …] ; focal : indice de l'étape mise en avant. Renvoie les
        chevrons."""
        n = len(items)
        cols = zone.cols(n, gap=0.06)
        band = 0.9
        shapes = []
        for k, (col, (title, body)) in enumerate(zip(cols, items)):
            kind = MSO_SHAPE.PENTAGON if k == 0 else MSO_SHAPE.CHEVRON
            on = k == focal
            sh = self._shape(slide, kind, col.x, zone.y, col.w, band, fill=PURPLE if on else GREY_LIGHT, line=None,
                             adj=[0.3], name=f"Étape « {title} »")
            self._fill_text(sh.text_frame, f"**{title}**", 14, WHITE if on else BLACK, "center", "middle")
            sh.text_frame.margin_left = Inches(0.3 if k else 0.15)
            sh.text_frame.margin_right = Inches(0.3)
            shapes.append(sh)
            if body:
                self.text(slide, col.x + 0.1, zone.y + band + 0.2, col.w - 0.2, zone.h - band - 0.2, body, size=size)
        return shapes

    def de_a(self, slide, zone, avant, apres, titre_avant="Aujourd'hui", titre_apres="Demain"):
        """Passage d'un état à un autre (« From issue to outcome » du starter pack) : panneau gris clair à gauche,
        grand « > » violet au centre, panneau violet foncé à droite (texte blanc). avant, apres : textes balisés
        (puces "- " acceptées). Renvoie les deux panneaux."""
        left, mid, right = zone.cols([None, 1.0, None], gap=0.2)
        inner_w = left.w - 0.6
        need = max(self._measure(t, inner_w, 22, HEADLINE) + 0.15 + text_height(b, inner_w, 14)
                   for t, b in ((titre_avant, avant), (titre_apres, apres))) + 0.6
        h = min(zone.h, need + 0.2)
        left, right = left.place(h=h, align="mc"), right.place(h=h, align="mc")
        a = self._shape(slide, MSO_SHAPE.RECTANGLE, *left, fill=GREY_LIGHT, line=None, name=f"Panneau « {titre_avant} »")
        b = self._shape(slide, MSO_SHAPE.RECTANGLE, *right, fill=PURPLE_DARKEST, line=None,
                        name=f"Panneau « {titre_apres} »")
        for panel, title, body, color in ((left, titre_avant, avant, BLACK), (right, titre_apres, apres, WHITE)):
            inner = panel.pad(0.3)
            head_h = self._measure(title, inner.w, 22, HEADLINE)
            self.headline(slide, inner.x, inner.y, inner.w, head_h, title, size=22, color=color)
            top = inner.y + head_h + 0.15
            self.text(slide, inner.x, top, inner.w, inner.y + inner.h - top, body, size=14, color=color)
        self.gt(slide, mid.x + (mid.w - 0.62) / 2, mid.cy - 0.4, 0.8)
        return a, b

    def citation(self, slide, x, y, w, h, text, auteur, size=28):
        """Citation : texte en Arial Black, auteur en Palatino violet dessous, filet violet à gauche."""
        self.rule(slide, x, y, x, y + h, color=PURPLE, width=3)
        th = h - 0.6
        self.headline(slide, x + 0.3, y, w - 0.3, th, text, size=size, anchor="middle")
        self.serif(slide, x + 0.3, y + th + 0.1, w - 0.3, 0.45, auteur, size=16)

    def chiffres(self, slide, zone, items, size=54, gap=0.6):
        """Rangée de chiffres clés (2 à 4) centrée dans la zone : valeur en Arial Black violette, libellé dessous.
        items : [(valeur, libellé), …]. Renvoie les zones des colonnes."""
        assert 2 <= len(items) <= 4, "chiffres : 2 à 4"
        cols = zone.cols(len(items), gap=gap)
        # Taille réduite pour que la valeur la plus large tienne sur une ligne (Arial Black, marges comprises).
        previous = octo_layout.FONT
        octo_layout.use_font(HEADLINE)
        try:
            widest = max(octo_layout.text_width(f"**{value}**", size) for value, _ in items)
        finally:
            octo_layout.use_font(previous)
        if widest > cols[0].w - 0.25:
            size = max(24, int(size * (cols[0].w - 0.25) / widest))
        value_h = size / 72 * 1.5
        label_h = max(text_height(label, c.w, 14) for c, (_, label) in zip(cols, items))
        top = zone.y + max(0.0, (zone.h - value_h - 0.05 - label_h) / 2)
        for col, (value, label) in zip(cols, items):
            self.chiffre(slide, col.x, top, col.w, value, label, size=size)
        return cols

    def matrice(self, slide, zone, axe_x, axe_y, quadrants, focal=None, graduations=("Faible", "Fort"), size=13):
        """Matrice 2 x 2 : quatre cases gris clair, la case focal en violet (texte blanc), axes nommés avec leurs
        graduations. quadrants : [(intitulé, texte), …] dans l'ordre haut gauche, haut droite, bas gauche, bas droite ;
        focal : indice de la case mise en avant. Renvoie les quatre cases."""
        assert len(quadrants) == 4, "matrice : 4 cases"
        side = min(zone.h - 0.75, zone.w - 1.9)
        x0 = zone.x + (zone.w - side - 1.5) / 2 + 1.5  # place à gauche pour l'axe vertical
        y0 = zone.y + (zone.h - side - 0.75) / 2
        grid = Frame(x0, y0, side, side).grid(2, 2, gap=(0.05, 0.05))
        cells = [c for row in grid for c in row]
        shapes = []
        for k, (cell, (title, body)) in enumerate(zip(cells, quadrants)):
            on = k == focal
            sh = self._shape(slide, MSO_SHAPE.RECTANGLE, *cell, fill=PURPLE if on else GREY_LIGHT, line=None,
                             name=f"Case « {title} »")
            shapes.append(sh)
            color = WHITE if on else BLACK
            inner = cell.pad(0.2)
            text = f"**{title}**" + (f"\n{body}" if body else "")
            self.text(slide, inner.x, inner.y, inner.w, inner.h, text, size=size, color=color, align="center",
                      anchor="middle")
        low, high = graduations
        self.text(slide, x0 - 1.5, y0, 1.4, 0.35, high, size=12, color=BLACK, align="right")
        self.text(slide, x0 - 1.5, y0 + side - 0.35, 1.4, 0.35, low, size=12, color=BLACK, align="right")
        label_h = text_height(f"**{axe_y}**", 1.4, 14, line_spacing=1.2)
        self.text(slide, x0 - 1.5, y0 + side / 2 - label_h / 2, 1.4, label_h, f"**{axe_y}**", size=14,
                  align="right", anchor="middle", line_spacing=1.2)
        self.text(slide, x0, y0 + side + 0.05, 1.4, 0.35, low, size=12, color=BLACK)
        self.text(slide, x0 + side - 1.4, y0 + side + 0.05, 1.4, 0.35, high, size=12, color=BLACK,
                  align="right")
        self.text(slide, x0 + side / 2 - 1.5, y0 + side + 0.35, 3.0, 0.4, f"**{axe_x}**", size=14, align="center")
        return shapes

    def barres(self, slide, zone, items, focal=None, unit="", size=13):
        """Barres horizontales dessinées (pas de graphique natif : Google Slides les rend mal) : libellé à gauche,
        barre gris clair proportionnelle à la valeur, la barre focal en violet, valeur au bout. items : [(libellé,
        valeur), …]. Renvoie les barres."""
        label_w, value_w = min(3.2, zone.w * 0.3), 1.2
        rows = zone.rows(len(items), gap=0.15)
        top = max(v for _, v in items) or 1
        bars = []
        for k, (row, (label, value)) in enumerate(zip(rows, items)):
            bar_h = min(0.55, row.h * 0.7)
            y = row.y + (row.h - bar_h) / 2
            self.text(slide, row.x, row.y, label_w - 0.15, row.h, label, size=size, align="right", anchor="middle")
            w = max(0.05, (row.w - label_w - value_w) * value / top)
            on = k == focal
            bars.append(self._shape(slide, MSO_SHAPE.RECTANGLE, row.x + label_w, y, w, bar_h,
                                    fill=PURPLE if on else GREY_LIGHT, line=None, name=f"Barre « {label} »"))
            self.text(slide, row.x + label_w + w + 0.1, row.y, value_w, row.h, f"**{value:g}{unit}**", size=size,
                      color=PURPLE if on else BLACK, anchor="middle")
        return bars

    def tableau(self, slide, zone, rows, widths=None, size=12):
        """Tableau natif : en-tête violet foncé (texte blanc gras), lignes alternées blanc et gris clair, texte
        noir. rows : [[cellule, …], …], la première ligne étant l'en-tête ; widths : largeurs relatives des colonnes.
        Renvoie la forme du tableau."""
        n_rows, n_cols = len(rows), len(rows[0])
        row_h = min(0.6, zone.h / n_rows)
        frame = slide.shapes.add_table(n_rows, n_cols, Inches(zone.x), Inches(zone.y), Inches(zone.w),
                                       Inches(row_h * n_rows))
        table = frame.table
        tbl_pr = table._tbl.tblPr
        for attr in ("bandRow", "firstRow"):
            tbl_pr.set(attr, "0")
        style = tbl_pr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}tableStyleId")
        if style is not None:
            tbl_pr.remove(style)
        widths = widths or [1] * n_cols
        for k, w in enumerate(widths):
            table.columns[k].width = Inches(zone.w * w / sum(widths))
        for r, row in enumerate(rows):
            table.rows[r].height = Inches(row_h)
            for c, value in enumerate(row):
                cell = table.cell(r, c)
                cell.fill.solid()
                cell.fill.fore_color.rgb = PURPLE_DARKEST if r == 0 else (GREY_LIGHT if r % 2 == 0 else WHITE)
                cell.margin_left = cell.margin_right = Inches(0.1)
                cell.vertical_anchor = MSO_ANCHOR_MIDDLE
                self._cell_borders(cell)
                tf = cell.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                for chunk, bold, _ in _runs(value):
                    run = p.add_run()
                    run.text = chunk
                    run.font.name, run.font.size = self.FONT, Pt(size)
                    run.font.bold = bold or r == 0
                    run.font.color.rgb = WHITE if r == 0 else BLACK
        frame.name = "Tableau"
        return frame

    @staticmethod
    def _cell_borders(cell):
        """Filets blancs fins autour de la cellule : sans style de tableau, PowerPoint trace des bordures noires."""
        from lxml import etree
        from pptx.oxml.ns import qn
        tcPr = cell._tc.get_or_add_tcPr()
        for tag in ("a:lnB", "a:lnT", "a:lnR", "a:lnL"):  # insérés en tête, dans l'ordre du schéma (L, R, T, B)
            for old in tcPr.findall(qn(tag)):
                tcPr.remove(old)
            ln = etree.Element(qn(tag), w="12700")
            fill = etree.SubElement(ln, qn("a:solidFill"))
            etree.SubElement(fill, qn("a:srgbClr")).set("val", "FFFFFF")
            tcPr.insert(0, ln)
