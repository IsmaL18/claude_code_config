"""Exemple de référence « vue d'ensemble en blocs emboîtés » : un panneau « why », trois freins et la réponse à
chacun, un bandeau de soutiens et d'attentes. Tiré d'une demande réelle (noms remplacés par des rôles).
Rendu attendu : assets/exemples/freins_leviers.png.

    uv run --with python-pptx python examples/freins_leviers.py out.pptx

Ce qui fait la slide : le pourquoi en panneau marine (point focal, seul aplat marine) ; à droite, trois rangées
frein > levier de même hauteur, sur les mêmes colonnes que leurs intertitres, le passage de l'un à l'autre marqué
par un chevron turquoise plutôt qu'une flèche ; en bas, trois blocs emboîtés (bords partagés, coins arrondis qui
varient), l'appel à décision en turquoise plein.

Mise en page (references/mise_en_page.md) : deux zones de départ, tout le reste découpé ; les largeurs de colonnes
viennent de la mesure des titres (text_width), et le texte a été raccourci jusqu'à zéro alerte.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from octo_slides import TURQ, TURQ_20, Deck, Frame  # noqa: E402

N = " "  # espace insécable avant « : ; ! ? % »

d = Deck()
s = d.slide("Un agent analytics pour tous les OCTOs",
            "Trois freins identifiés avec la DSI, **deux chantiers** que nous portons **sans charger les équipes "
            "internes**.", subtitle_size=13)

why = Frame(0.4, 1.3, 3.1, 4.0)
right = Frame(3.75, 1.3, 5.45, 3.9)  # bord droit en 9,2 : la pastille du numéro de page reste libre

d.why_panel(s, *why,
            f"Permettre à ==tous les OCTOs== d'analyser les données internes ==en langage naturel==, en toute "
            "autonomie.",
            intro=f"Pourquoi maintenant{N}:",
            bullets=[f"**Rendre OCTO data-driven**{N}: chaque réponse sans file d'attente, chaque chiffre avec sa "
                     "provenance.",
                     f"**Une pratique qui a fait ses preuves**{N}: chez Stripe, 83{N}% des employés utilisent "
                     "l'agent chaque semaine.",
                     f"**Décharger les équipes**{N}: chez Grab, l'agent prend 40{N}% du temps de l'équipe data.",
                     f"**Éprouver notre offre chez nous**{N}, avant de la porter sur le marché en 2027."],
            split=0.42, size=11, bullet_size=7.5)

cols = [2.05, 0.25, None]  # frein | chevron | levier : mêmes colonnes pour les intertitres et les rangées
head, rest = right.top(0.25, gap=0.1)
body, bottom = rest.bottom_band(0.95, gap=0.14)
for zone, title in zip(head.cols(cols, gap=0)[::2], ["Les freins", "Nos leviers"]):
    d.text(s, zone.x - 0.08, zone.y - 0.04, zone.w, None, f"**{title}**", size=11, line_spacing=1.0)

freins = [("Court terme", "Pas d'environnement de recette",
           "Aucune recette du datawarehouse avec des données désensibilisées."),
          ("Moyen terme", "Des droits portés par Metabase",
           "Seul Metabase ouvre la production ; l'accès direct est demandé."),
          ("Transverse", "Des équipes data surbookées",
           "En sous-effectif, elles n'absorbent pas de nouveaux besoins.")]
leviers = [("data-storage", "Un outil d'anonymisation, opéré par la DSI",
            "Dans vos standards, aveugle sur la production ; il produit le snapshot et sert vos développements."),
           ("cadenas-close", "Les habilitations répliquées dans PostgreSQL",
            "En Terraform : l'agent requête avec les droits de chaque utilisateur."),
           ("poignee_main", "L'effort porté par les ateliers OCTO",
            f"Data & AI et Cloud & Platform construisent{N}; vos équipes valident et opèrent.")]
for (frein_zone, chevron_zone, levier_zone), (tag, lead, text), (picto, lead2, text2) in zip(
        body.grid(3, cols, gap=(0.1, 0)), freins, leviers):
    d.bloc(s, *frein_zone, corners="tl", radius=0.3, title=lead, body=text, title_size=8, size=7, pad=0.13)
    d.label(s, frein_zone.x + 0.3, frein_zone.y - 0.09, tag, h=0.18, size=6.5)
    d.chevron(s, chevron_zone.cx + 0.05, chevron_zone.cy, size=0.2)
    d.bloc(s, *levier_zone, corners="br", radius=0.3, fill=TURQ_20, title=lead2, body=text2, picto=picto,
           picto_size=0.32, title_size=8, size=7, pad=0.13)

usages, soutiens, attentes = bottom.cols([1.4, None, 2.1], gap=0)
d.bloc(s, *usages, corners="bl", radius=0.35, title="Cas d'usage",
       body="> [à compléter]\n> [à compléter]\n> [à compléter]", title_size=8, size=7, pad=0.13)
d.bloc(s, *soutiens, corners="none", title="Nos soutiens",
       body="**[lead de la Fabrique OCTO]**, **[porteur]**, **[PM produits internes]**, "
            "**[deux encadrant(e)s]** du stage.",
       title_size=8, size=7, pad=0.13)
d.bloc(s, *attentes, corners="tr", radius=0.35, fill=TURQ, title="Nos attentes envers la DSI",
       body="- Votre feu vert aux deux chantiers\n- Un référent par chantier\n- L'exploitation de l'outil",
       title_size=8, size=7, pad=0.13)

d.save(sys.argv[1] if len(sys.argv) > 1 else "agent_analytics_apres.pptx")
