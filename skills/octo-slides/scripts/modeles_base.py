"""Base commune des decks de slides préformatées : copier un modèle du deck de la Com et l'adapter (show, modele,
borrow, set_text, set_cell, remove, duplicate, move, recolor, replace_picture, check). ModeleMixin ne connaît aucune
charte : il se combine avec le deck d'une charte, ModeleDeck(ModeleMixin, Deck) pour OCTO (octo_modeles.py),
ModeleGrosseConfDeck(ModeleMixin, GrosseConfDeck) pour La Grosse Conf (grosse_conf_modeles.py),
ModeleAccentureDeck(ModeleMixin, AccentureDeck) pour Accenture (accenture_modeles.py), qui fixent le deck de modèles,
la palette contrôlée (PALETTE) et, au besoin, les consignes et textes de gabarit propres à leur deck de modèles.

Chemins de forme : "3" = 4e forme de la slide (index à partir de 0), "3.1" = 2e forme du groupe 3.
Positions en pouces.
"""
import copy
import re

from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches

from deck_base import _runs
from octo_layout import lines_of, text_width

# Consignes internes du gabarit : la forme qui les porte est supprimée à la copie.
CONSIGNES = re.compile(r"A adapter à\s+sa situation|ici mettre une photo|Version compatible export", re.I)
# Textes de gabarit qui ne doivent pas rester dans un livrable.
GABARIT = re.compile(r"Lorem ipsum|\bxxx\b|Title text block|^Titre$|^Sous titre\.?$", re.I | re.M)
_ID_ATTR = re.compile(r"^(?:embed|link|id|pict)$")


class ModeleMixin:
    """À combiner avec le deck d'une charte (class ModeleDeck(ModeleMixin, Deck)). PALETTE : couleurs de la charte,
    contrôlées par recolor() et check(). CONSIGNES : texte des formes de consigne, retirées à la copie ; GABARIT :
    textes de gabarit à remplacer ; NOIR_INTERDIT : le texte noir est un écart à la charte ; SIGLES : mots en
    capitales admis."""
    PALETTE = set()
    CONSIGNES = CONSIGNES
    GABARIT = GABARIT
    NOIR_INTERDIT = True
    SIGLES = ("OCTO", "MLOPS", "LLM", "API")

    def __init__(self, template=None, target="pptx"):
        super().__init__(template, target)
        self._modeles = list(self.prs.slides._sldIdLst)

    def _number(self, slide):
        """Numéro dans le deck livré : les modèles, en tête du fichier, en sont retirés à l'enregistrement."""
        return self.prs.slides.index(slide) + 1 - len(self._modeles)

    # ---------- lire un modèle ----------
    def show(self, n):
        """Imprime les formes du modèle n (numéro de slide du deck de modèles, cf. l'index des modèles)."""
        slide = self.prs.slides[n - 1]
        print(f"Modèle {n} — layout « {slide.slide_layout.name} »")
        for path, sh, depth in self._walk(slide.shapes):
            kind = str(sh.shape_type).split(".")[-1].split(" ")[0] if sh.shape_type else "?"
            text = sh.text_frame.text.strip().replace("\n", " / ")[:60] if sh.has_text_frame else ""
            fill = self._fill_color(sh)
            x, y, w, h = self.bounds(slide, path)
            print(f"{'  ' * depth}{path:7} {kind:12} ({x:.2f}, {y:.2f}) {w:.2f}x{h:.2f}"
                  f"{' fond ' + fill if fill else ''}{'  « ' + text + ' »' if text else ''}")

    def _walk(self, shapes, prefix="", depth=0):
        for i, sh in enumerate(shapes):
            path = f"{prefix}{i}"
            yield path, sh, depth
            if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                yield from self._walk(sh.shapes, f"{path}.", depth + 1)

    def bounds(self, slide, path):
        """Position et taille (pouces) d'une forme dans la slide, y compris à l'intérieur d'un groupe."""
        x, y, w, h = (Emu(v).inches for v in (lambda s: (s.left, s.top, s.width, s.height))(self.get(slide, path)))
        parts = path.split(".")
        for depth in range(len(parts) - 1, 0, -1):
            xfrm = self.get(slide, ".".join(parts[:depth]))._element.find(qn("p:grpSpPr")).find(qn("a:xfrm"))
            off, ext = xfrm.find(qn("a:off")), xfrm.find(qn("a:ext"))
            ch_off, ch_ext = xfrm.find(qn("a:chOff")), xfrm.find(qn("a:chExt"))
            sx = int(ext.get("cx")) / int(ch_ext.get("cx")) if int(ch_ext.get("cx")) else 1
            sy = int(ext.get("cy")) / int(ch_ext.get("cy")) if int(ch_ext.get("cy")) else 1
            x = Emu(int(off.get("x"))).inches + (x - Emu(int(ch_off.get("x"))).inches) * sx
            y = Emu(int(off.get("y"))).inches + (y - Emu(int(ch_off.get("y"))).inches) * sy
            w, h = w * sx, h * sy
        return x, y, w, h

    def _fill_color(self, sh):
        fill = sh._element.find(qn("p:spPr"))
        val = fill.xpath("a:solidFill/a:srgbClr/@val") if fill is not None else []
        return f"#{val[0]}" if val else ""

    # ---------- copier un modèle ----------
    def modele(self, n):
        """Ajoute au deck une copie du modèle n, sans les consignes internes du gabarit."""
        src = self.prs.slides[n - 1]
        slide = self.prs.slides.add_slide(src.slide_layout)
        tree = slide.shapes._spTree
        for el in list(tree)[2:]:
            tree.remove(el)
        rids = self._copy_rels(src, slide)
        for el in list(src.shapes._spTree)[2:]:
            tree.append(self._remap(copy.deepcopy(el), rids))
        bg = src._element.find(qn("p:cSld")).find(qn("p:bg"))
        if bg is not None:
            slide._element.find(qn("p:cSld")).insert(0, self._remap(copy.deepcopy(bg), rids))
        for sh in list(slide.shapes):
            if self.CONSIGNES.search("".join(sh._element.xpath(".//a:t/text()"))):
                tree.remove(sh._element)
        # Formes et texte de la Com : contrôlés seulement une fois déplacés ou réécrits.
        self._as_is.update(tree.iter(qn("p:txBody")))
        self._as_is.update(list(tree)[2:])
        return slide

    def _copy_rels(self, src, slide):
        """Relations utiles (images, liens externes) de la slide source, recréées sur la slide cible : {ancien rId: nouveau}."""
        rids = {}
        for rId, rel in src.part.rels.items():
            if rel.reltype.endswith(("/slideLayout", "/notesSlide", "/slide")):
                continue  # un lien vers une autre slide du gabarit est retiré par _remap
            rids[rId] = (slide.part.rels.get_or_add_ext_rel(rel.reltype, rel.target_ref) if rel.is_external
                         else slide.part.relate_to(rel.target_part, rel.reltype))
        return rids

    def borrow(self, slide, n, path, x, y, w=None):
        """Pioche une forme, un groupe ou un visuel (photo 3D en goutte, illustration, frise, pictogramme composé)
        dans le modèle n et le pose sur la slide en (x, y) ; w redimensionne en gardant les proportions.
        Pour composer une slide à soi avec les assets des slides préformatées. Renvoie la forme posée."""
        src = self.prs.slides[n - 1]
        bx, by, bw, bh = self.bounds(src, path)
        el = self._remap(copy.deepcopy(self.get(src, path)._element), self._copy_rels(src, slide))
        next_id = max([int(i) for i in slide._element.xpath(".//p:cNvPr/@id")] + [1]) + 1
        for k, c in enumerate(el.xpath(".//p:cNvPr")):
            c.set("id", str(next_id + k))
        xfrm = el.xpath("./p:spPr/a:xfrm | ./p:grpSpPr/a:xfrm | ./p:xfrm")[0]
        scale = w / bw if w else 1
        xfrm.find(qn("a:off")).set("x", str(int(Inches(x))))
        xfrm.find(qn("a:off")).set("y", str(int(Inches(y))))
        xfrm.find(qn("a:ext")).set("cx", str(int(Inches(bw * scale))))
        xfrm.find(qn("a:ext")).set("cy", str(int(Inches(bh * scale))))
        slide.shapes._spTree.append(el)
        self._as_is.update(el.iter(qn("p:txBody")))
        return slide.shapes[-1]

    def _remap(self, el, rids):
        """Réécrit les références r:* (images, liens) vers les relations de la nouvelle slide."""
        for node in el.iter():
            for attr, value in list(node.attrib.items()):
                if attr.startswith("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}") \
                        and _ID_ATTR.match(attr.split("}")[1]):
                    if value in rids:
                        node.set(attr, rids[value])
                    elif node.tag == qn("a:hlinkClick"):
                        node.getparent().remove(node)
        return el

    # ---------- adapter ----------
    def get(self, slide, path):
        shapes, shape = slide.shapes, None
        for i in path.split("."):
            shape = list(shapes)[int(i)]
            shapes = shape.shapes if shape.shape_type == MSO_SHAPE_TYPE.GROUP else None
        return shape

    def set_text(self, slide, path, text, per_line=False, fit=False, color=None):
        """Remplace le texte d'une forme en gardant son style (paragraphe et premier run). Par défaut toutes les
        lignes prennent le style de la première ligne du modèle ; per_line=True : chaque ligne reprend la ligne de
        même rang (titre puis corps, niveaux de puces). fit=True : la forme s'élargit à son texte (étiquette d'axe,
        libellé court traduit), en gardant son alignement. color : couleur du texte (RGBColor de la charte), à la
        place de celle du modèle. Markup : **gras**."""
        txBody = self.get(slide, path).text_frame._txBody
        self._as_is.discard(txBody)
        old = txBody.findall(qn("a:p"))
        styles = [(p.find(qn("a:pPr")), p.find(qn("a:r") + "/" + qn("a:rPr"))) for p in old]
        styles = [s for s in styles if s[1] is not None] or styles
        for p in old:
            txBody.remove(p)
        for i, line in enumerate(lines_of(text)):
            pPr, rPr = styles[min(i, len(styles) - 1)] if per_line else styles[0]
            p = txBody.makeelement(qn("a:p"), {})
            if pPr is not None:
                p.append(copy.deepcopy(pPr))
            for chunk, bold, _ in _runs(line):
                r = p.makeelement(qn("a:r"), {})
                run_pr = copy.deepcopy(rPr) if rPr is not None else r.makeelement(qn("a:rPr"), {})
                if bold:
                    run_pr.set("b", "1")
                if color is not None:
                    assert str(color) in self.PALETTE, f"#{color} hors charte ({self.CHARTE_FILE})"
                    for old in run_pr.findall(qn("a:solidFill")):
                        run_pr.remove(old)
                    fill = run_pr.makeelement(qn("a:solidFill"), {})
                    fill.append(fill.makeelement(qn("a:srgbClr"), {"val": str(color)}))
                    run_pr.insert(0, fill)
                r.append(run_pr)
                t_el = r.makeelement(qn("a:t"), {})
                t_el.text = chunk
                r.append(t_el)
                p.append(r)
            txBody.append(p)
        if fit:
            self._fit_width(self.get(slide, path), text)

    @staticmethod
    def _fit_width(sh, text):
        """Élargit une forme à la plus longue ligne de son texte (taille du premier run), du côté opposé à son
        alignement : un libellé aligné à droite garde son bord droit, un centré son centre."""
        from pptx.enum.text import PP_ALIGN
        runs = [r for p in sh.text_frame.paragraphs for r in p.runs]
        size = next((r.font.size.pt for r in runs if r.font.size), None)
        if size is None:
            return
        bold = any(r.font.bold for r in runs)
        tf = sh.text_frame
        need = Inches(text_width(f"**{text}**" if bold else text, size) + 0.05) + tf.margin_left + tf.margin_right
        delta = int(need - sh.width)
        if delta <= 0:
            return
        align = sh.text_frame.paragraphs[0].alignment
        shift = delta if align == PP_ALIGN.RIGHT else delta // 2 if align == PP_ALIGN.CENTER else 0
        sh.left, sh.width = sh.left - shift, sh.width + delta

    def keep(self, slide, *paths):
        """Ne garde de la slide que les formes de premier niveau désignées (et les placeholders, dont le titre) :
        l'inverse de remove, pour un modèle dont on ne garde que quelques éléments."""
        wanted = {int(p.split(".")[0]) for p in paths}
        for i, sh in reversed(list(enumerate(slide.shapes))):
            if i not in wanted and not sh.is_placeholder:
                sh._element.getparent().remove(sh._element)

    def set_cell(self, slide, path, row, col, text):
        """Texte d'une cellule de tableau natif, style conservé."""
        cell = self.get(slide, path).table.cell(row, col)
        runs = cell.text_frame.paragraphs[0].runs
        rPr = copy.deepcopy(runs[0]._r.find(qn("a:rPr"))) if runs else None
        cell.text_frame.text = text
        if rPr is not None:
            for r in cell.text_frame.paragraphs[0].runs:
                r._r.insert(0, copy.deepcopy(rPr))

    def remove(self, slide, *paths):
        """Supprime des formes (les chemins se lisent avant suppression)."""
        for el in [self.get(slide, p)._element for p in paths]:
            el.getparent().remove(el)

    def duplicate(self, slide, path, dx=0, dy=0):
        """Copie une forme (ou un groupe) décalée de (dx, dy) pouces ; renvoie la copie."""
        el = self.get(slide, path)._element
        clone = copy.deepcopy(el)
        next_id = max(int(i) for i in slide._element.xpath(".//p:cNvPr/@id")) + 1
        for k, c in enumerate(clone.xpath(".//p:cNvPr")):
            c.set("id", str(next_id + k))
        el.addnext(clone)
        shape = next(sh for sh in el.getparent().iterchildren() if sh is clone)
        for off in clone.xpath("./*/a:xfrm/a:off"):
            off.set("x", str(int(off.get("x")) + Inches(dx)))
            off.set("y", str(int(off.get("y")) + Inches(dy)))
        return shape

    def move(self, slide, path, x=None, y=None, w=None, h=None):
        """Déplace ou redimensionne une forme (pouces). Un groupe est mis à l'échelle avec ses enfants."""
        sh = self.get(slide, path)
        self._as_is.discard(sh._element)  # déplacée : désormais contrôlée
        for attr, v in (("left", x), ("top", y), ("width", w), ("height", h)):
            if v is not None:
                setattr(sh, attr, Inches(v))

    def recolor(self, slide, path, fill=None, line=None):
        """Change le fond et / ou le contour d'une forme. Couleurs de la charte uniquement."""
        sh = self.get(slide, path)
        for color in (fill, line):
            assert color is None or str(color) in self.PALETTE, f"#{color} hors charte ({self.CHARTE_FILE})"
        if fill is not None:
            sh.fill.solid()
            sh.fill.fore_color.rgb = fill
        if line is not None:
            sh.line.color.rgb = line

    def replace_picture(self, slide, path, name):
        """Remplace une image du modèle (picto, illustration, photo) par un visuel de la bibliothèque du deck,
        à la même place et à la même hauteur, proportions respectées."""
        old = self.get(slide, path)
        pic = self.picto(slide, name, Emu(old.left).inches, Emu(old.top).inches, Emu(old.height).inches)
        pic.left = old.left + (old.width - pic.width) // 2
        old._element.addnext(pic._element)
        old._element.getparent().remove(old._element)
        return pic

    # ---------- vérifier ----------
    def check(self, slide):
        """Signale les écarts à la charte : couleurs hors palette, texte noir, capitales, italique,
        textes de gabarit restants. Renvoie la liste des alertes (vide si rien)."""
        alerts = []
        xml = slide._element
        palette = {p.upper() for p in self.PALETTE} | {"000000"}
        for path, sh, _ in self._walk(slide.shapes):
            if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                continue  # ses formes sont parcourues une à une
            off = sorted({v for v in sh._element.xpath(".//a:srgbClr/@val") if v.upper() not in palette})
            if off:
                # Y compris une couleur cachée, celle d'un paragraphe vide (endParaRPr) : le gris #3F3F3F de la
                # courbe du modèle 201. recolor(slide, path, …) corrige le fond et le contour.
                alerts.append(f"{path} : couleur hors charte {', '.join('#' + v for v in off)}")
        if self.NOIR_INTERDIT and xml.xpath(".//a:rPr/a:solidFill/a:srgbClr[@val='000000']"):
            alerts.append("texte noir")
        if xml.xpath(".//a:rPr[@i='1']"):
            alerts.append("italique")
        for path, sh, _ in self._walk(slide.shapes):
            if not sh.has_text_frame:
                continue
            text = sh.text_frame.text
            if self.GABARIT.search(text):
                alerts.append(f"{path} : texte de gabarit « {text.strip()[:40]} »")
            caps = [w for w in re.findall(r"\b[A-ZÀ-Ü]{4,}\b", text) if w not in self.SIGLES]
            if caps:
                alerts.append(f"{path} : capitales {caps[:3]}")
        for a in alerts:
            print("⚠", a)
        return alerts

    def save(self, path):
        """Enregistre en ne gardant que les slides créées (les modèles sont retirés)."""
        for sld_id in self._modeles:
            self.prs.part.drop_rel(sld_id.rId)
            self.prs.slides._sldIdLst.remove(sld_id)
        self._modeles = []
        return super().save(path)

