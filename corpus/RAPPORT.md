# Contentieux des antennes-relais : ce que montrent les décisions (open data de la justice administrative)

Analyse du 2026-10-15. Source : [opendata.justice-administrative.fr](https://opendata.justice-administrative.fr) (Licence Ouverte 2.0), 173 archives mensuelles téléchargées : Conseil d'État depuis 2021-06, cours administratives d'appel depuis 2022-03, tribunaux administratifs depuis 2022-06, jusqu'à 2026-10.

## Méthode et limites (à lire d'abord)

1. **Filtre automatique** : décisions qui parlent d'antenne-relais / station radioélectrique / pylône de téléphonie ET d'urbanisme (déclaration préalable, permis). **3 324 décisions candidates** (3 061 TA, 179 CAA, 84 CE), listées dans `index_decisions.csv`. Le filtre est large : il contient des faux positifs (toitures d'immeubles, logements, raccordements).
2. **Classement automatique** (qui attaque quoi, résultat) : approximatif. Pour les appels il est fragile (qui est appelant, sens du jugement de première instance). Les **taux de réussite** ci-dessous reposent uniquement sur la métadonnée « Solution » du TA, plus fiable.
3. **Lecture** : j'ai lu les passages décisifs d'environ 70 décisions (motifs et dispositif). **31 sont documentées** dans `lectures.csv` avec le moyen décisif, la régularisation éventuelle et la transférabilité. Les autres sont des lectures partielles et ne sont pas reportées.
4. **La métadonnée « Avocat_Requerant » est peu fiable** : elle désigne souvent l'avocat de l'opérateur, pas celui des riverains. Les avocats cités plus bas viennent du texte des décisions.
5. **Ce que les décisions ne disent pas** : pourquoi un requérant se désiste (56 désistements sur 62 sans motif), si un projet est finalement abandonné, ce que coûte un recours. Les abandons se voient surtout dans la presse locale.
6. Le corpus ne contient que les décisions publiées en open data (publication progressive et incomplète).

## Taux de réussite (tribunaux administratifs, riverains ou associations contre une non-opposition à DP ou un permis)

| Population | n | Rejeté au fond | Gagné (total) | Gagné (partiel) | Irrecevable | Désistement |
|---|---|---|---|---|---|---|
| Pylônes hors toiture, jugement au fond | 249 | 160 (64 %) | 14 (6 %) | 13 (5 %) | 20 (8 %) | 27 (11 %) |
| Pylônes, contexte rural, au fond | 176 | 138 (78 %) | 9 (5 %) | 7 (4 %) | 5 | 6 |
| Pylônes hors toiture, référé-suspension | 74 | 67 rejetés (dont 39 « pas de doute sérieux ») | 3 | 1 | | 3 |
| Tous types (toitures comprises), au fond | 386 | 218 (56 %) | 18 | 18 | 56 (15 %) | 49 |

**Ordre de grandeur : environ 10 % de réussite totale ou partielle devant le tribunal.** Un « gain partiel » est souvent une annulation limitée à un détail (clôture, plantations) avec un délai de trois à quatre mois pour régulariser (article L.600-5).

Dans votre ressort (pylônes, au fond): Rennes 17 décisions (4 gagnées), Nantes 19 (1 gagnée, 2 partielles), Caen 6 (1 gagnée).

## Ce qui a fait annuler ou suspendre (décisions lues)

| Motif décisif | Décisions lues | Régularisable ? | Transférable à Kersalous ? |
|---|---|---|---|
| **Loi Littoral** (L.121-8 : extension de l'urbanisation hors village ; L.121-13) | Plomeur 2022, Roscoff 2023, Carnac 2022 (confirmé en appel 2025), Plobannalec-Lesconil 2024, Notre-Dame-de-Monts 2024 (Phoenix), + 3 arrêts CAA Nantes, Talloires (CAA Lyon) | Non | **Non** : la commune de Plonéour-Lanvern n'est pas soumise à la loi Littoral (note du dossier). C'est le motif le plus gagnant dans l'Ouest, mais pas ici. |
| **Permis de construire exigé au lieu de la DP : abords d'un monument historique + covisibilité + hauteur > 12 m** (R.421-1, R.421-11) | Le Vigan (TA Toulouse 2023-09-28), Mont-Saint-Jean (TA Dijon 2023-02-02) | **Non** : le juge a refusé la régularisation à Dijon | **À vérifier en priorité** : la parcelle est-elle dans les abords d'un monument historique ? Le dossier note un périmètre des abords à 163 m et un manoir à 648 m. Sans périmètre délimité, la règle est « moins de 500 m et visible en même temps ». |
| **Pièces du dossier contradictoires (hauteur)** → décision fondée sur des faits inexacts | TA Nîmes, référé du 2026-09-11 : suspension d'une DP de **Phoenix France Infrastructure** (zone A), urgence présumée (L.600-3) | — | **Piste à vérifier** : l'avis dit 30 m, le dossier d'information 32,65 m. Ce n'est exploitable que si les pièces de la DP elles-mêmes divergent. |
| **Règle précise du PLU** : clôture (hauteur, mailles), plantations (art. 13), marge de recul, hauteur en zone A | Toutainville (Rouen 2024), Fégréac (Nantes 2025), Grenoble ×3, CAA Douai ×2, Teyran (Montpellier 2024) | **Oui, le plus souvent** (3 à 4 mois) | Oui, à examiner dans le règlement de la zone A de Plonéour-Lanvern. Retarde, ne tue pas le projet. |
| **Avis de l'architecte des Bâtiments de France non recueilli** | Roscoff 2023 | Oui (vice de procédure) | Même condition que ci-dessus (être dans un périmètre protégé). |
| Sécurité (R.111-2) : vent | Antilles 2024 | — | Non (cyclones) |

## Ce qui n'a quasiment jamais fonctionné (selon les décisions lues et un balayage automatique)

- **Dossier d'information du maire, code des postes (L.34-9-1, D.98-6-1), décret du 3 mai 2002 sur l'exposition** : écarté comme **inopérant** dans 48 des 73 décisions où il apparaît et jamais retenu comme motif d'annulation. Le juge de l'urbanisme applique « l'indépendance des législations ». Ce moyen peut servir pour la pression politique et le calendrier, pas pour annuler la DP. **Cela contredit l'intérêt que je lui avais donné dans le dossier**.
- **Ondes, santé, principe de précaution** : écartés partout (aucun élément circonstancié ; la police des ondes appartient à l'État).
- **Utilité du projet, couverture, mutualisation** : inopérants (aucune obligation de partage de site).
- **R.111-27 (atteinte aux lieux avoisinants)** : soulevé dans plus de 100 affaires, gagné de façon isolée (Roscoff, avec covisibilité). Un pylône treillis entouré de végétation passe presque toujours.
- **Zone A / N** : la plupart des TA admettent le pylône comme équipement d'intérêt collectif ou ouvrage de réseau (Pau, Guiclan, Cléden-Cap-Sizun, La Ferrière, Lys-Haut-Layon). Teyran (Montpellier) est l'exception lue.
- **PC au lieu de DP à cause de l'emprise** : échoue quand les locaux techniques sont petits (1,16 m², 1,10 m², 5 m²). Seul compte l'emprise des **locaux et installations techniques**, pas celle du pylône (avis du Conseil d'État du 21 mars 2024 n° 490536 et jugements de Fégréac et Rouen). **La fondation de 29,16 m² du dossier ne compte donc probablement pas** si elle est enterrée et que le local technique reste sous 20 m². À vérifier dans les pièces de la DP.
- **Recevabilité** : environ 15 % des recours (toutes natures) sont irrecevables. Des distances de 60 à 200 m ont suffi quand les requérants prouvaient une vue directe (Plobannalec 60/90 m ; Le Vigan 200 m ; Fégréac 120 m). La CAA de Toulouse a infirmé en 2023 pour défaut d'intérêt (21TL00540).

## Cas où le maire s'oppose (utile si le maire de Plonéour-Lanvern refuse la DP renouvelée)

Sur 42 arrêts d'appel de pylônes en contexte rural où le maire s'était opposé : opposition confirmée 12 fois, annulée 23 fois (classement automatique, à fiabiliser). Les motifs du maire qui tiennent sont rares ; les motifs de précaution/santé et R.111-27 sans éléments sont régulièrement censurés. Un très grand nombre de décisions concernent aussi des **retraits de non-opposition** par le maire : le classement automatique en compte 105 annulés à la demande de l'opérateur contre 28 maintenus. Les opérateurs invoquent l'article 222 de la loi du 23 novembre 2018 (texte et décisions non lus en détail).

## Avocats (à partir du texte des décisions)

Beaucoup de cabinets, peu de spécialistes. Côté **riverains**, les plus actifs repérés dans les décisions lues : **Me Corneloup (cabinet Adaes Avocats)** (8 affaires identifiées, plusieurs annulations ou suspensions : Cabris, Toutainville), Concept Avocats (Plomeur), Saout et Galia (Roscoff), Earth Avocats (Carnac), De Baynast (Notre-Dame-de-Monts), Terrien-Crette (Bordeaux). Côté **opérateurs**, les grands cabinets récurrents sont Pamlaw, Bon-Julien, Earth Avocats, Katam, Hamri et Gentilhomme. Pour 53 affaires sur 249, l'avocat n'est pas identifiable dans le texte. Ce relevé décrit des activités, pas des compétences : il ne remplace pas une consultation.

## Projets abandonnés

Visibles dans le corpus : Prudemanche (Eure-et-Loir, 2020-2023) où ATC et son partenaire ont abandonné le pylône, la DP est retirée en 2020 et le tribunal prononce un non-lieu en 2023 ; retraits de DP à Grenoble (2024), Limoges (2022) et Orléans (2026). Les causes de ces abandons ne sont pas dans les décisions.

## Pour Kersalous : ordre de vérification proposé

1. **Abords de monument historique** : la parcelle YX 26 est-elle dans un périmètre délimité ? si non, à moins de 500 m et visible en même temps qu'un monument ? (atlas des patrimoines, base Mérimée). C'est le seul motif non régularisable repéré qui s'applique hors littoral.
2. **Cohérence des pièces de la DP** (hauteurs, plans, emprises) et **règlement de la zone A** (clôture, plantations, recul, hauteur) : motifs de suspension rapides ou de retard.
3. **Emprise réelle des locaux techniques** (5 à 20 m²) et statut de la fondation.
4. **Recevabilité** : réunir les preuves de vue directe et de distance pour chaque requérant.
5. Ne pas fonder le recours sur les ondes, le dossier d'information ou l'utilité de l'antenne.

Délai : deux mois à compter de l'affichage sur le terrain (R.600-2), avec constat de commissaire de justice. Le référé-suspension contre une non-opposition bénéficie d'une urgence présumée (L.600-3) mais doit être déposé avant la cristallisation des moyens. À valider par un avocat.
