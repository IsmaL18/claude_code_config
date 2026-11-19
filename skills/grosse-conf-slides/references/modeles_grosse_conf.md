# Partir d'un modèle La Grosse Conf, puis l'adapter

`assets/modeles_grosse_conf.pptx` contient 39 slides préformatées de l'édition 2025 de La Grosse Conf (le deck source en compte 48 ; `tools/build_modeles.py --grosse-conf` en retire les couleurs et règles de contraste (3 et 4, texte OCTO et photos bleues), les banques de pictos et d'illustrations, le tutoriel de recoloration et les pictos du Drive). Index : `modeles_index_grosse_conf.md` ; miniatures : `assets/modeles-grosse-conf/planche_NN.png` (12 par planche).

**Deux usages, par ordre de préférence :**
1. **Structure à transformer** : copier le modèle (`d.modele(n)` avec `ModeleGrosseConfDeck`, `scripts/grosse_conf_modeles.py`) quand sa structure colle au besoin (pyramide, entonnoir, cible, Venn, jauges, listes, tableaux), puis l'adapter : `set_text`, `remove`, `duplicate`, `recolor`, `check`. Les noms et paramètres sont ceux d'`octo_modeles.ModeleDeck`.
2. **Réservoir de formes** : poser un élément d'un modèle dans sa propre slide avec `d.borrow(slide, n, "<chemin>", x, y, w)` (trackers, flèches, guillemets, avatars des modèles 3 à 5).

**Un modèle n'est jamais un formulaire à remplir** : on garde sa structure et ses formes signature, on l'adapte au contenu, toujours dans la charte (`charte_grosse_conf.md`). Les textes « Lorem ipsum », « xxx », « Puce 1 » sont remplacés (`check()` les signale) ; les photos des modèles (échelle bleue, visuel 3D, portraits) sont hors charte grosse conf : les retirer ou les remplacer par un picto ou une illustration.

## Trouver un modèle par sa forme

| Forme | Modèles | Notes |
|---|---|---|
| Éléments graphiques : trackers à numéros, formes, guillemets, tête d'Octo, avatars « Octos » et « Clients » | 3 | à emprunter avec `borrow` |
| Séparateurs, filets, bulles de texte en fenêtre (avec onglet) | 4 | |
| Flèches : droites, doubles, creuses, courbes, anthracite et rouge | 5 | `arrow()` reproduit la flèche pleine |
| Intercalaires de chapitre : texte, illustration, picto, photo | 6 à 10 | `chapter()` ; layouts « 51 - Chapitre … » |
| Slide thématique, speaker, focus | 1, 2, 22 | `thematic()`, `speaker()`, `focus()` |
| Texte et visuel : photo + texte, visuel à droite ou à gauche, titre et visuel | 11 à 18 | layouts 51 - Photo + texte, 63, 69, 60 |
| Jauge circulaire et texte | 15, 25 | pourcentages : 10 à 100 % en anneaux |
| Citation avec auteur et photo | 20 | `citation()` |
| Démo, visuel 3D | 21 | |
| Démarche en 3 étapes avec pictos | 24 | |
| Pyramide à 4 niveaux (descentes du rouge) | 26 | |
| Entonnoir à 5 niveaux | 27 | |
| Flèches radiales autour d'un cercle central | 28 | |
| Cible concentrique (pourquoi, comment, quoi) | 29 | |
| Diagramme de Venn à trois cercles | 30 | |
| Listes : cartes empilées, étapes numérotées « 01. » à flèche, grilles de puces à onglet, onglets décalés avec picto | 32 à 36 | |
| Tableaux | 38, 39 | `set_cell` |
| Intercalaires d'exemples (rubriques « schémas », « listes », « tableaux ») | 23, 31, 37 | à ne pas reprendre dans un livrable |

## Ce qu'il faut savoir

- Les modèles de la rubrique « Exemples de chapitres » (11 à 22) sont des slides types avec leur visuel : leur layout est celui du template (`layouts_grosse_conf.md`).
- Les modèles des rubriques de schémas et de listes sont **à plat** (cercles, flèches, aplats rouge, rose, anthracite) : ils n'ont pas de fenêtre web ; la fenêtre sert aux slides de texte et de rupture.
- Pas d'`asset()` : il n'existe pas de visuels de modèles à part pour grosse conf ; les visuels sont les pictos et illustrations de `assets/` (`picto="<nom>"`, `replace_picture`).
