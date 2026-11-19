# Layouts du template Accenture

Les layouts de `assets/template_accenture.pptx` (le starter pack de la marque, version aux polices système) portent
déjà le masque : le « > » en bas à gauche, le copyright et le numéro de page en bas à droite, les dégradés et les
photos des couvertures et des intercalaires. **Les utiliser dès qu'un layout correspond**, plutôt que de redessiner :
une couverture, un intercalaire ou un message clé recréés à la main perdent le masque et les dégradés.

Aperçu de chaque layout : `assets/layouts-accenture/<aperçu>.png` (placeholders étiquetés « [idx] »). En cas de doute,
lire l'image avant de choisir. Régénérer après un changement de template : `tools/preview_layouts.py --accenture`.

## Utilisation

```python
d = AccentureDeck()
d.layout("section_dark", {0: "Notre approche", 2: "02", 1: "Sous-titre"})   # clé de LAYOUTS, ou nom complet
d.layout("Columns 2 - Headline + GT Sectra", {0: "Titre", 1: "Accroche en Palatino", 2: "Texte"})
```

- `texts` : `{idx: texte balisé}` ; le style du layout (police, taille, couleur) est conservé ; un placeholder absent
  de `texts` est supprimé. Le titre (idx 0) est réduit s'il ne tient pas sur une ligne.
- `visuals` : un élément par placeholder photo, dans l'ordre des idx : chemin d'une photo, ou nom d'une icône
  (`pictos_accenture.md`). Sans visuel, l'emplacement est supprimé : jamais de cadre vide.
- Les idx d'un même rôle changent d'un layout à l'autre (le grand numéro d'intercalaire est l'idx 2 sur fond foncé,
  l'idx 1 sur fond clair) : les raccourcis s'en chargent. Raccourcis : `cover(titre, sous-titre, date, auteur,
  variant)`, `agenda(entrées, titre, intro)`, `section(titre, numéro, sous-titre, style)`, `key_message(texte,
  style)`, `slide(titre, sous-titre, dark)`, `blank(titre, dark)`, `closing(texte, gradient)`.
- Les couvertures « Greetings » et « Cover Image » ont des photos et des dégradés de la marque : les garder telles
  quelles, sans y poser de visuel.

## Index

| Aperçu | Nom complet | Clé | Quand l'utiliser | Placeholders |
|---|---|---|---|---|
| `Title_and_Content-Light` | Title and Content - Light | `content` | Slide de contenu courante, fond blanc : `slide()` | 0 titre, 1 body |
| `Cover_Basic-Light_Black_Text` | Cover Basic - Light, Black Text | `cover_light` | Couverture sur fond blanc : `cover(variant="light")` | 0 titre, 1 subtitle, 2 body, 10 date |
| `Agenda` | Agenda | `agenda` | Sommaire numéroté, 1 à 16 entrées : `agenda()` | 0 titre, 1 accroche, 2 à 9 puis 21 à 28 entrées, 13 à 20 puis 29 à 36 numéros |
| `Section_Divider_with_Image-Gradient_Light` | Section Divider with Image - Gradient Light | — | Intercalaire avec image, dégradé clair | 0 titre, 1 body, 2 photo |
| `Section_Divider-Numbered_Gradient_Light` | Section Divider - Numbered, Gradient Light | `section_light` | Intercalaire numéroté, dégradé clair, texte noir : `section(style="light")` | 0 titre, 1 body, 2 body |
| `Columns_2-Headline_GT_Sectra` | Columns 2 - Headline + GT Sectra | `headline_serif` | Titre et accroche en Palatino à gauche, texte à droite | 0 titre, 1 body, 2 body |
| `Columns_2-Headline_Content` | Columns 2 - Headline + Content | — | Deux colonnes : intitulé et texte | 0 titre, 1 body, 2 body, 3 body, 4 body, 5 body, 6 body |
| `Columns_3-List` | Columns 3 - List | `columns_3` | Trois colonnes numérotées (le composant `colonnes()` fait de même en libre) | 0 titre, 1 body, 2 body, 3 body, 4 body, 5 body, 6 body, 7 body, 8 body, 9 body |
| `Columns_4-List` | Columns 4 - List | `columns_4` | Quatre colonnes numérotées | 0 titre, 1 body, 2 body, 3 body, 4 body, 5 body, 6 body, 7 body, 8 body, 9 body, 13 body, 14 body, 15 body |
| `Icons_5` | Icons 5 | — | Cinq icônes et leur texte | 0 titre, 1 body, 2 photo, 3 body, 4 body, 5 body, 6 body, 7 photo, 8 photo, 9 photo, 13 photo |
| `Team_4-Box_Shadow` | Team 4 - Box Shadow | — | Équipe de 4 : photos et noms | 0 titre, 1 body, 2 photo, 3 photo, 4 photo, 5 photo, 6 body, 7 body, 8 body |
| `Team_6-Light` | Team 6 - Light | — | Équipe de 6, fond blanc | 0 titre, 1 body, 2 photo, 3 photo, 4 photo, 5 photo, 6 photo, 7 photo, 8 body, 9 body, 13 body, 14 body, 15 body |
| `Team_8_Text` | Team 8 + Text | — | Équipe de 8 avec un texte | 0 titre, 1 body, 2 photo, 3 photo, 4 photo, 5 photo, 6 body, 7 body, 8 body, 9 body, 13 photo, 14 photo, 15 photo, 16 photo, 17 body, 18 body, 19 body, 20 body |
| `Text_and_Image_1` | Text and Image 1 | `text_image` | Titre et accroche à gauche, photo pleine hauteur à droite | 0 titre, 1 body, 2 photo, 12 slide_number |
| `Quote_Portrait_1` | Quote + Portrait 1 | `quote` | Citation et portrait | 0 titre, 2 photo |
| `Stat_1` | Stat 1 | `stat` | Quatre chiffres clés et une photo | 1 body, 2 photo, 3 body, 4 body, 5 body, 6 body, 7 body, 8 body, 9 body |
| `Stat_2` | Stat 2 | — | Chiffres clés, variante à deux images | 0 titre, 1 body, 3 body, 4 body, 5 body, 6 body, 7 body, 8 photo, 9 body, 13 body |
| `Key_Message_Gradient_Light_1` | Key Message Gradient Light 1 | `message_light` | Message clé seul, dégradé clair : `key_message(style="light")` | 0 titre |
| `Blank-Light` | Blank - Light | `blank` | Slide libre, titre facultatif : `blank()` | 0 titre |
| `Greetings_Slide-GTS` | Greetings Slide - GTS | — | Couverture ou slide d'accueil de la marque (« Greetings », « Cover Image ») : variante visuelle | 0 titre |
| `Greetings_Slide-Logo` | Greetings Slide - Logo | — | Couverture ou slide d'accueil de la marque (« Greetings », « Cover Image ») : variante visuelle | 0 titre |
| `Greetings_Greater_Than_L_Blank` | Greetings + Greater Than L Blank | — | Couverture ou slide d'accueil de la marque (« Greetings », « Cover Image ») : variante visuelle | 0 titre |
| `Greetings_Greater_Than_L` | Greetings + Greater Than L | `closing` | Slide de fin, grand « > » : `closing()` | 0 titre |
| `Greetings_Greater_Than_S_with_Image` | Greetings + Greater Than S with Image | — | Couverture ou slide d'accueil de la marque (« Greetings », « Cover Image ») : variante visuelle | 0 titre |
| `Greetings_Greater_Than_S` | Greetings + Greater Than S  | — | Couverture ou slide d'accueil de la marque (« Greetings », « Cover Image ») : variante visuelle | 0 titre |
| `Cover_Image-Centered_GTS` | Cover Image - Centered, GTS | — | Couverture ou slide d'accueil de la marque (« Greetings », « Cover Image ») : variante visuelle | 0 titre, 1 body, 2 body, 10 date |
| `Cover_Image-Centered_Logo` | Cover Image - Centered, Logo | — | Couverture ou slide d'accueil de la marque (« Greetings », « Cover Image ») : variante visuelle | 0 titre, 1 body, 2 body, 10 date |
| `Cover_Image-Large_GTS` | Cover Image - Large GTS | — | Couverture ou slide d'accueil de la marque (« Greetings », « Cover Image ») : variante visuelle | 0 titre, 1 body, 2 body, 10 date |
| `Cover_Image-Left-aligned_GTS` | Cover Image - Left-aligned, GTS | — | Couverture ou slide d'accueil de la marque (« Greetings », « Cover Image ») : variante visuelle | 0 titre, 1 subtitle, 2 body, 10 date |
| `Cover_Image-Left-aligned_Logo` | Cover Image - Left-aligned, Logo | `cover_image` | Couverture sur photo de fond du template : `cover(variant="image")` | 0 titre, 1 body, 2 subtitle, 10 date |
| `Cover_Image-Left-aligned_GTS_with_Image` | Cover Image - Left-aligned, GTS, with Image | — | Couverture ou slide d'accueil de la marque (« Greetings », « Cover Image ») : variante visuelle | 0 titre, 1 subtitle, 2 body, 10 date |
| `Cover_Image-Left-aligned_Logo_with_Image` | Cover Image - Left-aligned, Logo, with Image | — | Couverture ou slide d'accueil de la marque (« Greetings », « Cover Image ») : variante visuelle | 0 titre, 1 body, 2 subtitle, 10 date |
| `Cover_Basic-Dark_White_Text` | Cover Basic - Dark, White Text | `cover` | Couverture par défaut, fond violet foncé : `cover()` | 0 titre, 1 subtitle, 2 body, 10 date |
| `Section_Divider_with_Image-Gradient_Dark` | Section Divider with Image - Gradient Dark | — | Intercalaire avec image, dégradé foncé | 0 titre, 1 body, 2 photo |
| `Section_Divider_with_Image-Gradient_Mid` | Section Divider with Image - Gradient Mid | — | Intercalaire avec image, dégradé moyen | 0 titre, 1 body, 2 photo |
| `Section_Divider_with_Image-Gradient_Core` | Section Divider with Image - Gradient Core | — | Intercalaire avec image, dégradé violet vif | 0 titre, 1 body, 2 photo |
| `Section_Divider-Numbered_Gradient_Dark_Purple` | Section Divider - Numbered, Gradient Dark Purple | `section_dark` | Intercalaire numéroté, dégradé violet foncé : `section(style="dark")` | 0 titre, 1 body, 2 body |
| `Section_Divider-Numbered_Gradient_Mid_Purple` | Section Divider - Numbered, Gradient Mid Purple | `section_mid` | Intercalaire numéroté, dégradé violet moyen : `section(style="mid")` | 0 titre, 1 body, 2 body |
| `Section_Divider-Numbered_Gradient_Core_Purple` | Section Divider - Numbered, Gradient Core Purple | `section_core` | Intercalaire numéroté, dégradé violet vif : `section(style="core")` | 0 titre, 1 body, 2 body |
| `Title_and_Content-Dark` | Title and Content - Dark | `content_dark` | Slide de contenu sur fond violet foncé : `slide(dark=True)`, texte blanc | 0 titre, 1 body |
| `Team_6-Dark` | Team 6 - Dark | — | Équipe de 6, fond foncé | 0 titre, 1 body, 2 photo, 3 photo, 4 photo, 5 photo, 6 photo, 7 body, 8 photo, 9 body, 13 body, 14 body, 15 body |
| `Text_and_Image_2` | Text and Image 2 | — | Texte et image sur fond foncé | 0 titre, 1 body |
| `Key_Message_Gradient_Dark_1` | Key Message Gradient Dark 1 | `message_dark` | Message clé seul, dégradé foncé : `key_message()` | 0 titre |
| `Key_Message_Mid_Purple` | Key Message Mid Purple | `message_purple` | Message clé seul, aplat violet : `key_message(style="purple")` | 0 titre |
| `Full_Bleed_Image` | Full Bleed Image | — | Photo plein cadre et titre | 0 titre, 2 photo, 12 slide_number |
| `Blank-Dark` | Blank - Dark | `blank_dark` | Slide libre sur fond violet foncé : `blank(dark=True)` | 0 titre |
| `Greetings_Greater_Than_L_Gradient` | Greetings + Greater Than L Gradient | `closing_gradient` | Slide de fin sur dégradé : `closing(gradient=True)` | 0 titre |
