#!/usr/bin/env bash
set -euo pipefail

APPLY="${APPLY:-0}"
IMAGE="${IMAGE:-zai-coder-app-studio:local}"

echo "== Docker build plan =="
echo "image: $IMAGE"
echo "apply: $APPLY"

if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to build image."
  exit 0
fi

docker build -t "$IMAGE" .
