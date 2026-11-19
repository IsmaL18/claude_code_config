# Autocontrôle : ce que je propose sert-il l'objectif ?

Contrôle que l'agent fait **lui-même**, deux fois : sur le plan, avant de le soumettre, et sur le rendu, avant de
livrer. Il ne produit rien de visible dans le deck ni dans le plan : il sert à retravailler ce qui ne tient pas avant
de le montrer à l'utilisateur. L'objectif du deck et son public viennent de la spec ; l'objectif de chaque slide, de
son rôle, noté dans le plan.

## Pour chaque slide

- **Elle sert l'objectif du deck** : si on la retirait, le public perdrait-il quelque chose d'utile pour atteindre
  l'objectif de la spec ? Sinon, la retirer ou la fusionner.
- **Elle atteint son propre objectif** : le rôle qu'on lui a donné (expliquer, comparer, prouver…) est-il rempli par
  ce qu'elle montre, regardée seule, sur le rendu ? Le titre et le point focal disent-ils la même chose ?
- **Rien n'y est gratuit** : chaque boîte, flèche, chiffre ou visuel sert ce rôle ; ce qui ne le sert pas est retiré.

## Selon la nature du deck

**Pédagogique** (former, expliquer) : la slide est-elle compréhensible pour le public de la spec, à son niveau,
sans le contexte de l'auteur ?
- Les termes techniques et sigles sont introduits avant d'être utilisés, **sur la slide** : une définition qui
  n'est que dans les notes manque à qui lit le deck sans l'orateur (« partagées via APM » → « installées avec APM, un
  gestionnaire de paquets »).
- Chaque texte se lit seul : pas de « Sinon », « Elle » ou « Ce dernier » dont l'antécédent est dans une autre
  boîte.
- Une notion abstraite a un exemple, un cas ou une analogie.
- Le schéma se suit dans l'ordre de lecture et explique le mécanisme sans tout le texte.
- La slide s'appuie sur la précédente et prépare la suivante.

Pour viser la pédagogie maximale (session de formation, acculturation d'un comité de direction) :
- **Une analogie écrite sur la slide**, pas seulement dite : l'apprenti à qui l'on montre des cas résolus (machine
  learning), réviser les annales puis passer l'examen (entraînement), la cuisine et ses ingrédients (données), les
  suggestions du clavier du téléphone (modèle de langage), le thermostat (température), le brief à un nouveau collègue
  (prompt), l'examen à livre ouvert (RAG), le bibliothécaire qui range par sujet (embeddings).
- **Un même exemple suivi d'un bout à l'autre** : la même demande posée à chaque étape d'un processus, en bulles ; le
  même cas métier (la demande de chaleur d'un quartier) d'une slide à l'autre.
- **Un objet réel plutôt qu'une liste de critères** : un relevé de données avec ses défauts entourés vaut mieux que
  « quantité, qualité, étiquetage » en trois cartes ; une vraie capture d'outil vaut mieux qu'une description.
- **Des moments où le public agit**, annoncés dans l'agenda : tour de table, quiz à main levée, « vrai ou faux »
  dont les réponses arrivent en fin de partie, défi pendant la pause.
- **Un repère de progression** dans une session longue : agenda en piste proportionnelle, fil d'onglets sur chaque
  chapitre.
- **Le public relit la slide sans l'orateur** : chaque terme y est défini (une ligne suffit : « **GMAO** : le logiciel
  de gestion de la maintenance »), les données illustratives sont dites illustratives (dans la slide ou les notes).
- **Mesurer plutôt qu'inventer** : un découpage en tokens, un compte, un ordre de grandeur se vérifient avec l'outil
  réel (une capture), sinon ils restent `[à compléter]` ou passent dans « Faits à confirmer ».

**Commercial** (proposer, convaincre) : comprend-on les enjeux et les impacts pour le client ?
- L'enjeu du client (son objectif, son risque) est clair, dans ses termes à lui.
- L'impact est concret : ce qui change pour lui, chiffré si la matière le permet (sinon `[à compléter]`).
- Une slide qui parle de nous (démarche, équipe, outil) dit aussi ce que le client y gagne.
- Les promesses ont une preuve (référence, résultat, démonstration), ou leur absence est signalée.

**Interne** (décider, informer) : la décision attendue ou l'information clé ressort-elle sans effort ?

## Quand ça ne tient pas

Retravailler avant de soumettre : changer le type de slide, le titre, le point focal ou le contenu, dans le plan,
puis relancer le build. Ne pas compenser par du texte en plus. Ce qui reste fragile et dépend de l'utilisateur (une
preuve manquante, un chiffre à confirmer, un terme à valider) lui est signalé en une phrase.
