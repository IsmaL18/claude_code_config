# Partir d'un modèle OCTO, puis l'améliorer

`assets/modeles_octo.pptx` contient 303 slides préformatées par la Com OCTO (charte 2026) : démarches, plannings, tableaux, matrices, SWOT, roadmaps, équipes, propositions financières, schémas… Elles sont dessinées sur la slide (formes, groupes, tableaux natifs) : c'est le meilleur point de départ pour une slide OCTO.

**Deux usages, par ordre de préférence :**
1. **Réservoir d'assets** : composer sa propre slide selon les intentions de `style.md` (« Intentions de design ») et y poser des éléments pris dans les modèles avec `d.asset(slide, "<id>", x, y, w)` (identifiants dans `assets_modeles.md` et la section « Le style filaire OCTO » ci-dessous) ou `d.borrow(slide, n, chemin, x, y, w=…)` — visuels 3D en goutte des intercalaires, illustrations, pictogrammes composés, frises, matrices. Visuels 3D disponibles (`assets/modeles/visuels_3d.png`) : 13 interface web, 40 outils de conception, 50 checklist, 64 écran et loupe, 71 cible et échelle, 83 barres de croissance, 101 longue-vue, 122 chevalet, 143 checklist papier, 158 micro, 181 écran de mise en page, 204 molécule réseau, 235 coche, 242 livres, 253 smileys de satisfaction, 282 donut et rapport, 290 profil utilisateur, 293 pouce levé (chemin `"2"` pour l'image de l'intercalaire, vérifier avec `show(n)`).
2. **Structure à transformer** : copier le modèle (`modele(n)`) quand sa structure colle exactement au besoin (tableau, Gantt, SWOT, matrice), puis le transformer franchement.

Les éléments graphiques de la Com (modèles 8 à 10 : formes, trackers, bulles, séparateurs, flèches) et ses suggestions de mise en page (modèles 41 à 49 : blocs emboîtés à grands coins arrondis) sont repris en helpers (`bloc`, `goutte`, `steps`, `tracker`, `separator`, `chevron`, `connect`) : voir `mise_en_page.md`. Les regarder (`assets/modeles/planche_01.png`, `planche_04.png`) avant de composer une slide sans modèle, et citer dans le plan les modèles consultés (colonne Modèles consultés de `plan_template.md`).

**Un modèle n'est jamais un formulaire à remplir.** On garde sa structure et ses formes signature, puis on l'adapte au contenu et on l'améliore, toujours dans la charte (`charte.md`).

## Le style filaire OCTO : réutiliser le vocabulaire des modèles

Les slides de la Com ont une signature reconnaissable : presque tout est **au trait** (contours marine fins, grands
rayons, beaucoup de blanc), les pictos sont posés **dans des médaillons cerclés**, les rubriques sont titrées par des
**onglets** posés sur le bord des cartes, un **point turquoise** marque les repères, et les visuels 3D vivent **dans des
gouttes** à fond turquoise. Les aplats sont rares : un bandeau marine, une carte turquoise, pas plus. Une slide qui
n'utilise que des boîtes et des aplats est juste, mais ne ressemble pas aux slides OCTO : composer d'abord avec ce
vocabulaire, puis ajouter les aplats qui portent le point focal.

| Élément des modèles | Modèles | Helper | Quand |
|---|---|---|---|
| Médaillon : picto bichrome dans un cercle au trait, pastille « 01 » en bas à droite | 98 à 100, 145, 156, 85 à 89 | `medaillon(s, cx, cy, d, picto=, number=)` | tout picto posé dans un contenu ; à cheval sur le bord d'une carte, ou en tête de colonne |
| Colonne pilule : capsule au trait, numéro en tête, médaillon en pied | 156, 157 | `capsule(s, *zone, title=, body=, picto=, number=)` | 3 à 6 étapes, familles, piliers côte à côte |
| Carte à onglet : onglet titre sur le bord haut, puce cible à cheval sur le bord gauche | 153 à 155, 87 à 92 | `tab_card(s, *zone, onglet, corps)` | rubriques empilées, étapes détaillées, plutôt qu'un bandeau plein |
| Numéro en goutte au trait, puce cible au pied, filet vers le texte | 97 | `numero(s, cx, y, n)` | démarche en étapes numérotées |
| Puce cible : anneau au trait, point turquoise | 97, 153, 96 | `target_dot(s, cx, cy)` | repère d'un jalon, d'un onglet, d'une légende |
| Visuel 3D en goutte turquoise | 13 à 24, 47 à 49, intercalaires | `asset(s, "<id>", x, y, w, h=, shape="goutte")` | ouverture de partie, slide récit, une idée forte (`assets_modeles.md`) |
| Illustration au trait (personnages, scènes) | 51, 52, 54, 55, 57, 117, 192, 195 | `picto("illustr-filaire-…")`, `asset(s, "<id>", …)` | slide récit, constat, intention ; en grand, à côté du texte |
| Guillemets marine « 66 / 99 » | 31 à 39 | `quote` + pictos guillemets | verbatim, témoignage |
| Onglets d'étapes, jalons sur pilule | 8 | `steps`, `tracker` | situer la slide dans une démarche |
| Blocs emboîtés à grands coins arrondis | 41 à 49 | `bloc` + `Frame.cols(gap=0)` | contenu en blocs |

### Compositions à emprunter telles quelles

Des schémas des modèles sont des groupes de formes : on les pose d'un bloc avec `asset(s, "<modèle>.<groupe>", x, y,
w)`, puis on écrit ou pose dessus (médaillons au centre des anneaux, textes dessous). Les recadrer en largeur (`w`)
garde leurs proportions.

| id | Composition | Usage |
|---|---|---|
| `185.0` | Chaîne de quatre anneaux, arcs turquoise et flèches (centres des anneaux à x + 1,12 + k × 1,855 pour w = 7,91) | démarche en quatre temps, facteurs liés |
| `182.0` | Boucle infinie DevOps (deux anneaux, textes et pictos à remplacer) | boucle continue entre deux mondes |
| `173.38` | Escalier de flèches montantes (taxonomie de l'analytique) | maturité croissante |
| `197.0` | Triangle à trois zones avec libellés | concept à trois composantes |
| `199.3` | Fleur de pétales autour d'un centre | facettes d'un concept, écueils |
| `195.3` | Maison (toit, piliers, socle) au trait | piliers d'une démarche |
| `161.0` | Cœur entouré de quatre domaines | concept central |

### Les visuels des modèles

`references/assets_modeles.md` indexe les 125 visuels que portent les modèles et que la bibliothèque n'a pas : 53
visuels 3D sur fond turquoise (robot et bulles, cible, longue-vue, checklist, ampoule…), 10 illustrations au trait,
19 pictos composés, 18 portraits photo et 21 logos (événements OCTO, labels RSE). Chaque visuel a un identifiant « modèle.chemin » et une
vignette numérotée sur `assets/modeles/visuels_NN.png`. Les pictos et illustrations que les modèles partagent avec la
bibliothèque (plus de 300 usages) ne sont pas répétés : `picto()` les pose par leur nom.

## Trouver le bon modèle

0. **Par sa forme** (la table ci-dessous) : `grep -i "pyramide\|boucle" <SKILL_DIR>/references/modeles.md`. Les extraits
   de l'index sont souvent du « Lorem ipsum » : la forme y est introuvable, d'où cette table.
1. Chercher dans `references/modeles_index.md` (titre, partie, extrait de texte) : `grep -i "planning\|roadmap" <SKILL_DIR>/references/modeles_index.md`.
2. Regarder la planche qui le contient : `assets/modeles/planche_NN.png`, avec NN = (n - 1) // 12 + 1, sur deux chiffres. Comparer 2 ou 3 candidats visuellement.
3. `d.show(n)` : liste des formes du modèle (chemin, type, position, fond, texte), pour savoir quoi modifier.

Les numéros des pages citées dans `catalogue.md` viennent du PDF de la Com et ne correspondent pas à `n` : toujours passer par cette table ou par `modeles_index.md`.

### Trouver un modèle par sa forme

Numéros `n` pour `modele(n)`, `show(n)` ou `borrow(…, n, …)` ; planche = (n - 1) // 12 + 1. Quand un helper reproduit la
forme, il est indiqué : partir du helper, et du modèle seulement comme référence (colonne Modèles consultés du plan).

| Forme | Modèles | Pour | Helper |
|---|---|---|---|
| Éléments graphiques : formes, trackers, bulles, séparateurs, flèches | 8, 9, 10 | composer sans modèle | `bloc`, `goutte`, `tracker`, `separator`, `connect` |
| Blocs emboîtés à grands coins arrondis (suggestions de mise en page) | 41 à 49 | tout contenu en blocs | `bloc` + `Frame.cols(gap=0)` |
| Intercalaires avec visuel 3D en goutte | 13, 40, 50, 64, 71, 83, 101, 122, 143, 158, 181, 204, 235, 242, 253, 282, 290, 293 | chapitre ; visuel à emprunter | `chapter`, `borrow` |
| Photo ou visuel + texte, bulle, encart | 17 à 37 | slide récit | layouts 63 à 70 |
| Verbatims, citations | 38, 39 | preuve, témoignage | `quote` |
| Executive summary, convictions, hypothèses | 51 à 63 | ouverture d'une proposition | — |
| Contexte et demande, démarche en cartes ou tableau | 65 à 82 | cadrage | — |
| Étapes numérotées en colonnes (gouttes, pictos ronds), 4 à 6 | 97 à 100, 157 | démarche, étapes | `goutte`, `steps` |
| Frise à pastilles le long d'une ligne | 145 | parcours court | `timeline` |
| Cartes numérotées 2 x 2, onglet numéro | 146, 147 | 4 points | `bloc` |
| Quatre quadrants autour d'un picto central | 148 | 4 facettes d'un sujet | — |
| Rangées numérotées à chevron, détail à droite | 149 à 152 | étapes détaillées | `chevron` |
| Blocs à onglet « Titre » | 153 à 155 | rubriques | `label` |
| Colonnes en pilules avec picto en pied | 156 | 5 piliers | `column` |
| Plannings, Gantt, calendriers, rétroplanning | 102 à 121 | planning | `lane`, `bar` |
| Tableaux natifs simples et croisés | 123 à 141 | comparer | `table`, `set_cell` |
| SWOT | 159 | constat | — |
| Progression en 3 temps (Shu-Ha-Ri) | 160 | montée en compétence | — |
| Un cœur entouré de 4 domaines | 161 | concept central | — |
| Avant / après (projet vers produit) | 162, 163 | changement | — |
| Grille de cartes 4 x 3, une carte marine | 164 | compétences, offres | `bloc` |
| Phases en colonnes : objectifs, activités, livrables | 165 | démarche | — |
| Processus à 6 phases avec boucle de retour | 166 | processus itératif | `loop_back` |
| Flux agile (Scrum), boucle de sprint | 169 | itération | `cycle`, `loop_back` |
| Venn deux mondes (métier / IT) | 170, 183 | binôme, recouvrement | — |
| Architecture en couches (layer cake) | 174 | couches | `nested`, `container` |
| Escalier montant (taxonomie) | 173 | maturité croissante | — |
| Tableau comparatif à en-tête marine | 178 | comparer des profils | `table` |
| Boucle DevOps (infini) | 182 | cycle dev / ops | `cycle` |
| Étapes en anneaux qui s'enchaînent | 184, 185, 223 | démarche itérative | — |
| Organigramme en cercles de regroupement | 186 | organisation | — |
| **Définitions emboîtées en escalier** | 187 | introduire des termes, du plus large au plus précis | `nested` |
| Échelle de maturité | 188 | auto-évaluation | — |
| Roadmap multi-stream | 189 | roadmap | `lane`, `bar` |
| Phases produit en cercles, courbe de cycle de vie | 190, 191 | cycle produit | — |
| Parcours sinueux (journée, route) | 192 à 194 | parcours illustré | — |
| Maison (toit, piliers, socle) | 195 | piliers d'une démarche | — |
| Baromètre | 196 | satisfaction | — |
| Triangle à 3 zones | 197 | concept à 3 composantes | — |
| Losange central, fleur autour d'un centre | 198, 199 | idéation, écueils | — |
| Encadré marine en nuage de mots | 200 | principes, valeurs | — |
| Courbe de Hype | 201 | maturité d'une techno | — |
| Matrices 2 x 2 ou 3 x 3, Wardley, gain / effort | 202, 203, 217, 218, 237 | prioriser | — |
| Donuts segmentés de 3 à 8 parts | 205 à 211 | répartition, cycle | — |
| Jauges en pourcentage | 212 à 214 | KPI | `kpi` |
| Radars | 215, 216 | multicritère | — |
| Barres, courbes | 219 à 222 | données | — |
| Pétales, étoile, anneau, cercle central | 224 à 228 | concept central et facettes | — |
| Entonnoir, cône | 229, 230 | filtrage, élargissement | — |
| **Pyramide à 3 niveaux, légendes alignées à droite** | 231 | hiérarchie : peu en haut, beaucoup en bas | `pyramid` |
| Cercles imbriqués (pourquoi, comment, quoi) | 232 | sens d'une démarche | — |
| Venn 3 cercles | 233 | recoupement de 3 notions | — |
| Ishikawa | 234 | analyse de causes | — |
| Fiche recommandation, référentiel en grille | 236, 238 | audit | — |
| Démarche en 3 temps sur ligne de temps | 239 | audit, cadrage | `timeline` |
| Cartes de convictions, principes à icônes | 240, 241 | principes | `bloc` |
| Kit canvas : lean canvas, persona, thèse, experience map, North Star, carte d'empathie | 243 à 252 | atelier | — |
| Équipe, contacts, charges, mini-bios | 254 à 281 | équipe | `persona` |
| Propositions financières, CV, fiche de référence | 283 à 295 | réponse à appel d'offres | — |

## Adapter et améliorer

Après `s = d.modele(n)` (copie du modèle, consignes internes « A adapter à sa situation » retirées) :

| Besoin | Outil |
|---|---|
| Réécrire un texte, style conservé | `d.set_text(s, "3.2", "**Lead.** Texte")` (`per_line=True` pour garder titre / corps ou niveaux de puces) |
| Remplir un tableau natif | `d.set_cell(s, "2", ligne, colonne, "texte")` |
| Retirer ce qui ne sert pas | `d.remove(s, "5", "6")` |
| Ajouter un élément de même nature (une carte, une étape) | `d.duplicate(s, "3", dx=2.3)` puis `set_text` sur la copie |
| Recaler, agrandir, réaligner | `d.move(s, "3", x=…, y=…, w=…, h=…)` ; `d.bounds(s, "3.1")` donne la position réelle d'une forme dans un groupe |
| Hiérarchie des aplats, mise en avant | `d.recolor(s, "0.0", fill=TURQ)` — refuse toute couleur hors charte |
| Remplacer une image par un visuel pertinent | `d.replace_picture(s, "4", "cible")` (picto, avatar, illustration, logo) |
| Piocher un élément d'un autre modèle | `d.borrow(s, 71, "2", 7.3, 3.0, w=1.9)` (position et largeur en pouces, proportions gardées) |
| Ajouter ce qui manque | tous les helpers de `Deck` : `picto`, `takeaway`, `kpi`, `arrow`, `chip`, `box`… |
| Caler le texte dans un bloc haut (les blocs des modèles sont prévus pour beaucoup de texte) | `d.get(s, "3").text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE`, ou raccourcir le bloc avec `move(h=…)` et utiliser la place libérée (conclusion, chiffre clé) |
| Vérifier | `d.check(s)` : couleurs hors palette, texte noir, italique, capitales, textes de gabarit (« Lorem ipsum », « Titre », « xxx ») |

**`remove` décale les numéros des formes suivantes** : faire toutes les suppressions en un seul appel, en dernier, avec les chemins lus dans `show(n)`.

### Ce qu'on attend comme amélioration

- **Le contenu commande la structure.** 5 étapes dans un modèle à 4 : dupliquer une colonne et réespacer ; 3 idées dans une grille de 4 : retirer une case et recentrer, plutôt que laisser une case vide ou inventer un 4e point.
- **Un titre-message**, pas le nom du modèle : « SWOT » devient « Un socle solide, deux chantiers à ouvrir d'ici l'été ». Sous-titre-chute dessous (`style.md`).
- **Hiérarchie par l'intensité du turquoise** : l'élément le plus important en turquoise plein, les autres en teintes claires, le reste en blanc cerné de marine. Corriger au passage les teintes hors palette des modèles (`#DAF6FA`, `#B1F1F2`, `#3FBDD0`… signalées par `check`).
- **Des pictos qui portent le sens** du contenu (`pictos-index.md`), à la place des pictos génériques du modèle ; un visuel ou une illustration là où le modèle met une photo d'exemple.
- **Une phrase de conclusion** (`takeaway`) ou un chiffre clé (`kpi`) quand la slide en a besoin, si le modèle n'en a pas.
- **Moins de texte que le modèle** : les modèles sont remplis de « Lorem ipsum » sur 6 lignes ; viser 2 lignes par bloc, lead en gras.
- **Combiner** : un tableau de modèle + un bandeau de `chip`, une frise de modèle + des `kpi`. Rester sobre : un schéma OCTO est à 80 % blanc et marine au trait.
- **Varier** : dans un même deck, ne pas reprendre le même modèle pour N slides de même rang ; chercher des modèles différents ou transformer franchement le même.

### Pièges connus

- **Couleurs cachées** : un modèle peut porter une couleur hors charte dans une forme sans texte visible (la courbe
  du modèle 201 est grise, `#3F3F3F`, jusque dans son paragraphe vide). `check(s)` donne le chemin de la forme ;
  `recolor(s, chemin, line=NAVY)` corrige le contour, et une couleur restée dans le texte se remplace dans le XML
  (`a:srgbClr`).
- **Repères posés sur une courbe** (modèle 201) : placer le point au creux ou sur le plateau, et relier sa boîte par
  un trait vertical qui ne croise pas la courbe (`mise_en_page.md` §5).

### Ce qu'on ne fait pas

- Laisser un texte de gabarit, une consigne interne, une case vide ou une photo d'exemple hors sujet.
- Garder des capitales ou de l'italique du modèle quand la charte les exclut (`check` les signale) : la charte prime sur le gabarit.
- Ajouter des couleurs, ombres ou dégradés hors charte, ou des formes étrangères au système OCTO.
- Reproduire les slides de la partie « événements » (Duck Conf, USI…) : retirées du deck, charte propre.

## Exemple

```python
from octo_modeles import ModeleDeck
from octo_slides import TURQ, TURQ_20, TURQ_50, NAVY_10

d = ModeleDeck()
d.show(159)                                    # SWOT
s = d.modele(159)
d.set_text(s, "13", "Partenariat OCTO × Anthropic : où nous en sommes")
d.set_text(s, "12", "Un **socle solide**, deux chantiers à ouvrir d'ici l'été.")
d.set_text(s, "0.3", "**Expertise agentique** reconnue\n**Réseau Accenture** pour le go-to-market")
# … idem pour les 3 autres quadrants
for g, color in {"0": TURQ_20, "6": NAVY_10, "3": TURQ, "9": TURQ_50}.items():
    d.recolor(s, f"{g}.0", fill=color)         # l'opportunité en avant, teintes de la charte
d.picto(s, "cible", 9.0, 0.35, 0.45)
d.check(s)
d.save("docs/slides/deck.pptx")                # seules les slides créées sont gardées
```

## Régénérer

Quand la Com publie une nouvelle version du deck : `tools/build_modeles.py "<Slides préformatées OCTO.pptx>"` (retire tutoriels, banques de visuels et événements, réencode les photos), puis `tools/index_modeles.py` (index + planches, rendu PowerPoint, quelques minutes).
