from zai_coder.enterprise_sso_identity_center.core import *

def route_identity_status(): return identity_status()
def route_identity_overview(): return identity_overview()
def route_sso_plan(): return sso_config_plan()
def route_scim_mapping_draft(): return scim_mapping_plan()
def route_org_policy(): return {"policies": org_policy_registry()}
def route_access_review(): return access_review_summary()
def route_role_assignment_review(): return role_assignment_review()
def route_identity_evidence_export(): return {"evidence_path": write_identity_evidence("."), "report_path": write_identity_report(".")}
def route_identity_demo(): return identity_demo(".")
def route_identity_page(): return {"content_type":"text/html","html":"<h1>Enterprise SSO and Identity Center</h1>"}
def route_identity_sso_page(): return {"content_type":"text/html","html":"<h1>SSO Plan</h1>"}
def route_identity_scim_page(): return {"content_type":"text/html","html":"<h1>SCIM Mapping Drafts</h1>"}
def route_identity_policies_page(): return {"content_type":"text/html","html":"<h1>Organization Policies</h1>"}
def route_identity_access_review_page(): return {"content_type":"text/html","html":"<h1>Access Review</h1>"}
