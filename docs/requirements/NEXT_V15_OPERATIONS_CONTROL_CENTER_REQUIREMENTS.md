# ZAI Coder Control Plane v15 — Operations Control Center Requirements

## Added in v15

- Operations Control Center UI shell.
- Service status panel.
- Health dashboard.
- Safe log viewer.
- Backup dashboard.
- Restore plan route.
- Upgrade dashboard.
- Rollback plan route.
- Restart/status action plans.
- Server route integration.
- Operations scripts.
- Operations docs/runbooks.
- Tests.

## Safety

- Dashboards generate read-only plans by default.
- Mutating operations require explicit `APPLY=1` through existing scripts.
- Log viewer only allows safe relative `logs/` or `data/` paths.
- Backup is recommended before upgrade/rollback/restore.
- Public exposure still requires Cloudflare Access.
