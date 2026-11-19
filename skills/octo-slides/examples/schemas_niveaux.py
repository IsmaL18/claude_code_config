"""Exemple de référence « fourche, pyramide, définitions emboîtées » : trois schémas qu'on dessinait à la main.
Tirés du deck « Squad réduite augmentée par Claude Code » (weekly tribu, octobre 2026).
Rendu attendu : assets/exemples/schemas_niveaux.png.

    uv run --with python-pptx --with pillow python examples/schemas_niveaux.py out.pptx

1. Jonction puis fourche (join, fork) : trois preuves se rejoignent en un seul tronc qui entre dans « Merge main »,
   puis un seul tronc en sort et se divise vers dev et prod. Toutes les branches d'une fourche partent du même
   point ; deux connect() depuis une même boîte partiraient de points voisins et se croiseraient.
2. Pyramide (pyramid, modèle OCTO 231) : une pente unique, la pointe en turquoise (ce que nous connaissons), le bas
   en marine (ce que l'agent maîtrise), un filet pointillé tiré de la cassure vers les légendes.
3. Définitions emboîtées (nested, modèle OCTO 187) : du plus large au plus précis, une définition et un exemple par
   niveau, pour introduire des termes avant de s'en servir.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from octo_slides import (CONTENT, NAVY, NAVY_80, TURQ, TURQ_10, TURQ_20, TURQ_30, Deck, Emu,  # noqa: E402
                         Frame)

d = Deck()

# ---------------------------------------------------------------- 1. Jonction puis fourche
s = d.slide("Trois preuves pour merger, deux chemins pour livrer",
            "Les preuves se rejoignent avant main ; un seul tronc part ensuite vers chaque environnement.")
proofs_z, main_z, envs_z = CONTENT.pad(0, 0.2, 0, 0.3).cols([2.2, 1.9, 2.4], gap=1.05)
proofs = [d.box(s, *z, text, size=9.5) for z, text in zip(proofs_z.rows(3, gap=0.3), [
    "**Tests verts**\nunitaires et intégration", "**Revue de code**\npar l'agent puis par nous",
    "**Démo au PO**\nsur ses cas de référence"])]
main = d.box(s, *main_z.place(h=1.0, align="ml"), "**Merge main**\nseulement si tout est vert", size=9.5, fill=TURQ)
dev_z, prod_z = envs_z.pad(0, 0.35).rows(2, gap=0.6)
dev = d.box(s, *dev_z, "**Dev**\nun clic, mêmes tests rejoués", size=9.5)
prod = d.box(s, *prod_z, "**Prod**\nversion taguée, approbation", size=9.5, fill=NAVY)
d.join(s, proofs, main)
d.fork(s, main, [dev, prod])

# ---------------------------------------------------------------- 2. Pyramide et légendes
s = d.slide("L'agent maîtrise la base des tests, nous en connaissons la pointe",
            "Des milliers de tests écrits par l'agent ; nous ne suivons qu'une trentaine de cas métier.")
pyr_z, side_z = CONTENT.cols([4.0, None], gap=0.4)
pyr = d.pyramid(s, *pyr_z.pad(0, 0.1, 0, 0), [
    ("**Cas métier**\n32 cas", TURQ),
    ("**Tests d'intégration**", NAVY_80),
    ("**Tests unitaires**\nback et front", NAVY)], heights=[1.35, 1.0, None])
y_cut = pyr.cut(0)
d.rule(s, pyr.edge(y_cut) + 0.15, y_cut, side_z.right, y_cut, color=NAVY, dash=True)
top_band = Frame(side_z.x, pyr.tiers[0].y, side_z.w, y_cut - pyr.tiers[0].y - 0.1)
low_band, reassure_z = Frame(side_z.x, y_cut + 0.15, side_z.w, side_z.bottom - y_cut - 0.15).bottom_band(1.0, gap=0.15)
for band_z, picto, lead, body in [
        (top_band, "avatar_loupe", "Nous, on connaît la pointe.",
         "Des cas écrits par le métier : on sait ce que chacun vérifie, et le métier tranche un écart."),
        (low_band, "robot", "Le bas, seul l'agent le maîtrise.",
         "Il écrit les tests avant le code et les tient à jour. Nous n'en lisons pas le détail.")]:
    pic, txt = band_z.cols([0.45, None], gap=0.2)
    d.picto(s, picto, pic.x, band_z.y + 0.05, 0.45)
    t = d.text(s, txt.x - 0.08, txt.y, txt.w + 0.08, None, f"**{lead}**", size=12, line_spacing=1.1)
    d.text(s, txt.x - 0.08, txt.y + Emu(t.height).inches, txt.w + 0.08, None, body, size=10, line_spacing=1.3)
d.bloc(s, *reassure_z, corners="tr", radius=0.35, fill=TURQ_20, title="Ce qui nous rassure",
       body="Tests écrits avant le code, rejoués par la CI à chaque PR ; une page de synthèse en donne les chiffres.",
       title_size=10.5, size=9.5, pad=0.16)

# ---------------------------------------------------------------- 3. Définitions emboîtées
s = d.slide("Quatre mots pour parler d'un agent de code",
            "Du plus large au plus précis : chaque niveau s'appuie sur celui qui le contient.")
d.nested(s, *CONTENT, [
    ("**L'agent**, dans le terminal : il lit le repo, écrit le code, lance les tests.\n"
     "Exemple : « reproduis ce bug dans un test, puis corrige-le ».", TURQ_10),
    ("**Les règles du repo**, relues à chaque session : architecture, conventions, décisions déjà prises.\n"
     "Exemple : « l'agent ne commite jamais ».", TURQ_30),
    ("**Les skills**, des méthodes écrites que l'agent suit quand la tâche s'y prête.\n"
     "Exemple : test-driven-development, le test rouge avant le code.", TURQ),
    ("**Les commandes**, des raccourcis qui enchaînent des skills.\n"
     "Exemple : ==/dev-ticket== crée la branche du ticket et démarre la spec.", NAVY)])

d.save(sys.argv[1] if len(sys.argv) > 1 else "schemas_niveaux.pptx")
