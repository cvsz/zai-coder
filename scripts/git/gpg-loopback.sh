#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-status}"

case "$ACTION" in
  status)
    echo "gpg-agent config:"
    test -f ~/.gnupg/gpg-agent.conf && cat ~/.gnupg/gpg-agent.conf || true
    ;;
  enable)
    mkdir -p ~/.gnupg
    chmod 700 ~/.gnupg
    grep -q '^allow-loopback-pinentry' ~/.gnupg/gpg-agent.conf 2>/dev/null || echo allow-loopback-pinentry >> ~/.gnupg/gpg-agent.conf
    gpgconf --kill gpg-agent || true
    gpgconf --launch gpg-agent || true
    echo "DONE: loopback pinentry enabled."
    ;;
  *)
    echo "Usage: $0 [status|enable]" >&2
    exit 1
    ;;
esac
