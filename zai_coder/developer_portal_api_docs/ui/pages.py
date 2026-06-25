from zai_coder.developer_portal_api_docs.routes import (
    route_developer_page, route_developer_api_page, route_developer_openapi_page,
    route_developer_snippets_page, route_developer_quickstarts_page,
)
render_developer_overview_page = lambda: route_developer_page()["html"]
render_api_reference_page = lambda: route_developer_api_page()["html"]
render_openapi_page = lambda: route_developer_openapi_page()["html"]
render_snippets_page = lambda: route_developer_snippets_page()["html"]
render_quickstarts_page = lambda: route_developer_quickstarts_page()["html"]
