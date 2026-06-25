# ZAI Coder Control Plane v39 — Notification and Communication Center Requirements

## Added in v39

- Notification channel policy registry.
- Notification template registry.
- Customer preference center.
- Safe local draft renderer.
- Delivery gate.
- Portal inbox draft store.
- Digest/schedule planner.
- Communication thread builder.
- Notification export/report bundle.
- Notification dashboard.
- Notification audit log.
- Notification-center scripts/routes/docs/tests.

## Safety

- Local-first and draft-only.
- No real email, SMS, Slack, webhook, or external send.
- External channels are disabled and draft-only.
- Portal and in-app channels are local only.
- Demo writes require `APPLY=1`.
- Sensitive terms are blocked in templates and drafts.
