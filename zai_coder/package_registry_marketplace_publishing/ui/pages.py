from zai_coder.package_registry_marketplace_publishing.routes import (
    route_marketplace_page, route_marketplace_packages_page, route_marketplace_submissions_page,
    route_marketplace_validation_page, route_marketplace_checklist_page,
)
render_marketplace_overview_page = lambda: route_marketplace_page()["html"]
render_packages_page = lambda: route_marketplace_packages_page()["html"]
render_submissions_page = lambda: route_marketplace_submissions_page()["html"]
render_validation_page = lambda: route_marketplace_validation_page()["html"]
render_checklist_page = lambda: route_marketplace_checklist_page()["html"]
