from zai_coder.package_registry_marketplace_publishing.core import *

def route_marketplace_status(): return marketplace_status()
def route_marketplace_overview(): return marketplace_overview()
def route_package_catalog(): return {"packages": package_catalog(), "validation": validation_report()}
def route_marketplace_submission(): return marketplace_submission_draft("pkg-market-v42")
def route_publishing_checklist(): return publishing_checklist("pkg-market-v42")
def route_package_validation(): return package_validation_policy("pkg-market-v42")
def route_compatibility_matrix(): return {"compatibility": compatibility_matrix()}
def route_license_attribution(): return {"licenses": license_attribution_report()}
def route_marketplace_export(): return {"export_path": write_marketplace_export("."), "report_path": write_marketplace_report(".")}
def route_marketplace_demo(): return marketplace_demo(".")
def route_marketplace_page(): return {"content_type":"text/html","html":"<h1>Package Registry and Marketplace Publishing</h1>"}
def route_marketplace_packages_page(): return {"content_type":"text/html","html":"<h1>Packages</h1>"}
def route_marketplace_submissions_page(): return {"content_type":"text/html","html":"<h1>Marketplace Submissions</h1>"}
def route_marketplace_validation_page(): return {"content_type":"text/html","html":"<h1>Package Validation</h1>"}
def route_marketplace_checklist_page(): return {"content_type":"text/html","html":"<h1>Publishing Checklist</h1>"}
