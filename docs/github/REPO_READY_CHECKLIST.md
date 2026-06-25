# GitHub Ready Checklist

## Validate

```bash
python3 -m pytest -q
make github-ready
make repo-check
make secret-scan
make stage-manifest-check
make verify-source-package
```

## Create repo

```bash
make github-create-repo REPO_NAME=zai-coder-control-plane VISIBILITY=public
make github-create-repo APPLY=1 REPO_NAME=zai-coder-control-plane VISIBILITY=public
```

## Stage exact files only

```bash
make github-stage-manifest
make github-stage-manifest APPLY=1
```

## Commit, push, tag, release

```bash
make gpg-commit APPLY=1 MESSAGE="chore: publish ZAI Coder Control Plane"
make github-push APPLY=1 BRANCH=main
make gpg-tag APPLY=1 VERSION=v0.12.0
make github-release APPLY=1 VERSION=v0.12.0
```
