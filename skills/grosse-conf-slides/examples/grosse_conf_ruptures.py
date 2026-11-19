"""Exemple de référence grosse conf « ruptures » : couverture, sommaire, intercalaire à illustration et slide focus,
les quatre layouts du template qui portent le masque et les illustrations de la conf.
Rendu attendu : assets/exemples/grosse_conf_ruptures.png (planche de quatre slides).

    uv run --with python-pptx python examples/grosse_conf_ruptures.py out.pptx

Ce qui fait le deck : les ruptures sont des layouts (jamais redessinées), sur fond rose pâle ; le sommaire est sur fond
blanc ; l'intercalaire reprend une illustration filaire dans sa fenêtre.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from grosse_conf_slides import GrosseConfDeck  # noqa: E402

d = GrosseConfDeck()
d.cover("09.03.2027", "Maison de la Chimie")
d.toc(["Pourquoi", "Comment", "Quoi"])
d.chapter("Pourquoi.", 1, "illu-boule-cristal")
d.focus("Le message clé.", "Ce qu'il faut retenir", "Casser les codes, sans rien perdre en lisibilité.")
d.save(sys.argv[1] if len(sys.argv) > 1 else "grosse_conf_ruptures.pptx")
