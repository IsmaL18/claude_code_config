# Charte graphique Accenture (règles du starter pack)

Règles relevées dans le « Accenture PPT Starter Pack » (version aux polices système : Arial et Palatino Linotype),
slides « Getting started », « How to make your story impactful », « Colors and gradients », « Fonts » et
« Iconography ». Elles priment sur `style_accenture.md`. Pour toute question de marque non couverte ici, le starter
pack renvoie à brandsupport@accenture.com.

## Couleurs

Palette primaire, en constantes dans `scripts/accenture_slides.py` :

| Rôle | Constante | Hex | Texte lisible dessus |
|---|---|---|---|
| Core Purple 1 : accent, chiffres, icônes, le « > » | `PURPLE` | #A100FF | blanc |
| Core Purple 2 : aplats, fonds | `PURPLE_DARK` | #7500C0 | blanc |
| Core Purple 3 : fonds foncés | `PURPLE_DARKEST` | #460073 | blanc |
| Accent | `MAUVE` | #B455AA | noir (blanc seulement au-dessus de 18 pt) |
| Accent clair | `LAVENDER` | #BE82FF | noir |
| Accent très clair, mot-clé sur fond foncé | `LILAC` | #DCAFFF | noir |
| Sous-titre de couverture sur fond foncé | `LILAC_LIGHT` | #E6DCFF | noir |
| Texte, titres | `BLACK` | #000000 | blanc |
| Gris chaud | `GREY` | #96968C | noir |
| Gris chaud clair : panneaux, filets | `GREY_LIGHT` | #E6E6DC | noir |
| Blanc | `WHITE` | #FFFFFF | noir |

- Le violet est la couleur de la marque : **un seul violet fort par slide** (l'étape focale, le chiffre, le panneau
  d'arrivée), le reste en noir, blanc et gris chaud.
- Les dégradés de la marque (Dark, Mid, Core, Light) ne s'utilisent qu'à travers les layouts du template
  (intercalaires, messages clés, couvertures) : jamais de dégradé dessiné dans une forme (Google Slides ne le rend
  pas, et la marque ne le prévoit pas).
- Pour l'impression, préférer les layouts à fond blanc.
- Aucune couleur hors de cette palette : ni le marine ou le turquoise d'OCTO, ni le rouge ou l'anthracite de La
  Grosse Conf. Le starter pack barre #A055F5 (pas une couleur de thème) : à ne pas utiliser.

## Contrastes

Seuils WCAG AA, contrôlés à l'enregistrement : 4,5:1 pour le texte courant, 3:1 au-dessus de 18 pt ou en gras au-dessus
de 14 pt.

- Fond blanc ou gris clair : texte noir ; violet #A100FF ou plus foncé pour un accent (5,3:1 sur blanc) ; jamais de
  texte en #BE82FF, #DCAFFF ni #96968C en petite taille.
- Fond violet foncé (#460073, #7500C0) ou noir : texte blanc, #DCAFFF en secondaire.
- Fond #A100FF : texte blanc.

## Typographie

- **Arial** pour tout le texte courant (Graphik, la police de marque, quand elle est installée : le starter pack
  fourni ici est la version Arial, à garder).
- **Arial Black** pour les titres, les intitulés de carte et de colonne, les chiffres clés (`headline()`), en
  remplacement de Graphik Bold.
- **Palatino Linotype** pour les sous-titres de couverture, d'intercalaire et les accroches (`serif()`), en
  remplacement de GT Sectra Fine : un peu d'« humanité » sur les couvertures et les intercalaires seulement.
- Titres en phrase, sans point final, sur une ligne ; pas de capitales pour insister, pas d'italique.
- Texte : 16 pt minimum dans un deck projeté (« Go easy on the eyes »), 12 pt minimum dans un document lu.
- Google Slides : Arial y est toujours ; Arial Black et Palatino Linotype, polices système de Windows et macOS,
  peuvent être remplacées à l'import. Après import, vérifier titres et sous-titres, et au besoin choisir Arial Black
  et Palatino Linotype dans le menu des polices (`AccentureDeck(target="gslides")` le rappelle à l'enregistrement).
- Sans PowerPoint (claude.ai, Claude Desktop), le rendu passe par LibreOffice avec Liberation Sans, aux métriques
  d'Arial : les coupures de ligne sont fidèles, l'Arial Black et le Palatino sont approchés.

## Masque et marque

- Le « > » (Greater Than) en bas à gauche, le copyright et le numéro de page en bas à droite viennent du masque :
  toujours créer les slides sur un layout du template, ne rien poser sous y = 7,0 pouces.
- Le grand « > » des couvertures et de la slide de fin est dans les layouts. Le composant `gt()` en pose un sur une
  slide de contenu : comme flèche entre deux états, ou comme signature, une fois par slide au plus.
- Le logo Accenture, le copyright et les mentions sont ceux du template, non modifiés.
- Photos : celles de la banque d'images de la marque, ou fournies par l'utilisateur ; à angles droits (pas de
  découpe ronde ni de goutte).

## Icônes

Icônes monoline de la marque (`pictos_accenture.md`) : trait fin violet sur fond clair, blanc sur fond foncé. Ni
pictos OCTO, ni pictos de La Grosse Conf, ni icône dessinée à la main.

## Rédaction (« How to make your story impactful »)

1. Aller droit au but : le bénéfice d'abord, sans distraction.
2. Parler humain.
3. Rendre visuel : au moins 60 % du contenu en visuel, remplacer le texte par des images ou des chiffres.
4. Couper ce qui ne fait pas avancer le récit.
5. Ne pas enterrer l'essentiel.
6. Oser.
7. Varier les slides : chapitres visuels, ruptures.
8. Être concis : 20 mots ou moins par slide de présentation.
9. Ménager les yeux : 16 pt ou plus.

Structure d'une histoire (« How to structure a great story ») : l'accroche, les personnages et le contexte, la
mission, l'obstacle, les capacités pour le vaincre (3 ou 4), le dénouement, l'appel à l'action.

Présentation ou document : un deck projeté porte des titres et des points clés, pas le discours ; le discours va dans
les notes (`notes()`).

## Vérification avant livraison

- Palette Accenture seule ; un violet fort par slide ; aucun dégradé dessiné, aucune couleur d'OCTO ni de La Grosse
  Conf.
- Contrastes : texte noir sur clair, blanc sur violet foncé ; rien de lilas ni de gris en petit texte.
- Arial, Arial Black et Palatino seulement ; titres sur une ligne, sans point final.
- Masque présent (layout du template) ; rien sous y = 7,0 pouces ; logo et copyright non modifiés.
- Aucun texte de gabarit (« Text », « Insert text here », « Body copy », « Place headline here ») ni consigne
  (« Hints: ») repris d'un modèle.
- Texte relu : orthographe, langue du deck (`lang`), 20 mots par slide projetée au plus.
