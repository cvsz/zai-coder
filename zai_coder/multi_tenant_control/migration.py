"""Tenant migration plan."""

from __future__ import annotations


def tenant_migration_plan(source_org: str = "local-org", target_org: str = "new-org") -> dict:
    return {
        "dry_run": True,
        "source_org": source_org,
        "target_org": target_org,
        "steps": [
            "freeze mutating provider operations",
            "create source tenant backup",
            "verify source export integrity",
            "create target tenant organization",
            "import workspaces into target tenant",
            "re-issue tenant-scoped API keys",
            "verify tenant isolation checks",
            "run health and governance gates",
            "unfreeze operations after approval",
        ],
        "rollback": [
            "disable target tenant keys",
            "restore source tenant from backup",
            "record rollback audit event",
        ],
    }
