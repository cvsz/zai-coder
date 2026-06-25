#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/migration-center/migration-center-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
printf '<h1>Data Import Export and Migration Center</h1>\n' > "$OUT"
echo "$OUT"
