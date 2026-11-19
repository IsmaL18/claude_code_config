# Spec et plan d'un deck Accenture (gabarits)

Les deux premières étapes du déroulé de `SKILL.md`. Ce qui manque à la spec devient une question à l'utilisateur, pas
une supposition. À partir d'environ 5 slides, copier la spec dans `docs/slides/<deck>/spec.md` et le plan dans
`docs/slides/<deck>/plan.md` : le `build.py` suit le plan slide par slide, un changement de fond se fait d'abord ici.

---

# Spec — <nom du deck>

## Public

Qui regarde le deck, et ce qu'il sait déjà. Exemple : « le comité de direction d'un client Accenture, qui connaît
l'IA générative de nom et attend une feuille de route. »

## Message clé

La phrase que le public doit retenir en sortant, en une ligne. Tout le deck la sert.

## Objectif

Ce que le deck doit déclencher : une décision, une adhésion, une compréhension. Préciser sa nature (proposition,
présentation, formation, retour d'expérience) : l'autocontrôle de l'agent en dépend (`controle_objectif.md`).

## Format

- Présentation projetée (20 mots par slide au plus, 16 pt minimum) ou document lu sans l'orateur.
- Langue du deck (`AccentureDeck(lang="en-US")` pour l'anglais) ; nombre de slides visé.

## Matière

Les sources fournies (notes, article, deck existant lu avec `extract_text`, chiffres) et ce que chacune apporte.
Chaque chiffre du deck vient d'ici ; s'il manque, il apparaîtra en `[à compléter]`.

## Contraintes

Client, date, auteur pour la couverture ; mention de confidentialité (proposition ou présentation : modèles de fin de
la bibliothèque) ; sujets à éviter. Visuels : icônes et bibliothèque Accenture seulement ; une photo seulement si
l'utilisateur la fournit ou si elle vient de la banque d'images de la marque.

## Faits à confirmer

Les chiffres, dates et noms non vérifiés : une ligne par fait, avec sa source et s'il est affiché. Cette liste est
redonnée telle quelle à la livraison.

## Questions ouvertes

Ce que l'agent n'a pas pu déduire et doit faire trancher avant le plan.

---

# Plan — <nom du deck>

Spec : `spec.md` — message clé : « … »

## Fil du deck

Trois à cinq lignes, sur la structure d'histoire du starter pack : l'accroche, le contexte, la mission, l'obstacle,
les capacités (3 ou 4), le dénouement, l'appel à l'action.

## Plan de composition

Une ligne par slide : son rôle (verbe : accrocher, expliquer, comparer, prouver, conclure), son composant
(`style_accenture.md` §3), son modèle de la bibliothèque (numéro de `modeles_index_accenture.md`) ou son layout de
rupture (`layouts_accenture.md`), et son focal (le seul violet fort). Deux slides voisines n'ont pas le même composant.

| # | Titre (une ligne, sans point final) | Rôle | Composant, modèle ou layout | Focal (le violet) | Icônes | Matière |
|---|---|---|---|---|---|---|
| 1 | Couverture | ouvrir | `cover` | — | — | client, date |
| 2 | <titre-message> | expliquer | `etapes` | l'étape 3 | — | source |

## Vérifications du plan

- [ ] Chaque titre est un message, sur une ligne, sans point final ; une idée par slide.
- [ ] Une slide sur deux au moins porte un visuel (composant, modèle de la bibliothèque) ; aucune n'est une liste de
      puces.
- [ ] Un seul violet fort par slide ; le blanc reste la base, les fonds foncés pour les ruptures.
- [ ] Ruptures (couverture, agenda, intercalaires, messages clés, fin) sur les layouts du template.
- [ ] 20 mots par slide projetée au plus ; le discours dans les notes.
- [ ] Chaque chiffre a sa source dans la spec, sinon `[à compléter]`.
- [ ] Public qui découvre le sujet : chaque terme défini avant de servir, un exemple concret par idée, le message clé
      répété à la fin (`controle_objectif.md`).

## Décisions

Ce qui a changé après validation, et pourquoi (une ligne par décision).
