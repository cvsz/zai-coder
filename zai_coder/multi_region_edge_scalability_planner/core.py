from __future__ import annotations
import json
from pathlib import Path
from .models import RegionSpec, EdgeRoutePlan, CapacityModel, LatencyBudget, ScalingScenario

REGIONS = [
    RegionSpec("reg_bkk", "Bangkok Primary", "ap-southeast-th", "primary", "review", "allowed"),
    RegionSpec("reg_sgp", "Singapore Secondary", "ap-southeast-1", "secondary", "review", "allowed"),
    RegionSpec("reg_tok", "Tokyo Edge", "ap-northeast-1", "edge", "planned", "review"),
    RegionSpec("reg_eu", "EU Standby", "eu-west-1", "standby", "planned", "restricted"),
]

ROUTES = [
    EdgeRoutePlan("route_www", "www.zeaz.dev", "latency", "reg_bkk", "reg_sgp", "review", True),
    EdgeRoutePlan("route_api", "api.zeaz.dev", "failover", "reg_bkk", "reg_sgp", "review", True),
    EdgeRoutePlan("route_docs", "docs.zeaz.dev", "geo", "reg_sgp", "reg_tok", "draft", True),
]

CAPACITY = [
    CapacityModel("cap_api", "api-gateway", 100, 500, 40, "review"),
    CapacityModel("cap_workers", "worker-orchestration", 50, 250, 50, "draft"),
    CapacityModel("cap_docs", "developer-portal", 25, 150, 30, "review"),
]

LATENCY = [
    LatencyBudget("lat_th", "Thailand", 120, 95, "met"),
    LatencyBudget("lat_sg", "Singapore", 120, 80, "met"),
    LatencyBudget("lat_jp", "Japan", 180, 165, "planned"),
    LatencyBudget("lat_eu", "EU", 250, 260, "at_risk"),
]

SCENARIOS = [
    ScalingScenario("scale_spike", "Traffic spike during launch", "traffic_spike", "high", True),
    ScalingScenario("scale_failover", "Primary region failover drill", "region_failover", "critical", True),
    ScalingScenario("scale_cache", "Edge cache pressure review", "edge_cache_pressure", "medium", True),
    ScalingScenario("scale_queue", "Queue backlog recovery plan", "queue_backlog", "high", True),
]

def region_topology(): return [r.to_dict() for r in REGIONS]
def edge_routing_plans(): return [r.to_dict() for r in ROUTES]
def capacity_models(): return [c.to_dict() for c in CAPACITY]
def latency_budgets(): return [l.to_dict() for l in LATENCY]
def scaling_scenarios(): return [s.to_dict() for s in SCENARIOS]

def validation_report() -> dict:
    rows = [*REGIONS, *ROUTES, *CAPACITY, *LATENCY, *SCENARIOS]
    reports = [{"id": x.id, "issues": x.validate()} for x in rows]
    return {"ok": all(not r["issues"] for r in reports), "reports": reports}

def topology_plan() -> dict:
    return {"dry_run": True, "regions": region_topology(), "primary": "reg_bkk", "secondary": ["reg_sgp"], "edge": ["reg_tok"], "apply_infra": False}

def edge_routing_plan(route_id="route_api") -> dict:
    route = next((r for r in ROUTES if r.id == route_id), None)
    if not route: raise ValueError(f"unknown route: {route_id}")
    return {"dry_run": True, "route": route.to_dict(), "steps": ["review DNS target", "review health checks", "review fallback", "write route evidence"], "apply_dns": False, "apply_cloudflare": False}

def capacity_forecast() -> dict:
    rows = []
    for item in CAPACITY:
        required = int(item.peak_rps * (1 + item.headroom_percent / 100))
        rows.append({"id": item.id, "service": item.service, "peak_rps": item.peak_rps, "headroom_percent": item.headroom_percent, "required_rps": required, "status": item.status})
    return {"dry_run": True, "models": rows, "requires_review": True}

def latency_budget_report() -> dict:
    rows = []
    for item in LATENCY:
        delta = item.p95_ms - item.target_ms
        rows.append({**item.to_dict(), "delta_ms": delta, "within_budget": delta <= 0})
    return {"dry_run": True, "budgets": rows, "at_risk": [r for r in rows if not r["within_budget"]]}

def region_readiness_checklist() -> dict:
    items = [
        {"id": "dns", "title": "DNS routing plan reviewed", "done": True},
        {"id": "health", "title": "Health checks designed", "done": True},
        {"id": "capacity", "title": "Capacity forecast reviewed", "done": True},
        {"id": "residency", "title": "Data residency reviewed", "done": False},
        {"id": "manual-approval", "title": "Manual approval before infra changes", "done": False},
    ]
    return {"dry_run": True, "items": items, "ready": all(i["done"] for i in items), "apply_changes": False}

def scaling_scenario_plan(scenario_id="scale_spike") -> dict:
    scenario = next((s for s in SCENARIOS if s.id == scenario_id), None)
    if not scenario: raise ValueError(f"unknown scenario: {scenario_id}")
    return {"dry_run": True, "scenario": scenario.to_dict(), "steps": ["estimate load", "review cache posture", "review queue limits", "review fallback region", "write scenario evidence"], "execute_scaling": False}

def scalability_evidence_bundle() -> dict:
    return {
        "kind": "zai-multi-region-edge-scalability-evidence",
        "version": "1.0",
        "regions": region_topology(),
        "routes": edge_routing_plans(),
        "capacity": capacity_forecast(),
        "latency": latency_budget_report(),
        "scenarios": scaling_scenarios(),
        "readiness": region_readiness_checklist(),
        "validation": validation_report(),
        "external_apply": False,
        "requires_review": True,
    }

def write_scalability_export(root=".", out="scalability/evidence/scalability-evidence.json") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(scalability_evidence_bundle(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)

def write_scalability_report(root=".", out="scalability/reports/scalability-planner-report.md") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    regions = "\n".join(f"- {r.name} [{r.region_code} / {r.role} / {r.status}]" for r in REGIONS)
    routes = "\n".join(f"- {r.hostname}: {r.strategy} {r.primary_region}->{r.fallback_region or 'none'}" for r in ROUTES)
    path.write_text(f"# Multi Region Edge and Scalability Planner Report\n\n## Regions\n\n{regions}\n\n## Routes\n\n{routes}\n\n## Safety\n\n- Planning-only.\n- No infrastructure apply.\n- No production routing changes.\n", encoding="utf-8")
    return str(path)

def scalability_status():
    return {"ok": True, "systems": ["region_topology","edge_routing_plans","capacity_models","latency_budgets","scaling_scenarios","readiness_checklist","evidence_export","dashboard_routes"]}

def scalability_overview():
    return {"status": scalability_status(), "topology": topology_plan(), "routes": edge_routing_plans(), "capacity": capacity_forecast(), "latency": latency_budget_report(), "readiness": region_readiness_checklist(), "validation": validation_report()}

def scalability_demo(root="."):
    export_path = write_scalability_export(root)
    report_path = write_scalability_report(root)
    return {"export_path": export_path, "report_path": report_path, "route_plan": edge_routing_plan(), "scenario_plan": scaling_scenario_plan(), "bundle": scalability_evidence_bundle()}
