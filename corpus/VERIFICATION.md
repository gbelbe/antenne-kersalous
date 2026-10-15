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

**Appels (lecture à part, non chiffrée).** Les appels et le Conseil d'État ne sont pas dans le taux. J'ai lu les arrêts où les signaux A et B indiquent une victoire de tiers ou un renversement. Un jugement peut être renversé dans les deux sens :
- **Riverains gagnants en appel :** CAA de Nantes, 13 octobre 2026, n° 24NT03613 (Cléden-Cap-Sizun, Finistère : le TA de Rennes avait rejeté, la cour annule pour la loi Littoral) ; CAA de Bordeaux, 2 octobre 2025 (Guadeloupe, cyclones) ; CAA de Lyon, 6 février 2024 (raccordement électrique insuffisamment précis) ; CAA de Douai, 20 octobre 2022 (clôture grillagée de 2 m).
- **Annulations de première instance infirmées :** CAA de Nantes, 20 septembre 2022 (Saint-Léger-le-Petit) ; CAA de Bordeaux, 15 février 2024 (Latresne, zone rouge d'inondation : les riverains paient 1 000 € à chaque partie adverse) ; CAA de Versailles, 12 décembre 2022 (Vaucresson).
- **Annulations confirmées :** CAA de Nantes, 11 février 2025 (Carnac) ; CAA de Lyon, 13 décembre 2022 (Talloires).

**Limites.** Les appels et les décisions du Conseil d'État ne sont pas dans ce taux. Un taux de victoire n'est pas une probabilité pour un dossier donné : les motifs gagnants dépendent du lieu (loi Littoral, PLU, abords d'un monument).

Scripts : `tools/corpus/verif_victoires.py` (signaux A et B), `tools/corpus/taux.py` (tableau), `tools/corpus/victoires.py` (première version, abandonnée).
