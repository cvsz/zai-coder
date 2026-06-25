# Release Process

```bash
python3 -m pytest -q
make github-ready
make repo-check
make secret-scan
make stage-manifest-check
make verify-source-package
make release-plan
make release-build APPLY=1 NAME=zai-coder-control-plane-v0.12.0
make release-checksums
make release-sbom
```
