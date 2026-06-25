# ZAI Coder Control Plane v49 — Production Readiness and Go Live Command Center Requirements

## Added in v49

- Production readiness dashboard.
- Readiness gate registry.
- Go-live checklist.
- Launch command center.
- Manual approval gates.
- Rollback plan catalog.
- Launch evidence bundle.
- Release readiness scorecard.
- Go-live dashboard routes.
- Go-live scripts/routes/docs/tests.

## Safety

- Manual approval gates required.
- No automatic production launch.
- No production config mutation by default.
- Rollback plans are review-first.
- Demo/export writes require `APPLY=1`.
