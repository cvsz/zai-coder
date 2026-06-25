from zai_coder.production_readiness_go_live_command_center.core import *
def route_go_live_status(): return go_live_status()
def route_go_live_overview(): return go_live_overview()
def route_readiness_gates(): return {"gates": readiness_gates(), "scorecard": release_readiness_scorecard()}
def route_go_live_checklist(): return {"checklist": go_live_checklist()}
def route_launch_command_center(): return launch_command_center()
def route_manual_approval_gate(): return manual_approval_gate()
def route_rollback_plan(): return rollback_plan()
def route_launch_evidence_export(): return {"evidence_path": write_launch_evidence("."), "report_path": write_launch_report(".")}
def route_go_live_demo(): return go_live_demo(".")
def route_go_live_page(): return {"content_type":"text/html","html":"<h1>Production Readiness and Go Live Command Center</h1>"}
def route_go_live_gates_page(): return {"content_type":"text/html","html":"<h1>Readiness Gates</h1>"}
def route_go_live_checklist_page(): return {"content_type":"text/html","html":"<h1>Go Live Checklist</h1>"}
def route_go_live_command_center_page(): return {"content_type":"text/html","html":"<h1>Launch Command Center</h1>"}
def route_go_live_rollback_page(): return {"content_type":"text/html","html":"<h1>Rollback Plans</h1>"}
