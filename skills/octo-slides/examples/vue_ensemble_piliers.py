"""Exemple de référence : slide « vue d'ensemble » (panneau why + 6 cartes de piliers).
Rendu attendu : assets/exemples/vue_ensemble_piliers.png.

    uv run --with python-pptx python examples/vue_ensemble_piliers.py out.pptx

Mise en page (references/mise_en_page.md) : deux zones de départ, le panneau à gauche et la grille à droite ; la
grille s'arrête en x = 9,2 pour laisser libre la pastille du numéro de page, et ses cellules donnent les cartes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from octo_slides import Deck, Frame  # noqa: E402

N = " "  # espace insécable avant « : ; ! ? % »

d = Deck()
s = d.slide("Partenariat OCTO × Anthropic",
            "Construire une **relation privilégiée** avec Anthropic, bien au-delà d'une expertise sur Claude, "
            "autour de **6 piliers**.", subtitle_size=12)

why = Frame(0.4, 1.15, 2.8, 4.15)
droite = Frame(3.4, 0.98, 5.8, 4.32)  # x → 9,2 : la pastille du numéro de page reste libre
intertitre, cartes = droite.top(0.3, gap=0.14)

d.why_panel(s, *why,
            "Faire d'OCTO un ==partenaire technique de référence== d'Anthropic en France, qui transforme l'IA "
            "agentique en solutions concrètes, robustes et déployées chez les clients.",
            intro=f"Une relation privilégiée qui nous permette{N}:",
            bullets=["**D'être au cœur des projets stratégiques**, sur des rôles d'architecture et d'ingénierie à "
                     "forte valeur ajoutée (FDE).",
                     "**De devenir un acteur de référence des compétences Anthropic**, en interne comme sur le "
                     "marché.",
                     "**De générer des opportunités business communes** entre Accenture, OCTO et Anthropic.",
                     f"**De nous rapprocher de la frontière technologique**{N}: vision et R&D d'Anthropic."],
            split=0.48)

d.text(s, intertitre.x - 0.08, intertitre.y, intertitre.w, intertitre.h, "**Les 6 piliers du partenariat**", size=12)

piliers = [
    ("Expertise & leadership", "avatar_loupe",
     "Positionner des OCTOs comme Anthropic Architects sur des projets stratégiques, portés par Accenture ou "
     "directement par OCTO.",
     "Accéder à des rôles structurants, influencer les décisions d'architecture et développer une expertise "
     "reconnue par Anthropic."),
    ("Formation & certification", "checklist_stylo",
     "Faire d'OCTO l'un des premiers acteurs français habilités à délivrer les formations officielles Anthropic.",
     "Une offre de formation reconnue par Anthropic, pour nos consultants et nos clients, et devenir un acteur clé "
     "de la montée en compétences du marché."),
    ("Go-to-market & delivery communs", "poignee_main",
     f"Structurer la collaboration Accenture, OCTO et Anthropic{N}: devenir le partenaire naturel quand ses "
     "clients ont besoin d'ingénieurs expérimentés pour passer en production.",
     "Opportunités apportées par Anthropic, revues de comptes communes, co-financements, renfort des équipes "
     "PSD / FDE."),
    ("Communauté & rayonnement", "collaboration_mains",
     f"Co-organiser des événements Anthropic{N}: meetups et hackathons pour la communauté tech, journées "
     "thématiques clients (Retail, Agentic Coding chez OCTO).",
     "Faire d'OCTO un point de rencontre privilégié entre l'écosystème Anthropic, les communautés techniques et les "
     "décideurs clients."),
    ("Vision & influence stratégique", "cerveau_ampoule",
     f"Comprendre la vision d'Anthropic sur l'IA agentique et ses implications pour les entreprises{N}: "
     "savoir déployer, mais aussi expliquer et accompagner l'adoption.",
     "Anticiper les transformations, nourrir notre conseil stratégique et partager avec nos clients des "
     "convictions éclairées."),
    ("R&D &\nco-innovation", "fusee",
     "Relier la R&D d'OCTO aux équipes produit et engineering d'Anthropic, pour une circulation des innovations "
     "dans les deux sens.",
     "Programmes de bêta-test, expérimentation de fonctionnalités en amont, feedback terrain et opportunités de "
     "co-développement."),
]
cellules = [c for rangee in cartes.grid(2, 3, gap=(0.18, 0.1)) for c in rangee]
for i, (zone, (title, picto, body, ambition)) in enumerate(zip(cellules, piliers)):
    d.pillar_card(s, *zone, f"{i + 1:02d}", title, body, ambition, picto=picto, split=0.6)

d.save(sys.argv[1] if len(sys.argv) > 1 else "vue_ensemble_piliers.pptx")
