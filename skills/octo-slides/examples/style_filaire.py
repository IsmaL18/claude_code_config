"""Exemple de référence « style filaire » : le vocabulaire graphique des slides préformatées OCTO, réutilisé.
Rendu attendu : assets/exemples/style_filaire.png.

    uv run --with python-pptx --with pillow python examples/style_filaire.py out.pptx

Les slides de la Com sont au trait : cartes et capsules à contour fin, pictos dans des médaillons cerclés, onglets
posés sur le bord des cartes, puces cibles turquoise, numéros en goutte, visuels 3D en goutte turquoise, très peu
d'aplats. Trois slides le montrent, sur la matière d'un deck d'acculturation à l'IA :
1. Capsules à médaillon (modèles 156, 157) : quatre familles d'usages, numéro en tête, picto en pied.
2. Cartes à onglet (modèles 153 à 155) et visuel 3D en goutte (asset 29.2, robot et bulles) : les étapes du RAG.
3. Chaîne d'anneaux empruntée au modèle 185 (asset 185.0) et médaillons posés dans les anneaux, numéros au trait
   (modèle 97) : une démarche en quatre temps.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from octo_modeles import ModeleDeck  # noqa: E402
from octo_slides import CONTENT, Frame  # noqa: E402

d = ModeleDeck()

# 1. Capsules à médaillon
s = d.slide("Quatre familles d'usages : prédire, classer, recommander, détecter",
            "Les mêmes ressorts dans votre téléphone et dans une chaufferie.")
FAMILLES = [("Prédire", "Combien ? Quand ?\nLa demande de chaleur du lendemain.", "statistiques"),
            ("Classer", "Dans quelle catégorie ?\nTrier les rapports d'intervention.", "folder-data"),
            ("Recommander", "Que faire ?\nLes réglages les plus sobres.", "point-clef"),
            ("Détecter", "Est-ce normal ?\nUne vibration anormale sur une turbine.", "alarme")]
for i, (zone, (titre, texte, picto)) in enumerate(zip(CONTENT.pad(0.6, 0, 0.6, 0).cols(4, gap=0.45), FAMILLES)):
    d.capsule(s, *zone, title=titre, body=texte, picto=picto, number=i + 1, size=10, title_size=12)

# 2. Cartes à onglet et visuel 3D en goutte
s = d.slide("Le RAG cherche dans vos documents avant de répondre",
            "Génération augmentée par la recherche : un examen à livre ouvert, sources citées.")
cartes, visuel = CONTENT.cols([None, 2.6], gap=0.5)
ETAPES = [("1. Chercher", "Le moteur trouve, dans vos procédures et rapports d'incident, les passages proches de la "
                          "question, par le sens et pas seulement par les mots."),
          ("2. Augmenter", "Ces passages sont ajoutés à la question : le modèle lit vos documents au moment de "
                           "répondre, sans réentraînement."),
          ("3. Générer", "Le modèle rédige la réponse et cite ses sources : chacun peut vérifier d'où vient "
                         "chaque information.")]
for zone, (onglet, texte) in zip(cartes.rows(3, gap=0.18), ETAPES):
    d.tab_card(s, *zone, onglet, texte, size=10)
d.asset(s, "29.2", *visuel.place(h=2.6, align="ml")[:3], h=2.6, shape="goutte")

# 3. Chaîne d'anneaux et numéros au trait
s = d.slide("Une démarche en quatre temps, du cas d'usage à la production",
            "Chaque anneau s'appuie sur le précédent ; on peut s'arrêter à chaque étape.")
chaine = d.asset(s, "185.0", 1.04, 1.45, 7.91)
centres = [1.04 + 1.124 + k * 1.855 for k in range(4)]  # centres des anneaux, relevés sur le modèle 185
cy = 1.45 + 1.12
for cx, picto in zip(centres, ["cible", "data", "intelligence-artificielle", "fusee"]):
    d.medaillon(s, cx, cy, 0.78, picto=picto)
TEMPS = [("Cadrer", "un problème métier, une mesure du succès"), ("Préparer", "les données, leur qualité"),
         ("Expérimenter", "un premier modèle, sur des cas réels"), ("Industrialiser", "la mise en production, "
                                                                     "puis le suivi")]
for i, (cx, (titre, texte)) in enumerate(zip(centres, TEMPS)):
    col = Frame(cx - 0.85, 3.95, 1.7, 1.1)
    d.text(s, col.x, col.y, col.w, None, f"**{i + 1}. {titre}**\n{texte}", size=10, align="center",
           line_spacing=1.25)

d.save(sys.argv[1] if len(sys.argv) > 1 else "style_filaire.pptx")
