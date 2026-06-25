#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/package-registry/package-registry-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
printf '<h1>Package Registry and Marketplace Publishing</h1>\n' > "$OUT"
echo "$OUT"
