#!/usr/bin/env bash
set -euo pipefail

PREFIX="${PREFIX:-${HOME}/.local/share/zai-coder}"
VENV_DIR="${VENV_DIR:-${HOME}/.venvs/zai-coder}"
APPLY="${APPLY:-0}"
BIN_DIR="${BIN_DIR:-${HOME}/.local/bin}"
LAUNCHER="${BIN_DIR}/zai-coder"

echo "== ZAI Coder Install Plan =="
echo "PREFIX: ${PREFIX}"
echo "VENV_DIR: ${VENV_DIR}"
echo "APPLY:  ${APPLY}"

if [[ "${APPLY}" != "1" ]]; then
  echo "DRY-RUN: Run 'APPLY=1 make install' to execute."
  exit 0
fi

mkdir -p "$(dirname "${VENV_DIR}")"
mkdir -p "${VENV_DIR}"

mkdir -p "${PREFIX}"
mkdir -p "${BIN_DIR}"

# RSync the rest if needed, but the VENV already has the package
rsync -a \
  --exclude='.git/' \
  --exclude='.env' \
  --exclude='.zai-coder/' \
  --exclude='__pycache__/' \
  --exclude='.pytest_cache/' \
  --exclude='*.pyc' \
  --exclude='*.db' \
  --exclude='*.sqlite' \
  --exclude='*.sqlite3' \
  --exclude='*.tgz' \
  --exclude='*.zip' \
  --exclude='*.sha256' \
  --exclude='venv/' \
  --exclude='.venv/' \
  ./ "${PREFIX}/"

# Keep the launcher self-contained and offline-friendly.
# It resolves the package from the copied prefix instead of relying on a live
# editable install or network access during setup.

mkdir -p \
  "${PREFIX}/.zai-coder/logs" \
  "${PREFIX}/.zai-coder/cache" \
  "${PREFIX}/.zai-coder/tmp" \
  "${PREFIX}/.zai-coder/checkpoints"

cat > "${LAUNCHER}" <<LAUNCHER_EOF
#!/usr/bin/env bash
set -euo pipefail

PREFIX="${PREFIX:-${HOME}/.local/share/zai-coder}"
PYTHONPATH="\${PREFIX}:\${PYTHONPATH:-}" exec python3 -m zai_coder "\$@"
LAUNCHER_EOF

chmod +x "${LAUNCHER}"

echo "Installation complete to ${PREFIX}"
echo "Launcher: ${LAUNCHER}"
echo "VENV: ${VENV_DIR}"
