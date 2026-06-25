"""Migration and rollback gates."""

from __future__ import annotations


def migration_gate(migrations: list[dict]) -> dict:
    blocked = []
    for migration in migrations:
        if migration.get("destructive") and not migration.get("backup_required"):
            blocked.append(f"{migration.get('id', 'unknown')}: destructive migration requires backup")
        if migration.get("touches_tenant_data") and not migration.get("tenant_scope_verified"):
            blocked.append(f"{migration.get('id', 'unknown')}: tenant scope verification required")
        if not migration.get("dry_run_sql", True):
            blocked.append(f"{migration.get('id', 'unknown')}: dry-run SQL required")
    return {"allowed": not blocked, "blocked": blocked, "migrations": migrations}


def rollback_gate(backup_ready: bool, rollback_manifest_ready: bool, smoke_tests_defined: bool) -> dict:
    checks = {
        "backup_ready": backup_ready,
        "rollback_manifest_ready": rollback_manifest_ready,
        "smoke_tests_defined": smoke_tests_defined,
    }
    blocked = [key for key, ok in checks.items() if not ok]
    return {"allowed": not blocked, "blocked": blocked, "checks": checks}


def default_migration_plan() -> dict:
    migrations = [
        {"id": "mig_release_audit", "destructive": False, "touches_tenant_data": False, "dry_run_sql": True},
        {"id": "mig_update_manifest_index", "destructive": False, "touches_tenant_data": True, "tenant_scope_verified": True, "dry_run_sql": True},
    ]
    return {"dry_run": True, "gate": migration_gate(migrations), "migrations": migrations}
