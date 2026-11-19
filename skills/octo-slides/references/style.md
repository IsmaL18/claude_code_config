# Style des slides OCTO

Tiré d'un deck de référence (« Model Platform », 24 slides, février 2026) et de la bibliothèque « Slides préformatées OCTO » (charte 2026). Ce fichier décrit la manière de construire et d'écrire les slides. Les couleurs, la typographie, l'accessibilité et les règles de marque sont dans `charte.md`, **qui prime** : là où l'usage du deck d'origine s'en écartait (texte turquoise, capitales, flèches fines, badge), il a été aligné sur la charte.

## 1. Charte (résumé, détail dans `charte.md`)

- Format 16:9, 10 x 5,625 pouces. Toujours partir de `assets/template_octo.pptx` (masters et layouts OCTO : sigle, mentions légales verticales, numéro de page en pastille).
- Une seule police : Outfit. Gras pour l'emphase, jamais d'italique (les citations se marquent avec des guillemets “ ” ou « »).
- Bichromie : bleu marine `#0E2356` (tout le texte) + turquoise `#00D2DD` (fonds, accents, puces, pastilles). Le texte n'est jamais noir.
- **Jamais de texte turquoise sur fond clair.** Seule exception : le point final turquoise d'un titre de couverture, de slide « message » ou « héros ». Le turquoise en texte n'existe que sur fond marine.
- Teintes : uniquement les gammes marine et turquoise de `charte.md`, et pour les schémas et les fonds de blocs (consigne de la Com, modèle 5), jamais pour du texte.
- Accessibilité : la couleur n'est jamais le seul repère, texte aligné à gauche (centré seulement pour une phrase-message), interligne ≈ 1,5 pour le texte courant (1,2 toléré dans les blocs denses de 8 à 9 pt), ≤ 80 caractères par ligne, pas de capitales hors sigles, écriture inclusive avec parenthèses ou tiret (« ingénieur(e)s »), jamais de point médian, espaces insécables avant « ; : ! ? % ».

## 2. Trois registres

Le style a deux registres de deck, souvent dans le même deck (une partie récit, puis un « Deck détaillé » après une slide chapitre), et un registre de slide unique, la vue d'ensemble.

Récit / pitch (aéré) :
- Titre court et nominal, parfois une question : « Qui suis-je ? », « D'où vient l'idée ? », « Les moyens », « La suite », « Qu'en avons-nous tiré ? ».
- Une seule idée par slide : une grosse phrase en gras (24 pt) avec 2 ou 3 mots clés soulignés par la graisse et un **point final turquoise**, ou un visuel (frise illustrée, triangle des bénéfices, schéma avant / après avec personas).
- Beaucoup de blanc.

Détaillé (dense mais structuré) :
- Titre = une phrase affirmative qui porte le message : « Sans chemin standard du registre à la production, rien n'est reproductible ni traçable », « Un pilotage centralisé. Une isolation totale par projet », « La conformité AI Act, générée et opposable ». Souvent deux phrases nominales courtes, ou « X, Y et Z » en balancement. Pas de point final sur un titre de slide de contenu.
- Sous-titre juste dessous : une phrase-chute qui résume ou oppose (« Mettre un modèle en production coûte cher. Ne pas savoir ce qui tourne coûte encore plus cher. », « Centraliser la gouvernance et l'observabilité, pas les ressources. »).
- Corps en 9 à 11 pt, organisé en blocs (blocs emboîtés, schéma, tableau : `mise_en_page.md`). Des pictos avec modération, là où ils portent le sens (consigne de la Com : « user modérément des abréviations, pictos »), pas un picto par bloc par principe.
- Une phrase de conclusion en bas, en gras, avec picto (takeaway).

Vue d'ensemble (une slide qui se lit, envoyée ou posée en annexe) :
- Une seule slide porte toute une démarche : le **pourquoi** à gauche (panneau marine), le **quoi** à droite (N cartes).
- La matière fournie est **reprise presque intégralement**, découpée et rangée, pas résumée en slogans. Le texte des cartes descend à 6 pt, les titres de cartes à 8,5 pt : la densité est assumée parce que la structure est très régulière.
- Titre court et nominal (« Partenariat OCTO × Anthropic »), sous-titre qui porte la thèse avec 2 ou 3 mots en gras, réduit à 12 ou 13 pt pour tenir sur une ligne.
- Voir l'exemple de référence `examples/vue_ensemble_piliers.py` et son rendu `assets/exemples/vue_ensemble_piliers.png`.

## 3. Écriture du texte

- Français, franglais assumé pour les termes du métier (Model Registry, endpoint, namespace, gate, dashboard). Ne pas mélanger deux langues pour les phrases d'un même deck.
- Chaque bloc commence par un lead en gras qui dit l'idée, suivi d'une explication courte en regular : « **Chaque équipe déploie à sa façon.** À chaque nouveau projet, on se pose les mêmes questions… », « **Générée, pas rédigée.** La fiche de conformité est dérivée… ».
- Formules en balancement ou en opposition : « Générée, pas rédigée », « Démontrer, accélérer ou transposer », « Des principes, pas du code à porter », « La conformité n'est pas un rapport, c'est un contrôle ».
- Mots clés en gras à l'intérieur des puces (2 ou 3 par puce maximum) : « Mise en prod fluide sur **Kubernetes, Docker ou Batch**. »
- Libellés de schéma courts, en gras, avec une majuscule initiale seulement : « Espace projet A », « La plateforme », « Versionning », « Déploiement ».
- Verbatims de personas entre guillemets, ton oral, avec le mot important en gras : « “Ah zut je l'ai pas **versionné**, j'ai plus les artefacts” ».
- Pas de paragraphe de plus de 3 lignes dans un bloc. Pas de puce de plus de 2 lignes.
- Décimales avec virgule (« 24,3 % »).

## 4. Mise en page

La manière de poser les éléments (zones découpées, blocs emboîtés, formes de la Com, texte mesuré) est dans `mise_en_page.md`. Repères :

- Titre en (0,62 ; 0,40), largeur 8,7. Sous-titre en (0,62 ; 0,85). Zone de contenu `CONTENT` : x 0,6 → 9,2, y 1,3 → 5,2 (takeaway vers y = 4,4 à 4,6) ; la pastille du numéro de page occupe le coin bas droit (x > 9,2, y > 5,05), rien ne la recouvre.
- Marges latérales : contenu entre x = 0,6 et x = 9,5.
- Grilles observées : 3 bandes pleine largeur empilées ; 2 x 2 cartes ; 4 colonnes égales (largeur 2,13, pas de 2,26) ; schéma à gauche + puces dessous ; frise horizontale ; tableau.
- Pictos : 0,5 à 0,75 pouce, posés à gauche d'une bande, au-dessus d'une colonne (reliés par un filet pointillé), ou à cheval sur le coin haut gauche d'une carte. Bichromes sur fond clair, déclinaison `blanc/` sur fond marine.

## 5. Formes et schémas

- **Bloc OCTO** (`bloc`) : la forme de base du contenu dans les modèles de la Com, rectangle à un ou deux grands coins arrondis (rayon ≈ 0,45 pouce), les autres carrés, contour marine 0,75 pt ; les blocs d'un même ensemble s'emboîtent (bords partagés) et varient leur coin arrondi. Goutte (`goutte`), onglets (`steps`), jalons (`tracker`), séparateurs (`separator`) : `mise_en_page.md`.
- Boîte de schéma (`box`, pour les schémas techniques) : rectangle à coins légèrement arrondis (ajustement 0,08), contour marine 0,75 pt, fond blanc. En-tête : même forme, fond turquoise `#00D2DD`, texte marine gras 8,75 pt.
- Hiérarchie des aplats (voir `charte.md`) : marine plein + texte blanc pour le plus haut niveau ou la conclusion, turquoise plein pour le cœur du dispositif, teintes de turquoise pour les regroupements, blanc cerné de marine pour le reste. Au plus un aplat marine par schéma.
- Regroupement / périmètre : rectangle arrondi en pointillés marine 0,75 pt (la plateforme, un périmètre externe : un service hors plateforme se dessine en pointillés, à l'extérieur).
- Cadre « fenêtre d'application » : fond `#E7E9EE`, deux pastilles en haut à gauche (une pleine, une vide), titre en gras aligné à droite (« Kubernetes cluster », « Model Platform »).
- Flèches (charte, modèle OCTO n° 10 « Éléments graphiques 3/3 ») : **flux** en marine épaisse (4 pt), tige à bouts ronds et pointe en chevron ouvert à deux branches arrondies, droites ou coudées ; **boucle de retour** en turquoise épaisse (`loop_back`) ; **lien secondaire** en pointillés marine fins (0,75 pt). Transition entre deux blocs : chevron turquoise « > » isolé (`chevron`). Entre deux boîtes, toujours `connect(a, b)` : la flèche part et arrive sur les bords, centrée sur la partie commune des deux boîtes, avec le même écart partout ; ne pas calculer les points à la main.
- Cartes : rectangle à deux coins diagonaux arrondis (ROUND_2_DIAG), contour marine 1 pt. Colonnes : en-tête à coins hauts arrondis + corps encadré 0,75 pt.
- Pastilles (briques, technos) : rectangle arrondi `#72DFE7`, texte marine 8 pt, avec picto numéroté rond (num_1…num_6).
- Tableaux et chiffres clés : voir `graphiques-tableaux.md` (en-tête marine, lignes pointillées, bande turquoise en pied ; chiffre Bold marine très grand + libellé).
- Personas : avatars OCTO (`references/avatars.md`) avec une étiquette sous chacun (« Legal team », « Dev de modèle », « Consommateur de modèle », « Stakeholder »), sur fond blanc ou teinte claire de marine. Ne pas mêler avatars marine seul et bichromes dans une même vue.
- Illustrations au trait (`references/illustrations.md`) pour une slide récit ou chapitre, en goutte ou pilule, jamais en rectangle droit.
- Logos technos (MLflow, Kubernetes, Docker, Prometheus, Grafana, OpenTelemetry, EU AI Act) en couleurs d'origine, petits, sur une frise ou un bandeau « stack ».
- Pas d'ombre, pas de dégradé, pas de 3D.

## Intentions de design (avant toute mise en page)

Le style OCTO n'est pas une mise en page à reproduire : ce sont des intentions. Une même intention se réalise de nombreuses façons ; c'est ce qui évite que les slides d'un deck se ressemblent. Les helpers, layouts et modèles sont des moyens au service de ces intentions, jamais un gabarit à appliquer partout.

0. **Un schéma quand il y a un mécanisme à montrer.** Se poser la question pour chaque slide (test dans `types_de_slides.md`) : le contenu relie-t-il des éléments (qui produit quoi, dans quel ordre, avec quels retours) ? Si oui, le schéma est le meilleur type : boîtes et flèches de flux, boucle de retour turquoise (`loop_back`), éventail (`fan`), cycle (`cycle`), étages empilés, pipeline avec ce que chaque étape produit accroché dessous, Gantt de principe (`lane`, `bar`), conteneurs pointillés pour les périmètres ; des cartes ou colonnes de texte le réduiraient à une liste. Si non (des éléments indépendants, un chiffre, une citation, une question), un schéma serait décoratif : prendre le type qui sert le rôle de la slide. Exemples : `examples/pipeline_preuves.py`, `examples/schemas_types.py`.
1. **Un point focal par slide.** Décider ce que l'œil doit voir en premier — une phrase, un chiffre, une preuve, un schéma, un visuel — et lui donner le contraste le plus fort de la slide. Tout le reste est subordonné : plus petit, plus clair, plus fin.
2. **Un contraste franc, obtenu de façons variées.** Le foncé contre le clair est la signature OCTO, mais le moyen change d'une slide à l'autre :
   - une masse marine (panneau latéral, bandeau haut ou bas, colonne étroite, cadre autour d'une preuve) ;
   - **une seule** carte marine au milieu de cartes blanches, pour désigner l'élément clé ;
   - l'échelle seule : un chiffre ou une phrase immense sur du blanc ;
   - un visuel (illustration, visuel 3D OCTO, miniature) face à du texte sobre ;
   - le fond du layout (focus 05, couverture 41, chapitre) pour une rupture.
   Une slide sans masse marine est normale quand le contraste vient de l'échelle ou d'un visuel.
3. **Une hiérarchie par l'échelle.** Trois niveaux de taille au plus, avec un écart net entre eux (le point focal fait au moins deux fois la taille du texte courant). Pas de texte courant sous 9 pt.
4. **La forme vient du contenu.** Une séquence appelle une frise ou un flux ; une comparaison, un avant / après ou un tableau ; un ensemble de parties, des colonnes ou une grille ; un seul message, la pleine page ; des chiffres, des chiffres géants ; une preuve, la capture elle-même, en grand. Chercher la forme après avoir écrit le titre-message, pas avant.
5. **Le blanc est un matériau.** Asymétrie assumée, zones vides voulues ; ne pas remplir une grille par principe, ne pas étirer un bloc pour occuper la place.
6. **Les assets OCTO sont des accents.** Visuels 3D (`assets/modeles/visuels_3d.png`, `ModeleDeck.borrow`), illustrations, pictos : au plus un visuel fort par slide, pas sur toutes les slides, jamais deux fois le même dans un deck.
7. **Un deck a un rythme.** Alterner slides denses et aérées, foncé dominant et clair dominant, compositions à gauche, à droite, centrées, en bandeau. Intercaler des ruptures (couverture, sommaire, chapitre, focus, message plein cadre).
8. **Emboîter plutôt qu'espacer.** Les éléments d'un même ensemble se touchent et partagent leurs bords, avec un grand coin arrondi qui varie ; un passage d'un élément à l'autre se marque d'un chevron turquoise ; les flèches sont réservées aux flux (`mise_en_page.md` §2).
9. **Dessiner le mécanisme, pas le décrire.** Ce qui a des formes se dessine avec des formes : un nuage de points et la droite apprise pour « le modèle trouve la règle », un histogramme heure par heure pour une prévision, des cercles reliés pour un réseau de neurones, deux histogrammes côte à côte pour la température d'un modèle, des barres comparées pour un record (2 mois contre 10 ans). Dans une grille de N éléments (familles d'usages), un mini-schéma par élément plutôt qu'un picto : prolonger une série, ranger dans une case, proposer le bon choix, repérer le point hors norme. Une slide faite « que de carrés » de texte se relit mal : l'ordre de lecture se perd.
10. **Un ordre de lecture évident.** Un seul sens par slide (gauche → droite, ou haut → bas), porté par un axe du temps, des flèches ou des numéros ; deux colonnes comparées ont les mêmes boîtes aux mêmes places, et ce qui change de place (« les règles » en entrée à gauche, en sortie à droite) est mis en couleur.
11. **Des traits et des flèches nets** (`mise_en_page.md` §5) : liaisons horizontales, verticales ou en angle droit, jamais en biais ; flèches avec une tige visible ; jonctions à tronc long, cible centrée. Un trait oblique ou une pointe sans tige font négligé, même sur une slide juste.
12. **Des images qui portent l'information** (`images.md`) : une vraie capture, une une de presse, la photo de l'installation dont on parle, posées en goutte ou à coins arrondis. Sur une frise, une image par jalon.
13. **Le style filaire des modèles OCTO** (`modeles.md`, « Le style filaire OCTO ») : composer au trait avec le vocabulaire de la Com (médaillons cerclés pour les pictos, capsules, cartes à onglet, puces cibles, numéros en goutte, visuels 3D en goutte, illustrations au trait, compositions empruntées comme la chaîne d'anneaux), puis réserver les aplats au point focal. Un picto n'est jamais posé nu au milieu d'un texte : il est dans un médaillon, sur le bord d'une carte ou en tête de colonne. Sur un deck, au moins une slide sur deux réutilise un élément des modèles.

### Plan de composition (obligatoire pour 3 slides ou plus)

Avant de générer, écrire pour chaque slide une ligne :
`n. Titre-message — focal : … — contraste : … — géométrie : …`
Exemple : `2. Quatre briques encodent la charte — focal : la brique « charte » — contraste : une carte marine parmi trois blanches — géométrie : 4 colonnes`.
Puis vérifier : **deux slides consécutives ne partagent pas plus d'un des trois** (focal, contraste, géométrie), et aucun dispositif de contraste ne revient plus de deux fois dans un deck de 6 slides. Si le plan échoue, changer la forme avant d'écrire le code.

Ce qu'on évite : un mécanisme réduit à des cartes, bandes ou colonnes de texte ; à l'inverse, un schéma décoratif (des boîtes reliées par des flèches qui ne disent rien) plaqué sur un contenu sans mécanisme ; un même dispositif (panneau + cartes, grille de cartes blanches) répété de slide en slide ; des blocs à moitié vides ; du texte en 8 pt dans de grandes boîtes ; un modèle rempli comme un formulaire.

Réalisations possibles (une parmi d'autres) : `examples/vue_ensemble_piliers.py` (panneau « why » + 6 piliers, pour une vue d'ensemble dense) ; `examples/freins_leviers.py` (panneau « why », rangées frein > levier, bandeau de blocs emboîtés).

## 6. Slides types (à réutiliser)

D'abord les **modèles OCTO** (`modeles.md`) : 303 slides préformatées à copier puis adapter et améliorer — structure ajustée au contenu, titre-message, hiérarchie des aplats, pictos qui portent le sens, conclusion. Ensuite les layouts préformatés du template (`layouts.md`) : couverture 41 sans photo, sommaire à pastilles 90 à 98 (aussi pour une vue d'ensemble de N piliers), focus 05 pour le « pourquoi », chapitre 50 / 51, contenu + visuel + bloc conclu 63 à 70, clôture 59. Ensuite les slides types ci-dessous, dessinées avec les helpers. Pour une mise en page absente des deux (tableau, Gantt, matrice, SWOT, roadmap, équipe…), voir `catalogue.md`.

1 - Couverture (layout 40) : titre, sous-titre, date « jj.mm.aa », tag de tribu (« MLOps »).
2 - Chapitre (layout 50) : titre + numéro, visuel détouré en goutte (illustration OCTO possible).
3 - Message : petit titre nominal + grosse phrase en gras, mots clés en gras, point final turquoise.
4 - Constats : 3 bandes (picto, lead gras, explication) + citation en takeaway.
5 - Architecture : schéma (conteneur pointillé, boîtes à en-tête turquoise, flèches de flux, infra partagée à droite) + 2 ou 3 puces dessous dont le début est en gras.
6 - Fonctionnalités : 2 x 2 cartes avec picto à cheval + takeaway.
7 - Piliers : 4 colonnes avec picto au-dessus, puis bandeau « briques clés » en pastilles numérotées.
8 - Parcours : frise horizontale, libellés Bold marine alternés haut / bas, jalons en anneaux turquoise, logos technos, takeaway avec chrono.
9 - Avant / après : personas + verbatims + schéma, mêmes positions sur les deux slides pour que la comparaison saute aux yeux.
10 - Contributeurs : photos N&B en grille (rondes ou en goutte) avec trigramme dessous.
11 - Vue d'ensemble (piliers, axes, offres en détail) : `why_panel` à gauche (x 0,4, largeur 3,1, y 1,15 → 5,3) avec étiquette « Le why », phrase-ambition blanche et ==mots-clés== turquoise, filet pointillé, intro + 4 puces chevron « **Lead**, suite » ; à droite un intertitre gras 12 pt (« Les 6 piliers du partenariat ») et une grille 3 x 2 de `pillar_card` (largeur 1,92, hauteur 1,86, pas 0,1 / 0,15) : onglet « .01 » sur le bord haut, titre « X & Y » sur 2 lignes, picto bichrome en haut à droite, description, filet pointillé, étiquette « Ambition », détail. Le contenu de chaque carte est le texte source quasi complet. Exemple : `examples/vue_ensemble_piliers.py`.

## 7. Ce qu'on ne fait pas

- **Pas de gabarit cloné** : N slides de même rang (les 6 piliers d'une offre) ne reprennent pas toutes la même mise en page « formulaire » (deux boîtes à en-tête « Ce que nous voulons faire / Ambition », boîtes à moitié vides, pastilles qui redisent le bloc). Chaque slide a son visuel propre, tiré de son contenu : schéma de flux, frise, cartes, colonnes, avant / après, layout à visuel. Le fil commun passe par le titre, le sommaire et la numérotation, pas par une mise en page identique. (Ne s'applique pas aux N cartes d'**une même** slide de vue d'ensemble : là, une structure interne identique est ce qui rend la densité lisible.)
- **Pas de résumé appauvri** : quand la matière est détaillée, ne pas la réduire à un lead et une demi-phrase par bloc. Ranger le texte (description / filet / étiquette « Ambition » / détail) plutôt que le couper.
- **Pas de grille sans récit** : N cartes seules ne disent pas pourquoi. Poser la thèse (panneau why, sous-titre-thèse, intertitre) avant le détail.
- **Pas de lead et de corps sur la même ligne dans une carte dense** : titre de carte sur sa ligne, corps dessous.
- Pas de pastilles ni de takeaway qui répètent un bloc de la slide.

- Pas de slide « titre + 6 puces » sans visuel.
- Pas de texte noir, pas de texte turquoise sur fond clair, pas d'italique, pas de soulignement, pas de capitales pour insister.
- Pas de clipart hors bibliothèque OCTO, pas d'emoji, pas d'image générée par IA sans demande explicite.
- Pas de couleurs hors charte (pas de rouge / vert pour des statuts : utiliser l'intensité du turquoise + forme + libellé).
- Pas de consigne interne du gabarit (« A adapter à sa situation », « ici mettre une photo », « Lorem ipsum »).
- Pas de phrase de conclusion qui répète le titre.
- Pas de masquage du logo avec des rectangles blancs : choisir un layout « vide » si le logo gêne.
