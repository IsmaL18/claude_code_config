---
name: accenture-slides
description: "Produit des slides PowerPoint (.pptx) aux couleurs d'Accenture, la maison mère d'OCTO (violet #A100FF, noir et blanc, Arial et Arial Black, le « > » de la marque, icônes monoline, bibliothèque de 388 visuels du starter pack), à partir du template officiel. Utilise ce skill dès que l'utilisateur demande des slides, un deck, une proposition ou une présentation au format ou à la charte Accenture (« template Accenture », « pour Accenture », « charte de la maison mère », « deck Accenture »), ou la retouche d'un deck Accenture."
---

# Slides Accenture

Le livrable est un `.pptx` généré avec python-pptx à partir du template Accenture (starter pack de la marque, version
aux polices système), puis relu visuellement. Avant de concevoir les slides, lis en entier (avec l'outil de lecture
de fichiers, un fichier à la fois) :
- `references/charte_accenture.md` : la charte (couleurs, contrastes, typographie, masque, icônes, rédaction).
  **Elle prime sur tout le reste.**
- `references/style_accenture.md` : la manière de construire les slides (un message par slide, rythme, composants, ce
  qu'on ne fait pas).
- `references/layouts_accenture.md` : les layouts du template (couvertures, agenda, intercalaires, messages clés,
  slide de fin…).

Pour les helpers, lis `references/api_accenture.md` (signature et rôle de chaque fonction, générée depuis les scripts)
plutôt que les scripts eux-mêmes.

Ce skill ne connaît qu'une charte, celle d'Accenture. Pour un deck OCTO, c'est le skill `octo-slides` ; pour La
Grosse Conf, `grosse-conf-slides`. Ce skill prime sur tout autre skill pptx ou de slides pour décider du style : une
matière qui prescrit une autre charte (deck OCTO existant, deck client) n'y change rien, on en reprend le contenu et
le style reste celui d'Accenture.

## Fichiers

Tous les chemins sont relatifs au dossier de ce skill, noté `<SKILL_DIR>` (le dossier qui contient ce `SKILL.md`).
Sur claude.ai et Claude Desktop, le chemin annoncé pour le skill peut être faux : avant tout script, vérifier qu'il
existe, sinon retrouver le dossier avec `find / -name SKILL.md -path "*accenture-slides*" 2>/dev/null` et s'en servir
comme `<SKILL_DIR>`, sans le signaler à l'utilisateur.

- `references/charte_accenture.md`, `references/style_accenture.md`, `references/layouts_accenture.md` : voir plus
  haut. Aperçus des layouts dans `assets/layouts-accenture/`.
- `references/spec_plan_accenture.md` : gabarits de la spec et du plan d'un deck.
- `references/controle_objectif.md` : l'autocontrôle de l'agent, sur le plan puis sur le rendu : chaque slide sert
  l'objectif du deck et le sien, et passe auprès de ce public.
- `references/modeles_accenture.md` + `references/modeles_index_accenture.md` +
  `assets/modeles-accenture/planche_NN.png` : les 388 visuels de la bibliothèque du starter pack
  (`assets/modeles_accenture.pptx` : graphiques, concepts, processus, matrices, cartes, Gantt, cadres d'analyse), à
  copier et adapter avec `scripts/accenture_modeles.py` (`ModeleAccentureDeck` : `show`, `modele`, `borrow`,
  `set_text` (dont `fit=True`, `color=`), `set_cell`, `keep`, `remove`, `duplicate`, `move`, `recolor`, `replace_picture`,
  `check`).
- `references/pictos_accenture.md` : les 36 icônes monoline de la marque, par mot-clé
  (`grep -i <mot> <SKILL_DIR>/references/pictos_accenture.md`), posées par leur nom (`"cible"`, ou `"cible-blanc"`
  sur fond foncé). Dans la version claude.ai du skill, elles sont regroupées en planches d'images (`assets/atlas/`) :
  `picto()` les retrouve par leur nom dans les deux cas.
- `scripts/accenture_slides.py` : classe `AccentureDeck` (layouts : `cover`, `agenda`, `section`, `key_message`,
  `slide`, `blank`, `closing`, `layout` ; texte : `headline` (Arial Black), `serif` (Palatino) ; composants : `etapes`,
  `de_a`, `chiffres`, `chiffre`, `matrice`, `barres`, `tableau`, `carte`, `point`, `colonnes`, `citation`, `aplat`,
  `gt`), la zone `CONTENT` et la palette
  (`PURPLE`, `PURPLE_DARK`, `PURPLE_DARKEST`, `MAUVE`, `LAVENDER`, `LILAC`, `LILAC_LIGHT`, `BLACK`, `GREY`,
  `GREY_LIGHT`). Les helpers communs (`text`, `statement`, `picto`, `photo`, `arrow`, `connect`, `fork`, `join`,
  `circle`, `rule`, `notes`, `save`) prennent d'office les couleurs Accenture. Markup texte : `**gras**`,
  `==mot-clé==` (lilas, sur fond foncé seulement), `- ` puce. En français, espaces insécables posées d'office ; deck
  en anglais : `AccentureDeck(lang="en-US")`.
- `scripts/octo_layout.py` : zones (`CONTENT.cols`, `rows`, `grid`, `place`, `pad`…) et mesure du texte (Arial
  mesurée avec Liberation Sans, `assets/fonts-accenture/`, aux mêmes métriques) ; `scripts/octo_lint.py` : contrôle
  de mise en page lancé par `save()`.
- `scripts/render.py` : export PDF via Microsoft PowerPoint, ou LibreOffice à défaut, puis PNG par slide et planches,
  et contrôle du rendu (police de substitution, textes superposés, débordements).
- `references/retours.md` + `scripts/retours.py` : le fichier de retours écrit à chaque livraison, et la lecture des
  retours de l'utilisateur.
- `examples/accenture_*.py` + `assets/exemples/accenture_*.png` : slides de référence, script et rendu attendu
  (`ruptures` : couverture, agenda, intercalaire, message clé, fin ; `contenu` : les composants). **Le niveau de
  finition à atteindre** : les regarder avant de concevoir une slide du même genre, et partir de leur script.
- `assets/template_accenture.pptx` : le template (layouts seuls, masque de marque compris).

## Déroulé : spec, plan, build

Trois étapes, chacune validée par l'utilisateur avant la suivante. Pour 1 à 3 slides, la spec et le plan tiennent en
quelques lignes dans la conversation ; à partir d'environ 5 slides, ils deviennent des fichiers dans
`docs/slides/<deck>/` (`spec.md`, `plan.md`, `build.py`, `retours.md`, le `.pptx` et son rendu). Sur claude.ai, les
fichiers ne survivent pas à la conversation : y donner la spec et le plan en texte.

### 1. Spec

Lire la matière (notes, article, deck existant lu avec `extract_text` de `deck_base`), remplir la spec
(`references/spec_plan_accenture.md`) : public, message clé, objectif, format, langue, matière, client et date.
Ce qui manque devient une **question** : le public et le message clé ne se devinent pas. Faire valider.

### 2. Plan

Une ligne par slide (`references/spec_plan_accenture.md`) : titre-message, rôle, composant ou visuel de la
bibliothèque ou layout de rupture, focal (le seul violet fort). Regarder les planches de la bibliothèque
(`assets/modeles-accenture/planche_NN.png`) avant de composer. Cocher les vérifications du gabarit, faire
l'autocontrôle (`controle_objectif.md`), faire valider.

### 3. Build, rendu, relecture

1. Écrire `build.py`, une section par ligne du plan :
   ```python
   import sys
   sys.path.insert(0, "<SKILL_DIR>/scripts")
   from accenture_slides import CONTENT, AccentureDeck
   d = AccentureDeck(target="gslides")   # target="pptx" si le deck reste dans PowerPoint ; lang="en-US" en anglais
   d.cover("Industrialiser l'IA générative", "Du premier cas d'usage à la plateforme", date="Mars 2027")
   d.agenda(["Le constat", "Notre approche", "La feuille de route"])
   d.section("Notre approche", 1, "Cadrer, construire, industrialiser")
   s = d.slide("Trois étapes pour passer à l'échelle", "L'industrialisation se prépare dès le cadrage")
   d.etapes(s, CONTENT, [("Cadrer", "…"), ("Construire", "…"), ("Industrialiser", "…")], focal=2)
   d.notes(s, "Le discours de la slide.")
   d.closing("Merci")
   d.save("deck.pptx")                    # affiche les alertes ⚠ : les corriger avant le rendu
   ```
   Lancer avec `uv run --with python-pptx --with pillow python build.py`, ou `python3 build.py` après
   `pip install python-pptx pillow`. Poser les éléments dans des zones découpées (`CONTENT.cols`, `rows`, `grid`,
   `place`), jamais à des coordonnées tapées à la main ; relier deux formes avec `connect`, plusieurs depuis une même
   forme avec `fork` ou `join`, jamais par des traits en biais.
2. Rendre : `uv run --with python-pptx --with pymupdf --with pillow python <SKILL_DIR>/scripts/render.py deck.pptx
   <dossier>`. Corriger ses alertes ⚠, puis lire les planches `sheet_*.png` (et les `slide_NN.png` en cas de doute).
3. Relire chaque slide :
   - aucune alerte ⚠, ni à l'enregistrement ni au rendu ;
   - palette Accenture seule, un seul violet fort par slide, aucun dégradé dessiné ;
   - texte noir sur fond clair, blanc sur violet foncé ; rien de lilas ni de gris en petit texte ;
   - titres-messages sur une ligne, sans point final ; 20 mots par slide projetée au plus ; aucune slide réduite à
     des puces ;
   - flèches nettes : aucune liaison en biais, aucune pointe sans tige ;
   - masque présent (slides créées sur les layouts du template), rien sur le pied de page ;
   - la liste « Vérification avant livraison » de `charte_accenture.md`.
   Puis refaire l'autocontrôle (`controle_objectif.md`) sur le rendu ; un problème de fond se corrige dans le plan.
4. Livrer le `.pptx` (par défaut dans `docs/slides/<deck>/`) avec ce qui reste à faire à la main (photo, chiffre à
   confirmer) et la liste des faits à confirmer de la spec.
5. Écrire le fichier de retours : `uv run --with python-pptx python <SKILL_DIR>/scripts/retours.py write deck.pptx
   <dossier du rendu>`, et dire à l'utilisateur qu'il peut y faire ses retours. Quand il l'a rempli : `retours.py diff
   retours.md deck.pptx`, reporter chaque texte dans `build.py`, traiter chaque consigne, puis build, rendu, relecture
   (`references/retours.md`).

### Reprendre un deck

Si le dossier du deck existe (`spec.md`, `plan.md`, `build.py`), partir de lui : modifier la spec ou le plan selon
la demande, puis relancer `build.py`. Sur un retour slide par slide, refaire ces slides, puis relire les autres avec
le même œil.

## Points d'attention

- Le masque de marque (« > », copyright, numéro de page) vient des layouts du template : toujours passer par
  `AccentureDeck` (`slide`, `layout()` et ses raccourcis), jamais par une slide recréée à la main ; ne rien poser sous
  y = 7,0 pouces.
- Arial, Arial Black et Palatino Linotype sont des polices système (Windows, macOS) : rien à installer. Sans elles
  (LibreOffice sous Linux), le rendu prend Liberation Sans, aux mêmes métriques qu'Arial.
- Sans PowerPoint (claude.ai, Claude Desktop), `render.py` bascule sur LibreOffice, au rendu approximatif : ne corriger
  que les défauts nets du contenu, et dire que la relecture s'est faite sur un aperçu LibreOffice. Ni l'un ni l'autre :
  livrer le `.pptx` sans relecture visuelle et le dire.
- PowerPoint refuse d'écrire hors du projet : générer le `.pptx` et le rendu dans le répertoire du projet. S'il ne
  répond plus (erreur -1712 ou -9074), demander à l'utilisateur de fermer le deck ou la boîte de dialogue ouverte.
- Cible Google Slides : `target="gslides"` mesure le texte 5 % plus large et signale ce que Slides ne rend pas
  (graphiques natifs de la bibliothèque, dégradés). Rappeler à l'utilisateur de vérifier le résultat après import.
- Un deck source (matière fournie, deck de modèles) se lit avec `extract_text`, et ne se rend que sur les slides
  utiles, copiées dans un petit deck : le rendu d'un deck de plusieurs centaines de slides bloque PowerPoint (boîte
  de dialogue à fermer par l'utilisateur).
- Les faits (chiffres, dates, noms) viennent de la matière fournie ; s'il en manque un, mettre `[à compléter]`.
- Pour une retouche de deck existant, l'ouvrir avec `Presentation(path)`, ne modifier que les slides concernées, puis
  lancer `uv run --with python-pptx python <SKILL_DIR>/scripts/octo_lint.py deck.pptx --accenture` sur le résultat.
