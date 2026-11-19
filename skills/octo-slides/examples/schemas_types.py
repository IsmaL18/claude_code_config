"""Exemple de référence : quatre types de schémas qui reviennent, construits avec les helpers de schéma.
Rendu attendu : assets/exemples/schemas_types.png (planche des 4 slides).

    uv run --with python-pptx python examples/schemas_types.py out.pptx

1. Boucle de retour : humain → orchestrateur → conteneur d'agents, retour en flèche turquoise (loop_back).
2. Éventail : une commande, N agents en parallèle, une synthèse (fork vers les agents, join vers la synthèse :
   un seul tronc par boîte, 0,9 pouce d'écart pour que chaque branche garde une tige).
3. Cycle : quatre étapes qui bouclent, l'étape clé détaillée dans un conteneur (cycle).
4. Gantt de principe : couloirs, barres, la phase clé en turquoise plein (lane, bar).

Mise en page (references/mise_en_page.md) : chaque slide part de CONTENT découpé en colonnes ; les flèches entre
deux formes passent par connect(), qui les centre sur la partie commune des formes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from octo_slides import CONTENT, NAVY, NAVY_10, Deck, Emu, Frame, text_height  # noqa: E402

d = Deck()

# 1. Boucle de retour
s = d.slide("Je formule, les agents réalisent, je valide", "Le product owner pilote une équipe d'agents.")
haut, bas = CONTENT.top(2.25, gap=0.3)
po, orch_col, agents_col = haut.cols([1.5, 1.55, None], gap=0.7)
avatar = d.picto(s, "avatar_homme", po.cx - 0.65, po.y + 0.1, 1.3)
po_label = d.text(s, po.x, po.y + 1.45, po.w, None, "**Le PO**\nformule, valide", size=9, align="center",
                  line_spacing=1.0)
orch = d.box(s, *orch_col.place(h=0.5, align="tl").move(dy=0.85), "**Orchestrateur**", size=9, header=True)
agents = d.container(s, *agents_col, label="Agents")
interieur = agents_col.pad(0.15, 0.32, 0.15, 0.15)
roles, code = interieur.top(0.81, gap=0.12)
for zone, role in zip([c for r in roles.grid(2, 2, gap=0.09) for c in r],
                      ["Analyste", "Architecte", "Développeur", "Testeur"]):
    d.box(s, *zone, role, size=9)
d.box(s, *code, "**Le code** : écrit, testé, débogué par les agents.", size=9, fill=NAVY_10)
d.connect(s, avatar, orch)
d.connect(s, orch, agents)
retour_y = agents_col.bottom + 0.35
label_bas = Emu(po_label.top + po_label.height).inches
d.loop_back(s, [(agents_col.cx, agents_col.bottom), (agents_col.cx, retour_y), (po.cx, retour_y),
                (po.cx, label_bas + 0.06)])
d.text(s, po.cx + 0.3, retour_y + 0.08, agents_col.cx - po.cx - 0.6, None,
       "**Résultat et preuves**, puis : valide ou demande une reprise", size=9.5, align="center")

# 2. Éventail
s = d.slide("Une commande, des agents en parallèle, une synthèse", "L'orchestrateur découpe, puis rassemble.")
schema = CONTENT.place(h=2.6, align="mc").move(dy=-0.2)
commande_col, orch_col, agents_col, synthese_col = schema.cols([1.3, 1.5, 1.3, None], gap=0.9)
commande = d.box(s, *commande_col.place(h=0.6, align="ml"), "**Une commande**", size=10)
orch = d.box(s, *orch_col.place(h=0.6, align="ml"), "**Orchestrateur**", size=10, header=True)
synthese = d.box(s, *synthese_col.place(h=0.6, align="ml"), "**Synthèse et décisions**", size=10, fill=NAVY)
d.connect(s, commande, orch)
agents = [d.box(s, *zone, "Agent", size=10) for zone in agents_col.rows(3, gap=0.55)]
d.fork(s, orch, agents)
d.join(s, agents, synthese)
d.text(s, agents_col.x - 0.2, schema.bottom + 0.1, agents_col.w + 0.4, None, "en parallèle", size=9, align="center")

# 3. Cycle
s = d.slide("Mesurer, décider, livrer, observer : la boucle de pilotage", "L'étape clé est détaillée à droite.")
gauche, droite = CONTENT.cols([None, 3.3], gap=0.55)
W, H, RX, RY = 1.4, 0.5, 1.65, 1.2
centres = d.cycle(s, gauche.cx, gauche.cy, ["Mesurer", "Décider", "Livrer", "Observer"], key=1, rx=RX, ry=RY, w=W)
(dx, dy) = centres[1]
points = "- **Un verbe** par sujet : applique, refuse, adopte, écarte.\n- **Une date** tracée.\n" \
         "- **L'humain** a le dernier mot."
# Le cadre prend la hauteur de son texte (pas celle du cycle : il serait à moitié vide), centré sur l'étape détaillée.
detail_h = 0.4 + text_height(points, droite.w - 0.3, 10.5, line_spacing=1.4) + 0.15
detail = Frame(droite.x, dy - detail_h / 2, droite.w, detail_h)
d.container(s, *detail, label="Décider")
d.text(s, *detail.pad(0.15, 0.4, 0.15, 0.15), points, size=10.5, line_spacing=1.4)
d.connect(s, (dx - W / 2, dy - H / 2, W, H), detail, dash=True)

# 4. Gantt de principe
s = d.slide("Trois couloirs, une phase clé", "Un Gantt de principe : pas de dates, l'enchaînement suffit.")
barres = {}
for k, (label, bars) in enumerate([("Données", [(2.3, 1.8, "Collecte", False)]),
                                   ("Modèle", [(3.9, 2.2, "Entraînement", False), (6.3, 1.6, "Validation", True)]),
                                   ("Production", [(7.6, 1.6, "Déploiement", False)])]):
    y = 1.8 + k * 0.9
    d.lane(s, CONTENT.x, y, CONTENT.w, label)
    for bx, bw, text, key in bars:
        barres[text] = d.bar(s, bx, y, bw, text, key=key)
d.connect(s, barres["Validation"], barres["Déploiement"], dash=True)
d.takeaway(s, "La validation conditionne le déploiement : c'est elle qu'on outille en premier.", picto="cible",
           y=4.3)

d.save(sys.argv[1] if len(sys.argv) > 1 else "schemas_types.pptx")
