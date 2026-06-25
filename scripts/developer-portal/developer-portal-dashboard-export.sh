#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/developer-portal/developer-portal-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
printf '<h1>Developer Portal and API Docs</h1>\n' > "$OUT"
echo "$OUT"
