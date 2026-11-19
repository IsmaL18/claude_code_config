# Charte graphique OCTO (règles officielles)

Sources : charte graphique OCTO 2025, slides préformatées OCTO 2026 (Drive), mini guide accessibilité OCTO, page Confluence de la Com.
**Ces règles priment sur tout le reste** du skill, y compris sur `style.md` : en cas de doute, la charte gagne.

## Couleurs principales (bichrome)

| Rôle | Hex | Usage |
|---|---|---|
| Principale | `#0E2356` (bleu marine) | texte, titres, traits et contours, aplats d'en-tête |
| Secondaire | `#00D2DD` (bleu turquoise) | accents : aplats de mise en avant, filets, flèches de retour, pastilles, puces, série mise en avant d'un graphique |

**Turquoise et texte** :
- **Jamais de texte turquoise sur fond clair** (blanc, teintes claires) : contraste de 1,8:1, illisible.
- Sur fond bleu marine, le texte turquoise est autorisé pour un mot-clé ou un chiffre mis en avant, pas pour un paragraphe.
- Exception partout : le **point final turquoise** des titres de couverture, de slides « héros » et d'accroches (« Couleurs. »), et le point du numéro de page (« .12 », géré par le template) ou d'un onglet numéroté (« .01 » de `pillar_card`).
- Tout texte posé sur du turquoise est en bleu marine, jamais en blanc.

## Couleurs secondaires autorisées

N'utiliser **que** ces teintes, en plus du blanc `#FFFFFF`. Aucune autre couleur, y compris pour les ombres, dégradés ou couleurs d'état. Elles servent au relief, à la hiérarchie et aux schémas, pas à décorer.

Gamme bleu marine (du plus foncé au plus clair) :
`#0E2356` `#263967` `#3E4F78` `#586586` `#6E7B9A` `#8691AB` `#9FA7BB` `#B7BDCC` `#CFD3DD` `#DBDEE6` `#E7E9EE` `#F3F4F7`

Gamme turquoise (du plus saturé au plus clair) :
`#00D2DD` `#3CD7E0` `#5BDDE4` `#72DFE7` `#8AE4EB` `#9EE9ED` `#B2EEF2` `#C6F1F5` `#DAF6F9` `#EBFAFB`

Les teintes claires de turquoise ne servent jamais pour du texte. Les gris sont toujours des teintes de marine, jamais un gris neutre. Pas de rouge, d'orange ni de vert, même pour des statuts.

Constantes correspondantes dans `octo_slides.py` : `NAVY`, `NAVY_90` … `NAVY_5` et `TURQ`, `TURQ_90` … `TURQ_10` (voir le haut du fichier).

## Usages recommandés

- **Texte sur fond clair** : `#0E2356` (principal), `#3E4F78` (secondaire), `#586586` (discret, pas en dessous de 10 pt).
- **Texte sur fond bleu marine** : blanc (principal), `#CFD3DD` (secondaire), `#B7BDCC` (discret), `#00D2DD` (mot-clé).
- **Fonds** : blanc par défaut ; alternance `#EBFAFB` ou `#F3F4F7` ; bleu marine pour une couverture, un bandeau ou une section de mise en avant. Pas de fond marine plein sur une page de contenu.
- **Cartes et encadrés** : fond blanc, contour marine fin (0,75 à 1 pt), **sans ombre portée**.
- **Filets et séparateurs** : pointillés ou traits fins marine, ou `#CFD3DD`.
- **Pastilles et étiquettes** : fond `#00D2DD` ou `#C6F1F5`, texte marine.

## Hiérarchie des aplats (schémas)

1. **Marine plein, texte blanc** : élément de plus haut niveau, en-tête, conclusion.
2. **Turquoise plein, texte marine** : élément mis en avant, cœur du dispositif.
3. **Teintes de turquoise (`#C6F1F5`, `#DAF6F9`, `#B2EEF2`…), texte marine** : regroupements, niveaux intermédiaires.
4. **Blanc, contour marine, texte marine** : contenu courant, la majorité des cartes.

Un schéma OCTO est à 80 % blanc et marine au trait, avec un ou deux aplats turquoise et au plus un aplat marine.

## Formes signature

- **Rectangle à coins asymétriques** : grand rayon (20 à 40 % du petit côté) sur 2 ou 3 coins, au moins un coin vif, le plus souvent en haut à droite.
- **Goutte** (cercle avec un coin vif) pour les visuels, **pilules** pour les étiquettes et les étapes, **onglets** posés sur le bord haut d'une carte.
- Visuels jamais en rectangle droit : goutte, cercle ou coins opposés arrondis.
- **Flèches de flux** : marine épaisses (3 à 4 pt), pointe en chevron ouvert. **Boucles de retour** : turquoise épaisses. **Liens secondaires** : pointillés marine fins. Transition entre deux blocs : chevron turquoise isolé « > ».
- Le sigle en haut à gauche signe chaque slide (géré par le template).

## Typographie

- **Une seule police : Outfit**, pour les titres comme pour le texte courant.
- Texte en **bleu marine, jamais en noir**.
- Hiérarchie par la taille et la graisse : Bold pour les titres et les mots-clés, Regular pour le texte, Light pour les très grands chiffres.

## Rédaction et mise en forme du texte

- **Orthographe et typographie soignées** (lecture par les synthèses vocales) : espaces insécables avant « ; : ! ? % » et à l'intérieur des guillemets français, apostrophes et guillemets cohérents.
- **Écriture inclusive sans point médian** : jamais « content·e·s » ni « content.e.s ». Écrire « content-es », « content(e)s », ou reformuler.
- **Limiter les capitales** : majuscule en début de phrase et aux noms propres uniquement. Pas de titres, libellés ni mots en capitales pour insister.
- **Pas d'italique.** Les citations se marquent avec des guillemets (« » ou “ ”).
- **Soulignement réservé aux liens** ; pour mettre en valeur : gras, encadré, surlignage.
- **Aligner à gauche** : pas de texte justifié ni de paragraphe centré (une phrase-message courte peut être centrée).
- **Ne pas transmettre une information par la seule couleur** : doubler par une forme, un picto ou un libellé. Une slide doit rester compréhensible imprimée en noir et blanc.
- **Aérer** : interligne d'environ 1,5 pour le texte courant (pas nécessaire pour les titres).
- **80 caractères maximum par ligne** : préférer deux colonnes à une colonne trop large.
- Décimales avec virgule. Ne pas mélanger français et anglais dans un même deck.

## Contrastes (matrice OCTO, mini guide accessibilité)

✓✓ = contraste suffisant ; ✓ = gros caractères uniquement (18 pt regular ou 14 pt bold minimum) ; vide = insuffisant.

| Fond ↓ / texte → | blanc | `#0E2356` | `#3E4F78` | `#586586` | `#6E7B9A` | `#9FA7BB` | `#B7BDCC` | `#CFD3DD` | `#E7E9EE` | `#00D2DD` |
|---|---|---|---|---|---|---|---|---|---|---|
| blanc | | ✓✓ | ✓✓ | ✓✓ | ✓ | | | | | |
| `#0E2356` | ✓✓ | | | | ✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ |
| `#3E4F78` | ✓✓ | | | | | ✓ | ✓ | ✓✓ | ✓✓ | ✓ |
| `#586586` | ✓✓ | | | | | | ✓ | ✓ | ✓✓ | ✓ |
| `#6E7B9A` | ✓ | ✓ | | | | | | | ✓ | |
| `#9FA7BB` | | ✓✓ | ✓ | | | | | | | |
| `#B7BDCC` | | ✓✓ | ✓ | ✓ | | | | | | |
| `#CFD3DD` | | ✓✓ | ✓✓ | ✓ | | | | | | |
| `#E7E9EE` | | ✓✓ | ✓✓ | ✓✓ | ✓ | | | | | |
| `#00D2DD` | | ✓✓ | ✓ | ✓ | | | | | | |

À retenir : le turquoise n'est pas lisible sur du blanc, ni le blanc sur du turquoise. Sur turquoise, écrire en marine.

La matrice suit les seuils WCAG AA : 4,5:1, et 3:1 pour les gros caractères. `octo_lint.py` mesure le contraste de
chaque texte sur son fond (la forme du texte, la forme pleine dessous, ou le fond de la slide) et signale ce qui
passe sous le seuil. Repères : turquoise sur marine 8,1:1, blanc sur marine 15,1:1, marine sur `#72DFE7` 9,6:1,
turquoise sur blanc 1,9:1. Une capture d'écran macOS (profil Display P3) ne donne pas les valeurs de la charte :
juger une couleur sur le `.pptx`, pas sur la capture.

## Logos et visuels

- Logos dans `assets/logos/` : `logo-corporate-*` (documents officiels), `logo-code-*` (publications, refcards, événements), `sigle-*`. Déclinaison `couleur` ou `noir` sur fond clair, `blanc` sur fond marine. Jamais recolorés, déformés ni redessinés.
- Pictos (`references/pictos-index.md`), avatars (`references/avatars.md`) et illustrations (`references/illustrations.md`) : uniquement les fichiers OCTO fournis. Pas de banque d'images, d'icônes génériques ni d'emoji.
- Pas d'image générée par IA sans demande explicite (engagement RSE d'OCTO). Sans photo du catalogue OCTO (Drive), utiliser une illustration, un picto ou un aplat.

## Vérification avant livraison

- Aucun texte turquoise sur fond clair (seul le point final d'un titre de couverture, de slide héros ou d'accroche).
- Aucune couleur hors des deux gammes ci-dessus, aucun texte noir.
- Outfit seule police.
- Logos et pictos : fichiers de `assets/`, non modifiés, dans la bonne déclinaison pour le fond.
- Aucune consigne interne du gabarit reprise (« A adapter à sa situation », « ici mettre une photo », « Lorem ipsum »).
- Texte relu : orthographe, espaces insécables, aucun point médian, pas de capitales ni d'italique superflus, citations entre guillemets.
