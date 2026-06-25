#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/disaster-recovery/disaster-recovery-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
printf '<h1>Backup Restore and Disaster Recovery</h1>\n' > "$OUT"
echo "$OUT"
