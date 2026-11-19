"""Exemple de référence « pédagogie » : trois façons de faire comprendre plutôt que d'énumérer.
Tirées du deck « Acculturation IA du CoDir de la CCIAG » (octobre 2026), slides saluées par l'utilisateur.
Rendu attendu : assets/exemples/pedagogie.png.

    uv run --with python-pptx --with pillow python examples/pedagogie.py out.pptx

1. Un objet réel annoté plutôt qu'une liste de critères : un relevé de pompe, ses défauts entourés de turquoise et
   numérotés, reliés aux trois questions (quantité, qualité, étiquetage), et une analogie en bandeau.
2. Un même exemple suivi d'étape en étape : la même demande posée au modèle à chaque étape de son apprentissage, une
   réponse par étape, en bulles alignées d'une colonne à l'autre (chat, heights=).
3. Un mini-schéma par élément d'une grille plutôt qu'un picto : prolonger une série, ranger dans une case, proposer
   le bon choix, repérer le point hors norme ; la question, un exemple du quotidien et un exemple métier dessous.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402

from octo_slides import (CONTENT, NAVY, NAVY_30, TURQ, TURQ_10, TURQ_30, WHITE, Deck, Frame,  # noqa: E402
                         bloc_height, text_height)

d = Deck()

# 1. L'objet réel annoté
s = d.slide("Pas de bon modèle sans bonnes données : quantité, qualité, étiquetage",
            "Trois questions à poser sur vos propres données, avant tout projet.")
corps, bas = CONTENT.bottom_band(0.6, gap=0.25)
gauche, droite = corps.cols([None, 3.3], gap=0.35)
d.text(s, gauche.x - 0.08, gauche.y, gauche.w, 0.3, "**Les relevés d'une pompe**, un exemple", size=10.5)
RELEVES = [["Jour", "Température", "Pression (bar)", "Panne ?"],
           ["1er février", "72", "6,1", "non"], ["2 février", "73", "6,0", "non"], ["3 février", "", "6,2", "non"],
           ["4 février", "163", "6,1", "non"], ["5 février", "75", "4,2", "?"], ["6 février", "74", "6,0", "non"]]
CW, RH = [1.2, 1.15, 1.2, 0.85], 0.33
tx, ty = gauche.x, gauche.y + 0.42
d.table(s, tx, ty, sum(CW), RELEVES, col_widths=CW, row_h=RH, size=9.5)
for rang, col, num in [(0, 3, 1), (3, 1, 2), (4, 1, 2), (5, 3, 3)]:  # défauts entourés, numérotés comme les questions
    cx = tx + sum(CW[:col])
    d._shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx + 0.05, ty + rang * RH + 0.04, CW[col] - 0.1, RH - 0.08, fill=None,
             line=TURQ, line_w=2.25, adj=[0.3])
    d.goutte(s, tx + sum(CW) + 0.12, ty + rang * RH + (RH - 0.3) / 2, 0.3, corner="tr", fill=TURQ, text=str(num),
             size=8.5)
POINTS = [("1. Quantité", "Presque que des « non » : combien de pannes en dix ans ? Assez pour apprendre ?", WHITE),
          ("2. Qualité", "Une case vide, un relevé en Fahrenheit : des trous et des unités qui changent.", WHITE),
          ("3. Étiquetage", "« ? » : personne n'a noté si c'était une panne. Étiqueter, c'est noter la bonne "
                            "réponse ; vos experts métier le savent.", TURQ_10)]
hs = [bloc_height(droite.w, t, b, 11, 9.5, pad=0.18) for t, b, _ in POINTS]
for z, corner, (t, b, fill) in zip(droite.place(h=sum(hs), align="ml").rows(hs, gap=0), ["tr", "none", "br"], POINTS):
    d.bloc(s, *z, corners=corner, radius=0.35, fill=fill, title=t, body=b, title_size=11, size=9.5, pad=0.18)
d.banner(s, *bas, "**Comme en cuisine, pas de bon plat sans bons ingrédients.** Les données se collectent et se "
                  "documentent avant d'en avoir besoin.", picto="data", corners="tl")

# 2. Le même exemple, d'étape en étape
s = d.slide("De la machine à mots à l'assistant : comment ChatGPT est né",
            "Trois étapes d'apprentissage, comme un élève : il lit, il s'exerce, il est corrigé.")
corps, bas = CONTENT.bottom_band(0.6, gap=0.25)
DEMANDE = ("Vous", "écris un mail pour annuler la réunion de demain.")
ETAPES = [("1. Lire", "Comme un élève qui lit toute la bibliothèque.",
           "écris un mail pour la reporter. Écris un mail pour prévenir l'équipe. Écris…",
           "Il continue le texte, sans répondre.", "C'est le pré-entraînement.", WHITE),
          ("2. S'exercer", "Comme un élève qui fait des exercices corrigés.",
           "bonjour, je dois annuler la réunion de demain. Je reviens vers vous avec une date.",
           "Il suit la consigne.", "C'est l'ajustement.", TURQ_10),
          ("3. Être corrigé", "Comme un élève qui reçoit des notes.",
           "bonjour à tous, la réunion de demain est annulée. Je vous propose deux créneaux ; faut-il préciser le "
           "motif ?", "Il répond en assistant.", "C'est l'alignement.", TURQ_30)]
cols3 = corps.cols(3, gap=0.45)
iw = cols3[0].w - 0.36
bw = iw * 0.86
an_h = max(text_height(e[1], iw + 0.16, 9, line_spacing=1.2) for e in ETAPES)
heights = [text_height(f"**{DEMANDE[0]}** : {DEMANDE[1]}", bw, 8.5) + 0.02,  # bulles alignées entre colonnes
           max(text_height(f"**Le modèle** : {e[2]}", bw, 8.5) for e in ETAPES) + 0.02]
for z, (titre, analogie, reponse, verdict, technique, fill) in zip(cols3, ETAPES):
    d.bloc(s, *z, corners="tl-br", radius=0.35, fill=fill)
    inner = z.pad(0.18, 0.14)
    t = d.text(s, inner.x - 0.08, inner.y, inner.w + 0.16, None, f"**{titre}**", size=13, line_spacing=1.1)
    y = inner.y + t.height / 914400
    d.text(s, inner.x - 0.08, y, inner.w + 0.16, an_h, analogie, size=9, color=NAVY, line_spacing=1.2)
    y = d.chat(s, inner.x, y + an_h + 0.1, inner.w, [DEMANDE, ("Le modèle", reponse)], heights=heights) + 0.08
    d.text(s, inner.x - 0.08, y, inner.w + 0.16, inner.bottom - y, f"**{verdict}**\n{technique}", size=9,
           anchor="bottom", line_spacing=1.25)
for a, b in zip(cols3, cols3[1:]):
    d.chevron(s, (a.right + b.x) / 2 + 0.06, a.cy, size=0.22)
d.banner(s, *bas, "**Retenez** : le modèle de base sait continuer un texte ; ce sont des humains qui, en le "
                  "corrigeant, en font un assistant.", fill=TURQ_10)

# 3. Un mini-schéma par élément
s = d.slide("Quatre familles d'usages : prédire, classer, recommander, détecter",
            "Les mêmes ressorts dans votre téléphone et dans une chaufferie.")


def predire(v):
    base, step = v.bottom - 0.05, (v.w - 0.2) / 6
    for k, h in enumerate([0.35, 0.5, 0.42, 0.62, 0.55]):
        d._shape(s, MSO_SHAPE.RECTANGLE, v.x + 0.1 + k * step, base - h, 0.2, h, fill=TURQ_30, line=None)
    x = v.x + 0.1 + 5 * step
    d._shape(s, MSO_SHAPE.RECTANGLE, x, base - 0.72, 0.2, 0.72, fill=None, line=NAVY, dash=True)
    d.text(s, x - 0.15, base - 0.98, 0.5, 0.26, "**?**", size=11, align="center", anchor="middle")
    d.rule(s, v.x + 0.05, base, v.right - 0.05, base, color=NAVY)


def classer(v):
    cases = [Frame(v.x + 0.08, v.bottom - 0.5, 0.72, 0.48), Frame(v.right - 0.8, v.bottom - 0.5, 0.72, 0.48)]
    for k, c in enumerate(cases):
        d._shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, *c, fill=WHITE, line=NAVY, adj=[0.2])
        for j in range(3):
            x = c.x + 0.14 + j * 0.2
            if k == 0:
                d.circle(s, x + 0.07, c.cy, 0.065, fill=TURQ, line=None)
            else:
                d._shape(s, MSO_SHAPE.RECTANGLE, x, c.cy - 0.065, 0.13, 0.13, fill=NAVY_30, line=None)
    d.circle(s, cases[0].cx, v.y + 0.12, 0.08, fill=TURQ, line=None)  # la bille tombe à la verticale
    d.rule(s, cases[0].cx, v.y + 0.24, cases[0].cx, cases[0].y - 0.05, color=NAVY, dash=True)


def recommander(v):
    d.picto(s, "avatar_femme", v.x + 0.02, v.cy - 0.3, 0.6)
    tx = v.right - 1.05  # fourche à angles droits
    d.rule(s, v.x + 0.65, v.cy, tx, v.cy, color=NAVY, width=1)
    d.rule(s, tx, v.cy - 0.26, tx, v.cy + 0.26, color=NAVY_30, width=1)
    for k, dy in enumerate((-0.38, -0.12, 0.14)):
        c = Frame(v.right - 0.85, v.cy + dy, 0.85, 0.24)
        d.rule(s, tx, c.cy, c.x - 0.02, c.cy, color=NAVY if k == 1 else NAVY_30, width=1)
        sh = d._shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, *c, fill=TURQ if k == 1 else WHITE, line=NAVY, adj=[0.3])
        if k == 1:
            d._fill_text(sh.text_frame, "**pour vous**", 7.5, NAVY, "center", "middle")
            sh.text_frame.margin_top = sh.text_frame.margin_bottom = 0


def detecter(v):
    y0 = v.cy + 0.2
    d.rule(s, v.x + 0.05, y0, v.right - 0.05, y0, color=NAVY_30, dash=True)
    d.text(s, v.right - 0.7, y0 + 0.04, 0.7, 0.2, "normal", size=7.5, align="right")
    step = (v.w - 0.3) / 8
    for k, jit in enumerate([0.02, -0.03, 0.01, -0.02, 0.03, -0.01, None, 0.02, -0.02]):
        x = v.x + 0.15 + k * step
        if jit is None:
            d.circle(s, x, v.y + 0.25, 0.06, fill=TURQ, line=None)
            d.circle(s, x, v.y + 0.25, 0.16, fill=None, line=TURQ, line_w=2)
        else:
            d.circle(s, x, y0 + jit, 0.05, fill=NAVY, line=None)


FAM = [("Prédire", "Combien ? Quand ?", "l'heure d'arrivée du GPS", "la demande de chaleur de demain", predire),
       ("Classer", "Dans quelle catégorie ?", "le tri du spam", "trier les rapports d'intervention", classer),
       ("Recommander", "Que faire ?", "le film suivant sur Netflix", "les réglages de chaudière les plus sobres",
        recommander),
       ("Détecter", "Est-ce normal ?", "l'alerte de fraude de la banque", "une vibration anormale sur une turbine",
        detecter)]
texte = lambda q, a, b: f"**{q}**\n**Au quotidien** : {a}.\n**En industrie** : {b}."  # noqa: E731
th = max(text_height(texte(q, a, b), CONTENT.w / 4 - 0.24, 9.5, line_spacing=1.3) for _, q, a, b, _ in FAM)
fh = 0.15 + 0.36 + 0.12 + 1.05 + 0.12 + th + 0.12
corps, bas = CONTENT.place(h=fh + 0.25 + 0.45, align="ml").rows([fh, 0.45], gap=0.25)
for z, corner, (verbe, q, a, b, mini) in zip(corps.cols(4, gap=0), ["tl", "none", "none", "br"], FAM):
    d.bloc(s, *z, corners=corner, fill=WHITE)
    t_z, v_z, x_z = z.pad(0.2, 0.15, 0.2, 0.12).rows([0.36, 1.05, None], gap=0.12)
    d.text(s, t_z.x - 0.08, t_z.y, t_z.w, t_z.h, f"**{verbe}**", size=15, anchor="middle")
    mini(v_z)
    d.text(s, x_z.x - 0.08, x_z.y, x_z.w + 0.16, x_z.h, texte(q, a, b), size=9.5, line_spacing=1.3)
d.banner(s, *bas, "**Un point commun : elles apprennent toutes de vos données historiques.**", size=10.5)

d.save(sys.argv[1] if len(sys.argv) > 1 else "pedagogie.pptx")
