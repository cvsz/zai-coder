"""Tenant onboarding wizard."""

from __future__ import annotations


def tenant_onboarding_plan(org_name: str = "Local Org", org_slug: str = "local-org", workspace_name: str = "Default", workspace_slug: str = "default") -> dict:
    return {
        "dry_run": True,
        "steps": [
            "create tenant organization",
            "create default workspace",
            "assign tenant owner",
            "create workspace quota",
            "create tenant-scoped API key",
            "record onboarding audit event",
            "generate tenant backup/export policy",
        ],
        "payload": {
            "org_name": org_name,
            "org_slug": org_slug,
            "workspace_name": workspace_name,
            "workspace_slug": workspace_slug,
        },
    }
