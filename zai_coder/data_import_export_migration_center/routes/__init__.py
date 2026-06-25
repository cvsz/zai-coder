from zai_coder.data_import_export_migration_center.core import *

def route_migration_status(): return migration_status()
def route_migration_overview(): return migration_overview()
def route_import_plan(): return import_plan()
def route_export_plan(): return export_plan()
def route_schema_check(): return schema_compatibility_check()
def route_mapping_catalog(): return {"mappings": mapping_catalog()}
def route_rollback_preview(): return rollback_preview()
def route_migration_export(): return {"export_path": write_migration_export("."), "report_path": write_migration_report(".")}
def route_migration_demo(): return migration_demo(".")
def route_migration_page(): return {"content_type":"text/html","html":"<h1>Data Import Export and Migration Center</h1>"}
def route_migration_import_page(): return {"content_type":"text/html","html":"<h1>Import Plan</h1>"}
def route_migration_export_page(): return {"content_type":"text/html","html":"<h1>Export Plan</h1>"}
def route_migration_schema_page(): return {"content_type":"text/html","html":"<h1>Schema Compatibility</h1>"}
def route_migration_rollback_page(): return {"content_type":"text/html","html":"<h1>Rollback Preview</h1>"}
