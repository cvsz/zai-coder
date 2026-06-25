# ZAI Coder Control Plane v30 — Self-Healing Operations Requirements

## Added in v30

- Health signal monitor.
- Incident detector.
- Remediation playbooks.
- Safe auto-heal planner.
- Rollback guard.
- Maintenance window policy.
- Escalation policy.
- Postmortem generator.
- Self-healing dashboard.
- Healing audit log.
- Self-healing scripts/routes/docs/tests.

## Safety

- No automatic destructive remediation.
- Healing plans are dry-run-first.
- High-risk remediation requires approval.
- Outside maintenance window requires approval.
- Rollback plan, backup, and smoke tests are required.
- Demo file writes require `APPLY=1`.
