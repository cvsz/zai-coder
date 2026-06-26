#!/usr/bin/env bash
set -euo pipefail

MESSAGE="${1:-${MESSAGE:-chore: update zai coder control plane}}"
APPLY="${APPLY:-0}"

echo "== GPG signed commit plan =="
echo "message: $MESSAGE"
echo "apply:   $APPLY"

echo
git status --short

if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to create signed commit."
  exit 0
fi

export GPG_TTY="${GPG_TTY:-$(tty)}"
git commit -S -m "$MESSAGE"
