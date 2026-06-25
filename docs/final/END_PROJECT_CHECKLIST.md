# End Project Checklist

## Validate

```bash
python3 -m pytest -q
make final-status
make final-ui-demo
make app-generator-demo
make workflow-demo
make project-archive-plan
make openapi-full-export
```

## Publish

```bash
make scan
make gpg-doctor
make release-plan
make release-build APPLY=1
make release-checksums
make release-sbom
```

## GitHub

```bash
make github-plan
make github-create-repo REPO_NAME=zai-coder-control-plane
make github-create-repo APPLY=1 REPO_NAME=zai-coder-control-plane VISIBILITY=public
```

## Do not do

```text
git add .
git add -A
--no-verify
force push
commit secrets
commit apps/zlms/**
```
