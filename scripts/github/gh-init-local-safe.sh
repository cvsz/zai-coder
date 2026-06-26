#!/usr/bin/env bash
set -euo pipefail

APPLY="${APPLY:-0}"
BRANCH="${BRANCH:-main}"

echo "== Git init local plan =="
echo "branch: ${BRANCH}"
echo "apply:  ${APPLY}"

if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to initialize local repository."
  exit 0
fi

if [ ! -d .git ]; then
  git init
fi

git branch -M "$BRANCH"

echo "DONE: git initialized."
