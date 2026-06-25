#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/go-live-command-center/go-live-command-center-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
printf '<h1>Production Readiness and Go Live Command Center</h1>\n' > "$OUT"
echo "$OUT"
