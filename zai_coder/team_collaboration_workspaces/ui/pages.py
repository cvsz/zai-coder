from zai_coder.team_collaboration_workspaces.routes import (
    route_team_page, route_team_workspaces_page, route_team_members_page,
    route_team_review_queue_page, route_team_activity_page,
)
render_team_overview_page = lambda: route_team_page()["html"]
render_workspaces_page = lambda: route_team_workspaces_page()["html"]
render_members_page = lambda: route_team_members_page()["html"]
render_review_queue_page = lambda: route_team_review_queue_page()["html"]
render_activity_page = lambda: route_team_activity_page()["html"]
