"""Release Automation and Update Center route registry."""

from __future__ import annotations

from zai_coder.release_automation_update_center.control import release_center_status, release_plan_demo, update_manifest_demo, update_plan_demo, rollback_migration_demo, release_audit_demo
from zai_coder.release_automation_update_center.channels import release_channel_manifest, channel_policy
from zai_coder.release_automation_update_center.versioning import version_plan
from zai_coder.release_automation_update_center.changelog import default_changelog
from zai_coder.release_automation_update_center.update_manifest import update_manifest_schema
from zai_coder.release_automation_update_center.github_release import github_release_draft, github_release_command_plan
from zai_coder.release_automation_update_center.audit import ReleaseAuditLog
from zai_coder.release_automation_update_center.ui.pages import render_release_overview, render_release_plan_page, render_update_page, render_channels_page


def route_release_center_status() -> dict:
    return {
        "ok": True,
        "service": "zai-release-automation-update-center",
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


def route_release_channels() -> dict:
    return {"channels": release_channel_manifest()}


def route_release_channel_policy(channel: str = "stable") -> dict:
    return channel_policy(channel)


def route_version_plan(current: str = "v28.0.0", bump: str = "minor", channel: str = "stable") -> dict:
    return version_plan(current, bump, channel)


def route_release_plan_demo() -> dict:
    return release_plan_demo()


def route_changelog_demo() -> dict:
    return {"markdown": default_changelog("v29.0.0")}


def route_update_manifest_demo() -> dict:
    return update_manifest_demo(".")


def route_update_manifest_schema() -> dict:
    return update_manifest_schema()


def route_update_plan_demo() -> dict:
    return update_plan_demo(".")


def route_rollback_migration_demo() -> dict:
    return rollback_migration_demo()


def route_github_release_draft() -> dict:
    return github_release_draft("v29.0.0")


def route_github_release_command_plan() -> dict:
    return github_release_command_plan("v29.0.0")


def route_release_audit_demo() -> dict:
    return release_audit_demo()


def route_release_audit() -> dict:
    return {"events": ReleaseAuditLog().list_events()}


def route_release_center_page() -> dict:
    return {"content_type": "text/html", "html": render_release_overview()}


def route_release_plan_page() -> dict:
    return {"content_type": "text/html", "html": render_release_plan_page()}


def route_update_center_page() -> dict:
    return {"content_type": "text/html", "html": render_update_page()}


def route_release_channels_page() -> dict:
    return {"content_type": "text/html", "html": render_channels_page()}
