"""Partir d'une slide préformatée OCTO (assets/modeles_octo.pptx) et l'adapter au contenu.

Usage :
    import sys; sys.path.insert(0, "<skill>/scripts")
    from octo_modeles import ModeleDeck
    d = ModeleDeck()                  # tous les helpers de Deck restent disponibles
    d.show(140)                       # liste les formes du modèle 140 : chemin, type, position, texte
    s = d.modele(140)                 # copie du modèle, consignes internes retirées
    d.set_text(s, "2", "Titre du tableau")
    d.remove(s, "5", "6")             # retirer ce qui ne sert pas
    d.duplicate(s, "3", dx=2.3)       # une carte de plus
    d.recolor(s, "4", fill=TURQ)      # hiérarchie des aplats, couleurs de la charte seulement
    d.check(s)                        # écarts à la charte et textes de gabarit restants
    d.save("deck.pptx")               # seules les slides créées sont gardées

Chemins de forme : "3" = 4e forme de la slide (index à partir de 0), "3.1" = 2e forme du groupe 3.
Positions en pouces.
"""

from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.util import Inches

import octo_slides
from modeles_base import CONSIGNES, GABARIT, ModeleMixin  # noqa: F401 (réexportés)
from deck_base import _runs  # noqa: F401 (réexporté)
from octo_layout import lines_of  # noqa: F401 (réexporté)
from octo_slides import Deck

MODELES = octo_slides.ASSETS / "modeles_octo.pptx"
PALETTE = {str(v) for k, v in vars(octo_slides).items() if isinstance(v, RGBColor)}


class ModeleDeck(ModeleMixin, Deck):
    """Deck OCTO qui part des slides préformatées OCTO (assets/modeles_octo.pptx) : tous les helpers de Deck, plus
    ceux de ModeleMixin (modeles_base.py) et asset()."""
    PALETTE = PALETTE

    def __init__(self, template=MODELES, target="pptx"):
        super().__init__(template, target)

    _ASSET_SHAPES = {"goutte": MSO_SHAPE.TEAR, "rond": MSO_SHAPE.OVAL, "tl-br": MSO_SHAPE.ROUND_2_DIAG_RECTANGLE}

    def asset(self, slide, asset_id, x, y, w, h=None, shape=None):
        """Pose un visuel des slides préformatées par son identifiant « modèle.chemin » (references/assets_modeles.md :
        visuels 3D, illustrations au trait, photos, pictos composés ; « 185.0 » pour un groupe, la chaîne d'anneaux
        de references/modeles.md). w : largeur, proportions gardées. Pour une image : h et shape="goutte", "rond" ou
        "tl-br" la recadrent pour remplir w x h et la découpent dans la forme de la charte (un visuel 3D en goutte,
        comme les intercalaires). Renvoie la forme posée."""
        n, path = asset_id.split(".", 1)
        sh = self.borrow(slide, int(n), path, x, y, w=w)
        if h is not None and hasattr(sh, "image"):
            iw, ih = sh.image.size
            rz, ri = w / h, iw / ih
            sh.crop_left = sh.crop_right = max(0.0, (1 - rz / ri) / 2) if ri > rz else 0.0
            sh.crop_top = sh.crop_bottom = max(0.0, (1 - ri / rz) / 2) if ri < rz else 0.0
            sh.width, sh.height = Inches(w), Inches(h)
        if shape and hasattr(sh, "auto_shape_type"):
            sh.auto_shape_type = self._ASSET_SHAPES[shape]
            # Les réglages de la forme d'origine (adj1, adj2 d'un rectangle à coins arrondis) ne valent rien pour la
            # nouvelle : PowerPoint jugerait le fichier corrompu. La nouvelle forme prend ses réglages par défaut.
            for av in sh._element.iter(qn("a:avLst")):
                for gd in list(av):
                    av.remove(gd)
        return sh

