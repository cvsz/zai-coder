# GPG Loopback Guide

Loopback mode can help in CLI/automation contexts, but it must not store passphrases in the repository.

## Enable loopback in gpg-agent

```bash
mkdir -p ~/.gnupg
chmod 700 ~/.gnupg
grep -q '^allow-loopback-pinentry' ~/.gnupg/gpg-agent.conf 2>/dev/null || echo allow-loopback-pinentry >> ~/.gnupg/gpg-agent.conf
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

## Use helper

```bash
./scripts/git/gpg-loopback.sh status
```

## Safety

- Do not commit passphrases.
- Do not write private keys into repo.
- Do not paste secret material into config.
- Prefer interactive pinentry when possible.
