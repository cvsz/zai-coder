from pathlib import Path
from zai_coder.package_registry_marketplace_publishing.models import RegistryPackage, MarketplaceSubmission, CompatibilityRecord, LicenseAttribution
from zai_coder.package_registry_marketplace_publishing.core import *
from zai_coder.package_registry_marketplace_publishing.routes import *

def test_models_validation():
    assert RegistryPackage("p","Name","bundle","v1.0.0","desc").validate() == []
    assert RegistryPackage("","","bad","1","secret token", visibility="bad", status="bad").validate()
    assert MarketplaceSubmission("s","p").validate() == []
    assert MarketplaceSubmission("","","bad", status="bad", dry_run=False).validate()
    assert CompatibilityRecord("c","p","runtime","v1").validate() == []
    assert CompatibilityRecord("","","","1", status="bad").validate()
    assert LicenseAttribution("l","p","MIT","attr").validate() == []
    assert LicenseAttribution("","","Bad","", review_status="bad").validate()

def test_core_registry_policy():
    assert package_catalog()
    assert compatibility_matrix()
    assert license_attribution_report()
    assert validation_report()["ok"]
    assert package_by_id("pkg-market-v42")["id"] == "pkg-market-v42"
    policy = package_validation_policy("pkg-market-v42")
    assert policy["allowed"]
    draft = marketplace_submission_draft("pkg-market-v42")
    assert draft["dry_run"] is True
    assert draft["external_publish"] is False
    checklist = publishing_checklist("pkg-market-v42")
    assert checklist["requires_review"] is True
    assert marketplace_export_bundle()["external_publish"] is False

def test_exports(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert Path(write_marketplace_export(tmp_path)).exists()
    assert Path(write_marketplace_report(tmp_path)).exists()
    demo = marketplace_demo(str(tmp_path))
    assert Path(demo["export_path"]).exists()
    assert Path(demo["report_path"]).exists()

def test_routes():
    assert route_marketplace_status()["ok"]
    assert route_marketplace_overview()["validation"]["ok"]
    assert route_package_catalog()["packages"]
    assert route_marketplace_submission()["dry_run"]
    assert route_publishing_checklist()["requires_review"]
    assert route_package_validation()["allowed"]
    assert route_compatibility_matrix()["compatibility"]
    assert route_license_attribution()["licenses"]
    assert "export_path" in route_marketplace_export()
    assert "export_path" in route_marketplace_demo()
    assert route_marketplace_page()["content_type"] == "text/html"
    assert route_marketplace_packages_page()["content_type"] == "text/html"
    assert route_marketplace_submissions_page()["content_type"] == "text/html"
    assert route_marketplace_validation_page()["content_type"] == "text/html"
    assert route_marketplace_checklist_page()["content_type"] == "text/html"

def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/package-registry/marketplace-status.sh",
        "scripts/package-registry/package-catalog.sh",
        "scripts/package-registry/marketplace-draft.sh",
        "scripts/package-registry/publishing-checklist.sh",
        "scripts/package-registry/package-validation.sh",
        "scripts/package-registry/compatibility-matrix.sh",
        "scripts/package-registry/license-attribution.sh",
        "scripts/package-registry/registry-export.sh",
        "scripts/package-registry/marketplace-demo.sh",
        "scripts/package-registry/marketplace-dashboard-export.sh",
        "docs/package-registry/PACKAGE_REGISTRY_MARKETPLACE_GUIDE.md",
        "docs/package-registry/PACKAGE_VALIDATION_POLICY.md",
        "docs/package-registry/MARKETPLACE_PUBLISHING_POLICY.md",
        "docs/package-registry/COMPATIBILITY_MATRIX.md",
        "docs/package-registry/LICENSE_ATTRIBUTION.md",
        "docs/requirements/NEXT_V42_PACKAGE_REGISTRY_MARKETPLACE_REQUIREMENTS.md",
        "assets/package-registry/package_registry_marketplace_features.json",
    ]:
        assert (root / rel).exists(), rel
