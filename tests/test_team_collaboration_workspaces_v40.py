from pathlib import Path
from zai_coder.team_collaboration_workspaces.models import TeamWorkspace, TeamMember, ReviewQueueItem, WorkspaceInvitation
from zai_coder.team_collaboration_workspaces.core import *
from zai_coder.team_collaboration_workspaces.routes import *

def test_models_validation():
    assert TeamWorkspace("w","o","Workspace").validate() == []
    assert TeamWorkspace("","","", visibility="bad", status="bad").validate()
    assert TeamMember("m","w","u").validate() == []
    assert TeamMember("","","", role="bad", status="bad").validate()
    assert ReviewQueueItem("r","w","Review").validate() == []
    assert ReviewQueueItem("","","", item_type="bad", status="bad", priority="bad").validate()
    assert WorkspaceInvitation("i","w","u").validate() == []
    assert WorkspaceInvitation("","","", role="bad", status="bad", dry_run=False).validate()

def test_core_logic():
    assert role_decision("owner", "workspace:manage")["allowed"]
    assert not role_decision("viewer", "review:approve")["allowed"]
    assert validation_report()["ok"]
    assert workspace_directory()
    assert member_directory()
    assert review_queue()
    assert activity_summary()["event_count"] >= 1
    assert invitation_plan("tw_control","usr_new","reviewer")["allowed"]
    assert not invitation_plan("tw_control","usr_new","admin","viewer")["allowed"]
    assert review_decision_plan("rq_v40_manifest","reviewer")["allowed"]
    assert not review_decision_plan("rq_v40_manifest","viewer")["allowed"]

def test_export_and_demo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert Path(write_team_export(tmp_path)).exists()
    assert Path(write_team_report(tmp_path)).exists()
    demo = team_demo(str(tmp_path))
    assert Path(demo["export_path"]).exists()
    assert demo["bundle"]["external_publish"] is False

def test_routes_and_pages():
    assert route_team_status()["ok"]
    assert route_team_overview()["status"]["ok"]
    assert route_team_workspaces()["validation"]["ok"]
    assert route_team_members()["roles"]["owner"]
    assert route_team_review_queue()["decision"]["allowed"]
    assert route_team_activity()["event_count"] >= 1
    assert route_team_invitation()["send_external_invite"] is False
    assert route_team_page()["content_type"] == "text/html"
    assert route_team_workspaces_page()["content_type"] == "text/html"
    assert route_team_members_page()["content_type"] == "text/html"
    assert route_team_review_queue_page()["content_type"] == "text/html"
    assert route_team_activity_page()["content_type"] == "text/html"

def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/team-collaboration/team-status.sh",
        "scripts/team-collaboration/workspace-directory.sh",
        "scripts/team-collaboration/team-members.sh",
        "scripts/team-collaboration/review-queue.sh",
        "scripts/team-collaboration/collaboration-activity.sh",
        "scripts/team-collaboration/workspace-invite-plan.sh",
        "scripts/team-collaboration/team-demo.sh",
        "scripts/team-collaboration/team-export.sh",
        "scripts/team-collaboration/team-dashboard-export.sh",
        "docs/team-collaboration/TEAM_COLLABORATION_WORKSPACES_GUIDE.md",
        "docs/requirements/NEXT_V40_TEAM_COLLABORATION_WORKSPACES_REQUIREMENTS.md",
        "assets/team-collaboration/team_collaboration_workspaces_features.json",
    ]:
        assert (root / rel).exists(), rel
