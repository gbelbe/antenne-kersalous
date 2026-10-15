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
 ("m-hauteur-12m", "m-qualification", "Hauteur de plus de 12 m",
  "Seuil de hauteur qui fait basculer certaines constructions vers le permis de construire.",
  r"12 mètres|douze mètres|hauteur.{0,30}supérieure à 12"),

 ("m-reglement", None, "Règles d'urbanisme applicables au terrain",
  "Conformité du projet au plan local d'urbanisme, au règlement national d'urbanisme et aux lois d'aménagement spécial.", None),
 ("m-zone-agri-naturelle", "m-reglement", "Zone agricole ou naturelle (équipement d'intérêt collectif)",
  "Le pylône est-il admis en zone A ou N comme équipement d'intérêt collectif ou service public ? La plupart des tribunaux répondent oui.",
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
  "Projet implanté dans un emplacement réservé ou une zone prévue pour un équipement public. TA Montpellier, 13 février 2026, n° 2600444 (Saint-Just, Phoenix France Infrastructure 3) : suspension ; la commune ne peut corriger l'implantation par une prescription.",
  r"emplacement réservé|emplacements réservés|L\.? ?151-41|zone réservée"),
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
 ("m-natura", "m-milieux", "Natura 2000, ZNIEFF, espèces protégées", "Zonages d'inventaire ou de protection de la biodiversité.",
  r"Natura 2000|ZNIEFF|espèces? protégées?|biodiversité|trame verte|corridor écologique"),

 ("m-dossier", None, "Exactitude et complétude du dossier de la demande",
  "Le dossier permettait-il à l'administration d'apprécier le projet ? Une décision fondée sur des faits inexacts est illégale.", None),
 ("m-pieces-contradictoires", "m-dossier", "Pièces contradictoires ou faits inexacts",
  "Les pièces du dossier se contredisent (hauteur, emprise, position). TA Nîmes, 11 septembre 2026, n° 2604044 : suspension d'une DP de Phoenix France Infrastructure.",
  r"inexact|incohéren|discordan|erreur matérielle|faits matériellement|pièces?.{0,40}contradictoires"),
 ("m-dossier-incomplet", "m-dossier", "Dossier de déclaration incomplet", "Pièce manquante ou insuffisante (R.431-36 et suivants).",
  r"incomplet|R\.? ?431-36|R\.? ?431-|pièce.{0,30}manquant|notice (?:descriptive|insuffisante)"),
 ("m-fraude", "m-dossier", "Fraude", "Manœuvre destinée à tromper l'administration sur le projet.", r"fraude|manœuvre frauduleuse"),

 ("m-instruction", None, "Régularité de l'instruction et de la décision", "Compétence, avis obligatoires, délais, motivation, retrait de la décision.", None),
 ("m-abf", "m-instruction", "Avis de l'architecte des Bâtiments de France", "Avis non recueilli alors que le projet est dans un périmètre protégé.",
  r"architecte des bâtiments de France|\bABF\b|avis conforme"),
 ("m-retrait", "m-instruction", "Retrait d'une non-opposition par le maire", "Le maire retire sa décision tacite ou expresse (L.424-5, art. 222 de la loi ELAN). Souvent annulé à la demande de l'opérateur.",
  r"retrait.{0,80}(?:non-opposition|décision tacite|décision implicite)|L\.? ?424-5|article 222|loi ELAN|loi du 23 novembre 2018"),
 ("m-competence", "m-instruction", "Compétence du signataire", "Incompétence ou défaut de délégation.", r"incompétence|délégation de signature"),
 ("m-motivation", "m-instruction", "Motivation et procédure contradictoire", "Insuffisance de motivation ou atteinte aux droits de la défense.",
  r"insuffisamment motivé|défaut de motivation|principe du contradictoire"),
 ("m-delai-instruction", "m-instruction", "Délai d'instruction", "Décision tacite, majoration du délai, date de naissance de la non-opposition.",
  r"délai d'instruction|R\.? ?423-\d+"),

 ("m-securite", None, "Sécurité et santé publiques", "Risques invoqués contre le projet.", None),
 ("m-r111-2", "m-securite", "Sécurité et salubrité publiques (R.111-2)", "Risque pour la sécurité ou la salubrité publique.",
  r"R\.? ?111-2\b|sécurité publique|salubrité"),
 ("m-vent-chute", "m-securite", "Vent, chute, incendie, foudre", "Risque d'effondrement, de chute de glace, d'incendie.",
  r"effondrement|chute|tempête|cyclone|incendie|foudre"),
 ("m-ondes", "m-securite", "Ondes, santé et principe de précaution", "Effets des champs électromagnétiques et principe de précaution (Charte de l'environnement, art. 5). Écarté dans toutes les décisions lues : la police des ondes appartient à l'État.",
  r"\bondes\b|champs? électromagnétiques?|principe de précaution|charte de l'environnement|rayonnement"),
 ("m-risques-naturels", "m-securite", "Risques naturels (inondation, crue, argile)", "Plan de prévention des risques, cote de référence, retrait-gonflement des argiles.",
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

 ("m-recevabilite", None, "Recevabilité du recours", "Conditions pour que le juge examine la requête.", None),
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
 ("q-commune", None, "Commune ou collectivité", "Maire, commune, établissement public.", None),
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
