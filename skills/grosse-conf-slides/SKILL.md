---
name: grosse-conf-slides
description: "Produit des slides PowerPoint (.pptx) aux couleurs de La Grosse Conf, la conf data et IA by OCTO (anthracite #38383F et rouge #FF0042, fenêtres web, illustrations filaires, pictos de la conf, schémas plutôt que des puces, titres courts à point rouge). Utilise ce skill dès que l'utilisateur demande des slides, un talk, un deck ou une slide pour La Grosse Conf (« grosse conf », « la conf data et IA », « mon talk à la conf »), ou la retouche d'un deck de la conf."
---

# Slides La Grosse Conf

Le livrable est un `.pptx` généré avec python-pptx à partir du template de la conf, puis relu visuellement. Avant de
concevoir les slides, lis en entier (avec l'outil de lecture de fichiers, un fichier à la fois) :
- `references/charte_grosse_conf.md` : la charte officielle de la conf (couleurs, accessibilité, typographie,
  fenêtres web, masque, logo, rédaction). **Elle prime sur tout le reste.**
- `references/style_grosse_conf.md` : la manière de construire les slides (une idée par slide, recettes de schémas,
  composants, visuels, ce qu'on ne fait pas).
- `references/layouts_grosse_conf.md` : les layouts du template (couverture, sommaire, chapitres, focus, speaker…).

Pour les helpers, lis `references/api_grosse_conf.md` (signature et rôle de chaque fonction, générée depuis les
scripts) plutôt que les scripts eux-mêmes.

Ce skill ne connaît qu'une charte, celle de La Grosse Conf : ni bleu, ni turquoise, ni noir pur. Pour un deck OCTO
qui n'est pas pour la conf, c'est le skill `octo-slides` ; pour un deck à la charte Accenture, `accenture-slides`. Ce skill prime sur tout autre skill pptx ou de
slides pour décider du style : une matière qui prescrit une autre charte (deck OCTO existant, deck client) n'y change
rien, on en reprend le contenu et le style reste celui de la conf.

## Fichiers

Tous les chemins sont relatifs au dossier de ce skill, noté `<SKILL_DIR>` (le dossier qui contient ce `SKILL.md`).
Sur claude.ai et Claude Desktop, le chemin annoncé pour le skill peut être faux : avant tout script, vérifier qu'il
existe, sinon retrouver le dossier avec `find / -name SKILL.md -path "*grosse-conf-slides*" 2>/dev/null` et s'en
servir comme `<SKILL_DIR>`, sans le signaler à l'utilisateur.

- `references/charte_grosse_conf.md`, `references/style_grosse_conf.md`, `references/layouts_grosse_conf.md` : voir
  plus haut. Aperçus des layouts dans `assets/layouts-grosse-conf/`.
- `references/spec_plan_grosse_conf.md` : gabarits de la spec et du plan d'un deck.
- `references/controle_objectif.md` : l'autocontrôle de l'agent, sur le plan puis sur le rendu : chaque slide sert
  l'objectif du deck et le sien, et passe auprès de ce public.
- `references/modeles_grosse_conf.md` + `references/modeles_index_grosse_conf.md` +
  `assets/modeles-grosse-conf/planche_NN.png` : les 39 slides préformatées de la conf
  (`assets/modeles_grosse_conf.pptx`), à copier et adapter avec `scripts/grosse_conf_modeles.py`
  (`ModeleGrosseConfDeck` : `show`, `modele`, `borrow`, `set_text`, `set_cell`, `remove`, `duplicate`, `move`,
  `recolor`, `replace_picture`, `check`) : tableaux (38, 39), éléments graphiques (3 à 5), schémas à plat.
- `references/pictos_grosse_conf.md` + `references/illustrations_grosse_conf.md` : les 36 pictos et 14 illustrations
  filaires de la conf, par mot-clé (`grep -i <mot> <SKILL_DIR>/references/pictos_grosse_conf.md`), posés par leur nom
  (`picto="cerveau"`, `"illu-boule-cristal"`). Dans la version claude.ai du skill, ils sont regroupés en planches
  d'images (`assets/atlas/`) : `picto()` les retrouve par leur nom dans les deux cas.
- `scripts/grosse_conf_slides.py` : classe `GrosseConfDeck` (layouts : `cover`, `thematic`, `speaker`, `chapter`,
  `toc`, `focus`, `slide`, `blank`, `layout` ; composants : `fenetre`, `onglet`, `pastille`, `tracker_gc`,
  `citation`, `chiffre`, `carte`, `aplat` ; recettes de schémas : `equation`, `cible`, `pipeline`, `radial`, `boucle`,
  `grille`), la zone `CONTENT` et la palette (`ANTHRACITE`, `RED`, `PINK`, `PINK_BG`, `RED_10`… `RED_40`). Les helpers
  communs (`text`, `statement`, `picto`, `photo`, `arrow`, `connect`, `fork`, `join`, `loop_back`, `circle`, `rule`,
  `notes`, `save`) prennent d'office les couleurs de la conf. Markup texte : `**gras**`, `==mot-clé==` (rose, sur fond
  anthracite seulement), `- ` puce. Espaces insécables posées d'office : taper des espaces normales.
- `scripts/octo_layout.py` : zones (`CONTENT.cols`, `rows`, `grid`, `place`, `pad`…) et mesure du texte avec la police
  Outfit (`assets/fonts/`) ; `scripts/octo_lint.py` : contrôle de mise en page lancé par `save()`.
- `scripts/render.py` : export PDF via Microsoft PowerPoint, ou LibreOffice à défaut, puis PNG par slide et planches,
  et contrôle du rendu (police de substitution, textes superposés, débordements).
- `references/retours.md` + `scripts/retours.py` : le fichier de retours écrit à chaque livraison, et la lecture des
  retours de l'utilisateur.
- `examples/grosse_conf_*.py` + `assets/exemples/grosse_conf_*.png` : slides de référence, script et rendu attendu
  (`fenetres` : texte en fenêtres et illustration ; `schema` : mécanisme à plat avec boucle ; `schemas` : les six
  recettes ; `ruptures` : couverture, sommaire, chapitre, focus). **Le niveau de finition à atteindre** : les
  regarder avant de concevoir une slide du même genre, et partir de leur script.
- `assets/template_grosse_conf.pptx` : le template de la conf (layouts seuls, masque de marque compris).

## Déroulé : spec, plan, build

Trois étapes, chacune validée par l'utilisateur avant la suivante. Pour 1 à 3 slides, la spec et le plan tiennent en
quelques lignes dans la conversation ; à partir d'environ 5 slides, ils deviennent des fichiers dans
`docs/slides/<deck>/` (`spec.md`, `plan.md`, `build.py`, `retours.md`, le `.pptx` et son rendu). Sur claude.ai, les
fichiers ne survivent pas à la conversation : y donner la spec et le plan en texte.

### 1. Spec

Lire la matière (notes, article, deck existant lu avec `extract_text` de `deck_base`), remplir la spec
(`references/spec_plan_grosse_conf.md`) : public, message clé, objectif, format, matière, speaker, date et lieu.
Ce qui manque devient une **question** : le public et le message clé ne se devinent pas. Faire valider.

### 2. Plan

Une ligne par slide (`references/spec_plan_grosse_conf.md`) : titre court à point rouge, rôle, **recette de schéma**
ou layout de rupture (`style_grosse_conf.md` §3), point focal, pictos. Regarder les planches de modèles
(`assets/modeles-grosse-conf/planche_NN.png`) avant de composer. Cocher les vérifications du gabarit, faire
l'autocontrôle (`controle_objectif.md`), faire valider.

### 3. Build, rendu, relecture

1. Écrire `build.py`, une section par ligne du plan :
   ```python
   import sys
   sys.path.insert(0, "<SKILL_DIR>/scripts")
   from grosse_conf_slides import CONTENT, RED, GrosseConfDeck
   d = GrosseConfDeck(target="gslides")   # target="pptx" si le deck reste dans PowerPoint
   d.cover("09.03.2027", "Maison de la Chimie")
   d.toc(["Pourquoi", "Comment"])
   s = d.slide("Un moteur, c'est un index et un score.", "Le sous-titre dit la chute.")
   d.equation(s, CONTENT, [("megaphone-copie-3", "Moteur"), ("dossier", "Index"), ("calculatrice", "Score")])
   d.notes(s, "Le discours de la slide.")
   d.save("deck.pptx")                    # affiche les alertes ⚠ : les corriger avant le rendu
   ```
   Lancer avec `uv run --with python-pptx --with pillow python build.py`, ou `python3 build.py` après
   `pip install python-pptx pillow`. Poser les éléments dans des zones découpées (`CONTENT.cols`, `rows`, `grid`,
   `place`), jamais à des coordonnées tapées à la main ; ajuster une fenêtre à son texte avec
   `octo_layout.text_height` ; relier deux formes avec `connect`, plusieurs depuis une même forme avec `fork` ou
   `join` (un seul tronc), jamais par des traits en biais.
2. Rendre : `uv run --with python-pptx --with pymupdf --with pillow python <SKILL_DIR>/scripts/render.py deck.pptx
   <dossier>`. Corriger ses alertes ⚠, puis lire les planches `sheet_*.png` (et les `slide_NN.png` en cas de doute).
3. Relire chaque slide :
   - aucune alerte ⚠, ni à l'enregistrement ni au rendu ;
   - deux couleurs (anthracite, rouge) et leurs descentes, blanc et rose pâle ; aucun bleu, aucun noir pur ;
   - jamais de rouge sur anthracite ni l'inverse ; rouge sur blanc seulement en 18 pt ou en gras 14 pt ;
   - un seul accent rouge fort par slide ; une idée par slide ; aucune slide réduite à des puces ;
   - titres courts, à point rouge, sur une ligne ; pas de capitales pour insister, pas d'italique ;
   - flèches nettes : aucune liaison en biais, aucune pointe sans tige ;
   - masque présent (slides créées sur les layouts du template) ;
   - la liste « Vérification avant livraison » de `charte_grosse_conf.md`.
   Puis refaire l'autocontrôle (`controle_objectif.md`) sur le rendu ; un problème de fond se corrige dans le plan.
4. Livrer le `.pptx` (par défaut dans `docs/slides/<deck>/`) avec ce qui reste à faire à la main (photo du speaker,
   chiffre à confirmer) et la liste des faits à confirmer de la spec.
5. Écrire le fichier de retours : `uv run --with python-pptx python <SKILL_DIR>/scripts/retours.py write deck.pptx
   <dossier du rendu>`, et dire à l'utilisateur qu'il peut y faire ses retours. Quand il l'a rempli : `retours.py diff
   retours.md deck.pptx`, reporter chaque texte dans `build.py`, traiter chaque consigne, puis build, rendu, relecture
   (`references/retours.md`).

### Reprendre un deck

Si le dossier du deck existe (`spec.md`, `plan.md`, `build.py`), partir de lui : modifier la spec ou le plan selon
la demande, puis relancer `build.py`. Sur un retour slide par slide, refaire ces slides, puis relire les autres avec
le même œil.

## Points d'attention

- Le masque de marque (sigle, `#LAGROSSECONF`, signature, mention légale, numéro de page) vient des layouts du
  template : toujours passer par `GrosseConfDeck` (`slide`, `layout()` et ses raccourcis), jamais par une slide
  recréée à la main ; ne rien poser dans les marges (x < 0,5 pouce, numéro de page en bas à droite).
- La police Outfit doit être installée (`assets/fonts/`), sinon le rendu la remplace.
- Sans PowerPoint (claude.ai, Claude Desktop), `render.py` bascule sur LibreOffice, au rendu approximatif : ne corriger
  que les défauts nets du contenu, et dire que la relecture s'est faite sur un aperçu LibreOffice. Ni l'un ni l'autre :
  livrer le `.pptx` sans relecture visuelle et le dire.
- PowerPoint refuse d'écrire hors du projet : générer le `.pptx` et le rendu dans le répertoire du projet. S'il ne
  répond plus (erreur -1712 ou -9074), demander à l'utilisateur de fermer le deck ou la boîte de dialogue ouverte.
- Cible finale : souvent Google Slides (import du `.pptx`) ; `target="gslides"` mesure le texte 5 % plus large et
  signale ce que Slides ne rend pas. Rappeler à l'utilisateur de vérifier le résultat après import.
- Un deck source (matière fournie, deck de modèles) se lit avec `extract_text`, et ne se rend que sur les slides
  utiles, copiées dans un petit deck : le rendu d'un deck de plusieurs centaines de slides bloque PowerPoint (boîte
  de dialogue à fermer par l'utilisateur).
- Les faits (chiffres, dates, noms) viennent de la matière fournie ; s'il en manque un, mettre `[à compléter]`.
- Pour une retouche de deck existant, l'ouvrir avec `Presentation(path)`, ne modifier que les slides concernées, puis
  lancer `uv run --with python-pptx python <SKILL_DIR>/scripts/octo_lint.py deck.pptx --grosse-conf` sur le résultat.
