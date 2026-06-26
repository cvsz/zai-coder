#!/usr/bin/env bash
set -euo pipefail

APPLY="${APPLY:-0}"
echo "== Local deploy plan =="
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: make production-migrate-plan && make serve-fastapi"
  exit 0
fi

make production-migrate-apply APPLY=1
make serve-fastapi
