#!/usr/bin/env bash
set -euo pipefail

PREFIX="${PREFIX:-${HOME}/.local/share/zai-coder}"
APPLY="${APPLY:-0}"
BIN_DIR="${BIN_DIR:-${HOME}/.local/bin}"
LAUNCHER="${BIN_DIR}/zai-coder"

echo "== ZAI Coder Install Plan =="
echo "PREFIX: ${PREFIX}"
echo "APPLY:  ${APPLY}"

if [[ "${APPLY}" != "1" ]]; then
  echo "DRY-RUN: Run 'APPLY=1 make install' to execute."
  exit 0
fi

mkdir -p "${PREFIX}"
mkdir -p "${BIN_DIR}"

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
  ./ "${PREFIX}/"

mkdir -p \
  "${PREFIX}/.zai-coder/logs" \
  "${PREFIX}/.zai-coder/cache" \
  "${PREFIX}/.zai-coder/tmp" \
  "${PREFIX}/.zai-coder/checkpoints"

chmod +x "${PREFIX}/run.sh" 2>/dev/null || true
chmod +x "${PREFIX}/zai-coder" 2>/dev/null || true

cat > "${LAUNCHER}" <<LAUNCHER_EOF
#!/usr/bin/env bash
set -euo pipefail

PREFIX="\${ZAI_CODER_HOME:-${PREFIX}}"
cd "\${PREFIX}"

if python3 -m zai_coder --help >/dev/null 2>&1; then
  exec python3 -m zai_coder "\$@"
fi

if [[ -f "zai-coder/main.py" ]]; then
  exec python3 zai-coder/main.py "\$@"
fi

if [[ -x "./run.sh" ]]; then
  exec ./run.sh "\$@"
fi

echo "ERROR: Cannot find ZAI Coder entrypoint in \${PREFIX}" >&2
exit 1
LAUNCHER_EOF

chmod +x "${LAUNCHER}"

echo "Installation complete to ${PREFIX}"
echo "Launcher: ${LAUNCHER}"
