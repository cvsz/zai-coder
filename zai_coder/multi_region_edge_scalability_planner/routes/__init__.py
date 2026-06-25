from zai_coder.multi_region_edge_scalability_planner.core import *

def route_scalability_status(): return scalability_status()
def route_scalability_overview(): return scalability_overview()
def route_region_topology(): return topology_plan()
def route_edge_routing_plan(): return edge_routing_plan()
def route_capacity_model(): return capacity_forecast()
def route_latency_budget(): return latency_budget_report()
def route_scaling_scenarios(): return {"scenarios": scaling_scenarios(), "plan": scaling_scenario_plan()}
def route_region_readiness(): return region_readiness_checklist()
def route_scalability_export(): return {"export_path": write_scalability_export("."), "report_path": write_scalability_report(".")}
def route_scalability_demo(): return scalability_demo(".")
def route_scalability_page(): return {"content_type":"text/html","html":"<h1>Multi Region Edge and Scalability Planner</h1>"}
def route_scalability_regions_page(): return {"content_type":"text/html","html":"<h1>Region Topology</h1>"}
def route_scalability_edge_page(): return {"content_type":"text/html","html":"<h1>Edge Routing Plans</h1>"}
def route_scalability_capacity_page(): return {"content_type":"text/html","html":"<h1>Capacity Models</h1>"}
def route_scalability_scenarios_page(): return {"content_type":"text/html","html":"<h1>Scaling Scenarios</h1>"}
