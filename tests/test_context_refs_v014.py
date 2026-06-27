from zai_coder.core.safety import SafetyPolicy
from zai_coder.core.context_refs import ContextReferenceParser

def test_context_ref_file(tmp_path):
    safety = SafetyPolicy()
    parser = ContextReferenceParser(tmp_path, safety)
    
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello Ref")
    
    res = parser.resolve_references("Please read @file:test.txt and tell me")
    assert "@file:test.txt" in res
    assert res["@file:test.txt"] == "Hello Ref"

def test_context_ref_dir(tmp_path):
    safety = SafetyPolicy()
    parser = ContextReferenceParser(tmp_path, safety)
    
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "a.txt").write_text("a")
    (sub / "b.txt").write_text("b")
    
    res = parser.resolve_references("What is in @dir:sub?")
    assert "@dir:sub" in res
    assert "a.txt" in res["@dir:sub"]
    assert "b.txt" in res["@dir:sub"]
