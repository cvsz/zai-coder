#!/usr/bin/env bash
set -euo pipefail

PREFIX="${PREFIX:-${HOME}/.local/share/zai-coder}"
VENV_DIR="${VENV_DIR:-${HOME}/.venvs/zai-coder}"
LAUNCHER="${LAUNCHER:-${HOME}/.local/bin/zai-coder}"

echo "== Post-Install Check =="
echo "PREFIX: ${PREFIX}"
echo "VENV_DIR: ${VENV_DIR}"
echo "LAUNCHER: ${LAUNCHER}"

if [[ ! -d "${PREFIX}" ]]; then
  echo "Check: FAILED - install prefix missing"
  exit 1
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "Check: FAILED - venv directory missing"
  exit 1
fi

if [[ ! -x "${LAUNCHER}" ]]; then
  echo "Check: FAILED - launcher missing or not executable"
  exit 1
fi

# Check version
VERSION=$("${LAUNCHER}" --version 2>&1)
if [[ "${VERSION}" != *"0.1.3"* ]]; then
  echo "Check: FAILED - version mismatch (got: ${VERSION})"
  exit 1
fi

echo "Check: PASSED"
