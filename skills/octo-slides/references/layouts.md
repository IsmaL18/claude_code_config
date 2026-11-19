# Layouts préformatés du template OCTO

Les slides de `assets/template_octo.pptx` portent déjà la charte : formes signature, gouttes, pastilles, fonds. **Les utiliser dès qu'un layout correspond au besoin**, plutôt que de tout redessiner avec les helpers. Les helpers servent à composer le contenu d'une slide de contenu (01) ou à poser des blocs dans la zone libre d'un layout.

Aperçu de chaque layout : `assets/layouts/<numéro>.png` (placeholders étiquetés « [idx] », emplacements photo visibles). En cas de doute, lire l'image avant de choisir. Régénérer après un changement de template : `tools/preview_layouts.py`.

## Utilisation

```python
d.layout("65", {0: "Titre", 1: "- **Point.** Texte", 2: "**Conclusion** du bloc"}, ["fusee"])
```

- `texts` : `{idx: texte}`. Le style du layout est conservé (taille, couleur, puces) ; seul le markup `**gras**` est appliqué. Un placeholder absent de `texts` est supprimé.
- `visuals` : un élément par emplacement photo, dans l'ordre de la colonne « Emplacements ». Chemin d'une photo (recadrée dans la forme), ou nom d'un picto, avatar ou illustration (posé sur une goutte turquoise pâle `#C6F1F5`, comme le prévoit la charte sans photo). Un emplacement non fourni est couvert d'un aplat turquoise pâle : le texte rouge « ici mettre une photo » du gabarit n'apparaît jamais.
- Photos : seulement celles du catalogue OCTO (Drive) ou fournies par l'utilisateur. Sinon, une illustration de `references/illustrations.md` ou un picto.

Raccourcis : `cover(..., variant=1|2)`, `chapter(title, number, visual, variant=1|2)`, `focus(title, subtitle, body)`, `toc(items, title)`, `closing()`, `slide(title, subtitle)` (layout 01), `blank()` (layout 06).

## Index

| N° | Nom | Quand l'utiliser | Placeholders | Emplacements photo | Helper |
|---|---|---|---|---|---|
| 40 | Couverture [1] | Première slide, avec la photo d'équipe du gabarit (photo OCTO générique, voile bleu). | 0 titre, 1 sous-titre, 2 date « jj.mm.aa », 3 entité / tribu | — | `cover(variant=1)` |
| 41 | Couverture [2] | Première slide sans photo : aplat marine, pilule à contour blanc. **Par défaut** si la photo de la 40 est hors sujet. | idem 40 | — | `cover(variant=2)` |
| 90 à 98 | Table des matières [2] à [10] | Sommaire ou vue d'ensemble de 2 à 10 parties, piliers, thèmes : pastilles goutte « 01 »… natives. 90 : 2 entrées côte à côte ; 91 : 3 en colonnes ; 92 à 98 : 2 colonnes. | 0 titre, 1…9 entrées (la 10e entrée du 98 est l'idx 13) | — | `toc(items, title)` |
| 99 | Table des matières [all] | Sommaire long : entrées à gauche, numéros de page à droite. | 0 titre, 1 entrées (une par ligne), 2 numéros de page | — | `layout("99", …)` |
| 50 | Chapitre [1] | Intercalaire de partie : goutte ronde à gauche, onglet sigle | numéro, titre à droite. | 0 titre, 1 numéro (« 01 ») | 1 : goutte ronde (2,8 x 2,8) | `chapter(variant=1)` |
| 51 | Chapitre [2] | Intercalaire, variante goutte carrée haute à gauche. | 0 titre, 1 numéro | 1 : goutte carrée (4,0 x 4,6) | `chapter(variant=2)` |
| 05 | Focus | Message clé, « pourquoi », synthèse : grand cadre blanc sur fond `#3E4F78`. Le corps (idx 2) est centré verticalement : pour du contenu dessiné, laisser le corps vide et poser les helpers dans le cadre (x 0,6 → 9,3 ; y 1,3 → 5,0). | 0 titre, 1 sous-titre, 2 corps | — | `focus()` |
| 01 | Titre, sous-titre et contenu | **Slide de contenu standard** (titre-message + sous-titre-chute), zone libre pour les helpers. | 0 titre, 2 sous-titre, 1 corps | — | `slide()` |
| 02 | Titre et contenu | Contenu sans sous-titre, corps à puces pleine largeur. | 0 titre, 1 corps | — | `layout("02", …)` |
| 03 | Titre et sous-titre | Comme 01 sans corps. Doublon : « 03 - Titre et sous-titre_1 ». | 0 titre, 1 sous-titre | — | `layout("03", …)` |
| 04 | Titre seul | Schéma ou visuel pleine page sous un titre. | 0 titre | — | `layout("04", …)` |
| 06 | Slide vide | Slide entièrement dessinée (sigle, mentions et numéro gardés). | — | — | `blank()` |
| 63 | Titre, contenu et visuel à droite | Texte à gauche (5,8 de large), grande goutte photo à droite. | 0 titre, 1 corps | 1 : goutte coins opposés (2,8 x 4,1), droite | `layout("63", …)` |
| 64 | Titre, sous-titre, contenu et visuel à droite | Idem 63 avec sous-titre. | 0 titre, 2 sous-titre, 1 corps | 1 : idem 63 | `layout("64", …)` |
| 65 | Titre, contenu, visuel à droite et bloc conclu | Texte à gauche ; à droite, une goutte à contour qui porte la conclusion, et une petite goutte photo en dessous. | 0 titre, 1 corps, 2 bloc conclu | 1 : petite goutte (1,5 x 1,5), bas droite | `layout("65", …)` |
| 66 | Titre, sous-titre, contenu, visuel à droite et bloc conclu | Idem 65 avec sous-titre. | 0 titre, 2 sous-titre, 1 corps, 3 bloc conclu | 1 : idem 65 | `layout("66", …)` |
| 67 | Titre, contenu et visuel à gauche | Miroir de 63 : goutte photo à gauche, texte à droite. | 0 titre, 1 corps | 1 : goutte coins opposés (2,8 x 4,1), gauche | `layout("67", …)` |
| 68 | Titre, sous-titre, contenu et visuel à gauche | Idem 67 avec sous-titre. | 0 titre, 1 sous-titre, 2 corps | 1 : idem 67 | `layout("68", …)` |
| 69 | Titre, contenu, visuel à gauche et bloc conclu | Miroir de 65 : bloc conclu et petite goutte à gauche. | 0 titre, 1 bloc conclu, 2 corps | 1 : petite goutte (1,5 x 1,5), bas gauche | `layout("69", …)` |
| 70 | Titre, sous-titre, contenu, visuel à gauche et bloc conclu | Idem 69 avec sous-titre. | 0 titre, 2 sous-titre, 1 corps, 3 bloc conclu | 1 : idem 69 | `layout("70", …)` |
| 59 | There is a better way | Clôture : emblème au trait + « There is a better way. ». | — | — | `closing()` |

**À ne jamais utiliser** (marqués « Ne pas utiliser, merci de changer de mise en page » dans le template, `layout()` refuse) : 07 (slide vide fond foncé), 60 (titre et visuel), 61 (titre, sous-titre et visuel), 62 (visuel seul).

## Remarques

- Les numéros d'idx ne suivent pas toujours l'ordre visuel (64 : sous-titre = 2, corps = 1 ; 69 : bloc conclu = 1, corps = 2). Se fier à la colonne « Placeholders ».
- Bloc conclu (65, 66, 69, 70) : une phrase courte en gras, 3 lignes au plus ; dans 65 et 69 le placeholder a une puce, ne pas en ajouter.
- Corps des layouts 63 à 70 : 3 à 5 puces courtes, centrées verticalement par le layout.
- Après un layout préformaté, varier : un deck ne doit pas enchaîner plusieurs fois le même layout pour des slides de même rang (voir `style.md`).
