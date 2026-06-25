from pathlib import Path
from zai_coder.multi_region_edge_scalability_planner.models import RegionSpec, EdgeRoutePlan, CapacityModel, LatencyBudget, ScalingScenario
from zai_coder.multi_region_edge_scalability_planner.core import *
from zai_coder.multi_region_edge_scalability_planner.routes import *

def test_models_validation():
    assert RegionSpec("r","Region","code").validate() == []
    assert RegionSpec("","","", role="bad", status="bad", data_residency="bad").validate()
    assert EdgeRoutePlan("e","www.example.invalid","latency","reg").validate() == []
    assert EdgeRoutePlan("","","bad","", status="bad", dry_run=False).validate()
    assert CapacityModel("c","svc",10,100).validate() == []
    assert CapacityModel("","",-1,"bad", status="bad").validate()
    assert LatencyBudget("l","TH",100,90).validate() == []
    assert LatencyBudget("","",-1,"bad", status="bad").validate()
    assert ScalingScenario("s","Scenario","traffic_spike").validate() == []
    assert ScalingScenario("","","bad", severity="bad", dry_run=False).validate()

def test_core_scalability():
    assert region_topology()
    assert edge_routing_plans()
    assert capacity_models()
    assert latency_budgets()
    assert scaling_scenarios()
    assert validation_report()["ok"]
    assert topology_plan()["apply_infra"] is False
    assert edge_routing_plan()["apply_cloudflare"] is False
    assert capacity_forecast()["requires_review"] is True
    assert latency_budget_report()["dry_run"]
    assert region_readiness_checklist()["apply_changes"] is False
    assert scaling_scenario_plan()["execute_scaling"] is False
    assert scalability_evidence_bundle()["external_apply"] is False

def test_exports(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert Path(write_scalability_export(tmp_path)).exists()
    assert Path(write_scalability_report(tmp_path)).exists()
    demo = scalability_demo(str(tmp_path))
    assert Path(demo["export_path"]).exists()
    assert Path(demo["report_path"]).exists()

def test_routes():
    assert route_scalability_status()["ok"]
    assert route_scalability_overview()["validation"]["ok"]
    assert route_region_topology()["apply_infra"] is False
    assert route_edge_routing_plan()["apply_dns"] is False
    assert route_capacity_model()["requires_review"]
    assert route_latency_budget()["dry_run"]
    assert route_scaling_scenarios()["plan"]["execute_scaling"] is False
    assert route_region_readiness()["apply_changes"] is False
    assert "export_path" in route_scalability_export()
    assert "export_path" in route_scalability_demo()
    assert route_scalability_page()["content_type"] == "text/html"
    assert route_scalability_regions_page()["content_type"] == "text/html"
    assert route_scalability_edge_page()["content_type"] == "text/html"
    assert route_scalability_capacity_page()["content_type"] == "text/html"
    assert route_scalability_scenarios_page()["content_type"] == "text/html"

def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/scalability-planner/scalability-status.sh",
        "scripts/scalability-planner/region-topology.sh",
        "scripts/scalability-planner/edge-routing-plan.sh",
        "scripts/scalability-planner/capacity-model.sh",
        "scripts/scalability-planner/latency-budget.sh",
        "scripts/scalability-planner/scaling-scenarios.sh",
        "scripts/scalability-planner/region-readiness.sh",
        "scripts/scalability-planner/scalability-export.sh",
        "scripts/scalability-planner/scalability-demo.sh",
        "scripts/scalability-planner/scalability-dashboard-export.sh",
        "docs/scalability-planner/MULTI_REGION_EDGE_SCALABILITY_PLANNER_GUIDE.md",
        "docs/scalability-planner/REGION_TOPOLOGY.md",
        "docs/scalability-planner/EDGE_ROUTING_POLICY.md",
        "docs/scalability-planner/CAPACITY_MODEL.md",
        "docs/scalability-planner/LATENCY_BUDGETS.md",
        "docs/scalability-planner/SCALING_SCENARIOS.md",
        "docs/requirements/NEXT_V48_MULTI_REGION_EDGE_SCALABILITY_PLANNER_REQUIREMENTS.md",
        "assets/scalability-planner/multi_region_edge_scalability_features.json",
    ]:
        assert (root / rel).exists(), rel
