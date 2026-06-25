# GitHub Release Process

## Release checklist

1. Run tests.
2. Run safety scan.
3. Confirm no secrets.
4. Confirm stage manifest.
5. Create signed commit.
6. Push branch.
7. Create signed tag.
8. Create GitHub release.
9. Attach ZIP artifact if needed.

## Commands

```bash
python3 -m pytest -q
make scan
make gpg-doctor

mkdir -p .release
cp docs/github/STAGE_MANIFEST.example.txt .release/STAGE_MANIFEST.txt
APPLY=1 make github-stage-manifest
APPLY=1 make gpg-commit MESSAGE="release: v0.1.0"
APPLY=1 make github-push BRANCH=main
APPLY=1 make gpg-tag VERSION=v0.1.0
APPLY=1 make github-release VERSION=v0.1.0
```

## Never do this

```bash
git add .
git add -A
git commit --no-verify
git push --force
```
