from __future__ import annotations
import json
from pathlib import Path
from .models import IdentityProviderPlan, ScimMapping, OrgPolicy, AccessReviewItem

PROVIDERS = [
    IdentityProviderPlan("idp_oidc_demo", "Generic OIDC Demo Provider", "generic_oidc", "oidc", "review", True),
    IdentityProviderPlan("idp_saml_demo", "SAML Demo Provider", "saml", "saml", "draft", True),
    IdentityProviderPlan("idp_workspace", "Workspace Identity Provider Plan", "google_workspace", "oidc", "draft", True),
]

SCIM_MAPPINGS = [
    ScimMapping("scim_user_name", "userName", "username", "copy", "approved"),
    ScimMapping("scim_email", "emails.primary.value", "email_hash", "redact", "review"),
    ScimMapping("scim_display", "displayName", "display_name", "copy", "approved"),
    ScimMapping("scim_role", "groups", "roles", "normalize", "review"),
]

ORG_POLICIES = [
    OrgPolicy("pol_mfa", "MFA required for admins", "mfa", "manual_approval", "review"),
    OrgPolicy("pol_session", "Session review policy", "session", "report_only", "draft"),
    OrgPolicy("pol_access", "Quarterly access review", "access_review", "review", "approved"),
    OrgPolicy("pol_jml", "Joiner mover leaver process", "joiner_mover_leaver", "manual_approval", "review"),
]

ACCESS_REVIEWS = [
    AccessReviewItem("ar_owner", "usr_owner", "tw_control", "owner", "pending", "critical"),
    AccessReviewItem("ar_admin", "usr_admin", "tw_control", "admin", "pending", "high"),
    AccessReviewItem("ar_reviewer", "usr_reviewer", "tw_release", "reviewer", "approved", "normal"),
    AccessReviewItem("ar_auditor", "usr_auditor", "audit-reports", "auditor", "pending", "normal"),
]

def get_real_system_users():
    import pwd
    users = []
    try:
        all_users = pwd.getpwall()
        for idx, u in enumerate(all_users):
            # Only track a subset so it doesn't overwhelm the queue, filter by UID >= 1000 for humans, < 1000 for system
            uid = u.pw_uid
            risk = "normal"
            if uid == 0:
                risk = "critical"
            elif uid < 1000:
                risk = "high"
                
            users.append({
                "id": f"ar_sys_{uid}_{idx}",
                "subject_ref": f"usr_{u.pw_name}",
                "resource": "local_system_access",
                "role": "root" if uid == 0 else "service" if uid < 1000 else "user",
                "decision": "pending",
                "risk": risk
            })
            if len(users) >= 20:  # limit payload
                break
    except Exception:
        pass
    return users

def identity_provider_plans(): return [p.to_dict() for p in PROVIDERS]
def scim_mapping_drafts(): return [m.to_dict() for m in SCIM_MAPPINGS]
def org_policy_registry(): return [p.to_dict() for p in ORG_POLICIES]

def access_review_queue(execute: bool = False):
    reviews = [r.to_dict() for r in ACCESS_REVIEWS]
    if execute:
        sys_users = get_real_system_users()
        if sys_users:
            reviews.extend(sys_users)
    return reviews

def validation_report() -> dict:
    rows = [*PROVIDERS, *SCIM_MAPPINGS, *ORG_POLICIES, *ACCESS_REVIEWS]
    reports = [{"id": x.id, "issues": x.validate()} for x in rows]
    return {"ok": all(not r["issues"] for r in reports), "reports": reports}

def sso_config_plan(provider_id="idp_oidc_demo") -> dict:
    provider = next((p for p in PROVIDERS if p.id == provider_id), None)
    if not provider: raise ValueError(f"unknown provider: {provider_id}")
    return {
        "dry_run": True,
        "provider": provider.to_dict(),
        "required_env": ["SSO_ISSUER_URL", "SSO_CLIENT_ID", "SSO_REDIRECT_URI"],
        "forbidden_values": ["client_secret", "private_key", "real token"],
        "steps": ["review provider metadata", "configure redirect URI", "map groups to roles", "run access review"],
        "mutate_provider": False,
    }

def scim_mapping_plan() -> dict:
    blocked = [m.to_dict() for m in SCIM_MAPPINGS if m.status == "blocked"]
    return {"dry_run": True, "mappings": scim_mapping_drafts(), "blocked": blocked, "write_to_idp": False, "requires_review": True}

def access_review_summary(execute: bool = False) -> dict:
    queue = access_review_queue(execute)
    pending = [r for r in queue if r["decision"] == "pending"]
    high_risk = [r for r in queue if r["risk"] in {"high", "critical"}]
    return {"total": len(queue), "pending": len(pending), "high_risk": len(high_risk), "queue": queue, "apply_changes": False, "requires_review": True}

def role_assignment_review(subject_ref="usr_admin", new_role="reviewer") -> dict:
    valid_roles = {"owner","admin","operator","reviewer","viewer","auditor","root","service","user"}
    blocked = []
    if new_role not in valid_roles: blocked.append("invalid requested role")
    if subject_ref == "usr_owner" and new_role != "owner": blocked.append("owner downgrade requires explicit manual approval")
    return {"dry_run": True, "subject_ref": subject_ref, "requested_role": new_role, "allowed": not blocked, "blocked": blocked, "apply_role_change": False}

def identity_evidence_bundle(execute: bool = False) -> dict:
    return {
        "kind": "zai-enterprise-sso-identity-evidence",
        "version": "1.0",
        "providers": identity_provider_plans(),
        "scim_mappings": scim_mapping_drafts(),
        "org_policies": org_policy_registry(),
        "access_reviews": access_review_queue(execute),
        "sso_plan": sso_config_plan(),
        "scim_plan": scim_mapping_plan(),
        "access_summary": access_review_summary(execute),
        "validation": validation_report(),
        "external_mutation": False,
        "requires_review": True,
    }

def write_identity_evidence(root=".", out="identity/evidence/identity-evidence.json", execute: bool = False) -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(identity_evidence_bundle(execute), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)

def write_identity_report(root=".", out="identity/reports/identity-center-report.md", execute: bool = False) -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    providers = "\n".join(f"- {p.name} [{p.provider_type} / {p.protocol} / {p.status}]" for p in PROVIDERS)
    reviews = "\n".join(f"- {r.get('subject_ref')} on {r.get('resource')}: {r.get('role')} [{r.get('risk')} / {r.get('decision')}]" for r in access_review_queue(execute))
    path.write_text(f"# Enterprise SSO and Identity Center Report\n\n## Providers\n\n{providers}\n\n## Access Reviews\n\n{reviews}\n\n## Safety\n\n- Config examples only.\n- No real IdP secrets.\n- No live identity provider mutation.\n", encoding="utf-8")
    return str(path)

def identity_status():
    return {"ok": True, "systems": ["identity_dashboard","sso_config_planner","scim_mapping_drafts","org_policy_registry","access_review_queue","role_assignment_review","identity_evidence","dashboard_routes"]}

def identity_overview(execute: bool = False):
    return {"status": identity_status(), "providers": identity_provider_plans(), "scim": scim_mapping_drafts(), "policies": org_policy_registry(), "access": access_review_summary(execute), "validation": validation_report()}

def identity_demo(root=".", execute: bool = False):
    evidence_path = write_identity_evidence(root, execute=execute)
    report_path = write_identity_report(root, execute=execute)
    return {"evidence_path": evidence_path, "report_path": report_path, "sso_plan": sso_config_plan(), "role_review": role_assignment_review(), "bundle": identity_evidence_bundle(execute)}
