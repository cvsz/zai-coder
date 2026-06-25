#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/.."
zip -r zai-coder-standalone.zip zai-coder-standalone -x "*/__pycache__/*" "*.pyc" "*/.pytest_cache/*"
echo "created zai-coder-standalone.zip"
