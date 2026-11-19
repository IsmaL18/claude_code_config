# Catalogue des mises en page OCTO

Deux parties : le gabarit officiel d'une slide (positions, pages structurantes, formes), puis la description des 321 slides préformatées, utile pour savoir quand utiliser quel type. **Les numéros de page de ce fichier sont ceux du PDF de la Com, pas ceux des modèles : pour copier un modèle, chercher son numéro `n` dans la table « Trouver un modèle par sa forme » de `modeles.md` (forme → numéros, helper qui la reproduit), ou dans `modeles_index.md`.** Commencer par les 10 slides types de `style.md` §6 ; venir ici quand aucune ne colle.

## Gabarit officiel

Source : « Slides préformatées OCTO 2026 » (Drive, Google Slides 16:9, 720 × 405 pt ; 1 pouce = 72 pt, soit 10 × 5,625 pouces dans `octo_slides.py`). Positions approximatives (± 3 pt) ; les convertir en pourcentages pour d'autres formats.
Choisir une mise en page dans `slides-catalogue.md`, puis regarder la page source avant de la reproduire.
En .pptx, le masque officiel est le modèle « OCTO » du Drive (Google Slides > À partir d'un modèle) : le recommander quand l'utilisateur peut éditer lui-même.

### Gabarit d'une page de contenu
| Élément | Position | Style |
|---|---|---|
| Sigle | haut gauche, x ≈ 22, y ≈ 23, ≈ 13 pt | `assets/logos/sigle-bichrome.png` (géré par le template) |
| Titre | x ≈ 44, ligne de base y ≈ 46 | Outfit Bold, marine, 18–22 pt, aligné à gauche, sans point final |
| Sous-titre | sous le titre, y ≈ 60–75 | Outfit Regular, marine, 12–14 pt ; mots-clés en gras |
| Zone de contenu | x ≈ 44 → 675 (6 → 94 %), y ≈ 65 → 383 | fond blanc |
| Numéro de page | bas droite, x ≈ 675–698, y ≈ 368–384 | cartouche blanc cerné de marine (1 pt), trois coins arrondis, coin bas droit vif ; texte « .12 » : point turquoise, chiffre Bold marine 7–8 pt |
| Mention légale | marge gauche, verticale (lecture de bas en haut), x ≈ 23, y ≈ 250 → 378 | « OCTO I PART OF ACCENTURE © 2026 - All rights reserved », ≈ 5 pt, marine, première partie en gras |
| Série de pages | haut droite, aligné sur le titre | « 1/3 » en Bold marine |

Fond blanc par défaut. Pas de fond marine plein sur une page de contenu. Fond coloré toléré : `#3E4F78` sous une grande carte blanche (p. 7).

### Pages structurantes
#### Couverture (p. 1)
- Photo pleine page sous un voile marine prononcé (rendu bleu). Sans photo du catalogue : aplat `#0E2356`, éventuellement avec une illustration au trait blanc.
- Sigle blanc, haut gauche, deux fois plus grand qu'en page intérieure.
- Haut droite : « OCTO Technology I Part of Accenture », blanc, ≈ 5,5 pt.
- Bloc titre : grande pilule à **contour blanc** (≈ 1,5 pt), fond transparent, environ x 12 → 62 %, y 27 → 62 %. Titre Outfit Bold blanc 28–30 pt aligné à gauche, avec point final turquoise. Le coin bas droit de la pilule est vif et raccordé à un petit bloc (année | entité, Bold blanc ≈ 11 pt, séparés par un filet vertical).
- Un point turquoise isolé (≈ 11 pt) près du bloc ; une illustration au trait blanc accolée à droite.
- Bas gauche : « Digital thinkers & doers » ; marge droite verticale : « There is a better way » ; blanc, ≈ 5,5 pt.

#### Sommaire (p. 2)
Gabarit standard, titre « Sommaire ». Entrées en Bold marine ≈ 11 pt alignées à gauche (soulignées si ce sont des liens) ; numéros de page en Regular marine dans une colonne à droite, sans points de conduite.

#### Intercalaire de chapitre (p. 25, 52, 62…)
- Fond blanc, **point turquoise plein** (≈ 11 pt) à la place du sigle, en haut à gauche.
- Visuel en **goutte** (cercle dont le coin haut droit est vif), ≈ 200 pt, à gauche du centre. Dans le gabarit : objet 3D du catalogue photo sur fond bleu-turquoise. Sans photo : goutte turquoise pâle (`#C6F1F5`) avec un picto ou une illustration au trait.
- Onglet posé sur l'angle vif de la goutte : contour marine fin, haut arrondi, deux cellules séparées par un filet (sigle marine | « 01 » en Bold marine ≈ 12 pt).
- Titre du chapitre à droite du visuel, centré verticalement : Outfit Bold marine 20–28 pt, sans point final.
- Marge gauche verticale : « There is a better way ».
- Variante éditoriale (p. 26) : photo à coins opposés arrondis, titre géant « Chapitre. » à cheval sur la photo (blanc sur la photo, marine sur le fond, point turquoise), « 01 » géant.

#### Slide « héros » (p. 4, 26, 63)
Titre géant (≈ 54 pt Bold) avec **point final turquoise**, qui chevauche une photo à coins opposés arrondis. Réservée aux ouvertures et affirmations fortes ; c'est le seul cas de point final sur un titre de slide, avec la couverture et les accroches.

#### Clôture (p. 321)
Grand emblème au trait et « There is a better way. » avec point turquoise.

### Formes et éléments (p. 8–10)
- **Forme signature** : rectangle à coins asymétriques, grand rayon (20–40 % du petit côté) sur 2 ou 3 coins, au moins un coin vif. Variantes : coins haut gauche + bas droit, coins haut droit + bas gauche, goutte.
- **Pilules** (rayon 50 %) : étiquettes, barres de Gantt, lignes de tableau, bulles.
- **Cartes** : fond blanc, contour marine ≈ 0,75–1 pt, **sans ombre**. Cartes souvent accolées ou chevauchées, sans gouttière.
- **Onglets** : petit titre posé sur le bord haut d'une carte ; ou cercle à picto à cheval sur le bord gauche.
- **Séparateurs** : pointillés marine (colonnes, lignes), filets marine fins, double tiret court marine + turquoise, filet `#B7BDCC` épais.
- **Puces** : « ● » niveau 1, « ○ » niveau 2 (indentation ≈ 12 pt, corps plus petit), en marine ou turquoise. Le chevron « > » sert aussi de puce.
- **Citations** : grands guillemets pleins marine, carte cernée, pilule « Source : » sous la carte.
- **Flèches** : traits épais (≈ 4 pt) à bouts arrondis et pointe en chevron ouvert, marine, turquoise ou en contour.
- **Photos** : jamais en rectangle droit. Goutte, rectangle à coins opposés arrondis, cercle ou demi-pilule. Portraits ronds, en noir et blanc. Une petite forme arrondie décalée accompagne souvent la photo.

### Écriture des slides
- Une idée par slide ; titre court en Bold, sous-titre pour le message.
- Chiffres d'étapes sur deux chiffres (« 01 ») pour les chapitres, « 1. » ou « 01. » pour les étapes.
- Décimales avec virgule. Ne pas mélanger français et anglais dans un même deck.
- Les règles typographiques du `SKILL.md` s'appliquent (pas de titres en capitales, pas d'italique, alignement à gauche), même là où le gabarit s'en écarte.

## Catalogue des slides préformatées

Source : « Slides préformatées OCTO 2026 » (Drive, 321 pages). Le PDF n'est pas fourni : les descriptions suffisent à reproduire une mise en page avec les helpers ; l'utilisateur peut ouvrir la page citée sur le Drive. Les bandeaux « A adapter à sa situation », « Version compatible export .ppt » et le texte « ici mettre une photo » sont des consignes internes du gabarit : ne jamais les reproduire.

### Pages 1 à 160


| Pages | Type de slide | Description de la mise en page | Quand l'utiliser |
|---|---|---|---|
| 1 | Couverture | Voir `slides.md`. | Première page d'un deck. |
| 2 | Sommaire | Voir `slides.md`. | Deck long, navigation. |
| 3 | Pédagogie contraste | Titre dans une grande pilule à contour (titre Bold, 2e ligne en Bold plus petit, point turquoise). Photo dans l'angle haut-droit de la pilule. Grille 2 x 3 de pilules d'exemple avec une coche ou une croix dans un cercle à cheval sur le coin haut-gauche. Carte de message à droite (contour, coins arrondis en bas). | Référence. Montre aussi un patron « exemples ✔ / ✘ ». |
| 4 | Slide « héros » photo + texte | Photo dans un rectangle aux coins haut-droit et bas-gauche très arrondis, sur la moitié gauche (x 65–353, y 39–363). Titre géant « Couleurs. » (≈ 54 pt Bold) qui chevauche le bord de la photo : la partie sur la photo est blanche, la partie sur le fond blanc est marine, le point final est turquoise. Texte Bold marine à droite, puis deux pastilles goutte avec leur légende. | Ouverture d'une partie, affirmation forte. |
| 5 | Nuancier | Grille 5 x 4 de pastilles goutte + étiquettes. | Référence couleurs. |
| 6 | Matrice | Grand tableau à pastilles rondes en en-têtes de ligne et de colonne, cases colorées et coches. | Référence. Patron réutilisable pour une matrice à double entrée. |
| 7 | Checklist | Fond #3E4F78, grande carte blanche, 2 colonnes de 3 encadrés à contour marine et coins très arrondis ; titre de chaque encadré en Bold, puces ●. | Liste de règles ou de critères en 6–7 blocs. |
| 8–10 | Kit d'éléments graphiques | Planches de formes, trackers, avatars, guillemets, sigles, bulles, séparateurs, flèches. Une rubrique = un libellé regular suivi d'un filet gris fin horizontal. | Référence des primitives (voir `slides.md`). |
| 11–12 | Logos | Grille 3 x 3 de cartes à contour et coins arrondis contenant les logos (OCTO en version blanche, marine et turquoise, Duck Conf, Accenture, La Conf Data IA, USI, OCTO academy, B Corp, Great Place To Work, OCTO events, OCTO SKOOL, Numérique Responsable, autre cercle). Phrase Bold à droite. | Ajout de logos. |
| 13–15 | Tutoriels | Captures et étapes « 01. », « 02. » (Bold, numéro sur deux chiffres + point), texte. | Interne, à ne pas reproduire. |
| 16–18 | Photos pour pages chapitre | Trois photos 3D en goutte ou cercle, fond bleu-gris. | Banque d'images. |
| 19–21 | Pictos | Trois colonnes, chacune avec une pilule marine pleine (libellé blanc), une grille de pictos et des séparateurs verticaux pointillés. | Banque. Patron « catégories en pilules marine ». |
| 22–24 | Illustrations | Grille 3 x 2 de scénettes au trait, inscrites dans des pilules ou en forme libre. | Banque. |
| 25, 52, 62, 76, 82, 94, 112, 132, 154 | **Intercalaires de chapitre** 01 à 09 | Voir `slides.md`. | Début de chaque partie. |
| 26 | Intercalaire variante « Chapitre. » | Comme la p. 4 : photo à coins opposés arrondis à gauche, titre géant « Chapitre. » à cheval (blanc puis marine, point turquoise), « 01 » géant Bold marine, phrase Medium ≈ 20 pt marine. | Variante plus éditoriale de l'intercalaire. |
| 27–28 | Sous-chapitre | Carte à contour (coins haut-droit et bas-gauche arrondis), surmontée d'un onglet « XX \| sigle », titre Bold ≈ 22 pt. Photo en cercle (27) ou en goutte (28) accolée à droite. | Sous-partie. |
| 29–30 | Frise photo + texte | Cinq demi-pilules photo alternées haut / bas, avec le texte dans les vides, sur une bande horizontale bleu-gris. | 5 étapes ou idées très visuelles. |
| 31–32 | Message clé + visuel | Photo en forme libre à gauche, grande bulle à contour à droite avec la phrase Bold ≈ 20 pt et le point turquoise. | Message clé, citation interne. |
| 33–38 | Photo + texte (1 colonne) | Photo à coins opposés arrondis ou en goutte, petite forme d'accompagnement, titre Bold ≈ 20 pt ou paragraphe ≈ 9 pt. Un filet marine se termine par un cercle turquoise cerclé. En p. 38, encart de 3 colonnes séparées par des filets verticaux dans une carte à contour. | Message illustré, page de texte avec visuel. |
| 39–42 | Photo + zone libre | Photo sur environ un tiers de la largeur (en haut, avec une carte à contour dessous en 39–40 ; colonne droite en 41–42). Le reste est vide. | Base libre avec visuel. |
| 43–49 | Bulle citation / encart + photo | Grande carte à contour (coins opposés arrondis), guillemet marine, photo en goutte qui déborde du coin. En 49, un picto remplace la photo. | Verbatim, mise en exergue. |
| 50–51 | Verbatims / Citations / Feedbacks | Portrait (noir et blanc ou couleur) dans un rectangle arrondi, carte de citation à contour qui chevauche la photo, guillemets marine 66 / 99, pilule « Source : » sous la carte. | Témoignage client. |
| 53 | 1 sous-titre + 3 cartes | Lien avec un filet turquoise à gauche (« https://www.octo.com/ »), « Sous titre. » Bold avec point turquoise, paragraphe Bold. Trois cartes à contour emboîtées avec des titres Bold ≈ 20 pt, de grands pictos. | Présentation de 3 points avec intro. |
| 54–61 | Suggestions de mise en page | Combinaisons de titre Bold ≈ 20 pt, cartes emboîtées, listes à puces, pictos dans des cercles, photos en goutte, encarts à 3 colonnes séparées par des filets fins. | Pages de contenu libres. |
| 63–69 | Executive summary / présentation OCTO | Contenu réel. 63 : titre héros à point turquoise, illustration dans une pilule, grille 2 x 2 de cartes marine pleines (Bold blanc + regular), colonne de texte dans une grande carte à contour. 64 : titre sur 2 lignes, sous-titre, une carte marine, deux cartes à contour avec picto, une carte turquoise pleine avec 4 pictos en cercle. 65 : illustration dans une pilule verticale à gauche, 3 blocs coche turquoise + titre Bold + texte avec du gras. 66 : cartes de listes + 4 prismes en pictos ronds + bandeau marine plein en bas. 67 : titre dans un onglet turquoise, 2 colonnes séparées par un pointillé, bandeau marine en bas. 68–69 (en anglais) : lettre d'introduction avec portraits ronds en noir et blanc et légende nom Bold / fonction. | Synthèse, pitch, mot d'introduction. |
| 70–73 | Cadrage : frise + 4 colonnes | Grande flèche-frise en contour avec 2 à 5 jalons numérotés (pastilles goutte « 1. ») et un point turquoise « (hors périmètre) ». Dessous, 4 colonnes à onglets avec picto (Durée, Objectifs, Périmètre, Livrables) dans un cadre à contour aux coins arrondis en bas à gauche et en haut à droite. | Périmètre d'une mission. |
| 74–75 | Hypothèses | Cartes à contour accolées en mosaïque, titre Bold de chaque bloc, puces turquoise, avatar ou picto. | Hypothèses, prérequis, engagements. |
| 77–81 | Contexte et demande | 2 grandes cartes avec pastille picto + libellé à gauche et une ligne de conclusion en bas (77) ; 2 blocs empilés + chevron turquoise > + carte de synthèse (78–79) ; 3 cartes à onglets reliées par « + » et « = » dans des pastilles turquoise (80) ; 4 colonnes à onglets centrés reliées par des points turquoise (81). | Contexte, besoin, équation « contexte + cas d'usage = format ». |
| 83–85 | Démarche en tableau | Grille de 3, 4 ou 5 colonnes à en-têtes numérotés « 1. Titre » ; 2 lignes « Activités » / « Livrables » avec des libellés verticaux blancs sur une bande marine pleine à gauche ; coin bas-droit arrondi. | Démarche par phases × activités et livrables. |
| 86–90 | Démarche en cartes | 2 à 4 cartes à contour avec un en-tête « Titre » souligné, un picto numéro rond turquoise dans l'angle, une section « LIVRABLES » en capitales Bold sous un filet (86–88). 4 colonnes numérotées + picto (89). 3 cartes avec une pastille numéro à cheval + une bande « LIVRABLES » + pointillés (90). | Étapes détaillées. |
| 91 | Étape unique | Parcours en serpentin à contour, onglets « 1. Démarche » et « 2. Livrables », pastille turquoise « Objectif de l'étape ». | Zoom sur une étape. |
| 92 | Feuille de route | Frise en S de 5 phases en pilules à contour, jalons en pastilles turquoise, libellés Bold ou regular, bloc « Objectifs » avec picto cible + puces turquoise et flèches. | Proposition de démarche. |
| 93 | 4 piliers + bandeau | 4 colonnes « 1. … » dans des cartes, puces avec du gras, rangée de pilules numérotées en dessous. | Principes d'architecture. |
| 95–101 | Détails étape | 2 à 4 cartes à contour avec un cercle picto + libellé (Démarche, Prérequis, Livrables, DNS…) à cheval sur le bord gauche. Onglets de titre (98, 100, 101). En 101, une ligne « Résultats pour le client » avec un chevron turquoise. | Fiche d'étape. |
| 102–103 | Grille 3 + 4 ou 4 + 4 | Cartes à onglet picto + titre Bold, séparateurs pointillés verticaux. En 103, la dernière colonne a des en-têtes marine pleins (mise en avant). | 7 à 8 thèmes. |
| 104–105 | Fiche atelier / recommandation | Trois pilules à contour (OBJECTIFS, PRÉ-REQUIS, INDICATEURS en capitales Bold, picto, puces « > »), jauges à 5 ronds, filet pointillé, texte + carte à contour, rangée de 5 cercles numérotés. En 105, colonne de pilules à gauche et carte marine « NOTRE PROPOSITION DE VALEUR » à droite. | Atelier, recommandation. |
| 106 | Profil entité | Tableau d'identité (en-têtes turquoise), radar à gauche, bandeaux marine « Périmètre », « Les constats clés », 3 cartes Forces / Faiblesses / Perspectives à en-tête marine. | Diagnostic d'organisation. |
| 107–111 | Étapes en 3 à 6 colonnes | Picto dans une goutte à contour, pastille de jalon turquoise, filet pointillé vertical, « Title text block » + texte centré. Variantes : numéros géants « 1. », numéros « 01 » dans un onglet, pastille numéro turquoise. 108 : cartes en arche reliées à une frise de mois. | Processus, étapes, piliers. |
| 113–116 | Planning Gantt | Bandeau marine en pilule avec les jours ou les mois en capitales blanches (L M M J V S D / JANV FÉVR…), pilules « ETAPE 01 » à contour, barres de tâches en pilules turquoise dans des pilules à contour, colonne « LIVRABLES » (en-tête marine). 115 : légende Terminé (marine) / En cours (turquoise) / A faire (gris), losanges de jalons. | Planning de mission. |
| 117–120 | Timelines et plannings détaillés | Frise de 4 phases en bandes de dégradé (gris → marine), jalons sur des tiges de hauteurs variées. Planning d'ateliers par semaines et par axes (pilules, pictos ronds turquoise). Projection par lots (pilules numérotées turquoise). Planning annuel multi-pistes. Légende dans un encadré en haut à droite, note en bas dans un bandeau turquoise (118). | Plannings riches. |
| 121 | Semaine | Mois en capitales Bold, 7 jours en chiffres géants Bold (≈ 30 pt) + abréviations en capitales (LUN…). Samedi et dimanche en turquoise. Lignes pointillées. | Planning hebdomadaire. |
| 122–130 | Calendriers | Année (12 mini-tableaux, en-tête marine, numéros de semaine en colonne turquoise), semestres, trimestres (en-têtes de mois marine, semaines S1… sur bande turquoise, colonnes pointillées). | Calendrier de mission. |
| 131 | Rétroplanning | Colonnes de phases à fond turquoise clair (descente 10–30 %), étiquettes d'activités en pilules marine pleines, pastilles de légende. | Rétroplanning à deux pistes. |
| 133–139 | Tableau simple 3 à 5 colonnes, 1 à 5 lignes | En-tête marine plein, coins haut arrondis (≈ 6 pt), texte blanc ≈ 10 pt. Corps blanc, filets verticaux marine fins, séparateurs de lignes **pointillés**. **Bande turquoise pleine ≈ 12 pt en pied**, coins bas arrondis. Cadre extérieur marine fin. Le tableau occupe x ≈ 75–645, y ≈ 88–383. Le titre de la slide est le type de tableau. | Tableaux standard. |
| 140–145 | Tableau croisé 2 colonnes × 1 à 5 lignes, 4 × 5 | Comme 133–139, avec une colonne d'en-têtes de ligne à gauche (fond blanc, « Titre » en Medium ≈ 12 pt). L'en-tête marine commence après cette colonne. | Comparaisons à double entrée. |
| 146, 153 | Tableau en pilules | En-têtes de colonnes en pilules marine, lignes en pilules à contour, libellés de ligne dans des pilules reliées par un pointillé. Dans les cases : 3 ronds d'évaluation (blanc, turquoise, marine) en 146, texte en 153. | Matrices d'évaluation, scoring. |
| 147–148 | Rétro / bilan | Tableau à en-tête marine, 4 lignes avec picto + libellé Bold, chevron turquoise vers une carte de synthèse à en-tête marine. | Rétrospective, bilan. |
| 149–151 | Grille 4, 8 ou 6 cases | Grand cadre arrondi divisé en cases par des filets, avec un losange incurvé (« astroïde ») à chaque intersection. | 4 à 8 blocs de texte égaux. |
| 152 | Template CIR | 8 cartes : en-têtes marine (6) et turquoise (2) avec texte Bold centré. | Gabarit de dossier. |
| 155–156 | Listes en serpentin / frise | Ligne sinueuse en contour double, numéros en pictos ronds turquoise, texte centré (155). Pilules verticales alternées sur un axe horizontal, avec des pictos (156). | 5 étapes ou idées. |
| 157–160 | Listes numérotées | 4 cartes avec une colonne « 1. » géant souligné + « Titre », et puces (157–158). 4 quarts de cercle autour d'un picto central (159). 4 lignes avec une pastille « 1. » + une flèche-pilule « Titre » en contour + un paragraphe (160). | Listes de 4 éléments. |

### Pages 161 à 321


| Pages | Type de slide | Description (structure, éléments) | Quand l'utiliser |
|---|---|---|---|
| 161-162 | Rangées numérotées | 2 ou 3 rangées ; onglet « 1. » ; résumé gras à gauche dans un cadre arrondi ; 2 colonnes de puces à droite séparées par des filets | Plan d'action, points d'une synthèse avec détail |
| 163-165 | Blocs à onglet « Titre » | 2, 3 ou 4 cadres pleine largeur, onglet en pilule avec point turquoise, texte courant | Énumérer 2 à 4 messages développés |
| 166-167 | Colonnes en pilules | 5 stades verticaux au contour marine ; titre, texte, picto en bas (166) ou numéro cerclé en haut (167) | 5 piliers, 5 étapes |
| 168, 191, 214, 247, 253, 264, 293, 301, 304, 307, 314 | Intercalaire de chapitre | voir `slides.md` | Ouvrir une partie |
| 169 | SWOT | 4 cartes : pavé lettre « S. W. O. T. » en Bold souligné + libellé, dans des teintes de turquoise croissantes (#DAF6FA → #B1F1F2 → #72DFE7 → #00D2DD), puces à droite | Analyse SWOT |
| 170 | 3 étapes progressives (Shu-Ha-Ri) | Onglets numérotés dont l'en-tête passe de blanc à turquoise puis marine ; contenu ; sablier + durée | Montée en autonomie, transfert |
| 171 | Cœur + 4 quadrants | Cercle turquoise central « CULTURE », 4 cadres autour avec titre et liste centrée, pictos | Modèle à 4 dimensions autour d'un noyau |
| 172-173 | Avant / après | Deux blocs (Projet → Produit) ; onglets 01/02 ; chevron ou flèche turquoise ; citation en bas avec picto télescope | Changement de modèle |
| 174 | Grille de cartes 4×3 | Cartes blanches, dernière colonne mise en avant en teinte, turquoise puis marine | Référentiel de compétences, catalogue |
| 175 | Phases en colonnes | 3 phases 01-02-03 en bandeau turquoise ; lignes Objectifs / Activités / Livrables avec pictos à gauche ; bandeau « Documents souhaités » en bas | Démarche détaillée d'accompagnement |
| 176 | Processus à 6 phases | Pictos + titres en CAPITALES + sous-titre ; grand aplat turquoise ; colonnes séparées par des pointillés ; boucle de retour sous le schéma | Cycle de vie complet, chaîne de valeur |
| 177 | Principes par domaine | Cartes avec tag (PRODUIT / TECH / ORGA) et mini-schémas | Principes de cadrage |
| 178-179 | Schéma de flux agile | Backlog → sprints → incrément ; flèches marine (flux) et turquoise (retours) ; encadré en bas avec 3 onglets turquoise | Expliquer un cadre de travail (Scrum, MVP) |
| 180-181, 193 | Organisation / Venn métier-IT | Schéma en couloirs (Process / Product / People), Venn de deux cercles turquoise | Modèle d'organisation |
| 182, 199 | Feuille de route | Jalons sur une flèche (182) ; couloirs « stream » × trimestres avec aires turquoise et étiquettes « Feat » (199), cible à droite | Roadmap |
| 183, 197 | Escalier / imbrication | Marches diagonales en teintes croissantes (183) ; blocs emboîtés IA > ML > DL > GenAI, du pâle au marine (197) | Niveaux de maturité, taxonomie |
| 184 | Pile de couches | Couches empilées avec des bandeaux marine, libellés à gauche, enjeux à droite | Architecture en couches |
| 185-187 | Slides de positionnement | Titre long Bold avec point final turquoise, logos de labels, cercles d'idées (187) | Message institutionnel, panorama |
| 188-190 | Tableaux | voir `graphiques-schemas.md` | Benchmark, comitologie, plan de charge |
| 192 | Boucle DevOps | Infini turquoise/marine, pictos au centre | DevOps |
| 194-195, 234 | Étapes en boucles | 4-5 anneaux turquoise enchaînés, pictos ou numéros dedans, onglets de titres dessous | Démarche en 4-5 étapes |
| 196 | Cercles de regroupement | 3 cercles pointillés avec personnages ; étiquettes en CAPITALES dans des rectangles arrondis ; conclusion avec picto cible | Cartographie de responsabilités |
| 198 | Échelle de maturité | Échelle illustrée à gauche, 4 niveaux : constat (blanc) / niveau (turquoise) | Auto-évaluation |
| 200-201 | Phases produit | 3 cercles (discovery / delivery / croissance) au-dessus de pilules en marine dégradé ; courbe en S remplie de turquoise (201) | Cycle de vie produit |
| 202-204 | Parcours sinueux | Chemin #3FBDD0 avec personnages et horaires ; route illustrée | Journée type, parcours utilisateur |
| 205 | Maison du Lean | Toit, piliers, socle, au trait ; variante segmentée en 3 | Modèle à piliers |
| 206 | Baromètre | 6 smileys turquoise, titres, barre graduée en 5 teintes + blanc, flèche marine pour la position | Échelle de satisfaction, de maturité |
| 207-209 | Triangle, losange, fleur | Triangle à 3 zones (blanc / marine / turquoise) ; losange central turquoise avec activités autour ; cercle turquoise « Fails » entouré de cercles | Concept à 3 composantes, idéation, erreurs fréquentes |
| 210 | Nuage de mots | Encadré marine, mots en blanc et en turquoise, en tailles et graisses variées | Principes, valeurs |
| 211 | Courbe Hype Gartner | Courbe marine, colonnes de phases en en-tête | Maturité d'une technologie |
| 212-213, 227-228, 249 | Matrices | voir `graphiques-schemas.md` | Priorisation, Wardley, APM |
| 215-221 | Donuts, cycles | voir `graphiques-schemas.md` | Répartitions, cycles de 3 à 8 étapes |
| 222-224 | Jauges | voir `graphiques-schemas.md` | KPI en pourcentage |
| 225-226 | Radars | voir `graphiques-schemas.md` | Évaluation multicritère |
| 229-233 | Barres, courbe | voir `graphiques-schemas.md` | Données chiffrées |
| 235-239, 244 | Schémas radiaux | Pétales autour d'un centre turquoise ; flèches en étoile ; anneau segmenté ; cercles imbriqués (Pourquoi / Comment / Quoi : marine au centre, turquoise, blanc) | Concept central et facettes |
| 240 | Démarche en 3 temps sur ligne de temps | Picto en pastille turquoise au-dessus d'une ligne marine, jalon en anneau, titre en CAPITALES Bold, onglet « GOALS » turquoise, puces avec passages en gras | Démarche d'audit, de cadrage |
| 241-243 | Entonnoir, cône, pyramide | Disques turquoise empilés sur un axe marine fléché ; pyramide à 3 niveaux turquoise avec légende de points | Filtrage, hiérarchie |
| 245 | Venn 3 cercles | Turquoise / blanc / marine, intersections teintées, légende à droite par cartouches verticaux | Recoupement de 3 notions |
| 246 | Diagramme d'Ishikawa | Arêtes marine fines, titres et texte | Analyse de causes |
| 248 | Fiche recommandation | Code « 2-A » turquoise + 2 mini-jauges Gain/Effort ; bandeau Description ; 3 cartes Bénéfices / Points d'attention / Profils, avec pictos coche et triangle d'alerte | Détail d'une recommandation |
| 250 | Référentiel en grille | Lignes de domaines × colonnes, en-têtes marine, sous-en-têtes en bandeaux turquoise en CAPITALES | Référentiel d'architecture |
| 251-252 | Cartes de convictions, principes à icônes | Grille de 6 cartes (une marine, une turquoise) ; 2×3 principes avec picto en cercle | Convictions, principes |
| 254-263 | Kit canvas | Lean canvas, persona, thèse d'investissement, experience map, North Star Metric, carte d'empathie ; versions remplies et vierges ; en-têtes marine, zones turquoise pâle à remplir ; mention de licence Creative Commons en bas | Ateliers |
| 265-275 | Équipe | Équipe en blocs marine / turquoise avec photos rondes ; mosaïque de photos en gouttes + cartouche « Votre équipe » ; cartes de 2 à 4 personnes (nom Bold, fonction, texte) | Présenter l'équipe |
| 276-286 | Charges par étape | Pilules « ETAPE 0x » ; pastilles turquoise « Xj » par profil ; total en pastille marine ; photos au-dessus ; description des rôles à droite | Plan de charge en jours-homme |
| 287-292 | Mini-bios | Photo en goutte, nom, texte ; barres de compétence turquoise ; versions pour réponse Word | Réponse à appel d'offres |
| 294-300 | Propositions financières | Encadrés à coins arrondis avec pictos (billets, sablier, train) et montants en gras ; 4 pilules d'options ; tableau de répartition ; rate card ; OPEX/CAPEX ; offre de partenariat avec picto | Partie financière d'une proposition |
| 302-303 | CV | Expériences en colonne, certifications / formations / contributions / compétences dans des colonnes à pastilles | CV de consultant |
| 305-306 | Fiche de référence | Tag secteur en pilule ; 3 blocs numérotés (contexte, mission, résultats) ; chiffres « + XX » ; citations avec guillemets turquoise épais | Référence client |
| 308-313 | Arbre OCTO | Grand arbre au trait marine (raison d'être, champs d'actions, leviers, expertise, racines) ; une zone grisée à la fois | Fil conducteur, mise en avant d'une dimension |
| 315 | Conférences | Photos en gouttes, dates et noms soulignés | Présenter les événements |
| 316-320 | Événements à charte propre | La Duck Conf : jaune #FFFF00, noir ; La Grosse Conf : fond sombre #2D2D33, rouge #FD0041 ; USI : violet-bleu #362EE6, vert menthe #6FF0C9 | **Hors charte OCTO** : à ne reproduire que pour ces événements |
| 321 | Clôture | Grand emblème au trait + « THERE IS A BETTER WAY. » en capitales espacées, point turquoise | Dernière slide |

