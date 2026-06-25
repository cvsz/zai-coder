from zai_coder.data_import_export_migration_center.routes import (
    route_migration_page, route_migration_import_page, route_migration_export_page,
    route_migration_schema_page, route_migration_rollback_page,
)
render_migration_overview_page = lambda: route_migration_page()["html"]
render_import_page = lambda: route_migration_import_page()["html"]
render_export_page = lambda: route_migration_export_page()["html"]
render_schema_page = lambda: route_migration_schema_page()["html"]
render_rollback_page = lambda: route_migration_rollback_page()["html"]
