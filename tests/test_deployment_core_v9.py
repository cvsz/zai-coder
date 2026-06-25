import tempfile
from pathlib import Path
import tarfile
import zipfile

from zai_coder.deployment_core.health import run_deployment_health, health_summary
from zai_coder.deployment_core.auth_middleware import authorize_request, is_local_host
from zai_coder.deployment_core.backup_restore import create_backup, restore_backup
from zai_coder.deployment_core.admin_bootstrap import bootstrap_admin
from zai_coder.deployment_core.cloudflare_config import CloudflareTunnelConfig
from zai_coder.deployment_core.checksums import sha256_file, build_checksum_manifest
from zai_coder.deployment_core.sbom import generate_minimal_sbom
from zai_coder.deployment_core.release_builder import build_release_zip
from zai_coder.deployment_core.server.app import ZaiAppStudioHandler


def test_health_summary():
    results = run_deployment_health(".")
    summary = health_summary(results)
    assert "checks" in summary


def test_auth_middleware_localhost_and_api_key():
    assert is_local_host("127.0.0.1")
    assert authorize_request("127.0.0.1", "127.0.0.1").allowed
    assert not authorize_request("192.168.1.5", "0.0.0.0").allowed

    class Rec:
        name = "admin"

    assert authorize_request("192.168.1.5", "0.0.0.0", "key", verify_key=lambda k: Rec()).allowed


def test_backup_plan_and_create_restore():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "project"
        root.mkdir()
        (root / "README.md").write_text("hello", encoding="utf-8")
        (root / ".env").write_text("SECRET=1", encoding="utf-8")
        plan = create_backup(root, Path(td) / "backups", apply=False)
        assert plan.dry_run is True
        assert "README.md" in plan.files

        created = create_backup(root, Path(td) / "backups", apply=True)
        assert Path(created.archive_path).exists()

        target = Path(td) / "restore"
        target.mkdir()
        restored = restore_backup(created.archive_path, target, apply=False)
        assert restored["dry_run"] is True


def test_admin_bootstrap_dry_run_and_apply():
    with tempfile.TemporaryDirectory() as td:
        dry = bootstrap_admin(Path(td) / "app.db", "admin@example.com", apply=False)
        assert dry.dry_run is True
        real = bootstrap_admin(Path(td) / "app.db", "admin@example.com", apply=True)
        assert real.raw_api_key.startswith("zai_")


def test_cloudflare_config_generation():
    cfg = CloudflareTunnelConfig("zai-coder", "zai.zeaz.dev")
    rendered = cfg.render_yaml()
    assert "zai.zeaz.dev" in rendered
    assert "http://127.0.0.1:8765" in rendered


def test_checksums_and_sbom():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "artifact.zip"
        p.write_text("abc", encoding="utf-8")
        assert sha256_file(p)
        manifest = build_checksum_manifest(td)
        assert "artifact.zip" in manifest
        sbom = generate_minimal_sbom(td)
        assert sbom["format"] == "zai-minimal-sbom-v1"


def test_release_builder_dry_run_and_apply():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "project"
        root.mkdir()
        (root / "README.md").write_text("hello", encoding="utf-8")
        (root / "apps").mkdir()
        (root / "apps" / "zlms").mkdir()
        (root / "apps" / "zlms" / "ignore.md").write_text("ignore", encoding="utf-8")
        plan = build_release_zip(root, Path(td) / "release", "demo", apply=False)
        assert plan.dry_run is True
        real = build_release_zip(root, Path(td) / "release", "demo", apply=True)
        assert Path(real.path).exists()
        with zipfile.ZipFile(real.path) as z:
            names = set(z.namelist())
        assert "README.md" in names
        assert "apps/zlms/ignore.md" not in names


def test_deploy_files_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "deploy/systemd/zai-coder-production.service").exists()
    assert (root / "deploy/logrotate/zai-coder").exists()
    assert (root / "deploy/docker/docker-compose.production.yml").exists()
    assert (root / "deploy/cloudflare/generated-tunnel.example.yml").exists()
    assert (root / "scripts/deploy/serve-local.sh").exists()
    assert (root / "scripts/release/build-release-safe.sh").exists()
