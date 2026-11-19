# Spec et plan d'un deck La Grosse Conf (gabarits)

Les deux premières étapes du déroulé de `SKILL.md`. Ce qui manque à la spec devient une question à l'utilisateur,
pas une supposition. À partir d'environ 5 slides, copier la spec dans `docs/slides/<deck>/spec.md` et le plan dans
`docs/slides/<deck>/plan.md` : le `build.py` suit le plan slide par slide, un changement de fond se fait d'abord ici.

---

# Spec — <nom du deck>

## Public

Qui regarde le deck, et ce qu'il sait déjà. Exemple : « les participants de La Grosse Conf, data scientists et
décideurs, qui connaissent le RAG de nom. »

## Message clé

La phrase que le public doit retenir en sortant, en une ligne. Tout le deck la sert.

## Objectif

Ce que le talk doit déclencher : une compréhension, une envie d'essayer, une adhésion. Préciser sa nature
(pédagogique, retour d'expérience, inspiration) : l'autocontrôle de l'agent en dépend (`controle_objectif.md`).

## Format

- Talk (durée), atelier, keynote, ou deck relu sans l'orateur.
- Nombre de slides visé ; un talk de conf : une idée par slide, peu de texte.

## Matière

Les sources fournies (notes, article, deck existant lu avec `extract_text`, chiffres) et ce que chacune apporte.
Chaque chiffre du deck vient d'ici ; s'il manque, il apparaîtra en `[à compléter]`.

## Contraintes

Speaker (nom, poste, photo fournie), date et lieu de la conf pour la couverture, sujets à éviter, langue.
Visuels : pictos et illustrations de la conf seulement ; une photo seulement si l'utilisateur la fournit.

## Faits à confirmer

Les chiffres, dates et noms non vérifiés : une ligne par fait, avec sa source et s'il est affiché. Cette liste est
redonnée telle quelle à la livraison.

## Questions ouvertes

Ce que l'agent n'a pas pu déduire et doit faire trancher avant le plan.

---

# Plan — <nom du deck>

Spec : `spec.md` — message clé : « … »

## Fil du deck

Trois à cinq lignes : comment le talk amène le public au message clé (accroche, constat, mécanisme, preuve, ce qu'il
faut retenir).

## Plan de composition

Une ligne par slide. Pour chaque slide : son rôle (verbe : accrocher, expliquer, comparer, prouver, conclure), sa
recette (`style_grosse_conf.md` §3 : équation, cercles emboîtés, étapes avec boucle, élément central entouré, cycle,
grille de fenêtres, chiffre, focus) ou son layout de rupture (`layouts_grosse_conf.md`), et ses pictos. Deux slides
voisines ne partagent pas plus d'un des trois critères focal / contraste / géométrie, et jamais la même recette.

| # | Titre (≤ 50 caractères, point final) | Rôle | Recette ou layout | Focal (l'aplat rouge) | Pictos / illustration | Matière |
|---|---|---|---|---|---|---|
| 1 | Couverture | ouvrir | `cover` | — | — (dans le layout) | date, lieu |
| 2 | <titre court.> | expliquer | étapes avec boucle (`pipeline`) | l'étape 2, ombre rouge | ecriture, livre, equerre | source |

## Vérifications du plan

- [ ] Chaque titre est court (≤ 50 caractères) et finit par un point ; une idée par slide.
- [ ] Une slide sur deux au moins porte un schéma ou des cartes à picto ; aucune n'est une liste de puces.
- [ ] Un mécanisme (ordre, inclusion, boucle, entourage) a sa recette ; des cas indépendants, une grille sans flèche.
- [ ] Un seul accent rouge fort par slide ; flèches anthracite, boucle de retour rouge.
- [ ] Chaque picto une seule fois par deck ; une illustration au plus par slide, jamais deux fois la même.
- [ ] Ruptures (couverture, sommaire, chapitres, focus) sur les layouts du template, en alternance avec le contenu.
- [ ] Chaque chiffre a sa source dans la spec, sinon `[à compléter]`.
- [ ] Public qui découvre le sujet : chaque terme défini avant de servir, un exemple concret par idée, un même fil
      rouge d'un bout à l'autre, le message clé répété à la fin (`controle_objectif.md`).

## Décisions

Ce qui a changé après validation, et pourquoi (une ligne par décision).
