# Publier le site

Le dépôt génère un site statique (carte, chronologie, jurisprudence, propriétaires de pylônes, sources, explorateur) à partir des fichiers `*.ttl`. GitHub Actions le reconstruit et le publie sur GitHub Pages **à chaque push** qui touche le graphe.

## Mise en route (une fois)

1. Relire `publish.toml` (voir « Ce qui est publié » ci-dessous).
2. Pousser le dépôt sur GitHub (`git push`).
3. *Settings → Pages → Build and deployment → Source : **GitHub Actions***.
4. Le premier déploiement part au push suivant, ou à la main : onglet *Actions → Publier le site → Run workflow*.
5. Le site est à `https://<utilisateur>.github.io/<dépôt>/`.

> ⚠ **Un site GitHub Pages est public**, même si le dépôt est privé (sauf offre Enterprise).

## Voir le site en local

```bash
pip install -r tools/requirements.txt
tools/publish.sh serve        # http://localhost:8000
tools/publish.sh check        # contrôle de confidentialité partiel
node tools/smoke_test.js      # chaque vue et chaque fiche se rendent
```

## Mise à jour automatique

Le workflow `.github/workflows/pages.yml` se déclenche sur un push modifiant `*.ttl`, `publish.toml`, `requetes.sparql`, `tools/`, `site-src/` ou `sources/`. Modifier le graphe, commiter, pousser : le site est à jour en une à deux minutes. Le pied de page affiche la date du dernier commit. Les délais (« dans 12 jours ») sont calculés dans le navigateur : ils restent justes sans reconstruction.

## Ce qui est publié, ce qui ne l'est pas

Tout est réglé dans `publish.toml`.

| Élément | Par défaut |
|---|---|
| Graphe (entités, relations, notes, sources) | publié, **après retrait** des entités masquées |
| Habitations riveraines (classe `Batiment`) | masquées (position de particuliers) |
| Personnes physiques | masquées, sauf `allow_persons` (maire, personne nommée sur l'avis public) |
| Propriétaire de la parcelle, exploitant, porteur du dossier | masqués |
| Fichiers de `sources/` | **aucun**, sauf ceux listés dans `[files].publish` (photos de l'avis et du panneau, parcelle, rapport de couverture, table ANFR) |
| Courriels, courrier du maire, dossier d'information (`sources/pdf/`, `mail_*.txt`) | non publiés |
| Fichier Turtle téléchargeable | version filtrée `data/graphe-public.ttl`, jamais les `.ttl` bruts |

Les masquages s'appliquent aux données **et** aux relations : une entité masquée disparaît des fiches qui la citaient. Pour retirer une expression d'un texte, ajoutez une expression régulière à `redact`.

`tools/publish.sh check` cherche quelques motifs sensibles ; il ne remplace pas une relecture.

## Cartes

- **Carte interactive** : Leaflet, fonds OpenStreetMap et orthophoto IGN (sans clé), supports colorés par propriétaire, couverture 4G, cercles de distance. Chaque point a un lien *Google Maps* et *Street View*.
- **Vue Google Maps** : par défaut, intégration satellite **sans clé** centrée sur le site (non officielle, peut changer). Pour l'API officielle, créez une clé *Maps Embed API*, **restreignez-la aux référents** `https://<utilisateur>.github.io/*`, puis ajoutez-la comme secret `GOOGLE_MAPS_API_KEY` du dépôt. Elle sera visible dans le code du site : la restriction par référent est indispensable.
- Les tuiles Google ne sont pas utilisées dans la carte interactive (leurs conditions l'interdisent en dehors de l'API Maps).

## Où modifier quoi

| Je veux… | Fichier |
|---|---|
| Changer titre, avertissement, masquages | `publish.toml` |
| Changer l'apparence ou une vue | `site-src/` (`app.js`, `style.css`, `index.html`) |
| Changer ce qui est extrait du graphe | `tools/build_site.py` |
| Ajouter un évènement à la chronologie | le graphe : `ant:Evenement` avec `ant:dateEvenement` |
| Ajouter une décision de justice | le graphe : `ant:Jurisprudence` (voir `antenne-jurisprudence.ttl`) |

La chronologie, la jurisprudence, les moyens, les propriétaires et les sources sont **lus dans le graphe** : aucune de ces pages n'est écrite à la main.

## Identité des commits

Les commits doivent porter uniquement l'adresse `385068+gbelbe@users.noreply.github.com`. Trois protections :

- **Réglage git** : identité du dépôt (`git config user.name/user.email`) et, au niveau du dossier, `[includeIf "gitdir:~/Documents/adeo_ster/antenne/"]` dans `~/.gitconfig` vers `~/.gitconfig-perso`. `user.useConfigOnly = true` empêche git de deviner une identité.
- **Hooks locaux** (`.githooks/`, activés par `git config core.hooksPath .githooks` — à refaire après un nouveau clone) : `commit-msg` refuse un commit dont l'auteur n'est pas l'adresse autorisée ou dont le message contient une adresse professionnelle ; `pre-push` contrôle les commits avant l'envoi.
- **CI** (`.github/workflows/identity.yml`) : alerte après coup si un commit poussé porte une autre identité.

Les règles sont dans `tools/check_identity.sh` (`ALLOWED_EMAIL`, `BLOCKED_PATTERNS`). Contrôle manuel : `git log --all --format='%ae %ce' | sort | uniq -c`.
