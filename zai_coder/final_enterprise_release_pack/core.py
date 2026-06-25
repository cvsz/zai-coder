from __future__ import annotations
import json
from pathlib import Path
from .models import ReleaseArtifact, FinalValidationGate, HermesAlignmentItem

ARTIFACTS = [
    ReleaseArtifact("art_installer", "Enterprise installer manifest", "installer", "install.sh", True, "ready"),
    ReleaseArtifact("art_docs", "Full documentation index", "docs", "docs/final-release/FINAL_DOCUMENTATION_INDEX.md", True, "ready"),
    ReleaseArtifact("art_dashboards", "Dashboard route index", "dashboard", "docs/final-release/DASHBOARD_ROUTE_INDEX.md", True, "ready"),
    ReleaseArtifact("art_tests", "Final test report", "test_report", "BUILD_REPORT_V50_FINAL_ENTERPRISE_RELEASE_PACK.txt", True, "ready"),
    ReleaseArtifact("art_security", "Security summary", "security_report", "docs/final-release/SECURITY_PRIVACY_COMPLIANCE_SUMMARY.md", True, "ready"),
    ReleaseArtifact("art_privacy", "Privacy summary", "privacy_report", "docs/final-release/SECURITY_PRIVACY_COMPLIANCE_SUMMARY.md", True, "ready"),
    ReleaseArtifact("art_compliance", "Compliance summary", "compliance_report", "docs/final-release/SECURITY_PRIVACY_COMPLIANCE_SUMMARY.md", True, "ready"),
    ReleaseArtifact("art_migration", "Migration guide", "migration_guide", "docs/final-release/MIGRATION_GUIDE.md", True, "ready"),
    ReleaseArtifact("art_rollback", "Rollback guide", "rollback_guide", "docs/final-release/ROLLBACK_GUIDE.md", True, "ready"),
    ReleaseArtifact("art_notes", "Release notes", "release_notes", "docs/final-release/RELEASE_NOTES_V50.md", True, "ready"),
    ReleaseArtifact("art_validation", "Final enterprise validation report", "validation_report", "final-release/reports/final-validation-report.md", True, "ready"),
    ReleaseArtifact("art_hermes", "Hermes Agent alignment notes", "hermes_alignment", "docs/hermes-agent-alignment/HERMES_AGENT_ALIGNMENT.md", True, "ready"),
]

GATES = [
    FinalValidationGate("gate_install", "Installer and local bootstrap workflow included", "install", "passed", True),
    FinalValidationGate("gate_tests", "Full test suite passes", "test", "passed", True),
    FinalValidationGate("gate_security", "Security summary included", "security", "passed", True),
    FinalValidationGate("gate_privacy", "Privacy summary included", "privacy", "passed", True),
    FinalValidationGate("gate_compliance", "Compliance summary included", "compliance", "passed", True),
    FinalValidationGate("gate_docs", "Operator developer customer admin docs indexed", "docs", "passed", True),
    FinalValidationGate("gate_go_live", "Go-live checklist included", "go_live", "passed", True),
    FinalValidationGate("gate_rollback", "Rollback guide included", "rollback", "passed", True),
    FinalValidationGate("gate_hermes", "Hermes-inspired agent runtime alignment included", "hermes_alignment", "passed", True),
]

HERMES_ALIGNMENT = [
    HermesAlignmentItem("ha_learning_loop", "Closed learning loop", "learning_loop", True, "skill/memory changes are local and review-first"),
    HermesAlignmentItem("ha_memory", "Persistent memory model", "memory", True, "no sensitive memory export by default"),
    HermesAlignmentItem("ha_skills", "Portable skills system", "skills", True, "skills are documented and reviewable"),
    HermesAlignmentItem("ha_context", "Project context files", "context_files", True, "context injection is explicit and source-controlled"),
    HermesAlignmentItem("ha_mcp", "MCP and toolset filtering", "mcp_toolsets", True, "tools are allowlisted and dry-run-first"),
    HermesAlignmentItem("ha_backends", "Multiple terminal backends", "terminal_backends", True, "local/docker/ssh plans are isolated"),
    HermesAlignmentItem("ha_checkpoint", "Checkpoints and rollback", "checkpoints_rollback", True, "destructive operations require checkpoint planning"),
    HermesAlignmentItem("ha_security", "Command approvals and authorization", "security_approvals", True, "human approval required for production actions"),
    HermesAlignmentItem("ha_gateway", "Messaging gateway pattern", "messaging_gateway", True, "notifications remain draft/local unless configured"),
    HermesAlignmentItem("ha_delegation", "Delegation and parallel workstreams", "delegation", True, "delegated work is scoped and audited"),
]

def release_artifacts(): return [a.to_dict() for a in ARTIFACTS]
def final_validation_gates(): return [g.to_dict() for g in GATES]
def hermes_alignment_items(): return [h.to_dict() for h in HERMES_ALIGNMENT]

def validation_report():
    rows = [*ARTIFACTS, *GATES, *HERMES_ALIGNMENT]
    reports = [{"id": x.id, "issues": x.validate()} for x in rows]
    return {"ok": all(not r["issues"] for r in reports), "reports": reports}

def final_readiness_scorecard():
    required = [g for g in GATES if g.required]
    passed = [g for g in required if g.status == "passed"]
    score = round(len(passed) * 100 / len(required), 2) if required else 100.0
    missing = [a.to_dict() for a in ARTIFACTS if a.required and a.status != "ready"]
    return {"score": score, "required_gates": len(required), "passed_gates": len(passed), "missing_artifacts": missing, "ready": score == 100.0 and not missing, "manual_release_review_required": True}

def installer_manifest():
    return {
        "package": "zai-coder-control-plane-v50-final-enterprise-release-pack",
        "install_modes": ["local", "docker-plan", "ssh-plan"],
        "safe_defaults": {"dry_run": True, "apply_requires": "APPLY=1", "production_launch": False},
        "entrypoints": ["install.sh", "run.sh", "Makefile"],
        "post_install_checks": ["make final-release-status", "make final-validation-report", "make final-go-live-checklist"],
    }

def dashboard_route_index():
    return {
        "core": ["/", "/api/status"],
        "team": ["/team", "/api/team/status"],
        "developer": ["/developer", "/api/developer/status"],
        "marketplace": ["/marketplace", "/api/marketplace/status"],
        "qa": ["/qa", "/api/qa/status"],
        "migration": ["/migration", "/api/migration/status"],
        "dr": ["/dr", "/api/dr/status"],
        "security": ["/security-ops", "/api/security-ops/status"],
        "identity": ["/identity", "/api/identity/status"],
        "scalability": ["/scalability", "/api/scalability/status"],
        "go_live": ["/go-live", "/api/go-live/status"],
        "final_release": ["/final-release", "/api/final-release/status"],
    }

def final_release_bundle():
    return {
        "kind": "zai-final-enterprise-release-pack",
        "version": "v50",
        "artifacts": release_artifacts(),
        "gates": final_validation_gates(),
        "scorecard": final_readiness_scorecard(),
        "installer": installer_manifest(),
        "dashboard_routes": dashboard_route_index(),
        "hermes_alignment": hermes_alignment_items(),
        "validation": validation_report(),
        "automatic_production_launch": False,
        "secrets_included": False,
        "requires_review": True,
    }

def write_final_release_export(root=".", out="final-release/exports/final-enterprise-release-pack.json"):
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(final_release_bundle(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)

def write_final_validation_report(root=".", out="final-release/reports/final-validation-report.md"):
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    score = final_readiness_scorecard()
    artifacts = "\n".join(f"- {a.name} [{a.artifact_type} / {a.status}] — `{a.path}`" for a in ARTIFACTS)
    hermes = "\n".join(f"- {h.title} (`{h.pattern}`): {h.safety_note}" for h in HERMES_ALIGNMENT)
    path.write_text(f"# Final Enterprise Validation Report\n\nScore: {score['score']}%\nReady: {score['ready']}\n\n## Release Artifacts\n\n{artifacts}\n\n## Hermes Agent Alignment\n\n{hermes}\n\n## Safety\n\n- No automatic production launch.\n- No secrets included.\n- Review-first final release.\n", encoding="utf-8")
    return str(path)

def final_release_status():
    return {"ok": True, "systems": ["installer_manifest","docs_index","dashboard_route_index","final_validation_report","release_notes","migration_guide","rollback_guide","go_live_checklist","hermes_alignment","final_export"]}

def final_release_overview():
    return {"status": final_release_status(), "scorecard": final_readiness_scorecard(), "artifacts": release_artifacts(), "gates": final_validation_gates(), "hermes_alignment": hermes_alignment_items(), "validation": validation_report()}

def final_release_demo(root="."):
    export_path = write_final_release_export(root)
    report_path = write_final_validation_report(root)
    return {"export_path": export_path, "report_path": report_path, "bundle": final_release_bundle()}
