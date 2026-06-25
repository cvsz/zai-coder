from zai_coder.developer_portal_api_docs.core import *

def route_developer_status(): return developer_status()
def route_developer_overview(): return developer_overview()
def route_api_reference(): return {"endpoints": endpoint_registry(), "validation": validation_report()}
def route_openapi_export(): return {"openapi": openapi_spec(), "path": write_openapi_export(".")}
def route_sdk_snippets(): return {"snippets": snippet_registry()}
def route_quickstarts(): return {"quickstarts": quickstart_registry()}
def route_developer_docs_export(): return {"export_path": write_docs_export("."), "report_path": write_developer_report(".")}
def route_developer_demo(): return developer_demo(".")
def route_developer_page(): return {"content_type":"text/html","html":"<h1>Developer Portal and API Docs</h1>"}
def route_developer_api_page(): return {"content_type":"text/html","html":"<h1>API Reference</h1>"}
def route_developer_openapi_page(): return {"content_type":"text/html","html":"<h1>OpenAPI Export</h1>"}
def route_developer_snippets_page(): return {"content_type":"text/html","html":"<h1>SDK Snippets</h1>"}
def route_developer_quickstarts_page(): return {"content_type":"text/html","html":"<h1>Quickstarts</h1>"}
