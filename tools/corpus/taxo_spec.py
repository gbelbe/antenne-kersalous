"""Spécification unique de la taxonomie du contentieux (schémas SKOS, concepts, définitions, règles de repérage).

Chaque concept : (identifiant court, parent ou None, libellé, définition, regex de repérage ou None).
- `taxonomie.py` en tire le Turtle (antenne-contentieux.ttl).
- `tag.py` applique les regex aux textes des décisions : une regex repère un moyen **évoqué** (cité ou discuté),
  jamais un moyen retenu ou écarté. Seules les lectures humaines (corpus/lectures.csv) distinguent retenu / écarté.
Les références d'articles viennent de ma connaissance du droit, pas d'une relecture à la source : à vérifier avant toute citation.
"""

SCHEMES = {
    "Moyens": ("Moyens juridiques invoqués dans le contentieux des antennes", "M",
               "Ce que les requérants (ou l'opérateur, ou la commune) invoquent devant le juge. Une décision est reliée à un moyen par trois relations distinctes : évoqué, retenu, écarté."),
    "Resultat": ("Résultat de la décision", "R", "Le dispositif de la décision, tel que le juge l'a rendu."),
    "EffetProjet": ("Effet sur le projet d'antenne", "E", "Ce que la décision change pour le projet, quel que soit le requérant."),
    "ActeAttaque": ("Acte attaqué ou en cause", "A", "La décision administrative dont la légalité est discutée."),
    "Procedure": ("Procédure et mécanismes procéduraux", "P", "Voie de droit utilisée et outils que le code de l'urbanisme ou de justice administrative met à disposition du juge."),
    "Requerant": ("Qui saisit le juge", "Q", "Nature du demandeur."),
    "ContexteSite": ("Contexte du site et de l'ouvrage", "C", "Où est le projet et de quoi s'agit-il. Sert à retrouver les cas qui ressemblent à Kersalous."),
    "Niveau": ("Niveau de juridiction", "J", "Premier ressort, appel, cassation."),
    "Proximite": ("Proximité avec le cas de Kersalous", "X", "Ressemblance de la décision avec le dossier. Calculée par score (voir proximite.py) ; discutable décision par décision."),
    "Transferabilite": ("Transférabilité du motif décisif à Kersalous", "T", "Le motif qui a fait gagner ou perdre s'applique-t-il à notre cas ?"),
    "NiveauLecture": ("Niveau de lecture de la décision", "L", "Ce qu'on peut affirmer d'une décision : repérage automatique, lecture humaine, vérification à la source."),
}

# ──────────────────────────────────────────────────────────────────────────────
MOYENS = [
 ("m-qualification", None, "Nature de l'autorisation exigée (déclaration préalable ou permis)",
  "Le projet relevait-il d'un permis de construire plutôt que d'une déclaration préalable ? Seuils du code de l'urbanisme (R.421-1, R.421-2, R.421-9, R.421-11).", None),
 ("m-emprise-locaux", "m-qualification", "Emprise des locaux techniques (seuil de 20 m²)",
  "Au-delà de 20 m² d'emprise au sol ou de surface de plancher, un permis est exigé. Selon l'avis du Conseil d'État du 21 mars 2024 (n° 490536, à relire), seule compte l'emprise des locaux et installations techniques, pas celle du pylône.",
  r"R\.? ?421-9|R\.? ?421-2|emprise au sol|surface de plancher|locaux? techniques?|490536"),
 ("m-abords-mh-pc", "m-qualification", "Abords d'un monument historique : permis exigé (covisibilité)",
  "Dans les abords d'un monument historique, une construction de plus de 12 m de haut qui est en covisibilité avec lui exige un permis (R.421-11). Annulation non régularisable dans les deux jugements lus (Le Vigan, Mont-Saint-Jean).",
  r"R\.? ?421-11|abords? d'un monument|abords? des? monuments?|périmètre.{0,40}monument|L\.? ?621-3[02]"),
 ("m-permis-precaire", "m-qualification", "Permis de construire à titre précaire (L.433-1)", "Autorisation exceptionnelle d'une construction temporaire qui déroge aux règles, réservée aux nécessités caractérisées. TA Caen, 18 mars 2025, n° 2301119 (Trouville-sur-Mer, Bouygues) : annulation d'un permis délivré à titre précaire pour une antenne, moyen relevé d'office ; suspension préalable le 24 mai 2023.",
  r"L\.? ?433-1|à titre précaire"),
 ("m-hauteur-12m", "m-qualification", "Hauteur de plus de 12 m",
  "Seuil de hauteur qui fait basculer certaines constructions vers le permis de construire.",
  r"12 mètres|douze mètres|hauteur.{0,30}supérieure à 12"),

 ("m-reglement", None, "Règles d'urbanisme applicables au terrain",
  "Conformité du projet au plan local d'urbanisme, au règlement national d'urbanisme et aux lois d'aménagement spécial.", None),
 ("m-zone-agri-naturelle", "m-reglement", "Zone agricole ou naturelle (équipement d'intérêt collectif)",
  "Le pylône est-il admis en zone A ou N comme équipement d'intérêt collectif ou service public ? La plupart des tribunaux répondent oui, mais l'admission peut dépendre du texte du PLU : TA Amiens, 11 juin 2025, n° 2200831 (Bruyères-et-Montbérault, Orange, zone N) annule parce qu'une antenne n'est pas un « équipement public » et n'est admise que si un impératif technique justifie sa localisation.",
  r"zone (?:A|N)\b|zone agricole|zone naturelle|équipements? (?:d'intérêt )?collectifs?|secteur (?:agricole|naturel)"),
 ("m-zone-urbaine", "m-reglement", "Zone urbaine ou à urbaniser", "Compatibilité du pylône avec le règlement d'une zone U ou AU.",
  r"zone (?:U[A-Za-z]*|AU[A-Za-z]*)\b|zone urbaine|à urbaniser"),
 ("m-regle-plu", "m-reglement", "Règle précise du règlement du PLU",
  "Violation d'un article particulier du règlement. Souvent régularisable (3 à 4 mois, L.600-5).", None),
 ("m-regle-hauteur", "m-regle-plu", "Hauteur maximale", "Dépassement de la hauteur permise par le règlement de la zone.",
  r"hauteur maximale|hauteur maximum|hauteur (?:autorisée|limitée)"),
 ("m-regle-cloture", "m-regle-plu", "Clôture", "Hauteur ou nature de la clôture du poste technique.", r"clôtures?(?! de l'instruction| d'instruction)"),
 ("m-regle-plantations", "m-regle-plu", "Plantations et espaces verts", "Obligation de plantations, de haies ou d'espaces verts.",
  r"\bplantations?|\bhaies?\b|espaces? verts|végétalis"),
 ("m-regle-implantation", "m-regle-plu", "Recul et implantation", "Marge de recul par rapport aux voies et aux limites séparatives.",
  r"marge de recul|limites séparatives|implantation par rapport"),
 ("m-regle-aspect", "m-regle-plu", "Aspect extérieur et architecture", "Règle d'aspect extérieur des constructions.",
  r"aspect extérieur|prescriptions architecturales"),
 ("m-littoral", "m-reglement", "Loi Littoral", "Dispositions des articles L.121-1 et suivants du code de l'urbanisme. Motif le plus gagnant dans l'Ouest, mais Plonéour-Lanvern n'est pas concernée.",
  r"loi littoral|L\.? ?121-\d+|\blittoral\b"),
 ("m-littoral-urbanisation", "m-littoral", "Extension de l'urbanisation hors village ou agglomération (L.121-8)",
  "Construction nouvelle en discontinuité avec les agglomérations et villages existants.", r"L\.? ?121-8|extension de l'urbanisation|hors (?:d'un )?village"),
 ("m-littoral-espaces", "m-littoral", "Espaces proches du rivage, espaces remarquables, coupures d'urbanisation",
  "Extension limitée en espaces proches du rivage (L.121-13), protection des espaces remarquables (L.121-23).",
  r"L\.? ?121-13|L\.? ?121-23|espaces? proches? du rivage|espaces? remarquables?|coupures? d'urbanisation|L\.? ?121-22"),
 ("m-montagne", "m-reglement", "Loi Montagne", "Dispositions des articles L.122-1 et suivants (urbanisation en continuité).",
  r"loi montagne|L\.? ?122-\d+|zone de montagne"),
 ("m-desserte", "m-reglement", "Desserte par les réseaux publics (électricité, eau) (L.111-11)",
  "Si des travaux sur les réseaux publics sont nécessaires, la déclaration doit être refusée quand l'autorité ne peut dire quand et par qui ils seront faits. TA Rennes, 19 mars 2026, n° 2401193 (La Gouesnière) : annulation, extension électrique de 408 m sans diligences du maire auprès du syndicat d'énergie ; suspension préalable le 30 octobre 2025.",
  r"L\.? ?111-11|extension du réseau|réseau (?:public )?de distribution d.électricité|\bEnedis\b"),
 ("m-emplacement-reserve", "m-reglement", "Emplacement réservé ou projet public d'infrastructure",
  "Projet implanté dans un emplacement réservé ou une zone prévue pour un équipement public. TA Nice, 11 juin 2025, n° 2205993 (Châteauneuf-Grasse, Free) : annulation, l'emplacement était réservé à un parking. TA Montpellier, 13 février 2026, n° 2600444 (Saint-Just, Phoenix France Infrastructure 3) : suspension ; la commune ne peut corriger l'implantation par une prescription.",
  r"emplacement réservé|emplacements réservés|L\.? ?151-41|zone réservée"),
 ("m-acces", "m-reglement", "Accès, voirie et consultation du gestionnaire de voirie (R.423-53)",
  "Création d'un accès sur une route départementale ou communale : le gestionnaire doit être consulté. TA Nantes, 30 septembre 2025, n° 2114721 (Saint-Cyr-en-Talmondais, Orange) : annulation partielle, 6 mois pour régulariser.",
  r"R\.? ?423-53|nouvel accès|création d.un accès|gestionnaire de (?:la )?voirie"),
 ("m-rnu", "m-reglement", "Constructibilité limitée (RNU, hors parties urbanisées)",
  "Règle de constructibilité limitée des communes sans document d'urbanisme (L.111-3).",
  r"constructibilité limitée|L\.? ?111-3\b|règlement national d'urbanisme|parties? urbanisées?"),

 ("m-insertion", None, "Insertion dans le site et patrimoine (R.111-27)",
  "Atteinte au caractère ou à l'intérêt des lieux avoisinants, aux sites, aux paysages naturels ou urbains, aux perspectives monumentales.", None),
 ("m-paysage", "m-insertion", "Atteinte au paysage (R.111-27)", "Erreur manifeste d'appréciation de l'atteinte au paysage. Rarement retenue pour un pylône treillis entouré de végétation.",
  r"R\.? ?111-27|111-27|atteinte.{0,40}paysage|intérêt des lieux avoisinants"),
 ("m-covisibilite", "m-insertion", "Covisibilité avec un monument ou un bâti remarquable", "Le pylône est visible en même temps qu'un monument ou depuis lui.",
  r"covisibilité|co-visibilité|visible depuis|visibles? en même temps"),
 ("m-patrimoine", "m-insertion", "Site protégé ou patrimonial", "Site classé ou inscrit, site patrimonial remarquable, AVAP, périmètre délimité des abords.",
  r"site (?:classé|inscrit)|site patrimonial|\bAVAP\b|\bSPR\b|périmètre délimité"),

 ("m-milieux", None, "Milieux naturels et environnement", "Atteinte à une zone humide, à un boisement, à des espèces ou à un espace naturel protégé.", None),
 ("m-zone-humide", "m-milieux", "Zone humide et eau", "Zone humide, cours d'eau, loi sur l'eau (L.211-1, L.214-1).",
  r"zone humide|L\.? ?211-1|loi sur l'eau|cours d'eau"),
 ("m-ebc", "m-milieux", "Espace boisé classé et boisement", "Espace boisé classé (L.113-1, L.113-2) ou boisement protégé.",
  r"espace boisé classé|\bEBC\b|L\.? ?113-[12]|espaces? boisés?"),
 ("m-captage", "m-milieux", "Périmètre de protection d'un captage d'eau potable", "Arrêté préfectoral de protection d'un captage qui interdit ou limite les constructions. TA Amiens, 8 novembre 2022, n° 2100398 (Rethondes, association Les Galiciens) : annulation non régularisable.",
  r"captage|périmètre de protection (?:immédiate|rapprochée|éloignée)|alimentation en eau potable"),
 ("m-natura", "m-milieux", "Natura 2000, ZNIEFF, espèces protégées", "Zonages d'inventaire ou de protection de la biodiversité.",
  r"Natura 2000|ZNIEFF|espèces? protégées?|biodiversité|trame verte|corridor écologique"),

 ("m-dossier", None, "Exactitude et complétude du dossier de la demande",
  "Le dossier permettait-il à l'administration d'apprécier le projet ? Une décision fondée sur des faits inexacts est illégale.", None),
 ("m-pieces-contradictoires", "m-dossier", "Pièces contradictoires ou faits inexacts",
  "Les pièces du dossier se contredisent (hauteur, emprise, position). TA Nîmes, 11 septembre 2026, n° 2604044 : suspension d'une DP de Phoenix France Infrastructure.",
  r"inexact|incohéren|discordan|erreur matérielle|faits matériellement|pièces?.{0,40}contradictoires"),
 ("m-dossier-incomplet", "m-dossier", "Dossier de déclaration incomplet", "Pièce manquante ou insuffisante (R.431-36 et suivants).",
  r"incomplet|R\.? ?431-36|R\.? ?431-|pièce.{0,30}manquant|notice (?:descriptive|insuffisante)"),
 ("m-qualite-petitionnaire", "m-dossier", "Qualité du pétitionnaire pour déposer la demande (R.423-1)", "Le demandeur doit attester avoir qualité pour déposer. Retenu en référé quand une erreur sur la propriété est reconnue par la commune (TA Lille, 29 avril 2026, n° 2604207, Beuvry) ou quand les droits sur les espaces communs d'un lotissement sont douteux (TA Nantes, 17 avril 2024, n° 2404854).",
  r"qualité pour (?:déposer|présenter)|R\.? ?423-1\b|L\.? ?442-9"),
 ("m-fraude", "m-dossier", "Fraude", "Manœuvre destinée à tromper l'administration sur le projet.", r"fraude|manœuvre frauduleuse"),

 ("m-instruction", None, "Régularité de l'instruction et de la décision", "Compétence, avis obligatoires, délais, motivation, retrait de la décision.", None),
 ("m-abf", "m-instruction", "Avis de l'architecte des Bâtiments de France", "Avis non recueilli alors que le projet est dans un périmètre protégé.",
  r"architecte des bâtiments de France|\bABF\b|avis conforme"),
 ("m-retrait", "m-instruction", "Retrait d'une non-opposition par le maire", "Le maire retire sa décision tacite ou expresse (L.424-5). L'article 222 de la loi ELAN interdit de retirer une décision qui autorise une antenne ou ne s'y oppose pas : le retrait est le plus souvent annulé à la demande de l'opérateur (ex. TA Marseille, 20 juin 2023, n° 2007088).",
  r"retrait.{0,80}(?:non-opposition|décision tacite|décision implicite)|L\.? ?424-5|article 222|loi ELAN|loi du 23 novembre 2018"),
 ("m-competence", "m-instruction", "Compétence du signataire", "Incompétence ou défaut de délégation.", r"incompétence|délégation de signature"),
 ("m-motivation", "m-instruction", "Motivation et procédure contradictoire", "Insuffisance de motivation ou atteinte aux droits de la défense.",
  r"insuffisamment motivé|défaut de motivation|principe du contradictoire"),
 ("m-delai-instruction", "m-instruction", "Délai d'instruction", "Décision tacite, majoration du délai, date de naissance de la non-opposition.",
  r"délai d'instruction|R\.? ?423-\d+"),

 ("m-securite", None, "Sécurité et santé publiques", "Risques invoqués contre le projet.", None),
 ("m-r111-2", "m-securite", "Sécurité et salubrité publiques (R.111-2)", "Risque pour la sécurité ou la salubrité publique.",
  r"R\.? ?111-2\b|sécurité publique|salubrité"),
 ("m-vent-chute", "m-securite", "Vent, chute, foudre", "Risque d'effondrement, de chute de glace ou de matériel en cas de vent ou de cyclone. TA Guadeloupe et CAA Bordeaux (2 octobre 2025, n° 23BX01363) : annulation du permis tacite (cyclones).",
  r"effondrement|chute|tempête|cyclone|foudre"),
 ("m-incendie", "m-securite", "Risque d'incendie (R.111-2, SDIS)", "Projet au contact d'un massif boisé sans moyens de défense contre l'incendie. TA Toulon, 24 février 2025, n° 2203480 (Cuers, Free) : sursis à statuer de 4 mois pour régulariser (point d'eau incendie validé par le SDIS) ; même vice relevé à Le Beausset (TA Toulon, 6 janvier 2025, n° 2202464).",
  r"risque d.incendie|défense (?:extérieure )?contre l.incendie|point d.eau incendie|\bSDIS\b|feux de forêt"),
 ("m-ondes", "m-securite", "Ondes, santé et principe de précaution", "Effets des champs électromagnétiques et principe de précaution (Charte de l'environnement, art. 5). Écarté dans toutes les décisions lues : la police des ondes appartient à l'État.",
  r"\bondes\b|champs? électromagnétiques?|principe de précaution|charte de l'environnement|rayonnement"),
 ("m-risques-naturels", "m-securite", "Risques naturels (inondation, crue, argile)", "Plan de prévention des risques, cote de référence, retrait-gonflement des argiles. TA Lyon, 30 mars 2023, n° 2101323 : sursis à statuer, dalle sous la cote de référence en zone bleue du PPRI.",
  r"\bPPR[IN]?\b|plan de prévention des risques|\bcrues?\b|inondation|retrait-gonflement"),
 ("m-bruit", "m-securite", "Bruit et nuisances", "Nuisances sonores ou vibrations des équipements.", r"\bbruit|nuisances? sonores?|vibrations?"),
 ("m-aerodrome", "m-securite", "Servitudes aéronautiques et balisage", "Servitudes de dégagement, balisage lumineux.", r"servitudes? aéronautiques?|aérodrome|balisage"),
 ("m-police-maire", "m-securite", "Pouvoirs de police du maire", "Le maire peut-il réglementer l'implantation des antennes ? Non pour motifs sanitaires (CE, 26 octobre 2011, nos 326492 et 329904).",
  r"pouvoirs? de police|L\.? ?2212|L\.? ?2213|arrêté municipal"),

 ("m-connexes", None, "Législations connexes (le plus souvent inopérantes)",
  "Moyens tirés d'autres législations que l'urbanisme. Le juge de l'urbanisme applique l'indépendance des législations. Écartés comme inopérants dans 48 des 73 décisions lues ou repérées.", None),
 ("m-dim", "m-connexes", "Dossier d'information du maire (L.34-9-1 CPCE, D.98-6-1)", "Absence, retard ou insuffisance du dossier d'information transmis au maire. Jamais retenu pour annuler une DP dans le corpus. Peut servir la pression politique.",
  r"L\.? ?34-9-1|D\.? ?98-6-1|dossier d'information"),
 ("m-decret-2002", "m-connexes", "Décret du 3 mai 2002 : valeurs limites d'exposition", "Respect des valeurs limites d'exposition du public ; contrôle par l'ANFR.",
  r"2002-775|valeurs limites d'exposition|\bANFR\b|agence nationale des fréquences"),
 ("m-utilite", "m-connexes", "Utilité du projet et besoin de couverture", "Zone blanche, New Deal Mobile, qualité de service : inopérants contre une DP.",
  r"zone blanche|new deal|qualité de service|couverture (?:mobile|du territoire|numérique)|besoin de couverture"),
 ("m-mutualisation", "m-connexes", "Mutualisation et choix d'un autre site", "Aucune obligation légale de partage de site ni de rechercher une autre implantation.",
  r"mutualis|partage de site|autre emplacement|autre site|pylône existant|co-?localis"),
 ("m-droits-tiers", "m-connexes", "Droit de propriété et droits des tiers", "Titre du pétitionnaire, servitudes privées : l'autorisation est délivrée sous réserve du droit des tiers.",
  r"droit des tiers|autorisation du propriétaire|servitude de droit privé|droit de propriété"),

 ("m-foncier-communal", None, "Acte de la commune propriétaire du terrain (vente, bail)", "Quand le terrain appartient à la commune, la délibération du conseil municipal qui le vend ou le loue à l'opérateur peut être attaquée comme toute décision. Le juge contrôle l'intérêt général de l'opération.", r"domaine privé|cession d.une partie de la parcelle|délibération du conseil municipal[^.]{0,120}(?:vente|cession|bail)"),
 ("m-recevabilite", None, "Recevabilité du recours", "Conditions pour que le juge examine la requête. Ici, « retenu » veut dire que le recours est déclaré irrecevable (contre le requérant) ; « écarté » que la fin de non-recevoir est rejetée.", None),
 ("m-interet-agir", "m-recevabilite", "Intérêt à agir du requérant (L.600-1-2)", "Distance, vue directe, nature de la gêne. 60 à 200 m ont été admis avec vue directe.",
  r"intérêt (?:pour )?agir|L\.? ?600-1-2|qualité pour agir"),
 ("m-qualite-association", "m-recevabilite", "Qualité d'une association pour agir (L.600-1-1)", "Objet statutaire, antériorité des statuts par rapport à l'affichage en mairie.",
  r"L\.? ?600-1-1|objet social|statuts de l'association|statuts"),
 ("m-notification", "m-recevabilite", "Notification du recours (R.600-1)", "Le requérant doit notifier son recours à l'auteur de la décision et au bénéficiaire dans les quinze jours.",
  r"R\.? ?600-1\b|notification du recours|défaut de notification"),
 ("m-delai-recours", "m-recevabilite", "Délai de recours et forclusion (R.600-2)", "Deux mois à compter de l'affichage sur le terrain. Tardiveté, forclusion.",
  r"R\.? ?600-2|tardi|forclusi|délai de recours"),
 ("m-affichage", "m-recevabilite", "Affichage de l'autorisation sur le terrain", "Un affichage irrégulier empêche le délai de courir (R.424-15, A.424-15 et suivants).",
  r"affichage|panneau|[RA]\.? ?424-15"),
]

# ──────────────────────────────────────────────────────────────────────────────
RESULTAT = [
 ("r-rejet", None, "Requête rejetée", "Le juge refuse de faire droit à la demande.", None),
 ("r-rejet-fond", "r-rejet", "Rejet au fond", "Moyens examinés et écartés.", None),
 ("r-rejet-doute", "r-rejet", "Rejet en référé : pas de doute sérieux", "Référé-suspension rejeté faute de moyen propre à créer un doute sérieux.", None),
 ("r-rejet-manifeste", "r-rejet", "Rejet par ordonnance (irrecevabilité ou infondé manifeste)", "Ordonnance rendue sans audience (R.222-1).", None),
 ("r-irrecevable", None, "Requête irrecevable", "Défaut d'intérêt, de qualité, de notification, tardiveté.", None),
 ("r-sans-jugement", None, "Pas de jugement au fond", "L'instance se termine sans trancher le litige.", None),
 ("r-desistement", "r-sans-jugement", "Désistement", "Le requérant retire sa requête. Le motif n'est presque jamais indiqué.", None),
 ("r-non-lieu", "r-sans-jugement", "Non-lieu à statuer", "L'acte est retiré ou abrogé, ou le projet abandonné, en cours d'instance.", None),
 ("r-sursis", "r-sans-jugement", "Sursis à statuer ou mesure d'instruction", "Le juge attend une régularisation ou un complément.", None),
 ("r-annulation", None, "Annulation ou suspension", "Le juge fait droit en tout ou partie à la demande.", None),
 ("r-annulation-totale", "r-annulation", "Annulation totale", "L'acte attaqué est annulé.", None),
 ("r-annulation-partielle", "r-annulation", "Annulation partielle ou assortie d'une régularisation", "Annulation limitée à un point (clôture, plantations) ou jugement avant dire droit laissant le temps de régulariser (L.600-5, L.600-5-1).", None),
 ("r-suspension", "r-annulation", "Suspension en référé", "Exécution de l'acte suspendue (L.521-1 CJA, L.600-3).", None),
 ("r-appel-confirme", None, "Appel : jugement confirmé", "La cour confirme le jugement de première instance.", None),
 ("r-appel-infirme", None, "Appel : jugement infirmé", "La cour annule ou réforme le jugement.", None),
]

EFFET = [
 ("e-maintenu", None, "Projet maintenu", "L'autorisation du projet subsiste (recours rejeté, irrecevable ou retiré).", None),
 ("e-bloque", None, "Projet bloqué", "Autorisation annulée ou suspendue, ou refus de l'administration confirmé.", None),
 ("e-debloque", None, "Projet débloqué", "Le refus ou le retrait de l'administration est annulé : l'opérateur peut poser le pylône.", None),
 ("e-retarde", None, "Projet retardé ou à régulariser", "Annulation partielle, régularisation ou sursis à statuer.", None),
 ("e-indetermine", None, "Effet indéterminé", "Décision dont l'effet n'a pas pu être classé automatiquement.", None),
]

ACTE = [
 ("a-non-opposition", None, "Non-opposition à déclaration préalable", "Décision expresse ou tacite du maire de ne pas s'opposer aux travaux (L.424-1, R.424-1).", None),
 ("a-opposition", None, "Opposition à déclaration préalable", "Arrêté du maire s'opposant aux travaux. L'opérateur le conteste le plus souvent.", None),
 ("a-retrait", None, "Retrait d'une non-opposition", "Retrait par le maire d'une décision favorable (L.424-5).", None),
 ("a-pc", None, "Permis de construire", "Permis accordé, refusé ou tacite.", None),
 ("a-certificat", None, "Certificat de non-opposition", "Certificat délivré ou refusé après décision tacite.", None),
 ("a-autre", None, "Autre acte", "Raccordement, arrêté de police, autre.", None),
 ("a-indetermine", None, "Acte non déterminé", "L'acte attaqué n'a pas pu être classé automatiquement.", None),
]

PROCEDURE = [
 ("p-voie", None, "Voie de droit", "Nature du recours devant le juge.", None),
 ("p-fond", "p-voie", "Recours au fond (excès de pouvoir)", "Demande d'annulation de l'acte.", None),
 ("p-refere", "p-voie", "Référé-suspension", "Suspension d'urgence (L.521-1 CJA).", None),
 ("p-defere", "p-voie", "Déféré du préfet (contrôle de légalité)", "Le préfet attaque lui-même l'autorisation devant le tribunal et peut en demander la suspension. TA Nantes, 20 octobre 2022, n° 2212834 (Guérande, Free) : permis suspendu à la demande du préfet de Loire-Atlantique (loi Littoral).",
  r"déféré|le préfet de[^.]{0,60}demande"),
 ("p-appel", "p-voie", "Appel", "Recours devant une cour administrative d'appel.", None),
 ("p-cassation", "p-voie", "Cassation", "Recours devant le Conseil d'État.", None),
 ("p-avis", "p-voie", "Avis contentieux", "Avis du Conseil d'État sur une question de droit nouvelle (L.113-1 CJA).", None),
 ("p-mecanisme", None, "Mécanismes procéduraux", "Outils que le juge peut utiliser sur l'acte attaqué.", None),
 ("p-regularisation", "p-mecanisme", "Régularisation en cours d'instance", "L.600-5 (annulation partielle) et L.600-5-1 (sursis à statuer pour régulariser).",
  r"L\.? ?600-5\b|600-5-1|sursis à statuer|régularis"),
 ("p-urgence-presumee", "p-mecanisme", "Urgence présumée contre un permis (L.600-3)", "Le référé-suspension contre une autorisation d'urbanisme bénéficie d'une urgence présumée si le requérant l'introduit dans le délai prévu.",
  r"L\.? ?600-3"),
 ("p-recours-abusif", "p-mecanisme", "Recours abusif et dommages-intérêts (L.600-7)", "Le bénéficiaire peut demander des dommages-intérêts si le recours est abusif.",
  r"L\.? ?600-7|recours abusif|dommages et intérêts|dommages-intérêts"),
 ("p-demolition", "p-mecanisme", "Démolition ou mise en conformité (L.480-13, L.480-14)", "Après l'annulation définitive d'une autorisation, le tiers peut demander à la commune de saisir le tribunal judiciaire en vue de la démolition. TA Rennes, 4 avril 2025, n° 2203183 (Plomeur, Free) : le refus de la commune est annulé et le juge lui enjoint d'agir.",
  r"L\.? ?480-1[34]"),
 ("p-frais", "p-mecanisme", "Frais irrépétibles (L.761-1 CJA)", "Somme mise à la charge de la partie perdante pour les frais d'avocat.",
  r"L\.? ?761-1|frais (?:exposés|irrépétibles)"),
 ("p-cristallisation", "p-mecanisme", "Cristallisation des moyens (R.600-5)", "Après un délai, plus de moyen nouveau en première instance.", r"R\.? ?600-5\b"),
]

REQUERANT = [
 ("q-riverains", None, "Particuliers riverains", "Habitants ou propriétaires voisins, dont les noms sont pseudonymisés.", None),
 ("q-association", None, "Association ou collectif", "Personne morale. Le nom est publié dans la décision.", None),
 ("q-asso-environnement", "q-association", "Association d'environnement ou de cadre de vie", "Défense de la nature, du cadre de vie, de la santé.", None),
 ("q-asso-patrimoine", "q-association", "Association de patrimoine", "Défense des sites et monuments.", None),
 ("q-collectif", "q-association", "Collectif ou association de riverains", "Groupement créé pour le projet.", None),
 ("q-commune", None, "Commune ou collectivité", "Maire, commune, établissement public. Dans les décisions favorables à un tiers, c'est souvent la commune de Nice contre une décision du préfet, ou une commune voisine.", None),
 ("q-prefet", None, "Préfet (déféré du contrôle de légalité)", "Le préfet attaque lui-même l'autorisation délivrée par un maire (déféré), avec ou sans demande de suspension. Motif le plus fréquent : loi Littoral (Locmaria-Plouzané dans le Finistère, Guérande, Marseillan, Marseille).", None),
 ("q-syndicat", None, "Syndicat de copropriétaires ou société civile", "Copropriété ou société civile immobilière voisine du projet.", None),
 ("q-operateur", None, "Opérateur ou société de pylônes", "Bénéficiaire du projet, qui conteste l'opposition ou le retrait.", None),
 ("q-indetermine", None, "Requérant non déterminé", "Non classé automatiquement.", None),
]

CONTEXTE = [
 ("c-territoire", None, "Territoire", "Nature du territoire d'implantation.", None),
 ("c-littoral", "c-territoire", "Commune soumise à la loi Littoral", "Détectée par mention de la loi Littoral dans la décision.", r"loi littoral|L\.? ?121-\d+"),
 ("c-montagne", "c-territoire", "Zone de montagne", "Loi Montagne.", r"loi montagne|L\.? ?122-\d+"),
 ("c-rural", "c-territoire", "Zone agricole ou naturelle", "Terrain classé en zone A ou N.", r"zone (?:A|N)\b|zone agricole|zone naturelle"),
 ("c-urbain", "c-territoire", "Zone urbaine", "Terrain en zone U.", r"zone U[A-Za-z]*\b|zone urbaine"),
 ("c-abords-mh", "c-territoire", "Abords d'un monument historique", "Dans les abords d'un monument.", r"abords? d'un monument|abords? des? monuments?|L\.? ?621-3[02]"),
 ("c-site-protege", "c-territoire", "Site classé, inscrit ou patrimonial", "Site protégé.", r"site (?:classé|inscrit)|site patrimonial"),
 ("c-ouvrage", None, "Type d'ouvrage", "Nature et taille du support.", None),
 ("c-pylone", "c-ouvrage", "Pylône hors toiture", "Support au sol : treillis, mât tubulaire, poteau.", r"pylône|mât"),
 ("c-pylone-treillis", "c-pylone", "Pylône treillis", "Structure en treillis (cas de Kersalous).", r"pylône treillis|treillis"),
 ("c-rehausse", "c-ouvrage", "Rehausse d'un pylône existant", "Augmentation de la hauteur d'un support déjà installé.", r"rehausse|rehaussement|surélévation"),
 ("c-toiture", "c-ouvrage", "Antenne sur toiture d'immeuble", "Faux positif fréquent du filtre pour notre cas.", r"toiture|toit-terrasse|terrasse de l'immeuble|en toiture"),
 ("c-camoufle", "c-ouvrage", "Support camouflé", "Faux arbre, cheminée, château d'eau.", r"faux arbre|camouflé|monopole.{0,20}arbre"),
 ("c-habitations", None, "Distance aux habitations", "Distance entre le support et la maison la plus proche, repérée dans le texte quand elle y figure.", None),
 ("c-hab-50", "c-habitations", "Moins de 50 m", "Habitation à moins de 50 m (Kersalous : 23 m).", None),
 ("c-hab-100", "c-habitations", "De 50 à 100 m", "Habitation entre 50 et 100 m.", None),
 ("c-hab-300", "c-habitations", "De 100 à 300 m", "Habitation entre 100 et 300 m.", None),
 ("c-hab-loin", "c-habitations", "Plus de 300 m", "Habitation au-delà de 300 m.", None),
]

NIVEAU = [
 ("j-premier", None, "Premier ressort (tribunal administratif)", "Jugements et ordonnances des TA.", None),
 ("j-appel", None, "Appel (cour administrative d'appel)", "Arrêts des cinq cours (Nantes, Douai, Bordeaux, Lyon, Marseille, Paris, Toulouse, Versailles, Nancy).", None),
 ("j-cassation", None, "Conseil d'État", "Cassation, avis et décisions en premier et dernier ressort.", None),
]

PROXIMITE = [
 ("x-tres-proche", None, "Très proche de Kersalous", "Score de 75 ou plus.", None),
 ("x-proche", None, "Proche", "Score de 50 à 74.", None),
 ("x-eloigne", None, "Éloignée", "Score de 25 à 49.", None),
 ("x-non-pertinente", None, "Non pertinente", "Score inférieur à 25 : toiture, faux positif, décision sans lien avec un pylône rural.", None),
]

TRANSFERABILITE = [
 ("t-transferable", None, "Transférable à Kersalous", "Le motif décisif s'applique à la parcelle YX 26.", None),
 ("t-verifier", None, "À vérifier pour Kersalous", "Dépend d'un fait à établir sur le terrain ou dans le dossier.", None),
 ("t-non-transferable", None, "Non transférable", "Motif propre à un contexte absent ici (loi Littoral, cyclones…).", None),
]

LECTURE = [
 ("l-auto", None, "Repérage automatique", "Classée par filtre et expressions régulières. Fiabilité limitée.", None),
 ("l-lu", None, "Lue par un humain ou un assistant", "Motifs et dispositif lus ; moyens retenus et écartés renseignés.", None),
 ("l-partiel", None, "Lue en partie (intertitres, motifs, dispositif)", "Intertitres des motifs, passages décisifs et dispositif lus ; le détail de chaque moyen n'a pas été relu.", None),
 ("l-verifie", None, "Vérifiée à la source officielle", "Texte comparé à Légifrance, ArianeWeb ou à la juridiction.", None),
]

ALL = {"Moyens": MOYENS, "Resultat": RESULTAT, "EffetProjet": EFFET, "ActeAttaque": ACTE, "Procedure": PROCEDURE,
       "Requerant": REQUERANT, "ContexteSite": CONTEXTE, "Niveau": NIVEAU, "Proximite": PROXIMITE,
       "Transferabilite": TRANSFERABILITE, "NiveauLecture": LECTURE}

# Moyens du dossier (dos:moyen-*) -> concepts de la taxonomie du corpus : la vue « Moyens & actions » en tire
# le nombre de décisions qui évoquent, retiennent ou écartent le moyen.
MOYEN_DOSSIER = {
 "dos:moyen-seuil-pc": ["m-emprise-locaux"],
 "dos:moyen-talus": ["m-regle-plantations"],
 "dos:moyen-zone-humide": ["m-zone-humide"],
 "dos:moyen-zone-a": ["m-zone-agri-naturelle"],
 "dos:moyen-covisibilite": ["m-covisibilite", "m-abords-mh-pc"],
 "dos:moyen-affichage": ["m-affichage"],
 "dos:moyen-numero-panneau": ["m-affichage"],
 "dos:moyen-dim": ["m-dim"],
 "dos:moyen-dim-incomplet": ["m-dim"],
 "dos:moyen-delai-dim": ["m-dim"],
 "dos:moyen-ondes": ["m-ondes"],
}


# Explications « en pratique » (skos:scopeNote) : ce que le moyen veut dire et comment les décisions lues l'ont traité.
EXPLICATIONS = {
 "m-qualite-petitionnaire": "Le demandeur d'une déclaration préalable ou d'un permis doit être propriétaire du terrain, son mandataire, ou attester sur l'honneur y être autorisé par lui (R.423-1 a, R.431-35). Le maire ne vérifie pas les titres : il ne refuse que si la fraude est établie ou s'il apparaît, sans contestation sérieuse, que le demandeur n'a aucun droit de déposer (jurisprudence rappelée par le TA de Nantes, 17 avril 2024, n° 2404854). Le moyen n'a été retenu qu'en référé et dans deux situations : la commune reconnaît s'être trompée sur sa qualité de propriétaire (TA de Lille, 29 avril 2026, Beuvry) ; les droits du demandeur sur la parcelle sont douteux, ici les espaces communs d'un lotissement (Talmont-Saint-Hilaire). Hors fraude ou erreur reconnue, le droit de propriété et les servitudes privées sont écartés : l'autorisation est délivrée sous réserve du droit des tiers. Pour Kersalous : savoir qui est propriétaire de la parcelle YX 26, quel contrat le lie à Phoenix, et ce que dit l'attestation de la déclaration.",
 "m-zone-agri-naturelle": "Dans une zone agricole (A) ou naturelle (N) d'un PLU, on ne construit en principe que pour l'agriculture ou la forêt, avec des exceptions dont celle des équipements d'intérêt collectif ou services publics, souvent sous conditions. La plupart des tribunaux (Pluguffan, Guiclan, La Gouesnière, Rousson en appel) admettent l'antenne comme équipement d'intérêt collectif et regardent si ses conditions sont remplies : non-incompatibilité avec l'activité agricole de l'unité foncière, absence d'atteinte aux espaces naturels et aux paysages (c'est la double condition de la zone A de Plonéour-Lanvern). Les annulations viennent du texte précis du PLU : à Amiens (2025), l'antenne n'est pas un « équipement public » et n'est admise que si un impératif technique justifie sa localisation ; à Bordeaux (2025), une modification du PLU avait supprimé les exceptions et la zone N interdisait toute construction (régularisable) ; à Neuville-sur-Oise (2026), la zone était dévolue aux sports et loisirs. À vérifier pour Kersalous : le texte exact de l'article A et l'usage agricole réel de la parcelle.",
 "m-desserte": "Si le projet exige des travaux sur les réseaux publics (électricité, eau), la déclaration préalable doit être refusée quand l'autorité ne peut pas dire dans quel délai et par quelle collectivité ou quel concessionnaire ils seront faits (L.111-11). À La Gouesnière (TA de Rennes, 2026), l'extension électrique de 408 m n'avait donné lieu à aucune démarche du maire auprès du syndicat d'énergie : suspension puis annulation. À Bouc-Bel-Air (TA de Marseille, 2023), le dossier ne précisait pas le raccordement, le poste haute tension étant à une centaine de mètres : sursis pour régulariser. Le moyen échoue quand l'arrêté met le coût du raccordement à la charge du pétitionnaire (Toutainville) ou quand le gestionnaire (Enedis) a été consulté (Le Beausset, régularisé). À vérifier pour Kersalous : distance au réseau, extension nécessaire, avis du gestionnaire dans le dossier.",
 "m-emprise-locaux": "Une déclaration préalable suffit tant que l'emprise au sol ou la surface de plancher créée reste sous 20 m² ; au-delà, il faut un permis. Les décisions lues ne comptent que les locaux et installations techniques, pas le pylône : à Nantes (2026), un massif béton de 31 m² avec une dalle affleurante de 6 m² reste en déclaration ; à Biot, une dalle enterrée de 25 m² ne compte pas ; à Pluguffan, 10,4 m² de surface de plancher. Écarté dans toutes les lectures. La fondation de Kersalous (29,16 m², dalle de 2 m²) tombe très probablement dans ce cas.",
 "m-abords-mh-pc": "Dans les abords d'un monument historique, une construction en covisibilité avec lui n'échappe au permis de construire que sous certaines conditions : au-delà de 12 m de haut, il faut un permis et la déclaration préalable est illégale. Trois tribunaux l'ont retenu (Le Vigan en 2023, Mont-Saint-Jean en 2023, Fourques en 2024) ; à Dijon, le juge a refusé de laisser régulariser. C'est le moyen non régularisable le plus sérieux hors littoral. À vérifier pour Kersalous : la parcelle YX 26 est-elle dans un périmètre délimité des abords du manoir, ou à moins de 500 m et visible en même temps ?",
 "m-regle-cloture": "Le PLU fixe souvent la hauteur et la nature des clôtures (par exemple 1,50 m ou 1,80 m maximum, mailles ou aspérités pour laisser passer la petite faune). Le poste technique d'une antenne est clôturé à 2 m : retenu 9 fois (Verrens-Arvey, La Baume-Cornillane, Toutainville, Fégréac, Rethondes…). Le vice ne porte que sur la clôture : annulation partielle puis régularisation en 3 à 6 mois. Il retarde, il ne tue pas le projet. À vérifier : le règlement de la zone A de Plonéour-Lanvern et la clôture prévue.",
 "m-incendie": "Le projet est au contact d'un massif boisé sans défense contre l'incendie (point d'eau, accès des secours). Retenu dans le Var (Cuers, Le Beausset) : sursis de 4 mois pour créer un point d'eau validé par le SDIS. Peu transférable en Finistère ; à contrôler si un boisement jouxte la parcelle (un espace boisé classé est à 34 m).",
 "m-acces": "Un nouvel accès sur une route départementale ou communale exige l'accord ou la consultation du gestionnaire de la voirie (R.423-53), et les règles du PLU sur la largeur et la desserte s'appliquent. Retenu à Saint-Cyr-en-Talmondais (Orange : nouvel accès sur la RD 45 sans consultation du gestionnaire ; annulation partielle, 6 mois pour régulariser) et à Sainte-Rose (Guadeloupe : un terrain sans accès à une voie publique est inconstructible ; sursis pour régulariser). Écarté quand l'accès existe déjà (Pluguffan).",
 "m-retrait": "Un maire ne peut pas retirer sa non-opposition à une antenne : l'article 222 de la loi ELAN l'interdit. Les retraits sont donc annulés à la demande de l'opérateur (ex. TA de Marseille, 20 juin 2023). Si la mairie de Plonéour-Lanvern retirait la décision ou la faisait renouveler, ce moyen jouerait contre elle ; hors ce cas, il n'avantage pas les riverains.",
 "m-interet-agir": "Pour attaquer une autorisation, il faut justifier d'un intérêt : être voisin dont les conditions d'occupation, d'utilisation ou de jouissance sont directement affectées (L.600-1-2). Le requérant doit préciser l'atteinte. Des distances de 60 à 200 m ont suffi avec vue directe (Plobannalec-Lesconil, Le Vigan, Fégréac) ; la cour administrative d'appel de Toulouse (2023) a jugé sans intérêt des riverains dont le bien n'était pas directement affecté. Environ 15 % des recours sont irrecevables.",
 "m-dim": "Le dossier d'information du maire (L.34-9-1 du code des postes, D.98-6-1) relève du droit des communications électroniques, pas de celui de l'urbanisme : le juge applique l'indépendance des législations et écarte le moyen comme inopérant. Jamais retenu dans le corpus pour annuler une déclaration préalable.",
 "m-competence": "Le signataire de l'arrêté doit avoir reçu une délégation de fonctions et de signature suffisamment précise. Retenu à Vallons-de-l'Erdre et à Achy : sursis à statuer, la commune régularise en quelques mois. Facile à vérifier, rarement décisif.",
 "m-rnu": "Hors parties urbanisées d'une commune sans PLU (règlement national d'urbanisme, carte communale), les constructions sont interdites sauf exceptions dont les équipements collectifs, à condition que le projet ne compromette pas l'activité agricole ou la qualité des paysages. Retenu à Montagnac-Montpezat (TA de Marseille, 2022, sursis) et à Beyrie-sur-Joyeuse (TA de Pau, 2023). Sans objet à Plonéour-Lanvern, qui a un PLU.",
 "m-pieces-contradictoires": "Si les pièces du dossier se contredisent sur un fait décisif (hauteur, emprise, position), la décision repose sur des faits inexacts. TA de Nîmes (11 septembre 2026, n° 2604044) : suspension d'une déclaration de Phoenix France Infrastructure. À vérifier pour Kersalous : 30 m sur le panneau, 32,65 m dans le dossier d'information ; seul compte ce que disent les pièces de la déclaration elle-même.",
 "m-paysage": "L'article R.111-27 permet de refuser ou d'encadrer un projet qui porte atteinte au caractère ou à l'intérêt des lieux avoisinants, aux sites, aux paysages. Le juge ne retient que l'erreur manifeste, rarement pour un pylône treillis entouré de végétation. Retenu en référé à Biot (environnement exceptionnel de golf et d'espaces naturels, aucun aménagement discret), puis non retenu au fond ; retenu à Roscoff avec covisibilité et à Beyrie-sur-Joyeuse.",
}

EXPLICATIONS["m-littoral"] = "La loi Littoral (L.121-1 et suivants) ne s'applique qu'aux communes littorales (article L.321-2 du code de l'environnement). Plonéour-Lanvern (INSEE 29174) n'est pas dans la liste officielle des 121 communes littorales et estuariennes du Finistère (DDTM 29, mise à jour du 19 juin 2019) : vérifié le 15 octobre 2026. Ses voisines Plomeur, Saint-Jean-Trolimon, Plovan, Pouldreuzic, Pont-l'Abbé, Combrit, Loctudy et Penmarc'h y sont, d'où les annulations de Plomeur et de Plobannalec-Lesconil. C'est le motif le plus gagnant de l'Ouest (10 décisions lues : Locmaria-Plouzané, Fouesnant, Roscoff, Carnac…) mais il ne joue pas à Kersalous."

EXPLICATIONS["m-foncier-communal"] = "TA de Limoges, 24 novembre 2022 (Saint-Jouvent, TDF) : la délibération par laquelle le conseil municipal vendait 147 m² de son domaine privé à l'opérateur est annulée, car le pylône était à 48 m d'une habitation, avec un fort impact visuel, et aucune recherche d'autre site n'avait été faite : le juge y voit une erreur manifeste d'appréciation de l'intérêt général. À vérifier pour Kersalous : à qui appartient la parcelle YX 26 ? Si c'est un particulier, ce moyen ne joue pas."
EXPLICATIONS["m-littoral"] = EXPLICATIONS["m-littoral"] + " Le TA de Rennes avait rejeté le recours à Cléden-Cap-Sizun ; la cour administrative d'appel de Nantes l'a accueilli le 13 octobre 2026 (n° 24NT03613), en jugeant le pylône isolé de toute construction et le vice non régularisable. La loi s'applique aussi aux rives des grands plans d'eau (Bas-Chablais, lac Léman)."
EXPLICATIONS["m-interet-agir"] = EXPLICATIONS["m-interet-agir"] + " Autres cas admis : 410 m avec vue directe sur un pylône de 30 m en terrain agricole peu boisé (CAA de Nantes, Cléden-Cap-Sizun, 2026) ; 13 m en ville (TA de Melun, Alfortville) ; 48 m (TA de Limoges)."

EXPLICATIONS["m-emprise-locaux"] = "Une déclaration préalable suffit tant que les locaux et installations techniques restent à 20 m² au plus de surface de plancher et d'emprise au sol ; au-delà, il faut un permis. L'avis du Conseil d'État du 21 mars 2024 (n° 490536, lu à la source) précise que seule compte l'emprise des **locaux et installations techniques**, **pas celle des pylônes** ; il est né de l'affaire de Guichen (TA de Rennes). Les décisions lues le confirment : à Nantes (2026), un massif béton de 31 m² avec une dalle affleurante de 6 m² reste en déclaration ; à Biot, une dalle enterrée de 25 m² ne compte pas ; à Pluguffan, 10,4 m² de surface de plancher. Écarté dans toutes les lectures. La fondation de Kersalous (29,16 m², dalle de 2 m²) relève du pylône et ne compte donc très probablement pas."
EXPLICATIONS["m-risques-naturels"] = "Un plan de prévention des risques (inondation, incendie de forêt) fixe ce qui est interdit ou admis dans une zone, souvent avec une exception pour les équipements publics. Les antennes d'opérateurs privés n'entrent généralement pas dans cette exception. Retenu à Guichen, en Ille-et-Vilaine (TA de Rennes, confirmé par la CAA de Nantes le 8 juillet 2025, n° 24NT02240 : zone rouge du PPRI de la Vilaine, une antenne n'est pas un « réseau divers » d'infrastructure publique), à Nice (zone rouge du plan incendie, TA 2024 et CAA de Marseille le 18 juin 2026) et à Marseillan (zone rouge Rn). Écarté quand le projet est surélevé et non clôturé pour laisser passer l'eau (CAA de Bordeaux, Latresne, 2024). À vérifier pour Kersalous : le terrain est-il dans un plan de prévention des risques, ou la zone humide à 8 m a-t-elle un classement réglementaire ?"
EXPLICATIONS["m-montagne"] = "Dans les communes de montagne, l'urbanisation se fait en continuité avec les bourgs, villages et hameaux (L.122-5) et les installations ne sont admises que dans des cas limités (L.122-3). CAA de Nancy, 21 mai 2026 (Arçon, Doubs, Free) : annulation confirmée. Sans objet dans le Finistère."
EXPLICATIONS["m-patrimoine"] = "Site patrimonial remarquable, aire de mise en valeur de l'architecture et du patrimoine (AVAP), site classé ou inscrit : le règlement du site peut interdire ou encadrer le pylône. CAA de Nantes, 4 juillet 2025 (n° 23NT03540, Orange) : annulation confirmée, le vice n'est pas régularisable au regard du règlement de l'AVAP devenue site patrimonial remarquable. À vérifier pour Kersalous : la parcelle YX 26 est-elle dans un périmètre de ce type (le périmètre des abords du monument est à 163 m) ?"
EXPLICATIONS["m-dossier-incomplet"] = "Les pièces exigées pour une déclaration préalable sont limitativement listées (R.431-35 à R.431-37) ; une insuffisance n'annule que si elle a faussé l'appréciation de l'administration. Presque toujours écarté. Retenu à Dammarie-les-Lys (CAA de Paris, 10 juillet 2025, n° 23PA02598) : les photomontages ne montraient ni les constructions voisines ni le pylône sur toute sa hauteur (R.431-10 c et d) ; le vice n'a pas été régularisé et l'arrêté est annulé. À Melun (TA, 2023) le motif était plus étroit (R.431-36 b) et la cour l'avait écarté."
EXPLICATIONS["m-interet-agir"] = EXPLICATIONS["m-interet-agir"] + " Pour les moyens de recevabilité, « retenu » veut dire que le juge a déclaré le recours irrecevable (au détriment du requérant) et « écarté » qu'il a admis l'intérêt à agir."
