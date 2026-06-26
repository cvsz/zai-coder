#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
REPO_NAME="${REPO_NAME:-zai-coder-control-plane}"
VISIBILITY="${VISIBILITY:-public}"
DESCRIPTION="${DESCRIPTION:-Local-first AI coding, automation, App Studio, deployment, integration, and SaaS control plane scaffold.}"
echo "repo=$REPO_NAME visibility=$VISIBILITY apply=$APPLY"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to create repository."
  exit 0
fi
if [ "$VISIBILITY" = "private" ]; then
  gh repo create "$REPO_NAME" --private --description "$DESCRIPTION" --source=. --remote=origin
else
  gh repo create "$REPO_NAME" --public --description "$DESCRIPTION" --source=. --remote=origin
fi
