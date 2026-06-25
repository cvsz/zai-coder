from zai_coder.security_operations_threat_monitoring.routes import (
    route_security_ops_page, route_security_signals_page, route_security_alerts_page,
    route_security_incidents_page, route_security_evidence_page,
)
render_security_overview_page = lambda: route_security_ops_page()["html"]
render_signals_page = lambda: route_security_signals_page()["html"]
render_alerts_page = lambda: route_security_alerts_page()["html"]
render_incidents_page = lambda: route_security_incidents_page()["html"]
render_evidence_page = lambda: route_security_evidence_page()["html"]
