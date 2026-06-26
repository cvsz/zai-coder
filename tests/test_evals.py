from zai_coder.evals.cases import CaseLoader, EvalCase
from zai_coder.evals.runner import EvalRunner
from zai_coder.evals.report import EvalReporter

def test_eval_case():
    c = EvalCase("1", "test", expect_blocked=True)
    assert c.id == "1"
    assert c.expect_blocked is True

def test_case_loader(tmp_path):
    assets = tmp_path / "assets" / "evals"
    assets.mkdir(parents=True)
    f = assets / "safety.json"
    f.write_text('[{"id":"1", "prompt":"rm -rf", "expect_blocked":true}]')
    
    loader = CaseLoader(tmp_path)
    cases = loader.load_suite("safety")
    assert len(cases) == 1
    assert cases[0].id == "1"

def test_eval_runner_and_report():
    runner = EvalRunner(".")
    c = EvalCase("1", "test", expect_blocked=True)
    res = runner.run_suite([c])
    assert len(res) == 1
    assert res[0]["blocked_dangerous_commands"] == 1
    
    report = EvalReporter(res)
    assert report.pass_count == 1
    assert report.blocked == 1
    md = report.to_markdown()
    assert "Pass Count**: 1" in md
