from pathlib import Path

from zai_coder.cloudflare_go_live.models import CloudflareGoLiveConfig
from zai_coder.cloudflare_go_live.hostname_validator import validate_hostname
from zai_coder.cloudflare_go_live.tunnel import render_tunnel_config, tunnel_install_plan
from zai_coder.cloudflare_go_live.access_policy import access_policy_checklist, access_policy_plan
from zai_coder.cloudflare_go_live.dns_planner import dns_record_plan, dns_rollback_plan
from zai_coder.cloudflare_go_live.exposure_scan import scan_text_for_exposure, exposure_scan_plan
from zai_coder.cloudflare_go_live.public_health import public_health_verification_plan
from zai_coder.cloudflare_go_live.go_live_wizard import go_live_wizard_plan
from zai_coder.cloudflare_go_live.ui.pages import render_go_live_page, render_access_page, render_dns_page, render_rollback_page, render_public_health_page
from zai_coder.cloudflare_go_live.routes import (
    route_cloudflare_status,
    route_hostname_validate,
    route_tunnel_plan,
    route_tunnel_config,
    route_access_checklist,
    route_access_plan,
    route_dns_plan,
    route_dns_rollback,
    route_exposure_scan,
    route_public_health_plan,
    route_go_live_wizard,
    route_go_live_page,
    route_access_page,
    route_dns_page,
    route_rollback_page,
    route_public_health_page,
)


def test_config_and_hostname_validation():
    cfg = CloudflareGoLiveConfig(hostname="zai.zeaz.dev", zone_name="zeaz.dev")
    assert cfg.validate() == []
    assert validate_hostname("zai.zeaz.dev")["ok"] is True
    assert validate_hostname("*.zeaz.dev")["ok"] is False
    assert validate_hostname("bad")["ok"] is False
    assert CloudflareGoLiveConfig(local_service_url="http://0.0.0.0:8765").validate()


def test_tunnel_plan_and_config():
    cfg = CloudflareGoLiveConfig(hostname="zai.zeaz.dev", tunnel_name="zai-coder")
    rendered = render_tunnel_config(cfg)
    assert "zai.zeaz.dev" in rendered
    assert "http://127.0.0.1:8765" in rendered
    plan = tunnel_install_plan(cfg)
    assert plan.dry_run is True
    assert "cloudflared tunnel create zai-coder" in plan.commands


def test_access_dns_public_health_plans():
    cfg = CloudflareGoLiveConfig(hostname="zai.zeaz.dev", tunnel_name="zai-coder")
    checklist = access_policy_checklist(cfg)
    assert any(item["required"] for item in checklist)
    assert access_policy_plan(cfg).dry_run is True
    dns = dns_record_plan(cfg)
    assert dns.dry_run is True
    assert "cfargotunnel.com" in list(dns.files.values())[0]
    rollback = dns_rollback_plan(cfg)
    assert rollback.dry_run is True
    public = public_health_verification_plan(cfg)
    assert public.dry_run is True
    assert any("api/status" in cmd for cmd in public.commands)


def test_exposure_scan():
    assert scan_text_for_exposure("--host 0.0.0.0")
    report = exposure_scan_plan(Path(__file__).resolve().parents[1])
    assert report["dry_run"] is True
    assert "Dockerfile.production" in report["checks"]


def test_go_live_wizard():
    cfg = CloudflareGoLiveConfig(hostname="zai.zeaz.dev", tunnel_name="zai-coder")
    plan = go_live_wizard_plan(cfg)
    assert plan.dry_run is True
    assert "validate hostname" in plan.steps
    assert "make cloudflare-dns-rollback-plan" in plan.commands


def test_ui_pages_render():
    cfg = CloudflareGoLiveConfig(hostname="zai.zeaz.dev")
    assert "Cloudflare Go-Live" in render_go_live_page(cfg)
    assert "Access Checklist" in render_access_page(cfg)
    assert "DNS Plan" in render_dns_page(cfg)
    assert "Rollback Plan" in render_rollback_page(cfg)
    assert "Public Health Verification" in render_public_health_page(cfg)


def test_routes():
    payload = {"hostname": "zai.zeaz.dev", "tunnel_name": "zai-coder", "zone_name": "zeaz.dev"}
    assert route_cloudflare_status()["ok"] is True
    assert route_hostname_validate(payload)["ok"] is True
    assert route_tunnel_plan(payload)["dry_run"] is True
    assert route_tunnel_config(payload)["content_type"] == "text/yaml"
    assert route_access_checklist(payload)["items"]
    assert route_access_plan(payload)["dry_run"] is True
    assert route_dns_plan(payload)["dry_run"] is True
    assert route_dns_rollback(payload)["dry_run"] is True
    assert route_exposure_scan(".")["dry_run"] is True
    assert route_public_health_plan(payload)["dry_run"] is True
    assert route_go_live_wizard(payload)["dry_run"] is True
    assert route_go_live_page(payload)["content_type"] == "text/html"
    assert route_access_page(payload)["content_type"] == "text/html"
    assert route_dns_page(payload)["content_type"] == "text/html"
    assert route_rollback_page(payload)["content_type"] == "text/html"
    assert route_public_health_page(payload)["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/cloudflare/hostname-validate.sh",
        "scripts/cloudflare/tunnel-plan.sh",
        "scripts/cloudflare/access-checklist.sh",
        "scripts/cloudflare/dns-plan.sh",
        "scripts/cloudflare/exposure-scan.sh",
        "scripts/cloudflare/public-health-plan.sh",
        "scripts/cloudflare/dns-rollback-plan.sh",
        "scripts/cloudflare/go-live-wizard.sh",
        "docs/cloudflare/CLOUDFLARE_GO_LIVE_GUIDE.md",
        "docs/cloudflare/CLOUDFLARE_ACCESS_CHECKLIST.md",
        "docs/cloudflare/CLOUDFLARE_DNS_ROLLBACK.md",
        "docs/cloudflare/PUBLIC_HEALTH_VERIFICATION.md",
        "docs/requirements/NEXT_V16_CLOUDFLARE_GO_LIVE_REQUIREMENTS.md",
        "assets/cloudflare/cloudflare_go_live_features.json",
    ]:
        assert (root / rel).exists(), rel
