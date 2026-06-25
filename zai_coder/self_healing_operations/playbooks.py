"""Safe remediation playbooks."""

from __future__ import annotations

from .models import RemediationPlaybook


DEFAULT_PLAYBOOKS = [
    RemediationPlaybook(
        id="restart-local-service",
        name="Restart Local Service Plan",
        service="core",
        trigger="heartbeat_age_seconds",
        actions=("make healthcheck", "make deploy-systemd", "make healthcheck"),
        risk_level="medium",
    ),
    RemediationPlaybook(
        id="drain-worker-queue",
        name="Drain Worker Queue Plan",
        service="workers",
        trigger="queue_depth",
        actions=("make worker-policy", "make worker-lease-and-plan", "make worker-audit"),
        risk_level="low",
    ),
    RemediationPlaybook(
        id="rollback-last-release",
        name="Rollback Last Release Plan",
        service="release-center",
        trigger="error_rate",
        actions=("make rollback-migration-gate", "make update-plan", "make release-audit"),
        risk_level="high",
    ),
    RemediationPlaybook(
        id="rotate-cloudflare-access-check",
        name="Cloudflare Access Check Plan",
        service="cloudflare",
        trigger="latency_ms",
        actions=("make cloudflare-access-checklist", "make cloudflare-exposure-scan", "make cloudflare-public-health-plan"),
        risk_level="medium",
    ),
]


def playbook_catalog() -> list[dict]:
    return [playbook.to_dict() for playbook in DEFAULT_PLAYBOOKS]


def find_playbook(playbook_id: str) -> RemediationPlaybook:
    for playbook in DEFAULT_PLAYBOOKS:
        if playbook.id == playbook_id:
            return playbook
    raise ValueError(f"unknown playbook: {playbook_id}")


def match_playbook(service: str, trigger: str) -> RemediationPlaybook:
    for playbook in DEFAULT_PLAYBOOKS:
        if playbook.service == service and playbook.trigger == trigger:
            return playbook
    for playbook in DEFAULT_PLAYBOOKS:
        if playbook.trigger == trigger:
            return playbook
    return DEFAULT_PLAYBOOKS[0]


def validate_playbook_catalog() -> dict:
    reports = [{"id": playbook.id, "issues": playbook.validate()} for playbook in DEFAULT_PLAYBOOKS]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}
