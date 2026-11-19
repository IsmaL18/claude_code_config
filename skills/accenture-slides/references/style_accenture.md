# Construire une slide Accenture

Comment composer les slides avec `AccentureDeck`, dans la charte (`charte_accenture.md`, qui prime). Slide de
13,333 x 7,5 pouces ; zone de contenu `CONTENT` (sous le titre et son sous-titre, au-dessus du pied de page).

## 1. Une slide, un message

- Le titre est le message, en phrase, sur une ligne : « Trois étapes pour passer à l'échelle », pas « Approche ».
- Un sous-titre facultatif (`slide(titre, sous_titre)`, Palatino violet) dit la chute ou le contexte.
- Une slide projetée porte 20 mots ou moins hors titre ; le reste va dans les notes.
- Au moins une slide sur deux porte un visuel : processus, chiffres, cartes à icône, schéma de la bibliothèque. Jamais
  une slide réduite à des puces.

## 2. Rythme du deck

Couverture (`cover`), agenda (`agenda`), puis des parties ouvertes par un intercalaire numéroté (`section`) ; un message
clé (`key_message`) pour une conclusion de partie ; slide de fin (`closing`). Varier les styles d'intercalaire (dark,
mid, core) d'une partie à l'autre, et alterner fond blanc et fond foncé (`slide(dark=True)`) avec mesure : le blanc
reste la base.

## 3. Composants

| Besoin | Composant | Rendu |
|---|---|---|
| Un processus, des étapes ordonnées | `etapes(slide, zone, [(intitulé, texte)], focal=k)` | chevrons gris clair, l'étape focale en violet, un texte sous chacun |
| Avant / après, problème / résultat | `de_a(slide, zone, avant, apres)` | panneau gris clair, grand « > », panneau violet foncé |
| Deux à quatre chiffres clés | `chiffres(slide, zone, [(valeur, libellé)])` | rangée centrée dans la zone ; `chiffre()` pour un seul |
| Des valeurs à comparer (3 à 8) | `barres(slide, zone, [(libellé, valeur)], focal=k, unit=" j")` | barres dessinées gris clair, la focale en violet, valeur au bout |
| Un tableau (rôles, comparaison) | `tableau(slide, zone, lignes, widths=[…])` | en-tête violet foncé, lignes alternées blanc et gris clair, `**gras**` dans les cellules |
| Un choix selon deux critères | `matrice(slide, zone, axe_x, axe_y, [4 cases], focal=k)` | 2 x 2 gris clair, la case focale en violet, axes gradués |
| Des idées parallèles avec une icône | `carte(slide, x, y, w, h, icône, intitulé, texte)` | icône monoline, filet violet, intitulé gras |
| Des principes, des règles numérotées | `point(slide, x, y, w, None, n, intitulé, texte)` | case « 1. » au cadre gris clair (comme le starter pack) |
| Deux à cinq colonnes égales | `colonnes(slide, zone, [(intitulé, texte)])` | numéro violet, intitulé Arial Black, filet violet |
| Une citation | `citation(slide, x, y, w, h, texte, auteur)` | texte Arial Black, filet violet, auteur en Palatino |
| Un bloc plein | `aplat(slide, x, y, w, h, texte, fill=PURPLE)` | angles droits ; texte blanc sur violet foncé, noir sur clair |
| La signature | `gt(slide, x, y, h)` | le « > » plein, une fois par slide au plus |
| Un intitulé, une accroche | `headline(...)`, `serif(...)` | Arial Black ; Palatino violet |

Les zones se découpent (`CONTENT.cols`, `rows`, `grid`, `place`, `pad`), jamais de coordonnées tapées à la main ; les
blocs d'une rangée ont la même hauteur. Relier deux formes avec `connect` (flèches violettes), plusieurs avec `fork` ou
`join`.

## 4. La bibliothèque de visuels avant le dessin

Pour un graphique (barres, colonnes, secteurs, cascade, radar), un schéma de concepts (équilibre, forces, causes,
barrières), un processus (flux linéaires, circulaires, « issue to outcome »), une matrice, une pyramide, un arbre, une
carte, un Gantt, un tableau de bord de programme, une matrice valeur / effort ou un cadre d'analyse (Porter, 2x2),
partir d'un des 388 modèles (`modeles_accenture.md`) plutôt que de le redessiner.

## 5. Ce qu'on ne fait pas

- Un dégradé dessiné, une ombre portée, une forme aux coins arrondis : la marque est à angles droits et à aplats.
- Plus d'un violet fort par slide ; du lilas ou du gris clair en petit texte.
- Une icône d'une autre bibliothèque, une icône dessinée à la main, une photo à découpe ronde.
- Un titre sur deux lignes, en capitales, avec un point final.
- Des puces seules sur une slide projetée.
- Un élément sous y = 7,0 pouces (pied de page de la marque).

## 6. Mise en page contrôlée à l'enregistrement

`save()` signale : texte qui déborde, blocs mal alignés ou qui se chevauchent, bloc à moitié vide, mot seul en fin de
paragraphe, élément hors des marges ou sur le pied de page, contraste insuffisant, flèches sans tige. Corriger chaque
alerte avant le rendu ; `target="gslides"` ajoute ce que Google Slides ne rend pas.
