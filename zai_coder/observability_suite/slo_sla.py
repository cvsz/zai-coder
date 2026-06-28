"""SLO/SLA templates."""

from __future__ import annotations


def slo_templates() -> list[dict]:
    return [
        {
            "name": "control_plane_availability",
            "objective": "99.5% monthly availability for authenticated control-plane UI",
            "measurement": "successful /healthz and /readyz checks",
            "window": "30d",
        },
        {
            "name": "execution_runner_success",
            "objective": "95% approved non-mutating command plans succeed",
            "measurement": "execution journal completed / total non-blocked runs",
            "window": "7d",
        },
        {
            "name": "backup_freshness",
            "objective": "backup created at least once every 24h",
            "measurement": "latest backup age",
            "window": "24h",
        },
    ]


def sla_template() -> dict:
    return {
        "name": "internal_self_hosted_support",
        "scope": "self-hosted internal service",
        "response_targets": {"sev1": "4h", "sev2": "1 business day", "sev3": "3 business days"},
        "exclusions": ["internet provider outage", "Cloudflare account misconfiguration", "host resource exhaustion"],
    }

def export_slo_dashboard() -> dict:
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return {
        "dashboard_name": "SLO/SLA Dashboard",
        "generated_at": now,
        "slos": slo_templates(),
        "slas": [sla_template()],
        "status": "active"
    }
