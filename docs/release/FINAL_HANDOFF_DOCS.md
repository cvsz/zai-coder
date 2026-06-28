# Final Handoff Docs

## Overview
ZAI Coder is fully transitioned from a local-first operational framework into a comprehensive, enterprise-grade production-ready control plane.

## Release Features
- **Web UI & Control Views**: Located at `/zai`, rendering dynamic JSON schema components via OpenUI registry. Module controls exist for operations, governance, compliance, provider routing, marketplace, and go-live pipelines.
- **Production Gateways & Deployment**: Cloudflare preflight checks verify DNS and Zero Trust Access. The gateway imposes TLS requirements, rate limiting, request-size bounds, and upstream failover.
- **Durable Operations**: SQLite stores for operational snapshots (health, KPIs, SLI/SLO dashboards, and audit).
- **Safety First**: External mutative actions (pushing, publishing, paid API tasks) are gated behind manual action requirements. No credentials or generated artifacts leak into source packages.

## Future Operator Guidance
1. **Starting the Runtime**: Use `docker-compose -f docker-compose.prod.yml up -d` for the complete stack, ensuring `TLS_TERMINATION` and `UPSTREAM_HEALTH_FAILOVER` environment boundaries are maintained.
2. **Web Migration**: Over time, you may transition legacy web features from standard layouts into OpenUI native components. Ensure components conform to `web/src/lib/zai/openui.ts` registry.
3. **External Actions Approval**: If external mutative actions become automated, you must update `zai_coder/github_ready_core/external_action.py` with proper role-based authorizations and audit paths.
