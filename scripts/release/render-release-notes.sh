#!/usr/bin/env bash
set -euo pipefail
VERSION="${VERSION:-v0.12.0}"
OUT="${OUT:-docs/release/RELEASE_NOTES_v0.12.0.md}"
python3 - <<PY
from pathlib import Path
from zai_coder.github_ready_core.release_notes import render_release_notes
Path("${OUT}").write_text(render_release_notes("${VERSION}"), encoding="utf-8")
print("${OUT}")
PY
