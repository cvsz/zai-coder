# ZAI Coder v0.1.2 Release Notes

## Release Properties
- **Release type**: Patch Release
- **Previous release**: v0.1.1 at `6f844d9`
- **Baseline before release PR**: main at `69adbfb`

## Summary of Changes
1. **Pytest Warning Cleanup**: Addressed all active collection and execution warnings in test suites, establishing a clean, 0-warning pytest execution baseline.
2. **Package-Check Hardening**: Rewrote `package-check.sh` to extract the package version authoritatively from `pyproject.toml` using `tomllib`, verifying that all versioned archives (`.tar.gz`, `.zip`, and `.sha256` checksum wrappers) are generated correctly.
3. **Strict Checksum & Manifest Auditing**: Integrated `sha256sum -c` checksum validation on both release archives. RELEASE_MANIFEST.json is parsed and validated as strict JSON, ensuring it accurately references the current version and artifacts list.
4. **Internal Core Coverage Expansion**: Expanded testing footprints across `server.py`, `migrations.py`, `update_system/manager.py`, and `repo_policy.py`. All tests use deterministic filesystem virtualization (e.g. `tmp_path`) with no real socket binding, home directory writes, or network requests.
5. **Private API Encapsulation**: Server, migration, policy, and updater internals remain strictly encapsulated; no public API stability claims are asserted in this cycle.

## Upgrade & Installation Guidance
- Pull the latest `main` branch after release.
- Re-run `make install APPLY=1` to update the local deployment path.
- Local runtime cache databases (`data/*.db`, `.pytest_cache/`) should not be copied across development environments.
