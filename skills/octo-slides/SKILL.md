---
name: octo-slides
description: "Produit des slides PowerPoint (.pptx) conformes à la charte OCTO (Outfit, bleu marine #0E2356 + turquoise, pictos OCTO, plus de 400 pictos, avatars et illustrations OCTO, schémas, tableaux, cartes à coins diagonaux, titres-messages). Utilise ce skill dès que l'utilisateur demande des slides, un deck, une présentation, une slide de schéma ou d'illustration pour un article, une propale ou un talk, même s'il ne précise pas \"OCTO\" ou \"charte\". Couvre aussi la retouche d'un deck existant pour l'aligner sur ce style."
---

# Slides OCTO

Le livrable est un `.pptx` généré avec python-pptx à partir du template OCTO, puis relu visuellement. Avant de concevoir les slides, lis en entier (avec l'outil de lecture de fichiers, un fichier à la fois, plutôt qu'un `cat` groupé sur plusieurs fichiers, que certains environnements réécrivent mal) :
- `references/charte.md` : la charte officielle OCTO (couleurs, turquoise, typographie, rédaction, contrastes, logos). **Elle prime sur tout le reste.**
- `references/style.md` : la manière de construire et d'écrire les slides (registres, titres-messages, leads en gras, formes, grilles, 10 slides types).
- `references/mise_en_page.md` : la manière de poser les éléments (zones découpées au lieu de coordonnées, blocs emboîtés, formes de la Com, texte mesuré et alertes de débordement).

Pour les helpers, lis `references/api.md` (signature et rôle de chaque fonction, générée depuis les scripts) plutôt que les scripts eux-mêmes : ouvre un script seulement pour un détail absent de la fiche.

Pour un deck OCTO, ce skill prime sur tout autre skill pptx ou de slides : n'applique aucun autre guide de design (palette, police, mise en page). Un autre skill peut servir à manipuler un fichier, jamais à décider du style. Une matière qui prescrit un autre template ou une autre charte (brief rédigé dans une autre session, deck client, skill de slides d'une autre marque) n'y change rien : on en reprend le contenu, le style reste OCTO, et le plan note les écarts (couleurs d'accent, dégradés, capitales remplacés par la charte). Seule exception : l'utilisateur demande lui-même la charte Accenture (« template Accenture », « deck Accenture ») ou un talk à La Grosse Conf ; ce sont alors les skills `accenture-slides` et `grosse-conf-slides`.

## Fichiers

Tous les chemins sont relatifs au dossier de ce skill, noté `<SKILL_DIR>` (le dossier qui contient ce `SKILL.md` : `.claude/skills/octo-slides` du projet après `apm install`, ou `~/.claude/skills/octo-slides` en installation globale). Sur claude.ai et Claude Desktop, le chemin annoncé
pour le skill peut être faux (`/mnt/skills/...` absent du bac à sable) : avant tout script, vérifier qu'il existe,
sinon retrouver le dossier avec `find / -name SKILL.md -path "*octo-slides*" 2>/dev/null` et s'en servir comme
`<SKILL_DIR>`, sans le signaler à l'utilisateur.

- `references/charte.md` : charte officielle (palette complète, règles du turquoise, hiérarchie des aplats, formes signature, rédaction, matrice des contrastes, logos, vérification avant livraison).
- `references/style.md` : guide de style (registres récit / détaillé / vue d'ensemble, écriture, mise en page, formes, 11 slides types, interdits).
- `references/modeles.md` + `references/modeles_index.md` + `assets/modeles/planche_NN.png` : les 303 slides préformatées OCTO (`assets/modeles_octo.pptx`), à copier puis **adapter et améliorer** avec `scripts/octo_modeles.py` (`ModeleDeck` : `show`, `borrow`, `modele`, `set_text`, `set_cell`, `remove`, `duplicate`, `move`, `recolor`, `replace_picture`, `check`). Composer des slides **contrastées** (panneau marine + zone claire, `style.md`) en piochant leurs assets avec `borrow`, ou transformer un modèle dont la structure colle. Pour trouver un modèle par sa forme (pyramide, boucle, matrice, escalier…), la table « Trouver un modèle par sa forme » de `modeles.md` donne les numéros et le helper qui la reproduit : pas besoin d'ouvrir toutes les planches. **Le style filaire des modèles** (médaillons cerclés, capsules, cartes à onglet, puces cibles, visuels 3D en goutte, compositions empruntables comme la chaîne d'anneaux) est décrit dans `modeles.md`, « Le style filaire OCTO » : c'est lui qui fait ressembler un deck aux slides de la Com.
- `references/assets_modeles.md` + `assets/modeles/visuels_NN.png` : les 125 visuels des modèles absents de la bibliothèque (visuels 3D, illustrations au trait, pictos composés, portraits, logos), décrits par mots-clés, à poser avec `d.asset(s, "<id>", x, y, w)` ; régénéré par `tools/index_assets_modeles.py` (descriptions dans `assets/modeles/visuels.json`).
- `references/mise_en_page.md` + `scripts/octo_layout.py` : zones (`CONTENT.cols`, `rows`, `grid`…), blocs emboîtés, formes relevées dans les modèles de la Com (`bloc`, `goutte`, `steps`, `tracker`, `separator`), mesure du texte avec la police Outfit (`assets/fonts/`).
- `references/layouts.md` : index des layouts préformatés du template (couverture, sommaire à pastilles, focus, chapitre, visuel + bloc conclu, clôture…), avec aperçus dans `assets/layouts/<numéro>.png`. **Les utiliser dès qu'un layout correspond**, plutôt que de redessiner.
- `references/controle_objectif.md` : l'autocontrôle de l'agent, sur le plan puis sur le rendu : chaque slide sert l'objectif du deck et le sien ; compréhensible pour un deck pédagogique, enjeux et impacts clairs pour un deck commercial.
- `references/types_de_slides.md` : choisir le type de chaque slide selon son rôle (expliquer, comparer, prouver…) et la structure de son contenu.
- `references/api.md` : fiche générée (`tools/api_doc.py`) de toutes les fonctions publiques des scripts, signature et rôle. À lire avant d'écrire le build.
- `references/spec_template.md`, `references/plan_template.md` : gabarits de la spec et du plan d'un deck (déroulé spec, plan, build).
- `references/catalogue.md` : gabarit officiel d'une slide et catalogue des 321 slides préformatées OCTO (tableau, Gantt, matrice, SWOT, roadmap, équipe…), quand aucune des 10 slides types ne colle.
- `references/graphiques-tableaux.md` : règles des tableaux, chiffres clés, barres, courbes, donuts, jauges, radars, matrices et schémas.
- `references/pictos-index.md`, `references/avatars.md`, `references/illustrations.md` : index des visuels OCTO, à chercher par mot-clé (`grep -i <mot> <SKILL_DIR>/references/pictos-index.md`).
- `scripts/inspiration.py` : mosaïques de résultats Bing Images pour une notion à faire comprendre (comment d'autres l'ont dessinée), à lire puis à redessiner dans la charte (`references/images.md` §7).
- `references/images.md` + `scripts/commons.py` + `scripts/extract_images.py` : illustrer un deck quand l'utilisateur demande des images : l'ordre de recherche (bibliothèque OCTO, decks OCTO existants, Wikimedia Commons sous licence libre, capture, emplacement « Image à insérer »), les outils, la pose dans la charte (`photo`, `photo_fit`, `image_slot`) et la slide de crédits.
- `scripts/octo_slides.py` : classe `Deck` avec des helpers prêts à l'emploi (layout, cover, chapter, focus, toc, closing, slide, blank, panel, bloc, goutte, steps, tracker, separator, rule, connect, arrow, arrow_path, chevron, loop_back, fan, fork, join, cycle, pyramid, nested, lane, bar, medaillon, capsule, tab_card, numero, target_dot, statement, band, banner, chat, card, column, box, titled_box, container, window, chip, label, why_panel, pillar_card, timeline, takeaway, quote, persona, picto, photo, photo_fit, image_slot, circle, text, table, kpi, notes ; fonction `bloc_height`) et les constantes de la palette (`NAVY`, `NAVY_10`…, `TURQ`, `TURQ_30`…). Markup texte : `**gras**`, `==mot-clé==` (gras ; turquoise seulement sur fond marine), `- ` en début de ligne pour une puce, `> ` pour une puce chevron turquoise. Les espaces insécables de la charte (avant « : ; ! ? % », dans les guillemets) sont posées d'office par tous les helpers, notes comprises : taper des espaces normales. Fonction `extract_text(path)` : texte d'un deck source (slides, groupes, tableaux, notes) en markdown, quand la matière fournie est un `.pptx`.
- `scripts/maquette.py` : mesure une maquette HTML (Chrome sans interface) et la traduit en pouces, teintes de la charte et `corners` de `bloc()`, pour la reproduire (`mise_en_page.md` §7).
- `scripts/render.py` : export PDF via Microsoft PowerPoint (AppleScript, macOS), ou LibreOffice à défaut (claude.ai, Claude Desktop, Linux ; rendu approximatif), d'une copie au nom unique, slides masquées rendues visibles, puis PNG par slide (150 dpi) + planches de 4, et contrôle du rendu (rendu périmé, police de substitution, textes superposés, texte hors slide, texte qui déborde de sa forme).
- `references/retours.md` + `scripts/retours.py` : le fichier de retours écrit à chaque livraison (`write` : texte de chaque slide repéré `[slide.élément]` sous sa capture, consignes `→`, remarques de design ; un fichier rempli est archivé, jamais écrasé) et la lecture des retours de l'utilisateur (`diff` : textes modifiés, consignes, remarques).
- `scripts/octo_lint.py` : contrôle géométrique et de lecture (bords presque alignés, écarts irréguliers, chevauchements, textes superposés, texte qui sort de son bloc, bloc à moitié vide, pastille du numéro de page, flèches dans le vide, qui partent de points voisins, à coude cranté ou sans tige, traits pointillés en biais, lead gras coupé sur deux lignes, mot seul en fin de paragraphe, image qui sort du coin arrondi de son bloc, contraste du texte sur son fond selon la matrice de la charte ; avec `target="gslides"`, ce que Google Slides ne rend pas), lancé par `save()` ; en ligne de commande sur un deck existant : `uv run --with python-pptx python <SKILL_DIR>/scripts/octo_lint.py deck.pptx [--gslides]`.
- `assets/template_octo.pptx` : template OCTO vide (layouts 01 à 99).
- `assets/pictos/*.png` : pictos du deck de référence (fusee, bouclier, marteau_juge, checklist_stylo, conteneur_grue, observabilite_360, avatar_*, logos technos logo_mlflow, logo_kubernetes…, num_1…num_6).
- `assets/pictos-octo/bichrome/`, `blanc/`, `marine/` : bibliothèque OCTO (bichrome sur fond clair, blanc sur fond marine, marine seul pour un support sobre ou imprimé ; `tools/import_pictos.py` intègre une nouvelle livraison de la Com) ; `assets/avatars/`, `assets/illustrations/`, `assets/logos/`. Dans la version claude.ai du skill, ces dossiers sont regroupés en planches d'images (`assets/atlas/`) : ne pas les chercher sur disque, `picto()` retrouve chaque visuel par son nom dans les deux cas. Toutes les déclinaisons n'existent pas pour chaque picto (par exemple pas de `blanc/journal`) : vérifier la colonne de `pictos-index.md` avant d'utiliser `blanc/<nom>` ou `marine/<nom>`. Tous s'insèrent par leur nom avec `picto="<nom>"` (ou `picto="blanc/<nom>"`, `picto="marine/<nom>"`).
- `assets/chapitre_visuel.png` : visuel par défaut des slides chapitre.
- `examples/*.py` + `assets/exemples/*.png` : slides de référence, script et rendu attendu (`vue_ensemble_piliers` : panneau et piliers ; `pipeline_preuves` : schéma pipeline avec preuves accrochées ; `schemas_types` : boucle de retour, éventail, cycle, Gantt ; `freins_leviers` : vue d'ensemble en blocs emboîtés, chevrons de transition ; `schemas_niveaux` : jonction puis fourche, pyramide et légendes, définitions emboîtées ; `pedagogie` : relevé annoté, même demande en bulles à chaque étape, mini-schéma par famille ; `style_filaire` : capsules à médaillon, cartes à onglet et visuel 3D en goutte, chaîne d'anneaux empruntée), construites sur des zones et sans alerte. **Le niveau de finition à atteindre** : les regarder avant de concevoir une slide du même genre, et partir de leur script.

## Déroulé : spec, plan, build

Trois étapes, chacune validée par l'utilisateur avant la suivante. **Proportionner** : pour 1 à 3 slides, la spec et
le plan tiennent en quelques lignes dans la conversation ; à partir d'environ 5 slides (ou sur demande), ils deviennent
des fichiers dans un dossier par deck, ce qui permet de reprendre, modifier et regénérer le deck plus tard :

```
docs/slides/<deck>/
├── spec.md      ← references/spec_template.md
├── plan.md      ← references/plan_template.md
├── build.py     ← le script de génération, régénérable
├── retours.md   ← fichier de retours de l'utilisateur (references/retours.md), écrit à chaque livraison
└── <deck>.pptx + render/
```

Sur claude.ai, les fichiers ne survivent pas à la conversation : y donner la spec et le plan en texte, que
l'utilisateur pourra recoller pour reprendre le deck.

### 1. Spec — comprendre avant de dessiner

- Lire la matière (texte d'article, notes, plan, ou deck existant lu avec `extract_text`).
- Remplir la spec (`references/spec_template.md`) : public, message clé, objectif, format et registre (récit / pitch
  ou détaillé, `style.md`), matière, contraintes. Ce qui manque devient une **question**, pas une supposition : le
  public et le message clé ne se devinent pas.
- Une demande d'**une** slide qui présente N éléments « en détail » (piliers, axes, offres) appelle la vue d'ensemble
  (`style.md` §6, slide type 11, exemple `examples/vue_ensemble_piliers.py`) : on garde la matière, on ne la résume pas.
- Une **maquette** fournie (page HTML d'un autre outil, capture, croquis) fixe le design : la noter dans la spec ;
  elle sera reproduite, pas recomposée (`mise_en_page.md` §7). Une demande de **variantes** (« propose-moi 3
  versions ») se note aussi : nombre de variantes, slides concernées.
- Une matière qui distingue des faits **vérifiés** et des faits **à confirmer** (statuts, dates de relevé, « de
  mémoire ») : reporter les seconds dans la section « Faits à confirmer » de la spec. Chacun y garde sa source et
  dit s'il est affiché ; la liste revient telle quelle à la livraison.
- Faire valider la spec. Si l'utilisateur a déjà tout donné (public, message, matière), la résumer en trois lignes
  et passer au plan.

### 2. Plan — une ligne par slide

**2a. Choisir le type de chaque slide** (`references/types_de_slides.md`). Avant toute composition, pour chaque
slide : son **rôle** (accrocher, constater, expliquer, raconter, comparer, prouver, chiffrer, décider, conclure),
la **structure** de son contenu (ordre, causalité, boucle, hiérarchie, opposition, grandeur), **si un schéma est
adapté** (test de `types_de_slides.md` : des relations nommables, des flèches qui disent quelque chose, lisible
sans légende ; sinon il serait décoratif), et le **type de slide** qui sert le mieux ce rôle, pesé sur trois critères : pédagogie (la forme suit la structure, une idée par
slide), impact (point focal évident), style (registre, schéma quand il y a un mécanisme, variété du deck). Noter le
pourquoi et l'alternative écartée. Le type découle du rôle, jamais du modèle disponible le plus proche.

**2b. Composer.**
- Une notion dont on ne voit pas la forme (ou une slide jugée « pas claire » par l'utilisateur) : chercher
  l'inspiration avant de composer (`references/images.md` §7, `scripts/inspiration.py` : mosaïques Bing Images des
  formes que d'autres ont trouvées), puis la redessiner avec les helpers ; noter la forme retenue dans le plan.
- Composer dans le style filaire des modèles (`modeles.md`, « Le style filaire OCTO ») : pour chaque slide, le plan
  dit quel élément des modèles elle réutilise (médaillons, capsules, onglets, visuel 3D en goutte, illustration au
  trait, composition empruntée) ; au moins une slide sur deux en réutilise un.
- Regarder les slides préformatées OCTO avant de composer : `assets/modeles/planche_01.png` (éléments graphiques :
  formes, trackers, bulles, séparateurs, flèches), `planche_04.png` (suggestions de mise en page : blocs emboîtés)
  et la planche de la partie qui correspond au contenu (`modeles_index.md`). Le plan **cite les modèles consultés**
  pour chaque slide (colonne Modèles du gabarit), qu'ils servent de point de départ ou seulement de référence.
- Écrire le plan (`references/plan_template.md`) : le fil du deck, les types retenus en 2a, puis pour chaque slide son titre-message et son
  **plan de composition** (`style.md`, « Intentions de design ») : point focal, dispositif de contraste, géométrie,
  variés d'une slide à l'autre, et son point de départ : composition libre avec les helpers, assets piochés dans les
  slides préformatées (`borrow` : visuels 3D, illustrations), modèle OCTO transformé quand sa structure colle
  exactement (tableau, Gantt, SWOT), layout du template pour les ruptures (couverture, sommaire, chapitre, focus,
  clôture).
- Cocher les vérifications du gabarit (titres-messages, variété, chiffres sourcés), puis faire l'**autocontrôle**
  (`references/controle_objectif.md`) : chaque slide sert-elle l'objectif du deck et remplit-elle son rôle ? Pour un
  deck pédagogique, est-elle compréhensible pour ce public ; pour un deck commercial, voit-on les enjeux et impacts
  pour le client ? Pour un public qui découvre le sujet (pédagogique, interne à une autre équipe), cocher aussi les
  vérifications pédagogiques du gabarit : chaque terme défini avant de servir, un exemple concret par idée à retenir,
  le message répété à la fin. Retravailler ce qui ne tient pas, puis faire valider le plan. Si
  l'utilisateur a donné le plan, le compléter (focal, contraste, géométrie) sans le réécrire.
- **Maquette fournie** : le point de départ de la slide est la maquette ; le plan dit seulement ce qui sera corrigé
  (couleur hors charte, texte trop petit, alerte prévisible).
- **Variantes** : pour chaque slide concernée, 2 ou 3 compositions qui diffèrent par au moins deux des trois
  critères (focal, contraste, géométrie), et pas seulement par une couleur ou un coin arrondi ; une ligne par
  variante dans le plan (A, B, C), avec ce qu'elle privilégie. Même matière, même titre-message.

### 3. Build — générer, rendre, relire

1. Écrire `build.py` (dans le dossier du deck, ou le scratchpad pour une slide isolée), une section par ligne du plan :
   ```python
   import sys, os
   sys.path.insert(0, "<SKILL_DIR>/scripts")
   from octo_modeles import ModeleDeck
   from octo_slides import CONTENT  # zones : references/mise_en_page.md
   d = ModeleDeck(target="gslides")       # Deck + modèles OCTO ; Deck(target="gslides") seul si aucun modèle n'est
                                          # utilisé ; target="pptx" si le deck reste dans PowerPoint
   m = d.modele(159)                      # partir d'un modèle, puis l'adapter (references/modeles.md)
   d.set_text(m, "13", "Titre-message")
   d.check(m)
   s = d.slide("Titre affirmatif", "Sous-titre qui dit le message.")
   corps, bas = CONTENT.bottom_band(0.6, gap=0.2)           # zones, jamais de coordonnées à la main
   for zone, coin, (titre, texte) in zip(corps.cols(3, gap=0), ["tl", "none", "br"], blocs):  # emboîtés
       d.bloc(s, *zone, corners=coin, title=titre, body=texte)
   d.takeaway(s, "Phrase de conclusion.", picto="chrono_vitesse", y=bas.y)
   d.save("deck.pptx")                    # affiche les alertes ⚠ (mise_en_page.md §4) : les corriger avant le rendu
   ```
   Maquette fournie : la mesurer d'abord (`scripts/maquette.py`, `mise_en_page.md` §7) et construire les zones à
   partir de ses mesures. Variantes : une slide par variante, à la suite, chacune décrite dans ses notes
   (`d.notes(s, "Variante B — focal : … ; contraste : … ; géométrie : …")`).
   Lancer avec `uv run --with python-pptx python build.py` si `uv` est disponible, sinon `python3 build.py` après
   `pip install python-pptx` (cas d'un bac à sable sans uv, comme claude.ai). Si un helper ne couvre pas un besoin,
   compose avec `box`, `text`, `arrow` et les constantes de couleur plutôt que d'inventer un nouveau style.
   Plusieurs flèches qui partent d'une même boîte ou arrivent dans une même boîte : `fork` / `join` (un seul tronc),
   jamais plusieurs `connect` ; une hiérarchie peu / beaucoup : `pyramid` ; des termes à introduire : `nested`.
2. Rendre (PowerPoint, ou LibreOffice à défaut, voir Points d'attention) :
   `uv run --with python-pptx --with pymupdf --with pillow python <SKILL_DIR>/scripts/render.py deck.pptx <dossier>`
   (sans uv : `pip install python-pptx pymupdf pillow` puis `python3`). Le rendu porte sur une copie : les slides
   masquées y sont visibles, et un PDF périmé (version en cache de PowerPoint) arrête le rendu au lieu d'être relu.
   Corriger ses alertes ⚠ (police, textes superposés, débordements), puis lire les planches `sheet_*.png` (et les
   `slide_NN.png` en cas de doute). Pour une retouche d'une slide, ne relire que son `slide_NN.png`.
3. Relire chaque slide avec cette grille, corriger, re-rendre :
   - titre sur une ligne (≤ 70 caractères), sans chevauchement avec le sous-titre ;
   - aucune alerte ⚠, ni à l'enregistrement ni au rendu (`mise_en_page.md` §4) : débordements, alignements, écarts,
     chevauchements, texte qui sort de son bloc, blocs à moitié vides, pastille du numéro de page, flèches dans le vide,
     dédoublées, à coude cranté ou sans tige, traits pointillés en biais, leads coupés, mots seuls, contrastes ;
   - traits et flèches nets (`mise_en_page.md` §5) : aucune liaison en biais, aucune pointe sans tige ou collée à la
     barre d'une jonction, aucun trait qui croise une courbe ; regarder les flèches sur le `slide_NN.png`, pas
     seulement sur la planche ;
   - le style des modèles : pictos dans des médaillons (jamais nus dans un texte), onglets et capsules au trait plutôt
     que des aplats, visuels 3D en goutte ; une slide qui n'est faite que de boîtes et d'aplats est à revoir ;
   - un ordre de lecture évident (un sens, porté par un axe, des flèches ou des numéros) ; un mécanisme qui a une
     forme est dessiné, pas réduit à des carrés de texte (`style.md`, intentions 9 et 10) ;
   - colonnes parallèles (numéro, titre, corps) : les corps partent de la même hauteur, sous le plus haut des titres ;
   - un même chiffre garde le même périmètre et la même date d'une slide à l'autre (« +2 400 tests backend » en
     slide 2, « 2 454 tests back, 871 front » en slide 7) ;
   - pictos alignés, de taille homogène sur une même slide ;
   - texte marine, aucun texte turquoise sur fond clair (seul le point final d'une slide message ou héros) ;
   - pas de capitales pour insister, pas d'italique (les espaces insécables sont posées par les helpers) ;
   - un lead en gras par bloc, pas de pavé ;
   - la liste « Vérification avant livraison » de `charte.md`.
   Puis refaire l'**autocontrôle** (`references/controle_objectif.md`) sur le rendu, slide par slide : ce qui est
   construit sert-il l'objectif du deck et de la slide, et passe-t-il auprès de ce public ?
   Un problème de fond (slide inutile, message mal porté, deux slides qui se ressemblent) se corrige dans le plan,
   puis on relance le build ; noter la décision dans `plan.md`.
4. Pour des variantes, livrer un tableau d'une ligne par variante (ce qu'elle privilégie, pour quel usage) et
   laisser l'utilisateur choisir ; ne garder ensuite que la variante retenue dans le deck.
   Pour une maquette, dire ce qui a été corrigé par rapport à elle.
5. Livrer le `.pptx` à l'emplacement demandé (par défaut le dossier du deck dans `docs/slides/`) et donner le
   chemin, avec une phrase sur ce qui reste à faire à la main (photo à insérer, chiffre à confirmer) et la liste
   « Faits à confirmer » de la spec, pour ceux qui sont affichés. Le `.pptx` est
   ensuite importé dans Google Slides par l'utilisateur : rappelle-lui de jeter un œil au résultat après import.
6. Écrire le **fichier de retours**, à chaque livraison, que l'utilisateur s'en serve ou non
   (`references/retours.md`) :
   `uv run --with python-pptx python <SKILL_DIR>/scripts/retours.py write deck.pptx <dossier du rendu>`.
   Il pose `retours.md` à côté du `.pptx` : le texte de chaque slide repéré `[slide.élément]` sous sa capture, à
   corriger sur place, des consignes `→` et des remarques de design. Un `retours.md` déjà rempli est archivé
   (`retours_v1.md`…), jamais écrasé. Une variante par fichier : un `retours.md` par `.pptx` (troisième argument).
   Sans rendu (ni PowerPoint ni LibreOffice), les captures manquent mais le fichier reste utilisable ; sur claude.ai,
   le donner à télécharger avec le `.pptx`. Dire en une phrase à l'utilisateur qu'il peut y faire ses retours.

### Reprendre un deck

Si un dossier de deck existe déjà (`spec.md`, `plan.md`, `build.py`), partir de lui : modifier la spec ou le plan
selon la demande, puis relancer `build.py`. Ne pas régénérer le deck de zéro.

Quand l'utilisateur fige une version (« enregistre cette version en V1 ») avant une refonte, la copier telle quelle
dans un sous-dossier (`v1/` : `build.py`, `spec.md`, `plan.md`, le `.pptx` renommé `<deck>_v1.pptx`, son rendu) ; la
version suivante se construit dans le dossier du deck, sous un nom à son numéro (`<deck>_v2.pptx`, `render_v2/`), et
`plan.md` dit ce qui change par rapport à la précédente.

Quand l'utilisateur a rempli `retours.md` (« retours faits »), lire ses retours avec
`uv run --with python-pptx python <SKILL_DIR>/scripts/retours.py diff retours.md deck.pptx`, avant de régénérer :
textes modifiés, consignes, remarques de design. Reporter chaque texte dans `build.py` (orthographe et charte
corrigées au passage, et signalées), traiter chaque consigne et remarque ou dire pourquoi non ; un texte réécrit qui
ne tient plus se resserre au plus près de sa formulation, signalé dans le nouveau fichier par
`→ Claude : votre version : « … »` sous l'élément. Puis build, rendu, relecture, et `retours.py write` : le fichier
rempli est archivé, un fichier neuf attend le tour suivant (`references/retours.md`).

Sur un retour slide par slide (« la 16 n'est pas claire, la 17 c'est que des carrés »), refaire ces slides, puis
relire aussi les autres avec le même œil : le défaut signalé (une jonction tordue, un trait en biais, une slide sans
schéma) existe souvent ailleurs dans le deck.

## Points d'attention

- La police Outfit doit être installée (`brew install --cask font-outfit`), sinon le rendu la remplace. Si PowerPoint tournait avant une installation de police, il faut le relancer. Pour vérifier : `pymupdf` → `page.get_fonts()` sur le PDF doit lister Outfit.
- Le rendu de référence passe par Microsoft PowerPoint. Sans lui (bac à sable de claude.ai ou Claude Desktop), `render.py` bascule seul sur LibreOffice (`soffice` ; s'il manque : `apt-get install -y libreoffice-impress`) et installe Outfit depuis `assets/fonts`. Ce rendu est approximatif : LibreOffice dessine mal les formes libres du gabarit (bulle de la couverture, pastille du numéro de page) et peut couper une ligne ailleurs. Ne corriger que les défauts nets du contenu ; ne jamais retoucher le gabarit ni raccourcir un texte (une date, un titre) pour ce seul rendu. Dire à l'utilisateur que la relecture s'est faite sur un aperçu LibreOffice. Ni PowerPoint ni LibreOffice : livrer le `.pptx` sans relecture visuelle et le dire.
- L'utilisateur ouvre souvent le deck dans PowerPoint entre deux rendus : PowerPoint refuse alors la copie de rendu (erreur -9074) ou ne répond plus (-1712). Après un nouvel essai qui échoue encore, lui demander de fermer la présentation, puis relancer.
- Images : la bibliothèque OCTO d'abord ; des images du web (Wikimedia Commons sous licence libre, captures) seulement si l'utilisateur demande des illustrations, avec une slide de crédits (`references/images.md`). Une page qui demande une vérification « humain » ne se contourne pas.
- Cible finale : Google Slides (import du `.pptx`). Reste sur les formes des helpers, qui passent l'import ; pas de SmartArt, d'effets ni d'animations. `target="gslides"` mesure le texte 5 % plus large (Slides ne coupe pas les lignes comme PowerPoint : un texte calé au plus juste y prend une ligne de plus) et `save()` signale ce que Slides ne rend pas : dégradé, ombre (y compris héritée du thème), 3D, graphique natif, SmartArt, SVG, texte réduit automatiquement, colonnes de texte, capitales par attribut, espacement des lettres, connecteur coudé, vidéo. Le rendu PowerPoint ne montre pas ces écarts : seul le contrôle les voit.
- PowerPoint est sandboxé : `render.py` passe la copie de rendu et le PDF par le conteneur de PowerPoint (`~/Library/Containers/com.microsoft.Powerpoint/Data/Documents`), où il n'a pas à demander « Accorder l'accès ». Le `.pptx` et le dossier de rendu peuvent donc être n'importe où (projet, scratchpad).
- Le premier export PowerPoint expire souvent : `render.py` réessaie, ne pas relancer en boucle à la main. S'il échoue
  encore, son message dit pourquoi (boîte de dialogue ouverte, fichier hors du projet) : ne pas quitter PowerPoint ni
  fermer les présentations de l'utilisateur pour forcer le passage.
- Une capture d'écran macOS est en profil Display P3 : ses pixels n'ont pas les valeurs de la charte (#00D2DD y lit
  #5FCFDB, #0E2356 y lit #132253) alors que le `.pptx` est juste. Pour une question de couleur ou de contraste, lire
  les couleurs dans le `.pptx` (le contrôle de contraste de `octo_lint.py` le fait), jamais sur la capture.
- Un deck source (matière fournie, deck de modèles) se lit avec `extract_text`, et ne se rend que sur les slides
  utiles, copiées dans un petit deck : le rendu d'un deck de plusieurs centaines de slides bloque PowerPoint (boîte
  de dialogue à fermer par l'utilisateur).
- Les faits (chiffres, dates, noms) viennent de la matière fournie. S'il en manque un, mets `[à compléter]` dans la slide plutôt qu'une valeur plausible.
- Après un ajout d'asset ou de modèle, `tools/check_assets.py` vérifie que tout est indexé dans `references/` ; après
  un changement de helper, régénérer `references/api.md` (`tools/api_doc.py`), ce que `check_assets.py` vérifie aussi.
- Pour une retouche de deck existant, ouvre-le avec `Presentation(path)` plutôt que le template, et ne modifie que les slides concernées ; puis lance `scripts/octo_lint.py` sur le résultat (les contrôles de `save()` ne passent que par `Deck`).
