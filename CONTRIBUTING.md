# Contributing

## Validate

```bash
python3 -m pytest -q
make repo-check
make secret-scan
make stage-manifest-check
```

## Safe Git rule

Stage exact paths only:

```bash
git add -- README.md docs/github/REPO_READY_CHECKLIST.md
```

Avoid broad staging, bypass flags, force pushes, secrets, generated files, and `apps/zlms/**`.
