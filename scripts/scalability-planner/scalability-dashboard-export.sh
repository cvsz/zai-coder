#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/scalability-planner/scalability-planner-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
printf '<h1>Multi Region Edge and Scalability Planner</h1>\n' > "$OUT"
echo "$OUT"
