from pathlib import Path
from zai_coder.quality_assurance_test_lab.models import TestCase as QATestCase, FixtureSpec, QualityGate
from zai_coder.quality_assurance_test_lab.core import get_test_matrix, fixture_catalog, quality_gates, validation_report, smoke_plan, regression_report, quality_gate_evaluation, evidence_bundle, write_qa_evidence, write_qa_report, qa_demo, run_pytest
from zai_coder.quality_assurance_test_lab.routes import *

def test_models_validation():
    assert QATestCase("t","Name","suite").validate() == []
    assert QATestCase("","","", test_type="bad", priority="bad", status="bad", command="pytest --no-verify").validate()
    assert FixtureSpec("f","Fixture","json").validate() == []
    assert FixtureSpec("","","bad", scope="bad", safe=False).validate()
    assert QualityGate("g","Gate",1.0,"tests_passed").validate() == []
    assert QualityGate("","","-1","bad").validate()

def test_core_qa():
    assert get_test_matrix()
    assert fixture_catalog()
    assert quality_gates()
    assert validation_report()["ok"]
    assert smoke_plan()["dry_run"] is True
    assert regression_report()["external_publish"] is False
    assert quality_gate_evaluation()["ok"] is True
    assert evidence_bundle()["requires_review"] is True

def test_run_pytest_preserves_quoted_arguments(monkeypatch):
    calls = []

    class Result:
        returncode = 0
        stdout = "ok"
        stderr = ""

    def fake_run(args, **kwargs):
        calls.append((args, kwargs))
        return Result()

    monkeypatch.setattr("subprocess.run", fake_run)

    result = run_pytest('python -m pytest "tests/path with spaces.py" -q')

    assert result["passed"] is True
    assert calls[0][0] == ["python", "-m", "pytest", "tests/path with spaces.py", "-q"]

def test_exports(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert Path(write_qa_evidence(tmp_path)).exists()
    assert Path(write_qa_report(tmp_path)).exists()
    demo = qa_demo(str(tmp_path))
    assert Path(demo["evidence_path"]).exists()
    assert Path(demo["report_path"]).exists()

def test_routes():
    assert route_qa_status()["ok"]
    assert route_qa_overview()["validation"]["ok"]
    assert route_test_matrix()["validation"]["ok"]
    assert route_regression_report()["status"] == "ready"
    assert route_fixture_catalog()["fixtures"]
    assert route_smoke_plan()["dry_run"]
    assert route_quality_gate()["ok"]
    assert "evidence_path" in route_qa_evidence_export()
    assert "evidence_path" in route_qa_demo()
    assert route_qa_page()["content_type"] == "text/html"
    assert route_qa_matrix_page()["content_type"] == "text/html"
    assert route_qa_regression_page()["content_type"] == "text/html"
    assert route_qa_fixtures_page()["content_type"] == "text/html"
    assert route_qa_gates_page()["content_type"] == "text/html"

def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/qa-test-lab/qa-status.sh",
        "scripts/qa-test-lab/test-matrix.sh",
        "scripts/qa-test-lab/regression-report.sh",
        "scripts/qa-test-lab/fixture-catalog.sh",
        "scripts/qa-test-lab/smoke-plan.sh",
        "scripts/qa-test-lab/quality-gate.sh",
        "scripts/qa-test-lab/qa-evidence-export.sh",
        "scripts/qa-test-lab/qa-demo.sh",
        "scripts/qa-test-lab/qa-dashboard-export.sh",
        "docs/qa-test-lab/QUALITY_ASSURANCE_TEST_LAB_GUIDE.md",
        "docs/qa-test-lab/TEST_MATRIX.md",
        "docs/qa-test-lab/QUALITY_GATES.md",
        "docs/qa-test-lab/FIXTURE_CATALOG.md",
        "docs/qa-test-lab/EVIDENCE_EXPORT_POLICY.md",
        "docs/requirements/NEXT_V43_QUALITY_ASSURANCE_TEST_LAB_REQUIREMENTS.md",
        "assets/qa-test-lab/quality_assurance_test_lab_features.json",
    ]:
        assert (root / rel).exists(), rel
