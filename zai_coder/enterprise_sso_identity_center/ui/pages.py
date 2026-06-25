from zai_coder.enterprise_sso_identity_center.routes import (
    route_identity_page, route_identity_sso_page, route_identity_scim_page,
    route_identity_policies_page, route_identity_access_review_page,
)
render_identity_overview_page = lambda: route_identity_page()["html"]
render_sso_page = lambda: route_identity_sso_page()["html"]
render_scim_page = lambda: route_identity_scim_page()["html"]
render_policies_page = lambda: route_identity_policies_page()["html"]
render_access_review_page = lambda: route_identity_access_review_page()["html"]
