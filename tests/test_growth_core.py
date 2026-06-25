import tempfile
from pathlib import Path

from zai_coder.members.service import MemberService
from zai_coder.members.roles import has_permission
from zai_coder.update_system.manager import UpdateManager
from zai_coder.update_system.manifest import UpdateManifest
from zai_coder.core_system.feature_registry import default_growth_registry
from zai_coder.marketing_shared.campaigns import Campaign, validate_campaign
from zai_coder.marketing_shared.assets import is_allowed_asset
from zai_coder.social_media_core.composer import SocialPost, validate_post, compose_variants
from zai_coder.social_media_core.scheduler import SocialScheduler


def test_members_roles_and_permissions():
    with tempfile.TemporaryDirectory() as td:
        svc = MemberService(Path(td) / "members.db")
        svc.add_member("dev@example.com", "Dev", ["developer"])
        assert svc.can("dev@example.com", "agents:run")
        assert not svc.can("dev@example.com", "members:write")


def test_role_wildcard_permission():
    assert has_permission(["marketer"], "social:write")
    assert has_permission(["marketer"], "marketing:campaign")


def test_update_system_blocks_unsafe_paths():
    with tempfile.TemporaryDirectory() as td:
        mgr = UpdateManager(td)
        manifest = UpdateManifest(
            version="1.0.1",
            files=["zai_coder/core.py", "../secret", "apps/zlms/nope.py", ".env"],
        )
        plan = mgr.plan(manifest)
        assert plan.warnings
        assert any("unsafe path" in w for w in plan.warnings)
        assert any("apps/zlms" in w for w in plan.warnings)


def test_feature_registry_contains_growth_core():
    reg = default_growth_registry()
    slugs = {f.slug for f in reg.list()}
    assert "members-system" in slugs
    assert "social-media-core" in slugs


def test_campaign_validation():
    campaign = Campaign(
        slug="launch",
        name="Launch",
        objective="Announce ZAI Coder",
        audience="developers",
        channels=["linkedin", "x"],
    )
    assert validate_campaign(campaign) == []


def test_asset_validation_blocks_bad_paths():
    assert is_allowed_asset("assets/post.svg")
    assert not is_allowed_asset("../secret.txt")
    assert not is_allowed_asset("apps/zlms/file.md")


def test_social_post_validation_and_variants():
    posts = compose_variants("Hello ZAI Coder", ["x", "linkedin"])
    assert len(posts) == 2
    assert validate_post(posts[0]) == []


def test_social_scheduler_dry_run_default():
    with tempfile.TemporaryDirectory() as td:
        scheduler = SocialScheduler(Path(td) / "social.db")
        result = scheduler.schedule(SocialPost(platform="x", text="Hello"), "2026-07-01T09:00:00Z")
        assert result["dry_run"] is True
        assert scheduler.list_posts() == []
