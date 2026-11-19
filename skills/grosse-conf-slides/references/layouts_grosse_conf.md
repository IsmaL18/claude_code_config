# Layouts préformatés du template La Grosse Conf

Les layouts de `assets/template_grosse_conf.pptx` portent déjà le masque de la charte (sigle panda, `#LAGROSSECONF`, signature, mention légale verticale, numéro de page en rond) et les fenêtres web. **Les utiliser dès qu'un layout correspond**, plutôt que de redessiner : sur les slides de contenu, le style est dans les cadres du layout, pas dans des zones de texte stylées.

Aperçu de chaque layout : `assets/layouts-grosse-conf/<aperçu>.png` (placeholders étiquetés « [idx] »). En cas de doute, lire l'image avant de choisir. Régénérer après un changement de template : `tools/preview_layouts.py --grosse-conf`.

## Utilisation

```python
d = GrosseConfDeck()
d.layout("focus", {0: "Titre", 2: "Sous-titre", 1: "Message clé"})           # clé de LAYOUTS, ou nom complet
d.layout("63 - Titre, contenu et visuel à droite - cadre blanc", {0: "Titre", 1: "- Point"}, ["cerveau"])
```

- Les numéros « 51 - » sont partagés par plusieurs layouts : **le nom complet** (ou la clé) désigne un layout, pas le numéro.
- `texts` : `{idx: texte balisé}` ; le style du layout (taille, couleur, puces) est conservé ; un placeholder absent de `texts` est supprimé.
- `visuals` : un élément par placeholder image, dans l'ordre des idx : chemin d'une photo, ou nom d'un picto ou d'une illustration (`pictos_grosse_conf.md`, `illustrations_grosse_conf.md`). Sans visuel, l'emplacement est supprimé : jamais de cadre vide.
- Raccourcis : `cover(date, lieu)`, `thematic(titre, sous-titre, note)`, `speaker(nom, poste, photo)`, `chapter(titre, numéro, visual)`, `toc(items)`, `focus(titre, sous-titre, corps)`, `slide(titre, sous-titre)`, `blank()`.

## Index

| Aperçu | Nom complet | Clé | Quand l'utiliser | Placeholders | Visuels |
|---|---|---|---|---|---|
| `51-Couverture` | 51 - Couverture | `cover` | Première slide : logo « la grosse conf. », illustration en fenêtre, éléments codés ; fond rose pâle | aucun (date et lieu : `cover()`) | — |
| `51-Couverture_1` | 51 - Couverture_1 | `cover_2` | Couverture sur image de fond du template | aucun | — |
| `51-Slide_THEMATIQUE` | 51 - Slide THEMATIQUE | `thematic` | Ouverture d'une session ou d'un thème : grande fenêtre de titre, petite fenêtre de note | 0 titre, 1 sous-titre, 2 note | — |
| `51-Slide_SPEAKER` | 51 - Slide SPEAKER | `speaker` | Présenter un·e speaker : nom, poste et entreprise, photo ronde | 0 nom, 1 poste | 2 : photo ronde |
| `51-Chapitre_PICTOS` | 51 - Chapitre PICTOS | `chapter_pictos` | Intercalaire avec illustration ou picto à gauche | 0 titre, 1 numéro | posé par `chapter(visual=)` |
| `51-Chapitre_TEXTE` | 51 - Chapitre TEXTE | `chapter_text` | Intercalaire sans visuel : fenêtre avec onglet « 01 » | 0 titre, 1 numéro | — |
| `51-Chapitre_PHOTO` | 51 - Chapitre PHOTO | `chapter_photo` | Intercalaire avec photo | 0 titre, 1 numéro | 2 : photo |
| `51-Photo_texte` | 51 - Photo + texte | `photo_text` | Texte à gauche en fenêtre, photo ou visuel à droite | 0 titre, 1 corps | 2 : photo |
| `51-Focus` | 51 - Focus | `focus` | Message clé, « pourquoi », synthèse : grand cadre rose plein | 0 titre, 2 sous-titre, 1 corps | — |
| `01-Titre_sous-titre_et_contenu` | 01 - Titre, sous-titre et contenu | `title_sub_content` | **Slide de contenu standard** : titre, sous-titre, zone libre `CONTENT` pour les helpers | 0 titre, 2 sous-titre, 1 corps | — |
| `02-Titre_et_contenu` | 02 - Titre et contenu | `title_content` | Contenu sans sous-titre | 0 titre, 1 corps | — |
| `03-Titre_et_sous-titre` | 03 - Titre et sous-titre | `title_sub` | Comme 01 sans corps : schéma, liste ou tableau dessiné dessous (modèles 24 à 36) | 0 titre, 1 sous-titre | — |
| `04-Titre_seul` | 04 - Titre seul | `title_only` | Schéma ou visuel pleine page sous un titre | 0 titre | — |
| `06-Slide_vide` | 06 - Slide vide | `blank` | Slide entièrement dessinée (masque seul) | aucun | — |
| `60-Titre_et_visuel` | 60 - Titre et visuel | — | Titre et grand visuel | 0 titre | 2 : visuel |
| `60-Titre_et_visuel_1` | 60 - Titre et visuel_1 | `title_visual` | Variante avec sous-titre | 0 titre, 1 sous-titre | 2 : visuel |
| `63-Titre_contenu_et_visuel_à_droite-cadre_blanc` | 63 - Titre, contenu et visuel à droite - cadre blanc | `visual_right` | Texte à gauche, fenêtre de visuel à droite | 0 titre, 2 sous-titre, 1 corps | 3 : visuel |
| `69-Titre_contenu_visuel_à_gauche_et_bloc_conclu-cadre_blanc` | 69 - Titre, contenu, visuel à gauche et bloc conclu - cadre blanc | `visual_left` | Visuel à gauche, texte à droite, bloc de conclusion | 0 titre, 1 corps | 2 : visuel |
| `CUSTOM` | CUSTOM | — | Deux colonnes titrées (deux blocs de texte) | 0 et 3 titres, 1 et 2 corps | — |
| `CUSTOM_1` | CUSTOM_1 | — | Cinq titres autour d'un visuel | 0, 3, 4, 5, 6 titres | 2 : visuel |
| `90-Table_des_matières_2` | 90 - Table des matières [2] | `toc` | Sommaire de 2 entrées, pastilles « 01 » | 0 titre, 1 et 2 entrées | — |
| `91-Table_des_matières_3` | 91 - Table des matières [3] | `toc` | 3 entrées en colonnes | 0 titre, 1 à 3 | — |
| `92-Table_des_matières_4` | 92 - Table des matières [4] | `toc` | 4 entrées | 0 titre, 1 à 4 | — |
| `94-Table_des_matières_5` | 94 - Table des matières [5] | `toc` | 5 entrées sur 2 colonnes | 0 titre, 1 à 5 | — |
| `94-Table_des_matières_6` | 94 - Table des matières [6] | `toc` | 6 entrées sur 2 colonnes | 0 titre, 1 à 6 | — |
| `94-Table_des_matières_6__1` | 94 - Table des matières [6]_1 | — | Variante à 5 entrées (3 + 2) | 0 titre, 1 à 5 | — |
| `95-Table_des_matières_7` | 95 - Table des matières [7] | `toc` | 7 entrées | 0 titre, 1 à 7 | — |
| `96-Table_des_matières_8` | 96 - Table des matières [8] | `toc` | 8 entrées | 0 titre, 1 à 8 | — |
| `97-Table_des_matières_9` | 97 - Table des matières [9] | `toc` | 9 entrées | 0 titre, 1 à 9 | — |
| `98-Table_des_matières_10` | 98 - Table des matières [10] | `toc` | 10 entrées (la 10e est l'idx 13) | 0 titre, 1 à 9 et 13 | — |
| `99-Table_des_matières_all` | 99 - Table des matières [all] | — | Sommaire long : entrées à gauche, numéros de page à droite | 0 titre, 1 entrées, 2 numéros | — |

## Remarques

- Les idx des placeholders ne suivent pas l'ordre visuel des sommaires : `toc()` range les entrées colonne par colonne, de haut en bas.
- Les couvertures et slides de rupture sont sur fond rose pâle `#FFEDF2` (pied « LA CONF DATA I IA BY OCTO TECHNOLOGY ») ; les slides de contenu sont sur fond blanc (mention légale verticale à gauche).
- Les layouts ne doivent pas être enchaînés à l'identique pour des slides de même rang : voir `style_grosse_conf.md`.
