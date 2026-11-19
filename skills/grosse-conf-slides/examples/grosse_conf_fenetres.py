"""Exemple de référence grosse conf « slide de texte » : le texte vit dans des fenêtres web, une illustration forte à
côté. Rendu attendu : assets/exemples/grosse_conf_fenetres.png.

    uv run --with python-pptx python examples/grosse_conf_fenetres.py out.pptx

Ce qui fait la slide : un seul aplat rouge (l'ombre de la fenêtre principale) pour le point focal, le reste au trait
anthracite sur blanc ; les deux fenêtres de textes sont de tailles différentes, la petite posée sur la grande ;
l'illustration est livrée avec sa propre fenêtre et n'est pas remise dans un cadre.

Mise en page (references/style_grosse_conf.md) : une découpe en deux colonnes de la zone CONTENT ; fenetre() renvoie la
zone intérieure, où le texte se pose.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from grosse_conf_slides import CONTENT, GrosseConfDeck  # noqa: E402

d = GrosseConfDeck()
s = d.slide("Une conf qui casse les codes.", "La data et l'IA, sans le bleu ni le noir habituels.")
texte, visuel = CONTENT.cols(["5fr", "4fr"], gap=0.4)

haut, reste = texte.top(1.5, gap=0.3)
inner = d.fenetre(s, *haut, title="Le parti pris")
d.text(s, *inner, "**Un décalage assumé.** Le rouge et le rose remplacent les codes habituels de la data et de l'IA, "
                  "sans rien perdre en lisibilité.", size=12)
inner = d.fenetre(s, *reste.place(w=reste.w - 0.5, h=1.2, align="tr"), title="Le principe", ombre=False)
d.text(s, *inner, "- Une idée par slide\n- Un seul aplat rouge", size=11)

cote = 3.3  # l'illustration garde sa fenêtre : pas de cadre autour, et elle reste à gauche du numéro de page
x, y = visuel.place(w=cote, h=cote, align="mc")[:2]
d.picto(s, "illu-boule-cristal", x, y, cote)
d.save(sys.argv[1] if len(sys.argv) > 1 else "grosse_conf_fenetres.pptx")
