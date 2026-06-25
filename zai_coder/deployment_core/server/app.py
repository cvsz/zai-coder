"""Dependency-light local HTTP server for ZAI App Studio.

This is intentionally simple and stdlib-only. It serves health, status, and a
static HTML dashboard. Production deployments can replace it with FastAPI later.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from zai_coder.app_studio.routes import route_status, route_dashboard
from zai_coder.deployment_core.health import run_deployment_health, health_summary
from zai_coder.integration_core.routes import route_integrations, route_github_status, route_docker_status, route_openapi
from zai_coder.production_saas_core.routes import route_saas_status, route_billing_dashboard, route_settings_dashboard
from zai_coder.app_studio_final.routes import route_final_status, route_home, route_plugins, route_workflows, route_models, route_deployments
from zai_coder.app_studio_final.openapi_full import build_full_openapi_schema
from zai_coder.operations_control_center.routes import route_ops_status, route_ops_overview, route_ops_services_page, route_ops_health_page, route_ops_backup_page, route_ops_upgrade_page
from zai_coder.cloudflare_go_live.routes import route_cloudflare_status, route_go_live_page, route_access_page, route_dns_page, route_rollback_page, route_public_health_page
from zai_coder.real_provider_adapters.routes import route_providers_status, route_providers_page, route_provider_audit_page
from zai_coder.execution_runner.routes import route_execution_status, route_approval_dashboard, route_execution_timeline
from zai_coder.observability_suite.routes import route_observability_status, route_metrics_prometheus, route_observability_page, route_metrics_page, route_alerts_page, route_health_trends_page
from zai_coder.enterprise_governance.routes import route_governance_status, route_governance_page, route_policies_page, route_roles_page, route_risks_page, route_release_gate_page, route_compliance_page
from zai_coder.multi_tenant_control.routes import route_tenant_status, route_tenant_page, route_tenant_onboarding_page, route_tenant_backup_page, route_tenant_migration_page
from zai_coder.billing_usage_enforcement.routes import route_billing_status, route_billing_page, route_billing_plans_page, route_billing_usage_page, route_billing_invoice_page
from zai_coder.payment_provider_sandbox.routes import route_payment_status, route_payment_page, route_payment_checkout_page, route_payment_subscription_page, route_payment_webhooks_page
from zai_coder.production_api_gateway.routes import route_gateway_status, route_gateway_page, route_gateway_routes_page, route_gateway_upstreams_page, route_gateway_security_page, route_gateway_openapi
from zai_coder.worker_orchestration.routes import route_worker_status, route_worker_page, route_worker_schedules_page, route_worker_policy_page
from zai_coder.agent_runtime_supervisor.routes import route_agent_status, route_agent_page, route_agent_sandbox_page, route_agent_lifecycle_page, route_agent_policy_page
from zai_coder.agent_marketplace_and_skills.routes import route_marketplace_status, route_marketplace_page, route_marketplace_skills_page, route_marketplace_agents_page, route_marketplace_policy_page
from zai_coder.plugin_connector_hub.routes import route_connector_status, route_connector_page, route_connector_catalog_page, route_connector_policy_page, route_connector_sync_page
from zai_coder.release_automation_update_center.routes import route_release_center_status, route_release_center_page, route_release_plan_page, route_update_center_page, route_release_channels_page
from zai_coder.self_healing_operations.routes import route_self_healing_status, route_self_healing_page, route_self_healing_incidents_page, route_self_healing_playbooks_page, route_self_healing_policy_page
from zai_coder.enterprise_compliance_center.routes import route_compliance_status, route_compliance_page, route_compliance_frameworks_page, route_compliance_controls_page, route_compliance_risks_page
from zai_coder.enterprise_reporting_board_pack.routes import route_board_pack_status, route_board_pack_page, route_board_kpis_page, route_board_decisions_page, route_board_risks_page
from zai_coder.enterprise_admin_console.routes import route_admin_status, route_admin_page, route_admin_tenants_page, route_admin_users_page, route_admin_flags_page, route_admin_services_page
from zai_coder.customer_portal_onboarding.routes import route_customer_portal_status, route_customer_page, route_customer_accounts_page, route_customer_onboarding_page, route_customer_features_page, route_customer_support_page
from zai_coder.usage_analytics_insights.routes import route_usage_analytics_status, route_analytics_page, route_analytics_metrics_page, route_analytics_insights_page, route_analytics_funnel_page, route_analytics_privacy_page
from zai_coder.feedback_roadmap_center.routes import route_feedback_roadmap_status, route_roadmap_page, route_roadmap_feedback_page, route_roadmap_items_page, route_roadmap_customer_view_page, route_roadmap_prioritization_page
from zai_coder.knowledge_base_help_center.routes import route_help_center_status, route_help_page, route_help_articles_page, route_help_faq_page, route_help_search_page, route_help_admin_page
from zai_coder.template_content_studio.routes import route_content_studio_status, route_content_studio_page, route_content_templates_page, route_content_render_page, route_content_brand_page, route_content_library_page
from zai_coder.notification_communication_center.routes import route_notification_center_status, route_notifications_page, route_notifications_channels_page, route_notifications_templates_page, route_notifications_preferences_page, route_notifications_drafts_page


class ZaiAppStudioHandler(BaseHTTPRequestHandler):
    server_version = "ZAIAppStudio/0.1"

    def _send_json(self, payload: dict, status: int = 200) -> None:
        data = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


    def _send_text(self, text, status=200, content_type="text/plain"):
        data = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_html(self, html: str, status: int = 200) -> None:
        data = html.encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "text/html; charset=utf-8")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):  # noqa: N802 - stdlib handler name
        path = urlparse(self.path).path
        if path == "/healthz":
            self._send_json(health_summary(run_deployment_health()))
            return
        if path == "/api/status":
            self._send_json(route_status())
            return
        if path == "/api/integrations":
            self._send_json(route_integrations())
            return
        if path == "/api/integrations/github/status-plan":
            self._send_json(route_github_status())
            return
        if path == "/api/integrations/docker/status-plan":
            self._send_json(route_docker_status())
            return
        if path == "/openapi.json":
            self._send_json(route_openapi())
            return
        if path == "/api/saas/status":
            self._send_json(route_saas_status())
            return
        if path == "/api/final/status":
            self._send_json(route_final_status())
            return
        if path == "/api/ops/status":
            self._send_json(route_ops_status())
            return
        if path == "/api/cloudflare/status":
            self._send_json(route_cloudflare_status())
            return
        if path == "/api/providers/status":
            self._send_json(route_providers_status())
            return
        if path == "/api/execution/status":
            self._send_json(route_execution_status())
            return
        if path == "/api/observability/status":
            self._send_json(route_observability_status())
            return
        if path == "/api/governance/status":
            self._send_json(route_governance_status())
            return
        if path == "/api/tenants/status":
            self._send_json(route_tenant_status())
            return
        if path == "/api/billing/status":
            self._send_json(route_billing_status())
            return
        if path == "/api/payments/status":
            self._send_json(route_payment_status())
            return
        if path == "/api/gateway/status":
            self._send_json(route_gateway_status())
            return
        if path == "/api/workers/status":
            self._send_json(route_worker_status())
            return
        if path == "/api/agents/status":
            self._send_json(route_agent_status())
            return
        if path == "/api/marketplace/status":
            self._send_json(route_marketplace_status())
            return
        if path == "/api/connectors/status":
            self._send_json(route_connector_status())
            return
        if path == "/api/release-center/status":
            self._send_json(route_release_center_status())
            return
        if path == "/api/self-healing/status":
            self._send_json(route_self_healing_status())
            return
        if path == "/api/compliance/status":
            self._send_json(route_compliance_status())
            return
        if path == "/api/board-pack/status":
            self._send_json(route_board_pack_status())
            return
        if path == "/api/admin/status":
            self._send_json(route_admin_status())
            return
        if path == "/api/customer/status":
            self._send_json(route_customer_portal_status())
            return
        if path == "/api/analytics/status":
            self._send_json(route_usage_analytics_status())
            return
        if path == "/api/roadmap/status":
            self._send_json(route_feedback_roadmap_status())
            return
        if path == "/api/help/status":
            self._send_json(route_help_center_status())
            return
        if path == "/api/content-studio/status":
            self._send_json(route_content_studio_status())
            return
        if path == "/api/notifications/status":
            self._send_json(route_notification_center_status())
            return
        if path in {"/notifications", "/notifications/"}:
            self._send_html(route_notifications_page()["html"])
            return
        if path == "/notifications/channels":
            self._send_html(route_notifications_channels_page()["html"])
            return
        if path == "/notifications/templates":
            self._send_html(route_notifications_templates_page()["html"])
            return
        if path == "/notifications/preferences":
            self._send_html(route_notifications_preferences_page()["html"])
            return
        if path == "/notifications/drafts":
            self._send_html(route_notifications_drafts_page()["html"])
            return
        if path in {"/content-studio", "/content-studio/"}:
            self._send_html(route_content_studio_page()["html"])
            return
        if path == "/content-studio/templates":
            self._send_html(route_content_templates_page()["html"])
            return
        if path == "/content-studio/render":
            self._send_html(route_content_render_page()["html"])
            return
        if path == "/content-studio/brand":
            self._send_html(route_content_brand_page()["html"])
            return
        if path == "/content-studio/library":
            self._send_html(route_content_library_page()["html"])
            return
        if path in {"/help", "/help/"}:
            self._send_html(route_help_page()["html"])
            return
        if path == "/help/articles":
            self._send_html(route_help_articles_page()["html"])
            return
        if path == "/help/faq":
            self._send_html(route_help_faq_page()["html"])
            return
        if path == "/help/search":
            self._send_html(route_help_search_page()["html"])
            return
        if path == "/help/admin":
            self._send_html(route_help_admin_page()["html"])
            return
        if path in {"/roadmap", "/roadmap/"}:
            self._send_html(route_roadmap_page()["html"])
            return
        if path == "/roadmap/feedback":
            self._send_html(route_roadmap_feedback_page()["html"])
            return
        if path == "/roadmap/items":
            self._send_html(route_roadmap_items_page()["html"])
            return
        if path == "/roadmap/customer-view":
            self._send_html(route_roadmap_customer_view_page()["html"])
            return
        if path == "/roadmap/prioritization":
            self._send_html(route_roadmap_prioritization_page()["html"])
            return
        if path in {"/analytics", "/analytics/"}:
            self._send_html(route_analytics_page()["html"])
            return
        if path == "/analytics/metrics":
            self._send_html(route_analytics_metrics_page()["html"])
            return
        if path == "/analytics/insights":
            self._send_html(route_analytics_insights_page()["html"])
            return
        if path == "/analytics/funnel":
            self._send_html(route_analytics_funnel_page()["html"])
            return
        if path == "/analytics/privacy":
            self._send_html(route_analytics_privacy_page()["html"])
            return
        if path in {"/customer", "/customer/"}:
            self._send_html(route_customer_page()["html"])
            return
        if path == "/customer/accounts":
            self._send_html(route_customer_accounts_page()["html"])
            return
        if path == "/customer/onboarding":
            self._send_html(route_customer_onboarding_page()["html"])
            return
        if path == "/customer/features":
            self._send_html(route_customer_features_page()["html"])
            return
        if path == "/customer/support":
            self._send_html(route_customer_support_page()["html"])
            return
        if path in {"/admin", "/admin/"}:
            self._send_html(route_admin_page()["html"])
            return
        if path == "/admin/tenants":
            self._send_html(route_admin_tenants_page()["html"])
            return
        if path == "/admin/users":
            self._send_html(route_admin_users_page()["html"])
            return
        if path == "/admin/flags":
            self._send_html(route_admin_flags_page()["html"])
            return
        if path == "/admin/services":
            self._send_html(route_admin_services_page()["html"])
            return
        if path in {"/board-pack", "/board-pack/"}:
            self._send_html(route_board_pack_page()["html"])
            return
        if path == "/board-pack/kpis":
            self._send_html(route_board_kpis_page()["html"])
            return
        if path == "/board-pack/decisions":
            self._send_html(route_board_decisions_page()["html"])
            return
        if path == "/board-pack/risks":
            self._send_html(route_board_risks_page()["html"])
            return
        if path in {"/compliance", "/compliance/"}:
            self._send_html(route_compliance_page()["html"])
            return
        if path == "/compliance/frameworks":
            self._send_html(route_compliance_frameworks_page()["html"])
            return
        if path == "/compliance/controls":
            self._send_html(route_compliance_controls_page()["html"])
            return
        if path == "/compliance/risks":
            self._send_html(route_compliance_risks_page()["html"])
            return
        if path in {"/self-healing", "/self-healing/"}:
            self._send_html(route_self_healing_page()["html"])
            return
        if path == "/self-healing/incidents":
            self._send_html(route_self_healing_incidents_page()["html"])
            return
        if path == "/self-healing/playbooks":
            self._send_html(route_self_healing_playbooks_page()["html"])
            return
        if path == "/self-healing/policy":
            self._send_html(route_self_healing_policy_page()["html"])
            return
        if path in {"/release-center", "/release-center/"}:
            self._send_html(route_release_center_page()["html"])
            return
        if path == "/release-center/plan":
            self._send_html(route_release_plan_page()["html"])
            return
        if path == "/release-center/updates":
            self._send_html(route_update_center_page()["html"])
            return
        if path == "/release-center/channels":
            self._send_html(route_release_channels_page()["html"])
            return
        if path in {"/connectors", "/connectors/"}:
            self._send_html(route_connector_page()["html"])
            return
        if path == "/connectors/catalog":
            self._send_html(route_connector_catalog_page()["html"])
            return
        if path == "/connectors/policy":
            self._send_html(route_connector_policy_page()["html"])
            return
        if path == "/connectors/sync":
            self._send_html(route_connector_sync_page()["html"])
            return
        if path in {"/marketplace", "/marketplace/"}:
            self._send_html(route_marketplace_page()["html"])
            return
        if path == "/marketplace/skills":
            self._send_html(route_marketplace_skills_page()["html"])
            return
        if path == "/marketplace/agents":
            self._send_html(route_marketplace_agents_page()["html"])
            return
        if path == "/marketplace/policy":
            self._send_html(route_marketplace_policy_page()["html"])
            return
        if path in {"/agents", "/agents/"}:
            self._send_html(route_agent_page()["html"])
            return
        if path == "/agents/sandbox":
            self._send_html(route_agent_sandbox_page()["html"])
            return
        if path == "/agents/lifecycle":
            self._send_html(route_agent_lifecycle_page()["html"])
            return
        if path == "/agents/policy":
            self._send_html(route_agent_policy_page()["html"])
            return
        if path in {"/workers", "/workers/"}:
            self._send_html(route_worker_page()["html"])
            return
        if path == "/workers/schedules":
            self._send_html(route_worker_schedules_page()["html"])
            return
        if path == "/workers/policy":
            self._send_html(route_worker_policy_page()["html"])
            return
        if path == "/gateway/openapi.json":
            self._send_json(route_gateway_openapi())
            return
        if path in {"/gateway", "/gateway/"}:
            self._send_html(route_gateway_page()["html"])
            return
        if path == "/gateway/routes":
            self._send_html(route_gateway_routes_page()["html"])
            return
        if path == "/gateway/upstreams":
            self._send_html(route_gateway_upstreams_page()["html"])
            return
        if path == "/gateway/security":
            self._send_html(route_gateway_security_page()["html"])
            return
        if path in {"/payments", "/payments/"}:
            self._send_html(route_payment_page()["html"])
            return
        if path == "/payments/checkout":
            self._send_html(route_payment_checkout_page()["html"])
            return
        if path == "/payments/subscription":
            self._send_html(route_payment_subscription_page()["html"])
            return
        if path == "/payments/webhooks":
            self._send_html(route_payment_webhooks_page()["html"])
            return
        if path in {"/billing", "/billing/"}:
            self._send_html(route_billing_page()["html"])
            return
        if path == "/billing/plans":
            self._send_html(route_billing_plans_page()["html"])
            return
        if path == "/billing/usage":
            self._send_html(route_billing_usage_page()["html"])
            return
        if path == "/billing/invoice":
            self._send_html(route_billing_invoice_page()["html"])
            return
        if path in {"/tenants", "/tenants/"}:
            self._send_html(route_tenant_page()["html"])
            return
        if path == "/tenants/onboarding":
            self._send_html(route_tenant_onboarding_page()["html"])
            return
        if path == "/tenants/backup":
            self._send_html(route_tenant_backup_page()["html"])
            return
        if path == "/tenants/migration":
            self._send_html(route_tenant_migration_page()["html"])
            return
        if path in {"/governance", "/governance/"}:
            self._send_html(route_governance_page()["html"])
            return
        if path == "/governance/policies":
            self._send_html(route_policies_page()["html"])
            return
        if path == "/governance/roles":
            self._send_html(route_roles_page()["html"])
            return
        if path == "/governance/risks":
            self._send_html(route_risks_page()["html"])
            return
        if path == "/governance/release":
            self._send_html(route_release_gate_page()["html"])
            return
        if path == "/governance/compliance":
            self._send_html(route_compliance_page()["html"])
            return
        if path == "/metrics":
            payload = route_metrics_prometheus()
            self._send_text(payload["text"], content_type="text/plain")
            return
        if path in {"/observability", "/observability/"}:
            self._send_html(route_observability_page()["html"])
            return
        if path == "/observability/metrics":
            self._send_html(route_metrics_page()["html"])
            return
        if path == "/observability/alerts":
            self._send_html(route_alerts_page()["html"])
            return
        if path == "/observability/health":
            self._send_html(route_health_trends_page()["html"])
            return
        if path in {"/execution/approval", "/execution/approval/"}:
            self._send_html(route_approval_dashboard()["html"])
            return
        if path in {"/execution/timeline", "/execution/timeline/"}:
            self._send_html(route_execution_timeline()["html"])
            return
        if path in {"/providers", "/providers/"}:
            self._send_html(route_providers_page()["html"])
            return
        if path == "/providers/audit":
            self._send_html(route_provider_audit_page()["html"])
            return
        if path in {"/cloudflare", "/cloudflare/"}:
            self._send_html(route_go_live_page()["html"])
            return
        if path == "/cloudflare/access":
            self._send_html(route_access_page()["html"])
            return
        if path == "/cloudflare/dns":
            self._send_html(route_dns_page()["html"])
            return
        if path == "/cloudflare/rollback":
            self._send_html(route_rollback_page()["html"])
            return
        if path == "/cloudflare/public-health":
            self._send_html(route_public_health_page()["html"])
            return
        if path in {"/ops", "/ops/"}:
            self._send_html(route_ops_overview()["html"])
            return
        if path == "/ops/services":
            self._send_html(route_ops_services_page()["html"])
            return
        if path == "/ops/health":
            self._send_html(route_ops_health_page()["html"])
            return
        if path == "/ops/backup":
            self._send_html(route_ops_backup_page()["html"])
            return
        if path == "/ops/upgrade":
            self._send_html(route_ops_upgrade_page()["html"])
            return
        if path == "/openapi.full.json":
            self._send_json(build_full_openapi_schema())
            return
        if path in {"/studio", "/studio/"}:
            self._send_html(route_home()["html"])
            return
        if path == "/studio/plugins":
            self._send_html(route_plugins()["html"])
            return
        if path == "/studio/workflows":
            self._send_html(route_workflows()["html"])
            return
        if path == "/studio/models":
            self._send_html(route_models()["html"])
            return
        if path == "/studio/deployments":
            self._send_html(route_deployments()["html"])
            return
        if path == "/saas/billing":
            self._send_html(route_billing_dashboard()["html"])
            return
        if path == "/saas/settings":
            self._send_html(route_settings_dashboard()["html"])
            return
        if path in {"/", "/dashboard"}:
            payload = {
                "projects": [{"slug": "demo", "title": "Demo Project", "project_type": "game", "status": "draft"}],
                "members": [{"email": "admin@example.com", "display_name": "Admin", "status": "active"}],
                "plans": [{"slug": "free", "name": "Free", "monthly_price_cents": 0}],
                "runs": [{"id": "run-demo", "run_type": "health", "status": "ok"}],
                "audit_events": [{"actor": "system", "action": "serve", "target": "dashboard"}],
            }
            self._send_html(route_dashboard(payload)["html"])
            return
        self._send_json({"error": "not found", "path": path}, status=404)

    def log_message(self, fmt, *args):  # reduce noisy stdout by default
        return


def run_server(host: str = "127.0.0.1", port: int = 8765) -> ThreadingHTTPServer:
    if host in {"0.0.0.0", "::"}:
        print("WARNING: binding publicly. Use API auth and Cloudflare Access before exposing this service.")
    server = ThreadingHTTPServer((host, int(port)), ZaiAppStudioHandler)
    print(f"ZAI App Studio serving on http://{host}:{port}")
    server.serve_forever()
    return server
