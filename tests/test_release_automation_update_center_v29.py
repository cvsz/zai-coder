from pathlib import Path
import tempfile
import json

from zai_coder.release_automation_update_center.models import ReleaseVersion, ReleasePlan, UpdateManifest, UpdateDecision
from zai_coder.release_automation_update_center.channels import release_channel_manifest, channel_policy
from zai_coder.release_automation_update_center.versioning import parse_version, next_version, version_plan
from zai_coder.release_automation_update_center.checksums import sha256_file, artifact_manifest, verify_artifact
from zai_coder.release_automation_update_center.changelog import changelog_from_items, default_changelog
from zai_coder.release_automation_update_center.planner import create_release_plan, release_readiness_check
from zai_coder.release_automation_update_center.update_manifest import build_update_manifest, write_update_manifest, update_manifest_schema
from zai_coder.release_automation_update_center.updater import compare_versions, update_decision, dry_run_update_plan
from zai_coder.release_automation_update_center.migrations import migration_gate, rollback_gate, default_migration_plan
from zai_coder.release_automation_update_center.github_release import github_release_draft, github_release_command_plan
from zai_coder.release_automation_update_center.audit import ReleaseAuditLog
from zai_coder.release_automation_update_center.control import release_center_status, release_plan_demo, update_manifest_demo, update_plan_demo, rollback_migration_demo, release_audit_demo
from zai_coder.release_automation_update_center.ui.pages import render_release_overview, render_release_plan_page, render_update_page, render_channels_page
from zai_coder.release_automation_update_center.routes import (
    route_release_center_status,
    route_release_channels,
    route_release_channel_policy,
    route_version_plan,
    route_release_plan_demo,
    route_changelog_demo,
    route_update_manifest_demo,
    route_update_manifest_schema,
    route_update_plan_demo,
    route_rollback_migration_demo,
    route_github_release_draft,
    route_github_release_command_plan,
    route_release_audit_demo,
    route_release_audit,
    route_release_center_page,
    route_release_plan_page,
    route_update_center_page,
    route_release_channels_page,
)


def test_models_and_channels():
    assert ReleaseVersion("v1.0.0").validate() == []
    assert ReleaseVersion("1.0.0", channel="bad").validate()
    assert UpdateManifest("u", "v1.0.0", "stable", "pkg", "pkg.zip").validate() == []
    assert UpdateManifest("", "", "bad", "", "", rollback_supported=False).validate()
    assert UpdateDecision(True, "upgrade", "ok").to_dict()["allowed"] is True
    assert "stable" in release_channel_manifest()
    assert channel_policy("stable")["requires_approval"] is True


def test_versioning_changelog():
    assert parse_version("v1.2.3")["minor"] == 2
    assert next_version("v1.2.3", "patch").version == "v1.2.4"
    assert next_version("v1.2.3", "minor", "beta").version == "v1.3.0-beta.1"
    assert version_plan("v1.0.0", "minor", "stable")["release"]["version"] == "v1.1.0"
    assert "Changelog v1.1.0" in changelog_from_items("v1.1.0", ["added x"])
    assert "Release automation center" in default_changelog("v29.0.0")


def test_checksums_manifest_and_update(tmp_path):
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("artifact", encoding="utf-8")
    checksum = sha256_file(artifact)
    manifest = artifact_manifest(artifact)
    assert manifest["ok"] is True
    assert verify_artifact(artifact, checksum)["matches"] is True
    update_manifest = build_update_manifest("v29.0.0", "stable", "pkg", str(artifact))
    assert update_manifest.sha256 == checksum
    written = write_update_manifest(update_manifest, tmp_path)
    assert Path(written).exists()
    assert update_manifest_schema()["safe_defaults"]["rollback_supported"] is True
    comparison = compare_versions("v28.0.0", "v29.0.0")
    assert comparison["upgrade"] is True
    decision = update_decision("v28.0.0", update_manifest.to_dict(), "approved_manual_001", True, True)
    assert decision.allowed is True
    blocked = update_decision("v28.0.0", update_manifest.to_dict(), "", False, True)
    assert blocked.allowed is False
    plan = dry_run_update_plan("v28.0.0", update_manifest.to_dict())
    assert plan["dry_run"] is True


def test_release_plan_migrations_github_audit(tmp_path):
    plan = create_release_plan("v28.0.0", "minor", "stable")
    assert plan.dry_run is True
    blocked = release_readiness_check(plan, {})
    assert blocked["allowed"] is False
    ok = release_readiness_check(plan, {
        "tests_passed": True,
        "repo_check_ok": True,
        "secret_scan_ok": True,
        "artifacts_present": True,
        "checksums_generated": True,
        "rollback_plan_ready": True,
        "approval_id": "approved_manual_001",
    })
    assert ok["allowed"] is True
    assert migration_gate([{"id":"m1", "destructive": True, "backup_required": False}])["allowed"] is False
    assert rollback_gate(True, True, True)["allowed"] is True
    assert default_migration_plan()["gate"]["allowed"] is True
    draft = github_release_draft("v29.0.0")
    assert draft["dry_run"] is True
    assert "no force push" in draft["safe_git_policy"]
    assert github_release_command_plan("v29.0.0")["requires_manual_review"] is True
    audit = ReleaseAuditLog(tmp_path / "release.db")
    event = audit.record("tester", "release.plan", "v29.0.0")
    assert audit.list_events()[0]["id"] == event.id


def test_control_ui_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert release_center_status()["ok"] is True
    assert release_plan_demo()["readiness"]["allowed"] is True
    assert Path(update_manifest_demo(tmp_path)["path"]).exists()
    assert update_plan_demo(tmp_path)["decision"]["allowed"] is True
    assert rollback_migration_demo()["rollback"]["allowed"] is True
    assert release_audit_demo(str(tmp_path / "audit.db"))["event"]["id"].startswith("rae_")
    assert "Release Automation and Update Center" in render_release_overview()
    assert "Release Plan" in render_release_plan_page()
    assert "Update Center" in render_update_page()
    assert "Release Channels" in render_channels_page()
    assert route_release_center_status()["ok"] is True
    assert route_release_channels()["channels"]
    assert route_release_channel_policy("stable")["channel"] == "stable"
    assert route_version_plan("v28.0.0", "minor", "stable")["release"]["version"] == "v28.1.0"
    assert route_release_plan_demo()["readiness"]["allowed"] is True
    assert "markdown" in route_changelog_demo()
    assert Path(route_update_manifest_demo()["path"]).exists()
    assert route_update_manifest_schema()["required"]
    assert route_update_plan_demo()["decision"]["allowed"] is True
    assert route_rollback_migration_demo()["rollback"]["allowed"] is True
    assert route_github_release_draft()["dry_run"] is True
    assert route_github_release_command_plan()["dry_run"] is True
    assert route_release_audit_demo()["event"]
    assert "events" in route_release_audit()
    assert route_release_center_page()["content_type"] == "text/html"
    assert route_release_plan_page()["content_type"] == "text/html"
    assert route_update_center_page()["content_type"] == "text/html"
    assert route_release_channels_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/release-center/release-center-status.sh",
        "scripts/release-center/release-channels.sh",
        "scripts/release-center/version-plan.sh",
        "scripts/release-center/release-plan.sh",
        "scripts/release-center/changelog-generate.sh",
        "scripts/release-center/update-manifest.sh",
        "scripts/release-center/update-plan.sh",
        "scripts/release-center/rollback-migration-gate.sh",
        "scripts/release-center/github-release-draft.sh",
        "scripts/release-center/release-audit.sh",
        "scripts/release-center/release-dashboard-export.sh",
        "docs/release-center/RELEASE_AUTOMATION_UPDATE_CENTER_GUIDE.md",
        "docs/release-center/RELEASE_CHANNELS.md",
        "docs/release-center/UPDATE_MANIFEST.md",
        "docs/release-center/DRY_RUN_UPDATER.md",
        "docs/release-center/ROLLBACK_AND_MIGRATION_GATES.md",
        "docs/release-center/GITHUB_RELEASE_DRAFT.md",
        "docs/requirements/NEXT_V29_RELEASE_AUTOMATION_UPDATE_CENTER_REQUIREMENTS.md",
        "assets/release-center/release_automation_update_center_features.json",
    ]:
        assert (root / rel).exists(), rel
