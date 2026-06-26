#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/qa-test-lab/qa-test-lab-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
printf '<h1>Quality Assurance and Test Lab</h1>\n' > "$OUT"
echo "$OUT"
