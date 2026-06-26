#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
python3 - <<PY
from zai_coder.app_studio_final.project_archive import export_project_archive
print(export_project_archive(".", "release/zai-project-archive.zip", {"name":"zai-coder"}, apply="${APPLY}"=="1"))
PY
