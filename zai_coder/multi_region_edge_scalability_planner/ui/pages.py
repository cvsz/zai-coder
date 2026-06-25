from zai_coder.multi_region_edge_scalability_planner.routes import (
    route_scalability_page, route_scalability_regions_page, route_scalability_edge_page,
    route_scalability_capacity_page, route_scalability_scenarios_page,
)
render_scalability_overview_page = lambda: route_scalability_page()["html"]
render_regions_page = lambda: route_scalability_regions_page()["html"]
render_edge_page = lambda: route_scalability_edge_page()["html"]
render_capacity_page = lambda: route_scalability_capacity_page()["html"]
render_scenarios_page = lambda: route_scalability_scenarios_page()["html"]
