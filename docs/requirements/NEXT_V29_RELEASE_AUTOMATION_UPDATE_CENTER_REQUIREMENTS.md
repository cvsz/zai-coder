# ZAI Coder Control Plane v29 — Release Automation and Update Center Requirements

## Added in v29

- Release planner.
- Version/channel policy.
- Changelog generator.
- Update manifest builder.
- Checksum verifier.
- Dry-run updater.
- Migration gate.
- Rollback gate.
- GitHub release draft generator.
- Release/update dashboard.
- Release audit log.
- Release scripts/routes/docs/tests.

## Safety

- Dry-run-first release and update flow.
- No GitHub API call or publish action.
- No branch push, force push, or broad git staging.
- Updates require backup, approval, checksum, and rollback plan.
- Update manifest write demo requires `APPLY=1`.
