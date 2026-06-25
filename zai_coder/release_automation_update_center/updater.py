"""Dry-run updater and update gates."""

from __future__ import annotations

from .models import UpdateDecision


def compare_versions(current: str, target: str) -> dict:
    # Lightweight deterministic comparison for vMAJOR.MINOR.PATCH.
    def parts(v: str) -> tuple[int, int, int]:
        core = v[1:].split("-", 1)[0] if v.startswith("v") else v
        p = core.split(".")
        return (int(p[0]), int(p[1]), int(p[2]))
    current_parts = parts(current)
    target_parts = parts(target)
    return {"current": current, "target": target, "upgrade": target_parts > current_parts, "same": target_parts == current_parts, "downgrade": target_parts < current_parts}


def update_decision(current_version: str, manifest: dict, approval_id: str = "", backup_ready: bool = False, dry_run_completed: bool = True) -> UpdateDecision:
    comparison = compare_versions(current_version, manifest["version"])
    if not dry_run_completed:
        return UpdateDecision(False, "blocked", "dry-run required before update")
    if not backup_ready:
        return UpdateDecision(False, "blocked", "backup required before update")
    if not str(approval_id).startswith("approved_"):
        return UpdateDecision(False, "blocked", "approval required before update")
    if comparison["same"]:
        return UpdateDecision(False, "noop", "already on requested version", required_backup=False, required_approval=False)
    if comparison["downgrade"] and not manifest.get("rollback_supported", False):
        return UpdateDecision(False, "blocked", "rollback not supported by manifest")
    return UpdateDecision(True, "upgrade" if comparison["upgrade"] else "rollback", "update may proceed as approved dry-run plan")


def dry_run_update_plan(current_version: str, manifest: dict) -> dict:
    comparison = compare_versions(current_version, manifest["version"])
    return {
        "dry_run": True,
        "comparison": comparison,
        "manifest": manifest,
        "steps": [
            "verify artifact checksum",
            "create backup",
            "stop worker/agent schedulers",
            "apply update package",
            "run migrations in dry-run mode",
            "run smoke tests",
            "resume schedulers",
            "write release audit event",
        ],
        "rollback": [
            "stop schedulers",
            "restore previous package",
            "restore backup if migration touched state",
            "run smoke tests",
            "write rollback audit event",
        ],
    }
