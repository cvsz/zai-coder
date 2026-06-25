#!/usr/bin/env bash
set -euo pipefail
PREFIX="${PREFIX:-${HOME}/.local/share/zai-coder}"
APPLY="${APPLY:-0}"

echo "== ZAI Coder Install Plan =="
echo "PREFIX: $PREFIX"
echo "APPLY:  $APPLY"

if [ "$APPLY" != "1" ]; then
    echo "DRY-RUN: Run 'APPLY=1 make install' to execute."
    exit 0
fi

mkdir -p "$PREFIX"
mkdir -p "$HOME/.local/bin"

# Sync files, excluding sensitive/unnecessary ones
rsync -av --exclude='.git/' --exclude='.env' --exclude='__pycache__/' \
      --exclude='.pytest_cache/' --exclude='*.pyc' --exclude='*.db' \
      --exclude='*.sqlite*' --exclude='*.tgz' --exclude='*.zip' \
      --exclude='*.sha256' --exclude='FINAL_RELEASE_*' \
      . "$PREFIX/"

# Create runtime dirs
mkdir -p "$PREFIX/.zai-coder/logs" "$PREFIX/.zai-coder/cache" \
         "$PREFIX/.zai-coder/tmp" "$PREFIX/.zai-coder/checkpoints"

# Create launcher
cat <<EOF > "$HOME/.local/bin/zai-coder"
#!/usr/bin/env bash
cd "$PREFIX" && ./run.sh "\$@"
EOF
chmod +x "$HOME/.local/bin/zai-coder"

echo "Installation complete to $PREFIX"
EOF
