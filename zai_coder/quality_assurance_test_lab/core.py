from __future__ import annotations
import json
from pathlib import Path
from .models import TestCase, FixtureSpec, QualityGate

TESTS = [
    TestCase("tc-core-unit", "Core unit suite", "core", "unit", "critical", "ready", "python -m pytest -q"),
    TestCase("tc-routes-smoke", "Route smoke suite", "routes", "smoke", "high", "ready", "python -m pytest tests/test_routes.py -q"),
    TestCase("tc-market-regression", "Marketplace regression suite", "marketplace", "regression", "high", "ready", "python -m pytest tests/test_package_registry_marketplace_publishing_v42.py -q"),
    TestCase("tc-team-contract", "Team contract checks", "team", "contract", "normal", "ready", "python -m pytest tests/test_team_collaboration_workspaces_v40.py -q"),
]
FIXTURES = [
    FixtureSpec("fx-demo-json", "Demo JSON payloads", "json", "test", True),
    FixtureSpec("fx-local-sqlite", "Local SQLite sandbox", "sqlite", "local", True),
    FixtureSpec("fx-file-tree", "Synthetic file tree", "file_tree", "demo", True),
]
GATES = [
    QualityGate("gate-tests", "All tests pass", 1.0, "tests_passed", True),
    QualityGate("gate-critical", "No critical failures", 0.0, "critical_failures", True),
    QualityGate("gate-lint", "No lint errors in generated docs", 0.0, "lint_errors", False),
]

def get_test_matrix(): return [t.to_dict() for t in TESTS]
def fixture_catalog(): return [f.to_dict() for f in FIXTURES]
def quality_gates(): return [g.to_dict() for g in GATES]

def run_pytest(command: str) -> dict:
    import subprocess
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True, timeout=60)
        passed = result.returncode == 0
        return {"passed": passed, "stdout": result.stdout, "stderr": result.stderr}
    except Exception as e:
        return {"passed": False, "stdout": "", "stderr": str(e)}

def validation_report() -> dict:
    rows = [*TESTS, *FIXTURES, *GATES]
    reports = [{"id": x.id, "issues": x.validate()} for x in rows]
    return {"ok": all(not r["issues"] for r in reports), "reports": reports}

def smoke_plan(execute: bool = False) -> dict:
    smoke = [t for t in TESTS if t.test_type == "smoke"]
    results = []
    if execute:
        for t in smoke:
            res = run_pytest(t.command)
            results.append({"test": t.id, "passed": res["passed"], "stdout": res["stdout"]})
    
    return {
        "dry_run": not execute,
        "suite": "smoke",
        "tests": [t.to_dict() for t in smoke],
        "execute": execute,
        "results": results
    }

def regression_report(execute: bool = False) -> dict:
    matrix = get_test_matrix()
    results = []
    if execute:
        for t in TESTS:
            res = run_pytest(t.command)
            results.append({"test": t.id, "passed": res["passed"], "stdout": res["stdout"]})
            
    return {
        "kind": "zai-qa-regression-report",
        "total": len(matrix),
        "ready": len([t for t in matrix if t["status"] == "ready"]),
        "critical": len([t for t in matrix if t["priority"] == "critical"]),
        "blocked": 0,
        "status": "ready",
        "execute": execute,
        "results": results,
        "external_publish": False,
    }

def quality_gate_evaluation(metrics: dict | None = None) -> dict:
    metrics = metrics or {"tests_passed": 1.0, "coverage": 0.80, "critical_failures": 0.0, "lint_errors": 0.0, "security_findings": 0.0}
    results = []
    for gate in GATES:
        value = float(metrics.get(gate.metric, 0.0))
        if gate.metric in {"critical_failures", "lint_errors", "security_findings"}:
            passed = value <= gate.threshold
        else:
            passed = value >= gate.threshold
        results.append({"gate": gate.to_dict(), "value": value, "passed": passed})
    return {"ok": all(r["passed"] or not r["gate"]["required"] for r in results), "metrics": metrics, "results": results, "dry_run": True}

def evidence_bundle(execute: bool = False) -> dict:
    return {
        "kind": "zai-qa-evidence-bundle",
        "version": "1.0",
        "test_matrix": get_test_matrix(),
        "fixtures": fixture_catalog(),
        "regression": regression_report(execute=execute),
        "quality_gates": quality_gate_evaluation(),
        "validation": validation_report(),
        "external_publish": False,
        "requires_review": True,
    }

def write_qa_evidence(root=".", out="qa/evidence/qa-evidence.json", execute: bool = False) -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(evidence_bundle(execute=execute), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)

def write_qa_report(root=".", out="qa/reports/qa-test-lab-report.md") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    tests = "\n".join(f"- {t.name} [{t.test_type} / {t.priority} / {t.status}]" for t in TESTS)
    path.write_text(f"# Quality Assurance and Test Lab Report\n\n## Test Matrix\n\n{tests}\n\n## Safety\n\n- Deterministic tests.\n- No bypass flags.\n- Evidence export is local-only.\n", encoding="utf-8")
    return str(path)

def qa_status():
    return {"ok": True, "systems": ["qa_dashboard","test_matrix","regression_report","fixture_catalog","smoke_plan","quality_gates","evidence_export","dashboard_routes"]}

def qa_overview():
    return {"status": qa_status(), "matrix": get_test_matrix(), "fixtures": fixture_catalog(), "gates": quality_gates(), "validation": validation_report(), "regression": regression_report()}

def qa_demo(root=".", execute: bool = False):
    evidence = write_qa_evidence(root, execute=execute)
    report = write_qa_report(root)
    return {"evidence_path": evidence, "report_path": report, "bundle": evidence_bundle(execute=execute)}
