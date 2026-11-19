# API des scripts La Grosse Conf (générée)

Générée par `tools/api_doc.py` depuis les docstrings : signature et première phrase. Lire ce fichier au lieu des scripts ; ouvrir un script seulement pour un détail qui manque ici.

```python
import sys; sys.path.insert(0, "<SKILL_DIR>/scripts")
from grosse_conf_slides import GrosseConfDeck, CONTENT, ANTHRACITE, RED, PINK   # d = GrosseConfDeck()
from grosse_conf_modeles import ModeleGrosseConfDeck   # d = ModeleGrosseConfDeck() : + modèles de la conf
```

Markup des textes : `**gras**`, `==mot-clé==` (rose sur fond anthracite seulement), `\n` retour à la ligne, `- ` puce. Espaces insécables posées d'office (`typo`). Tout est en pouces ; slide de 10 x 5,625.

## Zones (`octo_layout.Frame` ; `CONTENT` dans `grosse_conf_slides`)

Zones de départ : `CONTENT = (0.62, 1.4, 8.55, 3.6)`.

- `zone.cols(spec, gap=0.2)` : Colonnes côte à côte, de même hauteur.
- `zone.rows(spec, gap=0.2)` : Rangées empilées, de même largeur.
- `zone.grid(rows, cols, gap=0.2)` : Grille [rangée][colonne] : toutes les cellules d'une rangée ont la même hauteur et toutes celles d'une colonne les mêmes bords.
- `zone.pad(left, top=None, right=None, bottom=None)` : Zone intérieure : pad(0.2) sur les quatre côtés, pad(0.2, 0.1) horizontal / vertical, ou les quatre.
- `zone.top(h, gap=0)` : (bande du haut de hauteur h, reste de la zone sous la bande et l'écart).
- `zone.bottom_band(h, gap=0)` : (reste de la zone au-dessus de la bande et de l'écart, bande du bas de hauteur h).
- `zone.left(w, gap=0)` : (bande de gauche de largeur w, reste à droite).
- `zone.right_band(w, gap=0)` : (reste à gauche, bande de droite de largeur w).
- `zone.place(w=None, h=None, align='tl')` : Zone de taille w x h posée dans celle-ci : align = deux lettres, t / m / b puis l / c / r ("mc" : centré).
- `zone.move(dx=0, dy=0)` : Même zone, décalée de dx vers la droite et de dy vers le bas.
- `zone.union(*others)` : Plus petite zone qui contient celle-ci et les autres (un bloc qui couvre deux cellules d'une grille).

## Mesure du texte et typographie (`octo_layout`)

- `text_width(text, size, bold=False)` : Largeur (pouces) de la plus longue ligne d'un texte balisé, sans retour à la ligne automatique.
- `text_height(text, w, size, bold=False, line_spacing=None, margins=(0.08, 0.04), space_before=0)` : Hauteur (pouces) qu'occupe un texte balisé dans une boîte de largeur w, marges internes comprises (par défaut celles de Deck.text).
- `wrap(text, w, size, bold=False)` : Lignes affichées d'un texte balisé dans une largeur utile w (pouces), retour à la ligne aux espaces comme PowerPoint.
- `lines_of(text)` : Lignes d'un texte balisé, typographie appliquée (typo).
- `typo(text)` : Typographie française de la charte, appliquée à tout texte posé par les helpers : espace insécable avant « : ; !

## Helpers communs (`deck_base.BaseDeck`, hérités par GrosseConfDeck)

Texte, formes de base, flèches, images, notes et enregistrement ; leurs couleurs par défaut sont celles de la charte du deck.

- `d.notes(slide, text)` : Notes de l'orateur de la slide (texte brut) : le discours, ou la description d'une variante (« Variante B — focal : le chiffre ; contraste : un seul aplat ; géométrie : 3 colonnes »).
- `d.text(slide, x, y, w, h, text, size=10, color='auto', align='left', anchor='top', bold=False, line_spacing=None)` : Zone de texte balisé.
- `d.statement(slide, text, y=1.6, h=2.4, size=24)` : Grosse phrase-message centrée, en gras ; si elle finit par un point, il prend la couleur POINT.
- `d.arrow_path(slide, points, loop=False, weight=4, head=True)` : Flèche le long d'une ligne brisée (pouces) : tronçons à bouts ronds, chevron sur le dernier point, couleur de flux de la charte (FLOW).
- `d.arrow(slide, x1, y1, x2, y2, elbow=True, dash=False, both=False, loop=False, weight=4)` : Flèche de flux épaisse à chevron ouvert (couleur FLOW de la charte) ; loop=True : boucle de retour (LOOP) ; dash=True : lien secondaire en pointillés fins, petite pointe ouverte.
- `d.chevron(slide, x, y, size=0.16, direction='right', color='auto')` : Chevron de transition « > » entre deux blocs : pointe en (x, y), size = hauteur en pouces, couleur CHEVRON de la charte par défaut.
- `d.connect(slide, a, b, gap=0.06, dash=False, loop=False, weight=4)` : Flèche de la boîte a vers la boîte b, de bord à bord.
- `d.seg(slide, x1, y1, x2, y2)` : Tronçon de boucle de retour (LOOP), épais, sans pointe.
- `d.loop_back(slide, points)` : Boucle de retour en L ou en U : tronçons (LOOP) entre les points (pouces), pointe sur le dernier.
- `d.fan(slide, src, dsts, dash=False)` : Éventail : une flèche coudée d'un point source vers chaque point cible, ou de chaque point vers un même point cible si src est une liste et dsts un point.
- `d.fork(slide, src, dsts, gap=0.06, trunk=None, loop=False)` : Fourche : un seul tronc sort de la boîte src, puis une branche vers chaque boîte de dsts (une PR qui part en dev et en prod, une commande qui lance trois agents).
- `d.join(slide, srcs, dst, gap=0.06, trunk=None, loop=False)` : Jonction, l'inverse de fork() : une branche part de chaque boîte de srcs, elles se rejoignent en un seul tronc qui entre dans dst (trois preuves qui mènent à une conclusion).
- `d.picto(slide, name, x, y, size=0.6)` : Visuel de la bibliothèque du deck (VISUAL_DIRS) par son nom (sans .png), à la hauteur size.
- `d.photo(slide, image, x, y, w, h, shape='auto', anchor='mc', line='auto')` : Photo, capture ou une de presse qui remplit la zone, recadrée sans déformation et découpée : shape = "arrondi", "rond", "tl-br" (coins opposés arrondis), "goutte" ou "droit" (angles droits : charte Accenture…
- `d.photo_fit(slide, image, x, y, w, h)` : Image entière, proportions gardées, centrée dans la zone : un schéma ou une capture à lire en entier.
- `d.circle(slide, cx, cy, r, fill=(255, 255, 255), line='auto', line_w=0.75, dash=False)` : Cercle de centre (cx, cy) et de rayon r : point d'un nuage, neurone, jalon, bille d'un mini-schéma.
- `d.rule(slide, x1, y1, x2, y2, color='auto', width=0.75, dash=False)` : Filet fin : séparateur de colonnes (vertical), sous un intertitre (horizontal), ou lien d'un picto vers sa forme.
- `d.save(path)` : —

## GrosseConfDeck (`grosse_conf_slides`) : charte `charte_grosse_conf.md`

Palette : `ANTHRACITE`, `RED`, `PINK`, `RED_40`, `RED_30`, `RED_20`, `RED_10`, `PINK_BG`, `WHITE`, `descente(pct)`.

- `d.layout(name, texts=None, visuals=None)` : Slide sur un layout du template, désigné par son nom complet (« 51 - Focus ») ou une clé de LAYOUTS (« focus »).
- `d.cover(date, place, variant=1)` : Couverture : le logo de la conf et l'illustration sont dans le layout ; reste la date et le lieu (« 09.03.2027 I Maison de la Chimie »).
- `d.thematic(title, subtitle=None, note=None)` : Slide thématique : titre dans la grande fenêtre, sous-titre, et une note (date, lieu) dans la petite.
- `d.speaker(name, role, photo)` : Slide speaker : nom, titre du poste et entreprise, photo ronde (chemin d'un fichier).
- `d.chapter(title, number, visual=None)` : Intercalaire : onglet « 01 », titre dans la fenêtre.
- `d.toc(items, title='Sommaire.')` : Sommaire à pastilles « 01 »… (layouts 90 à 98), de 2 à 10 entrées.
- `d.focus(title, subtitle=None, body=None)` : Slide « focus » : grand cadre rose plein, pour un message clé ou le « pourquoi ».
- `d.slide(title, subtitle=None, subtitle_size=None)` : Slide de contenu : titre court qui finit par un point (rouge), sous-titre, zone libre CONTENT dessous.
- `d.blank()` : Slide vide : masque (sigle, mention légale, numéro de page) seul.
- `d.fenetre(slide, x, y, w, h, title=None, ombre=True, fill=(255, 255, 255), defilement=False)` : Fenêtre web, le composant signature : cadre au trait anthracite, deux pastilles (rouge pleine, vide) en haut à gauche, barre de titre, ombre rouge décalée.
- `d.onglet(slide, x, y, text='01', w=0.86, h=0.3)` : Onglet posé sur le bord haut d'une fenêtre (« 01 »), fond rose pâle, texte gras.
- `d.pastille(slide, x, y, text='01', d=0.5, fill=(255, 237, 242))` : Pastille carrée arrondie du sommaire (« 01 », « 02 »), fond rose pâle, texte gras anthracite.
- `d.tracker_gc(slide, x, y, w, number, text, h=0.33, active=True, size=11)` : Étape d'un tracker : pilule anthracite (étape en cours, texte blanc) ou pilule au trait (étape à venir), précédée de son numéro (« 1 »).
- `d.citation(slide, x, y, w, h, text, auteur, size=20)` : Citation : texte gras dans une fenêtre, auteur dans une étiquette rose sous la fenêtre.
- `d.chiffre(slide, x, y, w, value, label, size=40)` : Chiffre clé : valeur très grande en gras anthracite, point rouge, libellé dessous.
- `d.carte(slide, x, y, w, h, picto, title, body='', size=10, vertical=False, ombre=False)` : Carte au trait : picto de la conf, titre en gras et texte courts.
- `d.equation(slide, zone, termes, operateurs=None, h=1.5, size=24)` : Équation en pictos : un grand picto et son libellé par terme, des opérateurs entre eux (« Agent = Model + Harness »).
- `d.cible(slide, zone, niveaux)` : Cercles emboîtés (2 à 4 niveaux, du plus large au plus étroit) : un niveau qui en contient un autre.
- `d.radial(slide, zone, centre, gauche, droite, size=9)` : Un élément central (aplat rouge) relié par des flèches à des cartes de part et d'autre : ce qui l'entoure.
- `d.boucle(slide, zone, etapes, focal=2, size=12)` : Cycle en quatre cartes (2 x 2, sens horaire) reliées par des flèches, la dernière retournant à la première par une flèche rouge.
- `d.pipeline(slide, zone, etapes, focal=None, retour=None, size=10, card_h=2.0)` : Étapes côte à côte (cartes à picto en haut), reliées de gauche à droite ; retour : texte d'une boucle rouge de la dernière étape à la première.
- `d.grille(slide, zone, items, cols=2, gap=0.3, ombre_premiere=True, size=11)` : Grille de fenêtres à picto (échecs, causes, critères indépendants : rien à relier).
- `d.aplat(slide, x, y, w, h, text='', fill=(255, 0, 66), size=14)` : Aplat de schéma à coins légèrement arrondis.

Fonctions du module :

- `descente(pct)` : Descente du rouge à pct % (50, 40, 30, 20, 10) : le rouge mêlé de blanc, pour les illustrations et les fonds.
- `extract_text(path)` : Texte d'un deck source (slides + notes), en markdown, pour en tirer la matière d'un nouveau deck.

## ModeleGrosseConfDeck (`grosse_conf_modeles`) : modèles de la conf, en plus de tout GrosseConfDeck

- `d.show(n)` : Imprime les formes du modèle n (numéro de slide du deck de modèles, cf.
- `d.bounds(slide, path)` : Position et taille (pouces) d'une forme dans la slide, y compris à l'intérieur d'un groupe.
- `d.modele(n)` : Ajoute au deck une copie du modèle n, sans les consignes internes du gabarit.
- `d.borrow(slide, n, path, x, y, w=None)` : Pioche une forme, un groupe ou un visuel (photo 3D en goutte, illustration, frise, pictogramme composé) dans le modèle n et le pose sur la slide en (x, y) ; w redimensionne en gardant les proportions.
- `d.get(slide, path)` : —
- `d.set_text(slide, path, text, per_line=False, fit=False, color=None)` : Remplace le texte d'une forme en gardant son style (paragraphe et premier run).
- `d.keep(slide, *paths)` : Ne garde de la slide que les formes de premier niveau désignées (et les placeholders, dont le titre) : l'inverse de remove, pour un modèle dont on ne garde que quelques éléments.
- `d.set_cell(slide, path, row, col, text)` : Texte d'une cellule de tableau natif, style conservé.
- `d.remove(slide, *paths)` : Supprime des formes (les chemins se lisent avant suppression).
- `d.duplicate(slide, path, dx=0, dy=0)` : Copie une forme (ou un groupe) décalée de (dx, dy) pouces ; renvoie la copie.
- `d.move(slide, path, x=None, y=None, w=None, h=None)` : Déplace ou redimensionne une forme (pouces).
- `d.recolor(slide, path, fill=None, line=None)` : Change le fond et / ou le contour d'une forme.
- `d.replace_picture(slide, path, name)` : Remplace une image du modèle (picto, illustration, photo) par un visuel de la bibliothèque du deck, à la même place et à la même hauteur, proportions respectées.
- `d.check(slide)` : Signale les écarts à la charte : couleurs hors palette, texte noir, capitales, italique, textes de gabarit restants.
- `d.save(path)` : Enregistre en ne gardant que les slides créées (les modèles sont retirés).
