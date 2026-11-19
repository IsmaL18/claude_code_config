# Style des slides La Grosse Conf

Ce fichier dit comment construire les slides grosse conf avec `GrosseConfDeck` (`scripts/grosse_conf_slides.py`). Les couleurs, la typographie, l'accessibilité et le masque sont dans `charte_grosse_conf.md`, **qui prime**. Il ne reprend ni `style.md` ni `charte.md` : le style OCTO (marine, turquoise, capsules, gouttes, style filaire) ne s'applique pas ici.
Ce qui est dit ici vient de la charte, du template et du deck de slides préformatées ; ce qu'ils ne disent pas (ton, densité du texte) est marqué **retenu** : à valider avec le premier deck livré.

## 1. Esprit et ton

- « Franc-tireur » : un décalage visuel qui met en lumière l'innovation, sans faire comme tout le monde (charte). Les exemples du deck : titres courts, nominaux ou en question, à point rouge (« Les couleurs. », « Mise en forme d'un texte. », « Pourquoi ? »).
- **Retenu** : une idée par slide, une phrase de titre courte (≤ 50 caractères), pas de paragraphe de plus de 3 lignes ; un lead en gras suivi d'une explication courte dans une fenêtre ; le français soigné de `charte_grosse_conf.md` (espaces insécables, pas de point médian), en bas de casse.
- La couleur sert le point focal : un seul aplat rouge fort par slide (un chiffre, un cœur de schéma), le reste au trait anthracite sur blanc ou rose pâle.

## 2. Composition

- **Les slides de texte et de rupture vivent dans des fenêtres web** (`fenetre()` renvoie la zone intérieure). Des fenêtres de tailles et de formes adaptées au contenu, qui peuvent se chevaucher (une petite sur une grande, comme la couverture) ; une ombre rouge sur la fenêtre principale seulement.
- **Les schémas sont à plat** : cercles, flèches, anneaux, aplats rouge, descentes du rouge, anthracite (modèles 24 à 30). Pas de fenêtre autour d'un schéma.
- Zone de contenu : `CONTENT` (x 0,62 → 9,17, y 1,4 → 5,0) ; ne rien poser dans les marges du masque (x < 0,5, numéro de page en bas à droite). Découper la zone avec `CONTENT.cols`, `rows`, `grid` (`octo_layout.Frame`), jamais de coordonnées à la main.
- Hiérarchie par l'échelle : trois tailles au plus, le point focal au moins deux fois plus gros que le texte courant ; pas de texte courant sous 9 pt.
- Rythme : alterner slides de rupture (fond rose pâle : couverture, thématique, chapitre, speaker, focus) et slides de contenu (fond blanc) ; ne pas enchaîner deux fois le même layout pour des slides de même rang.

## 3. Recettes de schémas : un deck vivant, pas des puces

**Par défaut, une slide grosse conf n'est ni une liste, ni un paragraphe** : elle dessine son idée et la porte avec un picto de la conf. Se poser, pour chaque slide, deux questions (test du schéma : des relations qu'on peut nommer, des flèches qui disent quelque chose, un dessin lisible sans légende ; sinon il serait décoratif) :

1. **Y a-t-il un mécanisme ?** Des éléments reliés, un ordre, une inclusion, une boucle, un entourage : alors la slide est un schéma, avec la recette ci-dessous. Des éléments sans lien entre eux : une `grille` de fenêtres, sans flèche. Une grandeur : `chiffre`. Une idée seule : `focus` ou `equation`.
2. **Quel picto porte chaque idée ?** Un picto de `pictos_grosse_conf.md` par idée (chercher un mot-clé : `grep -i <mot> references/pictos_grosse_conf.md`), jamais nu au milieu d'un texte (dans une `carte` ou une `fenetre`), un fichier **une seule fois par deck** (sauf un motif voulu, comme « prise-jack » pour le harness). Une illustration (`illustrations_grosse_conf.md`) pour une rupture ou une idée forte, pas plus d'une par slide.

| La slide dit… | Recette | Helper (zone = `CONTENT` ou une de ses découpes) |
|---|---|---|
| une définition, « A = B + C » | équation de pictos | `equation(s, zone, [(picto, libellé), …])` |
| un niveau qui en contient un autre | cercles emboîtés (2 à 4) | `cible(s, zone, [libellés, du plus large au plus étroit])`, cartes de définition à côté |
| un ordre, des étapes, un retour | étapes en cartes et boucle rouge | `pipeline(s, zone, [(picto, titre, texte), …], focal=, retour="…")` |
| un élément et ce qui l'entoure | élément central relié à 2 x 3 cartes | `radial(s, zone, "Centre", gauche, droite)` |
| une boucle fermée | cycle en quatre cartes | `boucle(s, zone, [(picto, titre), …], focal=)` |
| des cas indépendants (échecs, critères) | grille de fenêtres à picto | `grille(s, zone, [(picto, titre, texte), …], cols=2)` |
| un chiffre | chiffre héros + cartes | `chiffre`, `carte` |
| un message clé | focus | `focus`, `statement` |

Règles de composition : un seul accent rouge fort par slide (l'ombre d'un point focal, un aplat) ; des flèches anthracite pour le flux, une flèche rouge pour la boucle de retour ; jamais deux slides de suite avec la même recette ; une slide sur deux au moins porte un schéma ou des cartes à picto. Exemple de référence : `examples/grosse_conf_schemas.py` (les six recettes) et `assets/exemples/grosse_conf_schemas.png`.

## 3 bis. Composants (helpers)

| Besoin | Helper | Notes |
|---|---|---|
| Fenêtre de texte, de visuel, de citation | `fenetre(s, x, y, w, h, title=, defilement=)` | renvoie `(x, y, w, h)` intérieur ; `text(s, *inner, …)` y pose le texte |
| Onglet « 01 » sur le bord d'une fenêtre | `onglet(s, x, y, "01")` | à cheval sur le bord haut |
| Pastille de sommaire ou de liste | `pastille(s, x, y, "01")` | |
| Étapes d'un tracker | `tracker_gc(s, x, y, w, 1, "Étape")` | `active=False` pour une étape à venir |
| Citation avec auteur | `citation(s, x, y, w, h, texte, auteur)` | |
| Chiffre clé | `chiffre(s, x, y, w, "75 %", "libellé")` | point final rouge |
| Carte avec picto | `carte(s, x, y, w, h, "livre", "Titre", "texte", vertical=, ombre=)` | picto à gauche, ou en haut avec `vertical=True` ; une ombre rouge au plus par slide ; renvoie la forme, à relier avec `connect` |
| Aplat de schéma | `aplat(s, x, y, w, h, texte, fill=RED)` | blanc sur rouge ≥ 18 pt ou gras 14 pt |
| Flèches | `arrow`, `connect`, `fork`, `join`, `loop_back` (hérités) | flux anthracite, boucle rouge |
| Picto, illustration, photo | `picto("<nom>", x, y, taille)`, `photo`, `photo_fit` | noms : `pictos_grosse_conf.md`, `illustrations_grosse_conf.md` |
| Titre à point rouge, phrase-message | `statement`, `chiffre`, `slide()` | |
| Rupture | `cover`, `thematic`, `speaker`, `chapter`, `toc`, `focus` | layouts du template |

`GrosseConfDeck` n'a que ces composants et les helpers communs (texte, flèches, images : `api_grosse_conf.md`) ; rien de la charte OCTO. Ce qui manque se trouve dans les modèles (`modeles_grosse_conf.md`) : pour un tableau, copier le modèle 38 ou 39.

## 4. Visuels

- Une illustration forte par slide au plus, jamais deux fois la même dans un deck ; en grande taille (couverture, chapitre, à côté du texte), dans sa fenêtre d'origine.
- Un picto n'est pas posé nu au milieu d'un texte : à gauche d'une bande, au-dessus d'une colonne, ou dans une fenêtre.
- Une photo : seulement celle que l'utilisateur fournit (speaker, partenaire), en noir et blanc de préférence, dans une fenêtre ou un cercle.
- Ne pas redessiner : pas de clipart hors `assets/`, pas d'emoji.

## 5. Plan de composition

Avant de générer un deck de 3 slides ou plus, écrire une ligne par slide (`spec_plan_grosse_conf.md`) : `n. Titre — focal : … — contraste : … — géométrie : …` ; la géométrie nomme la recette du §3 (« boucle en quatre cartes ») et les pictos choisis (« ecriture, livre, prise-jack »), puis vérifier que deux slides consécutives ne partagent pas plus d'un des trois. Le plan cite le layout ou le modèle de départ (`layouts_grosse_conf.md`, `modeles_index_grosse_conf.md`).

## 6. Ce qu'on ne fait pas

- Pas de bleu, de turquoise, de noir pur, de vert ; pas de rouge sur anthracite ni l'inverse.
- Pas de style OCTO (capsules, gouttes, onglets marine) ni de photos OCTO bleues.
- Pas de slide recréée à la main qui perdrait le masque : toujours un layout du template.
- Pas de texte de gabarit (« Lorem ipsum », « xxx », « Auteur.trice », « SLIDE À SUPPRIMER AVANT PRÉSENTATION »).
- Pas de capitales pour insister, pas d'italique, pas de point médian.
