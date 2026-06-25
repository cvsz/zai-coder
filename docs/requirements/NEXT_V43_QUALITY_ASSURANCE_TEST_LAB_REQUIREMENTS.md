# ZAI Coder Control Plane v43 — Quality Assurance and Test Lab Requirements

## Added in v43

- QA dashboard.
- Release test matrix.
- Regression report generator.
- Fixture catalog.
- Smoke test planner.
- Quality gate policy.
- Validation evidence exporter.
- QA dashboard routes.
- QA test lab scripts/routes/docs/tests.

## Safety

- Deterministic tests.
- No disabled checks or bypass flags.
- Evidence export is local-only.
- Quality gates are dry-run evaluation by default.
- Demo/export writes require `APPLY=1`.
