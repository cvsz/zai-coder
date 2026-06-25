# Runbook: self-package

Build a release ZIP after tests and safety checks.

## Commands

```bash
make package APPLY=1
```
```bash
./scripts/package.sh zai-coder-release
```

## Outputs

- release zip

## Safety

- test before package
- no secrets
