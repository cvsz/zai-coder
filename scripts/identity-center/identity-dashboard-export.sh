#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/identity-center/identity-center-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
printf '<h1>Enterprise SSO and Identity Center</h1>\n' > "$OUT"
echo "$OUT"
