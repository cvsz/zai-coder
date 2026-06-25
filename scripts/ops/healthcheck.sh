#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8765}"
echo "Checking $BASE_URL"
curl -fsS "$BASE_URL/healthz"
echo
curl -fsS "$BASE_URL/readyz"
echo
