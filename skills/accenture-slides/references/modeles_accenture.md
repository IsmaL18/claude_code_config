# Partir d'un visuel de la bibliothèque Accenture, puis l'adapter

`assets/modeles_accenture.pptx` contient les 388 slides de la bibliothèque de visuels du starter pack Accenture
(« Visuals Library », de la slide 61 à la fin ; `tools/build_accenture.py` en retire le kit de démarrage, le mode
d'emploi des graphiques et les boutons « maison » qui renvoyaient à l'index). Index : `modeles_index_accenture.md` ;
miniatures : `assets/modeles-accenture/planche_NN.png` (12 par planche, planche = (n - 1) // 12 + 1).

**Deux usages, par ordre de préférence :**
1. **Structure à transformer** : copier le visuel (`d.modele(n)` avec `ModeleAccentureDeck`,
   `scripts/accenture_modeles.py`) quand sa structure colle au besoin, puis l'adapter : `show(n)` pour lire ses
   formes, `set_text`, `set_cell`, `remove`, `duplicate`, `move`, `recolor`, `check`.
2. **Réservoir de formes** : poser un élément d'un visuel dans sa propre slide avec
   `d.borrow(slide, n, "<chemin>", x, y, w)` (une carte du monde, une pyramide, une flèche de processus).

Au build, la bibliothèque est ramenée à la charte autant que possible : gris et violets hors palette passés à la
couleur de la palette la plus proche, puces en police de symboles remplacées par « • » en Arial. Restent les couleurs
de série de certains graphiques et notations (bleu, orange, rouge) : `check()` les signale, `recolor()` les corrige.

Outils d'adaptation : `keep(slide, "1", "4", …)` ne garde que les formes utiles (plus court que `remove` sur un modèle
chargé) ; `set_text(slide, chemin, texte, fit=True)` élargit l'étiquette à son texte (libellé traduit, plus long
que « Low » ou « Label »). Avant d'adapter une matrice 2 x 2 ou une rangée de chiffres, préférer les recettes
`matrice()` et `chiffres()` d'`AccentureDeck`.

**Un visuel n'est jamais un formulaire à remplir** : on garde sa structure, on l'adapte au contenu, dans la charte
(`charte_accenture.md`). Les textes de gabarit (« Text », « TEXT », « Insert text here », « Body copy », « Label A »,
« Option 1 ») sont remplacés ou les formes retirées : `check()` les signale. Les consignes (« Hints: »,
« Instructions: », « Ungroup map… ») sont retirées à la copie. Les intercalaires de partie de la bibliothèque sont
dans le deck (pour l'index) : ne pas les copier, utiliser `section()`.

## Parties de la bibliothèque

| Partie | Ce qu'on y trouve |
|---|---|
| Charts | barres horizontales (écart, plage, 100 %), colonnes (groupées, cascades, combinées), secteurs et anneaux, courbes, radars, portefeuilles en 2 et 3 dimensions |
| Dynamic Concepts | équilibre et déséquilibre, interaction et feedback, séparation et synthèse, causes, conflits, barrières et résistances, forces et influences |
| Processes | flux linéaires (chevrons, étapes, pipelines, croissance), « issue to outcome » (du problème au résultat, propositions de valeur), flux circulaires et itératifs |
| Static Objects | cercles (entrelacés, segments, illustrations), arbres (arbres de problèmes, cartographies), boîtes (facteurs, composants, cubes), objets de texte (conséquences, citations de presse, matrices, pyramides, frises de temps, piliers), autres structures |
| Standard Visuals | cartes (monde, continents), gestion de projet (Gantt, tableau de bord de programme, modèle de maturité, fiche de définition de problème, matrices valeur / effort), équipes (profil, organisation), évaluation (notation, avant / après, matrice 2x2), graphes illustratifs et cadres (Porter), objets utiles (légendes, puzzles) |
| Fin | mentions de confidentialité d'une proposition et d'une présentation |

**Les graphiques de la bibliothèque sont des images** (l'export du starter pack les a aplatis) : leurs données ne se
modifient pas. Ils servent d'inspiration ; pour un vrai graphique, `barres()` ou `tableau()` d'`AccentureDeck`.

Défauts connus du starter pack, à corriger à l'adaptation : des formes sans contour ni fond (les cercles de
« Interlocking Circles 2 » : `recolor(slide, chemin, line=GREY)`), des libellés lilas pâle illisibles sur blanc
(`set_text(..., color=BLACK)`), des pointes de pyramide trop étroites pour un mot long. Le contrôle de mise en page
(contraste, mots coupés) descend dans les groupes des modèles une fois leur texte réécrit.
