#!/usr/bin/env bash
# Vérifie l'identité des commits d'une plage : refuse toute adresse bloquée, et toute adresse d'auteur
# ou de committer différente de l'adresse autorisée.
#   tools/check_identity.sh <rev-list args>     ex. tools/check_identity.sh origin/master..HEAD
# Réglages : ALLOWED_EMAIL (adresse autorisée), BLOCKED_PATTERNS (regex insensible à la casse).
set -euo pipefail
ALLOWED_EMAIL="${ALLOWED_EMAIL:-385068+gbelbe@users.noreply.github.com}"
BLOCKED_PATTERNS="${BLOCKED_PATTERNS:-leroymerlin|\.hq\.corp|@adeo}"
# GitHub Actions et les fusions faites sur github.com utilisent leurs propres adresses noreply : tolérées.
OTHER_OK='^(noreply@github\.com|[0-9]+\+[A-Za-z0-9-]+@users\.noreply\.github\.com|[0-9]+\+github-actions\[bot\]@users\.noreply\.github\.com)$'
bad=0
for c in $(git rev-list "$@"); do
  ae=$(git log -1 --format=%ae "$c"); ce=$(git log -1 --format=%ce "$c")
  for e in "$ae" "$ce"; do
    if [ "$e" != "$ALLOWED_EMAIL" ] && ! printf '%s' "$e" | grep -Eq "$OTHER_OK"; then
      echo "✗ $(git log -1 --format='%h %s' "$c") : adresse non autorisée <$e>"; bad=1
    fi
  done
  if git log -1 --format='%an %ae %cn %ce%n%B' "$c" | grep -Eiq "$BLOCKED_PATTERNS"; then
    echo "✗ $(git log -1 --format='%h %s' "$c") : motif bloqué (adresse ou nom d'entreprise) dans l'identité ou le message"; bad=1
  fi
done
exit $bad
