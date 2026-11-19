# Mise en page : zones, blocs emboîtés, formes de la Com

Ce fichier dit **comment poser** les éléments d'une slide. Ce qu'on pose (point focal, contraste, type de slide) se
décide avant, avec `style.md` et `types_de_slides.md`.

## 1. On découpe des zones, on ne pose pas de coordonnées

Une slide se construit en découpant une zone de départ, jamais en calculant des positions à la main : c'est ce qui
garantit des rangées de même hauteur, des colonnes aux mêmes bords et des écarts réguliers. Le module
`scripts/octo_layout.py` fournit les zones (`Frame`, un tuple `x, y, w, h` en pouces qui se passe à tous les helpers
avec `*zone`).

```python
from octo_slides import CONTENT, Frame
why, droite = CONTENT.cols([3.1, None], gap=0.25)          # 3,1 pouces, puis le reste
tete, reste = droite.top(0.25, gap=0.1)                     # intertitres, puis le corps
corps, bas = reste.bottom_band(0.95, gap=0.14)              # corps, puis un bandeau en bas
g = corps.grid(3, [2.05, 0.25, None], gap=(0.1, 0))         # 3 rangées : frein | chevron | levier
for (frein, chevron, levier) in g:
    d.bloc(s, *frein, title="…", body="…")
```

| Méthode | Résultat |
|---|---|
| `cols(spec, gap)`, `rows(spec, gap)` | colonnes ou rangées ; `spec` = un entier (parts égales) ou une liste de tailles fixes, `None` (part égale du reste), `"2fr"` (part pondérée) |
| `grid(rangées, colonnes, gap)` | cellules `[rangée][colonne]`, gap = un écart ou (entre rangées, entre colonnes) |
| `top(h, gap)`, `bottom_band(h, gap)`, `left(w, gap)`, `right_band(w, gap)` | une bande et le reste |
| `pad(…)`, `place(w, h, align="mc")`, `move(dx, dy)`, `union(…)` | marge intérieure, zone posée dans une autre, décalage, zone qui couvre plusieurs cellules |

Zones de départ :
- `CONTENT` : x 0,6 → 9,2, y 1,3 → 5,2. Le bord droit s'arrête en 9,2 parce que la pastille du numéro de page occupe
  le coin bas droit (`PAGE_NUMBER`).
- `CONTENT_WIDE` : x 0,6 → 9,5, y 1,3 → 5,05, pour une slide qui a besoin de toute la largeur.
- Une vue d'ensemble avec panneau « why » part de deux zones : `Frame(0.4, 1.3, 3.1, 4.0)` pour le panneau, le reste
  à droite (exemple : `examples/freins_leviers.py`).

Les intertitres de colonnes se posent dans les colonnes de la même découpe que le corps (`tete.cols(spec)` avec le
même `spec`) : ils tombent ainsi exactement au-dessus de leur colonne.

Dans des colonnes parallèles (numéro, titre, corps), un titre qui passe sur deux lignes décale son corps : mesurer
d'abord le plus haut des titres, puis faire partir tous les corps de la même hauteur.

```python
title_h = max(text_height(f"**{t}**", z.w, 14, line_spacing=1.1) for z, t in zip(colonnes, titres))
```

## 2. Emboîter plutôt qu'espacer

Les suggestions de mise en page de la Com (modèles 41 à 49, `assets/modeles/planche_04.png`) ne posent pas des
boîtes séparées par des espaces : leurs blocs **se touchent et partagent leurs bords**, en escalier ou en puzzle, et
un picto ou une goutte se pose à cheval sur la jonction. C'est la signature OCTO à reproduire.

- Des éléments d'un même ensemble (les parties d'une offre, les soutiens et l'appel à décision) : zones voisines sans
  écart, `cols(…, gap=0)` ou `rows(…, gap=0)`, et un grand coin arrondi qui varie d'un bloc à l'autre (`corners`).
- Un passage d'un élément à un autre (un frein et sa réponse, un avant et un après) : un écart étroit portant un
  chevron turquoise `chevron()`, pas une flèche.
- Un flux (un ordre, une cause, un retour) : là seulement, des boîtes séparées et des flèches `connect(a, b)`.
- Plusieurs colonnes de texte dans un même bloc, séparées par un filet vertical fin (`rule`), plutôt qu'un bloc par
  colonne.

## 3. Les formes de la Com

Relevées dans les modèles 8 à 10 (« Éléments graphiques ») et 41 à 49 : contour marine 0,75 pt, fond blanc ou teinte
de la charte, grands rayons.

| Helper | Forme | Usage |
|---|---|---|
| `bloc(s, *zone, corners=…, radius=0.45, fill=…, title=…, body=…, picto=…)` | rectangle à un ou deux grands coins arrondis (`"tl-br"`, `"tr-bl"`, `"tl"`, `"tr"`, `"bl"`, `"br"`, `"top"`, `"bottom"`, `"all"`, `"none"`) | la forme de base de tout contenu ; titre gras et corps posés dedans |
| `goutte(s, x, y, d, corner=…, text=…, picto=…)` | cercle dont un coin reste carré | un picto, un numéro ou un mot ; plusieurs gouttes qui se touchent forment une chaîne |
| `steps(s, x, y, ["Cadrer", "Construire", "Opérer"], active=1)` | onglets à coins opposés arrondis, l'onglet actif en marine | situer la slide dans une démarche |
| `tracker(s, x, y, w, 1, "Collecte", active=True)` | goutte « 1. » sur une pilule gris clair | jalons numérotés, faits ou à venir |
| `separator(s, x, y, w, kind=…)` | `"accent"` (barres marine + turquoise courtes), `"line"`, `"dots"`, `"bold"` | ouvrir une rubrique, séparer deux parties |
| `rule(s, x1, y1, x2, y2)` | filet fin gris | séparer des colonnes dans un bloc, relier un picto à son bloc |
| `chevron(s, x, y, size)` | « > » turquoise | transition entre deux blocs |
| `connect(s, a, b)`, `arrow_path(s, points)`, `loop_back(s, points)` | flèches du modèle 10 (tige à bouts ronds, chevron ouvert) | flux, boucle de retour |
| `fork(s, src, [a, b])`, `join(s, [a, b, c], dst)` | un seul tronc, puis une branche par boîte (ou l'inverse), toutes au même point de départ | une boîte qui mène à plusieurs autres, plusieurs qui mènent à une : jamais plusieurs `connect` depuis une même boîte |
| `pyramid(s, *zone, niveaux, heights=…)` | pointe et trapèzes sur une même pente (modèle 231) ; renvoie `.tiers`, `.cut(i)`, `.edge(y)` pour poser légendes et filets | hiérarchie : peu en haut, beaucoup en bas |
| `nested(s, *zone, niveaux, dx=…, dy=…)` | blocs emboîtés en escalier, alignés à droite et en bas (modèle 187) | introduire des termes, du plus large au plus précis |
| `banner(s, *zone, texte, fill=NAVY, picto=…)` | bloc plein, picto à gauche, texte centré verticalement | la phrase à retenir, une analogie, une ambition, en bas de slide |
| `chat(s, x, y, w, [("Vous", …), ("Le modèle", …)])` | bulles : la demande à droite sur gris pâle, la réponse à gauche sur blanc | montrer par l'exemple ce que répond un modèle ; `heights=` aligne les bulles de plusieurs colonnes |
| `circle(s, cx, cy, r)` | cercle | points d'un nuage, neurones, billes et jalons des mini-schémas |
| `photo`, `photo_fit`, `image_slot` | images découpées selon la charte, emplacement « Image à insérer » | `images.md` |

`bloc_height(w, title, body, …)` (fonction du module) donne la hauteur d'un `bloc` ajustée à son texte : pour un bloc
sans vide en bas, ou N blocs côte à côte à la hauteur du plus rempli.

`box` (petits coins arrondis) reste la boîte des schémas techniques (architecture, pipeline) ; `card`, `column`,
`band` restent disponibles, mais un contenu qui n'est pas un schéma se pose d'abord en `bloc`.

Hiérarchie des aplats inchangée (`charte.md`) : un seul aplat marine par slide, le turquoise plein pour l'élément clé
(un appel à décision, la réponse), les teintes claires (`TURQ_20`, `NAVY_10`) pour un groupe, le blanc cerné de marine
pour le reste. Sur un fond turquoise, les puces passent en marine d'elles-mêmes.

## 4. Les contrôles : corriger les alertes avant de livrer

Deux contrôles automatiques voient ce qu'une planche de rendu cache (un écart de 0,03 pouce, un texte qui touche un
filet). Leurs alertes commencent par « ⚠ slide N » ; elles se corrigent toutes, puis on relance.

**À l'enregistrement** (`save()`, sur toutes les slides créées ; aussi `scripts/octo_lint.py deck.pptx` sur un deck
existant, sans le modifier). Le texte y est mesuré avec la police Outfit (`assets/fonts/`), comme PowerPoint : même
retour à la ligne, même pas de ligne (étalonné sur un rendu réel, `evals/etalonnage_texte.py`).

| Alerte | Correction |
|---|---|
| texte trop long pour sa forme | raccourcir le texte (2 lignes par bloc) ; élargir la colonne qui coupe un titre en deux ; agrandir la rangée en réduisant une autre zone ; baisser la police en dernier, jamais sous 7 pt hors vue d'ensemble |
| bords presque alignés (écart de 0,01 à 0,06) | les deux blocs doivent venir d'une même découpe (`cols`, `rows`, `grid`) : même rangée, même hauteur |
| écarts irréguliers | un seul `gap` pour toute la suite |
| chevauchement partiel | emboîter (bords partagés, `gap=0`) ou séparer |
| textes superposés | deux zones de texte l'une sur l'autre : découper la zone |
| recouvre la pastille du numéro de page, sort des marges ou de la slide | partir de `CONTENT` (bord droit en 9,2) ou `CONTENT_WIDE` (bas en 5,05) |
| flèche sans forme à son départ ou à son arrivée | `connect(a, b)` entre les deux formes |
| deux flèches partent (ou arrivent) de points voisins | une seule fourche : `fork(src, [a, b])` ou `join([a, b], dst)` |
| texte qui sort de son bloc | une zone de texte posée dans un bloc (chiffre clé et légende dans une boîte) dépasse : agrandir le bloc, raccourcir le texte |
| texte sous 6 pt | trop de texte : couper ou répartir |
| bloc à moitié vide | le contenu s'arrête haut et laisse un vide en bas : hauteur du bloc mesurée sur son texte (`text_height`), le blanc va entre les groupes, pas dans le bloc |
| flèche à coude cranté | flèche tracée par une ancienne version d'`arrow_path` : régénérer le deck |
| flèche sans tige | la pointe est posée seule : écarter les boîtes (0,45 pouce au moins) ; pour une jonction, `trunk` de 0,35 au moins et 0,8 pouce entre sources et cible ; pour un cycle, agrandir `rx` / `ry` |
| fourche ou jonction trop serrée, décentrée | 0,8 pouce entre la barre et les boîtes ; cible centrée sur les sources ; sinon regrouper les sources dans un `container` et une seule flèche (§5) |
| trait pointillé en biais | liaison horizontale, verticale ou en angle droit (deux `rule`), ou relier par un numéro |
| lead gras coupé sur deux lignes | élargir la colonne (part plus grande dans `cols`, par exemple `["1.15fr", None, …]`) ou raccourcir le lead |
| mot seul en fin de paragraphe | reformuler pour que la dernière ligne garde deux mots (« la marge du / mois » → « la meilleure / marge du mois »), ou élargir |
| image qui sort du coin arrondi | marge de l'image dans son bloc ≥ 0,36 × rayon (`bloc.pad(0.36 * radius)`), ou rayon plus petit |
| contraste insuffisant | la matrice de `charte.md` : marine sur fond clair et sur turquoise, blanc (ou turquoise pour un chiffre) sur marine |

Le texte d'un modèle OCTO laissé tel quel n'est pas contrôlé ; il l'est dès qu'il est réécrit (`set_text`) ou déplacé
(`move`).

**Au rendu** (`render.py`, sur le PDF exporté par PowerPoint, là où le texte est vraiment placé) : rendu périmé (le
PDF ne contient pas le texte du deck : arrêt), police de substitution (Outfit absente, ou caractère absent d'Outfit
rendu dans une autre police), lignes de texte superposées, texte hors de la slide, texte qui déborde de sa forme.

Pour dimensionner une colonne d'après son contenu : `text_width("**Titre du bloc**", 8)` donne la largeur d'un titre
sur une ligne, `text_height(texte, w, taille)` la hauteur d'un texte dans une largeur. `d.text(…, h=None)` ajuste la
hauteur de la zone au texte.

## 5. Traits et flèches nets

Un trait de travers ou une flèche réduite à sa pointe se voient tout de suite à la projection (« ce genre de chose
pas droites, c'est sale ») ; le contrôle les signale, mais ils s'évitent dès la composition.

- **Liaisons droites** : un trait qui relie un repère à sa boîte, une piste à ses blocs, une légende à un point est
  horizontal, vertical ou en angle droit. Si l'alignement est impossible (une piste de durées inégales au-dessus de
  quatre blocs égaux), relier par un numéro (« 1 · 15 min » dans la piste, goutte « 1 » sur le bloc). Un trait ne
  croise jamais une courbe : poser le repère là où le trait vertical reste libre (au creux d'une courbe, pas sur sa
  pente).
- **Flèches avec une tige** : 0,45 pouce au moins entre deux boîtes reliées, sinon seule la pointe apparaît.
  Plusieurs boîtes empilées et reliées : prévoir l'écart dans la découpe (`rows(4, gap=0.45)`), pas 0,25.
- **Jonctions** (`join`) : 0,8 pouce entre les sources et la cible, tronc final de 0,35 à 0,4 pouce (`trunk=`) pour
  que la pointe ne touche pas la barre ; la cible centrée sur la source du milieu (aligner leurs zones). Deux sources
  côte à côte au-dessus d'une cible : pas de jonction, mais les deux sources dans un `container` pointillé avec un
  « + » entre elles, puis une seule flèche droite (`connect(container, cible)`).
- **Boucles de retour** : le dernier tronçon, qui porte la pointe, garde lui aussi 0,4 pouce.
- Les arêtes d'un schéma oblique par nature (entrées d'un neurone, réseau de neurones, flèches d'un cycle) restent
  obliques : ce sont des formes, pas des liaisons.

## 6. Tailles

Les modèles de la Com écrivent gros et peu : message 20 à 30 pt, titre de bloc 12 à 20 pt, corps 10 à 12 pt.
Une slide récit ou détaillée garde le corps à 9 pt au moins ; seule la vue d'ensemble, qui reprend la matière presque
intégralement, descend à 7 pt (6 pt au plus bas, titres de bloc 8 pt). Si le texte ne tient pas à ces tailles, il y a trop de texte :
couper ou répartir sur deux slides.

## 7. Partir d'une maquette

Quand l'utilisateur fournit une maquette (une page HTML produite par un autre outil, une capture, un croquis), elle
**fixe le design** : on la reproduit en `.pptx` éditable, on ne la recompose pas. On garde sa structure, ses
proportions, sa hiérarchie et ses textes ; on ne corrige que ce qui sort de la charte (couleur, police, texte
turquoise sur fond clair) ou ce qui déclenche une alerte, et on dit à l'utilisateur ce qui a été corrigé.

**Maquette HTML** : la mesurer, plutôt que l'estimer à l'œil.

```bash
uv run --with python-pptx python <SKILL_DIR>/scripts/maquette.py maquette.html <dossier>
```

`maquette.md` donne un élément par ligne, en pouces sur la slide : position, taille, fond et contour ramenés à la
teinte de la charte la plus proche (⚠ quand la couleur est loin de la charte), coins arrondis déjà traduits en
`corners` de `bloc()` (« tl-br », « tr », « goutte »…), texte avec sa taille en pt, sa graisse et son balisage
`**gras**`. `maquette.png` est la capture, à mettre à côté du rendu du `.pptx` pour comparer.

Passer des mesures aux zones :
- repérer la grille de la maquette (colonnes, rangées, écarts) et la redécouper avec `cols`, `rows`, `grid` : des
  bords que la maquette aligne à quelques centièmes près deviennent une même découpe, avec un seul écart ;
- chaque forme mesurée devient un `bloc` (coins `corners`, rayon `r`), une `goutte`, une étiquette `label`, un
  `chevron`, une flèche `connect` ; chaque texte, le texte du bloc ou une zone `text` ;
- garder les tailles de texte mesurées, arrondies au demi-point, et les remonter si elles tombent sous les minima du
  §6 ;
- rendre, puis comparer le rendu à `maquette.png` : mêmes masses, mêmes alignements, même point focal.

Sans navigateur (claude.ai), lire le HTML et sa CSS directement : une page de 1280 px de large donne 0,0078 pouce par
pixel (10 / 1280), une police de 16 px y fait 9 pt.

**Capture ou croquis** : relever les masses et la grille à l'œil, au dixième de pouce, puis même démarche.
