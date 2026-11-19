# Plan — <nom du deck>

<!-- Gabarit de plan d'un deck OCTO (étape 2 du déroulé de SKILL.md), dérivé de la spec validée.
Copier dans docs/slides/<deck>/plan.md. Le build.py suit ce plan slide par slide ; un changement de fond se fait
ici d'abord, puis on relance le build. -->

Spec : `spec.md` — message clé : « … »

## Fil du deck

Trois à cinq lignes : comment le deck amène le public au message clé (constat, proposition, preuve, appel à l'action).

## Type de chaque slide

Pour chaque slide (`types_de_slides.md`) : son rôle (verbe), la structure de son contenu, le type retenu et
pourquoi, l'alternative écartée. La colonne Schéma ? applique le test de `types_de_slides.md` (relations, flèches
porteuses, lisible sans légende). Se fait **avant** la composition.

| # | Rôle | Structure du contenu | Schéma ? | Type retenu | Pourquoi (pédagogie, impact, style) | Écarté |
|---|---|---|---|---|---|---|
| 2 | expliquer | flux en 3 étapes, des traces par étape | oui : relations nommables, flèches porteuses | schéma pipeline, preuves accrochées | la causalité se voit avant de se lire | colonnes de texte : perdent l'ordre |
| 3 | frapper | un chiffre qui change la perception | non : une grandeur, rien à relier | chiffre héros | point focal immédiat, respiration après un schéma dense | kpi dans un bandeau : trop discret |
| 4 | convaincre | trois bénéfices indépendants | non : pas de relation entre eux | piliers | chaque bénéfice lisible seul | schéma : flèches décoratives |

## Plan de composition

Une ligne par slide (`style.md`, « Intentions de design »). Deux slides voisines ne partagent pas plus d'un des
trois critères focal / contraste / géométrie. Pour une slide à schéma, la colonne Géométrie **nomme le schéma** :
ses nœuds, ses flèches, ses boucles (« demande → 3 étapes → livrable, preuves accrochées sous chaque étape,
conclusion marine »), pas seulement « 4 cartes » ou « 3 colonnes ».

| # | Titre-message | Focal | Contraste | Géométrie | Point de départ | Modèles consultés | Matière |
|---|---|---|---|---|---|---|---|
| 1 | Couverture : <titre> | titre | fond du layout | — | layout 41 | — | spec |
| 2 | <phrase affirmative> | … | … | … | helpers / modèle n / layout NN / maquette | 43, 46 (planche 04) | source, chiffre |

Point de départ : `helpers` (composition libre), `modèle n` (slide préformatée transformée, `modeles_index.md`),
`layout NN` (`layouts.md`), `borrow n` (visuel pioché dans un modèle), `maquette` (fournie par l'utilisateur,
reproduite : `mise_en_page.md` §7). Modèles consultés : les slides préformatées regardées pour composer la slide,
même quand elles ne servent que de référence (planches 01 et 04, et celle de la partie du contenu).

## Variantes (si demandées)

| # | Variante | Focal | Contraste | Géométrie | Ce qu'elle privilégie |
|---|---|---|---|---|---|
| 2 | A | … | … | … | la lecture seule (envoyée par mail) |
| 2 | B | … | … | … | la projection (peu de texte, un chiffre héros) |

Deux variantes d'une même slide diffèrent par au moins deux des trois critères.

## Vérifications du plan

- [ ] Chaque slide a un rôle (verbe) et un type choisi pour ce rôle, avec son pourquoi et l'alternative écartée.
- [ ] Chaque titre est une phrase-message (pas un nom de section), 70 caractères au plus.
- [ ] Pour chaque slide, la question du schéma est tranchée : un mécanisme a son schéma nommé dans Géométrie ;
      un contenu sans mécanisme n'en a pas (pas de schéma décoratif).
- [ ] Le message clé de la spec est porté par au moins une slide, idéalement la dernière avant la clôture.
- [ ] Aucun dispositif de contraste ne revient plus de deux fois sur six slides ; un visuel 3D au plus par slide,
      jamais deux fois le même.
- [ ] Chaque chiffre a sa source dans la spec, sinon `[à compléter]` ; un fait « à confirmer » affiché est dans la
      liste de la spec, qui sera redonnée à la livraison.
- [ ] Un chiffre qui revient sur plusieurs slides garde le même périmètre et la même date, ou dit le sien
      (« +2 400 tests backend » face à « 2 454 tests back, 871 front ») : sinon le public croit à une contradiction.
- [ ] Public qui découvre le sujet (deck pédagogique, autre équipe) :
  - [ ] chaque terme technique ou sigle est défini avant de servir, ou au moment où il sert (une définition en clair
        dans la boîte, `nested` pour plusieurs termes emboîtés), sur la slide et pas seulement dans les notes ;
  - [ ] chaque idée à retenir a sa slide, et chaque notion abstraite son exemple concret (un cas vécu, une phrase
        qu'on dit à l'outil, un chiffre réel) ;
  - [ ] le message clé est répété dans la dernière slide de contenu, pas seulement en ouverture.
  - [ ] pédagogie maximale (formation, acculturation) : une analogie écrite sur les slides clés, un même exemple
        suivi d'un bout à l'autre, un objet réel annoté plutôt qu'une liste de critères, des moments où le public
        agit (quiz, vrai ou faux), un repère de progression (`controle_objectif.md`).
- [ ] Style des modèles OCTO (`modeles.md`, « Le style filaire OCTO ») : chaque slide nomme l'élément des modèles
      qu'elle réutilise (médaillon, capsule, onglet, puce cible, visuel 3D en goutte, illustration au trait,
      composition empruntée, avec son id d'`assets_modeles.md`) ; au moins une slide sur deux ; aucun picto nu.
- [ ] Chaque mécanisme qui a une forme est dessiné (nuage de points, histogramme, réseau, mini-schéma par élément),
      avec un ordre de lecture évident ; pas de slide « que des carrés » (`style.md`, intentions 9 et 10).
- [ ] Images : leur source est décidée (bibliothèque OCTO, deck OCTO existant, Wikimedia Commons, capture,
      emplacement « Image à insérer ») et la slide de crédits est prévue si une image est sous licence libre
      (`images.md`).
- [ ] Chaque slide cite les modèles OCTO consultés (ou « — » pour un layout du template).
- [ ] Variantes demandées : deux variantes d'une même slide diffèrent par au moins deux critères sur trois.

## Décisions

Ce qui a changé après validation, et pourquoi (une ligne par décision).
