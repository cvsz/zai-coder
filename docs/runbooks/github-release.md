# Runbook — GitHub Release

## Preflight

```bash
gh auth status
make gpg-doctor
python3 -m pytest -q
make scan
```

## Create repo

```bash
make github-create-repo REPO_NAME=zai-coder-control-plane
make github-create-repo APPLY=1 REPO_NAME=zai-coder-control-plane VISIBILITY=public
```

## Publish

```bash
make github-init-local APPLY=1
cp docs/github/STAGE_MANIFEST.example.txt .release/STAGE_MANIFEST.txt
make github-stage-manifest APPLY=1
make gpg-commit APPLY=1 MESSAGE="chore: publish initial release"
make github-push APPLY=1 BRANCH=main
```

## Release

```bash
make gpg-tag APPLY=1 VERSION=v0.1.0
make github-release APPLY=1 VERSION=v0.1.0
```
