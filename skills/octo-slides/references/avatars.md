# Index des avatars OCTO (assets/avatars/)

Fichiers dans `<SKILL_DIR>/assets/avatars/` (PNG). Avec les helpers : `picto="<nom sans .png>"`. Un **Octo** (consultant OCTO) a une tête en anneau comme le sigle, avec un œil et un point satellite ; un **client** a un visage humain à deux yeux (seule la famille `filaire-client*` est dans ce cas). Les personas métier et les personnages thématiques ont tous une tête d'Octo.
Le **marine seul** (fichiers `filaire-*` sans suffixe) sert aux supports sobres, aux petites tailles et aux impressions monochromes. Le **bichrome** (marine et turquoise : suffixe `-bichro`, `-rvb`, `persona-*`) sert à mettre un personnage en avant ; dans une même vue, ne pas mélanger les deux traitements.

Couleurs mesurées sur tous les PNG (conversion BMP par `sips` puis comptage des pixels opaques, script Python sans PIL ; le SVG est relevé par grep). **oui** = #0E2356 et #00D2DD ; **proche** = turquoise #00D2DD mais trait marine désaturé #212B51 (hors charte, écart visible seulement côte à côte) ; **non** = couleurs étrangères à la charte.
Doublons : aucun fichier identique au pixel près. `tir-a-l-arc` existe en PNG, SVG et AI (même image) : préférer le SVG. Il y a aussi des quasi-doublons, signalés dans le tableau.

## 1. Avatars filaires génériques

| fichier | type | description | couleurs | conforme palette ? |
|---|---|---|---|---|
| filaire-client.png | client | Homme, mèche relevée, costume-cravate. | marine seul | oui |
| filaire-client-bichro.png | client | Même homme en costume, cheveux, yeux et veste turquoise. | bichrome | oui |
| filaire-client-2.png | client | Homme moustachu, chemise et cravate. | marine seul | oui |
| filaire-client-2-bichro.png | client | Même homme moustachu, cheveux, yeux et cravate turquoise. | bichrome | oui |
| filaire-cliente-bichro.png | client | Femme aux cheveux longs avec frange, cils, chemisier à col. Pas de version marine. | bichrome | oui |
| filaire-client-non-binaire.png | client | Personne sans cheveux, genre non marqué, polo à col. | marine seul | oui |
| filaire-client-non-binaire-bichro.png | client | Même personne, yeux et polo turquoise. | bichrome | oui |
| filaire-client-non-bianaire-2.png | client | Personne aux cheveux crépus volumineux, genre non marqué, veste ouverte sur un t-shirt. Faute de frappe dans le nom (« bianaire »). | marine seul | oui |
| filaire-client-non-bianaire-2-bichro.png | client | Même personne, cheveux et t-shirt turquoise. | bichrome | oui |
| filaire-femme.png | Octo | Femme de profil, cheveux longs, cils, encolure en cœur. | marine seul | oui |
| filaire-femme-bichro.png | Octo | Même femme, œil et buste turquoise. | bichrome | oui |
| filaire-femme-2.png | Octo | Femme aux cheveux bouclés sur l'épaule, col en V. | marine seul | oui |
| filaire-femme-2-bichro.png | Octo | Même femme, œil et buste turquoise. | bichrome | oui |
| filaire-femme-3.png | Octo | Femme aux cheveux afro volumineux, veste ouverte. | marine seul | oui |
| filaire-femme-3-bichro.png | Octo | Même femme, cheveux et t-shirt turquoise. | bichrome | oui |
| filaire-homme.png | Octo | Homme à la mèche relevée et à la barbe, sweat à capuche. | marine seul | oui |
| filaire-homme-bichro.png | Octo | Même homme, cheveux, barbe et sweat turquoise. | bichrome | oui |
| filaire-homme-2.png | Octo | Homme à la mèche relevée, chemise et cravate. | marine seul | oui |
| filaire-homme-2-bichro.png | Octo | Même homme, cheveux et cravate turquoise. | bichrome | oui |
| filaire-homme-3.png | Octo | Homme barbu et moustachu, veste ouverte sur un t-shirt. | marine seul | oui |
| filaire-homme-3-bichro.png | Octo | Même homme, barbe et t-shirt turquoise. | bichrome | oui |
| filaire-homme-4.png | Octo | Homme aux cheveux afro, barbu, en costume. | marine seul | oui |
| filaire-homme-4-bichro.png | Octo | Même homme, cheveux, barbe et veste turquoise. | bichrome | oui |
| filaire-non-binaire.png | Octo | Octo « nu » : tête-sigle et buste en goutte, sans attribut de genre. Quasi-doublon de `-2`, sans le col. | marine seul | oui |
| filaire-non-binaire-2.png | Octo | Octo neutre en t-shirt à col rond. | marine seul | oui |
| filaire-non-binaire-2-bichro.png | Octo | Même Octo neutre, œil et t-shirt turquoise. Pas de bichrome pour `filaire-non-binaire`. | bichrome | oui |

## 2. Personas métier

| fichier | type | description | couleurs | conforme palette ? |
|---|---|---|---|---|
| filaire-controleur-train-bichro.png | persona métier | Contrôleur ou contrôleuse de train, genre non marqué, casquette à galons, costume-cravate. | bichrome | proche |
| persona-biologiste-01.png | persona métier | Biologiste au genre non marqué, en blouse, avec stylo, microscope et bulle « … ». | bichrome | oui |
| persona-biologiste-02.png | persona métier | Biologiste homme barbu, même scène. | bichrome | oui |
| persona-biologiste-03.png | persona métier | Biologiste femme aux cheveux afro, cils, même scène. | bichrome | oui |
| persona-facteur.png | persona métier | Facteur ou factrice au genre non marqué, casquette, veste, enveloppe. | bichrome | oui |
| persona-facteur-homme.png | persona métier | Facteur moustachu. Quasi-doublon de `persona-facteur`, avec la moustache en plus. | bichrome | oui |
| persona-factrice-femme.png | persona métier | Factrice aux cheveux mi-longs et aux cils. | bichrome | oui |
| persona-femme-caissiere-01.png | persona métier | Caissière à chignon, cils, devant une caisse enregistreuse. | bichrome | oui |
| persona-femme-caissiere-02.png | persona métier | Caissier ou caissière au genre non marqué, même caisse. Le nom dit « femme ». | bichrome | oui |
| persona-femme-caissiere-03.png | persona métier | Caissier barbu à mèche, même caisse. Le nom dit « femme ». | bichrome | oui |
| persona-femme-chef.png | persona métier | Cheffe cuisinière aux cheveux bouclés, toque, veste à boutons. | bichrome | oui |
| persona-homme-chef.png | persona métier | Chef cuisinier barbu, toque, veste à boutons. | bichrome | oui |
| persona-femme-enceinte-01.png | persona métier | Personne enceinte au genre non marqué : ventre arrondi, t-shirt. | bichrome | oui |
| persona-femme-enceinte-02.png | persona métier | Femme enceinte à chignon, boucles d'oreilles, cils. | bichrome | oui |
| persona-homme-architecte-01.png | persona métier | Architecte au genre non marqué : casquette, crayon sur l'oreille, salopette. | bichrome | proche |
| persona-homme-architecte-02.png | persona métier | Architecte femme (cheveux longs, cils), même tenue. Le nom dit « homme ». | bichrome | proche |
| persona-medecin-homme-01.png | persona métier | Médecin au genre non marqué : tunique, stéthoscope, badge à croix. | bichrome | proche |
| persona-medecin-homme-02.png | persona métier | Médecin homme aux cheveux en épis, même tenue. | bichrome | proche |
| persona-medecin-homme-03.png | persona métier | Médecin femme aux cheveux mi-longs et aux cils, même tenue. Le nom dit « homme ». | bichrome | proche |
| policier-homme-fr-01.png | persona métier | Policier ou policière au genre non marqué, casquette et gilet « POLICE ». Contient du texte. | bichrome | oui |
| policier-homme-fr-02.png | persona métier | Policier homme aux cheveux courts, même tenue. | bichrome | oui |
| policier-homme-fr-03.png | persona métier | Policière aux cheveux mi-longs et aux cils, même tenue. Le nom dit « homme ». | bichrome | oui |
| chef-policier.png | persona métier | Commissaire ou gradé au genre non marqué : casquette à galons, chemise, cravate, poches. | bichrome | proche |
| militaire-f-rvb.png | persona métier | Militaire femme (cils), casque à lampe, treillis camouflage. Petit format (426 px). | bichrome | oui |
| militaire-h-rvb.png | persona métier | Militaire homme. Quasi-doublon de `militaire-f-rvb`, sans les cils. | bichrome | oui |

## 3. Série « Buffy contre les vampires »

Série complète en un seul style : trait #212B51, alliés en turquoise désaturé #3FBDCF, vampires en lavande #B1ACBF avec crocs et goutte de sang turquoise.

| fichier | type | description | couleurs | conforme palette ? |
|---|---|---|---|---|
| buffy-contre-vampire-angel.png | personnage thématique | Angel : homme à la mèche relevée, t-shirt. | marine + turquoise désaturé | non |
| buffy-contre-vampire-buffy.png | personnage thématique | Buffy : femme à la frange, hache, pieu, gouttes. | marine + turquoise désaturé | non |
| buffy-contre-vampire-cordelia.png | personnage thématique | Cordelia : femme aux cheveux longs ondulés, bouche ouverte. | marine + turquoise désaturé | non |
| buffy-contre-vampire-dawn.png | personnage thématique | Dawn : femme aux cheveux longs, pull à chevrons. | marine + turquoise désaturé | non |
| buffy-contre-vampire-oz.png | personnage thématique | Oz : homme aux cheveux en épis, t-shirt. | marine + turquoise désaturé | non |
| buffy-contre-vampire-rupert-giles.png | personnage thématique | Giles : homme à lunettes, costume-cravate, livre. | marine + turquoise désaturé | non |
| buffy-contre-vampire-tara.png | personnage thématique | Tara : sorcière aux cheveux longs, boule de cristal, fiole, étincelles. | marine + turquoise désaturé | non |
| buffy-contre-vampire-dalton.png | personnage thématique | Dalton : vampire en costume-cravate, crocs. | marine + lavande | non |
| buffy-contre-vampire-darla.png | personnage thématique | Darla : vampire femme aux cheveux mi-longs, crocs. | marine + lavande | non |
| buffy-contre-vampire-drussila.png | personnage thématique | Drusilla : vampire femme aux cheveux longs lavande, col en V. | marine + lavande | non |
| buffy-contre-vampire-eve.png | personnage thématique | Ève : vampire femme aux cheveux longs, col en V. | marine + lavande | non |
| buffy-contre-vampire-harmony.png | personnage thématique | Harmony : vampire femme aux cheveux bouclés lavande. | marine + lavande | non |
| buffy-contre-vampire-kakistos.png | personnage thématique | Kakistos : vampire chauve à l'œil barré, crocs. | marine + lavande | non |
| buffy-contre-vampire-knox.png | personnage thématique | Knox : vampire homme à la mèche, veste ouverte. | marine + lavande | non |
| buffy-contre-vampire-le-maitre.png | personnage thématique | Le Maître : vampire ridé sur un trône de pierre. | marine + lavande | non |
| buffy-contre-vampire-mistertrick.png | personnage thématique | Mister Trick : vampire homme moustachu en costume. | marine + lavande | non |
| buffy-contre-vampire-spike.png | personnage thématique | Spike : vampire homme aux cheveux plaqués, veste ouverte. | marine + lavande | non |
| buffy-contre-vampire-tedbuchanan.png | personnage thématique | Ted Buchanan : personnage au carré, à la mâchoire mécanique vissée. | marine + lavande | non |
| buffy-contre-vampire-turokhan.png | personnage thématique | Turok-Han : vampire primitif chauve, torse musclé. | marine + lavande | non |

## 4. Autres personnages thématiques

| fichier | type | description | couleurs | conforme palette ? |
|---|---|---|---|---|
| tir-a-l-arc.png | personnage thématique | Octo neutre qui tire à l'arc (cible). | bichrome | oui |
| virtual-reality2-rvb-01.png | personnage thématique | Octo homme barbu avec un casque de réalité virtuelle. | bichrome | oui |
| virtual-reality2-rvb-02.png | personnage thématique | Octo au genre non marqué avec un casque de réalité virtuelle. | bichrome | oui |
| virtual-reality2-rvb-03.png | personnage thématique | Octo femme aux cheveux longs avec un casque de réalité virtuelle. | bichrome | oui |
| formation-2-rvb.png | personnage thématique | Octo au genre non marqué en toque et toge de diplômé (formation, diplôme). | bichrome | proche |
| intello-2-rvb.png | personnage thématique | Octo homme à la houppe, grosses lunettes rondes, t-shirt marqué du sigle OCTO. | bichrome | proche |
| homme18-rvb.png | personnage thématique | Octo homme à la raie sur le côté, nœud papillon. | bichrome | proche |
| femme10-rvb.png | personnage thématique | Octo femme aux cheveux longs ondulés, point sur le front, haut croisé. | bichrome | proche |
| femme11-rvb.png | personnage thématique | Octo femme à la coiffure volumineuse, taches de rousseur, t-shirt tête de mort. | bichrome | proche |
| punk-rvb.png | personnage thématique | Octo punk, crête et cils, taches de rousseur, perfecto. | bichrome | proche |
| jardinier-rvb.png | personnage thématique | Jardinier moustachu, chapeau de paille, salopette à pousse, sécateur et râteau. | bichrome | proche |
| pompier-rvb.png | personnage thématique | Pompier casqué au genre peu marqué, veste à bandes, extincteur. | bichrome | proche |
| marin-rvb.png | personnage thématique | Marin barbu, casquette à ancre, marinière, pipe. | bichrome | proche |
| matelot-rvb.png | personnage thématique | Matelote aux cheveux longs, bachi à pompon, marinière. | bichrome | proche |
| chevalier-rvb.png | personnage thématique | Chevalier moustachu, heaume, épée, bouclier orné du sigle OCTO. | bichrome | proche |
| garde-anglais-rvb.png | personnage thématique | Garde royal britannique, bonnet à poil, cabine téléphonique. | bichrome | proche |
| marianne-rvb.png | personnage thématique | Marianne, bonnet phrygien à cocarde, écharpe. | bichrome | proche |
| wewantyou-rvb.png | personnage thématique | Oncle Sam barbu, haut-de-forme étoilé (« We want you »). | bichrome | proche |
| octo-hiver-rvb.png | personnage thématique | Octo neutre en bonnet à pompon, écharpe, pull à losanges. | bichrome | proche |
| frankenstein-rvb.png | personnage thématique | Octo en Frankenstein : cicatrice, boulons dans le cou, costume. | bichrome | proche |
| cochon.png | personnage thématique | Cochon à l'œil d'Octo, groin et queue en tire-bouchon (famille des « Trois petits cochons »). Petit format (193 px). | marine + turquoise désaturé | non (#42BDCE, #212B51) |

## Usage

- **Support client (persona, parcours utilisateur)** : piocher dans les personas métier (biologiste, médecin, caissier, facteur, chef, architecte, policier, contrôleur, militaire). Ce sont des Octos : pour représenter explicitement « le client » face à « l'équipe OCTO », utiliser la famille `filaire-client*`, la seule au visage humain.
- **Équipe, organigramme, intervenants OCTO** : `filaire-homme*`, `filaire-femme*` et `filaire-non-binaire*`, tous en marine seul ou tous en bichrome.
- **À éviter chez un client** : toute la série Buffy (fiction, sang, crocs, palette hors charte), les déguisements (`wewantyou`, `marianne`, `garde-anglais`, `chevalier`, `frankenstein`, `punk`, `femme11` à tête de mort, `octo-hiver`, `cochon`). Ce sont des clins d'œil internes, réservés aux supports internes ou à l'événementiel.
- **Neutres et réutilisables** : `tir-a-l-arc` (objectif), `virtual-reality2-rvb-0x` (innovation), `formation-2-rvb` (formation) et `intello-2-rvb` (expertise).
- **Diversité** : dans un même groupe, varier les genres (femme, homme, non marqué), les coiffures (lisses, bouclées, afro) et la pilosité. Les séries à variantes s'y prêtent : `-01/-02/-03`, `femme/homme`, `non-binaire`. Ne pas se fier aux noms : plusieurs fichiers « homme » ou « femme » montrent un autre genre (voir le tableau).
- **Cohérence** : ne pas mêler dans une même vue des avatars « oui » (#0E2356) et « proche » (#212B51) en grand format. Si c'est inévitable, garder au moins le même traitement (marine seul ou bichrome).
- **Fond** : poser les avatars sur du blanc ou sur une teinte claire de marine (`#E7E9EE` ou `#F3F4F7`). Les PNG sont détourés (fond transparent), mais leurs aplats intérieurs sont blancs : jamais de fond marine ni de fond turquoise, le trait et l'œil turquoise y disparaissent.
- **Format** : ne pas agrandir `cochon` (193 px) ni `militaire-*` (426 px).
