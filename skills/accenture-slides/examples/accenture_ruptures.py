"""Exemple de référence Accenture « ruptures » : couverture, agenda, intercalaire numéroté, message clé et slide de
fin, les layouts du template qui portent le masque, les dégradés et le « > » de la marque.
Rendu attendu : assets/exemples/accenture_ruptures.png (planche des slides).

    uv run --with python-pptx --with pillow python examples/accenture_ruptures.py out.pptx

Ce qui fait le deck : les ruptures sont des layouts (jamais redessinées) ; les dégradés et le « > » viennent du
template ; le sous-titre est en Palatino, les titres en Arial Black.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from accenture_slides import AccentureDeck  # noqa: E402

d = AccentureDeck()
d.cover("Industrialiser l'IA générative", "Du premier cas d'usage à la plateforme", date="Mars 2027",
        author="OCTO Technology, part of Accenture")
d.agenda(["Le constat", "Notre approche", "Trois cas concrets", "La feuille de route"],
         intro="Une heure pour décider de la suite")
d.section("Notre approche", 2, "Cadrer, construire, industrialiser")
d.key_message("La valeur vient de la production, pas du POC")
d.closing("Merci")
d.save(sys.argv[1] if len(sys.argv) > 1 else "accenture_ruptures.pptx")
