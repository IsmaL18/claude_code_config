"""Exemple de référence « schéma » : un pipeline d'étapes, des preuves accrochées sous chaque étape en flèches
pointillées, qui convergent vers une conclusion marine. Tiré du deck « Sur parole ou sur preuves » (OCTO Talks).
Rendu attendu : assets/exemples/pipeline_preuves.png.

    uv run --with python-pptx python examples/pipeline_preuves.py out.pptx

Ce qui fait la slide : le mécanisme se lit de gauche à droite (étapes), puis de haut en bas (ce que chaque étape
laisse comme trace), et la boîte marine dit ce qu'on en conclut. Une seule étape mise en avant (en-tête turquoise).

Mise en page (references/mise_en_page.md) : une seule découpe en colonnes sert aux étapes, aux preuves et à la
conclusion, si bien que chaque preuve tombe sous son étape ; toutes les flèches passent par connect().
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from octo_slides import CONTENT, NAVY, Deck, Emu  # noqa: E402

N = " "  # espace insécable avant « : ; ! ? % »

d = Deck()
s = d.slide("Quatre preuves remplacent la lecture du code",
            "Chaque demande traverse trois étapes confiées aux agents et laisse des traces lisibles.")

# Trois bandes : les étapes, les preuves, la conclusion ; les mêmes colonnes pour les trois. La hauteur des preuves
# suit leur contenu : le blanc restant va sous la conclusion, pas dans des cartes à moitié vides.
COLS = [1.15, 1.15, 1.15, 2.5, None]
GAP = 0.42  # assez pour que chaque flèche garde une tige derrière sa pointe
etapes_bande, reste = CONTENT.top(0.45, gap=0.5)
preuves_bande, reste = reste.top(1.45, gap=0.4)
conclusion_bande, _ = reste.top(0.7)
etapes_zones = etapes_bande.cols(COLS, GAP)
preuves_zones = preuves_bande.cols(COLS, GAP)

labels = [("Demande", False), ("Cadrer", False), ("Réaliser", False), ("Vérifier", True), ("Livrable", False)]
etapes = [d.box(s, *z, f"**{label}**", size=9.5, header=key) for z, (label, key) in zip(etapes_zones, labels)]
for a, b in zip(etapes, etapes[1:]):
    d.connect(s, a, b)


def preuve(zone, picto, titre, texte):
    """Carte de preuve : même structure partout (picto, titre, texte), texte ajusté à la carte."""
    carte = d.box(s, *zone)
    inner = zone.pad(0.12)
    d.picto(s, picto, inner.x, inner.y, 0.4)
    t = d.text(s, inner.x - 0.08, inner.y + 0.48, inner.w + 0.16, None, f"**{titre}**", size=8.5, line_spacing=1.0)
    top = inner.y + 0.48 + Emu(t.height).inches
    d.text(s, inner.x - 0.08, top, inner.w + 0.16, inner.bottom - top + 0.04, texte, size=8, line_spacing=1.1)
    return carte


# Le journal couvre les deux premières étapes ; l'étape « Vérifier » laisse deux preuves.
rendu_zone, revue_zone = preuves_zones[3].cols(2, gap=0.1)
journal = preuve(preuves_zones[0].union(preuves_zones[1]), "journal", "Journal des exécutions",
                 f"Une ligne par demande, à chaque étape. Interdit d'écrire «{N}succès{N}» sur un livrable à valider.")
tests = preuve(preuves_zones[2], "tests-reussite", "Tests rejoués", f"**4{N}228** sur le hub, tous rejoués avant de rendre la main.")
rendu = preuve(rendu_zone, "oeil", "Rendu regardé", "Capture de l'écran que verra l'utilisateur.")
revue = preuve(revue_zone, "robot", "Revue d'un autre agent", "Rapport classé par gravité.")

# Ce qui n'est pas lu : en pointillés, hors du flux des preuves.
code_zone = preuves_zones[4]
code = d.container(s, *code_zone)
d.text(s, *code_zone.pad(0.05), "**Code**\nnon lu par l'humain", size=8, align="center", anchor="middle")

for etape, cible in [(etapes[0], journal), (etapes[1], journal), (etapes[2], tests), (etapes[3], rendu),
                     (etapes[3], revue), (etapes[4], code)]:
    d.connect(s, etape, cible, dash=True)

# La conclusion : un seul aplat marine, sous les quatre colonnes qui laissent une preuve.
largeur = preuves_zones[0].union(preuves_zones[3])
conclusion = d.box(s, largeur.x, conclusion_bande.y, largeur.w, conclusion_bande.h,
                   "**L'humain lit les preuves, pas le code.** Elles disent que le travail a été fait comme prévu, "
                   "pas qu'il fallait le faire.", size=9.5, fill=NAVY, align="left")
for p in (journal, tests, rendu, revue):
    d.connect(s, p, conclusion)

d.save(sys.argv[1] if len(sys.argv) > 1 else "pipeline_preuves.pptx")
