# RELEASE NOTES: ZAI Coder v0.1.3

## Overview
This patch release (`v0.1.3`) focuses on operational hardening, developer experience improvements, and robust release automation.

## Key Improvements
- **CLI UX**: Consistent help and error diagnostics for all subcommands.
- **Safety**: Expanded regression coverage for `SafeRunner` and `SafetyPolicy`.
- **Diagnostics**: Hardened local installer and uninstaller diagnostic paths.
- **Release Automation**: Robust dry-run mechanisms in the packaging process.
- **Compliance**: Verified strict exclusion of generated files/artifacts in tracked repositories.

## Changes
- Add unit tests for CLI help consistency.
- Regress path patterns and dangerous command blocking in safety policies.
- Verify safe dry-run behaviors for installers and uninstaller scripts.
- Validate checksums and manifest metadata in package automation.

## Important Note
This release does not include any changes to the core public-facing APIs. Users should verify existing setups using the new `doctor` and diagnostic tools.
