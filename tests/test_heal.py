from zai_coder.core.heal import SelfHeal
from zai_coder.core.failure_parser import FailureParser

def test_failure_parser_pytest():
    output = "FAILED tests/test_demo.py::test_fail - AssertionError: msg"
    parser = FailureParser()
    res = parser.parse(output)
    assert len(res) == 1
    assert res[0]["type"] == "pytest"
    assert res[0]["file"] == "tests/test_demo.py"

def test_failure_parser_compile():
    output = "Compiling 'bad.py'...\nSyntaxError: invalid syntax"
    parser = FailureParser()
    res = parser.parse(output)
    assert len(res) == 1
    assert res[0]["type"] == "compile"
    assert res[0]["file"] == "bad.py"

def test_self_heal(tmp_path):
    healer = SelfHeal(tmp_path)
    res = healer.analyze_log("FAILED tests/test_demo.py::test_fail - AssertionError")
    plan = healer.generate_plan(res)
    assert "Repair Plan" in plan
    assert "tests/test_demo.py" in plan
