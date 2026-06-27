# ZAI Coder Roadmap

Last updated: 2026-06-27

This is the canonical tracked roadmap for the ZAI Coder Control Plane. It is evidence-backed by the current repository tree and separates local release readiness from external, always-on production service readiness.

Target state: Master Advanced Professional Enterprise-grade Final Release Complete, production-ready for local-first AI coding, automation, operations, and OpenUI-backed control-plane workflows.

## Scan Baseline

Repository scan evidence from the current working tree:

| Surface | Count | Evidence |
| --- | ---: | --- |
| Feature-pack metadata files | 46 | `assets/**/*features.json` |
| Python package module directories | 67 | `zai_coder/*` |
| Python test files | 136 | `tests/test_*.py` |
| Markdown docs | 429 | `docs/**/*.md` |
| Script files | 437 | `scripts/**/*` |
| Web files | 4946 | `web/**/*` |
| Local AI skill files | 2 | `skills/*/SKILL.md` |
| Codex role configs | 3 | `.codex/agents/*.toml` |

The scan confirms a broad local-first enterprise control plane with feature metadata, module code, docs, scripts, and tests across v3-v50 feature packs. It also confirms that `web/` is now a first-party Open WebUI-based surface with a narrow ZAI command center at `/zai`, while external go-live remains blocked by runtime, gateway, auth, persistence, and web CI gates.

## Current Release State

The repository is in a v50 final enterprise release-candidate state for local-first packaging and control-plane workflows.

Verified as local release-ready:

- Source package gates: `compileall`, full `pytest`, `repo-check`, `secret-scan`, `stage-manifest-check`, `final-release-status`, source-package verification, checksum generation, and SBOM generation.
- Local-first execution model: dry-run-first command routing, provider-operation planning, safety checks, and approval-gated apply paths.
- Release/security guardrails: tracked-source secret scanning, exact-path stage manifest validation, forbidden-command checks, and local-only release artifact generation.
- Enterprise modules: governance, compliance center, SSO identity, reporting board pack, observability, execution runner, provider adapters, tenant controls, connector hub, disaster recovery, go-live command center, and final release pack foundations.
- Evaluation coverage now uses real local execution paths for planner contracts, command safety, and retrieval checks instead of echo-only simulation.
- Web surface ownership now has an explicit smoke gate: `make web-check`.
- `/web` includes a first-party ZAI Command Center at `/zai`, backed by `web/src/lib/zai/migration-manifest.json`, `web/src/lib/zai/openui.ts`, and `web/src/lib/components/zai/OpenUIRenderer.svelte`.
- `make web-migration-report` generates a strict repository inventory from the same manifest used by the UI and fails on web hygiene drift.

Not yet externally production-ready:

- `web/src/lib/zai/migration-manifest.json` reports `externalGoLiveReady: false` and `coveragePercent: 64`.
- Production server dependencies are optional in the base package and isolated in `requirements-production.txt`.
- The public gateway, auth/session lifecycle, durable operational persistence, and web CI pipeline still need integrated release gates.

## Milestones

- [x] **Local-first release gate** - Preserve the no-mandatory-third-party runtime, dry-run-first execution, exact-path staging, and local release artifact checks.
- [x] **Enterprise feature-pack foundation** - Keep v3-v50 feature packs discoverable through metadata, module code, tests, docs, and scripts.
- [x] **Open WebUI ownership decision** - Treat `web/` as an owned first-party surface with ZAI migration manifest, smoke gate, and `/zai` command center.
- [ ] **v51 Production Runtime Gate** - Validate production dependencies, ASGI import, health/readiness probes, auth/session routes, gateway envelope behavior, and package version mapping.
- [ ] **v52 Durable Operations Gate** - Add durable stores and retention policy for KPI snapshots, health trends, compliance evidence, provider audit streams, and operational history.
- [ ] **v53 External Deployment Gate** - Add public gateway profile, Cloudflare Access/DNS preflight, container/runtime smoke tests, rollback gates, and explicit external-action approval workflow.
- [ ] **v54 Web Product Gate** - Promote full web install/lint/typecheck/test/build/accessibility/SBOM/license/secret gates into CI and expand `/zai` into first-party module views.
- [ ] **v55 GA Release Gate** - Produce signed release metadata, semver mapping, final handoff docs, and a clean production readiness report with no known external go-live blockers.

## Completed

| Milestone | Date | Evidence |
| --- | --- | --- |
| Local-first release gate | 2026-06-27 | `Makefile`, `scripts/repo/*`, `scripts/release/*`, `FINAL_RELEASE_*` |
| Enterprise feature-pack foundation | 2026-06-27 | `assets/**/*features.json`, `zai_coder/*`, `tests/test_*_v*.py`, `docs/archive/build-reports/*` |
| Open WebUI ownership decision | 2026-06-27 | `web/src/lib/zai/migration-manifest.json`, `tests/test_web_surface.py`, `scripts/repo/web-migration-report.py` |

## Feature File Inventory

This table lists every scanned feature-pack metadata file and the primary implementation evidence. `Legacy/foundation` means the feature is represented by metadata, tests, docs, scripts, or shared core modules rather than a same-named `zai_coder/<feature>` package.

| Feature pack | Metadata file | Primary code evidence | Test evidence | Docs/scripts evidence |
| --- | --- | --- | --- | --- |
| Enterprise Admin Console | `assets/admin-console/enterprise_admin_console_features.json` | `zai_coder/enterprise_admin_console` | `tests/test_enterprise_admin_console_v33.py` | `docs/admin-console/*`, `scripts/admin-console/*` |
| Agent Runtime Supervisor | `assets/agents/agent_runtime_supervisor_features.json` | `zai_coder/agent_runtime_supervisor` | `tests/test_agent_runtime_supervisor_v26.py` | `docs/agents/*`, `scripts/agents/*` |
| App Studio | `assets/app_studio_features.json` | `zai_coder/app_studio` | `tests/test_app_studio_v8.py`, `tests/test_app_studio_final_v12.py` | `docs/runbooks/app-studio.md` |
| App Studio Final | `assets/app_studio_final_features.json` | `zai_coder/app_studio_final` | `tests/test_app_studio_final_v12.py` | `scripts/final/*` |
| Billing Usage Enforcement | `assets/billing/billing_usage_enforcement_features.json` | `zai_coder/billing_usage_enforcement` | `tests/test_billing_usage_enforcement_v22.py` | `docs/billing/*`, `scripts/billing/*` |
| Enterprise Reporting Board Pack | `assets/board-pack/enterprise_reporting_board_pack_features.json` | `zai_coder/enterprise_reporting_board_pack` | `tests/test_enterprise_reporting_board_pack_v32.py` | `docs/board-pack/*`, `scripts/board-pack/*` |
| Cloudflare Go Live | `assets/cloudflare/cloudflare_go_live_features.json` | `zai_coder/cloudflare_go_live` | `tests/test_cloudflare_go_live_v16.py` | `docs/cloudflare/*`, `scripts/cloudflare/*` |
| Enterprise Compliance Center | `assets/compliance-center/enterprise_compliance_center_features.json` | `zai_coder/enterprise_compliance_center` | `tests/test_enterprise_compliance_center_v31.py` | `docs/compliance-center/*`, `scripts/compliance-center/*` |
| Plugin Connector Hub | `assets/connectors/plugin_connector_hub_features.json` | `zai_coder/plugin_connector_hub` | `tests/test_plugin_connector_hub_v28.py` | `docs/connectors/*`, `scripts/connectors/*` |
| Template Content Studio | `assets/content-studio/template_content_studio_features.json` | `zai_coder/template_content_studio` | `tests/test_template_content_studio_v38.py` | `docs/content-studio/*`, `scripts/content-studio/*` |
| Creative Automation | `assets/creative_automation_features.json` | `zai_coder/creative_automation` | `tests/test_creative_automation_v5.py` | `docs/runbooks/creative-automation.md` |
| Creative Core | `assets/creative_core_features.json` | Legacy/foundation | `tests/test_creative_core.py` | `docs/requirements/NEXT_CREATIVE_CORE_REQUIREMENTS.md` |
| Customer Portal Onboarding | `assets/customer-portal/customer_portal_onboarding_features.json` | `zai_coder/customer_portal_onboarding` | `tests/test_customer_portal_onboarding_v34.py` | `docs/customer-portal/*`, `scripts/customer-portal/*` |
| Deployment Core | `assets/deployment_core_features.json` | `zai_coder/deployment_core` | `tests/test_deployment_core_v9.py` | `docs/deploy/*`, `scripts/deploy/*` |
| Developer Portal API Docs | `assets/developer-portal/developer_portal_api_docs_features.json` | `zai_coder/developer_portal_api_docs` | `tests/test_developer_portal_api_docs_v41.py` | `docs/developer-portal/*`, `scripts/developer-portal/*` |
| Backup Restore Disaster Recovery | `assets/disaster-recovery/backup_restore_disaster_recovery_features.json` | `zai_coder/backup_restore_disaster_recovery` | `tests/test_backup_restore_disaster_recovery_v45.py` | `docs/disaster-recovery/*`, `scripts/disaster-recovery/*` |
| Execution Runner | `assets/execution/execution_runner_features.json` | `zai_coder/execution_runner` | `tests/test_execution_runner_v18.py` | `docs/execution/*`, `scripts/execution/*` |
| Feedback Roadmap Center | `assets/feedback-roadmap/feedback_roadmap_center_features.json` | `zai_coder/feedback_roadmap_center` | `tests/test_feedback_roadmap_center_v36.py` | `docs/feedback-roadmap/*`, `scripts/feedback-roadmap/*` |
| Final Enterprise Release Pack | `assets/final-release/final_enterprise_release_pack_features.json` | `zai_coder/final_enterprise_release_pack` | `tests/test_final_enterprise_release_pack.py`, `tests/test_final_enterprise_release_pack_v50.py` | `docs/final-release/*`, `scripts/final-release/*` |
| Production API Gateway | `assets/gateway/production_api_gateway_features.json` | `zai_coder/production_api_gateway` | `tests/test_production_api_gateway_v24.py` | `docs/gateway/*`, `scripts/gateway/*` |
| Production Readiness Go Live | `assets/go-live-command-center/production_readiness_go_live_features.json` | `zai_coder/production_readiness_go_live_command_center` | `tests/test_production_readiness_go_live_command_center_v49.py` | `docs/go-live-command-center/*`, `scripts/go-live-command-center/*` |
| Enterprise Governance | `assets/governance/enterprise_governance_features.json` | `zai_coder/enterprise_governance` | `tests/test_enterprise_governance_v20.py` | `docs/governance/*`, `scripts/governance/*` |
| Growth Core | `assets/growth_core_features.json` | Legacy/foundation | `tests/test_growth_core.py` | `docs/requirements/NEXT_GROWTH_CORE_REQUIREMENTS.md` |
| Knowledge Base Help Center | `assets/help-center/knowledge_base_help_center_features.json` | `zai_coder/knowledge_base_help_center` | `tests/test_knowledge_base_help_center_v37.py` | `docs/help-center/*`, `scripts/help-center/*` |
| Enterprise SSO Identity Center | `assets/identity-center/enterprise_sso_identity_center_features.json` | `zai_coder/enterprise_sso_identity_center` | `tests/test_enterprise_sso_identity_center_v47.py` | `docs/identity-center/*`, `scripts/identity-center/*` |
| Integration Core | `assets/integration_core_features.json` | `zai_coder/integration_core` | `tests/test_integration_core_v10.py` | `docs/runbooks/integration-core.md`, `scripts/integration/*` |
| Agent Marketplace And Skills | `assets/marketplace/agent_marketplace_and_skills_features.json` | `zai_coder/agent_marketplace_and_skills` | `tests/test_agent_marketplace_and_skills_v27.py` | `docs/marketplace/*`, `scripts/marketplace/*` |
| Data Import Export Migration Center | `assets/migration-center/data_import_export_migration_center_features.json` | `zai_coder/data_import_export_migration_center` | `tests/test_data_import_export_migration_center_v44.py` | `docs/migration-center/*`, `scripts/migration-center/*` |
| Monetization Core | `assets/monetization_core_features.json` | `zai_coder/monetization_core` | `tests/test_monetization_core_v7.py` | `docs/runbooks/monetization-core.md` |
| Notification Communication Center | `assets/notification-center/notification_communication_center_features.json` | `zai_coder/notification_communication_center` | `tests/test_notification_communication_center_v39.py` | `docs/notification-center/*`, `scripts/notification-center/*` |
| Observability Suite | `assets/observability/observability_suite_features.json` | `zai_coder/observability_suite` | `tests/test_observability_suite_v19.py` | `docs/observability/*`, `scripts/observability/*` |
| Operations Control Center | `assets/ops-center/ops_control_center_features.json` | `zai_coder/operations_control_center` | `tests/test_operations_control_center_v15.py` | `docs/operations/*`, `scripts/ops-center/*` |
| Package Registry Marketplace | `assets/package-registry/package_registry_marketplace_features.json` | `zai_coder/package_registry_marketplace_publishing` | `tests/test_package_registry_marketplace_publishing_v42.py` | `docs/package-registry/*`, `scripts/package-registry/*` |
| Payment Provider Sandbox | `assets/payments/payment_provider_sandbox_features.json` | `zai_coder/payment_provider_sandbox` | `tests/test_payment_provider_sandbox_v23.py` | `docs/payments/*`, `scripts/payments/*` |
| Production SaaS Core | `assets/production_saas_core_features.json` | `zai_coder/production_saas_core` | `tests/test_production_saas_core_v11.py` | `docs/saas/*`, `scripts/saas/*` |
| Real Provider Adapters | `assets/providers/real_provider_adapters_features.json` | `zai_coder/real_provider_adapters` | `tests/test_real_provider_adapters_v17.py` | `docs/providers/*`, `scripts/providers/*` |
| Quality Assurance Test Lab | `assets/qa-test-lab/quality_assurance_test_lab_features.json` | `zai_coder/quality_assurance_test_lab` | `tests/test_quality_assurance_test_lab_v43.py` | `docs/qa-test-lab/*`, `scripts/qa-test-lab/*` |
| Release Automation Update Center | `assets/release-center/release_automation_update_center_features.json` | `zai_coder/release_automation_update_center` | `tests/test_release_automation_update_center_v29.py` | `docs/release-center/*`, `scripts/release-center/*` |
| Multi Region Edge Scalability | `assets/scalability-planner/multi_region_edge_scalability_features.json` | `zai_coder/multi_region_edge_scalability_planner` | `tests/test_multi_region_edge_scalability_planner_v48.py` | `docs/scalability-planner/*`, `scripts/scalability-planner/*` |
| Security Operations Threat Monitoring | `assets/security-ops/security_operations_threat_monitoring_features.json` | `zai_coder/security_operations_threat_monitoring` | `tests/test_security_operations_threat_monitoring_v46.py` | `docs/security-ops/*`, `scripts/security-ops/*` |
| Self Healing Operations | `assets/self-healing/self_healing_operations_features.json` | `zai_coder/self_healing_operations` | `tests/test_self_healing_operations_v30.py` | `docs/self-healing/*`, `scripts/self-healing/*` |
| Self Platform | `assets/self_features.json` | `zai_coder/core`, `zai_coder/cli.py`, `zai_coder/server.py` | `tests/test_self_core.py`, `tests/test_self_queue_v014.py`, `tests/test_self_healing_operations_v30.py` | `docs/ops/*`, `scripts/zai-self-dev.sh` |
| Team Collaboration Workspaces | `assets/team-collaboration/team_collaboration_workspaces_features.json` | `zai_coder/team_collaboration_workspaces` | `tests/test_team_collaboration_workspaces_v40.py` | `docs/team-collaboration/*`, `scripts/team-collaboration/*` |
| Multi Tenant Control | `assets/tenants/multi_tenant_control_features.json` | `zai_coder/multi_tenant_control` | `tests/test_multi_tenant_control_v21.py` | `docs/tenants/*`, `scripts/tenants/*` |
| Usage Analytics Insights | `assets/usage-analytics/usage_analytics_insights_features.json` | `zai_coder/usage_analytics_insights` | `tests/test_usage_analytics_insights_v35.py` | `docs/usage-analytics/*`, `scripts/usage-analytics/*` |
| Worker Orchestration | `assets/workers/worker_orchestration_features.json` | `zai_coder/worker_orchestration` | `tests/test_worker_orchestration_v25.py` | `docs/workers/*`, `scripts/workers/*` |

## Web And OpenUI Inventory

| Area | Current evidence | Status | Next production gate |
| --- | --- | --- | --- |
| Open WebUI baseline | `web/package.json`, `web/src/lib/*`, `web/backend/open_webui/*` | Owned/imported first-party surface | Dependency install, lint, typecheck, test, build, SBOM, license, and secret-scan in CI |
| ZAI command center | `web/src/routes/(app)/zai/+page.svelte` | Shipped local command center | Expand to module-level operations/governance/compliance/provider/marketplace views |
| OpenUI renderer | `web/src/lib/zai/openui.ts`, `web/src/lib/components/zai/OpenUIRenderer.svelte` | Runtime JSON schema renderer shipped | Add remote schema validation tests and component registry contract tests |
| Migration manifest | `web/src/lib/zai/migration-manifest.json`, `web/src/lib/zai/migration.ts` | 8 epics, 17 feature rows, 64% coverage | Close `runtime-production-deps`, `gateway-hardening`, `auth-session-e2e`, `durable-operations`, `web-ci-pipeline`, and `ide-symbol-intelligence` gaps |
| Web smoke gates | `tests/test_web_surface.py`, `scripts/repo/web-migration-report.py`, `make web-check` | Local smoke coverage exists | Promote to CI and add full web build gates |

## Open Production Gaps

| Area | Gap | Production risk | Target |
| --- | --- | --- | --- |
| Runtime server | FastAPI/ASGI runtime is optional and reports missing production dependencies unless `requirements-production.txt` is installed. | Deployments can pass local package tests but fail to serve if production extras are absent. | v51 |
| Production API gateway | Gateway modules are route/planning surfaces, not a fully managed live reverse proxy with TLS, upstream health failover, and public edge policy. | Public exposure would need external gateway hardening. | v51 |
| Auth/session operations | Local auth/session foundations exist, but enterprise SSO/session lifecycle needs end-to-end runtime validation against real deployment config. | Misconfigured auth can allow weak deployment posture. | v51 |
| Evaluation depth | Core local evals are more realistic now, but non-core suites need explicit live integration targets if they are to support external execution claims. | External execution claims can drift if suites stay local-only. | v51 |
| Observability | Health checks and trend reports exist, but alert deduplication, saturation control, durable trend storage, and SLO dashboards remain limited. | Noisy or missing alerts during incident response; history can be lost on restart. | v52 |
| Persistence | Several dashboards and reports use static/local snapshots; not all metrics, evidence, audit, and KPI streams have durable retention policies. | Restart or local file cleanup can lose operational history. | v52 |
| External providers | Provider adapters remain dry-run-first and require manual execution or an approved runner. | Correct for safety, but not full automated provider lifecycle management. | v52 |
| Frontend integration | `web/` has a smoke gate and ZAI command center, but full install/lint/typecheck/build/accessibility/SBOM gates are not yet first-class CI requirements. | Web regressions can pass backend-only release gates. | v54 |
| Versioning | Python package metadata (`0.1.4`) and v50 release labels are not a simple semver line. | Downstream automation may need explicit version mapping. | v51 |

## Candidate Defects To Validate

These came from the current tree and the untracked `docs/ROADMAPS.md` draft. Treat them as focused validation targets before implementation.

| Area | File | Candidate issue | Target |
| --- | --- | --- | --- |
| Observability | `zai_coder/observability_suite/health_trends.py` | `default_health_trend_store(execute=True)` catches broad exceptions and inserts an `"ok"` fallback, which can hide telemetry failures. | v52 |
| Operations Control Center | `zai_coder/operations_control_center/service_status.py` | Missing service checks now catch subprocess exceptions, but tests should cover exception paths and preserve diagnostic details. | v51 |
| Production API Gateway | `zai_coder/production_api_gateway/*` | Live routing, TLS, upstream health failover, and request-size/rate-limit behavior need integrated runtime smoke tests. | v51 |
| Execute/apply payloads | Routes and command handlers | Continue expanding tests for string booleans, apply flags, and dry-run/apply return types across route surfaces. | v51 |

## Release Priorities

### v51: Production Runtime Gate

- Add `make production-runtime-check` that installs or verifies `requirements-production.txt`, imports the ASGI server, and runs health/readiness probes.
- Promote optional FastAPI dependency state into `FINAL_RELEASE_STATUS.md` and final release reports.
- Add route-level tests for auth/session, gateway envelope handling, provider apply-denial behavior, and string/JSON boolean payloads.
- Add tests for Operations Control Center live service status exception paths.
- Update package/version metadata strategy so v50-style release labels and Python package versions are mapped intentionally.

### v52: Durable Operations Gate

- Add durable SQLite-backed stores for KPI snapshots, health trend history, compliance evidence inventory, execution/provider audit streams, and release evidence.
- Change observability fallback behavior so telemetry failures produce explicit degraded/diagnostic records, not healthy synthetic records.
- Add backup restore integration tests for safe extraction into a temporary tree and rejected archive member types.
- Add observability alert deduplication, rate limits, incident-review queues, and SLO dashboard exports.
- Add explicit retention policy for generated release, audit, and evidence artifacts.

### v53: External Deployment Gate

- Add a production gateway deployment profile with TLS termination assumptions, upstream health failover, request-size limits, rate limits, and structured audit logging.
- Add documented Cloudflare Access and DNS preflight gates for public exposure.
- Add container/runtime smoke tests for the production Docker Compose profile.
- Keep publishing, pushing, paid jobs, and third-party mutations manual until an approved external-action workflow is implemented.

### v54: Web Product Gate

- Promote `make web-check` and `make web-migration-report` into CI.
- Add full `web/` release pipeline: dependency install, lint, typecheck, test, build, accessibility, SBOM, license, and secret-scan gates.
- Expand `/zai` from the migration command center into module-level web control views for operations, governance, compliance, provider routing, marketplace, go-live, release, and eval workflows.
- Add OpenUI schema validation tests for remote components, dynamic registry entries, live preview, inspector behavior, and persisted theme modes.
- Keep vendor/reference-only content separate from the tracked release tree if any future imports are not intended to ship.

### v55: GA Release Gate

- Produce signed release metadata, checksums, SBOM, final manifest, and final production readiness report.
- Generate final handoff docs that distinguish shipped local features, dry-run plans, external go-live blockers, and manual approval boundaries.
- Require all release gates to run green from a clean checkout.
- Do not call the release externally production-ready until runtime, gateway, auth, persistence, web, and rollback gates are green together.

## Done Criteria For Production-Ready Claims

A release can be called production-ready only when all of the following are true:

- `python3 -m compileall -q zai_coder` passes.
- `python3 -m pytest -q` passes.
- `make repo-check`, `make secret-scan`, `make stage-manifest-check`, and `make final-release-status APPLY=1` pass.
- `make web-check APPLY=1` and `make web-migration-report` pass.
- Full `web/` install, lint, typecheck, test, build, accessibility, SBOM, license, and secret-scan gates pass.
- `make verify-source-package`, `make release-checksums`, and `make release-sbom` pass.
- Production runtime import and health/readiness probes pass with production dependencies installed.
- Public gateway, auth/session, Cloudflare Access/DNS, rate limiting, and rollback preflight gates pass.
- Durable operational persistence and retention policies are verified for metrics, evidence, audit, and release history.
- No untracked product surface is required for the release.
- External mutation workflows remain manual-only unless a scoped approval and audit path exists.
- Release notes list known warnings and clearly distinguish shipped features from dry-run plans.

## Operating Rules

- Keep local-first and dry-run-first behavior as the default.
- Never hardcode secrets or include `.env` files in release artifacts.
- Keep release scans focused on tracked source files; scan imported vendor/product trees only after ownership is explicit.
- Treat public exposure as blocked until Cloudflare Access, auth, rate limiting, logging, and rollback plans are verified.
- Keep roadmap items evidence-backed by tests, release gates, feature metadata, or generated reports.
- Do not claim external production readiness from local package tests alone.
