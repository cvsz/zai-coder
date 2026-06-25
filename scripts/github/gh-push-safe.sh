#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
BRANCH="${BRANCH:-main}"
echo "branch=$BRANCH apply=$APPLY"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to push."
  exit 0
fi
git status --short
git push -u origin "$BRANCH"
