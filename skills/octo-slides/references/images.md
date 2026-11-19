# Illustrer un deck : où trouver les images, et comment les poser

Un deck pédagogique se retient par ses images : une vraie capture, une une de presse, la photo de l'installation dont
on parle. Ce fichier dit où les chercher, dans quel ordre, avec quels outils, et comment les poser dans la charte.
La charte (`charte.md`, « Logos et visuels ») prime : visuels OCTO d'abord, jamais de visuel en rectangle droit,
pas d'image générée par IA sans demande explicite.

## 1. L'ordre de recherche

| # | Source | Pour | Outil |
|---|---|---|---|
| 1 | Bibliothèque OCTO : pictos, illustrations, visuels 3D, avatars | concepts, chapitres, personas | `pictos-index.md`, `illustrations.md`, `ModeleDeck.borrow` |
| 2 | Decks OCTO existants (formations, références) | captures d'outils, schémas déjà faits, unes de presse | `scripts/extract_images.py` |
| 3 | Wikimedia Commons (licences libres) | photos réelles : installation industrielle, portrait historique, matériel | `scripts/commons.py` |
| 4 | Capture faite soi-même | montrer un outil en vrai (un tokenizer, une interface) | Chrome DevTools (MCP), `take_screenshot` |
| 5 | Emplacement « Image à insérer » | rien de libre ne convient, et l'utilisateur veut une image | `Deck.image_slot` |

Les sources 2 à 5 ne servent que si l'utilisateur demande des images d'illustration (« mets des images », « illustre
bien les slides ») : sans cette demande, la charte réserve les visuels aux fichiers OCTO.

Une image trouvée sur le web par une recherche générale (Google Images, Firecrawl) **sert d'inspiration, pas de
contenu** : ses droits sont inconnus. On s'en inspire pour dessiner le schéma avec les helpers, ou on cherche
l'équivalent libre sur Commons.

## 2. Reprendre les images d'un deck OCTO

```bash
uv run --with python-pptx --with pillow python <SKILL_DIR>/scripts/extract_images.py formation.pptx tmp/formation
```

Lire les planches `tmp/formation/planche_*.png`, retenir les images utiles, les copier (allégées) dans un dossier
`images/` du deck. On reprend des contenus (une capture de ChatGPT, le schéma d'un neurone, une une de presse), jamais
le style du deck source. Vérifier ce qu'on reprend :
- une capture qui contient une faute ou un exemple faux ne se reprend pas : refaire la capture (§4) ;
- un schéma aux couleurs hors charte (flèches rouges) se signale à l'utilisateur, ou se redessine ;
- une image générée par IA ne se reprend que si elle est l'objet de la démonstration (l'effet d'un prompt), pas
  comme décoration, et on le dit à l'utilisateur.

## 3. Wikimedia Commons

```bash
python3 -I <SKILL_DIR>/scripts/commons.py search tmp/images "turbine|steam turbine power plant" "pompe|centrifugal pump"
# lire tmp/images/planche_*.png, noter les titres retenus dans index.json, puis :
python3 -I <SKILL_DIR>/scripts/commons.py fetch docs/slides/<deck>/images "turbine=File:Westinghouse steam turbine 01.jpg"
```

- Seuls le domaine public, CC0, CC BY et CC BY-SA sont gardés ; les crédits vont dans `images/credits_commons.json`.
- Requêtes en anglais ; pour une installation industrielle, essayer aussi l'allemand (« Dampfturbine Kraftwerk »,
  « Biomasseheizwerk »). Plusieurs passes sont normales : la première trouve rarement tout.
- Écarter : les photos floues ou en noir et blanc d'archive quand on montre l'actuel, les images avec du texte
  étranger, les rendus générés par IA (Commons en contient, titres « DALL·E »…).
- Ce qui n'existe pas en libre (ImageNet, une capture d'un produit commercial) : changer d'image en gardant le
  message (une puce graphique pour « 2012, le deep learning décolle »), dessiner l'élément (un clavier de téléphone
  et ses suggestions en formes), ou poser un emplacement.

## 4. Faire une capture

Avec le MCP Chrome DevTools : ouvrir la page dans un contexte isolé, saisir l'exemple, `take_screenshot`, puis rogner
la zone utile (Pillow). Taper au clavier (`type_text`) quand le remplissage direct (`fill`) ne déclenche pas le calcul
de la page.

- Une page qui demande une vérification « humain » (Cloudflare, captcha) ne se contourne pas : prendre un outil libre
  équivalent (Tiktokenizer, `tiktokenizer.vercel.app`, plutôt que le tokenizer d'OpenAI), ou demander la capture à
  l'utilisateur.
- **La capture vérifie le chiffre** : un découpage en tokens, un compte, un temps de réponse affichés sur une slide se
  mesurent, ils ne s'inventent pas. Sur le deck CCIAG, la capture a corrigé un découpage imaginé (« CCIAG » coûte
  trois tokens, pas deux) et l'ordre de grandeur (1,3 token par mot).

## 5. Poser une image dans la charte

| Helper | Usage |
|---|---|
| `d.photo(s, image, *zone, shape="tl-br", anchor="mc")` | photo ou capture qui remplit la zone, recadrée sans déformation, découpée en coins opposés arrondis, goutte (`"goutte"`), cercle (`"rond"`) ; `anchor="tc"` garde le haut (une capture, un visage, une une) |
| `d.photo_fit(s, image, *zone)` | image entière, centrée, posée dans un `bloc` blanc : schéma, capture à lire en entier. Marge dans le bloc d'au moins 0,36 × le rayon (`zone = bloc.pad(0.36 * radius)`) : en deçà, le coin carré de l'image sort de l'arrondi |
| `d.image_slot(s, *zone, "sujet")` | emplacement gris « Image à insérer » + sujet ; `shape="goutte"` pour une petite goutte. Listé par `save()` avec son numéro de slide, pour la livraison |

Des gouttes photo sur une frise (une image par jalon), une capture face à un graphique, une une de presse posée sur
la courbe d'adoption : l'image porte l'information, elle n'est pas un décor. Au plus un visuel fort par slide hors
frises et galeries.

Après import dans Google Slides, vérifier les images découpées (goutte, coins arrondis) : c'est l'élément le plus
fragile.

## 6. Créditer

Les licences CC BY et CC BY-SA demandent l'auteur et la licence. Une slide « Crédits des images » avant la clôture :
une ligne par image, `numéro de slide · sujet · auteur · licence` (`commons.credit_line(credit)` met en forme les
deux derniers), et une colonne pour les images reprises d'un deck OCTO (« capture de ChatGPT 3.5, formation FDXIA »).
La page d'origine de chaque photo reste dans `credits_commons.json`.

## 7. Chercher l'inspiration pour un concept pédagogique

Une notion résiste : on ne voit pas sa forme (« comment montrer la température d'un modèle ? »), la slide est faite
« que de carrés », ou l'utilisateur la trouve « pas claire ». Avant de recomposer, regarder comment d'autres l'ont
dessinée : une mosaïque de résultats d'images montre en un coup d'œil les formes qui reviennent, celles que des
centaines d'auteurs ont trouvées pour la même idée.

1. **Deux ou trois requêtes**, en anglais (plus de résultats) : la notion + « explained », « diagram », « simply »,
   « infographic » ou « analogy » ; une en français avec « schéma » si le sujet est français.
2. **Capturer les mosaïques** :
   ```bash
   uv run --with pillow python <SKILL_DIR>/scripts/inspiration.py tmp/inspiration \
       "temperature|LLM temperature explained diagram" "temperature2|LLM temperature analogy"
   ```
   Bing Images, par Chrome sans interface : une planche `inspiration_<clé>.png` par requête. Sans Chrome : le MCP
   Chrome DevTools sur `bing.com/images/search?q=…` (refuser les cookies, capture pleine page). Google Images renvoie
   une page « trafic inhabituel » (captcha) aux navigateurs pilotés : ne pas la contourner, Bing montre la même
   mosaïque. En dernier recours, la recherche web de la session (texte seul) ou Firecrawl s'il est installé
   (`npm install -g firecrawl-cli`, `firecrawl login --browser` : le plugin seul ne suffit pas).
3. **Lire les planches et nommer les formes qui reviennent**, pas une image en particulier. Relevé du 30/10/2026 :
   - température d'un modèle : un curseur « déterministe ↔ créatif », deux histogrammes de probabilités côte à côte
     (pointu à basse température, aplati à haute), un thermomètre ou un cadran, la même phrase complétée autrement ;
   - embeddings : un nuage de points en deux dimensions groupés par sens, « roi − homme + femme = reine », un objet
     qui entre dans un modèle et ressort en liste de nombres ;
   - RAG : le sigle décomposé lettre par lettre (Retrieve, Augment, Generate), deux phases séparées (indexer les
     documents, puis répondre), question → recherche → modèle → réponse.
4. **Choisir la forme qui sert le rôle de la slide** (`types_de_slides.md`), la noter dans `plan.md` (« inspiration :
   deux histogrammes comparés, curseur »), puis la **redessiner avec les helpers**, dans la charte : marine et
   turquoise, formes de la Com, exemple tiré du métier du public. Rien n'est copié : ni l'image, ni ses couleurs, ni
   son style.

Les planches restent dans `tmp/` : elles ne vont ni dans le deck, ni dans le dossier du deck.
