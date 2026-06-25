#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/final-release/final-enterprise-release-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
printf '<h1>Final Enterprise Release Pack</h1>\n' > "$OUT"
echo "$OUT"
