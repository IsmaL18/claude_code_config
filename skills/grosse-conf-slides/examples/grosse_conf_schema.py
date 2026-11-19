"""Exemple de référence grosse conf « schéma » : un mécanisme à plat (pas de fenêtre autour), trois étapes reliées
par des flèches anthracite, une boucle de retour rouge, un seul aplat rouge pour le cœur du dispositif.
Rendu attendu : assets/exemples/grosse_conf_schema.png.

    uv run --with python-pptx python examples/grosse_conf_schema.py out.pptx

Ce qui fait la slide : le mécanisme se lit de gauche à droite ; l'étape centrale est la seule en rouge (blanc gras
sur rouge, au-dessus de 14 pt : charte_grosse_conf.md) ; les deux autres sont au trait sur blanc ; la boucle de retour
est rouge. Les flèches passent par connect() et loop_back().
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from grosse_conf_slides import ANTHRACITE, CONTENT, RED, WHITE, GrosseConfDeck  # noqa: E402

d = GrosseConfDeck()
s = d.slide("Chaque expérience nourrit la suivante.", "Un cycle court vaut mieux qu'un grand plan.")
zone = CONTENT.pad(0, 0.6, 0, 0.5)
a, b, c = (col.place(h=1.0, align="mc") for col in zone.cols(3, gap=0.9))
essayer = d.aplat(s, *a, "Essayer", fill=WHITE, size=16)
mesurer = d.aplat(s, *b, "Mesurer", fill=RED, size=16)
partager = d.aplat(s, *c, "Partager", fill=WHITE, size=16)
d.connect(s, essayer, mesurer)
d.connect(s, mesurer, partager)
y = a.bottom + 0.55  # la boucle revient sous les trois étapes, de la dernière à la première
d.loop_back(s, [(c.cx, c.bottom + 0.1), (c.cx, y), (a.cx, y), (a.cx, a.bottom + 0.1)])
d.text(s, zone.x, y + 0.15, zone.w, 0.3, "On recommence avec ce qu'on a appris.", size=11, color=ANTHRACITE,
       align="center")
d.save(sys.argv[1] if len(sys.argv) > 1 else "grosse_conf_schema.pptx")
