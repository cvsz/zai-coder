from zai_coder.integration_core.registry import list_integrations, get_integration
from zai_coder.integration_core.models import ensure_dry_run
from zai_coder.integration_core.adapters.github_adapter import is_safe_repo_path, exact_path_publish_plan, repo_status_plan
from zai_coder.integration_core.adapters.cloudflare_adapter import CloudflareDnsRecord, dns_plan, tunnel_validate_plan
from zai_coder.integration_core.adapters.docker_adapter import docker_status_plan, safe_cleanup_plan
from zai_coder.integration_core.adapters.huggingface_adapter import model_publish_plan, dataset_upload_plan, space_scaffold_plan, model_card
from zai_coder.integration_core.adapters.social_drafts import create_social_drafts
from zai_coder.integration_core.adapters.storage_backends import local_storage_plan, object_storage_upload_plan, StorageConfig
from zai_coder.integration_core.adapters.notifications import email_draft, slack_payload_draft, discord_payload_draft, telegram_payload_draft
from zai_coder.integration_core.openapi import build_openapi_schema, export_openapi_json
from zai_coder.integration_core.routes import (
    route_integrations,
    route_github_status,
    route_github_publish,
    route_cloudflare_tunnel,
    route_docker_status,
    route_huggingface_plan,
    route_social_drafts,
    route_storage_plan,
    route_notification,
    route_openapi,
)


def test_registry():
    providers = list_integrations()
    slugs = {p["slug"] for p in providers}
    assert "github" in slugs
    assert get_integration("docker").name == "Docker"


def test_github_adapter_safety():
    assert is_safe_repo_path("README.md")
    assert not is_safe_repo_path("apps/zlms/nope.md")
    assert not is_safe_repo_path("../secret")
    plan = exact_path_publish_plan(["README.md", "apps/zlms/nope.md"])
    assert plan.dry_run is True
    assert "README.md" in plan.payload["safe_paths"]
    assert plan.payload["blocked_paths"] == ["apps/zlms/nope.md"]
    assert all("git add ." not in cmd for cmd in plan.commands)


def test_cloudflare_adapter():
    record = CloudflareDnsRecord("zai.zeaz.dev", "CNAME", "tunnel.example.com")
    plan = dns_plan([record])
    assert plan.dry_run is True
    assert plan.warnings == []
    assert tunnel_validate_plan().provider == "cloudflare"


def test_docker_adapter_blocks_volume_delete():
    plan = safe_cleanup_plan()
    assert all("--volumes" not in cmd for cmd in plan.commands)
    assert docker_status_plan().provider == "docker"


def test_huggingface_adapter():
    assert "# cvsz/demo" in model_card("cvsz/demo")
    assert model_publish_plan("cvsz/demo").dry_run is True
    assert dataset_upload_plan("cvsz/ds").dry_run is True
    assert "app.py" in space_scaffold_plan("cvsz/space").files


def test_social_storage_notifications():
    social = create_social_drafts("Title", "Body")
    assert len(social.payload["drafts"]) == 6
    assert local_storage_plan("storage").dry_run is True
    r2 = object_storage_upload_plan(StorageConfig("r2", bucket="b", endpoint_url="https://r2.example"), "a.zip", "a.zip")
    assert "--endpoint-url" in r2.commands[-1]
    assert email_draft("a@example.com", "S", "B").dry_run is True
    assert "slack-payload.json" in slack_payload_draft("#ops", "hello").files
    assert "discord-payload.json" in discord_payload_draft("hello").files
    assert "telegram-payload.json" in telegram_payload_draft("123", "hello").files


def test_openapi_schema():
    schema = build_openapi_schema()
    assert schema["openapi"] == "3.1.0"
    assert "/api/integrations" in schema["paths"]
    assert "ZAI Coder Integration Core API" in export_openapi_json()


def test_routes():
    assert "integrations" in route_integrations()
    assert route_github_status()["provider"] == "github"
    assert route_github_publish({"paths": ["README.md"], "branch": "main"})["provider"] == "github"
    assert route_cloudflare_tunnel()["provider"] == "cloudflare"
    assert route_docker_status()["provider"] == "docker"
    assert route_huggingface_plan({"kind": "space", "repo_id": "cvsz/space"})["provider"] == "huggingface"
    assert route_social_drafts({"title": "T", "body": "B"})["provider"] == "social"
    assert route_storage_plan({"backend": "local", "path": "storage"})["provider"] == "storage"
    assert route_notification({"kind": "slack", "channel": "#ops", "text": "hi"})["provider"] == "notifications"
    assert route_openapi()["openapi"] == "3.1.0"


def test_all_plans_dry_run():
    plans = [
        repo_status_plan(),
        exact_path_publish_plan(["README.md"]),
        tunnel_validate_plan(),
        docker_status_plan(),
        model_publish_plan("cvsz/demo"),
        create_social_drafts("T", "B"),
        local_storage_plan("storage"),
        email_draft("a@example.com", "s", "b"),
    ]
    for plan in plans:
        ensure_dry_run(plan)
