#!/usr/bin/env bash
set -euo pipefail

echo "== GPG Doctor =="
command -v gpg >/dev/null 2>&1 || { echo "ERROR: gpg not found"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "ERROR: git not found"; exit 1; }

echo "gpg: $(gpg --version | head -1)"
echo "git: $(git --version)"
echo "GPG_TTY=${GPG_TTY:-}"

echo
echo "== Git signing config =="
git config --get user.name || true
git config --get user.email || true
git config --get user.signingkey || true
git config --get commit.gpgsign || true
git config --get tag.gpgsign || true
git config --get gpg.program || true

echo
echo "== Secret keys =="
gpg --list-secret-keys --keyid-format=long || true
