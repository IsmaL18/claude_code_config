# Charte graphique La Grosse Conf (règles officielles)

Sources : « Charte graphique La Grosse Conf 2025 » (PDF de la Com, gardé dans le dépôt du skill, hors du skill livré), template G-Slide (`assets/template_grosse_conf.pptx`) et deck « Slides préformatées » de l'édition 2025 (`assets/modeles_grosse_conf.pptx`).
**À lire pour tout deck grosse conf** : c'est la seule charte de ce skill ; celle d'OCTO (bleu marine, turquoise) ne s'applique pas ici. La Grosse Conf fait partie de la marque OCTO, avec une identité propre : « franc-tireur », elle casse les codes visuels de la data et de l'IA (ni bleu, ni noir : rouge et rose).

## Couleurs (bichrome)

| Rôle | Hex | CMJN / Pantone | Usage |
|---|---|---|---|
| Principale 1 : gris anthracite | `#38383F` | C72 M63 J50 N56, Pantone 7547 U | texte, traits, fonds foncés, contours des fenêtres |
| Principale 2 : rouge | `#FF0042` | C0 M100 J60 N0, Pantone 2270 U | accent : pastilles, point final, ombres de fenêtres, aplats du point focal |
| Secondaires : descentes du rouge | `#FF80A1` (50 %), puis 40, 30, 20, 10 % | — | contraste dans les illustrations, schémas, pictos et fonds |
| Fond rose pâle | `#FFEDF2` | — | fond des slides de rupture (couverture, chapitres, speaker) |
| Blanc | `#FFFFFF` | — | fond des slides de contenu, intérieur des fenêtres |

Constantes dans `scripts/grosse_conf_slides.py` : `ANTHRACITE`, `RED`, `PINK` (50 %), `RED_40`, `RED_30`, `RED_20`, `RED_10`, `PINK_BG`, `WHITE`, et `descente(pct)`. Aucune autre couleur, pas de bleu ni de turquoise (celui des photos OCTO du deck de modèles est hors charte grosse conf).
Le deck de slides préformatées de la Com donnait le rouge en `#ED013A` (erreur de gabarit) et gardait des gris-bleus et turquoises OCTO : `tools/build_modeles.py` les remplace à la construction par la palette ci-dessus, la charte fait foi.

## Accessibilité (charte, p. 12, et modèle 4)

- Texte anthracite sur fond clair ou rose ; texte blanc ou rose (`#FF80A1`) sur fond anthracite.
- **Le rouge n'est pas lisible sur l'anthracite, ni l'anthracite sur le rouge** : jamais l'un sur l'autre.
- Rouge sur fond blanc, ou blanc sur fond rouge : seulement au-dessus de 18 pt, ou en gras au-dessus de 14 pt. `octo_lint.py` le mesure (seuils WCAG 4,5:1, et 3:1 pour les gros caractères) et propose le remède de cette charte.
- Ne pas transmettre une information par la seule couleur : doubler par une forme, un picto ou un libellé.

## Typographie

- **Outfit**, comme OCTO, de ExtraLight à Black ; le template embarque Outfit (`assets/fonts/` pour l'installation). Aucune autre police : l'Arial et le Century Gothic du thème du template ne servent pas.
- Titres en gras, gros, avec un **point final rouge** (« Les couleurs. »). Texte courant en Regular, en anthracite.
- Retenu pour ce skill (la charte ne tranche pas) : **bas de casse** (majuscule de début de phrase et noms propres), pas de capitales pour insister ; rédaction : espaces insécables avant « ; : ! ? % » et à l'intérieur des guillemets (posées d'office par les helpers : taper des espaces normales), guillemets français « », pas de point médian, pas d'italique, nombres en chiffres.

## Composants signature

- **Fenêtre web** : rectangle à coins arrondis au trait anthracite (0,75 à 1 pt), deux pastilles en haut à gauche (une rouge pleine, une vide), barre de titre, **ombre rouge décalée** sur certaines, barre de défilement rouge pour un texte long. « Tous les textes sont mis en valeur dans des fenêtres web, de taille et de forme adaptées au contenu. » Helper : `fenetre()`.
- **Onglet** (« 01 ») posé sur le bord haut d'une fenêtre ; **pastille** de sommaire (carré arrondi rose pâle, « 01 »).
- **Illustrations filaires** (`illustrations_grosse_conf.md`) : formes géométriques, un trait de **2 pt fixe** sur tous les éléments d'une même illustration, blanc ou anthracite selon le fond, un aplat rouge (ou sa descente) pour le relief. Elles associent les codes de l'IA et de la data pour un élément loufoque, une forme improbable.
- **Pictos** (`pictos_grosse_conf.md`) : pictos OCTO aux couleurs de la conf (anthracite et rouge ou rose), ou illustrations sans leur fenêtre web.
- **Éléments codés** du logo OCTO (cible, chrono, croix, triangle, parenthèse), à disséminer avec parcimonie ; ils sont déjà dans les layouts de rupture.
- **Trackers, flèches, séparateurs, bulles, guillemets, avatars** : modèles 3 à 5 du deck (`modeles_index_grosse_conf.md`).
- Visuels : jamais de banque d'images ni d'emoji ; pas d'image générée par IA sans demande explicite ; les photos OCTO du deck de modèles (échelle bleue, visuel 3D bleu, portraits) sont hors charte, sauf une photo fournie par l'utilisateur (speaker).

## Logo, signature et masque

- Logo « la grosse conf. » (sigle panda + texte) : taille minimale d'impression 15 mm, zone de protection égale à la hauteur de la tête du panda, déclinaisons : fond clair avec texte anthracite, fond foncé avec texte blanc, monochrome seulement faute d'autre solution. Jamais recoloré ni déformé. Il est dans les layouts (couverture, sigle en haut à gauche).
- Signature : « La Conf Data I IA by OCTO », sur tous les supports. Pied de page des slides de rupture : « LA CONF DATA I IA BY OCTO TECHNOLOGY » ; texte légal vertical à gauche des slides de contenu.
- **Masque** (obligatoire dans toute présentation) : la zone de marque qui encadre la slide (sigle, `#LAGROSSECONF`, signature, copyright, numéro de page en rond). Il vient des layouts du template : **toujours passer par un layout** (`GrosseConfDeck.layout()`), jamais par une slide recréée à la main, et ne rien poser dans les marges (x < 0,5 po, numéro de page en bas à droite). Sur slide, le texte du masque est en regular et bas de casse.

## Vérification avant livraison

- Deux couleurs seulement (anthracite, rouge) et leurs descentes, plus blanc et rose pâle ; aucun bleu, aucun noir pur.
- Contrastes : jamais rouge sur anthracite ni l'inverse ; rouge sur blanc seulement en 18 pt ou en gras 14 pt.
- Outfit seule police ; trait des illustrations de 2 pt ; ombres rouges uniquement sur les fenêtres.
- Masque présent (layout du template) ; logos, pictos et illustrations : fichiers de `assets/`, non modifiés.
- Aucune consigne du gabarit reprise (« Lorem ipsum », « xxx », « SLIDE À SUPPRIMER AVANT PRÉSENTATION », « Exemple intercalaire… »).
- Texte relu : orthographe, espaces insécables, pas de point médian, pas de capitales ni d'italique superflus.
