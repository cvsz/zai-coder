# Source Package Verification

```bash
python3 -m pytest -q
make repo-check
make secret-scan
make stage-manifest-check
make release-checksums
make release-sbom
```
