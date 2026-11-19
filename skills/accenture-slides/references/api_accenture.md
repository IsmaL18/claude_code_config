# API des scripts Accenture (générée)

Générée par `tools/api_doc.py` depuis les docstrings : signature et première phrase. Lire ce fichier au lieu des scripts ; ouvrir un script seulement pour un détail qui manque ici.

```python
import sys; sys.path.insert(0, "<SKILL_DIR>/scripts")
from accenture_slides import AccentureDeck, CONTENT, PURPLE, PURPLE_DARKEST, GREY_LIGHT  # d = AccentureDeck()
from accenture_modeles import ModeleAccentureDeck   # d = ModeleAccentureDeck() : + bibliothèque de visuels
```

Markup des textes : `**gras**`, `==mot-clé==` (lilas sur fond foncé seulement), `\n` retour à la ligne, `- ` puce violette. Police Arial ; `headline` pour l'Arial Black, `serif` pour le Palatino. Deck en anglais : `AccentureDeck(lang="en-US")`, sans typographie française. Espaces insécables posées d'office (`typo`). Tout est en pouces ; slide de 13,333 x 7,5.

## Zones (`octo_layout.Frame` ; `CONTENT` dans `accenture_slides`)

Zones de départ : `CONTENT = (0.42, 1.75, 12.5, 5.1)`, `SLIDE = (0, 0, 13.333, 7.5)`.

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

## Helpers communs (`deck_base.BaseDeck`, hérités par AccentureDeck)

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

## AccentureDeck (`accenture_slides`) : charte `charte_accenture.md`

Palette : `WHITE`, `PURPLE`, `PURPLE_DARK`, `PURPLE_DARKEST`, `MAUVE`, `LAVENDER`, `LILAC`, `LILAC_LIGHT`, `BLACK`, `GREY`, `GREY_LIGHT`, `WHITE`. Clés de layout : `LAYOUTS`.

- `d.save(path)` : Enregistre (voir BaseDeck.save).
- `d.text(slide, x, y, w, h, text, size=10, color='auto', align='left', anchor='top', bold=False, line_spacing=None)` : Zone de texte balisé (voir BaseDeck.text).
- `d.headline(slide, x, y, w, h, text, size=20, color=None, align='left', anchor='top')` : Intitulé en Arial Black (titre de carte, de colonne, chiffre) : la graisse de la marque pour les titres.
- `d.serif(slide, x, y, w, h, text, size=20, color=None, align='left', anchor='top')` : Texte en Palatino Linotype (sous-titre, accroche, citation), violet par défaut, lilas sur une slide foncée.
- `d.layout(name, texts=None, visuals=None, fit_title=1)` : Slide sur un layout du template, désigné par son nom complet (« Agenda ») ou une clé de LAYOUTS (« section_dark »).
- `d.cover(title, subtitle=None, date=None, author=None, variant='dark')` : Couverture : titre (Arial Black), sous-titre (Palatino), date et auteur ; le logo et le copyright sont dans le layout.
- `d.agenda(items, title='Agenda', intro=None)` : Sommaire numéroté (1 à 16 entrées, sur une ou deux colonnes) ; intro : accroche en Palatino sous le titre.
- `d.section(title, number=None, subtitle=None, style='dark')` : Intercalaire numéroté : grand numéro (Arial Black), titre, sous-titre en Palatino.
- `d.key_message(text, style='dark')` : Message clé seul sur la slide (Arial Black, 54 pt dans le layout).
- `d.slide(title, subtitle=None, dark=False)` : Slide de contenu : titre en Arial Black sur une ligne (réduit si besoin), sous-titre facultatif, zone libre CONTENT dessous.
- `d.blank(title=None, dark=False)` : Slide libre : masque (logo, copyright, numéro de page) et titre facultatif.
- `d.closing(text='Merci', gradient=False)` : Slide de fin : grand « > » de la marque et un mot (« Merci », « Questions ?
- `d.gt(slide, x, y, h, color=None)` : Le « > » de la marque (Greater Than), plein, de hauteur h : signature visuelle, ou flèche entre deux blocs.
- `d.chiffre(slide, x, y, w, value, label, size=54, color=None)` : Chiffre clé : valeur en Arial Black violette, libellé en dessous.
- `d.point(slide, x, y, w, h, number, title, body='', frame=True, size=12)` : Case numérotée façon starter pack (« 1.
- `d.point_height(w, title, body='', size=12)` : Hauteur d'une case point() à son contenu.
- `d.colonnes(slide, zone, items, numbered=True, size=13)` : Colonnes côte à côte (2 à 5) façon layouts « Columns » : numéro violet, intitulé en Arial Black, filet violet court, texte.
- `d.carte(slide, x, y, w, h, picto, title, body='', size=12, dark=None)` : Carte à icône : icône monoline violette (blanche si dark), intitulé en gras, texte court ; sans cadre, un filet violet sous l'icône.
- `d.aplat(slide, x, y, w, h, text='', fill=None, size=16, align='center')` : Aplat à angles droits.
- `d.etapes(slide, zone, items, focal=None, size=12)` : Processus linéaire : chevrons en gris clair (texte noir), l'étape focal en violet (texte blanc), un texte sous chaque chevron.
- `d.de_a(slide, zone, avant, apres, titre_avant="Aujourd'hui", titre_apres='Demain')` : Passage d'un état à un autre (« From issue to outcome » du starter pack) : panneau gris clair à gauche, grand « > » violet au centre, panneau violet foncé à droite (texte blanc).
- `d.citation(slide, x, y, w, h, text, auteur, size=28)` : Citation : texte en Arial Black, auteur en Palatino violet dessous, filet violet à gauche.
- `d.chiffres(slide, zone, items, size=54, gap=0.6)` : Rangée de chiffres clés (2 à 4) centrée dans la zone : valeur en Arial Black violette, libellé dessous.
- `d.matrice(slide, zone, axe_x, axe_y, quadrants, focal=None, graduations=('Faible', 'Fort'), size=13)` : Matrice 2 x 2 : quatre cases gris clair, la case focal en violet (texte blanc), axes nommés avec leurs graduations.
- `d.barres(slide, zone, items, focal=None, unit='', size=13)` : Barres horizontales dessinées (pas de graphique natif : Google Slides les rend mal) : libellé à gauche, barre gris clair proportionnelle à la valeur, la barre focal en violet, valeur au bout.
- `d.tableau(slide, zone, rows, widths=None, size=12)` : Tableau natif : en-tête violet foncé (texte blanc gras), lignes alternées blanc et gris clair, texte noir.

Fonctions du module :

- `extract_text(path)` : Texte d'un deck source (slides + notes), en markdown, pour en tirer la matière d'un nouveau deck.

## ModeleAccentureDeck (`accenture_modeles`) : bibliothèque de visuels, en plus de tout AccentureDeck

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
