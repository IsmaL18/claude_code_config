"""Partir d'une slide préformatée La Grosse Conf (assets/modeles_grosse_conf.pptx) et l'adapter au contenu.

Mêmes méthodes que les modèles OCTO (show, modele, set_text, set_cell, remove, duplicate, move, recolor,
replace_picture, borrow, check : modeles_base.ModeleMixin), sur le deck de slides préformatées de la Grosse Conf,
avec les helpers et la palette de GrosseConfDeck ; rien d'OCTO :

    import sys; sys.path.insert(0, "<skill>/scripts")
    from grosse_conf_modeles import ModeleGrosseConfDeck
    d = ModeleGrosseConfDeck()
    d.show(12)                        # liste les formes du modèle 12 : chemin, type, position, texte
    s = d.modele(12)                  # copie du modèle
    d.set_text(s, "2", "Titre du schéma")
    d.check(s)                        # écarts à la charte grosse conf et textes de gabarit restants
    d.save("deck.pptx")               # seules les slides créées sont gardées

Les numéros sont ceux de references/modeles_index_grosse_conf.md. Les visuels se posent par leur nom (picto, carte,
replace_picture) depuis assets/pictos-grosse-conf et assets/illustrations-grosse-conf.
"""
from deck_base import ASSETS, WHITE
from grosse_conf_slides import ANTHRACITE, PINK, PINK_BG, RED, RED_10, RED_20, RED_30, RED_40, GrosseConfDeck
from modeles_base import ModeleMixin

MODELES_GROSSE_CONF = ASSETS / "modeles_grosse_conf.pptx"
PALETTE = {str(c) for c in (ANTHRACITE, RED, PINK, PINK_BG, RED_10, RED_20, RED_30, RED_40, WHITE)}
PALETTE.add("383840")  # l'anthracite du template, un cran au-dessus de #38383F de la charte : accepté


class ModeleGrosseConfDeck(ModeleMixin, GrosseConfDeck):
    PALETTE = PALETTE

    def __init__(self, template=MODELES_GROSSE_CONF, target="pptx"):
        super().__init__(template, target)
