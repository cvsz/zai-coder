#!/usr/bin/env bash
set -euo pipefail

PREFIX="${PREFIX:-${HOME}/.local/share/zai-coder}"
LAUNCHER="${LAUNCHER:-${HOME}/.local/bin/zai-coder}"

echo "== Post-Install Check =="
echo "PREFIX: ${PREFIX}"
echo "LAUNCHER: ${LAUNCHER}"

if [[ ! -d "${PREFIX}" ]]; then
  echo "Check: FAILED - install prefix missing"
  exit 1
fi

if [[ ! -x "${LAUNCHER}" ]]; then
  echo "Check: FAILED - launcher missing or not executable"
  exit 1
fi

if [[ ! -d "${PREFIX}/zai_coder" ]]; then
  echo "Check: FAILED - Python package directory missing"
  exit 1
fi

echo "Check: PASSED"
