# Vérifier qu'on a trouvé toutes les victoires de tiers

**Question.** Mon premier repérage du requérant (riverain, opérateur, commune…) se trompait souvent, donc le taux de réussite des riverains pouvait être sous-estimé. Comment s'assurer qu'aucune victoire n'a été oubliée ?

**Méthode : deux signaux indépendants, puis lecture de tous les désaccords.**

1. **Signal A, la solution enregistrée par la juridiction** (métadonnée « Solution » de l'open data) : « Satisfaction totale », « Satisfaction partielle », « Suspension accordée », « Sursis à statuer ». Une victoire de tiers est forcément dans cet ensemble (1 545 décisions de tribunaux administratifs).
2. **Signal B, la nature de l'acte annulé ou suspendu**, lue dans le dispositif (« l'arrêté par lequel le maire *ne s'est pas opposé*… est annulé ») et, à défaut, dans la première mention de l'acte dans le texte. Un acte **favorable** (non-opposition, permis) annulé = victoire d'un tiers ; un acte **défavorable** (opposition, refus, retrait, sursis, prescription) annulé = victoire de l'opérateur. Les deux lectures concordent dans 97 % des cas où le dispositif nomme l'acte (626 sur 644).
3. **Croisement.** « Satisfaction » + acte favorable = victoire de tiers possible, que le requérant soit détecté ou non (233 décisions).
4. **Lecture de tous les désaccords et incertitudes**, sans échantillonnage :
   - 100 décisions « acte favorable » où le requérant ressemblait à un opérateur : toutes sont des opérateurs contre une mairie (prescriptions, sursis, oppositions). Aucune victoire de tiers cachée.
   - 39 décisions « acte favorable », requérant tiers, non lues jusque-là : 7 victoires ajoutées (dont 4 **déférés du préfet**, que mon premier repérage rangeait mal : Locmaria-Plouzané dans le Finistère, Guérande, Marseillan, Marseille ; 2 de la commune de Nice contre des décisions du préfet ; 1 de riverains à Nice, zone rouge du plan de risque incendie).
5. **Audit des négatifs.** 45 décisions tirées au hasard parmi les 562 « Satisfaction » dont l'acte est défavorable : 44 sont bien des opérateurs contre une opposition ou un refus, 1 est ambiguë (refus d'abroger).

**Résultat.** Aucune victoire de tiers contre une autorisation n'a été trouvée en dehors de ce qui est maintenant classé. Les erreurs restantes possibles : une décision dont ni le dispositif ni la première mention ne nomment l'acte (6 cas sur 1 545, tous relus : des opérateurs contre une mairie), et les victoires hors open data.

**Taux corrigé** (tribunaux administratifs, antenne comme sujet, acte attaqué = autorisation, requérant lu dans le texte) : `corpus/taux.json`.

| Requérant | Décisions | Gagné, suspension ou sursis |
|---|---|---|
| Riverains | 276 | 39 (14 %) |
| Association ou collectif | 15 | 2 (13 %) |
| Syndicat ou SCI | 19 | 4 (21 %) |
| Préfet (déféré) | 4 | 3 (75 %) |
| Commune | 18 | 3 (17 %) |
| **Tous** | **332** | **51 (15 %)** |
| dont au fond | 239 | 41 (17 %) |
| dont en référé | 93 | 10 (11 %) |

Les désistements et non-lieux (environ 90) sont sous-comptés parce que leur acte n'est pas toujours identifiable : en les ajoutant, on tombe vers **12 %**. L'ancien chiffre (« environ 10 % ») venait d'une population et d'un repérage différents ; il restait de bon ordre de grandeur mais sous-estimait les victoires des préfets et des syndicats.

**Appels et Conseil d'État (lecture systématique du 2026-10-15).** Sur 263 décisions (179 cours d'appel, 84 Conseil d'État), 153 portent sur des antennes ; pour 73 d'entre elles l'acte en cause est une autorisation (non-opposition, permis). Pour chacune, j'ai classé le sens du jugement de première instance et le résultat de l'appel, puis lu les arrêts où des tiers gagnent, perdent après avoir gagné, ou voient un rejet renversé. Les environ vingt-cinq appels de tiers simplement rejetés n'ont pas été lus en détail.
- **Annulations de première instance confirmées : 13** (Carnac, Fouesnant, Moëlan-sur-Mer, Guichen, Ambon, Langueux, Lattes, Arçon, Nice, Beaumont-lès-Valence, Talloires, Dammarie-les-Lys…). Motifs : loi Littoral (Fouesnant, Moëlan-sur-Mer, Ambon, Lattes, Carnac, Corse), plan de prévention des risques (Guichen, Nice), règlement du site patrimonial (Nantes), loi Montagne (Arçon), recul de 10 m (Beaumont-lès-Valence), zone UY (Langueux), photomontages insuffisants (Dammarie-les-Lys).
- **Annulations de première instance infirmées : 9 environ** (Saint-Léger-le-Petit, Latresne, Vaucresson, Vérac, Vincennes, Marseille…).
- **Rejets de première instance renversés au profit de tiers : peu.** Cléden-Cap-Sizun (CAA de Nantes, 13 octobre 2026), Guadeloupe (2025), Lyon (raccordement électrique, 2024), Douai (clôture, 2022). Les autres renversements d'ordonnances d'irrecevabilité (Caen, Marseille, Nantes) ont rouvert l'affaire sans donner raison au requérant sur le fond.
- **Conseil d'État.** Presque toujours « pourvoi non admis ». L'avis du 21 mars 2024 (n° 490536) a été lu : seuls comptent les locaux et installations techniques, pas les pylônes, pour les seuils de 5 et de 20 m².

**Limites.** Les appels et les décisions du Conseil d'État ne sont pas dans ce taux. Un taux de victoire n'est pas une probabilité pour un dossier donné : les motifs gagnants dépendent du lieu (loi Littoral, PLU, abords d'un monument).

Scripts : `tools/corpus/verif_victoires.py` (signaux A et B), `tools/corpus/taux.py` (tableau), `tools/corpus/victoires.py` (première version, abandonnée).
