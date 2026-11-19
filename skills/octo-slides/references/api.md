# API des scripts (générée)

Générée par `tools/api_doc.py` depuis les docstrings : signature et première phrase. Lire ce fichier au lieu des scripts ; ouvrir un script seulement pour un détail qui manque ici.

```python
import sys; sys.path.insert(0, "<SKILL_DIR>/scripts")
from octo_slides import Deck, CONTENT, Frame, NAVY, TURQ, TURQ_20  # d = Deck()
from octo_modeles import ModeleDeck                             # d = ModeleDeck() : Deck + modèles OCTO
```

Markup des textes : `**gras**`, `==mot-clé==` (turquoise sur fond marine seulement), `\n` retour à la ligne, `- ` puce, `> ` puce chevron turquoise. Espaces insécables posées d'office (`typo`). Tout est en pouces ; slide de 10 x 5,625.

## Zones (`octo_layout.Frame` ; `CONTENT` dans `octo_slides`)

Zones de départ : `CONTENT = (0.6, 1.3, 8.6, 3.9)`, `PAGE_NUMBER = (9.2, 5.05, 0.5, 0.35)`, `SLIDE = (0, 0, 10, 5.625)`.

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

## Helpers communs (`deck_base.BaseDeck`, hérités par Deck)

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

## Deck (`octo_slides`)

Palette (`charte.md`) : `WHITE`, `NAVY`, `NAVY_90`, `NAVY_80`, `NAVY_70`, `NAVY_60`, `NAVY_50`, `NAVY_40`, `NAVY_30`, `NAVY_20`, `NAVY_15`, `NAVY_10`, `NAVY_5`, `TURQ`, `TURQ_90`, `TURQ_80`, `TURQ_70`, `TURQ_60`, `TURQ_50`, `TURQ_40`, `TURQ_30`, `TURQ_20`, `TURQ_10`.

- `d.layout(number, texts=None, visuals=None)` : Slide sur un layout préformaté du template, désigné par son numéro ("05", "41", "65"…).
- `d.cover(title, subtitle, date, tag, variant=1)` : Couverture.
- `d.chapter(title, number, visual=None, variant=1, parts=None)` : Slide chapitre (layout 50, goutte ronde ; variant=2 : layout 51, goutte carrée).
- `d.focus(title, subtitle=None, body=None)` : Slide « focus » (layout 05) : cadre blanc sur fond #3E4F78, pour un message clé ou le « pourquoi ».
- `d.toc(items, title='Sommaire')` : Table des matières à pastilles goutte 01…n (layouts 90 à 98), de 2 à 10 entrées.
- `d.closing()` : Slide de clôture « There is a better way.
- `d.slide(title, subtitle=None, subtitle_size=None)` : Slide de contenu standard : titre (phrase affirmative) + sous-titre optionnel, zone libre dessous.
- `d.blank()` : —
- `d.box(slide, x, y, w, h, text='', header=False, size=8.75, fill=None, align=None)` : Boîte de schéma : coins légèrement arrondis, contour marine fin.
- `d.titled_box(slide, x, y, w, h, header, body, header_h=0.42, size=8.75, align=None)` : Boîte à en-tête turquoise + corps blanc (ex. Espace projet A / Registre MLflow...).
- `d.container(slide, x, y, w, h, label=None)` : Regroupement en pointillés (ex. 'la plateforme', un périmètre externe).
- `d.window(slide, x, y, w, h, title)` : Cadre façon fenêtre d'appli (fond gris pâle, 2 pastilles, titre à droite) : cluster, plateforme...
- `d.pyramid(slide, x, y, w, h, levels, heights=None, gap=0.1, size=11)` : Pyramide à niveaux (modèle OCTO 231) : une pointe en triangle puis des trapèzes, tous sur la même pente, séparés par gap.
- `d.nested(slide, x, y, w, h, levels, dx=0.55, dy=None, radius=0.35, size=10.5)` : Notions emboîtées en escalier (modèle OCTO 187, « A few definitions… ») : chaque niveau est un bloc posé dans le précédent, décalé de dx vers la droite et de dy vers le bas, tous alignés sur les bords droit et bas.
- `d.cycle(slide, cx, cy, labels, w=1.6, h=0.5, rx=2.2, ry=1.2, key=None, size=9.5)` : Cycle de N étapes posées sur une ellipse autour de (cx, cy), reliées par des flèches de flux ; la dernière flèche, qui ferme la boucle, est turquoise.
- `d.lane(slide, x, y, w, label, label_w=1.6, size=9)` : Couloir d'un Gantt ou d'une série temporelle de principe : libellé à gauche, filet pointillé marine.
- `d.bar(slide, x, y, w, text='', key=False, h=0.26, size=8)` : Barre de Gantt centrée sur le couloir y : pilule turquoise pâle, turquoise plein si key (charte : intensité du turquoise = priorité), contour marine fin.
- `d.image_slot(slide, x, y, w, h, subject, shape='tl-br')` : Emplacement d'une image à insérer, quand l'utilisateur le demande et qu'aucun visuel OCTO ni aucune image libre ne convient : bloc gris pâle, picto photo, « Image à insérer » et le sujet (shape="goutte" : petite…
- `d.bloc(slide, x, y, w, h, corners='tl-br', radius=0.45, fill=(255, 255, 255), line=(14, 35, 86), line_w=0.75, title=None, body=None, picto=None, pad=0.22, title_size=14, size=10, picto_size=0.45)` : Bloc OCTO : rectangle à grands coins arrondis, contour marine fin, la forme de base des suggestions de mise en page de la Com.
- `d.goutte(slide, x, y, d, corner='br', fill=(255, 255, 255), line=(14, 35, 86), line_w=0.75, text=None, picto=None, size=10)` : Goutte OCTO (modèles 8 et 44) : cercle de diamètre d dont un coin reste carré (corner : "tr", "br", "bl", "tl").
- `d.medaillon(slide, cx, cy, d=0.9, picto=None, number=None, text=None, fill=(255, 255, 255), size=10)` : Médaillon (modèles 98 à 100, 145, 156) : cercle au trait fin centré en (cx, cy), picto bichrome au centre (55 % du diamètre), et en option une pastille numérotée « 01 » à coins opposés arrondis, en bas à droite.
- `d.target_dot(slide, cx, cy, d=0.28)` : Puce cible (modèles 97, 153 à 155) : anneau au trait et point turquoise au centre ; repère d'un onglet, d'un jalon ou d'une étape.
- `d.numero(slide, cx, y, number, d=0.8, stem=0.6, size=16)` : Numéro d'étape au trait (modèle 97) : « 1.
- `d.tab_card(slide, x, y, w, h, tab, body=None, tab_w=None, tab_h=0.37, size=10, tab_size=10, fill=(255, 255, 255), radius=0.3)` : Carte à onglet (modèles 153 à 155) : onglet au trait posé sur le bord haut, qui porte le titre, une puce cible à cheval sur le bord gauche, et le corps au trait dessous (coin haut droit arrondi).
- `d.capsule(slide, x, y, w, h, title=None, body=None, picto=None, number=None, size=9.5, title_size=11, fill=(255, 255, 255))` : Colonne pilule (modèles 156, 157) : capsule au trait aux bouts entièrement arrondis ; en haut un numéro cerclé (number, modèle 157), puis le titre et le texte centrés ; en pied un médaillon (picto, modèle 156).
- `d.steps(slide, x, y, labels, active=0, w=None, h=0.34, gap=0.05, size=11)` : Onglets d'étapes (modèle 8, « Trackers ») : coins opposés arrondis, l'étape en cours en marine à texte blanc, les autres en blanc cerné de marine.
- `d.tracker(slide, x, y, w, number, text, h=0.33, active=True, size=11)` : Jalon numéroté (modèle 8) : goutte « 1.
- `d.separator(slide, x, y, w=1.0, kind='accent')` : Séparateurs de la Com (modèle 9) : "accent" (barre marine courte suivie d'une barre turquoise, pour ouvrir une rubrique), "line" (filet gris clair), "dots" (pointillés marine), "bold" (barre turquoise épaisse à bouts…
- `d.card(slide, x, y, w, h, lead, body, picto=None, size=10.5)` : Carte à coins diagonaux arrondis : lead en gras plus gros + explication.
- `d.column(slide, x, y, w, h, header, body, picto=None, header_h=0.44, size=9.5)` : Colonne : picto au-dessus relié par un filet, en-tête à coins hauts arrondis, corps encadré.
- `d.band(slide, x, y, w, h, lead, body, picto=None, size=10)` : Bande pleine largeur (liste de constats) : picto à gauche, lead en gras puis explication.
- `d.chip(slide, x, y, w, text, number=None, h=0.24)` : Pastille turquoise clair (brique, techno), avec numéro rond optionnel.
- `d.takeaway(slide, text, picto=None, y=4.6)` : Phrase de conclusion en bas de slide, en gras, avec picto à gauche.
- `d.banner(slide, x, y, w, h, text, fill=(14, 35, 86), picto=None, corners='tr', size=10.5, radius=0.3)` : Bandeau de message dans un bloc plein : ce qu'il faut retenir, une analogie, une ambition.
- `d.chat(slide, x, y, w, messages, size=8.5, gap=0.08, ratio=0.86, heights=None)` : Échange en bulles, pour montrer par l'exemple ce que répond un modèle : messages = [("Vous", texte), ("Le modèle", texte), …].
- `d.quote(slide, x, y, w, h, text, size=9, align='center')` : Verbatim entre guillemets typographiques, mots clés en gras.
- `d.persona(slide, x, y, picto, label, size=0.75)` : Avatar OCTO + étiquette dans un petit cadre arrondi.
- `d.label(slide, x, y, text, w=None, h=0.2, size=7.5, fill=(198, 241, 245))` : Étiquette pilule (« Ambition », « Le why ») : fond turquoise, texte marine gras.
- `d.panel(slide, x, y, w, h, tag=None, corner='tr')` : Zone foncée d'une slide contrastée : aplat marine à un grand coin arrondi (« tr » haut droit, « tl » haut gauche), étiquette pilule optionnelle.
- `d.why_panel(slide, x, y, w, h, statement, intro=None, bullets=(), tag='Le why', split=0.52, size=10.5, bullet_size=7)` : Panneau « why » d'une vue d'ensemble : aplat marine à grand coin arrondi en haut à droite, étiquette, phrase-ambition blanche avec ==mots-clés== turquoise, filet pointillé, puis puces chevron « lead.
- `d.pillar_card(slide, x, y, w, h, number, title, body, detail=None, picto=None, tag='Ambition', split=0.58, size=6, title_size=8.5)` : Carte de pilier d'une vue d'ensemble : onglet « .01 » posé sur le bord haut, titre gras sur 1 ou 2 lignes, picto en haut à droite, description, filet pointillé, étiquette (« Ambition ») et détail.
- `d.timeline(slide, items, y=2.6, x0=0.8, x1=9.3)` : Frise horizontale : flèche marine épaisse, jalons en anneaux turquoise, libellés alternés haut / bas.
- `d.table(slide, x, y, w, rows, col_widths=None, row_h=0.3, size=9)` : Tableau OCTO : en-tête marine (texte blanc gras), corps blanc à filets verticaux marine, lignes séparées en pointillés, bande turquoise en pied.
- `d.kpi(slide, x, y, w, value, label, size=28, dark=False)` : Chiffre clé : valeur Bold très grande + libellé Regular sur la même ligne, filet pointillé dessous.

Objet renvoyé par `d.pyramid` :

- `pyr.edge(y)` : Abscisse du flanc droit à l'ordonnée y (le flanc gauche est symétrique autour de cx).
- `pyr.cut(i)` : Ordonnée de la cassure entre le niveau i et le suivant : y poser un filet pointillé vers les légendes.

Fonctions du module :

- `bloc_height(w, title=None, body=None, title_size=14, size=10, pad=0.22, picto_size=0)` : Hauteur (pouces) d'un bloc() de largeur w ajustée à son titre et à son corps : pour un bloc sans vide en bas, ou pour donner à N blocs côte à côte la hauteur du plus rempli.
- `extract_text(path)` : Texte d'un deck source (slides + notes), en markdown, pour en tirer la matière d'un nouveau deck.
- `find_visual(name, dirs=None)` : Fichier d'un visuel OCTO par son nom.

## ModeleDeck (`octo_modeles`) : modèles OCTO, en plus de tout Deck

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
- `d.asset(slide, asset_id, x, y, w, h=None, shape=None)` : Pose un visuel des slides préformatées par son identifiant « modèle.chemin » (references/assets_modeles.md : visuels 3D, illustrations au trait, photos, pictos composés ; « 185.0 » pour un groupe, la chaîne d'anneaux…
