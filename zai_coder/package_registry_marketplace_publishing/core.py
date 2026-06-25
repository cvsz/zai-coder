from __future__ import annotations
import json, uuid
from pathlib import Path
from .models import RegistryPackage, MarketplaceSubmission, CompatibilityRecord, LicenseAttribution

PACKAGES = [
    RegistryPackage("pkg-team-v40", "Team Collaboration and Workspaces", "bundle", "v40.0.0", "Team workspace registry, review queues, and local collaboration workflows.", "MIT", "workspace", "approved"),
    RegistryPackage("pkg-dev-v41", "Developer Portal and API Docs", "bundle", "v41.0.0", "Developer portal, API reference, OpenAPI export, and SDK snippets.", "MIT", "workspace", "approved"),
    RegistryPackage("pkg-market-v42", "Package Registry and Marketplace Publishing", "bundle", "v42.0.0", "Internal package registry and draft-only marketplace publishing workflows.", "MIT", "private", "review"),
    RegistryPackage("pkg-help-center", "Knowledge Base and Help Center", "plugin", "v37.0.0", "Local help center and support deflection suggestions.", "MIT", "workspace", "approved"),
]

COMPATIBILITY = [
    CompatibilityRecord("compat-team", "pkg-team-v40", "zai-control-plane", "v40.0.0", "", "compatible"),
    CompatibilityRecord("compat-dev", "pkg-dev-v41", "zai-control-plane", "v41.0.0", "", "compatible"),
    CompatibilityRecord("compat-market", "pkg-market-v42", "zai-control-plane", "v42.0.0", "", "needs_review"),
]

LICENSES = [
    LicenseAttribution("lic-team", "pkg-team-v40", "MIT", "Generated local-first ZAI package.", "approved"),
    LicenseAttribution("lic-dev", "pkg-dev-v41", "MIT", "Generated local-first ZAI package.", "approved"),
    LicenseAttribution("lic-market", "pkg-market-v42", "MIT", "Generated local-first ZAI package.", "pending"),
]

def package_catalog(): return [p.to_dict() for p in PACKAGES]
def compatibility_matrix(): return [c.to_dict() for c in COMPATIBILITY]
def license_attribution_report(): return [l.to_dict() for l in LICENSES]

def validation_report() -> dict:
    rows = [*PACKAGES, *COMPATIBILITY, *LICENSES]
    reports = [{"id": x.id, "issues": x.validate()} for x in rows]
    return {"ok": all(not r["issues"] for r in reports), "reports": reports}

def package_by_id(package_id: str) -> dict:
    for pkg in PACKAGES:
        if pkg.id == package_id:
            return pkg.to_dict()
    raise ValueError(f"unknown package: {package_id}")

def package_validation_policy(package_id: str) -> dict:
    pkg = package_by_id(package_id)
    related_compat = [c for c in compatibility_matrix() if c["package_id"] == package_id]
    related_license = [l for l in license_attribution_report() if l["package_id"] == package_id]
    blocked = []
    if pkg["status"] not in {"approved","review"}: blocked.append("package must be in review or approved state")
    if not related_compat: blocked.append("missing compatibility record")
    if not related_license: blocked.append("missing license attribution")
    if any(item["status"] == "blocked" for item in related_compat): blocked.append("compatibility blocked")
    if any(item["review_status"] == "blocked" for item in related_license): blocked.append("license review blocked")
    return {"allowed": not blocked, "blocked": blocked, "package": pkg, "compatibility": related_compat, "licenses": related_license}

def marketplace_submission_draft(package_id: str, target: str = "internal-marketplace") -> dict:
    policy = package_validation_policy(package_id)
    submission = MarketplaceSubmission(f"sub_{uuid.uuid4().hex[:12]}", package_id, target, "draft", "Draft-only submission. No external publishing.", True)
    blocked = list(policy["blocked"]) + submission.validate()
    return {"dry_run": True, "allowed": not blocked, "blocked": blocked, "submission": submission.to_dict(), "policy": policy, "external_publish": False}

def publishing_checklist(package_id: str) -> dict:
    return {
        "package_id": package_id,
        "items": [
            {"id":"metadata", "title":"Metadata reviewed", "done": True},
            {"id":"compatibility", "title":"Compatibility matrix reviewed", "done": bool([c for c in compatibility_matrix() if c["package_id"] == package_id])},
            {"id":"license", "title":"License and attribution reviewed", "done": bool([l for l in license_attribution_report() if l["package_id"] == package_id])},
            {"id":"security", "title":"No secrets in package metadata", "done": True},
            {"id":"approval", "title":"Human review before publishing", "done": False},
        ],
        "external_publish": False,
        "requires_review": True,
    }

def marketplace_export_bundle() -> dict:
    return {
        "kind": "zai-package-registry-marketplace-export",
        "version": "1.0",
        "packages": package_catalog(),
        "compatibility": compatibility_matrix(),
        "licenses": license_attribution_report(),
        "validation": validation_report(),
        "draft_submission": marketplace_submission_draft("pkg-market-v42"),
        "checklist": publishing_checklist("pkg-market-v42"),
        "external_publish": False,
        "requires_review": True,
    }

def write_marketplace_export(root=".", out="marketplace/exports/marketplace-export.json") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(marketplace_export_bundle(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)

def write_marketplace_report(root=".", out="marketplace/reports/marketplace-report.md") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    packages = "\n".join(f"- {p.name} [{p.package_type} / {p.version} / {p.status}]" for p in PACKAGES)
    path.write_text(f"# Package Registry and Marketplace Publishing Report\n\n## Packages\n\n{packages}\n\n## Safety\n\n- Draft-only marketplace submissions.\n- No external publishing.\n- License and attribution review required.\n", encoding="utf-8")
    return str(path)

def marketplace_status():
    return {"ok": True, "systems": ["package_registry","marketplace_submission_drafts","publishing_checklist","compatibility_matrix","license_attribution","marketplace_exports","dashboard_routes"]}

def marketplace_overview():
    return {"status": marketplace_status(), "packages": package_catalog(), "validation": validation_report(), "compatibility": compatibility_matrix(), "licenses": license_attribution_report()}

def marketplace_demo(root="."):
    export_path = write_marketplace_export(root)
    report_path = write_marketplace_report(root)
    return {"export_path": export_path, "report_path": report_path, "bundle": marketplace_export_bundle()}
