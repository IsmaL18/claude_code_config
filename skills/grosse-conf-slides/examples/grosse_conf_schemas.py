"""Exemple de référence grosse conf « schémas » : les six recettes de `style_grosse_conf.md` (§3), une par slide :
équation de pictos, cercles emboîtés, étapes avec boucle de retour, élément central entouré, cycle en quatre
cartes, grille de fenêtres à picto. Rendu attendu : assets/exemples/grosse_conf_schemas.png (six slides).

    uv run --with python-pptx python examples/grosse_conf_schemas.py out.pptx

Ce qui fait ces slides : chacune dessine son mécanisme (une relation, une inclusion, un ordre, un entourage, une
boucle, des cas indépendants) avec un picto de la conf par idée, un seul accent rouge, des flèches anthracite et une
boucle de retour rouge ; aucune ne se réduit à des puces. Les helpers prennent une zone (`CONTENT.cols`, `rows`…) :
jamais de coordonnées à la main.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from grosse_conf_slides import CONTENT, GrosseConfDeck  # noqa: E402

d = GrosseConfDeck()

s = d.slide("Un agent, c'est un modèle et ce qui l'entoure.", "Une équation : trois termes, chacun son picto.")
d.equation(s, CONTENT, [("drone", "Agent"), ("cerveau", "Model"), ("prise-jack", "Harness")])

s = d.slide("Chaque niveau contient le précédent.", "Cercles emboîtés : du plus étroit au plus large.")
gauche, droite = CONTENT.left(3.5, gap=0.5)
rond = d.cible(s, gauche, ["Large", "Moyen", "Étroit"])
for cell, (nom, titre, texte) in zip(droite.__class__(droite.x, rond.y, droite.w, rond.h).rows(3, gap=0.2), (
        ("ecriture", "Étroit", "Le niveau du centre."), ("livre", "Moyen", "Il contient l'étroit."),
        ("fenetres", "Large", "Il contient les deux autres."))):
    d.carte(s, *cell, nom, titre, texte, size=11)

s = d.slide("Les étapes se suivent, et la dernière relance la première.", "Étapes en cartes, boucle de retour rouge.")
d.pipeline(s, CONTENT, [("cuisine", "Préparer", "Le point de départ."), ("artiste", "Produire", "Une chose à la fois."),
                        ("entonnoir-1", "Vérifier", "Un test avant de continuer.")],
           focal=1, retour="On recommence avec ce qu'on a appris")

s = d.slide("Un élément, six familles autour de lui.", "Élément central relié à ce qui l'entoure.")
d.radial(s, CONTENT, "Au centre",
         [("livre", "Famille A", "Texte court."), ("calculatrice", "Famille B", "Texte court."),
          ("fenetres", "Famille C", "Texte court.")],
         [("agenda", "Famille D", "Texte court."), ("entonnoir-1", "Famille E", "Texte court."),
          ("participants", "Famille F", "Texte court.")])

s = d.slide("Chaque erreur devient un correctif.", "Cycle en quatre cartes, une ombre rouge sur le point focal.")
d.boucle(s, CONTENT, [("canard", "Une erreur"), ("carte-3", "Sa cause"), ("equerre", "Une règle"),
                      ("fauteuil", "Plus d'erreur")])

s = d.slide("Quatre cas, aucun lien entre eux.", "Grille de fenêtres à picto : rien à relier, donc pas de flèche.")
d.grille(s, CONTENT, [("mixer", "Premier cas", "Une phrase qui le décrit."),
                      ("megaphone", "Deuxième cas", "Une phrase qui le décrit."),
                      ("site-date", "Troisième cas", "Une phrase qui le décrit."),
                      ("boule-cristal", "Quatrième cas", "Une phrase qui le décrit.")])
d.save(sys.argv[1] if len(sys.argv) > 1 else "grosse_conf_schemas.pptx")
