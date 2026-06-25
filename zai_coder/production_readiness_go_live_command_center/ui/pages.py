from zai_coder.production_readiness_go_live_command_center.routes import route_go_live_page, route_go_live_gates_page, route_go_live_checklist_page, route_go_live_command_center_page, route_go_live_rollback_page
render_go_live_overview_page = lambda: route_go_live_page()["html"]
render_gates_page = lambda: route_go_live_gates_page()["html"]
render_checklist_page = lambda: route_go_live_checklist_page()["html"]
render_command_center_page = lambda: route_go_live_command_center_page()["html"]
render_rollback_page = lambda: route_go_live_rollback_page()["html"]
