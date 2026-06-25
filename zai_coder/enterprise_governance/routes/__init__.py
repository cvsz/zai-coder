"""Enterprise governance route registry."""

from __future__ import annotations

from zai_coder.enterprise_governance.policy_engine import policy_manifest, governance_gate
from zai_coder.enterprise_governance.role_matrix import role_matrix_manifest, role_allows
from zai_coder.enterprise_governance.compliance import compliance_checklist, compliance_summary
from zai_coder.enterprise_governance.evidence import collect_evidence, write_evidence_bundle
from zai_coder.enterprise_governance.change_approval import sample_change_request, change_approval_decision
from zai_coder.enterprise_governance.risk_register import risk_register, risk_summary
from zai_coder.enterprise_governance.data_retention import data_retention_policy, data_retention_checklist
from zai_coder.enterprise_governance.tenant_isolation import tenant_isolation_policy, tenant_isolation_check
from zai_coder.enterprise_governance.release_gate import release_readiness_gate, sample_release_status
from zai_coder.enterprise_governance.ui.pages import (
    render_governance_overview,
    render_policies_page,
    render_roles_page,
    render_risks_page,
    render_release_gate_page,
    render_compliance_page,
)


def route_governance_status() -> dict:
    return {
        "ok": True,
        "service": "zai-enterprise-governance",
        "systems": [
            "governance_policy_engine",
            "role_permission_matrix",
            "compliance_checklist",
            "audit_evidence_collector",
            "change_approval_workflow",
            "risk_register",
            "data_retention_policy",
            "tenant_isolation_policy",
            "security_review_dashboard",
            "release_readiness_gate",
        ],
    }


def route_policy_manifest() -> dict:
    return {"policies": policy_manifest()}


def route_governance_gate(payload: dict | None = None) -> dict:
    return governance_gate(payload or {})


def route_role_matrix() -> dict:
    return {"roles": role_matrix_manifest()}


def route_role_allows(role: str = "viewer", permission: str = "governance:view") -> dict:
    return {"role": role, "permission": permission, "allowed": role_allows(role, permission)}


def route_compliance_checklist() -> dict:
    return {"items": compliance_checklist()}


def route_compliance_summary(status: dict | None = None) -> dict:
    return compliance_summary(status or {})


def route_evidence_collect(root: str = ".") -> dict:
    return collect_evidence(root)


def route_evidence_bundle(root: str = ".") -> dict:
    return {"path": write_evidence_bundle(root)}


def route_change_approval() -> dict:
    return change_approval_decision(sample_change_request())


def route_risk_register() -> dict:
    return {"risks": risk_register(), "summary": risk_summary()}


def route_data_retention() -> dict:
    return {"policy": data_retention_policy(), "checklist": data_retention_checklist()}


def route_tenant_isolation(payload: dict | None = None) -> dict:
    return {"policy": tenant_isolation_policy(), "check": tenant_isolation_check(payload or {})}


def route_release_gate(status: dict | None = None) -> dict:
    return release_readiness_gate(status or sample_release_status())


def route_governance_page() -> dict:
    return {"content_type": "text/html", "html": render_governance_overview()}


def route_policies_page() -> dict:
    return {"content_type": "text/html", "html": render_policies_page()}


def route_roles_page() -> dict:
    return {"content_type": "text/html", "html": render_roles_page()}


def route_risks_page() -> dict:
    return {"content_type": "text/html", "html": render_risks_page()}


def route_release_gate_page() -> dict:
    return {"content_type": "text/html", "html": render_release_gate_page()}


def route_compliance_page() -> dict:
    return {"content_type": "text/html", "html": render_compliance_page()}
