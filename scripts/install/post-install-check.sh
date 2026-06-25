#!/usr/bin/env bash
set -euo pipefail
PREFIX="${PREFIX:-${HOME}/.local/share/zai-coder}"

echo "== Post-Install Check =="
if [ -d "$PREFIX" ] && [ -x "$HOME/.local/bin/zai-coder" ]; then
    echo "Check: PASSED"
else
    echo "Check: FAILED"
    exit 1
fi
EOF
