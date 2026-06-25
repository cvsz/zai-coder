"""Release automation and update center control helpers."""

from __future__ import annotations

from pathlib import Path

from .planner import create_release_plan, release_readiness_check
from .changelog import default_changelog
from .update_manifest import build_update_manifest, write_update_manifest
from .updater import dry_run_update_plan, update_decision
from .migrations import default_migration_plan, rollback_gate
from .github_release import github_release_draft
from .audit import ReleaseAuditLog


def release_center_status() -> dict:
    return {
        "ok": True,
        "systems": [
            "release_planner",
            "version_channel_policy",
            "changelog_generator",
            "update_manifest_builder",
            "checksum_verifier",
            "dry_run_updater",
            "migration_gate",
            "rollback_gate",
            "github_release_draft",
            "release_audit_log",
        ],
    }


def release_plan_demo() -> dict:
    plan = create_release_plan()
    readiness = release_readiness_check(plan, {
        "tests_passed": True,
        "repo_check_ok": True,
        "secret_scan_ok": True,
        "artifacts_present": True,
        "checksums_generated": True,
        "rollback_plan_ready": True,
        "approval_id": "approved_manual_001",
    })
    return {"plan": plan.to_dict(), "readiness": readiness, "changelog": default_changelog(plan.version.version)}


def update_manifest_demo(root: str | Path = ".") -> dict:
    root = Path(root)
    artifact = root / "releases/drafts/demo-artifact.txt"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text("demo artifact for update manifest\n", encoding="utf-8")
    manifest = build_update_manifest("v29.0.0", "stable", "zai-coder-control-plane", str(artifact))
    path = write_update_manifest(manifest, root)
    return {"manifest": manifest.to_dict(), "path": path}


def update_plan_demo(root: str | Path = ".") -> dict:
    manifest_payload = update_manifest_demo(root)["manifest"]
    plan = dry_run_update_plan("v28.0.0", manifest_payload)
    decision = update_decision("v28.0.0", manifest_payload, "approved_manual_001", True, True)
    return {"plan": plan, "decision": decision.to_dict()}


def rollback_migration_demo() -> dict:
    return {
        "migration": default_migration_plan(),
        "rollback": rollback_gate(True, True, True),
    }


def release_audit_demo(db_path: str = "data/release-update-center.db") -> dict:
    audit = ReleaseAuditLog(db_path)
    event = audit.record("system", "release.plan_created", "v29.0.0", {"dry_run": True})
    return {"event": event.to_dict(), "events": audit.list_events()}
