"""Exemple de référence Accenture « contenu » : les composants de la charte sur des slides de contenu (processus en
chevrons à étape focale, passage d'un état à un autre, chiffres clés, cartes à icône monoline, colonnes numérotées).
Rendu attendu : assets/exemples/accenture_contenu.png (planche des slides).

    uv run --with python-pptx --with pillow python examples/accenture_contenu.py out.pptx

Ce qui fait le deck : beaucoup de blanc, un seul violet fort par slide (l'étape focale, le chiffre, le panneau
d'arrivée), le gris chaud clair pour tout le reste, des titres-messages en Arial Black sur une ligne.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from accenture_slides import CONTENT, AccentureDeck  # noqa: E402

d = AccentureDeck()

s = d.slide("Trois étapes pour passer à l'échelle", "L'industrialisation se prépare dès le cadrage")
d.etapes(s, CONTENT.pad(0, 0.3, 0, 0), [
    ("Cadrer", "Un cas d'usage, un sponsor métier et une mesure de valeur avant la première ligne de code."),
    ("Construire", "Un produit minimal en six semaines, évalué sur des données réelles."),
    ("Industrialiser", "Une plateforme partagée : déploiement, suivi et coûts maîtrisés."),
], focal=2)

s = d.slide("Ce qui change pour vos équipes")
d.de_a(s, CONTENT, "- Des POC isolés, sans suite\n- Des modèles jamais suivis\n- Des coûts découverts trop tard",
       "- Une plateforme partagée\n- Des modèles suivis en production\n- Un coût par cas d'usage connu")

s = d.slide("Le programme en trois chiffres")
d.chiffres(s, CONTENT, [("80 %", "des POC n'atteignent jamais la production"),
                        ("6 sem.", "pour un premier produit en production"), ("x3", "cas d'usage livrés par an")])

s = d.slide("Trois briques, un seul socle")
for col, (picto, title, body) in zip(CONTENT.pad(0, 0.3, 0, 0).cols(3, gap=0.6), [
        ("cible", "Cibler", "Les cas d'usage qui comptent, classés par valeur et faisabilité."),
        ("engrenages", "Outiller", "Une plateforme commune pour déployer et suivre les modèles."),
        ("tendance-hausse", "Mesurer", "La valeur produite, suivie cas par cas.")]):
    d.carte(s, *col.place(h=2.6), picto, title, body, size=14)

s = d.slide("Nos principes")
d.colonnes(s, CONTENT.pad(0, 0.2, 0, 0), [
    ("Partir du métier", "Chaque cas d'usage a un sponsor et une mesure de valeur."),
    ("Livrer vite", "Un produit en production en six semaines, puis on itère."),
    ("Industrialiser tôt", "La plateforme se construit avec le premier cas, pas après."),
])
d.save(sys.argv[1] if len(sys.argv) > 1 else "accenture_contenu.pptx")
