from zai_coder.security_operations_threat_monitoring.core import *

def route_security_ops_status(): return security_ops_status()
def route_security_ops_overview(): return security_ops_overview()
def route_threat_signals(): return {"signals": threat_signal_registry(), "risk": risk_scorecard()}
def route_policy_alerts(): return {"alerts": policy_alert_catalog(), "queue": alert_review_queue()}
def route_incident_workflow_plan(): return incident_workflow_plan()
def route_security_evidence_export(): return {"evidence_path": write_security_evidence("."), "report_path": write_security_report(".")}
def route_security_ops_demo(): return security_ops_demo(".")
def route_security_ops_page(): return {"content_type":"text/html","html":"<h1>Security Operations and Threat Monitoring</h1>"}
def route_security_signals_page(): return {"content_type":"text/html","html":"<h1>Threat Signals</h1>"}
def route_security_alerts_page(): return {"content_type":"text/html","html":"<h1>Policy Alerts</h1>"}
def route_security_incidents_page(): return {"content_type":"text/html","html":"<h1>Incident Workflow Plans</h1>"}
def route_security_evidence_page(): return {"content_type":"text/html","html":"<h1>Security Evidence</h1>"}
