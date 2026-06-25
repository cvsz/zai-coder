from __future__ import annotations
import json, uuid
from pathlib import Path
from .models import TeamWorkspace, TeamMember, ReviewQueueItem, WorkspaceInvitation

ROLE_PERMISSIONS = {
    "owner": {"workspace:*","review:*","invite:*","audit:view"},
    "admin": {"workspace:view","workspace:manage","review:*","invite:create","audit:view"},
    "operator": {"workspace:view","review:view","review:comment","activity:view"},
    "reviewer": {"workspace:view","review:view","review:approve","review:comment"},
    "viewer": {"workspace:view","activity:view"},
    "auditor": {"workspace:view","audit:view","activity:view"},
}

WORKSPACES = [
    TeamWorkspace("tw_control", "org_local", "Control Plane Team", "private", "active"),
    TeamWorkspace("tw_customer_success", "org_local", "Customer Success", "org", "active"),
    TeamWorkspace("tw_release", "org_local", "Release Review", "private", "active"),
]
MEMBERS = [
    TeamMember("tm_owner", "tw_control", "usr_owner", "owner", "active"),
    TeamMember("tm_admin", "tw_control", "usr_admin", "admin", "active"),
    TeamMember("tm_reviewer", "tw_release", "usr_reviewer", "reviewer", "active"),
    TeamMember("tm_viewer", "tw_customer_success", "usr_viewer", "viewer", "active"),
]
REVIEWS = [
    ReviewQueueItem("rq_v40_manifest", "tw_release", "Review v40 team collaboration manifest", "release", "open", "high", "system"),
    ReviewQueueItem("rq_customer_copy", "tw_customer_success", "Approve onboarding copy update", "content", "in_review", "normal", "usr_admin"),
    ReviewQueueItem("rq_access_review", "tw_control", "Review workspace member roles", "access", "open", "normal", "usr_owner"),
]

def role_matrix(): return {r: sorted(p) for r, p in ROLE_PERMISSIONS.items()}

def role_decision(role: str, permission: str) -> dict:
    perms = ROLE_PERMISSIONS.get(role, set())
    domain = permission.split(":", 1)[0]
    allowed = permission in perms or f"{domain}:*" in perms or "workspace:*" in perms
    return {"allowed": allowed, "role": role, "permission": permission, "permissions": sorted(perms)}

def workspace_directory(): return [w.to_dict() for w in WORKSPACES]
def member_directory(workspace_id=None):
    rows = MEMBERS if not workspace_id else [m for m in MEMBERS if m.workspace_id == workspace_id]
    return [m.to_dict() for m in rows]
def review_queue(workspace_id=None):
    rows = REVIEWS if not workspace_id else [r for r in REVIEWS if r.workspace_id == workspace_id]
    return [r.to_dict() for r in rows]

def validation_report() -> dict:
    rows = [*WORKSPACES, *MEMBERS, *REVIEWS]
    reports = [{"id": x.id, "issues": x.validate()} for x in rows]
    return {"ok": all(not r["issues"] for r in reports), "reports": reports}

def invitation_plan(workspace_id: str, invitee_ref: str, role: str, actor_role: str = "owner") -> dict:
    blocked = []
    if role == "admin" and actor_role != "owner": blocked.append("only owner may invite admin")
    if not role_decision(actor_role, "invite:create")["allowed"] and "invite:*" not in ROLE_PERMISSIONS.get(actor_role, set()):
        blocked.append("actor lacks invite permission")
    inv = WorkspaceInvitation(f"wi_{uuid.uuid4().hex[:12]}", workspace_id, invitee_ref, role)
    blocked += inv.validate()
    return {"dry_run": True, "allowed": not blocked, "blocked": blocked, "invitation": inv.to_dict(), "send_external_invite": False}

def review_decision_plan(item_id: str, actor_role: str, decision: str = "approved") -> dict:
    item = next((i for i in REVIEWS if i.id == item_id), None)
    if not item: raise ValueError(f"unknown review item: {item_id}")
    blocked = []
    if decision not in {"approved","rejected","changes_requested"}: blocked.append("invalid decision")
    if not role_decision(actor_role, "review:approve")["allowed"]: blocked.append("actor lacks review approval permission")
    return {"dry_run": True, "allowed": not blocked, "blocked": blocked, "item": item.to_dict(), "decision": decision}

def activity_summary() -> dict:
    events = []
    for w in workspace_directory(): events.append({"kind":"workspace.status","workspace_id":w["id"],"summary":f"{w['name']} is {w['status']}"})
    for r in review_queue(): events.append({"kind":"review.item","workspace_id":r["workspace_id"],"summary":f"{r['title']} is {r['status']}"})
    counts = {}
    for e in events: counts[e["kind"]] = counts.get(e["kind"],0)+1
    return {"event_count": len(events), "counts": counts, "events": events}

def team_export_bundle() -> dict:
    return {"kind":"zai-team-collaboration-export","version":"1.0","workspaces":workspace_directory(),"members":member_directory(),"review_queue":review_queue(),"activity":activity_summary(),"roles":role_matrix(),"external_publish":False,"requires_review":True}

def write_team_export(root=".", out="team/exports/team-collaboration-export.json") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(team_export_bundle(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)

def write_team_report(root=".", out="team/reports/team-collaboration-report.md") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Team Collaboration and Workspaces Report\n\nLocal-first, role-gated, audit-ready collaboration report.\n", encoding="utf-8")
    return str(path)

def team_status():
    return {"ok": True, "systems": ["workspace_registry","member_roles","review_queue","activity_feed","invitation_plans","export_bundle","dashboard_routes"]}

def team_overview():
    return {"status": team_status(), "workspaces": workspace_directory(), "members": member_directory(), "reviews": review_queue(), "validation": validation_report(), "activity": activity_summary(), "roles": role_matrix()}

def team_demo(root="."):
    export_path = write_team_export(root)
    report_path = write_team_report(root)
    return {"export_path": export_path, "report_path": report_path, "invitation": invitation_plan("tw_control","usr_new","reviewer"), "review": review_decision_plan("rq_v40_manifest","reviewer"), "bundle": team_export_bundle()}
