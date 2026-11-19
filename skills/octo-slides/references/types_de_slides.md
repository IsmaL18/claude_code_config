# Choisir le type de chaque slide

Étape 2a du déroulé (SKILL.md) : avant de composer, décider pour chaque slide **ce qu'elle doit faire au public**,
puis le **type de slide** qui le fait le mieux. Le type découle du rôle et de la structure du contenu, jamais de
l'habitude ni du modèle le plus proche.

## Les trois questions, slide par slide

1. **Le rôle** : après cette slide, que doit savoir, croire ou faire le public ? Le résumer par un verbe :
   accrocher, situer, constater, expliquer, raconter, comparer, prouver, chiffrer, décider, conclure.
2. **La structure du contenu** : la matière a-t-elle une forme propre ? Un ordre (étapes), une causalité (qui
   produit quoi), une boucle (retour, itération), une hiérarchie (un tout et ses parties, des couches), une
   opposition (avant / après, options), une grandeur (un chiffre qui compte) ? **Cette forme dicte le type.**
3. **La place dans le deck** : que vient de voir le public, que va-t-il voir ensuite ? Une slide dense appelle une
   respiration ; trois slides de même type d'affilée appellent une rupture.

## Un schéma, ou pas ?

À trancher pour chaque slide, dans un sens comme dans l'autre. Un schéma est adapté si les réponses sont oui :

1. **Des relations** : le contenu relie au moins deux éléments par une relation qu'on peut nommer (produit,
   déclenche, alimente, contient, précède, renvoie à) ?
2. **Des flèches qui disent quelque chose** : chaque flèche porterait une information que le texte seul ne donne pas
   (un ordre, un sens, un retour) ?
3. **Lisible sans légende** : le schéma ferait comprendre le mécanisme même si on en retirait les phrases ?

- **Trois oui** : schéma (pipeline, boucle, éventail, cycle, couches, architecture).
- **Un ou deux non** : le contenu est une énumération, une grandeur, une opposition ou un message. Un schéma serait
  décoratif ; choisir le type de son rôle (cartes ou piliers pour des éléments indépendants, chiffre héros,
  comparatif, avant / après, citation, phrase-message).
- **Dans le doute**, préférer le schéma pour une slide détaillée qui parle d'un dispositif, d'un processus ou
  d'une organisation ; préférer l'autre type pour une slide qui donne des arguments, des bénéfices ou des chiffres.
- **Si la forme ne vient pas**, chercher comment d'autres ont dessiné la même notion (`images.md` §7) : les formes
  qui reviennent dans une mosaïque d'images sont souvent les plus faciles à comprendre.

## Rôle → type de slide

| Rôle | Structure du contenu | Type de slide | Réalisation (helpers, exemples) |
|---|---|---|---|
| Accrocher, poser la question | une phrase, une tension | Message plein cadre, question ouverte | `statement`, `blank` + phrase géante et point turquoise |
| Frapper avec un chiffre | une grandeur qui change la perception | Chiffre héros | phrase + `kpi` géant, visuel 3D (`borrow`) |
| Situer, structurer | des parties | Sommaire, intercalaire | `toc`, `chapter` |
| Constater, poser le problème | des irritants, des faits | Constats en bandes + conclusion, SWOT | `band` + bandeau marine ; modèle SWOT transformé |
| **Expliquer un mécanisme** | causalité, flux, acteurs | **Schéma** : pipeline, boucle de retour, éventail, couches, architecture | `box`, `arrow`, `loop_back`, `fan`, `container` ; `examples/pipeline_preuves.py`, `examples/schemas_types.py` |
| Raconter une séquence | un ordre dans le temps | Frise, démarche en chevrons, Gantt de principe | `timeline`, chevrons, `lane` + `bar` |
| Montrer une boucle | une itération, un retour | Cycle, avec l'étape clé détaillée | `cycle` + `container` |
| Comparer des options | des alternatives sur des critères | Tableau comparatif, colonne recommandée en turquoise | `table` ; modèles tableaux |
| Montrer un changement | un avant et un après | Avant / après, mêmes positions des deux côtés | personas + panneau ; deux miniatures + flèche |
| Montrer un tout et ses parties | une ambition, N briques | Vue d'ensemble : panneau why + piliers | `why_panel`, `pillar_card` ; `examples/vue_ensemble_piliers.py` |
| Montrer une hiérarchie de volumes | peu en haut, beaucoup en bas (tests, besoins, données) | Pyramide à niveaux + légendes alignées | `pyramid` ; `examples/schemas_niveaux.py` |
| Introduire des termes | des notions qui s'emboîtent, du plus large au plus précis | Définitions emboîtées en escalier, un exemple par niveau | `nested` ; `examples/schemas_niveaux.py` |
| Montrer une convergence ou une bifurcation | plusieurs causes, une conséquence ; une source, plusieurs chemins | Jonction, fourche | `join`, `fork` ; `examples/schemas_niveaux.py` |
| Prouver | une trace, un résultat observable | Capture ou miniature annotée, verbatim, preuve accrochée à un schéma | image cernée + pastilles numérotées ; `quote` |
| Chiffrer plusieurs résultats | 3 ou 4 grandeurs | Bandeau ou grille de chiffres clés | `kpi` (`dark=True` sur marine) |
| Décider, appeler à l'action | des options, une demande | Focus sur la décision, options en verbes | layout 05 `focus` ; chips |
| Conclure | le message clé | Phrase-message, clôture | `statement`, `closing` |
| Montrer par l'exemple ce que fait un outil | une demande, une ou plusieurs réponses | Dialogue en bulles ; la même demande à chaque étape d'un processus, une réponse par étape | `chat` (hauteurs alignées d'une colonne à l'autre) |
| Rendre concret un critère, un défaut | un objet réel et ses défauts | Artefact annoté : un relevé, une capture, un document, défauts entourés de turquoise et numérotés, reliés aux critères | `table` + entourages, `goutte` numérotées, blocs à droite |
| Opposer deux façons de faire | les mêmes éléments, rangés autrement | Deux colonnes face à face, mêmes boîtes aux mêmes places ; ce qui change de côté est en couleur | `container` + « + », une seule flèche droite |
| Faire participer | une question, un vote | Question plein cadre ; quiz à main levée (gouttes à picto) ; « Vrai ou faux » en ouverture de partie, réponses en fin de partie | `statement`, `goutte`, rangées numérotées |
| Situer dans une session longue | des parties et leurs durées | Piste proportionnelle aux durées, numéros reliant chaque segment à son bloc « contenu + À vous » ; fil d'onglets sur chaque chapitre | `chapter(parts=…)`, `steps` |
| Dessiner une donnée | une série, une distribution | Histogramme, barres comparées, nuage de points avec sa droite, dessinés aux formes | `_shape` rectangles, `circle`, `rule` |

Un même rôle peut avoir plusieurs réalisations : choisir celle qui varie le plus avec les slides voisines.

## Critères du choix

- **Pédagogie** : une idée par slide ; la forme suit la structure du contenu, pour que l'œil comprenne avant de lire ;
  progression du connu vers le nouveau ; pas plus de 5 à 7 éléments à retenir sur une slide.
- **Impact** : un point focal évident ; le type le plus visuel qui reste juste (un schéma plutôt qu'une liste, un
  chiffre géant plutôt qu'une phrase qui le contient).
- **Style** : le registre de la spec (récit ou détaillé) ; un schéma quand il y a un mécanisme (test ci-dessus,
  `style.md` intention 0) ; la variété et le rythme du deck (intention 7).

## Pièges

- Choisir le type d'après le modèle disponible le plus proche, puis y couler le contenu.
- Des cartes ou colonnes de texte pour un contenu qui a une causalité ou un ordre : c'est un schéma ou une frise.
- À l'inverse, un schéma plaqué sur une énumération : trois bénéfices indépendants reliés par des flèches qui ne
  signifient rien. Ce sont des cartes ou des piliers.
- Un tableau pour deux options : c'est un avant / après.
- Un chiffre noyé dans un paragraphe : c'est un chiffre héros ou un `kpi`.
- Trois slides de suite du même type (trois schémas pipeline, trois grilles de cartes).

## Trace dans le plan

Dans `plan.md`, chaque ligne porte le rôle, le type retenu et, en une phrase, **pourquoi** (structure du contenu,
impact, place dans le deck) ainsi que l'alternative écartée. C'est ce que l'utilisateur valide au plan.
