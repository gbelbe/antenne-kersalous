#!/usr/bin/env bash
# Utilitaire local de publication.
#   tools/publish.sh build     construit _site/
#   tools/publish.sh serve     construit puis sert http://localhost:8000
#   tools/publish.sh check     vérifie que rien de privé n'est dans _site/ (noms, adresses, fichiers)
#   tools/publish.sh push      commit-vérifie puis pousse : GitHub Actions publie (à lancer après relecture)
set -euo pipefail
cd "$(dirname "$0")/.."
cmd="${1:-build}"

check() {
  python3 tools/build_site.py >/dev/null
  fail=0
  # fichiers copiés : uniquement ceux de publish.toml
  for f in _site/files/*; do echo "  fichier publié : $(basename "$f")"; done
  # motifs sensibles (ajouter les vôtres dans PRIVATE_PATTERNS, séparés par |)
  pat="${PRIVATE_PATTERNS:-Habitation riveraine}"
  if grep -rIlE "$pat" _site/data _site/files 2>/dev/null | grep -v SHA256SUMS; then
    echo "⚠ motif sensible trouvé ci-dessus"; fail=1
  fi
  [ $fail -eq 0 ] && echo "✓ aucun motif sensible trouvé (vérification partielle : relisez publish.toml)" || exit 1
}

case "$cmd" in
  build) python3 tools/build_site.py ;;
  serve) python3 tools/build_site.py --serve ;;
  check) check ;;
  push)
    check
    git diff --quiet && git diff --cached --quiet || { echo "Des modifications ne sont pas commitées."; exit 1; }
    git push
    echo "Poussé. Suivez le déploiement : gh run watch  (ou l'onglet Actions du dépôt)"
    ;;
  *) echo "usage: $0 build|serve|check|push"; exit 2 ;;
esac
