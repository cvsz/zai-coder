# Generated State Guardrails

## Purpose
This document defines the guardrails for runtime-generated files (DBs, evidence, exports) to prevent drift and accidental commits.

## Classification
UNTRACK_GENERATED_RUNTIME_STATE:
- data/enterprise-admin-console.db
- data/provider-audit.db
- evidence/governance/evidence-bundle.json
- identity/evidence/identity-evidence.json
- marketplace/exports/marketplace-export.json
- migration/exports/migration-evidence.json
- security/evidence/security-ops-evidence.json

## Policy
- These files are classified as runtime outputs. They should not be tracked by git.
- If a file is required for testing, it must be promoted to a fixture path (e.g., `tests/fixtures/`) with explicit documentation.
- Future generated build reports or runtime state must not be committed at the repository root.

## Validation
- `make repo-check`
- `scripts/repo/check-generated-state.sh`
- `python3 -m pytest tests/test_generated_state_guardrails.py -q`
