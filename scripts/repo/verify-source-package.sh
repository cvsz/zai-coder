#!/usr/bin/env bash
set -euo pipefail
python3 -m pytest -q
scripts/repo/repo-check.sh
scripts/repo/secret-scan-safe.sh
scripts/repo/stage-manifest-check.sh
echo "OK: source package verified"
