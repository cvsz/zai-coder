# GitHub Repository Setup

This guide explains how to create and publish the ZAI Coder Control Plane repository using GitHub CLI and GPG-signed commits.

## Prerequisites

```bash
sudo apt update
sudo apt install -y git gh gnupg jq
gh auth login
gh auth status
gpg --version
```

## Recommended repository

```text
Owner: cvsz
Name: zai-coder-control-plane
Visibility: public or private
Default branch: main
Description: Local-first AI coding and creative automation control plane with safety dry-run and GPG release workflow.
Topics:
  ai
  coding-agent
  local-first
  ollama
  multi-agent
  automation
  creative-tools
  github-cli
  gpg
  python
```

## Dry-run repository creation

```bash
./scripts/github/gh-create-repo-safe.sh REPO_NAME=zai-coder-control-plane
```

## Real repository creation

```bash
APPLY=1 ./scripts/github/gh-create-repo-safe.sh \
  REPO_NAME=zai-coder-control-plane \
  VISIBILITY=public
```

## Initialize local Git repository

```bash
APPLY=1 ./scripts/github/gh-init-local-safe.sh
```

## Stage exact files

```bash
mkdir -p .release
cp docs/github/STAGE_MANIFEST.example.txt .release/STAGE_MANIFEST.txt
APPLY=1 ./scripts/github/gh-stage-manifest-safe.sh .release/STAGE_MANIFEST.txt
```

## Commit with GPG

```bash
APPLY=1 ./scripts/git/gpg-commit-safe.sh "chore: publish zai coder control plane"
```

## Push

```bash
APPLY=1 ./scripts/github/gh-push-safe.sh BRANCH=main
```

## Tag and release

```bash
APPLY=1 ./scripts/git/gpg-tag-safe.sh v0.1.0
APPLY=1 ./scripts/github/gh-release-safe.sh VERSION=v0.1.0
```
