"""Partir d'un visuel de la bibliothèque Accenture (assets/modeles_accenture.pptx) et l'adapter au contenu.

Mêmes méthodes que les modèles OCTO (show, modele, set_text, set_cell, remove, duplicate, move, recolor,
replace_picture, borrow, check : modeles_base.ModeleMixin), sur la bibliothèque de visuels du starter pack Accenture
(graphiques, concepts dynamiques, processus, objets statiques, cartes, gestion de projet, équipes, évaluation,
cadres d'analyse), avec les helpers et la palette d'AccentureDeck ; rien d'OCTO ni de La Grosse Conf :

    import sys; sys.path.insert(0, "<skill>/scripts")
    from accenture_modeles import ModeleAccentureDeck
    d = ModeleAccentureDeck()
    d.show(120)                       # liste les formes du modèle 120 : chemin, type, position, texte
    s = d.modele(120)                 # copie du modèle, consignes (« Hints: ») retirées
    d.set_text(s, "2", "Titre du schéma")
    d.check(s)                        # écarts à la charte et textes de gabarit restants (« Text », « Insert text »)
    d.save("deck.pptx")               # seules les slides créées sont gardées

Les numéros sont ceux de references/modeles_index_accenture.md. Les icônes se posent par leur nom (picto, carte,
replace_picture) depuis assets/pictos-accenture.
"""
import re

from accenture_slides import (BLACK, GREY, GREY_LIGHT, LAVENDER, LILAC, LILAC_LIGHT, MAUVE, PURPLE, PURPLE_DARK,
                              PURPLE_DARKEST, AccentureDeck)
from deck_base import ASSETS, WHITE
from modeles_base import ModeleMixin

MODELES_ACCENTURE = ASSETS / "modeles_accenture.pptx"
PALETTE = {str(c) for c in (PURPLE, PURPLE_DARK, PURPLE_DARKEST, MAUVE, LAVENDER, LILAC, LILAC_LIGHT, BLACK, GREY,
                            GREY_LIGHT, WHITE)}
# Gris neutres de la bibliothèque de visuels (filets, trames, axes de graphiques) : acceptés.
PALETTE |= {"D4D4D0", "BFBFB9", "E9E9E7", "F2F2F2", "F4F4F0", "A055F5"}
# Consignes de la bibliothèque : modes d'emploi (« Hints: », « Instructions: »), aides de carte.
CONSIGNES = re.compile(r"^\s*(Hints?|Instructions?)\s*:|Ungroup map to select|Format Background", re.I | re.M)
# Textes de gabarit à remplacer : « Text », « TEXT », « Insert text here », « Body copy », « Label A », « Option 1 »…
GABARIT = re.compile(r"^\s*(Text|TEXT|Insert text( here)?|Body copy|Label [A-Z]?|Headline|Lorem ipsum.*|Product \d+|"
                     r"Option \d+|xx+)\s*$|Insert text here|<[^>]+>", re.M)


class ModeleAccentureDeck(ModeleMixin, AccentureDeck):
    """Deck Accenture qui part de la bibliothèque de visuels du starter pack (assets/modeles_accenture.pptx) : tous
    les helpers d'AccentureDeck, plus ceux de ModeleMixin (modeles_base.py)."""
    PALETTE = PALETTE
    CONSIGNES = CONSIGNES
    GABARIT = GABARIT
    NOIR_INTERDIT = False  # texte noir : la règle de la charte Accenture
    SIGLES = ("TEXT", "OCTO", "MLOPS", "LLM", "API", "KPI", "CESR", "AMC")

    def __init__(self, template=MODELES_ACCENTURE, target="pptx", lang=None):
        if lang:
            self.LANG = lang
        super().__init__(template, target)
