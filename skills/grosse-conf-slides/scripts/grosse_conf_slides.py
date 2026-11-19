"""Slides La Grosse Conf : la classe GrosseConfDeck, sur le template assets/template_grosse_conf.pptx et la charte
de references/charte_grosse_conf.md. Elle ne dépend d'aucun fichier OCTO : comme Deck (octo_slides.py), elle hérite
de deck_base.BaseDeck, qui ne connaît aucune charte.

    import sys; sys.path.insert(0, "<skill>/scripts")
    from grosse_conf_slides import CONTENT, GrosseConfDeck
    d = GrosseConfDeck()
    d.cover("09.03.2027", "Maison de la Chimie")
    s = d.slide("Une idée par slide", "Le sous-titre dit la chute.")
    inner = d.fenetre(s, *CONTENT.cols(2)[0], title="Le why")     # fenêtre web : renvoie la zone intérieure
    d.text(s, *inner, "**Un lead.** Une explication courte.")
    d.save("deck.pptx")

Les helpers génériques de BaseDeck (text, statement, picto, photo, arrow, connect, fork, join, circle, rule, notes,
save…) prennent la palette de la charte grosse conf (TEXT, LINE, ACCENT, POINT, BULLET, FLOW, LOOP, CHEVRON, RULE) ;
picto() ne cherche que dans les pictos et illustrations de la conf.
"""
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

from octo_layout import Frame, lines_of
from deck_base import ASSETS, WHITE, BaseDeck

TEMPLATE = ASSETS / "template_grosse_conf.pptx"

# Palette de la charte grosse conf (references/charte_grosse_conf.md). Aucune autre couleur.
ANTHRACITE = RGBColor(0x38, 0x38, 0x3F)  # principale 1 : texte, traits
RED = RGBColor(0xFF, 0x00, 0x42)  # principale 2 : accent, ombres, pastilles


def descente(pct):
    """Descente du rouge à pct % (50, 40, 30, 20, 10) : le rouge mêlé de blanc, pour les illustrations et les fonds."""
    mix = lambda c: round(255 - (255 - c) * pct / 100)  # noqa: E731
    return RGBColor(mix(0xFF), mix(0x00), mix(0x42))


PINK = descente(50)  # #FF80A1 : texte sur fond anthracite, aplats
RED_40, RED_30, RED_20, RED_10 = descente(40), descente(30), descente(20), descente(10)
PINK_BG = RGBColor(0xFF, 0xED, 0xF2)  # fond rose pâle des slides de rupture (couverture, chapitres, sommaire)

# Bibliothèque de visuels de la conf : picto() ne cherche que là (jamais dans celle d'OCTO, turquoise).
VISUAL_DIRS = [ASSETS / "pictos-grosse-conf", ASSETS / "illustrations-grosse-conf"]

# Layouts du template (noms exacts : les numéros « 51 - » y sont partagés, voir references/layouts_grosse_conf.md).
LAYOUTS = {
    "cover": "51 - Couverture",
    "cover_2": "51 - Couverture_1",
    "thematic": "51 - Slide THEMATIQUE",
    "speaker": "51 - Slide SPEAKER",
    "chapter_pictos": "51 - Chapitre PICTOS",
    "chapter_text": "51 - Chapitre TEXTE",
    "chapter_photo": "51 - Chapitre PHOTO",
    "photo_text": "51 - Photo + texte",
    "focus": "51 - Focus",
    "title_sub_content": "01 - Titre, sous-titre et contenu",
    "title_content": "02 - Titre et contenu",
    "title_sub": "03 - Titre et sous-titre",
    "title_only": "04 - Titre seul",
    "blank": "06 - Slide vide",
    "visual_right": "63 - Titre, contenu et visuel à droite - cadre blanc",
    "visual_left": "69 - Titre, contenu, visuel à gauche et bloc conclu - cadre blanc",
    "title_visual": "60 - Titre et visuel_1",
}
# Sommaires : layout selon le nombre d'entrées.
TOC_LAYOUTS = {2: "90 - Table des matières [2]", 3: "91 - Table des matières [3]", 4: "92 - Table des matières [4]",
               5: "94 - Table des matières [5]", 6: "94 - Table des matières [6]", 7: "95 - Table des matières [7]",
               8: "96 - Table des matières [8]", 9: "97 - Table des matières [9]",
               10: "98 - Table des matières [10]"}

# Zone de contenu d'une slide de contenu : sous le sous-titre, hors de la pastille du numéro de page (x > 9,2 et
# y > 5,05, en bas à droite).
CONTENT = Frame(0.62, 1.4, 8.55, 3.6)

class GrosseConfDeck(BaseDeck):
    """Deck La Grosse Conf : template, palette et visuels de la conf (references/charte_grosse_conf.md)."""
    TEMPLATE = TEMPLATE
    VISUAL_DIRS = VISUAL_DIRS
    TEXT = LINE = FLOW = RULE = ANTHRACITE  # texte et traits anthracite, jamais noir
    ACCENT = PINK  # mot-clé ==…== sur fond anthracite
    POINT = LOOP = CHEVRON = RED  # point final des titres, boucle de retour, chevron
    BULLET = "FF0042"
    PHOTO_SHAPE = "arrondi"
    CHARTE = "grosse_conf"
    CHARTE_FILE = "references/charte_grosse_conf.md"

    def __init__(self, template=TEMPLATE, target="pptx"):
        super().__init__(template, target)

    # ---------- layouts du template (references/layouts_grosse_conf.md) ----------
    def layout(self, name, texts=None, visuals=None):
        """Slide sur un layout du template, désigné par son nom complet (« 51 - Focus ») ou une clé de LAYOUTS
        (« focus »). texts : {idx du placeholder: texte balisé}, le style du layout est conservé ; un placeholder
        absent de texts est supprimé. visuals : un élément par placeholder image, dans l'ordre des idx : chemin d'une
        photo, ou nom d'un picto ou d'une illustration (assets/pictos-grosse-conf, assets/illustrations-grosse-conf).
        Un emplacement sans visuel est supprimé : jamais de cadre vide dans le livrable."""
        layout = self._layouts[LAYOUTS.get(name, name)]
        s = self.prs.slides.add_slide(layout)
        texts, visuals = texts or {}, list(visuals or [])
        pictures = sorted((ph for ph in s.placeholders if ph.placeholder_format.type == 18),  # PP_PLACEHOLDER.PICTURE
                          key=lambda ph: ph.placeholder_format.idx)
        for ph in list(s.placeholders):
            idx = ph.placeholder_format.idx
            if ph in pictures:
                continue
            if texts.get(idx):
                self._fill_placeholder(ph, texts[idx])
                self._no_bullet(ph, texts[idx])
                if idx == 0:
                    self._fit_title(ph, texts[idx])
                    self._final_point(ph.text_frame)  # point final rouge (POINT) d'un titre qui finit par « . »
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
    def _no_bullet(ph, text):
        """Retire la puce que le layout pose sur ce placeholder (un « ๏ », absent d'Outfit, dans le template de la
        Com) des lignes qui n'en demandent pas (« - » en tête). Seulement si le layout pose une puce : un retrait nul
        garde alors le texte à sa place ; un layout sans puce (sommaires) n'est pas touché."""
        base = ph._base_placeholder
        lst = base._element.find(qn("p:txBody") + "/" + qn("a:lstStyle")) if base is not None else None
        lvl1 = lst.find(qn("a:lvl1pPr")) if lst is not None else None
        if lvl1 is None or lvl1.find(qn("a:buChar")) is None:
            return
        for p, line in zip(ph.text_frame.paragraphs, lines_of(text)):
            if line.startswith("- "):
                continue
            pPr = p._p.get_or_add_pPr()
            for tag in ("a:buChar", "a:buAutoNum", "a:buBlip", "a:buNone"):
                for el in pPr.findall(qn(tag)):
                    pPr.remove(el)
            after = next((pPr.find(qn(t)) for t in ("a:tabLst", "a:defRPr", "a:extLst")
                          if pPr.find(qn(t)) is not None), None)
            none = pPr.makeelement(qn("a:buNone"), {})
            after.addprevious(none) if after is not None else pPr.append(none)
            pPr.set("indent", "0")

    def cover(self, date, place, variant=1):
        """Couverture : le logo de la conf et l'illustration sont dans le layout ; reste la date et le lieu
        (« 09.03.2027  I  Maison de la Chimie »). variant=2 : fond photo du template (51 - Couverture_1)."""
        s = self.layout("cover" if variant == 1 else "cover_2")
        tb = self.text(s, 2.0, 3.3, 3.1, 0.41, f"**{date}**  I  {place}", size=18, anchor="middle")
        for r in tb.text_frame.paragraphs[0].runs[1:]:
            r.font.size = Pt(9)  # le lieu, plus petit que la date (template)
        return s

    def thematic(self, title, subtitle=None, note=None):
        """Slide thématique : titre dans la grande fenêtre, sous-titre, et une note (date, lieu) dans la petite."""
        return self.layout("thematic", {0: title, 1: subtitle, 2: note})

    def speaker(self, name, role, photo):
        """Slide speaker : nom, titre du poste et entreprise, photo ronde (chemin d'un fichier)."""
        return self.layout("speaker", {0: name, 1: role}, [photo])

    def chapter(self, title, number, visual=None):
        """Intercalaire : onglet « 01 », titre dans la fenêtre. visual : nom d'une illustration ou d'un picto, posé à
        gauche (layout « Chapitre PICTOS ») ; sans visual, layout « Chapitre TEXTE »."""
        num = f"{number:02d}" if isinstance(number, int) else number
        s = self.layout("chapter_pictos" if visual else "chapter_text", {0: title, 1: num})
        for ph in s.placeholders:
            if ph.placeholder_format.idx == 1:
                ph.text_frame.word_wrap = False  # « 01 » dans l'onglet : jamais sur deux lignes
        if visual:
            path = visual if str(visual).endswith((".png", ".jpg", ".jpeg")) else self._visual(visual)
            s.shapes.add_picture(path, Inches(0.63), Inches(1.84), Inches(3.43), Inches(3.43))
        return s

    def toc(self, items, title="Sommaire."):
        """Sommaire à pastilles « 01 »… (layouts 90 à 98), de 2 à 10 entrées."""
        assert 2 <= len(items) <= 10, "toc : 2 à 10 entrées"
        layout = self._layouts[TOC_LAYOUTS[len(items)]]
        # Les idx des placeholders ne suivent pas l'ordre visuel : les entrées vont colonne par colonne, de haut en bas.
        entries = sorted((ph for ph in layout.placeholders if ph.placeholder_format.idx != 0),
                         key=lambda ph: (round(Emu(ph.left).inches, 1), ph.top))
        texts = {ph.placeholder_format.idx: item for ph, item in zip(entries, items)}
        return self.layout(TOC_LAYOUTS[len(items)], {0: title, **texts})

    def focus(self, title, subtitle=None, body=None):
        """Slide « focus » : grand cadre rose plein, pour un message clé ou le « pourquoi »."""
        s = self.layout("focus", {0: title, 1: body, 2: subtitle})
        for ph in s.placeholders:
            if ph.placeholder_format.idx == 1:  # corps : noir pur dans le layout, anthracite dans la charte
                for p in ph.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.color.rgb = ANTHRACITE
        return s

    def slide(self, title, subtitle=None, subtitle_size=None):
        """Slide de contenu : titre court qui finit par un point (rouge), sous-titre, zone libre CONTENT dessous."""
        s = self.layout("title_sub_content", {0: title, 2: subtitle})
        if subtitle_size:
            for ph in s.placeholders:
                if ph.placeholder_format.idx == 2:
                    for r in ph.text_frame.paragraphs[0].runs:
                        r.font.size = Pt(subtitle_size)
        return s

    def blank(self):
        """Slide vide : masque (sigle, mention légale, numéro de page) seul."""
        return self.layout("blank")

    # ---------- composants de la charte grosse conf ----------
    def fenetre(self, slide, x, y, w, h, title=None, ombre=True, fill=WHITE, defilement=False):
        """Fenêtre web, le composant signature : cadre au trait anthracite, deux pastilles (rouge pleine, vide) en haut
        à gauche, barre de titre, ombre rouge décalée. Renvoie la zone intérieure (x, y, w, h) sous la barre.
        title : texte gras dans la barre. defilement=True : ascenseur rouge à droite (fenêtre de texte long)."""
        bar = 0.26
        if ombre:
            self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x + 0.07, y + 0.07, w, h, fill=RED, line=None, adj=[0.05],
                        name="Ombre de fenêtre")
        self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=fill, line=ANTHRACITE, line_w=0.75,
                    adj=[0.05], name=f"Fenêtre « {title or ''} »")
        line = self._connector(slide.shapes, Inches(x), Inches(y + bar), Inches(x + w), Inches(y + bar))
        line.line.color.rgb = ANTHRACITE
        line.line.width = Pt(0.75)
        self._shape(slide, MSO_SHAPE.OVAL, x + 0.1, y + 0.085, 0.09, 0.09, fill=RED, line=RED)
        self._shape(slide, MSO_SHAPE.OVAL, x + 0.24, y + 0.085, 0.09, 0.09, fill=WHITE, line=ANTHRACITE)
        if title:
            self.text(slide, x + 0.45, y, w - 0.55, bar, f"**{title}**", size=8.5, anchor="middle")
        if defilement:
            self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x + w - 0.16, y + bar + 0.15, 0.1, 0.45, fill=RED,
                        line=None, adj=[0.5], name="Ascenseur")
        return Frame(x + 0.15, y + bar + 0.08, w - (0.4 if defilement else 0.3), h - bar - 0.16)

    def onglet(self, slide, x, y, text="01", w=0.86, h=0.3):
        """Onglet posé sur le bord haut d'une fenêtre (« 01 »), fond rose pâle, texte gras."""
        sh = self._shape(slide, MSO_SHAPE.ROUND_2_SAME_RECTANGLE, x, y, w, h, fill=PINK_BG, line=ANTHRACITE,
                         adj=[0.3, 0], name=f"Onglet de fenêtre « {text} »")
        self._fill_text(sh.text_frame, f"**{text}**", 11, ANTHRACITE, "center", "middle")
        return sh

    def pastille(self, slide, x, y, text="01", d=0.5, fill=PINK_BG):
        """Pastille carrée arrondie du sommaire (« 01 », « 02 »), fond rose pâle, texte gras anthracite."""
        sh = self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, d, d, fill=fill, line=ANTHRACITE, adj=[0.25],
                         name=f"Pastille « {text} »")
        self._fill_text(sh.text_frame, f"**{text}**", 11, ANTHRACITE, "center", "middle")
        return sh

    def tracker_gc(self, slide, x, y, w, number, text, h=0.33, active=True, size=11):
        """Étape d'un tracker : pilule anthracite (étape en cours, texte blanc) ou pilule au trait (étape à venir),
        précédée de son numéro (« 1 »)."""
        sh = self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=ANTHRACITE if active else WHITE,
                         line=ANTHRACITE, adj=[0.5], name=f"Étape {number}")
        self._fill_text(sh.text_frame, f"**{number}.** {text}", size, WHITE if active else ANTHRACITE, "left",
                        "middle")
        return sh

    def citation(self, slide, x, y, w, h, text, auteur, size=20):
        """Citation : texte gras dans une fenêtre, auteur dans une étiquette rose sous la fenêtre."""
        inner = self.fenetre(slide, x, y, w, h - 0.2)
        self.text(slide, *inner, f"**{text}**", size=size, anchor="middle")
        lab = self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x + w - 2.2, y + h - 0.42, 2.0, 0.34, fill=PINK_BG,
                          line=ANTHRACITE, adj=[0.2], name="Auteur")
        self._fill_text(lab.text_frame, auteur, 10, ANTHRACITE, "center", "middle")
        return inner

    def chiffre(self, slide, x, y, w, value, label, size=40):
        """Chiffre clé : valeur très grande en gras anthracite, point rouge, libellé dessous."""
        tb = self.text(slide, x, y, w, size / 72 * 1.3, f"**{value}**", size=size, anchor="bottom")
        self._final_point(tb.text_frame)
        self.text(slide, x, y + size / 72 * 1.3, w, None, label, size=11, color=ANTHRACITE)
        return tb

    def carte(self, slide, x, y, w, h, picto, title, body="", size=10, vertical=False, ombre=False):
        """Carte au trait : picto de la conf, titre en gras et texte courts. Par défaut le picto est à gauche et le
        texte à droite ; vertical=True : picto en haut, texte centré dessous. ombre=True : ombre rouge décalée (le point
        focal du schéma, une seule par slide). Renvoie la forme de la carte (à relier avec connect). picto : nom d'un
        fichier de assets/pictos-grosse-conf."""
        if ombre:
            self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x + 0.07, y + 0.07, w, h, fill=RED, line=None, adj=[0.08],
                        name="Ombre de carte")
        sh = self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=WHITE, line=ANTHRACITE, adj=[0.08],
                         name=f"Carte « {title} »")
        text = f"**{title}**" + (f"\n{body}" if body else "")
        if vertical:
            side = min(h * 0.45, 0.9)
            pic = self.picto(slide, picto, x, y + 0.12, side)
            pic.left = Inches(x + w / 2 - Emu(pic.width).inches / 2)
            top = y + 0.12 + side + 0.05
            self.text(slide, x + 0.05, top, w - 0.1, y + h - top - 0.05, text, size, align="center")
            return sh
        side = min(h - 0.2, 0.85)
        pic = self.picto(slide, picto, x + 0.12, y + (h - side) / 2, side)
        self._fill_text(sh.text_frame, text, size, ANTHRACITE, "left", "middle")
        sh.text_frame.margin_left = Inches(0.12 + Emu(pic.width).inches + 0.12)
        return sh

    # ---------- schémas (références : style_grosse_conf.md, §3 « Recettes de schémas ») ----------
    def equation(self, slide, zone, termes, operateurs=None, h=1.5, size=24):
        """Équation en pictos : un grand picto et son libellé par terme, des opérateurs entre eux (« Agent = Model +
        Harness »). termes : [(picto, libellé), …] ; operateurs : un par écart, par défaut « = » puis « + »."""
        n = len(termes)
        operateurs = operateurs or (["="] + ["+"] * max(n - 2, 0))[:n - 1]
        tw, ow = 2.6, 0.8
        scale = min(1.0, zone.w / (n * tw + (n - 1) * ow))
        tw, ow = tw * scale, ow * scale
        total = n * tw + (n - 1) * ow
        x, top = zone.x + (zone.w - total) / 2, zone.y + (zone.h - (h + 0.75)) / 2
        for k, (nom, libelle) in enumerate(termes):
            pic = self.picto(slide, nom, 0, top, h)
            pic.left = Inches(x + tw / 2 - Emu(pic.width).inches / 2)
            self.text(slide, x, top + h + 0.1, tw, 0.6, f"**{libelle}**", size=size, align="center")
            x += tw
            if k < n - 1:
                self.text(slide, x, top, ow, h, f"**{operateurs[k]}**", size=40, align="center", anchor="middle")
                x += ow

    def cible(self, slide, zone, niveaux):
        """Cercles emboîtés (2 à 4 niveaux, du plus large au plus étroit) : un niveau qui en contient un autre. Le plus
        étroit est rouge, texte blanc gras 14 pt. zone : le cercle le plus large s'y inscrit, centré. niveaux : les
        libellés, du plus large au plus étroit. Renvoie la zone carrée du cercle, pour aligner ce qui l'accompagne."""
        r = min(zone.w, zone.h) / 2
        cx, cy = zone.cx, zone.cy
        n = len(niveaux)
        assert 2 <= n <= 4, "cible : 2 à 4 niveaux"
        fills = {2: [WHITE, RED], 3: [WHITE, PINK_BG, RED], 4: [WHITE, PINK_BG, RED_30, RED]}[n]
        radii = [r * (n - k) / n for k in range(n)]
        for rad, fill in zip(radii, fills):
            self.circle(slide, cx, cy, rad, fill=fill, line=ANTHRACITE).name = "Cercle de cible"
        for k, libelle in enumerate(niveaux):
            if k == n - 1:
                self.text(slide, cx - 0.8, cy - 0.2, 1.6, 0.4, f"**{libelle}**", size=14, color=WHITE, align="center",
                          anchor="middle")
            else:
                self.text(slide, cx - 0.8, cy - radii[k] + 0.07, 1.6, 0.3, f"**{libelle}**", size=11, align="center")
        return Frame(cx - r, cy - r, 2 * r, 2 * r)

    def radial(self, slide, zone, centre, gauche, droite, size=9):
        """Un élément central (aplat rouge) relié par des flèches à des cartes de part et d'autre : ce qui l'entoure.
        gauche et droite : [(picto, titre, texte), …] (3 de chaque côté). Renvoie l'aplat central."""
        g, m, d = zone.cols([2.65, "1fr", 2.65], gap=0.45)
        cible_ = self.aplat(slide, *m.place(w=1.3, h=0.9, align="mc"), f"**{centre}**", fill=RED, size=15)
        boites = {}
        for cote, col, items in (("g", g, gauche), ("d", d, droite)):
            boites[cote] = [self.carte(slide, *cell, nom, titre, texte, size=size)
                            for cell, (nom, titre, texte) in zip(col.rows(len(items), gap=0.2), items)]
        self.fork(slide, cible_, boites["d"])
        self.fork(slide, cible_, boites["g"])
        return cible_

    def boucle(self, slide, zone, etapes, focal=2, size=12):
        """Cycle en quatre cartes (2 x 2, sens horaire) reliées par des flèches, la dernière retournant à la première
        par une flèche rouge. etapes : [(picto, titre), …] (4) ; focal : indice de l'étape à l'ombre rouge."""
        assert len(etapes) == 4, "boucle : 4 étapes"
        cadre = zone.place(w=min(zone.w, 7.6), h=min(zone.h, 3.3), align="mc")
        (a, b), (dd, cc) = cadre.grid(2, 2, gap=(0.8, 1.0))
        formes = [self.carte(slide, *cell, nom, titre, size=size, ombre=(k == focal))
                  for k, (cell, (nom, titre)) in enumerate(zip([a, b, cc, dd], etapes))]
        for k in range(3):
            self.connect(slide, formes[k], formes[k + 1])
        self.connect(slide, formes[3], formes[0], loop=True)
        return formes

    def pipeline(self, slide, zone, etapes, focal=None, retour=None, size=10, card_h=2.0):
        """Étapes côte à côte (cartes à picto en haut), reliées de gauche à droite ; retour : texte d'une boucle rouge
        de la dernière étape à la première. etapes : [(picto, titre, texte), …] ; focal : indice de l'ombre rouge ;
        card_h : hauteur des cartes."""
        zone = zone.pad(0, 0.1, 0, 0.6 if retour else 0.1)
        formes = [self.carte(slide, *col.place(h=card_h, align="mc"), nom, titre, texte, size=size, vertical=True,
                             ombre=(k == focal))
                  for k, (col, (nom, titre, texte)) in enumerate(zip(zone.cols(len(etapes), gap=0.5), etapes))]
        for a, b in zip(formes, formes[1:]):
            self.connect(slide, a, b)
        if retour:
            bas = zone.y + zone.h / 2 + card_h / 2 + 0.1
            y, x1, x2 = bas + 0.35, zone.x + zone.w / (2 * len(etapes)), zone.right - zone.w / (2 * len(etapes))
            self.loop_back(slide, [(x2, bas), (x2, y), (x1, y), (x1, bas)])
            self.text(slide, x1, y + 0.05, x2 - x1, 0.3, retour, size=10, align="center")
        return formes

    def grille(self, slide, zone, items, cols=2, gap=0.3, ombre_premiere=True, size=11):
        """Grille de fenêtres à picto (échecs, causes, critères indépendants : rien à relier). items : [(picto, titre,
        texte), …]. Une seule ombre rouge, sur la première fenêtre."""
        rows = -(-len(items) // cols)
        cells = [c for row in zone.grid(rows, cols, gap=(gap, gap)) for c in row]
        for k, (cell, (nom, titre, texte)) in enumerate(zip(cells, items)):
            inner = self.fenetre(slide, *cell, title=titre, ombre=(ombre_premiere and k == 0))
            side = min(inner.h - 0.1, 0.95)
            self.picto(slide, nom, inner.x, inner.y + (inner.h - side) / 2, side)
            self.text(slide, inner.x + 1.2, inner.y, inner.w - 1.2, inner.h, texte, size=size, anchor="middle")
        return cells

    def aplat(self, slide, x, y, w, h, text="", fill=RED, size=14):
        """Aplat de schéma à coins légèrement arrondis. Le texte suit la charte : blanc sur rouge ou anthracite (au-dessus
        de 18 pt ou en gras 14 pt sur rouge : 14 pt gras par défaut), anthracite sur blanc et sur les descentes du
        rouge."""
        sh = self._shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=fill, line=ANTHRACITE, adj=[0.08])
        if text:
            self._fill_text(sh.text_frame, text, size, WHITE if fill in (RED, ANTHRACITE) else ANTHRACITE, "center",
                            "middle", bold=fill == RED)
        return sh

