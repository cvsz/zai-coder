from zai_coder.quality_assurance_test_lab.core import *

def route_qa_status(): return qa_status()
def route_qa_overview(): return qa_overview()
def route_test_matrix(): return {"matrix": get_test_matrix(), "validation": validation_report()}
def route_regression_report(): return regression_report()
def route_fixture_catalog(): return {"fixtures": fixture_catalog()}
def route_smoke_plan(): return smoke_plan()
def route_quality_gate(): return quality_gate_evaluation()
def route_qa_evidence_export(): return {"evidence_path": write_qa_evidence("."), "report_path": write_qa_report(".")}
def route_qa_demo(): return qa_demo(".")
def route_qa_page(): return {"content_type":"text/html","html":"<h1>Quality Assurance and Test Lab</h1>"}
def route_qa_matrix_page(): return {"content_type":"text/html","html":"<h1>Test Matrix</h1>"}
def route_qa_regression_page(): return {"content_type":"text/html","html":"<h1>Regression Report</h1>"}
def route_qa_fixtures_page(): return {"content_type":"text/html","html":"<h1>Fixture Catalog</h1>"}
def route_qa_gates_page(): return {"content_type":"text/html","html":"<h1>Quality Gates</h1>"}
