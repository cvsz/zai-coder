#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/security-ops/security-ops-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
printf '<h1>Security Operations and Threat Monitoring</h1>\n' > "$OUT"
echo "$OUT"
