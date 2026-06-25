#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.deployment_core.checksums import write_checksum_manifest
print(write_checksum_manifest("release", "release/SHA256SUMS.json"))
PY
