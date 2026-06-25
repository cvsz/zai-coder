from zai_coder.final_enterprise_release_pack.routes import route_final_release_page, route_final_docs_page, route_final_dashboards_page, route_final_validation_page, route_final_go_live_page
render_final_release_page = lambda: route_final_release_page()["html"]
render_final_docs_page = lambda: route_final_docs_page()["html"]
render_final_dashboards_page = lambda: route_final_dashboards_page()["html"]
render_final_validation_page = lambda: route_final_validation_page()["html"]
render_final_go_live_page = lambda: route_final_go_live_page()["html"]
