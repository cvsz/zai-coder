# Release Branch Checklist Template

## Release
- Version:
- Target branch:
- Main baseline:
- Release candidate PR:
- Publish branch:
- Tag:
- GitHub release URL:

## Pre-release Candidate
- [ ] main synced
- [ ] working tree clean
- [ ] version before bump verified
- [ ] version bump committed on release branch only
- [ ] release notes finalized
- [ ] release candidate docs updated
- [ ] package candidate generated locally
- [ ] package-check passed
- [ ] no tag created
- [ ] no release published
- [ ] no assets uploaded

## Publish Phase
- [ ] release candidate PR merged
- [ ] main synced
- [ ] version verified on main
- [ ] CI workflow dependency setup verified
- [ ] full validation passed
- [ ] package artifacts generated
- [ ] checksums verified
- [ ] signed tag created
- [ ] tag pushed
- [ ] GitHub release created
- [ ] assets uploaded

## Post-release
- [ ] release viewed via gh
- [ ] all assets attached
- [ ] tag GPG verification passed
- [ ] full post-release validation passed
- [ ] post-release verification doc created
- [ ] post-release verification PR opened
- [ ] cleanup branches deleted if safe

## Stop Conditions
- [ ] unexpected tag exists
- [ ] version mismatch
- [ ] failing tests
- [ ] failing package-check
- [ ] generated files tracked
- [ ] CI dependency setup missing
- [ ] release assets missing or mismatched
