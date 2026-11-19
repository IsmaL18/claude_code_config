# Fichier de retours

Chaque deck livré est accompagné d'un `retours.md`, écrit par `scripts/retours.py`, qui sert à l'utilisateur à
faire ses retours sans recopier de texte ni décrire où se trouve un élément. Il l'utilise ou non : le fichier est
produit dans tous les cas.

## Ce qu'il contient

- Un mode d'emploi repliable (encadré Obsidian `> [!info]-`, lisible comme une citation ailleurs), avec un exemple
  par geste.
- « Tout le deck » : les retours d'ensemble.
- Pour chaque slide : la capture du rendu, puis tout son texte, un élément par ligne, repéré `[slide.élément]` et
  rangé par bloc dans l'ordre de lecture (`- [2.4] Titre de bloc : …`), puis les rubriques « Design » et
  « Remarques ».
- Une empreinte en dernière ligne (commentaire HTML) : elle dit si le fichier a été rempli, et sur quel état du deck
  il a été écrit.

Le texte reprend le balisage des helpers : `**gras**` (omis quand toute la phrase est en gras, comme un titre),
`==mot==` pour un mot-clé à la couleur d'accent de la charte (sur fond foncé), ` / ` pour un retour à la ligne.

## Les trois gestes de l'utilisateur

1. **Corriger ou reformuler** : il réécrit le texte après les deux-points.
2. **Confier une consigne** : une ligne `→ …` sous l'élément (« → plus court », « → 2 propositions »). `-->` et
   `->` sont lus comme `→`.
3. **Remarquer un point de design** : une puce sous « Design », avec un repère ou une position.

## Écrire le fichier

```bash
uv run --with python-pptx python <SKILL_DIR>/scripts/retours.py write <deck>.pptx <dossier du rendu> [retours.md]
```

Après le rendu et la relecture, à chaque livraison (première version comme retouche). Par défaut le fichier va à
côté du `.pptx`. Un `retours.md` resté intact est remplacé ; un `retours.md` rempli est d'abord archivé
(`retours_v1.md`, `retours_v2.md`…) : l'historique des retours se garde avec le deck.

Le fichier reconnaît les blocs aux noms que les helpers donnent à leurs formes (`Bloc`, `Panneau`, `Périmètre`,
`Capsule`, `Fenêtre`) : un bloc dessiné sans titre, dont le texte est posé à part, est quand même
regroupé.

## Lire les retours

Quand l'utilisateur annonce ses retours, ne pas relire le fichier à l'œil :

```bash
uv run --with python-pptx python <SKILL_DIR>/scripts/retours.py diff retours.md <deck>.pptx
```

La commande compare le fichier au texte du deck et liste les textes modifiés (avant / après), les consignes avec
leur repère, les remarques de design et les remarques libres, et les repères effacés (texte supprimé ou repère abîmé,
à vérifier). Elle prévient si le deck a changé depuis l'écriture du fichier : lancer le `diff` avant de régénérer.

Puis :
- reporter chaque texte modifié dans `build.py` ; corriger au passage l'orthographe, la typographie et la charte
  (point médian, emoji, capitales) d'un texte réécrit, et le dire à la livraison ;
- traiter chaque consigne et chaque remarque, ou dire pourquoi elle ne l'est pas ;
- un texte réécrit qui ne tient plus : le resserrer au plus près de la formulation de l'utilisateur, et le signaler
  dans le nouveau fichier par une ligne `→ Claude : votre version : « … »` sous l'élément, pour qu'il arbitre ;
- régénérer, rendre, relire, puis réécrire le fichier (`write`) : le fichier rempli est archivé.

Une remarque de design signalée sur un bloc vaut souvent pour toute la série (« valable pour les 6 blocs ») :
vérifier les éléments semblables, comme pour un retour slide par slide.
