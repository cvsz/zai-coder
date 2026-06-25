# GPG Signing Guide

## Goal

Use GPG-signed commits and tags for ZAI Coder releases.

## Check GPG

```bash
gpg --version
gpg --list-secret-keys --keyid-format=long
```

## Set Git signing key

```bash
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global gpg.program gpg
```

## Export public key

```bash
gpg --armor --export YOUR_KEY_ID
```

Add the public key to GitHub:

```text
GitHub Settings -> SSH and GPG keys -> New GPG key
```

## Fix terminal signing

```bash
export GPG_TTY="$(tty)"
echo 'export GPG_TTY="$(tty)"' >> ~/.bashrc
```

## Signed commit

```bash
git commit -S -m "message"
```

## Signed tag

```bash
git tag -s v0.1.0 -m "v0.1.0"
```

## Verify

```bash
git log --show-signature -1
git tag -v v0.1.0
```
