from zai_coder.backup_restore_disaster_recovery.routes import (
    route_dr_page, route_dr_backups_page, route_dr_restore_drills_page,
    route_dr_rpo_rto_page, route_dr_evidence_page,
)
render_dr_overview_page = lambda: route_dr_page()["html"]
render_backups_page = lambda: route_dr_backups_page()["html"]
render_restore_drills_page = lambda: route_dr_restore_drills_page()["html"]
render_rpo_rto_page = lambda: route_dr_rpo_rto_page()["html"]
render_evidence_page = lambda: route_dr_evidence_page()["html"]
