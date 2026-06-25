# Runbook — GPG Signed Release

## Preflight

```bash
export GPG_TTY="$(tty)"
gpg --list-secret-keys --keyid-format=long
git config --get user.signingkey
```

## Commit

```bash
APPLY=1 ./scripts/git/gpg-commit-safe.sh "release: v0.1.0"
```

## Tag

```bash
APPLY=1 ./scripts/git/gpg-tag-safe.sh v0.1.0
```

## Verify

```bash
git log --show-signature -1
git tag -v v0.1.0
```
