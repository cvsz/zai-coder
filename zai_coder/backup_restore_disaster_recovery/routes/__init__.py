from zai_coder.backup_restore_disaster_recovery.core import *

def route_dr_status(): return dr_status()
def route_dr_overview(): return dr_overview()
def route_backup_plan(): return backup_plan()
def route_restore_drill_preview(): return restore_drill_preview()
def route_rpo_rto_targets(): return {"targets": recovery_targets()}
def route_dr_scenarios(): return {"scenarios": dr_scenarios()}
def route_recovery_evidence(): return {"evidence_path": write_dr_evidence("."), "report_path": write_dr_report(".")}
def route_dr_demo(): return dr_demo(".")
def route_dr_page(): return {"content_type":"text/html","html":"<h1>Backup Restore and Disaster Recovery</h1>"}
def route_dr_backups_page(): return {"content_type":"text/html","html":"<h1>Backup Plans</h1>"}
def route_dr_restore_drills_page(): return {"content_type":"text/html","html":"<h1>Restore Drills</h1>"}
def route_dr_rpo_rto_page(): return {"content_type":"text/html","html":"<h1>RPO RTO Targets</h1>"}
def route_dr_evidence_page(): return {"content_type":"text/html","html":"<h1>Recovery Evidence</h1>"}
