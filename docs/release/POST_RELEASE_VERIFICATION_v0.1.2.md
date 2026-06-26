# ZAI Coder v0.1.2 Post-Release Verification Record

## Release Metadata
- **Version**: `v0.1.2`
- **Release URL**: https://github.com/cvsz/zai-coder/releases/tag/v0.1.2
- **PR #11 URL**: https://github.com/cvsz/zai-coder/pull/11
- **Merge Commit**: `3c6445d`
- **Tag Target Commit**: `3c6445d` (main HEAD post-PR #11 merge)

## Immutable Tag Signatures
- **v0.1.0 tag SHA**: `b6b09e3`
- **v0.1.1 tag SHA**: `6f844d9`
- **v0.1.2 tag SHA**: `ebd048d6a37c5c271659eb19c809f801bab00502` (pointing to `3c6445d`)
- **GPG Tag Verification**: Successfully verified GPG signature matching CVSz.

## Verification Evidence
- **Validation Suite**: `456 passed, 0 warnings` (fully warning-free). All compile, safety check, secret scanning, and stage checks passed.
- **Package-Check Verification**: Successful. Matches version `0.1.2` extracted authoritatively from `pyproject.toml`.
- **Checksum Validation**: Verified via `sha256sum -c`. Both `.tar.gz` and `.zip` checksums match exactly.
- **Manifest Verification**: RELEASE_MANIFEST.json validated as strict JSON, referencing version `0.1.2` and archives list.

## Uploaded Assets
- `RELEASE_MANIFEST.json`
- `zai-coder-standalone-0.1.2.tar.gz`
- `zai-coder-standalone-0.1.2.tar.gz.sha256`
- `zai-coder-standalone-0.1.2.zip`
- `zai-coder-standalone-0.1.2.zip.sha256`

## Exclusion Audit
- Verified that packaging directories (`dist/`), compiler caches (`__pycache__/`, `.pytest_cache/`), and local database caches (`data/*.db`) are correctly excluded and not tracked.

## Final Release Verdict
**PASSED**: All gates harden release verification perfectly.

## Next Steps
- Switch to branch `chore/plan-v0.1.3` to plan the next release cycle.
