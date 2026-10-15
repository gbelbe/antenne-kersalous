# Corpus de décisions : où est quoi

| Élément | Emplacement | Rôle |
|---|---|---|
| Textes d'origine | `corpus/decisions/<TA\|CAA\|CE>/<année>/<fichier>.xml` | Copie exacte des XML de l'[open data de la justice administrative](https://opendata.justice-administrative.fr) (Licence Ouverte 2.0). Ne pas modifier. |
| Registre | `corpus/manifest.csv` | Pour chaque fichier : chemin, empreinte SHA-256, archive mensuelle d'origine (URL), date de collecte, licence. |
| Index et lectures | `corpus/index_decisions.csv`, `corpus/lectures.csv`, `corpus/RAPPORT.md` | Classement initial, 31 décisions lues, synthèse. |
| Classement | `corpus/classement.json` | Résultat intermédiaire du classement (score, résultat, effet, requérants). |
| Taxonomie | `antenne-contentieux.ttl` | 11 schémas SKOS, 133 concepts, termes d'ontologie. **Généré** depuis `tools/corpus/taxo_spec.py`. |
| Loi Littoral | `antenne-littoral.ttl` (généré par `tools/corpus/littoral.py` depuis `corpus/communes_littorales_29.csv`) | Taxonomie des 121 communes littorales et estuariennes du Finistère (liste DDTM 29 du 19 juin 2019), plus Plonéour-Lanvern comme commune non soumise. Les décisions des tribunaux de Rennes et de Nantes dont la commune est dans la liste y sont reliées. |
| Décisions dans le graphe | `antenne-decisions.ttl` | Une fiche `ant:Jurisprudence` par décision, reliée aux concepts, avec un nœud `src:` de provenance (fichier local, empreinte, archive). **Généré**. |

## Régénérer

```bash
python3 -I tools/corpus/taxonomie.py "$PWD"        # antenne-contentieux.ttl
python3 -I tools/corpus/build_decisions.py "$PWD"  # antenne-decisions.ttl (3 minutes)
python3 tools/build_site.py                        # site : vue « Corpus »
```

Ajouter un concept ou corriger une expression régulière : modifier `tools/corpus/taxo_spec.py`, puis relancer les deux premières commandes. Les moyens retenus ou écartés des décisions lues sont saisis à la main dans `tools/corpus/lectures_map.py`.

## Ce qui est automatique et ce qui ne l'est pas

- **Moyens « évoqués »** : repérés par expression régulière dans tout le texte, visas compris. Un moyen évoqué n'est ni retenu ni même soulevé : il est cité.
- **Moyens retenus / écartés** : renseignés à la main pour les 93 décisions lues (`skt:l-lu`, 32) ou lues en partie (`skt:l-partiel`, 61 : intertitres, passages décisifs, dispositif). Pour 476 rejets complets, les moyens discutés dans les motifs sont déduits « écartés » (`ant:moyenEcarteDeduit`). Pour toutes les autres décisions, « retenu » est inconnu, pas nul.
- **Requérant, acte, résultat** : issus du classement automatique de l'index, corrigés pour les associations (nom lu dans le texte).
- **Avocats** : « représenté par Me X, demande » (requérant) ou « conclut » (partie adverse). Nom de famille seul, homonymes possibles.
- **Score de proximité** : somme de critères visibles dans `ant:detailScore` ; discutable décision par décision.
- **Distance aux habitations** : repérée dans 208 décisions seulement.

## Retrouver une décision

- Sur le site : vue **Corpus** (filtres par axe, recherche par numéro, tribunal, association ou avocat).
- Dans le graphe : `ant:aPourConcept` (propriété mère de toutes les facettes) ; exemple dans `requetes.sparql`.
